"""Reel Studio - a small local editor for remaking the inspiration reels with your own clips.

Start it by double-clicking "Start Reel Studio.bat" (or run: python studio.py).
It opens http://localhost:8777 in your browser. Keep the black window open while you edit.
"""
import hashlib, http.server, itertools, json, math, os, queue, re, shutil, subprocess, sys, threading, time, traceback
import urllib.parse, uuid, webbrowser
from array import array
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
# The first copy of Reel Studio lives inside a sorted trip folder (<trip>\Reels\Reel Studio) next to a pre-made clip
# index, library.json. That trip is the built-in "Europe trip" folder. A fresh copy (e.g. cloned from GitHub) has no
# library.json: it starts empty, you add footage folders, and everything it makes stays inside this folder.
LEGACY = os.path.exists(os.path.join(HERE, 'library.json'))
if LEGACY:
    REELS = os.path.dirname(HERE)                  # <trip>\Reels  (exports)
    ROOT = os.path.dirname(REELS)                  # <trip>
else:
    REELS = os.path.join(HERE, 'exports')
    ROOT = HERE
CACHE = os.path.join(HERE, 'cache')
PROXIES = os.path.join(CACHE, 'proxies')
STRIPS = os.path.join(CACHE, 'strips')
TEXTC = os.path.join(CACHE, 'text')
META = os.path.join(CACHE, 'meta')
TMP = os.path.join(CACHE, 'tmp')
PROJECTS = os.path.join(HERE, 'projects')
AUDIO = os.path.join(HERE, 'audio')
INSP = os.path.join(HERE, 'insp')
THUMBS = os.path.join(ROOT, '_Catalogue files', 'thumbs')
FPS, W, H = 30, 1080, 1920
IS_WIN, IS_MAC = sys.platform.startswith('win'), sys.platform == 'darwin'
sys.path.insert(0, HERE)
import fontfind  # noqa: E402  (fonts by Windows name; Mac stand-ins)


def find_ffmpeg():
    """FFmpeg must be callable as 'ffmpeg'. A double-clicked launcher may not see where Homebrew or winget put it,
    so look in the usual places and add the first one found to PATH."""
    if shutil.which('ffmpeg') and shutil.which('ffprobe'):
        return shutil.which('ffmpeg')
    cands = ['/opt/homebrew/bin', '/usr/local/bin', '/opt/local/bin']
    if IS_WIN:
        import glob
        la = os.environ.get('LOCALAPPDATA', '')
        cands = [os.path.join(la, 'Microsoft', 'WinGet', 'Links')] + sorted(
            glob.glob(os.path.join(la, 'Microsoft', 'WinGet', 'Packages', '*FFmpeg*', '*', 'bin')), reverse=True) + [
            r'C:\ffmpeg\bin', os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'ffmpeg', 'bin')]
    for d in cands:
        if os.path.exists(os.path.join(d, 'ffmpeg.exe' if IS_WIN else 'ffmpeg')):
            os.environ['PATH'] = d + os.pathsep + os.environ.get('PATH', '')
            return os.path.join(d, 'ffmpeg')
    return None


def open_in_files(path, select=False):
    """Show a folder (or a file, selected) in Explorer / Finder."""
    try:
        if IS_WIN:
            subprocess.Popen(['explorer', '/select,', path]) if select else os.startfile(path)
        elif IS_MAC:
            subprocess.Popen(['open', '-R', path] if select else ['open', path])
        else:
            subprocess.Popen(['xdg-open', os.path.dirname(path) if select else path])
    except Exception as e:
        print('could not open', path, e, flush=True)


find_ffmpeg()
PORT = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8777
CODE_FILE = os.path.abspath(__file__)
CODE_MTIME = os.path.getmtime(CODE_FILE)
SERVER = None
STOPPING = False


def is_stale():
    """True when studio.py on disk is newer than the code this server is running (it was updated)."""
    try:
        return os.path.getmtime(CODE_FILE) != CODE_MTIME
    except OSError:
        return False


LUTS = os.path.join(CACHE, 'luts')
PHOTO_DIR = os.path.join(CACHE, 'photos')
P_THUMB, P_PREV, P_RAW = (os.path.join(PHOTO_DIR, d) for d in ('thumb', 'prev', 'raw'))
for _d in (PROXIES, STRIPS, TEXTC, META, TMP, PROJECTS, LUTS, P_THUMB, P_PREV, P_RAW, AUDIO, INSP):
    os.makedirs(_d, exist_ok=True)
LOW = getattr(subprocess, 'BELOW_NORMAL_PRIORITY_CLASS', 0) | getattr(subprocess, 'CREATE_NO_WINDOW', 0)

LIB = json.load(open(os.path.join(HERE, 'library.json'), encoding='utf-8')) if LEGACY else []
for _c in LIB:
    _c['col'] = 'europe'
CLIPS = {c['id']: c for c in LIB}
PHOTOS = []                  # filled at start-up by scan_photos()

# =====================================================================================
# Folders ("collections"). With a library.json, its trip is the built-in folder. Every other footage folder is listed
# in collections.json and scanned into cache\collections\<key>.json: every video and photo gets an id (each folder
# has its own block of a million ids), thumbnails and a description from the folder's "_Clip list.csv" when there
# is one. Sub-folders starting with "_" (e.g. "_LRF proxies") and the ones in "skip" are left out.
# =====================================================================================
COLL_FILE = os.path.join(HERE, 'collections.json')
COLL_DIR = os.path.join(CACHE, 'collections')
CTHUMBS = os.path.join(CACHE, 'thumbs')
VIDEO_EXT = ('.mp4', '.mov', '.m4v')
COLLS = {}                   # key -> folder settings
COLL_ITEMS = []              # clips and photos from the extra folders
SCAN = {'state': 'idle', 'key': '', 'name': '', 'done': 0, 'total': 0, 'msg': ''}


def load_collections():
    COLLS.clear()
    if LEGACY:
        COLLS['europe'] = {'key': 'europe', 'name': 'Europe trip', 'root': ROOT, 'out': REELS, 'skip': [], 'base': 0, 'builtin': True}
    try:
        extra = json.load(open(COLL_FILE, encoding='utf-8-sig')) if os.path.exists(COLL_FILE) else []      # -sig: Notepad-safe
    except Exception:
        extra = []
    for e in extra:
        if e.get('key') and e['key'] != 'europe' and os.path.isdir(e.get('root', '')):
            COLLS[e['key']] = {'key': e['key'], 'name': e.get('name') or e['key'], 'root': e['root'],
                               'out': e.get('out') or os.path.join(e['root'], 'Reels'), 'skip': e.get('skip', []), 'base': int(e['base'])}


def save_collections():
    data = [{k: v for k, v in C.items() if k in ('key', 'name', 'root', 'out', 'skip', 'base')} for C in COLLS.values() if not C.get('builtin')]
    with open(COLL_FILE + '.part', 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
    os.replace(COLL_FILE + '.part', COLL_FILE)


load_collections()


def coll_of(cid):
    c = CLIPS.get(int(cid), {})
    return COLLS.get(c.get('col', 'europe')) or COLLS.get('europe') or {'root': ROOT, 'out': REELS}


def is_photo(cid):
    return CLIPS.get(int(cid), {}).get('kind') == 'photo'


def src_path(cid):
    return os.path.join(coll_of(cid)['root'], CLIPS[cid]['p'].replace('/', os.sep))


def lrf_path(cid):
    """DJI's own small preview copy of a clip (.LRF), next to it or in the folder's "_LRF proxies": a much faster
    source for Reel Studio's preview copy and thumbnails than the 4K original."""
    c = CLIPS.get(int(cid))
    if not c or c.get('col', 'europe') == 'europe' or c.get('kind') == 'photo':
        return None
    full = src_path(cid)
    stem = os.path.splitext(os.path.basename(full))[0]
    for p in (os.path.splitext(full)[0] + '.LRF', os.path.join(coll_of(cid)['root'], '_LRF proxies', stem + '.LRF')):
        if os.path.exists(p):
            return p
    return None


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# =====================================================================================
# Text styles and drawing
# =====================================================================================
STYLES = {   # shadow = (r, g, b, alpha), blur = shadow softness, off = shadow offset (all at 1080x1920)
    'lyric':  dict(label='Lyric serif (works for Urdu / Hindi)', font='times.ttf', engine='drawtext', fill=(255, 255, 255, 255),
                   xs=0.86, shadow=(0, 0, 0, 150), blur=6, off=(0, 3)),
    'serif':  dict(label='Serif with emoji', font='times.ttf', fill=(255, 255, 255, 255), xs=0.86, shadow=(0, 0, 0, 90), blur=5, off=(0, 3)),
    'hand':   dict(label='Handwritten', font='segoeprb.ttf', fill=(243, 230, 182, 255), xs=1.0, shadow=(0, 0, 0, 120), blur=4, off=(0, 2)),
    'bold':   dict(label='Bold yellow', font='COOPBL.TTF', fill=(247, 232, 166, 255), xs=1.0, shadow=(60, 35, 0, 130), blur=6, off=(0, 4)),
    'arc':    dict(label='Bold yellow, curved', font='COOPBL.TTF', fill=(247, 232, 166, 255), xs=1.0, shadow=(60, 35, 0, 120), blur=5, off=(0, 3), arc=True),
    'script': dict(label='Gold script', font='VLADIMIR.TTF', fill=(242, 178, 27, 255), xs=1.0, shadow=(0, 0, 0, 70), blur=5, off=(0, 3)),
    'clean':  dict(label='Clean white', font='GOTHIC.TTF', fill=(255, 255, 255, 255), xs=1.0, shadow=(0, 0, 0, 90), blur=5, off=(0, 3)),
    'impact': dict(label='Big white caps', font='impact.ttf', fill=(255, 255, 255, 255), xs=1.0, shadow=(0, 0, 0, 140), blur=6, off=(0, 4)),
    # House party: a plum / cream / gold editorial look, with fonts that come with Windows. "file#Instance" picks a
    # variable-font style; track = extra space between letters (as a share of the size).
    'hp_serif':  dict(label='House party · serif', font='SitkaVF.ttf#Banner', fill=(246, 235, 221, 255), xs=0.86,
                      shadow=(14, 4, 16, 215), blur=9, off=(0, 3)),
    'hp_italic': dict(label='House party · italic', font='SitkaVF-Italic.ttf#Banner Italic', fill=(245, 196, 81, 255), xs=0.88,
                      shadow=(14, 4, 16, 215), blur=9, off=(0, 3)),
    'hp_text':   dict(label='House party · italic text', font='SitkaVF-Italic.ttf#Text Italic', fill=(246, 235, 221, 255), xs=1.0,
                      shadow=(14, 4, 16, 215), blur=8, off=(0, 2)),
    'hp_num':    dict(label='House party · numbers', font='BOOKOSI.TTF', fill=(238, 122, 166, 255), xs=1.0,
                      shadow=(14, 4, 16, 215), blur=9, off=(0, 3)),
    'hp_caps':   dict(label='House party · small caps', font='segoeuisl.ttf', fill=(246, 235, 221, 255), xs=1.0, track=0.26,
                      shadow=(14, 4, 16, 230), blur=6, off=(0, 2)),
    'hp_script': dict(label='House party · script', font='KUNSTLER.TTF', fill=(246, 235, 221, 255), xs=1.0,
                      shadow=(14, 4, 16, 230), blur=8, off=(0, 3)),
}
_fonts = {}
_text_lock = threading.Lock()


def F(name, size):
    """A font by its Windows file name ('file.ttf' or 'file.ttf#Variable Instance'); on a Mac the closest Mac font."""
    return fontfind.load(name, size)


def text_img(text, font, size, fill, xscale=1.0, emoji_font=None, track=0.0):
    """Single line of text (+ colour emoji runs) as a tight RGBA image. track = letter spacing as a share of the size."""
    if emoji_font and not fontfind.available(emoji_font):
        emoji_font = None                        # no colour-emoji font here (e.g. a Mac): emoji use the text font
    if track:
        f = F(font, size)
        gap = size * track
        asc, desc = f.getmetrics()
        wd = int(sum(f.getlength(ch) + gap for ch in text)) + 40
        im = Image.new('RGBA', (wd + 40, asc + desc + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x = 20.0
        for ch in text:
            d.text((x, 20), ch, font=f, fill=fill)
            x += f.getlength(ch) + gap
        bb = im.getbbox()
        if not bb:
            return None
        im = im.crop(bb)
        if xscale != 1.0:
            im = im.resize((max(1, int(im.width * xscale)), im.height), Image.LANCZOS)
        return im
    runs, cur, is_emo = [], '', None
    for ch in text:
        e = emoji_font is not None and (ord(ch) > 0x2500 or ch == '\ufe0f')
        if is_emo is None or e == is_emo:
            cur += ch
        else:
            runs.append((cur, is_emo)); cur = ch
        is_emo = e
    if cur:
        runs.append((cur, is_emo))
    f = F(font, size)
    fe = F(emoji_font, int(size * 0.78)) if emoji_font else None
    asc, desc = f.getmetrics()
    total = sum(int((fe if e else f).getlength(t)) for t, e in runs) + 20
    im = Image.new('RGBA', (total + 40, asc + desc + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 20
    for t, e in runs:
        if e:
            t2 = t.replace('\ufe0f', '')
            d.text((x, 20 + asc - int(size * 0.72)), t2, font=fe, embedded_color=True)
            x += int(fe.getlength(t2))
        else:
            d.text((x, 20), t, font=f, fill=fill)
            x += int(f.getlength(t))
    bb = im.getbbox()
    if not bb:
        return None
    im = im.crop(bb)
    if xscale != 1.0:
        im = im.resize((max(1, int(im.width * xscale)), im.height), Image.LANCZOS)
    return im


def hex_rgba(h):
    return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255)


def drawtext_img(text, fontfile, size, xscale=1.0, color='white'):
    """Urdu / Hindi + Latin text, shaped properly by ffmpeg (harfbuzz)."""
    fbase = os.path.basename(fontfile)
    if not os.path.exists(os.path.join(TMP, fbase)):
        shutil.copyfile(fontfile, os.path.join(TMP, fbase))
    with open(os.path.join(TMP, 'dt.txt'), 'w', encoding='utf-8') as fh:
        fh.write(text)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=black@0.0:s=4000x{size * 3},format=rgba',
                    '-vf', f'drawtext=fontfile={fbase}:textfile=dt.txt:fontsize={size}:fontcolor={color}:x=40:y={size // 2}',
                    '-frames:v', '1', 'dt.png'], cwd=TMP, check=True)
    im = Image.open(os.path.join(TMP, 'dt.png')).convert('RGBA')
    bb = im.getbbox()
    if not bb:
        return None
    im = im.crop(bb)
    if xscale != 1.0:
        im = im.resize((max(1, int(im.width * xscale)), im.height), Image.LANCZOS)
    return im


def line_img(line, st, size, xs, col=None):
    """One line of text. col = '#rrggbb' to override the style's own colour."""
    if not line.strip():
        return None
    if st.get('engine') == 'drawtext':
        return drawtext_img(line, fontfind.path(st['font']), size, xs, ('0x' + col[1:]) if col else 'white')
    if st.get('track'):
        return text_img(line, st['font'], size, hex_rgba(col) if col else st['fill'], xs, None, st['track'])
    return text_img(line, st['font'], size, hex_rgba(col) if col else st['fill'], xs, 'seguiemj.ttf')


def prefix_width(prefix, st, size, xs):
    if not prefix.strip():
        return 0
    if st.get('engine') == 'drawtext':
        return int(F(st['font'], size).getlength(prefix.rstrip()) * xs) + 3
    if st.get('track'):
        im = text_img(prefix.rstrip(), st['font'], size, st['fill'], xs, None, st['track'])
        return (im.width + 3) if im else 0
    im = text_img(prefix.rstrip(), st['font'], size, st['fill'], xs, 'seguiemj.ttf')
    return (im.width + 3) if im else 0


def arc_img(text, size, st, r, fill=None):
    """Letters placed along a circle (like the curved 'Your thing right now'). Returns image + circle-centre offset."""
    f = F(st['font'], size)
    fill = fill or st['fill']
    side = int(2 * r + 4 * size + 200)
    cx = cy = side // 2
    img = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    theta = math.radians(160)
    for ch in text:
        wch = f.getlength(ch)
        mid = theta + (wch / 2) / r
        if ch != ' ':
            g = Image.new('RGBA', (int(wch) + 60, f.size + 60), (0, 0, 0, 0))
            ImageDraw.Draw(g).text((30, 20), ch, font=f, fill=fill)
            ang = math.degrees(math.atan2(math.cos(mid), -math.sin(mid)))
            g = g.rotate(-ang, resample=Image.BICUBIC, expand=True)
            px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
            # each letter gets its own shadow, like the original curved text (shadow is baked into this image)
            composite(img, g, int(px - g.width / 2), int(py - g.height / 2), st['shadow'], st['blur'] * TS,
                      (round(st['off'][0] * TS), round(st['off'][1] * TS)), 1.0)
        theta += wch / r
    bb = img.getbbox()
    if not bb:
        return None, 0, 0
    return img.crop(bb), cx - bb[0], cy - bb[1]


def render_key(L):
    st = STYLES.get(L.get('style'), STYLES['clean'])
    k = [L.get('text', ''), L.get('style'), int(L.get('size', 60)), round(float(L.get('xs', st['xs'])), 3), int(L.get('r', 542)) if st.get('arc') else 0]
    if L.get('color'):                 # only added when set, so texts made before colours keep their cached images
        k.append(L['color'].lower())
    if st.get('arc') and TS != 1.0:    # curved text has its shadow baked in, so a bigger export needs its own copy
        k.append(f'ts{TS:.3f}')
    return k


def text_resources(L):
    """Render a text layer once (cached on disk). Returns meta with image file names."""
    key = render_key(L)
    h = hashlib.sha1(json.dumps(key, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]
    mp = os.path.join(TEXTC, h + '.json')
    if os.path.exists(mp):
        try:
            return json.load(open(mp, encoding='utf-8'))
        except Exception:
            pass
    text, style, size, xs, r = key[:5]
    col = next((v for v in key[5:] if str(v).startswith('#')), None)
    st = STYLES.get(style, STYLES['clean'])
    with _text_lock:
        meta = {'hash': h, 'lines': [], 'states': [], 'wordEnds': []}
        if st.get('arc'):
            words = text.split()
            for n in range(1, len(words) + 1):
                im, ox, oy = arc_img(' '.join(words[:n]), size, st, r, hex_rgba(col) if col else None)
                if im is None:
                    continue
                fn = f'{h}_a{n}.png'
                im.save(os.path.join(TEXTC, fn), compress_level=1)
                meta['states'].append({'f': fn, 'w': im.width, 'h': im.height, 'ox': ox, 'oy': oy})
        else:
            count = 0
            for k, line in enumerate(text.split('\n')):
                vis = [ch for ch in line if ch != '\ufe0f']
                im = line_img(line, st, size, xs, col)
                for m in re.finditer(r'\S+', line):
                    meta['wordEnds'].append(count + len(line[:m.end()].replace('\ufe0f', '')))
                count += len(vis)
                if im is None:
                    meta['lines'].append({'f': None, 'w': 0, 'h': 0, 'n': len(vis), 'cuts': [0] * len(vis)})
                    continue
                cuts, prefix, seen = [], '', 0
                for ch in line:
                    prefix += ch
                    if ch == '\ufe0f':
                        continue
                    seen += 1
                    if seen == len(vis):
                        cuts.append(im.width)
                    else:
                        cuts.append(min(im.width, prefix_width(prefix, st, size, xs)))
                fn = f'{h}_l{k}.png'
                im.save(os.path.join(TEXTC, fn), compress_level=1)
                meta['lines'].append({'f': fn, 'w': im.width, 'h': im.height, 'n': len(vis), 'cuts': cuts})
        json.dump(meta, open(mp, 'w', encoding='utf-8'))
    return meta


def text_alpha(L, i):
    a = 1.0
    k = i - L['f0']
    if L.get('anim_in') == 'fade':
        a = min(1.0, (k + 1) / max(1, int(L.get('in_frames', 12))))
    if L.get('anim_out') == 'fade':
        end = float(L.get('fade_end', L['f1']))          # fade_end: exact (fractional) end copied from an original
        r = (end - i) / max(0.5, float(L.get('out_frames', 6)))
        if r < 1:
            a *= max(0.0, r)
    return round(a, 2)


def text_visible(L, i, R):
    """How much of the layer shows at frame i: None = everything, else a number of characters (or arc states)."""
    k = i - L['f0']
    anim = L.get('anim_in')
    if anim == 'type':
        n = int(k / FPS * float(L.get('cps', 30))) + 1
        return n
    if anim == 'words':
        wf = L.get('wframes')          # exact word timings copied from an original reel
        w = sum(1 for t in wf if k >= t) if wf else 1 + k // max(1, int(L.get('wstep', 7)))
        w = max(1, w)
        if R['states']:
            return min(w, len(R['states']))
        we = R['wordEnds']
        return None if w >= len(we) else we[w - 1]
    if R['states']:
        return len(R['states'])
    return None


def composite(canvas, im, x, y, shadow, blur, off, alpha):
    """Paste im at (x, y) with a soft drop shadow, like the earlier reels; clipped to the canvas."""
    if im is None:
        return
    if alpha < 1.0:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    layers = []
    if shadow and shadow[3] > 0:
        # same maths as the reels made before (shadow pasted through its own mask, then blurred)
        pad = int(blur * 4 + max(abs(off[0]), abs(off[1])) + 4)
        sh = Image.new('RGBA', im.size, tuple(shadow))
        sh.putalpha(im.getchannel('A').point(lambda v: int(v * shadow[3] / 255)))
        layer = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        layer.paste(sh, (pad + off[0], pad + off[1]), sh)
        layers.append((layer.filter(ImageFilter.GaussianBlur(blur)), x - pad, y - pad))
    layers.append((im, x, y))
    for src, sx, sy in layers:
        x0, y0 = max(0, sx), max(0, sy)
        x1, y1 = min(canvas.width, sx + src.width), min(canvas.height, sy + src.height)
        if x1 <= x0 or y1 <= y0:
            continue
        canvas.alpha_composite(src, (x0, y0), (x0 - sx, y0 - sy, x1 - sx, y1 - sy))


_res_imgs = {}


def res_image(fn):
    if fn not in _res_imgs:
        _res_imgs[fn] = Image.open(os.path.join(TEXTC, fn)).convert('RGBA')
    return _res_imgs[fn]


TS = 1.0      # text scale: 1 for the 1080 x 1920 design; bigger while a 2K / 4K export draws its texts


def draw_layer(canvas, L, R, vis, alpha):
    st = STYLES.get(L['style'], STYLES['clean'])
    sh, bl, off = st['shadow'], st['blur'] * TS, (round(st['off'][0] * TS), round(st['off'][1] * TS))
    if R['states']:
        if not vis:
            return
        s = R['states'][vis - 1]          # curved text already has its shadow drawn in
        composite(canvas, res_image(s['f']), int(L['x'] * W - s['ox']), int(L['y'] * H - s['oy']), None, bl, off, alpha)
        return
    lines = R['lines']
    n = len(lines)
    lg = float(L.get('lh', 1.15)) * int(L['size'])
    rem = vis
    for k, ln in enumerate(lines):
        if rem is not None and rem <= 0:
            break
        take = ln['n'] if rem is None else min(rem, ln['n'])
        if rem is not None:
            rem -= take
        if not ln['f'] or take <= 0:
            continue
        im = res_image(ln['f'])
        if take < ln['n']:
            cw = ln['cuts'][take - 1]
            if cw <= 0:
                continue
            im = im.crop((0, 0, min(cw, im.width), im.height))
        cy = L['y'] * H + (k - (n - 1) / 2) * lg
        composite(canvas, im, int(L['x'] * W - ln['w'] / 2), int(cy - ln['h'] / 2), sh, bl, off, alpha)


def fit_size(text, font, target_w, xscale=1.0, emoji_font=None):
    im = text_img(text, font, 200, (255, 255, 255, 255), xscale, emoji_font)
    return max(8, int(200 * target_w / im.width))


def fr(t):
    return int(round(t * FPS))


def segs_from(cuts, total):
    b = [0] + list(cuts) + [total]
    return [(b[i], b[i + 1]) for i in range(len(b) - 1)]


def TL(text, f0, f1, x, y, size, style, **kw):
    d = dict(text=text, f0=int(f0), f1=int(f1), x=round(x, 4), y=round(y, 4), size=int(size), style=style,
             xs=STYLES[style]['xs'], lh=1.15, anim_in='none', in_frames=12, cps=30, wstep=7, anim_out='none', out_frames=6)
    d.update(kw)
    return d


# =====================================================================================
# Templates. A template is a reel's beat: its length, cut points, sound and starting texts. Your own templates
# (e.g. made from an inspiration reel) are files in templates\ - see file_templates(). One is built in:
# "Blank", a 15-second reel with a cut every 1.5 s and no sound (add music in Instagram), so a new copy works at once.
# =====================================================================================
BLANK_KEY = 'blank'


def tpl_blank():
    total = 450
    texts = [TL('Your words here', 0, 90, 0.5, 0.2, 84, 'clean', anim_in='fade', in_frames=10)]
    return dict(key=BLANK_KEY, title='Blank · 15 s, a cut every 1.5 s', song=False, col='', total=total,
                cuts=[45 * i for i in range(1, 10)], grade='natural', texts=texts)


def blank_media():
    """Silence for the Blank template, and a plain dark 'original reel' to show beside your edit."""
    a, v = os.path.join(AUDIO, BLANK_KEY + '.m4a'), os.path.join(INSP, BLANK_KEY + '.mp4')
    if not os.path.exists(a):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', '15',
                        '-c:a', 'aac', '-b:a', '96k', a], capture_output=True, creationflags=LOW)
    if not os.path.exists(v):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=0x18181c:s=540x960:r=30', '-t', '15',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', v], capture_output=True, creationflags=LOW)


TEMPLATES = {}

# =====================================================================================
# Colour looks. The very same maths runs in the browser preview (WebGL shader in studio.html)
# and in the export (baked into a 3D LUT), so what you see is what you get.
#   exp = exposure (stops), gam = midtones, temp = warm(+)/cool(-), tint = magenta(+)/green(-),
#   con = contrast, hl / sd = brighten(+) or darken(-) highlights / shadows, sat = saturation,
#   vib = vibrance, mono = black & white amount, sh / hi = colour added to shadows / highlights,
#   fade = lifted blacks (film look)
# =====================================================================================
LOOKS = [
    ('none', 'Original', 'Basics', {}),
    ('natural', 'Natural', 'Basics', dict(con=1.03, sat=1.05)),
    ('crisp', 'Crisp', 'Basics', dict(con=1.1, hl=-0.3, sd=0.25, sat=1.05, vib=0.15)),
    ('bright', 'Bright & airy', 'Basics', dict(exp=0.18, con=0.93, sat=0.95, fade=0.02, temp=0.1, sd=0.2)),
    ('vivid', 'Vivid', 'Basics', dict(con=1.08, sat=1.22, vib=0.3)),
    ('punchy', 'Punchy', 'Basics', dict(con=1.18, sat=1.15, hl=-0.2, sd=-0.1)),
    ('softlight', 'Soft light', 'Basics', dict(con=0.9, hl=-0.25, sd=0.3, sat=0.97, fade=0.02)),
    ('matte', 'Matte', 'Basics', dict(fade=0.09, con=0.95, sat=0.95)),
    ('warm', 'Warm', 'Warm', dict(gam=0.97, con=1.05, sat=0.95, temp=0.45, hi=(0.01, 0.005, -0.015))),
    ('golden', 'Golden hour', 'Warm', dict(exp=0.05, temp=0.6, con=1.04, sat=1.08, hi=(0.04, 0.02, -0.02))),
    ('sunset', 'Sunset glow', 'Warm', dict(temp=0.7, tint=0.25, con=1.03, sat=1.12, sh=(0.02, -0.01, 0.03))),
    ('summer', 'Summer', 'Warm', dict(exp=0.08, temp=0.3, con=1.02, sat=1.15)),
    ('honey', 'Honey', 'Warm', dict(temp=0.5, tint=0.05, con=1.03, sat=1.05, hi=(0.03, 0.02, -0.02))),
    ('autumn', 'Autumn', 'Warm', dict(temp=0.45, tint=0.1, con=1.06, sat=1.12, vib=0.1, sh=(0.02, 0.0, -0.02), hi=(0.05, 0.02, -0.03))),
    ('amber', 'Amber', 'Warm', dict(temp=0.8, con=1.04, sat=0.95, fade=0.02)),
    ('terracotta', 'Terracotta', 'Warm', dict(temp=0.4, tint=0.15, con=1.05, sat=1.05, sh=(0.03, -0.01, -0.02))),
    ('desert', 'Desert', 'Warm', dict(temp=0.55, con=1.05, sat=0.88, fade=0.02, hi=(0.03, 0.02, -0.01))),
    ('warmfilm', 'Warm film', 'Warm', dict(temp=0.35, con=1.06, sat=1.04, fade=0.03, sh=(0.02, 0.01, -0.02), hi=(0.03, 0.02, 0.0))),
    ('cool', 'Cool', 'Cool', dict(temp=-0.5, con=1.03)),
    ('nordic', 'Nordic', 'Cool', dict(exp=0.03, temp=-0.35, con=1.02, sat=0.8, fade=0.03)),
    ('alpine', 'Alpine', 'Cool', dict(exp=0.02, temp=-0.15, con=1.08, sat=1.15, vib=0.2)),
    ('icy', 'Icy blue', 'Cool', dict(exp=0.06, temp=-0.7, con=1.0, sat=0.85, hi=(-0.01, 0.01, 0.03))),
    ('ocean', 'Ocean', 'Cool', dict(temp=-0.25, tint=-0.1, con=1.04, sat=1.1, sh=(-0.02, 0.02, 0.05))),
    ('winter', 'Winter', 'Cool', dict(exp=0.08, temp=-0.4, con=0.98, sat=0.7, fade=0.03)),
    ('glacier', 'Glacier', 'Cool', dict(exp=0.05, temp=-0.55, tint=-0.1, sat=0.9, hl=-0.2, hi=(-0.01, 0.02, 0.04))),
    ('mist', 'Morning mist', 'Cool', dict(exp=0.1, temp=-0.2, con=0.88, sat=0.8, fade=0.06)),
    ('moody', 'Moody', 'Cinematic', dict(exp=-0.04, con=1.1, sat=0.92, temp=0.35, hi=(0.01, 0.0, -0.01))),
    ('cinematic', 'Cinematic', 'Cinematic', dict(exp=-0.03, con=1.12, sat=0.9, fade=0.03, sh=(-0.01, 0.02, 0.04), hi=(0.03, 0.01, -0.02))),
    ('tealorange', 'Teal & orange', 'Cinematic', dict(con=1.08, sat=1.1, sh=(-0.03, 0.02, 0.06), hi=(0.06, 0.02, -0.04))),
    ('blockbuster', 'Blockbuster', 'Cinematic', dict(con=1.15, sat=1.1, sd=-0.1, sh=(-0.04, 0.02, 0.07), hi=(0.07, 0.02, -0.05))),
    ('emerald', 'Emerald', 'Cinematic', dict(tint=-0.4, con=1.04, sat=1.02, sh=(-0.02, 0.03, 0.01))),
    ('dusk', 'Dusk', 'Cinematic', dict(temp=-0.3, tint=0.25, con=1.06, sh=(0.02, -0.01, 0.05))),
    ('neonoir', 'Neo-noir', 'Cinematic', dict(exp=-0.05, con=1.15, sat=0.7, sh=(-0.02, 0.03, 0.03), hi=(0.02, 0.0, -0.02))),
    ('thriller', 'Thriller', 'Cinematic', dict(temp=-0.2, tint=-0.3, con=1.12, sat=0.75, sh=(-0.02, 0.03, 0.02))),
    ('drama', 'Drama', 'Cinematic', dict(con=1.25, sat=0.85, hl=-0.2, sd=-0.15)),
    ('dreamy', 'Dreamy', 'Cinematic', dict(exp=0.08, con=0.9, fade=0.05, hl=0.2, tint=0.15, sat=0.95, hi=(0.03, 0.0, 0.02))),
    ('western', 'Western', 'Cinematic', dict(temp=0.6, tint=0.05, con=1.12, sat=0.8, fade=0.03, hi=(0.04, 0.02, -0.03))),
    ('faded', 'Faded film', 'Film', dict(fade=0.08, con=0.92, sat=0.88, temp=0.15, hi=(0.02, 0.01, -0.01))),
    ('vintage', 'Vintage', 'Film', dict(fade=0.06, con=0.95, sat=0.75, temp=0.45, tint=0.1, sh=(0.03, 0.02, -0.02))),
    ('greenfilm', 'Green film', 'Film', dict(tint=-0.2, fade=0.04, con=1.04, sat=0.95, sh=(-0.01, 0.02, 0.0), hi=(0.02, 0.02, -0.02))),
    ('instant', 'Instant photo', 'Film', dict(temp=0.1, fade=0.08, con=0.95, sat=0.9, sh=(-0.02, 0.01, 0.04), hi=(0.04, 0.02, -0.02))),
    ('seventies', '70s', 'Film', dict(temp=0.5, con=0.97, sat=0.85, fade=0.06, sh=(0.03, 0.01, -0.03))),
    ('nineties', '90s film', 'Film', dict(temp=0.2, tint=-0.08, con=1.1, sat=1.15, fade=0.04)),
    ('slide', 'Slide film', 'Film', dict(temp=0.15, con=1.15, sat=1.2, hl=-0.15, sh=(0.0, 0.0, 0.02))),
    ('crossproc', 'Cross process', 'Film', dict(con=1.15, sat=1.15, sh=(-0.02, 0.0, 0.08), hi=(0.06, 0.05, -0.06))),
    ('expired', 'Expired film', 'Film', dict(tint=0.2, fade=0.1, sat=0.8, sh=(0.02, -0.02, 0.03), hi=(0.05, 0.04, -0.02))),
    ('pastel', 'Pastel', 'Film', dict(exp=0.12, fade=0.07, con=0.9, sat=0.7, tint=0.15)),
    ('rose', 'Rosé', 'Film', dict(temp=0.15, tint=0.45, sat=0.95, hi=(0.04, 0.0, 0.03))),
    ('mediterranean', 'Mediterranean', 'Travel', dict(temp=0.1, con=1.05, sat=1.05, vib=0.3, sh=(-0.02, 0.01, 0.05), hi=(0.03, 0.02, -0.01))),
    ('riviera', 'Riviera', 'Travel', dict(exp=0.06, temp=0.2, tint=0.05, con=1.03, vib=0.25, sh=(-0.01, 0.02, 0.04))),
    ('lush', 'Lush green', 'Travel', dict(tint=-0.15, con=1.04, sat=1.15, vib=0.2)),
    ('lakeside', 'Lakeside', 'Travel', dict(exp=0.04, temp=-0.15, hl=-0.15, sat=1.05, vib=0.15, sh=(-0.02, 0.02, 0.04))),
    ('mountain', 'Mountain air', 'Travel', dict(temp=-0.1, con=1.06, hl=-0.25, sd=0.15, vib=0.2)),
    ('oldtown', 'Old town', 'Travel', dict(temp=0.3, con=1.08, sat=0.95, fade=0.02, sh=(0.02, 0.01, -0.01), hi=(0.03, 0.02, -0.01))),
    ('tropical', 'Tropical', 'Travel', dict(temp=0.15, tint=-0.05, con=1.05, sat=1.2, vib=0.25)),
    ('softskin', 'Soft skin', 'Soft', dict(temp=0.15, con=0.95, hl=-0.2, sd=0.15, sat=0.95)),
    ('glow', 'Glow', 'Soft', dict(exp=0.1, temp=0.1, con=0.95, hl=0.15, sd=0.1, fade=0.03)),
    ('peach', 'Peach', 'Soft', dict(temp=0.3, tint=0.15, sat=0.95, fade=0.02, hi=(0.03, 0.01, 0.0))),
    ('milky', 'Milky', 'Soft', dict(exp=0.15, con=0.9, sat=0.75, fade=0.07)),
    ('blush', 'Blush', 'Soft', dict(temp=0.1, tint=0.3, sat=0.9, fade=0.03, hi=(0.03, 0.0, 0.02))),
    ('nightblue', 'Night blue', 'Night', dict(temp=-0.5, con=1.1, sat=0.9, sh=(-0.02, 0.0, 0.05))),
    ('neon', 'Neon', 'Night', dict(tint=0.2, con=1.1, sat=1.3, sh=(0.02, -0.02, 0.06))),
    ('citylights', 'City lights', 'Night', dict(con=1.1, sat=1.1, sh=(-0.02, 0.01, 0.05), hi=(0.06, 0.03, -0.02))),
    ('midnight', 'Midnight', 'Night', dict(exp=-0.1, temp=-0.35, con=1.12, sat=0.8, fade=0.02)),
    ('bw', 'Black & white', 'Black & white', dict(mono=1.0, con=1.1)),
    ('noir', 'Noir', 'Black & white', dict(mono=1.0, con=1.35, exp=-0.05)),
    ('highkey', 'High-key', 'Black & white', dict(mono=1.0, exp=0.25, con=0.9)),
    ('silver', 'Silver', 'Black & white', dict(mono=1.0, con=0.95, fade=0.05, sh=(-0.01, 0.0, 0.02))),
    ('selenium', 'Selenium', 'Black & white', dict(mono=1.0, con=1.1, sh=(-0.01, 0.0, 0.03), hi=(0.03, 0.02, 0.0))),
    ('sepia', 'Sepia', 'Black & white', dict(mono=1.0, con=1.05, sh=(0.07, 0.025, -0.06), hi=(0.09, 0.045, -0.05))),
    # the House Party 02 grade: candle-warm, orange pulled back a touch, plum-leaning shadows
    ('hp_party', 'House party · night', 'House party', dict(exp=-0.12, temp=-0.2, tint=0.04, con=1.17, hl=-0.22, sd=-0.08, sat=0.95, vib=0.06,
                                                          fade=0.012, sh=(0.012, -0.014, 0.035), hi=(0.015, 0.006, -0.012))),
    ('hp_shoot', 'House party · drinks', 'House party', dict(exp=-0.04, temp=-0.12, con=1.09, hl=-0.15, sat=0.98, vib=0.1, fade=0.01,
                                                           sh=(0.01, -0.01, 0.025))),
]
LOOK = {k: {'key': k, 'label': lb, 'group': g, 'p': p} for k, lb, g, p in LOOKS}
LW = (0.2126, 0.7152, 0.0722)


def look_rgb(c, P):
    """Apply a look to one colour (0..1). Keep in step with the WebGL shader in studio.html."""
    e = 2.0 ** P.get('exp', 0.0)
    r, g, b = c[0] * e, c[1] * e, c[2] * e
    gm = P.get('gam', 1.0)
    if gm != 1.0:
        r, g, b = (max(v, 0.0) ** (1.0 / gm) for v in (r, g, b))
    t, ti = P.get('temp', 0.0), P.get('tint', 0.0)
    r *= 1 + 0.1 * t
    b *= 1 - 0.1 * t
    g *= 1 - 0.06 * ti
    k = P.get('con', 1.0)
    r, g, b = ((v - 0.5) * k + 0.5 for v in (r, g, b))
    hl, sd = P.get('hl', 0.0), P.get('sd', 0.0)
    if hl or sd:                       # tone: lift / lower the dark and the bright parts separately
        l = min(1.0, max(0.0, r * LW[0] + g * LW[1] + b * LW[2]))
        d = 0.35 * (sd * 4 * l * (1 - l) * (1 - l) + hl * 4 * l * l * (1 - l))
        r, g, b = r + d, g + d, b + d
    l = r * LW[0] + g * LW[1] + b * LW[2]
    sat, vib = P.get('sat', 1.0), P.get('vib', 0.0)
    if vib:
        sat *= 1 + vib * (1 - min(1.0, max(0.0, max(r, g, b) - min(r, g, b))))
    r, g, b = (l + (v - l) * sat for v in (r, g, b))
    m = P.get('mono', 0.0)
    if m:
        l = r * LW[0] + g * LW[1] + b * LW[2]
        r, g, b = (v + (l - v) * m for v in (r, g, b))
    sh, hi = P.get('sh', (0.0, 0.0, 0.0)), P.get('hi', (0.0, 0.0, 0.0))
    l = min(1.0, max(0.0, r * LW[0] + g * LW[1] + b * LW[2]))
    ws, wh = (1 - l) * (1 - l), l * l
    r, g, b = r + sh[0] * ws + hi[0] * wh, g + sh[1] * ws + hi[1] * wh, b + sh[2] * ws + hi[2] * wh
    f = P.get('fade', 0.0)
    r, g, b = (f + v * (1 - f) for v in (r, g, b))
    return tuple(min(1.0, max(0.0, v)) for v in (r, g, b))


def look_key(p, T=None):
    k = p.get('grade') or (T or {}).get('grade') or 'natural'
    return k if k in LOOK else 'natural'


# Manual grading sliders (the "Adjust" tab). Stored as the slider values; turned into look parameters here
# and by adjParams() in studio.html with the same maths.
ADJ_KEYS = {'exp': (-1.5, 1.5), 'con': (-0.6, 0.6), 'hl': (-1, 1), 'sd': (-1, 1), 'sat': (-1, 1), 'vib': (-1, 1),
            'temp': (-1, 1), 'tint': (-1, 1), 'fade': (0, 0.25), 'sth': (0, 360), 'sta': (0, 1), 'hih': (0, 360), 'hia': (0, 1)}


def hue_rgb(h):
    """Pure colour for a hue (0..360), as r, g, b in 0..1."""
    def ch(n):
        k = (n + h / 60.0) % 6
        return 1 - max(0.0, min(k, 4 - k, 1.0))
    return ch(5), ch(3), ch(1)


def split_rgb(h, amt):
    c = hue_rgb(h)
    m = sum(c) / 3
    return tuple((v - m) * amt * 0.16 for v in c)


def clean_adj(a):
    out = {}
    if isinstance(a, dict):
        for k, (lo, hi) in ADJ_KEYS.items():
            try:
                v = round(max(lo, min(hi, float(a.get(k, 0) or 0))), 3)
            except (TypeError, ValueError):
                v = 0.0
            if v:
                out[k] = v
    return out


def adj_params(a):
    a = a or {}
    g = lambda k: float(a.get(k, 0) or 0)
    return {'exp': g('exp'), 'con': 1 + g('con'), 'hl': g('hl'), 'sd': g('sd'), 'sat': 1 + g('sat'), 'vib': g('vib'),
            'temp': g('temp'), 'tint': g('tint'), 'fade': g('fade'),
            'sh': split_rgb(g('sth'), g('sta')), 'hi': split_rgb(g('hih'), g('hia'))}


def colour_of(p, s, T=None):
    """The colour a shot uses: (look, strength, adjustments) - its own if it has one, otherwise the reel's."""
    own = s.get('look') if isinstance(s.get('look'), dict) else None
    if own:
        return own.get('grade', 'natural'), float(own.get('amt', 1.0)), clean_adj(own.get('adj'))
    return look_key(p, T), float(p.get('grade_amt', 1.0)), clean_adj(p.get('adj'))


def look_filter(key, amt, adj=None):
    """ffmpeg filter for a look at a strength (0..1) plus slider adjustments, or None for no change.
    Run ffmpeg with cwd=LUTS."""
    amt = round(max(0.0, min(1.0, float(amt))), 2)
    if key not in LOOK:
        key = 'natural'
    adj = clean_adj(adj)
    if (key == 'none' or amt <= 0) and not adj:
        return None
    P, A = LOOK[key]['p'], adj_params(adj) if adj else None
    tag = hashlib.sha1(json.dumps([key, amt, adj], sort_keys=True).encode()).hexdigest()[:12]
    fn = f'{key}_{int(round(amt * 100)):03d}_{tag}.cube'
    fp = os.path.join(LUTS, fn)
    if not os.path.exists(fp):
        N = 33
        out = [f'TITLE "{key}"', f'LUT_3D_SIZE {N}']
        for bi in range(N):
            for gi in range(N):
                for ri in range(N):
                    c0 = (ri / (N - 1), gi / (N - 1), bi / (N - 1))
                    c1 = look_rgb(c0, P)
                    c = tuple(a + (b - a) * amt for a, b in zip(c0, c1))
                    if A:
                        c = look_rgb(c, A)
                    out.append('%.6f %.6f %.6f' % c)
        tmp = fp + '.part'
        with open(tmp, 'w') as fh:
            fh.write('\n'.join(out) + '\n')
        os.replace(tmp, fp)
    return f'lut3d=file={fn}:interp=tetrahedral'


def clean_fx(fx):
    out = {}
    if isinstance(fx, dict):
        for k in ('vig', 'grain'):
            try:
                v = round(max(0.0, min(1.0, float(fx.get(k, 0) or 0))), 3)
            except (TypeError, ValueError):
                v = 0.0
            if v:
                out[k] = v
    return out


def vignette_png(amount):
    """Black picture whose see-through-ness makes the corners darker. Same formula as the WebGL preview."""
    import numpy as np
    fn = os.path.join(LUTS, f'vignette_{int(round(amount * 1000)):04d}' + ('' if (W, H) == (1080, 1920) else f'_{W}x{H}') + '.png')
    if not os.path.exists(fn):
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        qx, qy = ((x + 0.5) / W - 0.5) * 2, ((y + 0.5) / H - 0.5) * 2
        r = np.sqrt(qx * qx + qy * qy) / math.sqrt(2)
        s = np.clip((r - 0.3) / 0.7, 0, 1)
        a = np.clip(amount * 0.85 * s * s, 0, 1)
        im = np.zeros((H, W, 4), np.uint8)
        im[..., 3] = np.round(a * 255).astype(np.uint8)
        Image.fromarray(im, 'RGBA').save(fn)
    return fn


GRAIN_STRENGTH = 18          # ffmpeg noise strength at grain = 1: same spread (about 12 levels) as the preview's grain


import carousel_engine as CE  # noqa: E402  (Carousel Studio: same looks as the reels)
CE.setup(look_rgb, LOOK)

COLOR_TAGS = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def look_chain(lut):
    """Filters that apply a look to video frames (YUV -> RGB -> look -> YUV)."""
    if not lut:
        return ''
    return f',scale=in_color_matrix=bt709,format=gbrp,{lut},scale=out_color_matrix=bt709:out_range=tv,format=yuv420p'


def wave_for(path, total):
    """Peak loudness per video frame (0..1) for the timeline waveform."""
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '6000', '-f', 's16le', '-'], capture_output=True)
    a = array('h'); a.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    per = 6000 // FPS
    peaks = [max((abs(v) for v in a[i * per:(i + 1) * per]), default=0) for i in range(total)]
    m = max(peaks) or 1
    return [round(v / m, 3) for v in peaks]


TEMPLATE_DIR = os.path.join(HERE, 'templates')       # more templates as files: <key>.json (+ the sound and the reference reel)


def file_templates():
    """Templates kept as files (e.g. the House Party 02 reels). Each .json holds key, title, total (frames), cuts, grade,
    texts, 'audio' and 'insp' (paths to the sound and the reference video) and 'starter' (the first reel made from it)."""
    out = []
    if not os.path.isdir(TEMPLATE_DIR):
        return out
    for fn in sorted(os.listdir(TEMPLATE_DIR)):
        if not fn.endswith('.json'):
            continue
        try:
            T = json.load(open(os.path.join(TEMPLATE_DIR, fn), encoding='utf-8'))
            if not re.fullmatch(r'[A-Za-z0-9_-]{1,32}', T.get('key', '')):
                raise ValueError('bad key')
            for kind, folder, ext in (('audio', AUDIO, '.m4a'), ('insp', INSP, '.mp4')):
                src = T.get(kind)
                if src and not os.path.isabs(src):
                    src = os.path.join(TEMPLATE_DIR, src)
                dst = os.path.join(folder, T['key'] + ext)
                if src and os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst)):
                    shutil.copyfile(src, dst)
            T.setdefault('grade', 'natural'); T.setdefault('cuts', []); T['song'] = bool(T.get('song', False))
            out.append(T)
        except Exception as e:
            log('template file skipped:', fn, e)
    return out


def load_templates():
    blank_media()
    for T in [tpl_blank()] + file_templates():
        for k, L in enumerate(T['texts']):
            L['id'] = L.get('id') or f't{k + 1}'
        ap = os.path.join(AUDIO, T['key'] + '.m4a')
        mp = os.path.join(META, T['key'] + '.json')
        mt = int(os.path.getmtime(ap)) if os.path.exists(ap) else 0
        w = None
        if os.path.exists(mp):
            j = json.load(open(mp))
            if j.get('mt', mt) == mt and len(j['wave']) == T['total']:
                w = j['wave']
        if w is None:
            w = wave_for(ap, T['total']) if mt else [0.0] * T['total']
            json.dump({'wave': w, 'mt': mt}, open(mp, 'w'))
        T['wave'] = w
        for L in T['texts']:
            text_resources(L)
        TEMPLATES[T['key']] = T


def template_meta(T):
    return {k: T[k] for k in ('key', 'title', 'total', 'cuts', 'grade', 'texts', 'wave')} | {
        'audio': f"/audio/{T['key']}.m4a", 'insp': f"/insp/{T['key']}.mp4", 'fps': FPS, 'song': T.get('song', True),
        'col': T.get('col', 'europe')}


# =====================================================================================
# Starting projects: a template's own "starter" (its shots), or - for Blank - your newest clips, in the order filmed
# =====================================================================================
def auto_slots(n, need):
    """n shots from the newest footage folder: clips long enough for a shot of `need` seconds, oldest first."""
    vids = [c for c in COLL_ITEMS + LIB if c.get('kind') != 'photo' and c.get('d', 0) >= need]
    if not vids:
        return []
    newest = max(vids, key=lambda c: c.get('r', ''))['col']
    vids = sorted([c for c in vids if c['col'] == newest], key=lambda c: (c.get('r', ''), c['f']))
    pick = [vids[int(i * len(vids) / n)] for i in range(n)]          # spread across the folder; repeats if it has fewer clips
    return [{'clip': c['id'], 'in': round(max(0.0, c['d'] / 2 - need / 2), 2), 'cx': 0.5, 'cy': 0.5, 'zoom': 1.0, 'reverse': False}
            for c in pick]


def starter(key):
    T = TEMPLATES[key]
    s = T.get('starter') or {'name': 'My first reel' if key == BLANK_KEY else T['title'], 'grade': T.get('grade', 'natural'),
                             'slots': auto_slots(len(T['cuts']) + 1, (T['total'] / (len(T['cuts']) + 1)) / FPS)}
    p = {'id': '', 'template': key, 'name': s['name'], 'grade': s.get('grade', T.get('grade', 'natural')), 'cuts': list(T['cuts']),
         'slots': json.loads(json.dumps(s['slots'])), 'texts': json.loads(json.dumps(T['texts'])), 'updated': 0}
    for k in ('grade_amt', 'fx', 'adj', 'format', 'fill'):
        if k in s:
            p[k] = json.loads(json.dumps(s[k]))
    return p


def project_path(pid):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', pid or ''):
        raise ValueError('bad project id')
    return os.path.join(PROJECTS, pid + '.json')


def with_texts(p):
    """Older projects (made before text was editable) get the original text."""
    if 'texts' not in p and p.get('template') in TEMPLATES:
        p['texts'] = json.loads(json.dumps(TEMPLATES[p['template']]['texts']))
    return p


def list_projects():
    out = []
    for fn in os.listdir(PROJECTS):
        if fn.endswith('.json'):
            try:
                out.append(with_texts(json.load(open(os.path.join(PROJECTS, fn), encoding='utf-8'))))
            except Exception:
                pass
    out.sort(key=lambda p: (p.get('template', ''), p.get('name', '')))
    return out


def ensure_first_project():
    """A brand-new copy has no reels yet: as soon as there is footage, start "My first reel" on the Blank template."""
    if any(fn.endswith('.json') for fn in os.listdir(PROJECTS)) or BLANK_KEY not in TEMPLATES:
        return None
    p = starter(BLANK_KEY)
    if len(p['slots']) != len(p['cuts']) + 1:
        return None
    p = validate_project(p)
    p['id'] = 'my-first-reel'
    json.dump(p, open(project_path(p['id']), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    log('Started', p['name'])
    return p['id']


def clean_text_layer(L, total):
    st = L.get('style') if L.get('style') in STYLES else 'clean'
    col = L.get('color')
    col = col.lower() if isinstance(col, str) and re.fullmatch(r'#[0-9a-fA-F]{6}', col) else None
    f0 = max(0, min(total - 1, int(L.get('f0', 0))))
    f1 = max(f0 + 1, min(total, int(L.get('f1', f0 + 30))))
    out = dict(id=str(L.get('id') or uuid.uuid4().hex[:8])[:20], text=str(L.get('text', ''))[:400], f0=f0, f1=f1,
               x=float(L.get('x', 0.5)), y=float(L.get('y', 0.5)), size=max(8, min(400, int(L.get('size', 60)))), style=st,
               xs=max(0.3, min(2.0, float(L.get('xs', STYLES[st]['xs'])))), lh=max(0.5, min(4.0, float(L.get('lh', 1.15)))),
               anim_in=L.get('anim_in') if L.get('anim_in') in ('none', 'fade', 'type', 'words') else 'none',
               in_frames=max(1, int(L.get('in_frames', 12))), cps=max(1.0, min(200.0, float(L.get('cps', 30)))),
               wstep=max(1, int(L.get('wstep', 7))), anim_out=L.get('anim_out') if L.get('anim_out') in ('none', 'fade') else 'none',
               out_frames=max(0.5, float(L.get('out_frames', 6))))
    if col:
        out['color'] = col
    if L.get('fade_end') is not None and out['anim_out'] == 'fade':
        out['fade_end'] = max(float(f0), min(float(f1), float(L['fade_end'])))
    if STYLES[st].get('arc'):
        out['r'] = max(100, min(2000, int(L.get('r', 542))))
    if isinstance(L.get('wframes'), list) and out['anim_in'] == 'words':
        out['wframes'] = [max(0, int(v)) for v in L['wframes']][:100]
    return out


def validate_project(p):
    T = TEMPLATES[p['template']]
    cuts = [int(c) for c in p['cuts']]
    b = [0] + cuts + [T['total']]
    if any(b[i + 1] - b[i] < 1 for i in range(len(b) - 1)):
        raise ValueError('cuts out of order')
    if len(p['slots']) != len(b) - 1:
        raise ValueError('number of shots does not match the cuts')
    for s in p['slots']:
        if int(s['clip']) not in CLIPS:
            raise ValueError(f"unknown clip {s['clip']}")
        if s.get('move') not in (None, 'none', 'in', 'out'):
            s['move'] = 'none'
        if s.get('fit') not in (None, False, True, 'bars', 'blur', 'crop'):
            s.pop('fit', None)
        if rot_of(s):
            s['rot'] = rot_of(s)
        else:
            s.pop('rot', None)
        if speed_of(s) != 1:
            s['speed'] = speed_of(s)
        else:
            s.pop('speed', None)
        lk = s.get('look')
        if isinstance(lk, dict):
            try:
                amt = round(max(0.0, min(1.0, float(lk.get('amt', 1.0)))), 2)
            except (TypeError, ValueError):
                amt = 1.0
            s['look'] = {'grade': lk.get('grade') if lk.get('grade') in LOOK else 'natural', 'amt': amt, 'adj': clean_adj(lk.get('adj'))}
        else:
            s.pop('look', None)
    p['cuts'] = cuts
    p['format'] = p.get('format') if p.get('format') in REEL_FORMATS else '9:16'
    p['fill'] = p.get('fill') if p.get('fill') in FILLS else 'crop'
    p['grade'] = look_key(p, T)
    try:
        p['grade_amt'] = round(max(0.0, min(1.0, float(p.get('grade_amt', 1.0)))), 2)
    except (TypeError, ValueError):
        p['grade_amt'] = 1.0
    p['adj'] = clean_adj(p.get('adj'))
    p['fx'] = clean_fx(p.get('fx'))
    with_texts(p)
    p['texts'] = [clean_text_layer(L, T['total']) for L in p.get('texts', [])][:200]
    return p


# =====================================================================================
# Photos: every place's "Photos" folder. Raw-only photos (.dng without a .jpg) are
# developed once by Windows' own DNG decoder (it gives the camera's preview size).
# =====================================================================================
PHOTO_EXT = ('.jpg', '.jpeg', '.png')
RAW_PS = r'''param([string]$List)
Add-Type -AssemblyName PresentationCore
foreach ($line in [IO.File]::ReadAllLines($List, [Text.Encoding]::UTF8)) {
  $p = $line -split "`t"
  if ($p.Count -lt 2) { continue }
  try {
    $dec = [System.Windows.Media.Imaging.BitmapDecoder]::Create([Uri]$p[0], [System.Windows.Media.Imaging.BitmapCreateOptions]::None, [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad)
    $enc = New-Object System.Windows.Media.Imaging.JpegBitmapEncoder
    $enc.QualityLevel = 95
    $enc.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($dec.Frames[0]))
    $tmp = $p[1] + '.part'
    $fs = [IO.File]::Create($tmp); $enc.Save($fs); $fs.Close()
    Move-Item -LiteralPath $tmp -Destination $p[1] -Force
  } catch { Write-Output ('failed: ' + $p[0]) }
}
'''
_photo_locks, _pl_lock = {}, threading.Lock()


def find_photo_files():
    out = []
    for dirpath, dirs, files in os.walk(ROOT):
        if os.path.normcase(dirpath) == os.path.normcase(ROOT):
            dirs[:] = [d for d in dirs if not d.startswith(('_', '.')) and d not in ('Reels', 'Reel Inspirations')]
            continue
        if os.path.basename(dirpath) != 'Photos':
            continue
        stems = {os.path.splitext(f)[0].lower() for f in files if f.lower().endswith(PHOTO_EXT)}
        for f in sorted(files):
            stem, ext = os.path.splitext(f)
            if ext.lower() in PHOTO_EXT or (ext.lower() == '.dng' and stem.lower() not in stems):
                out.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
    return out


def photo_meta(path):
    im = Image.open(path)
    w, h = im.size
    ex = im.getexif()
    if ex.get(0x0112, 1) in (5, 6, 7, 8):
        w, h = h, w
    dt = ex.get_ifd(0x8769).get(36867) or ex.get(306) or ''
    return w, h, str(dt)


def develop_full(dng, ref_jpg):
    """Full-size raw develop (rawpy), with colours matched to the camera's own preview: for each colour channel
    we learn the curve that turns the raw render into the camera's look, then apply it at full size."""
    import numpy as np
    import rawpy
    with rawpy.imread(dng) as raw:
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=16)
    ref = Image.open(ref_jpg).convert('RGB')
    pw, ph = ref.size
    if (rgb.shape[1] > rgb.shape[0]) != (pw > ph):
        raise ValueError('orientation differs from the preview')
    pv = np.asarray(ref, dtype=np.float32)
    small = np.stack([np.asarray(Image.fromarray(rgb[..., i].astype(np.float32), 'F').resize((pw, ph), Image.BOX))
                      for i in range(3)], -1)
    nb = 1024
    centers = (np.arange(nb) + 0.5) / nb * 65536
    luts = []
    for i in range(3):
        x, y = small[..., i].ravel(), pv[..., i].ravel()
        bins = np.clip((x / 65536 * nb).astype(np.int64), 0, nb - 1)
        s, n = np.bincount(bins, weights=y, minlength=nb), np.bincount(bins, minlength=nb)
        ok = n >= 8
        ys = np.convolve(np.pad(s[ok] / n[ok], 2, mode='edge'), np.ones(5) / 5, mode='valid')
        ys = np.maximum.accumulate(ys)
        luts.append(np.clip(np.interp(np.arange(65536), centers[ok], ys) + 0.5, 0, 255).astype(np.uint8))
    return Image.fromarray(np.stack([luts[i][rgb[..., i]] for i in range(3)], -1))


def have_rawpy():
    try:
        import numpy, rawpy  # noqa: F401
        return True
    except Exception:
        return False


def develop_raws(jobs):
    lst, ps = os.path.join(TMP, 'raws.txt'), os.path.join(TMP, 'raws.ps1')
    with open(lst, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(f'{a}\t{b}' for a, b in jobs))
    with open(ps, 'w', encoding='utf-8') as fh:
        fh.write(RAW_PS)
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps, lst],
                       capture_output=True, text=True, timeout=7200, creationflags=LOW)
    bad = [ln for ln in (r.stdout or '').splitlines() if ln.startswith('failed')]
    if bad:
        log(f'{len(bad)} raw photos could not be opened')


def scan_photos():
    pi = os.path.join(META, 'photos.json')
    idx = {}
    if os.path.exists(pi):
        try:
            idx = json.load(open(pi, encoding='utf-8'))
        except Exception:
            idx = {}
    nxt = max([e['id'] for e in idx.values()], default=99999) + 1
    found, raw_jobs = [], []
    for rel in find_photo_files():
        key, full = rel.replace(os.sep, '/'), os.path.join(ROOT, rel)
        try:
            mt = int(os.path.getmtime(full))
        except OSError:
            continue
        e = idx.get(key)
        if e is None:
            e = idx[key] = {'id': nxt}
            nxt += 1
        raw = rel.lower().endswith('.dng')
        dev = os.path.join(P_RAW, f"{e['id']}.jpg")
        if e.get('mt') != mt:                      # new or changed: forget anything made from the old file
            for fp in (dev, os.path.join(P_THUMB, f"{e['id']}.jpg"), os.path.join(P_PREV, f"{e['id']}.jpg")):
                if os.path.exists(fp):
                    os.remove(fp)
            e.pop('w', None)
            e['mt'] = mt
        if 'w' not in e:
            if raw and not os.path.exists(dev):
                raw_jobs.append((full, dev, e))
            else:
                try:
                    e['w'], e['h'], e['dt'] = photo_meta(dev if raw else full)
                    if raw:
                        e['dt'] = str(Image.open(full).getexif().get(306) or '')
                except Exception as ex:
                    log('could not read photo', rel, ex)
        found.append((rel, key, e, raw))
    if raw_jobs:
        print(f'Preparing {len(raw_jobs)} raw photos (only needed once, about a minute)...', flush=True)
        develop_raws([(a, b) for a, b, _ in raw_jobs])
        for full, dev, e in raw_jobs:
            if os.path.exists(dev):
                try:
                    e['w'], e['h'], _ = photo_meta(dev)
                    e['dt'] = str(Image.open(full).getexif().get(306) or '')
                except Exception:
                    pass
    # with rawpy installed, raw photos are developed again at full size (once)
    todo = [(rel, e) for rel, key, e, raw in found if raw and not e.get('full') and 'w' in e]
    if todo and have_rawpy():
        print(f'Developing {len(todo)} raw photos at full size (only needed once - this can take a while)...', flush=True)

        def one(item):
            rel, e = item
            dev = os.path.join(P_RAW, f"{e['id']}.jpg")
            try:
                im = develop_full(os.path.join(ROOT, rel), dev)
                im.save(dev + '.part.jpg', quality=93)
                os.replace(dev + '.part.jpg', dev)
                e['w'], e['h'], e['full'] = im.width, im.height, True
                for fp in (os.path.join(P_THUMB, f"{e['id']}.jpg"), os.path.join(P_PREV, f"{e['id']}.jpg")):
                    if os.path.exists(fp):
                        os.remove(fp)
            except Exception as ex:
                log('raw develop failed', rel, ex)
        for done, item in enumerate(todo, 1):        # one at a time: the raw decoder already uses every CPU core
            one(item)
            if done % 25 == 0 or done == len(todo):
                print(f'  {done}/{len(todo)}', flush=True)
    with open(pi + '.part', 'w', encoding='utf-8') as fh:
        json.dump(idx, fh)
    os.replace(pi + '.part', pi)
    lib = []
    for rel, key, e, raw in found:
        if 'w' not in e:
            continue
        parts = rel.split(os.sep)
        dt = e.get('dt', '')
        lib.append({'id': e['id'], 'kind': 'photo', 'l': '\\'.join(parts[:-2]), 'p': key, 'f': parts[-1], 'g': 'Photos',
                    'o': 'portrait' if e['h'] > e['w'] else 'landscape', 'd': 0, 'w': e['w'], 'h': e['h'],
                    't': [], 's': '', 'n': 1, 'raw': raw, 'full': bool(e.get('full')),
                    'r': (dt[:10].replace(':', '-') + 'T' + dt[11:16]) if len(dt) >= 16 else ''})
    return lib


def photo_src(cid):
    c = CLIPS[cid]
    return os.path.join(P_RAW, f'{cid}.jpg') if c.get('raw') else src_path(cid)


def open_photo(cid, side=None):
    im = Image.open(photo_src(cid))
    if side:
        im.draft('RGB', (side, side))          # fast: let the JPEG decoder skip detail we don't need
    return ImageOps.exif_transpose(im).convert('RGB')


def photo_file(cid, kind):
    """Small copy of a photo for the library ('thumb') or the editor's preview ('prev')."""
    folder, side, q = (P_THUMB, 480, 80) if kind == 'thumb' else (P_PREV, 2048, 88)
    out = os.path.join(folder, f'{cid}.jpg')
    if os.path.exists(out):
        return out
    if not is_photo(cid):
        return None
    with _pl_lock:
        lock = _photo_locks.setdefault((cid, kind), threading.Lock())
    with lock:
        if not os.path.exists(out):
            try:
                im = open_photo(cid, side)
                im.thumbnail((side, side), Image.LANCZOS)
                im.save(out + '.part.jpg', quality=q)
                os.replace(out + '.part.jpg', out)
            except Exception as e:
                log('photo preview failed', cid, e)
                return None
    return out


def photo_warmer():
    """Make the library thumbnails for every photo in the background."""
    for c in list(PHOTOS) + [c for c in list(COLL_ITEMS) if c.get('kind') == 'photo']:
        if STOPPING:
            return
        if not os.path.exists(os.path.join(P_THUMB, f"{c['id']}.jpg")):
            photo_file(c['id'], 'thumb')
            time.sleep(0.005)


# ---------------------------------------------------------------------------- extra folders (collections)
TAG_WORDS = [('Food', ('drink', 'glass', 'cocktail', 'food', 'plate', 'table', 'flute', 'tumbler', 'garnish', 'spritz', 'sour')),
             ('People', ('guest', 'woman', 'man ', 'people', 'group', 'model', 'laugh', 'story', 'portrait', 'everyone', 'friends')),
             ('Detail', ('close-up', 'close', 'garnish', 'detail')), ('Indoor', ('room', 'sofa', 'table', 'wall', 'lamp', 'indoor')),
             ('Night', ('night', 'lights', 'string lights', 'candle'))]


def coll_index_path(key):
    return os.path.join(COLL_DIR, f'{key}.json')


def coll_thumb(cid, k):
    return os.path.join(CTHUMBS, f'{cid:04d}_{k:02d}.jpg')


def read_clip_list(root, key=None):
    """Descriptions from a "_Clip list.csv" (or "Clip list.csv") at the top of the folder - or, when the user prefers
    nothing written into their footage folder, from cache\\notes\\<key>.csv: file name -> (text, tags)."""
    import csv
    out = {}
    for fp in [os.path.join(root, n) for n in ('_Clip list.csv', 'Clip list.csv')] + ([os.path.join(CACHE, 'notes', f'{key}.csv')] if key else []):
        if not os.path.exists(fp):
            continue
        try:
            with open(fp, encoding='utf-8-sig') as fh:
                for r in csv.DictReader(fh):
                    f = (r.get('File') or r.get('file') or '').strip()
                    if not f:
                        continue
                    desc = next((v for k, v in r.items() if k and any(w in k.lower() for w in ('what happens', 'description', 'desc'))), '') or ''
                    good = next((v for k, v in r.items() if k and k.lower().startswith('good for')), '') or ''
                    out[f.lower()] = (desc.strip(), good.strip())
        except Exception as e:
            log('could not read', fp, e)
        break
    return out


def guess_tags(text, folder):
    hay = (' ' + text + ' ' + folder + ' ').lower()
    return [t for t, words in TAG_WORDS if any(w in hay for w in words)]


def probe_video(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,r_frame_rate:stream_side_data=rotation:stream_tags=rotate:format=duration',
                        '-of', 'json', path], capture_output=True, text=True, encoding='utf-8', errors='replace', creationflags=LOW)
    j = json.loads(r.stdout or '{}')
    s = (j.get('streams') or [{}])[0]
    w, h = int(s.get('width', 0)), int(s.get('height', 0))
    rot = 0
    for sd in s.get('side_data_list', []) or []:
        if 'rotation' in sd:
            rot = int(sd['rotation'])
    if (s.get('tags') or {}).get('rotate'):
        rot = int(s['tags']['rotate'])
    if abs(rot) in (90, 270):
        w, h = h, w
    num, den = (str(s.get('r_frame_rate', '30/1')) + '/1').split('/')[:2]
    fps = round(int(num) / max(1, int(den)), 2) if num.isdigit() and den.isdigit() else 30.0
    return float((j.get('format') or {}).get('duration', 0) or 0), w, h, fps


def recorded_at(path):
    m = re.search(r'(20\d{6})_?(\d{6})', os.path.basename(path))           # DJI_20261121203747_0961_D.MP4
    if m:
        d, t = m.groups()
        return f'{d[:4]}-{d[4:6]}-{d[6:]}T{t[:2]}:{t[2:4]}'
    return time.strftime('%Y-%m-%dT%H:%M', time.localtime(os.path.getmtime(path)))


def make_coll_thumbs(e, root):
    """Four little frames across a clip (like the Europe catalogue thumbnails), from DJI's .LRF copy when there is one."""
    os.makedirs(CTHUMBS, exist_ok=True)
    full = os.path.join(root, e['p'].replace('/', os.sep))
    stem = os.path.splitext(os.path.basename(full))[0]
    src = next((p for p in (os.path.splitext(full)[0] + '.LRF', os.path.join(root, '_LRF proxies', stem + '.LRF')) if os.path.exists(p)), full)
    vf = 'scale=180:320' if e['o'] == 'portrait' else 'scale=320:180'
    if e['w'] and e['h'] and abs(e['w'] / e['h'] - (9 / 16 if e['o'] == 'portrait' else 16 / 9)) > 0.02:
        vf = ('scale=180:320:force_original_aspect_ratio=increase,crop=180:320' if e['o'] == 'portrait'
              else 'scale=320:180:force_original_aspect_ratio=increase,crop=320:180')
    n = e.get('n', 4)
    for k in range(n):
        out = coll_thumb(e['id'], k)
        if os.path.exists(out):
            continue
        t = max(0.0, e['d'] * (k + 0.5) / n - 0.05)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', src, '-frames:v', '1', '-vf', vf, '-q:v', '4', out],
                       capture_output=True, creationflags=LOW)


def scan_collection(key, prog=None):
    """(Re)scan one extra folder. Known files keep their ids; new or changed files are read. Returns its items."""
    C = COLLS[key]
    root, skip = C['root'], {s.lower() for s in C.get('skip', [])}
    idxp = coll_index_path(key)
    try:
        old = {e['p']: e for e in json.load(open(idxp, encoding='utf-8'))}
    except Exception:
        old = {}
    nxt = max([e['id'] for e in old.values()], default=C['base'] - 1) + 1
    files = []
    out_dir = os.path.normcase(os.path.normpath(C.get('out') or ''))          # exported reels are not footage
    for dp, dns, fns in os.walk(root):
        rel_dir = os.path.relpath(dp, root)
        dns[:] = sorted(d for d in dns if not d.startswith(('_', '.')) and d.lower() not in skip
                        and os.path.normpath(os.path.join(rel_dir, d)).lower() not in skip
                        and os.path.normcase(os.path.normpath(os.path.join(dp, d))) != out_dir)
        for fn in sorted(fns):
            if fn.lower().endswith(VIDEO_EXT + PHOTO_EXT) and not fn.startswith(('~', '.')):
                files.append(os.path.normpath(os.path.join(rel_dir, fn)))
    notes = read_clip_list(root, key)
    items = []
    for i, rel in enumerate(files):
        p = rel.replace(os.sep, '/')
        full = os.path.join(root, rel)
        try:
            mt = int(os.path.getmtime(full))
        except OSError:
            continue
        e = old.get(p)
        if e is None or e.get('mt') != mt:
            cid = e['id'] if e else nxt
            if not e:
                nxt += 1
            photo = rel.lower().endswith(PHOTO_EXT)
            parts = rel.split(os.sep)
            folder = '\\'.join(parts[:-1]) or C['name']
            desc, good = notes.get(parts[-1].lower(), ('', ''))
            try:
                if photo:
                    w, h, _ = photo_meta(full)
                    d, fps = 0, 0
                else:
                    d, w, h, fps = probe_video(full)
            except Exception as ex:
                log('could not read', full, ex)
                continue
            if not w or not h or (not photo and d <= 0):
                continue
            e = {'id': cid, 'col': key, 'l': folder, 'p': p, 'f': parts[-1], 'g': parts[-2] if len(parts) > 1 else C['name'],
                 'o': 'portrait' if h > w else 'landscape', 'd': round(d, 2), 'fps': fps, 'w': w, 'h': h, 'hdr': False, 'cam': '',
                 't': guess_tags(desc + ' ' + good, folder), 's': desc, 'n': 1 if photo else 4, 'r': recorded_at(full), 'mt': mt}
            if photo:
                e.update(kind='photo', raw=False, full=False)
            for k in range(4):                                  # changed file: old thumbnails are out of date
                fp = coll_thumb(cid, k)
                if os.path.exists(fp):
                    os.remove(fp)
        note = notes.get(e['f'].lower())                       # descriptions can be written or improved later
        if note and note[0] and note[0] != e.get('s'):
            e['s'], e['t'] = note[0], guess_tags(note[0] + ' ' + note[1], e['l'])
        if e.get('kind') != 'photo':
            make_coll_thumbs(e, root)
        items.append(e)
        if prog:
            prog(i + 1, len(files))
    os.makedirs(COLL_DIR, exist_ok=True)
    with open(idxp + '.part', 'w', encoding='utf-8') as fh:
        json.dump(items, fh, ensure_ascii=False)
    os.replace(idxp + '.part', idxp)
    return items


def load_collection_items(key):
    try:
        return json.load(open(coll_index_path(key), encoding='utf-8'))
    except Exception:
        return []


def install_items(key, items):
    """Swap one folder's items into the live library."""
    COLL_ITEMS[:] = [c for c in COLL_ITEMS if c.get('col') != key] + items
    for cid in [i for i, c in CLIPS.items() if c.get('col') == key]:
        del CLIPS[cid]
    CLIPS.update({c['id']: c for c in items})


def scan_job(key):
    C = COLLS[key]
    SCAN.update(state='running', key=key, name=C['name'], done=0, total=0, msg='', first='')
    try:
        items = scan_collection(key, lambda a, b: SCAN.update(done=a, total=b))
        install_items(key, items)
        first = ensure_first_project()
        SCAN.update(state='done', msg=f"{len(items)} clips and photos", first=first or '')
        for c in items:
            if c.get('kind') != 'photo':
                request_proxy(c['id'], 3)
    except Exception as e:
        traceback.print_exc()
        SCAN.update(state='error', msg=str(e)[:300])


def add_collection(path, name, background=True):
    path = os.path.normpath(os.path.expandvars(os.path.expanduser(str(path or '').strip().strip('"'))))
    if not os.path.isdir(path):
        raise ValueError(f'Folder not found: {path}')
    for C in COLLS.values():
        if os.path.normcase(C['root']) == os.path.normcase(path):
            return C['key']
    if LEGACY and os.path.normcase(path).startswith(os.path.normcase(ROOT)):
        raise ValueError('That folder is already part of the built-in trip folder.')
    if os.path.normcase(path).startswith(os.path.normcase(HERE)):
        raise ValueError('That is Reel Studio’s own folder. Pick the folder where your videos are.')
    if SCAN['state'] == 'running':
        raise ValueError('Another folder is still being scanned. Try again when it has finished.')
    name = (str(name or '').strip() or os.path.basename(path))[:60]
    key = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:24] or 'folder'
    while key in COLLS:
        key += '-2'
    base = max([C['base'] for C in COLLS.values()], default=0) + 1_000_000
    COLLS[key] = {'key': key, 'name': name, 'root': path, 'out': os.path.join(path, 'Reels'), 'skip': [], 'base': base}
    save_collections()
    if background:
        SCAN.update(state='running', key=key, name=name, done=0, total=0, msg='')
        threading.Thread(target=scan_job, args=(key,), daemon=True).start()
    return key


def collections_info():
    counts = {}
    for c in LIB + PHOTOS + COLL_ITEMS:
        counts[c.get('col', 'europe')] = counts.get(c.get('col', 'europe'), 0) + 1
    return [{'key': C['key'], 'name': C['name'], 'root': C['root'], 'out': C['out'], 'count': counts.get(C['key'], 0)} for C in COLLS.values()]


def out_dir_for(p):
    """Exports go to the folder most of the reel's shots come from: its "out" folder (by default <footage folder>\\Reels)."""
    votes = {}
    for s in p.get('slots', []):
        k = CLIPS.get(int(s['clip']), {}).get('col', 'europe')
        votes[k] = votes.get(k, 0) + 1
    key = max(votes, key=votes.get) if votes else 'europe'
    d = (COLLS.get(key) or {'out': REELS})['out']
    os.makedirs(d, exist_ok=True)
    return d


# =====================================================================================
# Carousel Studio: every carousel is a folder in <trip>\Carousels (or Reel Studio\Carousels) with carousel.json + photos\
# =====================================================================================
CAROUSELS = os.path.join(ROOT, 'Carousels')
CCACHE = os.path.join(CACHE, 'carousel')
os.makedirs(os.path.join(CCACHE, 'thumbs'), exist_ok=True)
os.makedirs(os.path.join(CCACHE, 'r'), exist_ok=True)
IMG_EXT = ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp')
_rseq = itertools.count(int(time.time()))


def carousel_dir(name, must_exist=True):
    n = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', str(name or '')).strip().rstrip('.')
    if not n or n in ('.', '..'):
        raise ValueError('bad carousel name')
    d = os.path.join(CAROUSELS, n)
    if must_exist and not os.path.isfile(os.path.join(d, 'carousel.json')):
        raise ValueError('no such carousel')
    return d


def list_carousels():
    out = []
    if os.path.isdir(CAROUSELS):
        for n in sorted(os.listdir(CAROUSELS)):
            fp = os.path.join(CAROUSELS, n, 'carousel.json')
            if os.path.isfile(fp):
                try:
                    sp = json.load(open(fp, encoding='utf-8'))
                    out.append({'name': n, 'format': sp.get('format'), 'slides': len(sp.get('slides', [])), 'updated': os.path.getmtime(fp)})
                except Exception:
                    pass
    return out


def read_carousel(name):
    d = carousel_dir(name)
    return CE.clean_spec(json.load(open(os.path.join(d, 'carousel.json'), encoding='utf-8')))


def write_carousel(name, spec):
    d = carousel_dir(name, must_exist=False)
    os.makedirs(os.path.join(d, 'photos'), exist_ok=True)
    spec = CE.clean_spec(spec)
    spec['name'] = os.path.basename(d)
    tmp = os.path.join(d, 'carousel.json.part')
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(d, 'carousel.json'))
    return spec


def carousel_photos(name):
    d = os.path.join(carousel_dir(name), 'photos')
    out = []
    for f in os.listdir(d) if os.path.isdir(d) else []:
        if f.lower().endswith(IMG_EXT):
            fp = os.path.join(d, f)
            try:
                with Image.open(fp) as im:
                    w, h = im.size
                    if im.getexif().get(0x0112, 1) in (5, 6, 7, 8):
                        w, h = h, w
            except Exception:
                w = h = 0
            out.append({'file': f, 'mtime': os.path.getmtime(fp), 'w': w, 'h': h})
    out.sort(key=lambda p: -p['mtime'])
    return out


def safe_label(s):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s).strip() or 'photo'


def carousel_add(name, cid, t=None):
    """Copy a library photo (or a video frame at t seconds) into the carousel's photos folder, full size."""
    d = os.path.join(carousel_dir(name, must_exist=False), 'photos')
    os.makedirs(d, exist_ok=True)
    c = CLIPS[int(cid)]
    place = safe_label(c['l'].split('\\')[0])
    if c.get('kind') == 'photo':
        fn = f"{place} {c['id']}.jpg"
        fp = os.path.join(d, fn)
        if not os.path.exists(fp):
            im = open_photo(c['id'])
            im.save(fp + '.part.jpg', quality=95, subsampling=0)
            os.replace(fp + '.part.jpg', fp)
        return fn
    t = max(0.0, min(float(t or 0), max(0.0, c['d'] - 0.05)))
    fn = f"{place} frame {c['id']} {t:.1f}s.jpg"
    fp = os.path.join(d, fn)
    if not os.path.exists(fp):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', src_path(c['id']), '-frames:v', '1',
                            '-q:v', '1', '-pix_fmt', 'yuvj444p', fp + '.part.jpg'], capture_output=True)
        if r.returncode != 0 or not os.path.exists(fp + '.part.jpg'):
            raise RuntimeError('could not take that frame: ' + r.stderr.decode(errors='replace')[-200:])
        os.replace(fp + '.part.jpg', fp)
    return fn


def carousel_thumb(name, file):
    fp = os.path.join(carousel_dir(name), 'photos', os.path.basename(file))
    if not os.path.isfile(fp):
        return None
    key = hashlib.sha1(f'{fp}|{os.path.getmtime(fp)}'.encode('utf-8')).hexdigest()[:16]
    out = os.path.join(CCACHE, 'thumbs', key + '.jpg')
    if not os.path.exists(out):
        im = Image.open(fp)
        im.draft('RGB', (400, 400))
        im = ImageOps.exif_transpose(im).convert('RGB')
        im.thumbnail((400, 400))
        im.save(out, quality=82)
    return out


def carousel_render(name, spec):
    d = carousel_dir(name)
    slides, boxes = CE.render(d, spec)
    tok = f'{next(_rseq)}'
    rd = os.path.join(CCACHE, 'r', tok)
    os.makedirs(rd)
    urls = []
    for i, s in enumerate(slides):
        s.resize((540, 675), Image.LANCZOS).save(os.path.join(rd, f'{i:02d}.jpg'), quality=88)
        urls.append(f'/cr/{tok}/{i:02d}.jpg')
    old = sorted(os.listdir(os.path.join(CCACHE, 'r')), key=lambda x: int(x) if x.isdigit() else 0)
    for o in old[:-40]:
        shutil.rmtree(os.path.join(CCACHE, 'r', o), ignore_errors=True)
    return {'slides': urls, 'boxes': boxes}


def template_slides(fmt):
    """The template's sample slides (kind + sample words), empty photo spots."""
    out = []
    for item in CE.FORMATS[fmt]['default']:
        kind, over = (item, None) if isinstance(item, str) else (item[0], item[1])
        out.append(CE.empty_slide(fmt, kind, over))
    return out


def carousel_new(name, fmt, source=None):
    """A new carousel from a template. With source, it reuses that carousel's photos, in the order they appear."""
    d = carousel_dir(name, must_exist=False)
    if os.path.exists(os.path.join(d, 'carousel.json')):
        raise ValueError('a carousel with that name already exists')
    F = CE.FORMATS[fmt]
    spec = {'name': name, 'format': fmt, 'look': {'grade': F['look'][0], 'amt': F['look'][1]}, 'slides': template_slides(fmt)}
    if source:
        src = read_carousel(source)
        sd = os.path.join(carousel_dir(source), 'photos')
        os.makedirs(os.path.join(d, 'photos'), exist_ok=True)
        files = []
        for sl in src['slides']:
            for p in sl['photos']:
                if p and p['file'] not in files:
                    files.append(p['file'])
        files += [p['file'] for p in carousel_photos(source) if p['file'] not in files]
        for f in files:
            if os.path.exists(os.path.join(sd, f)) and not os.path.exists(os.path.join(d, 'photos', f)):
                shutil.copy2(os.path.join(sd, f), os.path.join(d, 'photos', f))
        k = 0
        for sl in spec['slides']:
            for i in range(len(sl['photos'])):
                if files:
                    sl['photos'][i] = {'file': files[k % len(files)], 'cx': 0.5, 'cy': 0.5, 'zoom': 1}
                    k += 1
        spec['look'] = src.get('look', spec['look'])
    return write_carousel(name, spec)


SAMPLE_IDS = [100660, 100673, 100621, 100905, 100884, 100857, 101003, 101050, 101075, 101352, 101363, 101316, 101333, 101334,
              101141, 101166, 101241, 101437, 101394, 100771, 100787, 101297, 101304, 100929, 101412, 101066]
_sample_lock = threading.Lock()


def sample_folder():
    """A hidden folder of example photos, used to draw the template gallery: the original trip's picks, else photos or
    video frames from your own folders, else plain colour cards (so the gallery always works)."""
    d = os.path.join(CCACHE, 'samples')
    os.makedirs(os.path.join(d, 'photos'), exist_ok=True)
    with _sample_lock:
        ids = [cid for cid in SAMPLE_IDS if cid in CLIPS]
        if not ids:
            mine = [c for c in COLL_ITEMS if c.get('kind') == 'photo'] or [c for c in COLL_ITEMS if c.get('d', 0) > 1]
            ids = [c['id'] for c in mine[:: max(1, len(mine) // 26)][:26]]
        for cid in ids:
            fp = os.path.join(d, 'photos', f'{cid}.jpg')
            if os.path.exists(fp):
                continue
            try:
                if is_photo(cid):
                    im = open_photo(cid, 1600)
                    im.thumbnail((1600, 1600), Image.LANCZOS)
                    im.save(fp, quality=88)
                else:
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{CLIPS[cid]['d'] / 2:.2f}", '-i', src_path(cid), '-frames:v', '1',
                                    '-vf', 'scale=1600:1600:force_original_aspect_ratio=decrease', '-q:v', '3', fp], capture_output=True)
            except Exception as e:
                log('sample photo failed', cid, e)
        files = [f'{cid}.jpg' for cid in ids if os.path.exists(os.path.join(d, 'photos', f'{cid}.jpg'))]
        if not files:
            for i, col in enumerate([(120, 96, 80), (70, 92, 110), (150, 120, 70), (90, 110, 80), (130, 90, 100), (60, 70, 90)]):
                fp = os.path.join(d, 'photos', f'blank{i}.jpg')
                if not os.path.exists(fp):
                    Image.new('RGB', (1080, 1350), col).save(fp, quality=90)
                files.append(f'blank{i}.jpg')
    return d, files


def template_preview(fmt):
    """First slides of a template, filled with example photos (cached)."""
    if fmt not in CE.FORMATS:
        return None
    fdir = os.path.join(HERE, 'fonts')
    ver = hashlib.sha1(b''.join(open(os.path.join(HERE, f), 'rb').read() for f in sorted(os.listdir(HERE))
                                if f.startswith('carousel_') and f.endswith('.py')) +
                       '|'.join(sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []).encode()).hexdigest()[:10]
    out = os.path.join(CCACHE, 'formats', f'{fmt}_{ver}.jpg')
    if os.path.exists(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    d, files = sample_folder()
    slides = template_slides(fmt)
    k = (sum(map(ord, fmt)) * 7) % max(1, len(files))
    for sl in slides:
        for i in range(len(sl['photos'])):
            sl['photos'][i] = {'file': files[k % len(files)], 'cx': 0.5, 'cy': 0.5, 'zoom': 1}
            k += 1
    F = CE.FORMATS[fmt]
    spec = {'name': fmt, 'format': fmt, 'look': {'grade': F['look'][0], 'amt': F['look'][1]}, 'slides': slides}
    imgs, _ = CE.render(d, spec)
    imgs = imgs[:3]
    tw, th = 216, 270
    sheet = Image.new('RGB', (len(imgs) * (tw + 6) - 6, th), (24, 24, 26))
    for i, s in enumerate(imgs):
        sheet.paste(s.resize((tw, th), Image.LANCZOS), (i * (tw + 6), 0))
    sheet.save(out, quality=86)
    return out


# =====================================================================================
# Preview proxies (small H.264 copies the browser can play and scrub smoothly)
# =====================================================================================
PSTAT = {}
PQ = queue.PriorityQueue()          # background warm-up
UQ = queue.LifoQueue()              # clips you just clicked: newest first, a dedicated worker takes these right away
_seq = itertools.count()
_plock = threading.Lock()
_urgent = set()


def proxy_file(cid):
    return os.path.join(PROXIES, f'{cid}.mp4')


def request_proxy(cid, prio):
    with _plock:
        if os.path.exists(proxy_file(cid)):
            PSTAT[cid] = 'ready'
            return 'ready'
        st = PSTAT.get(cid)
        if st == 'error':
            return st
        if st in ('queued', 'working'):
            if prio == 0 and st == 'queued' and cid not in _urgent:
                _urgent.add(cid); UQ.put(cid)
            return st
        PSTAT[cid] = 'queued'
        if prio == 0:
            _urgent.add(cid); UQ.put(cid)
        else:
            PQ.put((prio, next(_seq), cid))
        return 'queued'


def proxy_worker(urgent_only=False):
    while True:
        urgent = True
        if urgent_only:
            cid = UQ.get()
        else:
            try:
                cid = UQ.get_nowait()
            except queue.Empty:
                _, _, cid = PQ.get()
                urgent = False
        with _plock:
            if PSTAT.get(cid) in ('working', 'ready') or os.path.exists(proxy_file(cid)):
                if os.path.exists(proxy_file(cid)):
                    PSTAT[cid] = 'ready'
                continue
            if STOPPING:
                return
            PSTAT[cid] = 'working'
        tmp = os.path.join(PROXIES, f'{cid}.part.mp4')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-hwaccel', 'auto', '-i', lrf_path(cid) or src_path(cid), '-vf',
               "fps=30,scale='if(gt(iw,ih),960,-2)':'if(gt(iw,ih),-2,960)':flags=bilinear,format=yuv420p",
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-g', '15', '-an', '-movflags', '+faststart', tmp]
        try:
            flags = 0 if urgent else getattr(subprocess, 'BELOW_NORMAL_PRIORITY_CLASS', 0)
            r = subprocess.run(cmd, capture_output=True, creationflags=flags)
            ok = r.returncode == 0 and os.path.exists(tmp)
            if ok:
                os.replace(tmp, proxy_file(cid))
            with _plock:
                PSTAT[cid] = 'ready' if ok else 'error'
            if not ok:
                log('preview copy failed', cid, r.stderr[-300:])
        except Exception:
            traceback.print_exc()
            with _plock:
                PSTAT[cid] = 'error'


_slock = threading.Lock()


def strip_file(cid):
    out = os.path.join(STRIPS, f'{cid}.jpg')
    if os.path.exists(out):
        return out
    if not os.path.exists(proxy_file(cid)):
        return None
    with _slock:
        if not os.path.exists(out):
            d = max(0.4, CLIPS[cid]['d'])
            n = 14
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', proxy_file(cid), '-vf',
                            f'fps={n / d:.5f},scale=-2:90,tile={n}x1', '-frames:v', '1', out])
    return out if os.path.exists(out) else None


# =====================================================================================
# Export (full quality render)
# =====================================================================================
JOB = {'state': 'idle', 'msg': '', 'done': 0, 'total': 0, 'file': None}


REEL_FORMATS = {'9:16': (1080, 1920), '4:5': (1080, 1350), '1:1': (1080, 1080), '16:9': (1920, 1080)}
FILLS = ('crop', 'blur', 'bars')
# export quality: size multiplier, sharpening (ffmpeg's contrast-adaptive sharpen, on brightness only), final x264 settings,
# file-name suffix. Clips are always cut from the original files (4K for most), so 2K keeps detail that 1080p throws away.
QUALITIES = {
    'std':   dict(scale=1,     sharp=0,    crf=17, preset='medium', suffix=''),
    'sharp': dict(scale=1,     sharp=0.45, crf=15, preset='slow',   suffix=' (sharp)'),
    '2k':    dict(scale=4 / 3, sharp=0.4,  crf=15, preset='slow',   suffix=' (2K)'),
    '4k':    dict(scale=2,     sharp=0.4,  crf=16, preset='slow',   suffix=' (4K)'),
}


def fit_mode(p, s):
    """How shot s fills the frame: its own choice, else the reel's. crop = cut to fill, blur = whole clip over a blurred
    copy of itself, bars = whole clip with black bars."""
    f = s.get('fit')
    if f is True or f == 'bars':
        return 'bars'
    if f in ('blur', 'crop'):
        return f
    return p.get('fill') if p.get('fill') in FILLS else 'crop'


SPEEDS = (0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4)


def speed_of(s):
    try:
        v = float(s.get('speed', 1) or 1)
    except (TypeError, ValueError):
        return 1
    return v if v in SPEEDS else 1


def rot_of(s):
    r = int(s.get('rot', 0) or 0) % 360
    return r if r in (90, 180, 270) else 0


def rotated_size(c, s):
    return (c['h'], c['w']) if rot_of(s) in (90, 270) else (c['w'], c['h'])


def crop_rect(iw, ih, s):
    ar = W / H                                  # the reel's shape (9:16, 4:5, 1:1 or 16:9)
    if iw / ih > ar:
        bh, bw = ih, ih * ar
    else:
        bw, bh = iw, iw / ar
    z = max(1.0, float(s.get('zoom', 1) or 1))
    w, h = bw / z, bh / z
    x = max(0.0, min(iw - w, float(s.get('cx', 0.5)) * iw - w / 2))
    y = max(0.0, min(ih - h, float(s.get('cy', 0.5)) * ih - h / 2))
    ev = lambda v: int(v) // 2 * 2
    return ev(x), ev(y), max(2, ev(w)), max(2, ev(h))


def frame_filter(s, c, mode='crop'):
    pre = {90: 'transpose=1,', 180: 'hflip,vflip,', 270: 'transpose=2,'}.get(rot_of(s), '')
    if mode == 'bars':
        return pre + f'scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black'
    if mode == 'blur':                          # same idea as the preview: a soft, slightly darker cover behind the whole clip
        bw, bh = max(2, W // 8 // 2 * 2), max(2, H // 8 // 2 * 2)
        return (pre + f'split[fa][fb];[fa]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},gblur=sigma=5,'
                f'eq=brightness=-0.06,scale={W}:{H}:flags=bicubic[bg];[fb]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg];'
                f'[bg][fg]overlay=(W-w)/2:(H-h)/2')
    iw, ih = rotated_size(c, s)
    x, y, w, h = crop_rect(iw, ih, s)
    return pre + f'crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos'


def render_segment(s, n, lut, out, mode='crop'):
    c = CLIPS[int(s['clip'])]
    if c.get('kind') == 'photo':
        return render_photo_segment(s, c, n, lut, out, mode)
    sp = speed_of(s)
    need = n / FPS * sp                         # seconds of the clip this shot uses (0.5 = slow motion)
    start = max(0.0, min(float(s.get('in', 0)), max(0.0, c['d'] - need)))
    vf = ('' if sp == 1 else f'setpts=PTS/{sp},') + f"fps={FPS},{frame_filter(s, c, mode)},setsar=1{look_chain(lut)}"
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.3f}']
    if s.get('reverse'):
        cmd += ['-t', f'{need + 0.05:.3f}', '-i', src_path(c['id']), '-vf', vf + ',reverse,tpad=stop_mode=clone:stop_duration=30']
    else:
        cmd += ['-i', src_path(c['id']), '-vf', vf + ',tpad=stop_mode=clone:stop_duration=30']
    cmd += ['-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p'] + COLOR_TAGS + [out]
    subprocess.run(cmd, check=True, capture_output=True, cwd=LUTS)


def move_zoom(move, i, n):
    """Slow zoom for photos: how much extra zoom at frame i of n. Same formula as moveAt() in studio.html."""
    p = i / (n - 1) if n > 1 else 0.0
    return 1 + 0.08 * p if move == 'in' else (1.08 - 0.08 * p if move == 'out' else 1.0)


def crop_box(iw, ih, s, zoom):
    """Float crop box, same maths as cropRect() in studio.html."""
    ar = W / H
    if iw / ih > ar:
        bh, bw = ih, ih * ar
    else:
        bw, bh = iw, iw / ar
    z = max(1.0, zoom)
    w, h = bw / z, bh / z
    x = max(0.0, min(iw - w, float(s.get('cx', 0.5)) * iw - w / 2))
    y = max(0.0, min(ih - h, float(s.get('cy', 0.5)) * ih - h / 2))
    return (x, y, x + w, y + h)


def photo_frames(im, s, n, mode='crop'):
    move = s.get('move') or 'none'
    r = rot_of(s)
    if r:
        im = im.transpose({90: Image.ROTATE_270, 180: Image.ROTATE_180, 270: Image.ROTATE_90}[r])
    if mode in ('bars', 'blur'):
        sc = min(W / im.width, H / im.height)
        dw, dh = max(1, round(im.width * sc)), max(1, round(im.height * sc))
        if mode == 'blur':
            sm = im.copy()
            sm.thumbnail((W // 8 * 2, H // 8 * 2))
            cov = max(W / 8 / sm.width, H / 8 / sm.height)
            sm = sm.resize((max(1, round(sm.width * cov)), max(1, round(sm.height * cov))), Image.BILINEAR)
            l, t = (sm.width - W // 8) // 2, (sm.height - H // 8) // 2
            sm = sm.crop((l, t, l + W // 8, t + H // 8)).filter(ImageFilter.GaussianBlur(5))
            base = ImageEnhance.Brightness(sm.resize((W, H), Image.BICUBIC)).enhance(0.86)
        else:
            base = Image.new('RGB', (W, H))
        base.paste(im.resize((dw, dh), Image.LANCZOS), ((W - dw) // 2, (H - dh) // 2))
        if move == 'none':
            frame = base.tobytes()
            for _ in range(n):
                yield frame
            return
        for i in range(n):
            z = move_zoom(move, i, n)
            w, h = W / z, H / z
            yield base.resize((W, H), Image.BICUBIC, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2)).tobytes()
        return
    z0 = max(1.0, float(s.get('zoom', 1) or 1))
    if move == 'none':
        frame = im.resize((W, H), Image.LANCZOS, box=crop_box(im.width, im.height, s, z0)).tobytes()
        for _ in range(n):
            yield frame
        return
    x0, y0, x1, y1 = crop_box(im.width, im.height, s, z0)
    f = min(1.0, W * 1.3 / (x1 - x0))                  # shrink once so every frame is quick to draw
    if f < 1.0:
        im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
    for i in range(n):
        yield im.resize((W, H), Image.BICUBIC, box=crop_box(im.width, im.height, s, z0 * move_zoom(move, i, n))).tobytes()


def render_photo_segment(s, c, n, lut, out, mode='crop'):
    im = open_photo(c['id'])
    vf = (lut + ',' if lut else '') + 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', str(FPS), '-i', '-',
           '-vf', vf, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p'] + COLOR_TAGS + [out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=LUTS)
    err = []
    threading.Thread(target=lambda: err.append(proc.stderr.read()), daemon=True).start()
    try:
        for fr_ in photo_frames(im, s, n, mode):
            proc.stdin.write(fr_)
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        time.sleep(0.2)
        raise RuntimeError('photo shot failed: ' + (err[0] if err else b'').decode(errors='replace')[-300:])


def safe_name(name):
    n = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name or '').strip().rstrip('.')
    return n or 'Untitled reel'


def text_frames(p, total):
    """Yield the RGBA text overlay for every frame (only re-drawn when something changes).
    Texts are designed on the 1080 x 1920 reel. For other shapes the whole text layer is drawn on a larger 'virtual'
    frame of the same shape and scaled down, so texts keep their size and spacing relative to the frame height
    (same as textScale() in studio.html)."""
    global W, H, TS
    FW, FH = W, H
    k = min(FW / 1080, FH / 1920)
    VW, VH = round(FW / k), round(FH / k)
    texts = [L for L in p['texts'] if L['text'].strip()]
    if k > 1.001:
        # bigger than the design (2K / 4K export): draw the texts themselves bigger, so they stay sharp
        VW, VH = FW, FH
        texts = [dict(L, size=max(1, round(int(L.get('size', 60)) * k)), r=round(int(L.get('r', 542)) * k)) for L in texts]
        TS = k
    try:
        layers = [(L, text_resources(L)) for L in texts]
    finally:
        TS = 1.0
    blank = bytes(FW * FH * 4)
    last_key, last = None, blank
    for i in range(total):
        state = []
        for idx, (L, R) in enumerate(layers):
            if L['f0'] <= i < L['f1']:
                a = text_alpha(L, i)
                if a > 0:
                    state.append((idx, text_visible(L, i, R), a))
        key = tuple(state)
        if key != last_key:
            if not state:
                last = blank
            else:
                W, H = VW, VH                    # draw_layer places texts with the module's W and H
                TS = k if (VW, VH) == (FW, FH) and k > 1.001 else 1.0
                try:
                    canvas = Image.new('RGBA', (VW, VH), (0, 0, 0, 0))
                    for idx, vis, a in state:
                        L, R = layers[idx]
                        draw_layer(canvas, L, R, vis, a)
                finally:
                    W, H, TS = FW, FH, 1.0
                if (VW, VH) != (FW, FH):
                    canvas = canvas.resize((FW, FH), Image.LANCZOS)
                last = canvas.tobytes()
            last_key = key
        yield last


def render_project(p, fmt=None, quality='std'):
    """Export at the reel's format, or at fmt when given (the same reel can go out vertical and landscape),
    at the chosen quality (1080p, 1080p sharpened, 2K or 4K)."""
    global W, H
    fmt = fmt if fmt in REEL_FORMATS else p.get('format', '9:16')
    Q = QUALITIES.get(quality) or QUALITIES['std']
    bw, bh = REEL_FORMATS.get(fmt, (1080, 1920))
    W, H = int(round(bw * Q['scale'] / 2)) * 2, int(round(bh * Q['scale'] / 2)) * 2
    try:
        return _render_project(p, fmt, Q)
    finally:
        W, H = 1080, 1920


def _render_project(p, fmt, Q=QUALITIES['std']):
    T = TEMPLATES[p['template']]
    total = T['total']
    b = [0] + p['cuts'] + [total]
    work = os.path.join(TMP, 'render')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    JOB.update(total=len(p['slots']) + 1, done=0)
    listing = []
    for k, s in enumerate(p['slots']):
        seg = os.path.join(work, f'seg{k:02d}.mp4')
        render_segment(s, b[k + 1] - b[k], look_filter(*colour_of(p, s, T)), seg, fit_mode(p, s))
        listing.append(f"file '{seg}'")
        JOB['done'] = k + 1
    with open(os.path.join(work, 'list.txt'), 'w') as fh:
        fh.write('\n'.join(listing))
    dur = total / FPS
    fname = safe_name(p['name']) + ('' if fmt == '9:16' else f" ({fmt.replace(':', 'x')})") + Q['suffix'] + '.mp4'
    od = out_dir_for(p)
    JOB['dir'] = od
    out = os.path.join(od, fname)
    tmp_out = os.path.join(work, 'final.mp4')
    # film effects for the whole reel, under the text: (sharpening,) vignette (dark corners), then grain
    fx = clean_fx(p.get('fx'))
    sharpen = f",cas=strength={Q['sharp']}:planes=1" if Q['sharp'] else ''
    # each shot's file holds exactly its own frames, but their timestamps can start a frame late; joined as they are, the cuts
    # drifted later and later (up to 4 frames by the end of a 23-cut reel) and 3-5 frame shots got swallowed.
    # Numbering the frames afresh puts every cut exactly on its beat.
    extra, chain, base = [], f'[0:v]setpts=N/({FPS}*TB){sharpen}[b0];', 'b0'
    if fx.get('vig'):
        extra += ['-i', vignette_png(fx['vig'])]
        chain += f'[3:v]format=rgba[vg];[{base}][vg]overlay=0:0:format=auto[b1];'
        base = 'b1'
    if fx.get('grain'):
        chain += f"[{base}]noise=c0s={fx['grain'] * GRAIN_STRENGTH:.2f}:c0f=t[b2];"
        base = 'b2'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'list.txt'),
           '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-framerate', str(FPS), '-i', '-',
           '-t', f'{dur:.3f}', '-i', os.path.join(AUDIO, T['key'] + '.m4a')] + extra + [
           '-filter_complex', chain + f'[1:v]setpts=PTS-STARTPTS[c];[{base}][c]overlay=0:0:format=auto,format=yuv420p[v];'
                              f'[2:a]asetpts=PTS-STARTPTS,afade=t=out:st={dur - 0.05:.3f}:d=0.05[a]',
           '-map', '[v]', '-map', '[a]', '-r', str(FPS), '-frames:v', str(total),
           '-c:v', 'libx264', '-crf', str(Q['crf']), '-preset', Q['preset'], '-profile:v', 'high', '-pix_fmt', 'yuv420p'] + (
           ['-tune', 'film'] if Q['sharp'] else []) + COLOR_TAGS + [
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', tmp_out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    errbuf = []
    threading.Thread(target=lambda: errbuf.append(proc.stderr.read()), daemon=True).start()
    try:
        for data in text_frames(p, total):
            proc.stdin.write(data)
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        time.sleep(0.2)
        raise RuntimeError((errbuf[0] if errbuf else b'').decode(errors='replace')[-500:])
    os.replace(tmp_out, out)
    JOB['done'] = JOB['total']
    return fname


def render_job(pid, fmt=None, quality='std'):
    try:
        p = validate_project(json.load(open(project_path(pid), encoding='utf-8')))
        JOB.update(state='running', msg='', file=None)
        log('Exporting', p['name'], fmt or p.get('format'), quality)
        f = render_project(p, fmt, quality)
        JOB.update(state='done', file=f, msg='')
        log('Exported', f)
    except Exception as e:
        traceback.print_exc()
        JOB.update(state='error', msg=str(e)[:400])


# =====================================================================================
# Web server
# =====================================================================================
MIME = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
        '.png': 'image/png', '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.m4a': 'audio/mp4'}


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(b)

    def send_file(self, path, cache=True):
        if not path or not os.path.isfile(path):
            self.send_response(404); self.send_header('Content-Length', '0'); self.end_headers(); return
        size = os.path.getsize(path)
        ctype = MIME.get(os.path.splitext(path)[1].lower(), 'application/octet-stream')
        start, end, code = 0, size - 1, 200
        rng = self.headers.get('Range')
        if rng:
            m = re.match(r'bytes=(\d*)-(\d*)', rng)
            if m:
                a, b = m.groups()
                if a:
                    start = int(a); end = int(b) if b else size - 1
                elif b:
                    start = max(0, size - int(b))
                end = min(end, size - 1)
                if start > end:
                    self.send_response(416); self.send_header('Content-Range', f'bytes */{size}'); self.send_header('Content-Length', '0'); self.end_headers(); return
                code = 206
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(end - start + 1))
        if code == 206:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Cache-Control', 'max-age=3600' if cache else 'no-store')
        self.end_headers()
        try:
            with open(path, 'rb') as fh:
                fh.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = fh.read(min(262144, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def body(self):
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n).decode('utf-8')) if n else {}

    def do_GET(self):
        try:
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            path = urllib.parse.unquote(u.path)
            base = os.path.basename(path)
            if path in ('/', '/index.html'):
                return self.send_file(os.path.join(HERE, 'studio.html'), cache=False)
            if path in ('/carousel', '/carousel.html'):
                return self.send_file(os.path.join(HERE, 'carousel.html'), cache=False)
            if path == '/api/carousel/list':
                return self.send_json({'carousels': list_carousels(), 'formats': CE.FORMATS,
                                       'looks': [LOOK[k] for k, *_ in LOOKS]})
            if path == '/api/carousel/get':
                n = q['name'][0]
                return self.send_json({'spec': read_carousel(n), 'photos': carousel_photos(n)})
            if path == '/api/carousel/photos':
                return self.send_json({'photos': carousel_photos(q['name'][0])})
            if path == '/api/carousel/thumb':
                return self.send_file(carousel_thumb(q['name'][0], q['file'][0]))
            if path == '/api/carousel/template-preview':
                return self.send_file(template_preview(q['key'][0]))
            if path.startswith('/cr/'):
                parts = path.split('/')
                if len(parts) == 4 and parts[2].isdigit() and re.fullmatch(r'\d\d\.jpg', parts[3]):
                    return self.send_file(os.path.join(CCACHE, 'r', parts[2], parts[3]))
            if path == '/api/init':
                styles = {k: {'label': v['label'], 'shadow': v['shadow'], 'blur': v['blur'], 'off': v['off'], 'xs': v['xs'],
                              'arc': bool(v.get('arc')), 'fill': '#%02x%02x%02x' % tuple(v['fill'][:3])} for k, v in STYLES.items()}
                return self.send_json({'library': LIB + PHOTOS + COLL_ITEMS, 'collections': collections_info(), 'projects': list_projects(),
                                       'styles': styles, 'stale': is_stale(), 'looks': [LOOK[k] for k, *_ in LOOKS],
                                       'templates': {k: template_meta(T) for k, T in TEMPLATES.items()},
                                       'starters': {k: starter(k) for k in TEMPLATES}})
            if path == '/api/library':
                return self.send_json({'library': LIB + PHOTOS + COLL_ITEMS, 'collections': collections_info()})
            if path == '/api/collections/status':
                return self.send_json(dict(SCAN))
            if path.startswith(('/pthumb/', '/pprev/')):
                try:
                    cid = int(os.path.splitext(base)[0])
                except ValueError:
                    cid = -1
                return self.send_file(photo_file(cid, 'thumb' if path.startswith('/pthumb/') else 'prev') if is_photo(cid) else None)
            if path == '/api/proxy':
                cid = int(q['id'][0])
                if is_photo(cid):
                    return self.send_json({'status': 'ready', 'url': f'/pprev/{cid}.jpg'})
                if q.get('peek'):
                    st = 'ready' if os.path.exists(proxy_file(cid)) else PSTAT.get(cid, 'none')
                else:
                    st = request_proxy(cid, 0)
                return self.send_json({'status': st, 'url': f'/proxies/{cid}.mp4'})
            if path.startswith('/src/'):
                try:
                    cid = int(base)
                except ValueError:
                    cid = -1
                return self.send_file(src_path(cid) if cid in CLIPS else None)
            if path == '/api/strip':
                return self.send_file(strip_file(int(q['id'][0])))
            if path == '/api/version':
                page = os.path.join(HERE, 'studio.html')       # lets an open page notice it is out of date
                return self.send_json({'app': 'reel-studio', 'stale': is_stale(), 'busy': JOB['state'] == 'running',
                                       'page': int(os.path.getmtime(page)) if os.path.exists(page) else 0, 'code': int(CODE_MTIME)})
            if path == '/api/render-status':
                return self.send_json(JOB)
            if path == '/api/warm-status':
                with _plock:
                    left = sum(1 for v in PSTAT.values() if v in ('queued', 'working'))
                return self.send_json({'left': left})
            if path.startswith('/thumbs/'):                 # Europe catalogue thumbnails, else the extra folders' own
                fp = os.path.join(THUMBS, base)
                return self.send_file(fp if os.path.exists(fp) else os.path.join(CTHUMBS, base))
            if path.startswith('/reels/'):                  # the last export, wherever its folder is
                fp = os.path.join(JOB.get('dir') or REELS, base)
                return self.send_file(fp if os.path.exists(fp) else os.path.join(REELS, base), cache=False)
            for prefix, folder in (('/proxies/', PROXIES), ('/audio/', AUDIO), ('/insp/', INSP), ('/text/', TEXTC)):
                if path.startswith(prefix):
                    return self.send_file(os.path.join(folder, base))
            self.send_response(404); self.send_header('Content-Length', '0'); self.end_headers()
        except Exception as e:
            traceback.print_exc()
            self.send_json({'error': str(e)}, 500)

    def do_POST(self):
        try:
            path = urllib.parse.urlparse(self.path).path
            data = self.body()
            if path == '/api/text':                 # draw one text layer, return its images
                L = clean_text_layer(data, 10 ** 6)
                return self.send_json(text_resources(L))
            if path == '/api/project':
                p = validate_project(data)
                if not p.get('id'):
                    p['id'] = 'p' + uuid.uuid4().hex[:10]
                p['updated'] = int(time.time() * 1000)
                tmp = project_path(p['id']) + '.tmp'
                json.dump(p, open(tmp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
                os.replace(tmp, project_path(p['id']))
                return self.send_json({'ok': True, 'id': p['id'], 'updated': p['updated']})
            if path == '/api/project/delete':
                fp = project_path(data['id'])
                if os.path.exists(fp):
                    os.remove(fp)
                return self.send_json({'ok': True})
            if path == '/api/render':
                if JOB['state'] == 'running':
                    return self.send_json({'ok': False, 'msg': 'Another export is still running.'})
                JOB.update(state='running', done=0, total=1, file=None, msg='')
                q = data.get('quality') if data.get('quality') in QUALITIES else 'std'
                threading.Thread(target=render_job, args=(data['id'], data.get('format'), q), daemon=True).start()
                return self.send_json({'ok': True})
            if path == '/api/warm':
                n = 0
                for cid in data.get('ids', [])[:3000]:
                    cid = int(cid)
                    if cid in CLIPS and not is_photo(cid) and request_proxy(cid, 2) != 'ready':
                        n += 1
                return self.send_json({'ok': True, 'queued': n})
            if path == '/api/open-folder':
                d = JOB.get('dir') or REELS
                os.makedirs(d, exist_ok=True)
                open_in_files(d)
                return self.send_json({'ok': True})
            if path == '/api/collections/rescan':      # re-read a folder (e.g. after its _Clip list.csv changed)
                key = data.get('key')
                if key not in COLLS or COLLS[key].get('builtin'):
                    raise ValueError('unknown folder')
                if SCAN['state'] == 'running':
                    raise ValueError('A folder is already being scanned.')
                SCAN.update(state='running', key=key, name=COLLS[key]['name'], done=0, total=0, msg='', first='')
                threading.Thread(target=scan_job, args=(key,), daemon=True).start()
                return self.send_json({'ok': True})
            if path == '/api/templates/reload':        # pick up new or changed files in templates\
                load_templates()
                return self.send_json({'ok': True, 'templates': list(TEMPLATES)})
            if path == '/api/collections/add':
                key = add_collection(data.get('path'), data.get('name'))
                return self.send_json({'ok': True, 'key': key})
            if path == '/api/carousel/save':
                return self.send_json({'ok': True, 'spec': write_carousel(data['name'], data['spec'])})
            if path == '/api/carousel/render':
                return self.send_json(carousel_render(data['name'], data['spec']))
            if path == '/api/carousel/add':
                return self.send_json({'file': carousel_add(data['name'], data['clip'], data.get('t'))})
            if path == '/api/carousel/new':
                fmt = data.get('format') if data.get('format') in CE.FORMATS else 'pair'
                return self.send_json({'spec': carousel_new(data['name'], fmt, data.get('from'))})
            if path == '/api/carousel/export':
                d = carousel_dir(data['name'])
                write_carousel(data['name'], data['spec'])
                return self.send_json({'files': CE.export(d, read_carousel(data['name'])), 'folder': d})
            if path == '/api/carousel/open':
                d = carousel_dir(data['name'])
                if data.get('file'):
                    fp = os.path.join(d, 'photos', os.path.basename(data['file']))
                    open_in_files(fp, select=True)
                else:
                    open_in_files(os.path.join(d, 'photos') if data.get('photos') else d)
                return self.send_json({'ok': True})
            if path == '/api/quit':                 # a newer Reel Studio is starting and wants this port
                if JOB['state'] == 'running':
                    return self.send_json({'ok': False, 'busy': True})
                self.send_json({'ok': True})
                print('\n  A newer Reel Studio was started - closing this one.\n', flush=True)
                threading.Thread(target=SERVER.shutdown, daemon=True).start()
                return
            self.send_json({'error': 'not found'}, 404)
        except Exception as e:
            traceback.print_exc()
            self.send_json({'error': str(e)}, 400)


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def stop_children():
    """Stop any ffmpeg this server started, so a newer Reel Studio can take over cleanly."""
    if not IS_WIN:
        try:
            subprocess.run(['pkill', '-P', str(os.getpid()), 'ffmpeg'], capture_output=True, timeout=20)
        except Exception:
            pass
        return
    try:
        subprocess.run(['powershell', '-NoProfile', '-Command',
                        f"Get-CimInstance Win32_Process -Filter 'ParentProcessId={os.getpid()}' | "
                        "Where-Object { $_.Name -eq 'ffmpeg.exe' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                       capture_output=True, timeout=20, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except Exception:
        pass


def ask_running(path, post=False):
    """Talk to a Reel Studio that is already using our port. Returns its JSON reply, or None."""
    import urllib.request
    req = urllib.request.Request(f'http://127.0.0.1:{PORT}{path}', data=b'{}' if post else None,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception:
        return None


def take_port():
    """Open the server. If an older Reel Studio is still running, ask it to close and take over."""
    try:
        return Server(('127.0.0.1', PORT), Handler)
    except OSError:
        pass
    info = ask_running('/api/version')
    if info and not info.get('stale'):
        print('Reel Studio is already running - opening it in your browser.')
        webbrowser.open(f'http://localhost:{PORT}/')
        return None
    if info and info.get('busy'):
        print('\n  An older Reel Studio is still running and is exporting a reel.\n'
              '  Wait for the export to finish, close its black window, then start Reel Studio again.\n')
        sys.exit(1)
    if info:
        print('An older Reel Studio is still running - replacing it with this version...', flush=True)
        ask_running('/api/quit', post=True)
        for _ in range(20):
            time.sleep(0.5)
            try:
                return Server(('127.0.0.1', PORT), Handler)
            except OSError:
                pass
    print('\n  An older Reel Studio is still running and could not be closed automatically.\n'
          '  Close the other black "Reel Studio" window, then double-click Start Reel Studio.bat again.\n')
    sys.exit(1)


def main():
    global SERVER, STOPPING
    arg = lambda flag: sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv and sys.argv.index(flag) + 1 < len(sys.argv) else None
    if '--add-folder' in sys.argv:                 # python studio.py --add-folder "D:\Trips\Goa" --name "Goa trip"   (set-up, no server)
        key = add_collection(arg('--add-folder'), arg('--name'), background=False)
        items = scan_collection(key, lambda a, b: print(f'  reading {a}/{b}', end='\r', flush=True))
        install_items(key, items)
        load_templates()
        first = ensure_first_project()
        print(f"\n  Added {COLLS[key]['name']}: {len(items)} clips and photos." + (' Started "My first reel".' if first else ''))
        return
    if '--scan' in sys.argv:                       # python studio.py --scan <key>   (re-read one folder, then stop)
        key = arg('--scan')
        items = scan_collection(key, lambda a, b: print(f'  {a}/{b}', end='\r', flush=True))
        print(f"\n  {COLLS[key]['name']}: {len(items)} clips and photos")
        return
    print('Starting Reel Studio...', flush=True)
    load_templates()
    if '--prepare' in sys.argv:
        return
    if LEGACY:
        PHOTOS[:] = scan_photos()
        for c in PHOTOS:
            c['col'] = 'europe'
        CLIPS.update({c['id']: c for c in PHOTOS})
        print(f'  {len(LIB)} videos and {len(PHOTOS)} photos in the library', flush=True)
    for key, C in COLLS.items():                   # extra folders: what was scanned before, at once; new files in the background
        if C.get('builtin'):
            continue
        items = load_collection_items(key)
        install_items(key, items)
        print(f"  {C['name']}: {len(items)} clips and photos ({C['root']})", flush=True)
    if not COLLS:
        print('  No footage yet: the page will ask for your first folder.', flush=True)
    ensure_first_project()
    server = SERVER = take_port()
    if server is None:
        return
    for _ in range(2):
        threading.Thread(target=proxy_worker, daemon=True).start()
    threading.Thread(target=proxy_worker, args=(True,), daemon=True).start()
    threading.Thread(target=photo_warmer, daemon=True).start()

    def rescan_all():                              # pick up files added to the extra folders since last time
        for key, C in list(COLLS.items()):
            if not C.get('builtin') and SCAN['state'] != 'running':
                scan_job(key)
        SCAN.update(state='idle')
    threading.Thread(target=rescan_all, daemon=True).start()
    for p in list_projects():
        for s in p.get('slots', []):
            if not is_photo(s['clip']):
                request_proxy(int(s['clip']), 1)
    print('\n  Reel Studio is running at  http://localhost:%d\n  Keep this window open while you edit. Close it to stop.\n' % PORT, flush=True)
    if '--no-browser' not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(f'http://localhost:{PORT}/')).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    STOPPING = True                 # no new preview copies; stop running ones, then free the port
    stop_children()
    server.server_close()


if __name__ == '__main__':
    main()
