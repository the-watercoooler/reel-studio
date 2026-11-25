"""Carousel engine: turns a carousel spec (carousel.json) into 1080x1350 slides.

Used by Carousel Studio (studio.py serves /carousel) and by Carousels\\carousel_maker.py.
Every photo a carousel uses is a plain image file in <carousel>\\photos\\, so you can edit it in any app and save it back.

spec = {
  "name": "...", "format": "pair" | "frames3" | "postcards",
  "look": {"grade": "warmfilm", "amt": 0.85},
  "slides": [{"kind": "...", "photos": [{"file": "x.jpg", "cx": .5, "cy": .5, "zoom": 1} | null, ...],
              "text": {"field": "words"}}, ...],
  "versions": [{"label": "...", "time": 0, "spec": {...}}]
}
"""
import json, math, os, re, threading, time
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1080, 1350
_look_rgb, _LOOK = None, {}


def setup(look_rgb, looks):
    """Hand over Reel Studio's colour-look maths, so carousels and reels share the same looks."""
    global _look_rgb, _LOOK
    _look_rgb, _LOOK = look_rgb, looks


# ------------------------------------------------------------------ formats
FORMATS = {
    'pair': {
        'label': 'Split pair (“…” / “That’s the point”)',
        'about': 'Two photos per slide. A line on the top photo, the answer on the bottom one.',
        'look': ('mountain', 0.7),
        'kinds': {
            'pair': {'label': 'Two photos', 'photos': ['Top photo', 'Bottom photo'],
                     'fields': [['top', 'Top line'], ['bottom', 'Bottom line']]},
        },
    },
    'frames3': {
        'label': 'Told in 3 frames',
        'about': 'White border. A cover, then 3 stacked photos per slide: wide, medium, close.',
        'look': ('warmfilm', 0.85),
        'kinds': {
            'cover': {'label': 'Cover', 'photos': ['Cover photo'],
                      'fields': [['title', 'Title'], ['subtitle', 'Small line'], ['credit', 'Credit (bottom)']]},
            'triptych': {'label': '3 frames', 'photos': ['Wide', 'Medium', 'Close'], 'fields': [['caption', 'Caption (optional)']]},
        },
    },
    'postcards': {
        'label': 'Postcards (seamless)',
        'about': 'A cover of letter strips, then framed postcards with small polaroids across the slide edges.',
        'look': ('faded', 0.9),
        'kinds': {
            'strips': {'label': 'Letter strips cover', 'photos': ['Strip 1', 'Strip 2', 'Strip 3', 'Strip 4', 'Strip 5', 'Strip 6'],
                       'fields': [['letters', 'Letters (one per strip)'], ['subtitle', 'Small line'], ['footer', 'Bottom line']]},
            'card': {'label': 'Postcard', 'photos': ['Postcard', 'Polaroid on the right edge (optional)'], 'fields': [['caption', 'Caption']]},
            'end': {'label': 'Closing slide', 'photos': ['Soft background (optional)'], 'fields': [['title', 'Title'], ['subtitle', 'Small line']]},
        },
    },
}


def empty_slide(fmt, kind, over=None):
    """A new slide of this kind, with its sample words (over = words to use instead)."""
    k = FORMATS[fmt]['kinds'][kind]
    if 'defaults' in k:
        text = {f: k['defaults'].get(f, '') for f, _ in k['fields']}
        text.update({f: v for f, v in (over or {}).items() if f in text})
        return {'kind': kind, 'photos': [None] * len(k['photos']), 'text': text}
    defaults = {'top': '“There’s absolutely nothing to do here”', 'bottom': 'That’s the point', 'title': 'A VISUAL STORY' if fmt == 'frames3' else 'wish you were here',
                'subtitle': '“TOLD IN 3 FRAMES. FELT FOR A LIFETIME.”' if fmt == 'frames3' else ('P O S T C A R D S' if kind == 'strips' else '—  E U R O P E ,  2 0 2 6'),
                'letters': 'EUROPE', 'footer': 'SUMMER 2026'}
    return {'kind': kind, 'photos': [None] * len(k['photos']), 'text': {f: defaults.get(f, '') for f, _ in k['fields']}}


def clean_spec(spec):
    """Keep a spec well-formed (used before saving anything the browser sends)."""
    fmt = spec.get('format') if spec.get('format') in FORMATS else 'pair'
    F = FORMATS[fmt]
    out = {'name': str(spec.get('name') or 'Untitled carousel')[:80], 'format': fmt, 'slides': []}
    lk = spec.get('look') if isinstance(spec.get('look'), dict) else {}
    g = lk.get('grade') if lk.get('grade') in _LOOK or not _LOOK else F['look'][0]
    try:
        amt = max(0.0, min(1.0, float(lk.get('amt', F['look'][1]))))
    except (TypeError, ValueError):
        amt = F['look'][1]
    out['look'] = {'grade': g or F['look'][0], 'amt': round(amt, 2)}
    for sl in (spec.get('slides') or [])[:20]:
        kind = sl.get('kind') if sl.get('kind') in F['kinds'] else next(iter(F['kinds']))
        k = F['kinds'][kind]
        photos = []
        src = sl.get('photos') or []
        for i in range(len(k['photos'])):
            p = src[i] if i < len(src) else None
            if isinstance(p, dict) and p.get('file'):
                photos.append({'file': os.path.basename(str(p['file'])),
                               'cx': round(min(1, max(0, float(p.get('cx', 0.5)))), 4),
                               'cy': round(min(1, max(0, float(p.get('cy', 0.5)))), 4),
                               'zoom': round(min(4, max(1, float(p.get('zoom', 1)))), 3)})
            else:
                photos.append(None)
        text = sl.get('text') if isinstance(sl.get('text'), dict) else {}
        out['slides'].append({'kind': kind, 'photos': photos, 'text': {f: str(text.get(f, ''))[:200] for f, _ in k['fields']}})
    vers = spec.get('versions') if isinstance(spec.get('versions'), list) else []
    out['versions'] = [v for v in vers if isinstance(v, dict) and isinstance(v.get('spec'), dict)][-30:]
    return out


# ------------------------------------------------------------------ pictures
_cache, _clock = {}, threading.Lock()


def load(folder, file, max_side):
    """A photo from the carousel's photos folder (re-read automatically when the file is edited)."""
    fp = os.path.join(folder, 'photos', os.path.basename(file))
    try:
        mt = os.path.getmtime(fp)
    except OSError:
        return None
    key = (fp, mt, max_side)
    with _clock:
        im = _cache.get(key)
    if im is None:
        im = Image.open(fp)
        if max_side:
            im.draft('RGB', (max_side, max_side))
        im = ImageOps.exif_transpose(im).convert('RGB')
        if max_side:
            im.thumbnail((max_side, max_side), Image.LANCZOS)
        with _clock:
            if len(_cache) > 120:
                _cache.clear()
            _cache[key] = im
    return im


def fill(im, w, h, cx=0.5, cy=0.5, zoom=1.0):
    iw, ih = im.size
    if iw / ih > w / h:
        ch = ih / zoom; cw = ch * w / h
    else:
        cw = iw / zoom; ch = cw * h / w
    x = min(max(0, cx * iw - cw / 2), iw - cw)
    y = min(max(0, cy * ih - ch / 2), ih - ch)
    return im.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS, box=(x, y, x + cw, y + ch))


_luts = {}


def look(im, lk):
    key, amt = (lk or {}).get('grade'), float((lk or {}).get('amt', 1))
    if not _look_rgb or key in (None, 'none') or key not in _LOOK or amt <= 0:
        return im
    k = (key, round(amt, 2))
    if k not in _luts:
        P = _LOOK[key]['p']

        def f(r, g, b):
            c1 = _look_rgb((r, g, b), P)
            return tuple(a + (c - a) * amt for a, c in zip((r, g, b), c1))
        _luts[k] = ImageFilter.Color3DLUT.generate(33, f)
    return im.convert('RGB').filter(_luts[k])


def placeholder(w, h, label='add a photo'):
    im = Image.new('RGB', (max(1, int(w)), max(1, int(h))), (58, 58, 64))
    d = ImageDraw.Draw(im)
    f = font('segoeuil.ttf', max(14, int(min(w, h) / 9)))
    t = '+ ' + label
    tw = f.getlength(t)
    d.text(((w - tw) / 2, h / 2 - f.size / 2), t, font=f, fill=(150, 150, 160))
    return im


class Ctx:
    def __init__(self, folder, spec, max_side):
        self.folder, self.spec, self.max_side = folder, spec, max_side

    def photo(self, ph, w, h, label='add a photo'):
        """The slot's photo cropped to w x h with the carousel's look, or a placeholder."""
        if not ph:
            return placeholder(w, h, label)
        im = load(self.folder, ph['file'], self.max_side)
        if im is None:
            return placeholder(w, h, 'photo missing')
        return look(fill(im, w, h, ph.get('cx', 0.5), ph.get('cy', 0.5), ph.get('zoom', 1)), self.spec.get('look'))

    def raw(self, ph):
        if not ph:
            return None
        im = load(self.folder, ph['file'], self.max_side)
        return look(im, self.spec.get('look')) if im is not None else None


# ------------------------------------------------------------------ type
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fontfind  # noqa: E402  (fonts\ next to this file wins; on a Mac, the closest Mac fonts)


def font_path(name):
    f = fontfind.find(name)
    return f[0] if f else None


def font(name, size):
    """A font by its Windows file name; 'file.ttf#Instance' picks a named style of a variable font (e.g.
    'bahnschrift.ttf#Bold Condensed'). Other systems get the closest font they have (see fontfind.py)."""
    return fontfind.load(name, size)


def text_size(t, f, track=0):
    if not t:
        return 0, 0
    w = sum(f.getlength(ch) for ch in t) + track * (len(t) - 1)
    a, d = f.getmetrics()
    return w, a + d


def paste(cv, im, x, y):
    """alpha_composite that also works when the picture hangs over an edge."""
    x, y = int(round(x)), int(round(y))
    sx, sy = max(0, -x), max(0, -y)
    if sx >= im.width or sy >= im.height or x >= cv.width or y >= cv.height:
        return
    if sx or sy:
        im = im.crop((sx, sy, im.width, im.height))
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    w = min(im.width, cv.width - max(x, 0))
    h = min(im.height, cv.height - max(y, 0))
    if w <= 0 or h <= 0:
        return
    if (w, h) != im.size:
        im = im.crop((0, 0, w, h))
    cv.alpha_composite(im, (max(x, 0), max(y, 0)))


def draw_text(img, xy, t, f, fill=(255, 255, 255), track=0, anchor='mt', shadow=110, blur=6, rot=0, stroke=0, outline=False, alpha=255, scol=None):
    """Text with letter-spacing and a soft shadow (drawn on a small layer, so it is quick on long strips)."""
    if not t:
        return 0, 0
    w, h = text_size(t, f, track)
    m = int(blur * 3 + 8 + stroke * 2)
    layer = Image.new('RGBA', (int(w) + 2 * m, int(h) + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = m
    col = tuple(fill[:3])
    for ch in t:
        if outline:
            d.text((cx, m), ch, font=f, fill=col + (0,), stroke_width=max(1, stroke), stroke_fill=col + (alpha,))
        else:
            d.text((cx, m), ch, font=f, fill=col + (alpha,), stroke_width=stroke, stroke_fill=col + (alpha,))
        cx += f.getlength(ch) + track
    out = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    if shadow:
        sh = Image.new('RGBA', layer.size, tuple(scol or (0, 0, 0)) + (0,))   # scol: a coloured glow instead of a shadow
        sh.putalpha(layer.getchannel('A').point(lambda v: v * shadow // 255))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (0, 0 if scol else 2))
    out.alpha_composite(layer)
    x, y = xy
    ax = {'l': 0, 'm': w / 2, 'r': w}[anchor[0]]
    ay = {'t': 0, 'm': h / 2, 'b': h}[anchor[1]]
    if rot:
        big = out.rotate(rot, resample=Image.BICUBIC, expand=True)
        # keep the anchor point where it was asked to be
        px, py = m + ax - out.width / 2, m + ay - out.height / 2
        r = math.radians(rot)
        qx, qy = px * math.cos(r) + py * math.sin(r), -px * math.sin(r) + py * math.cos(r)
        paste(img, big, x - big.width / 2 - qx, y - big.height / 2 - qy)
    else:
        paste(img, out, x - ax - m, y - ay - m)
    return w, h


# ------------------------------------------------------------------ renderers
# Each returns (slides, boxes): boxes[slide] = [{"i": photo index, "slide": owner slide, "rect": [x0,y0,x1,y1], "rot": deg}]
def r_pair(c):
    slides, boxes = [], []
    fq, fp = font('BELL.TTF', 46), font('GARAIT.TTF', 50)
    half = H // 2
    for n, sl in enumerate(c.spec['slides']):
        s = Image.new('RGBA', (W, H), (20, 20, 22, 255))
        p = sl['photos']
        s.paste(c.photo(p[0], W, half, 'top photo'), (0, 0))
        s.paste(c.photo(p[1], W, H - half, 'bottom photo'), (0, half))
        draw_text(s, (W / 2, 62), sl['text'].get('top', ''), fq, track=1, shadow=150, blur=8)
        draw_text(s, (W / 2, half + 58), sl['text'].get('bottom', ''), fp, track=1, shadow=150, blur=8)
        slides.append(s)
        boxes.append([{'i': 0, 'slide': n, 'rect': [0, 0, W, half], 'rot': 0}, {'i': 1, 'slide': n, 'rect': [0, half, W, H], 'rot': 0}])
    return slides, boxes


def r_frames3(c):
    B = 24
    fw, fh = W - 2 * B, (H - 4 * B) // 3
    ORANGE = (236, 128, 52)
    slides, boxes = [], []
    for n, sl in enumerate(c.spec['slides']):
        s = Image.new('RGBA', (W, H), (255, 255, 255, 255))
        t = sl['text']
        if sl['kind'] == 'cover':
            s.paste(c.photo(sl['photos'][0], W - 2 * B, H - 2 * B, 'cover photo'), (B, B))
            draw_text(s, (W / 2, 300), t.get('title', ''), font('GOTHICB.TTF', 74), fill=ORANGE, track=6, shadow=120, blur=10)
            draw_text(s, (W / 2, 396), t.get('subtitle', ''), font('GARAIT.TTF', 30), track=3, shadow=140, blur=6)
            draw_text(s, (W / 2, H - 92), t.get('credit', ''), font('GARAIT.TTF', 26), fill=(240, 240, 240), track=1, shadow=140, blur=5)
            boxes.append([{'i': 0, 'slide': n, 'rect': [B, B, W - B, H - B], 'rot': 0}])
        else:
            bx = []
            for i in range(3):
                s.paste(c.photo(sl['photos'][i], fw, fh, ('wide', 'medium', 'close')[i]), (B, B + i * (fh + B)))
                bx.append({'i': i, 'slide': n, 'rect': [B, B + i * (fh + B), B + fw, B + i * (fh + B) + fh], 'rot': 0})
            draw_text(s, (W / 2, H - B - 70), t.get('caption', ''), font('GARAIT.TTF', 34), track=1, shadow=170, blur=7)
            boxes.append(bx)
        slides.append(s)
    return slides, boxes


def _strips_cover(c, sl, n):
    photos = sl['photos']
    letters = [ch for ch in (sl['text'].get('letters') or '') if not ch.isspace()]
    cnt = len(photos)
    sw = W // cnt
    cover = Image.new('RGBA', (W, H), (20, 18, 16, 255))
    fl = font('segoeuil.ttf', 64)
    bx = []
    for i, ph in enumerate(photos):
        x0 = i * sw
        cover.paste(c.photo(ph, sw - 4, H, str(i + 1)), (x0 + 2, 0))
        if i < len(letters):
            draw_text(cover, (x0 + sw / 2, int(H * 0.60)), letters[i], fl, shadow=150, blur=8)
        bx.append({'i': i, 'slide': n, 'rect': [x0 + 2, 0, x0 + sw - 2, H], 'rot': 0})
    draw_text(cover, (W / 2, int(H * 0.60) + 96), sl['text'].get('subtitle', ''), font('GOTHIC.TTF', 24), track=4, shadow=170, blur=6)
    draw_text(cover, (W / 2, H - 70), sl['text'].get('footer', ''), font('GOTHIC.TTF', 18), fill=(235, 235, 235), track=6, shadow=170, blur=5)
    return cover, bx


def r_postcards(c):
    spec = c.spec
    out = [None] * len(spec['slides'])
    boxes = [[] for _ in spec['slides']]
    strip_idx = [n for n, sl in enumerate(spec['slides']) if sl['kind'] != 'strips']
    for n, sl in enumerate(spec['slides']):
        if sl['kind'] == 'strips':
            out[n], boxes[n] = _strips_cover(c, sl, n)
    if strip_idx:
        ns = len(strip_idx)
        SW = ns * W
        # background: each postcard's own photo, very soft and dim, blended into its neighbours
        acc = np.zeros((H, SW, 3), np.float32)
        wsum = np.zeros((H, SW, 1), np.float32)
        xs = np.arange(SW, dtype=np.float32)
        last = None
        for j, n in enumerate(strip_idx):
            sl = spec['slides'][n]
            im = c.raw(sl['photos'][0]) if sl['photos'] and sl['photos'][0] else None
            im = im or last
            if im is None:
                continue
            last = im
            cxp, bw = (j + 0.5) * W, 3400
            ph = sl['photos'][0] or {}
            bg = fill(im, bw // 8, H // 8, ph.get('cx', 0.5), ph.get('cy', 0.5)).filter(ImageFilter.GaussianBlur(6)).resize((bw, H), Image.BICUBIC)
            arr = np.asarray(bg, np.float32)
            x0 = int(cxp - bw / 2)
            lo, hi = max(0, x0), min(SW, x0 + bw)
            wgt = np.exp(-((xs[lo:hi] - cxp) / 520.0) ** 2)[None, :, None]
            acc[:, lo:hi] += arr[:, lo - x0:hi - x0] * wgt
            wsum[:, lo:hi] += wgt
        base = np.array([42, 37, 33], np.float32)
        bgm = (acc + base * 0.02) / (wsum + 0.02)
        grey = bgm.mean(2, keepdims=True)
        bgm = (grey + (bgm - grey) * 0.55) * 0.55
        strip = Image.fromarray(np.clip(bgm, 0, 255).astype(np.uint8)).convert('RGBA')
        f_cap = font('GOTHIC.TTF', 22)
        sbox = []          # boxes in strip coordinates
        mini_n = 0
        for j, n in enumerate(strip_idx):
            sl = spec['slides'][n]
            cx = int((j + 0.5) * W)
            if sl['kind'] == 'card':
                ph = sl['photos'][0]
                src = load(c.folder, ph['file'], c.max_side) if ph else None
                portrait = src is None or src.height >= src.width
                pw, phh = (560, 746) if portrait else (800, 600)
                cy = int(H * (0.45 if portrait else 0.42))
                brd = 22
                card = Image.new('RGBA', (pw + 2 * brd, phh + 2 * brd), (250, 248, 243, 255))
                card.paste(c.photo(ph, pw, phh, 'postcard'), (brd, brd))
                x, y = cx - card.width // 2, cy - card.height // 2
                sh = Image.new('RGBA', strip.size, (0, 0, 0, 0))
                ImageDraw.Draw(sh).rectangle((x + 10, y + 16, x + card.width + 10, y + card.height + 16), fill=(0, 0, 0, 120))
                strip.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
                strip.alpha_composite(card, (x, y))
                draw_text(strip, (cx, y + card.height + 34), sl['text'].get('caption', ''), f_cap, fill=(240, 236, 228), track=5, shadow=160, blur=5)
                sbox.append({'i': 0, 'slide': n, 'rect': [x + brd, y + brd, x + brd + pw, y + brd + phh], 'rot': 0})
                # small polaroid across this slide's right edge
                mp = sl['photos'][1] if len(sl['photos']) > 1 else None
                if mp and j < ns - 1:
                    yy, tilt = ((0.80, -6), (0.17, 5))[mini_n % 2]
                    mini_n += 1
                    pol = Image.new('RGBA', (300, 350), (250, 248, 243, 255))
                    pol.paste(c.photo(mp, 270, 270), (15, 15))
                    pol = pol.rotate(tilt, resample=Image.BICUBIC, expand=True)
                    ex, ey = (j + 1) * W, int(yy * H)
                    px, py = int(ex - pol.width / 2), int(ey - pol.height / 2)
                    shd = Image.new('RGBA', strip.size, (0, 0, 0, 0))
                    shd.paste((0, 0, 0, 110), (px + 8, py + 12), pol.getchannel('A'))
                    strip.alpha_composite(shd.filter(ImageFilter.GaussianBlur(12)))
                    strip.alpha_composite(pol, (px, py))
                    sbox.append({'i': 1, 'slide': n, 'rect': [ex - 150, ey - 175, ex + 150, ey + 175], 'rot': tilt})
            elif sl['kind'] == 'end':
                draw_text(strip, (cx, int(H * 0.44)), sl['text'].get('title', ''), font('GARAIT.TTF', 74), shadow=170, blur=9)
                draw_text(strip, (cx, int(H * 0.44) + 104), sl['text'].get('subtitle', ''), font('GOTHIC.TTF', 22), fill=(230, 226, 218), track=2, shadow=170, blur=5)
                sbox.append({'i': 0, 'slide': n, 'rect': [cx - 300, int(H * 0.62), cx + 300, int(H * 0.62) + 90], 'rot': 0, 'hint': 'background'})
        for j, n in enumerate(strip_idx):
            out[n] = strip.crop((j * W, 0, (j + 1) * W, H))
            for b in sbox:   # a box shows on every slide it overlaps
                x0, x1 = b['rect'][0] - j * W, b['rect'][2] - j * W
                if x1 > 0 and x0 < W:
                    boxes[n].append(dict(b, rect=[x0, b['rect'][1], x1, b['rect'][3]]))
    return out, boxes


# ================================================================== generic templates
# A template is a list of slide kinds; each kind is a list of elements (photos, text, shapes...) drawn in order.
# Templates themselves live in carousel_templates.py.
_paper = {}


def paper(w, h, tone=(240, 234, 222), grain=7, seed=3):
    key = (w, h, tone, grain, seed)
    if key not in _paper:
        rng = np.random.default_rng(seed)
        n = rng.normal(0, grain, (h // 2 + 1, w // 2 + 1, 1)).astype(np.float32)
        n = np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)[..., 0], 'L').resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.8)), np.float32)[..., None] - 128
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        vig = 1 - 0.06 * (((xx % 1080) / 1080 - 0.5) ** 2 * 4 + (yy / h - 0.5) ** 2 * 4)
        arr = (np.array(tone, np.float32)[None, None, :] + n) * vig[..., None]
        if len(_paper) > 8:
            _paper.clear()
        _paper[key] = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
    return _paper[key].copy()


def rounded_mask(w, h, r):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    return m


def pixel_stretch(im, side, frac):
    """The photo with one edge's pixels stretched out (the 'pixel stretch' look)."""
    w, h = im.size
    keep = max(2, int(w * (1 - frac)) if side in ('left', 'right') else int(h * (1 - frac)))
    out = Image.new('RGB', (w, h))
    if side == 'right':
        out.paste(im.resize((keep, h), Image.LANCZOS, box=(0, 0, w, h)) if False else im.crop((0, 0, keep, h)), (0, 0))
        out.paste(im.crop((keep - 2, 0, keep, h)).resize((w - keep, h), Image.NEAREST), (keep, 0))
    elif side == 'left':
        out.paste(im.crop((w - keep, 0, w, h)), (w - keep, 0))
        out.paste(im.crop((w - keep, 0, w - keep + 2, h)).resize((w - keep, h), Image.NEAREST), (0, 0))
    elif side == 'bottom':
        out.paste(im.crop((0, 0, w, keep)), (0, 0))
        out.paste(im.crop((0, keep - 2, w, keep)).resize((w, h - keep), Image.NEAREST), (0, keep))
    else:
        out.paste(im.crop((0, h - keep, w, h)), (0, h - keep))
        out.paste(im.crop((0, h - keep, w, h - keep + 2)).resize((w, h - keep), Image.NEAREST), (0, 0))
    return out


def wrap_lines(t, f, maxw, track=0):
    lines = []
    for para in str(t).split('\n'):
        cur = ''
        for word in para.split(' '):
            test = (cur + ' ' + word).strip()
            if cur and text_size(test, f, track)[0] > maxw:
                lines.append(cur)
                cur = word
            else:
                cur = test
        lines.append(cur)
    return lines


def _slot_label(T, sl, i):
    names = T['kinds'][sl['kind']]['photos']
    return names[i] if i < len(names) else f'photo {i + 1}'


def _photo_tile(c, e, ph, label):
    x, y, w, h = e['rect']
    w, h = int(w), int(h)
    im = c.photo(ph, w, h, label)
    if e.get('mono'):
        im = ImageOps.grayscale(im).convert('RGB')
    if e.get('blur'):
        im = im.filter(ImageFilter.GaussianBlur(e['blur']))
    if e.get('dim'):
        im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), e['dim'])
    if e.get('duo'):                         # duotone: shadows in one colour, highlights in another
        im = ImageOps.colorize(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1), tuple(e['duo'][0]), tuple(e['duo'][1])).convert('RGB')
    if e.get('riso'):                        # two-ink risograph print, slightly out of register
        im = riso(im, *e['riso'])
    if e.get('flat'):                        # screen-print poster: the photo reduced to a few flat colours (dark → light)
        pal = [tuple(c) for c in e['flat']]
        g = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(im).filter(ImageFilter.MedianFilter(5)), cutoff=2), np.float32)
        idx = np.clip((g / 256 * len(pal)).astype(int), 0, len(pal) - 1)
        im = Image.fromarray(np.array(pal, np.uint8)[idx])
    if e.get('xerox'):                       # photocopy: hard black and white with toner noise
        g = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=4), np.float32)
        g = (g - 128) * 2.4 + 128 + np.random.default_rng(4).normal(0, 22, g.shape)
        im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert('RGB')
    if e.get('negative'):                    # colour negative: inverted with the orange film mask
        a = 255 - np.asarray(im, np.float32)
        a = a * np.array([1.0, 0.72, 0.5]) + np.array([30, 12, 0])
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if e.get('stretch'):
        im = pixel_stretch(im, *e['stretch'])
    b, pb = int(e.get('border', 0)), int(e.get('pb', 0))
    tile = Image.new('RGBA', (w + 2 * b, h + 2 * b + pb), tuple(e.get('bcolor', (250, 248, 243))) + (255,))
    tile.paste(im, (b, b))
    if e.get('shape'):
        tile.putalpha(_shape_mask(tile.width, tile.height, e['shape']))
    elif e.get('radius'):
        tile.putalpha(rounded_mask(tile.width, tile.height, int(e['radius'])))
    return tile


def _draw_photo(cv, ox, e, c, sl, j, T, boxes):
    slot = e['slot']
    ph = sl['photos'][slot] if slot < len(sl['photos']) else None
    x, y, w, h = e['rect']
    tile = _photo_tile(c, e, ph, _slot_label(T, sl, slot))
    rot = e.get('rot', 0)
    if rot:
        tile = tile.rotate(rot, resample=Image.BICUBIC, expand=True)
    b, pb = int(e.get('border', 0)), int(e.get('pb', 0))
    cx, cy = ox + x + w / 2, y + h / 2 + pb / 2
    px, py = cx - tile.width / 2, cy - tile.height / 2
    if e.get('shadow'):
        sh = Image.new('RGBA', (tile.width + 80, tile.height + 80), (0, 0, 0, 0))
        sh.paste((0, 0, 0, int(e['shadow'])), (40, 40), tile.getchannel('A'))
        paste(cv, sh.filter(ImageFilter.GaussianBlur(e.get('sblur', 14))), px - 40 + e.get('sx', 8), py - 40 + e.get('sy', 12))
    paste(cv, tile, px, py)
    if not e.get('nobox'):
        boxes.append({'i': slot, 'slide': j, 'rect': [ox + x, y, ox + x + w, y + h], 'rot': rot})


def _text_of(e, sl):
    t = e['text'] if 'text' in e else sl['text'].get(e['field'], '')
    case = e.get('case')
    if case == 'upper':
        t = t.upper()
    elif case == 'lower':
        t = t.lower()
    elif case == 'spaced':
        t = ' '.join(t.upper())
    if '{' in t and '_j' in sl:              # page numbers: {no} = this slide, {of} = how many
        t = t.replace('{no}', f"{sl['_j'] + 1:02d}").replace('{of}', f"{sl['_n']:02d}")
    return t


def _with_globals(slides):
    """Words in fields named g_… (an @handle, a brand line) are typed once and show on every slide."""
    g = {}
    for sl in slides:
        for k, v in sl['text'].items():
            if k.startswith('g_') and v and k not in g:
                g[k] = v
    n = len(slides)
    return [dict(sl, text={**g, **{k: v for k, v in sl['text'].items() if v or not k.startswith('g_')}}, _j=j, _n=n)
            for j, sl in enumerate(slides)]


def _aa_layer(w, h, s=3):
    """A transparent layer drawn s times larger, for smooth edges once shrunk."""
    return Image.new('RGBA', (max(1, int(w * s)), max(1, int(h * s))), (0, 0, 0, 0))


def _shape_mask(w, h, shape, s=3):
    m = Image.new('L', (w * s, h * s), 0)
    d = ImageDraw.Draw(m)
    if shape == 'circle':
        d.ellipse((0, 0, w * s - 1, h * s - 1), fill=255)
    elif shape == 'arch':
        d.rounded_rectangle((0, 0, w * s - 1, h * s - 1), radius=w * s // 2, fill=255)
        d.rectangle((0, h * s // 2, w * s - 1, h * s - 1), fill=255)
    elif shape == 'pill':
        d.rounded_rectangle((0, 0, w * s - 1, h * s - 1), radius=min(w, h) * s // 2, fill=255)
    elif shape == 'stamp':                    # postage stamp: perforated edge
        r = max(6, min(w, h) // 34)
        d.rectangle((0, 0, w * s - 1, h * s - 1), fill=255)
        n_x, n_y = max(2, int(w / (r * 2.6))), max(2, int(h / (r * 2.6)))
        for i in range(n_x + 1):
            cx = i * w / n_x
            for cy in (0, h):
                d.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s), fill=0)
        for i in range(n_y + 1):
            cy = i * h / n_y
            for cx in (0, w):
                d.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s), fill=0)
    return m.resize((w, h), Image.LANCZOS)


def _draw_pill(cv, ox, e, sl):
    """A label in a rounded box sized to its words (chips, buttons, tags)."""
    t = _text_of(e, sl)
    if not t:
        return
    f = font(e['font'], e['size'])
    track = e.get('track', 0)
    w, _ = text_size(t, f, track)
    px, py = e.get('pad', (30, 14))
    bw, bh = w + 2 * px, e['size'] * 1.2 + 2 * py
    x, y = e['xy']
    a = e.get('anchor', 'mm')
    x0 = x - {'l': 0, 'm': bw / 2, 'r': bw}[a[0]]
    y0 = y - {'t': 0, 'm': bh / 2, 'b': bh}[a[1]]
    _draw_rect(cv, ox, dict(rect=(x0, y0, bw, bh), fill=e.get('fill'), outline=e.get('outline'), width=e.get('width', 3),
                            radius=int(e.get('radius', bh / 2)), shadow=e.get('shadow', 0), rot=e.get('rot', 0)))
    draw_text(cv, (ox + x0 + bw / 2, y0 + bh / 2 + e['size'] * 0.03), t, f, fill=e.get('color', (30, 30, 30)), track=track,
              anchor='mm', shadow=0, rot=e.get('rot', 0))


def riso(im, ink1, ink2, off=(9, 6)):
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    a = ImageOps.colorize(g, tuple(ink1), (255, 255, 255))
    b = ImageOps.colorize(g.point(lambda v: min(255, int(v * 0.55 + 125))), tuple(ink2), (255, 255, 255))
    b = ImageChops.offset(b, int(off[0]), int(off[1]))
    out = ImageChops.multiply(a.convert('RGB'), b.convert('RGB'))
    n = np.random.default_rng(3).normal(0, 9, (out.height, out.width, 1)).astype(np.float32)
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + n, 0, 255).astype(np.uint8))


def _draw_ticket(cv, ox, e):
    """A ticket or boarding pass: rounded card, notches at the tear line, dashed perforation, optional header band."""
    x, y, w, h = e['rect']
    w, h = int(w), int(h)
    s, m = 2, 40
    lay = _aa_layer(w + 2 * m, h + 2 * m, s)
    d = ImageDraw.Draw(lay)
    rad = e.get('radius', 14)
    d.rounded_rectangle((m * s, m * s, (m + w) * s, (m + h) * s), radius=rad * s, fill=tuple(e.get('fill', (243, 236, 220))) + (255,))
    if e.get('band'):
        bc, bh = e['band']
        d.rounded_rectangle((m * s, m * s, (m + w) * s, (m + bh) * s), radius=rad * s, fill=tuple(bc) + (255,))
        d.rectangle((m * s, (m + bh / 2) * s, (m + w) * s, (m + bh) * s), fill=tuple(bc) + (255,))
    sx, r = m + w * e.get('stub', 0.72), e.get('notch', 24)
    for cy in (m, m + h):
        d.ellipse(((sx - r) * s, (cy - r) * s, (sx + r) * s, (cy + r) * s), fill=(0, 0, 0, 0))
    pc = tuple(e.get('perf', (140, 128, 110))) + (210,)
    for yy in range(int(m + r + 10), int(m + h - r - 10), 18):
        d.line((sx * s, yy * s, sx * s, (yy + 9) * s), fill=pc, width=3 * s)
    lay = lay.resize((w + 2 * m, h + 2 * m), Image.LANCZOS)
    if e.get('shadow'):
        sh = Image.new('RGBA', lay.size, (0, 0, 0, 0))
        sh.putalpha(lay.getchannel('A').point(lambda v: v * e['shadow'] // 255))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        sh2 = Image.new('RGBA', lay.size, (0, 0, 0, 0))
        sh2.alpha_composite(sh, (6, 10))
        sh2.alpha_composite(lay)
        lay = sh2
    if e.get('rot'):
        lay = lay.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x + w / 2 - lay.width / 2, y + h / 2 - lay.height / 2)


def _draw_topo(cv, ox, e):
    """Contour lines like a topographic map, around one or more summits."""
    x, y, w, h = e['rect']
    w, h = int(w), int(h)
    s = 2
    lay = _aa_layer(w, h, s)
    d = ImageDraw.Draw(lay)
    col = tuple(e.get('color', (255, 255, 255))) + (e.get('alpha', 70),)
    rng = np.random.default_rng(e.get('seed', 5))
    for cx, cy in e.get('centers', [(w * 0.5, h * 0.5)]):
        ph, amp = rng.uniform(0, 2 * np.pi, 4), rng.uniform(0.05, 0.14, 4)
        for k in range(1, e.get('rings', 12) + 1):
            r0 = k * e.get('step', 40)
            pts = []
            for i in range(181):
                t = 2 * math.pi * i / 180
                rr = r0 * (1 + sum(amp[q] * math.sin((q + 2) * t + ph[q] + k * 0.18) for q in range(4)))
                pts.append(((cx + rr * math.cos(t)) * s, (cy + rr * math.sin(t) * e.get('squash', 0.8)) * s))
            d.line(pts, fill=col, width=int(e.get('width', 2) * s), joint='curve')
    paste(cv, lay.resize((w, h), Image.LANCZOS), ox + x, y)


def _draw_profile(cv, ox, e, sl):
    """An elevation profile: heights typed as '1035, 1650, 2516, …' (metres), drawn as a filled line."""
    x, y, w, h = e['rect']
    t = _text_of(e, sl) if ('field' in e or 'text' in e) else ''
    try:
        hs = [float(v) for v in re.split(r'[,\s]+', t.strip()) if v] if t else []
    except ValueError:
        hs = []
    hs = hs if len(hs) >= 2 else [1035, 1400, 1980, 2516, 1900, 1650, 2200, 2665, 1500]
    lo, hi = min(hs), max(hs)
    s = 2
    lay = _aa_layer(w, h + 60, s)
    d = ImageDraw.Draw(lay)
    pts = [((w * i / (len(hs) - 1)) * s, (40 + (h - 10) * (1 - (v - lo) / (hi - lo + 1e-6))) * s) for i, v in enumerate(hs)]
    col = tuple(e.get('color', (217, 108, 63)))
    d.polygon(pts + [(w * s, (h + 40) * s), (0, (h + 40) * s)], fill=col + (e.get('alpha', 60),))
    d.line(pts, fill=col + (255,), width=4 * s, joint='curve')
    k = hs.index(hi)
    px, py = pts[k]
    d.ellipse((px - 9 * s, py - 9 * s, px + 9 * s, py + 9 * s), fill=col + (255,))
    lay = lay.resize((int(w), int(h + 60)), Image.LANCZOS)
    paste(cv, lay, ox + x, y - 40)
    lab = e.get('label', '{:,.0f} m')
    draw_text(cv, (ox + x + px / s, y - 40 + py / s - 18), lab.format(hi), font(e.get('font', 'consola.ttf'), 24),
              fill=tuple(e.get('tcolor', (255, 255, 255))), anchor='mb', shadow=0)


def _draw_flap(cv, ox, e, sl):
    """Split-flap departure-board letters: one character per dark tile, split across the middle."""
    t = _text_of(e, sl).upper()
    x, y = e['xy']
    th = int(e.get('size', 64))
    tw, gap = int(th * 0.72), e.get('gap', 6)
    n = e.get('cols', len(t))
    f = font(e.get('font', 'consola.ttf'), th * 0.78)
    fg, tile = tuple(e.get('color', (250, 210, 60))), tuple(e.get('tile', (34, 34, 36)))
    lay = Image.new('RGBA', (max(1, n * (tw + gap)), th + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        ch = t[i] if i < len(t) else ' '
        bx = i * (tw + gap)
        d.rounded_rectangle((bx, 0, bx + tw, th), radius=max(2, th // 12), fill=tile + (255,))
        if ch.strip():
            bb = f.getbbox(ch)
            d.text((bx + (tw - (bb[2] - bb[0])) / 2 - bb[0], (th - (bb[3] - bb[1])) / 2 - bb[1]), ch, font=f, fill=fg + (255,))
        d.line((bx, th / 2, bx + tw, th / 2), fill=(0, 0, 0, 160), width=max(1, th // 26))
    paste(cv, lay, ox + x, y)


def _draw_ransom(cv, ox, e, sl):
    """Ransom-note letters: every character cut from a different 'magazine' (font, paper, ink)."""
    t = _text_of(e, sl)
    x, y = e['xy']
    size, maxw = e['size'], e.get('maxw', 960)
    fonts = e.get('fonts', ['impact.ttf', 'COOPBL.TTF', 'GOTHICB.TTF', 'BASKVILL.TTF', 'seguibl.ttf', 'courbd.ttf'])
    fills = [tuple(c) for c in e.get('fills', [(255, 255, 255), (20, 20, 20), (240, 210, 60), (220, 60, 50), (60, 110, 200)])]
    rng = np.random.default_rng(e.get('seed', 7))
    cx, cy = x, y
    for li, line in enumerate(t.split('\n')):
        if li:
            cx, cy = x, cy + size * 1.32
        for wi, word in enumerate(line.split(' ')):
            tiles = []
            for ch in word:                 # cut out the whole word first, so lines only break between words
                k = int(rng.integers(0, 1 << 30))
                fnt = font(fonts[k % len(fonts)], size * rng.uniform(0.82, 1.08))
                bg = fills[k % len(fills)]
                ink = fills[(k // 7 + 1) % len(fills)]
                if ink == bg:
                    ink = fills[(k // 7 + 2) % len(fills)]
                bb = fnt.getbbox(ch)
                pad = int(size * 0.14)
                tile = Image.new('RGBA', (max(1, bb[2] - bb[0] + 2 * pad), int(size * 1.12)), bg + (255,))
                ImageDraw.Draw(tile).text((pad - bb[0], (tile.height - (bb[3] - bb[1])) / 2 - bb[1]), ch, font=fnt, fill=ink + (255,))
                tiles.append((tile.rotate(rng.uniform(-7, 7), resample=Image.BICUBIC, expand=True), rng.uniform(-6, 6)))
            ww = sum(tl.width + 2 for tl, _ in tiles)
            if wi and cx > x and cx + ww > x + maxw:
                cx, cy = x, cy + size * 1.32
            for tl, dy in tiles:
                paste(cv, tl, ox + cx, cy + dy)
                cx += tl.width + 2
            cx += size * 0.42


def _draw_poly(cv, ox, e):
    pts = e['pts']
    s = 3
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    lay = _aa_layer(x1 - x0 + 4, y1 - y0 + 4, s)
    ImageDraw.Draw(lay).polygon([((px - x0 + 2) * s, (py - y0 + 2) * s) for px, py in pts], fill=tuple(e['fill']) + (e.get('alpha', 255),))
    paste(cv, lay.resize((int(x1 - x0 + 4), int(y1 - y0 + 4)), Image.LANCZOS), ox + x0 - 2, y0 - 2)


def _draw_chips(cv, ox, e, sl):
    """A row of pills that wraps onto the next line (one pill per field)."""
    x0, y = e['xy']
    maxw, gap = e.get('maxw', 940), e.get('gap', 16)
    f = font(e['font'], e['size'])
    px, py = e.get('pad', (30, 14))
    bh = e['size'] * 1.2 + 2 * py
    fills = e.get('fills', [(255, 255, 255)])
    x = x0
    for k, fld in enumerate(e['fields']):
        t = str(sl['text'].get(fld, '')).strip()
        if not t:
            continue
        w = text_size(t, f, e.get('track', 0))[0] + 2 * px
        if x > x0 and x + w > x0 + maxw:
            x, y = x0, y + bh + gap
        _draw_pill(cv, ox, dict(text=t, xy=(x, y), anchor='lt', font=e['font'], size=e['size'], pad=(px, py), fill=fills[k % len(fills)],
                                color=e.get('color'), outline=e.get('outline'), width=e.get('width', 3), shadow=e.get('shadow', 0),
                                track=e.get('track', 0)), sl)
        x += w + gap


def _draw_spark(cv, ox, e):
    """A four-point sparkle ✦ (curved sides)."""
    x, y = e['xy']
    r = e.get('r', 34)
    s = 3
    lay = _aa_layer(2 * r + 4, 2 * r + 4, s)
    c = (r + 2) * s
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        ca, sa = math.cos(a), math.sin(a)
        pts.append((c + r * s * (abs(ca) ** 3) * (1 if ca >= 0 else -1), c + r * s * (abs(sa) ** 3) * (1 if sa >= 0 else -1)))
    ImageDraw.Draw(lay).polygon(pts, fill=tuple(e.get('color', (255, 255, 255))) + (e.get('alpha', 255),))
    lay = lay.resize((2 * r + 4, 2 * r + 4), Image.LANCZOS)
    if e.get('rot'):
        lay = lay.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x - lay.width / 2, y - lay.height / 2)


def _draw_badge(cv, ox, e, sl):
    """Words running round a circle (the round 'stamp' badge), with an optional word or symbol in the middle."""
    x, y, r = e['xy'][0], e['xy'][1], e['r']
    s = 2
    col = tuple(e.get('color', (30, 30, 30)))
    sz = int(2 * r + 12)
    lay = _aa_layer(sz, sz, s)
    d = ImageDraw.Draw(lay)
    c = sz * s / 2
    if e.get('fill'):
        d.ellipse((c - r * s, c - r * s, c + r * s, c + r * s), fill=tuple(e['fill']) + (255,))
    if e.get('ring', True):
        d.ellipse((c - r * s, c - r * s, c + r * s, c + r * s), outline=col + (255,), width=max(2, int(e.get('ringw', 2) * s)))
    t = _text_of(e, sl).upper()
    f = font(e['font'], e['size'] * s)
    rr = (r - e['size'] * 0.55 - e.get('inset', 12)) * s
    if t and rr > 0:
        ws = [f.getlength(ch) for ch in t]
        total = sum(ws)
        reps = max(1, int(2 * math.pi * rr / max(1, total * 1.15)))
        seq = (t * reps)
        ws = ws * reps
        gap = (2 * math.pi * rr - sum(ws)) / len(seq)
        ang = 0.0
        for ch, cw in zip(seq, ws):
            mid = ang + (cw / 2) / rr
            if ch.strip():
                g = Image.new('RGBA', (int(cw) + 8, int(e['size'] * s * 1.4) + 8), (0, 0, 0, 0))
                ImageDraw.Draw(g).text((4, 4), ch, font=f, fill=col + (255,))
                g = g.rotate(-math.degrees(mid), resample=Image.BICUBIC, expand=True)
                gx, gy = c + rr * math.sin(mid), c - rr * math.cos(mid)
                lay.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
            ang += (cw + gap) / rr
    lay = lay.resize((sz, sz), Image.LANCZOS)
    if e.get('center'):
        draw_text(lay, (sz / 2, sz / 2), e['center'], font(e.get('cfont', e['font']), e.get('csize', r * 0.5)), fill=col, anchor='mm', shadow=0)
    if e.get('rot'):
        lay = lay.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x - lay.width / 2, y - lay.height / 2)


def _draw_waves(cv, ox, e):
    """Wavy postmark lines."""
    x, y, w, h = e['rect']
    n, amp, per = e.get('n', 5), e.get('amp', 9), e.get('period', 80)
    s = 2
    lay = _aa_layer(w + 4 * amp, h + 4 * amp, s)
    d = ImageDraw.Draw(lay)
    col = tuple(e.get('color', (40, 60, 140))) + (e.get('alpha', 230),)
    for i in range(n):
        yy = (2 * amp + (h * i / max(1, n - 1))) * s
        pts = [((2 * amp + px) * s, yy + amp * s * math.sin(2 * math.pi * px / per)) for px in range(0, int(w) + 1, 4)]
        d.line(pts, fill=col, width=int(e.get('width', 5) * s), joint='curve')
    lay = lay.resize((int(w + 4 * amp), int(h + 4 * amp)), Image.LANCZOS)
    if e.get('rot'):
        lay = lay.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x + w / 2 - lay.width / 2, y + h / 2 - lay.height / 2)


def _draw_ellipse(cv, ox, e):
    x, y, w, h = e['rect']
    s = 3
    lay = _aa_layer(w + 8, h + 8, s)
    ImageDraw.Draw(lay).ellipse((4 * s, 4 * s, (w + 4) * s, (h + 4) * s), fill=tuple(e['fill']) + (e.get('alpha', 255),) if e.get('fill') else None,
                                outline=tuple(e['outline']) + (255,) if e.get('outline') else None, width=int(e.get('width', 3) * s))
    lay = lay.resize((int(w + 8), int(h + 8)), Image.LANCZOS)
    paste(cv, lay, ox + x - 4, y - 4)


def _draw_ruled(cv, ox, e):
    """Notebook paper: lines, a dot grid or squares."""
    x, y, w, h = e['rect']
    step = e.get('step', 54)
    col = tuple(e.get('color', (120, 140, 180))) + (e.get('alpha', 70),)
    lay = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    kind = e.get('kind', 'lines')
    if kind == 'dots':
        for py in range(step // 2, int(h), step):
            for px in range(step // 2, int(w), step):
                d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=col)
    else:
        for py in range(step, int(h), step):
            d.line((0, py, w, py), fill=col, width=2)
        if kind == 'grid':
            for px in range(step, int(w), step):
                d.line((px, 0, px, h), fill=col, width=2)
    paste(cv, lay, ox + x, y)


def _grain(im, amount, seed):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), np.float32)
    n = rng.normal(0, amount, a.shape[:2]).astype(np.float32)[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).convert('RGBA')


def _draw_text(cv, ox, e, sl):
    t = _text_of(e, sl)
    if not t:
        return
    size = e['size']
    track = e.get('track', 0)
    f = font(e['font'], size)
    if e.get('fit'):
        while size > 10 and max(text_size(ln, f, track)[0] for ln in t.split('\n')) > e['fit']:
            size = int(size * 0.92)
            f = font(e['font'], size)
    lines = wrap_lines(t, f, e['wrap'], track) if e.get('wrap') else t.split('\n')
    lh = e.get('lh', 1.18) * size
    x, y = e['xy']
    if e.get('valign') == 'bottom':
        y -= lh * (len(lines) - 1)
    elif e.get('valign') == 'middle':
        y -= lh * (len(lines) - 1) / 2
    anchor = e.get('anchor', 'mt')
    if e.get('hl') or e.get('ul'):           # a marker highlight behind each line / an underline under it
        d = ImageDraw.Draw(cv)
        for k, line in enumerate(lines):
            if not line.strip():
                continue
            lw, lhh = text_size(line, f, track)
            x0 = ox + x - {'l': 0, 'm': lw / 2, 'r': lw}[anchor[0]]
            y0 = y + k * lh - {'t': 0, 'm': lhh / 2, 'b': lhh}[anchor[1]]
            if e.get('hl'):
                col, px, py = e['hl']
                d.rectangle((x0 - px, y0 + size * 0.18 - py, x0 + lw + px, y0 + size * 1.08 + py), fill=tuple(col) + (255,))
            if e.get('ul'):
                col, wd = e['ul']
                uy = y0 + size * 1.12
                d.line((x0, uy, x0 + lw, uy), fill=tuple(col) + (255,), width=wd)
    for k, line in enumerate(lines):
        draw_text(cv, (ox + x, y + k * lh), line, f, fill=e.get('color', (255, 255, 255)), track=track, anchor=anchor,
                  shadow=e.get('shadow', 110), blur=e.get('sblur', 6), rot=e.get('rot', 0), stroke=e.get('stroke', 0),
                  outline=e.get('outline', False), alpha=e.get('alpha', 255), scol=e.get('scol'))


def _draw_rect(cv, ox, e):
    x, y, w, h = e['rect']
    lay = Image.new('RGBA', (int(w) + 60, int(h) + 60), (0, 0, 0, 0))
    box = (30, 30, 30 + int(w) - 1, 30 + int(h) - 1)
    if e.get('shadow'):                      # soft shadow under the box
        sh = Image.new('RGBA', lay.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((36, 40, 36 + int(w) - 1, 40 + int(h) - 1), radius=e.get('radius', 0), fill=(0, 0, 0, e['shadow']))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(lay)
    fill = e.get('fill')
    d.rounded_rectangle(box, radius=e.get('radius', 0), fill=tuple(fill) if fill else None,
                        outline=tuple(e['outline']) if e.get('outline') else None, width=e.get('width', 0))
    if e.get('rot'):
        lay = lay.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
        paste(cv, lay, ox + x + w / 2 - lay.width / 2, y + h / 2 - lay.height / 2)
    else:
        paste(cv, lay, ox + x - 30, y - 30)


def _draw_line(cv, ox, e):
    d = ImageDraw.Draw(cv)
    pts = [(ox + px, py) for px, py in e['pts']]
    col = tuple(e.get('color', (255, 255, 255))) + (e.get('alpha', 255),)
    wd = e.get('width', 2)
    if e.get('dash'):
        on, off = e['dash']
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            k = 0.0
            while k < L:
                a, b2 = k / L, min(L, k + on) / L
                d.line((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b2, y0 + (y1 - y0) * b2), fill=col, width=wd)
                k += on + off
    else:
        d.line(pts, fill=col, width=wd, joint='curve')


def _bezier(p0, p1, p2, p3, n=40):
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c2, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c2 * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c2 * p2[1] + d * p3[1]))
    return out


def _draw_tape(cv, ox, e):
    x, y, w, h = e['rect']
    lay = Image.new('RGBA', (int(w), int(h)), tuple(e.get('color', (235, 225, 196))) + (e.get('alpha', 175),))
    d = ImageDraw.Draw(lay)
    for k in range(0, int(h), 6):          # ragged torn ends
        d.polygon([(0, k), (5, k + 3), (0, k + 6)], fill=(0, 0, 0, 0))
        d.polygon([(w, k), (w - 5, k + 3), (w, k + 6)], fill=(0, 0, 0, 0))
    lay = lay.rotate(e.get('rot', 0), resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x + w / 2 - lay.width / 2, y + h / 2 - lay.height / 2)


def _draw_torn(cv, ox, e, j):
    x, y, w, h = e['rect']
    rng = np.random.default_rng(e.get('seed', 7) + j)
    pts_top = [(px, rng.uniform(0, 14)) for px in range(0, int(w) + 1, 18)]
    pts_bot = [(px, h - rng.uniform(0, 14)) for px in range(int(w), -1, -18)]
    lay = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon(pts_top + pts_bot, fill=tuple(e.get('color', (246, 240, 228))) + (255,))
    sh = Image.new('RGBA', (lay.width + 40, lay.height + 40), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 90), (20, 24), lay.getchannel('A'))
    lay2 = sh.filter(ImageFilter.GaussianBlur(8))
    lay2.alpha_composite(lay, (20, 20))
    if e.get('rot'):
        lay2 = lay2.rotate(e['rot'], resample=Image.BICUBIC, expand=True)
    paste(cv, lay2, ox + x + w / 2 - lay2.width / 2, y + h / 2 - lay2.height / 2)


def _draw_stamp(cv, ox, e, sl):
    x, y, r = e['xy'][0], e['xy'][1], e['r']
    col = tuple(e.get('color', (170, 40, 40)))
    sz = int(r * 2 + 20)
    lay = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx = cy = sz / 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (230,), width=5)
    d.ellipse((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), outline=col + (230,), width=2)
    t = _text_of(e, sl).upper()
    lines = [s.strip() for s in t.split('·')] if '·' in t else [t]
    f1, f2 = font('GOTHICB.TTF', r * 0.36), font('GOTHIC.TTF', r * 0.2)
    if lines:
        w1, h1 = text_size(lines[0], f1, 2)
        while w1 > r * 1.5 and f1.size > 10:
            f1 = font('GOTHICB.TTF', f1.size * 0.9); w1, h1 = text_size(lines[0], f1, 2)
        d.text((cx - w1 / 2, cy - h1 / 2 - (r * 0.12 if len(lines) > 1 else 0)), lines[0], font=f1, fill=col + (235,))
        for k, ln in enumerate(lines[1:3]):
            w2, h2 = text_size(ln, f2, 3)
            d.text((cx - w2 / 2, cy + h1 * 0.45 + k * h2), ln, font=f2, fill=col + (235,))
    # worn ink: knock out speckles
    rng = np.random.default_rng(int(x + y))
    a = np.asarray(lay.getchannel('A'), np.float32) * (rng.random((sz, sz)) > 0.18)
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    lay = lay.rotate(e.get('rot', -12), resample=Image.BICUBIC, expand=True)
    paste(cv, lay, ox + x - lay.width / 2, y - lay.height / 2)


def _draw_film(cv, ox, e):
    """A strip of 35mm film (black band with sprocket holes) across the given area."""
    x, y, w, h = e['rect']
    d = ImageDraw.Draw(cv)
    d.rectangle((ox + x, y, ox + x + w, y + h), fill=(16, 14, 12, 255))
    hole_w, hole_h, step = 26, 36, 58
    for px in range(int(ox + x) + 14, int(ox + x + w) - 20, step):
        for py in (y + 18, y + h - 18 - hole_h):
            d.rounded_rectangle((px, py, px + hole_w, py + hole_h), radius=5, fill=tuple(e.get('hole', (240, 234, 222))) + (255,))


def _draw_masktext(cv, ox, e, c, sl, j, T, boxes):
    """Big letters with photos inside them (one photo per letter, cycling through the given slots)."""
    t = _text_of(e, sl).replace(' ', '')
    if not t:
        return
    x, y, w, h = e['rect']
    vertical = e.get('dir') == 'v'
    n = len(t)
    slots = e['slots']
    for k, ch in enumerate(t):
        if vertical:
            cw, chh = w, h / n
            bx, by = x, y + k * chh
        else:
            cw, chh = w / n, h
            bx, by = x + k * cw, y
        size = int(min(chh * 1.25, cw * 1.35))
        f = font(e['font'], size)
        bb = f.getbbox(ch)
        while (bb[2] - bb[0] > cw * 0.98 or bb[3] - bb[1] > chh * 0.98) and size > 10:
            size = int(size * 0.94); f = font(e['font'], size); bb = f.getbbox(ch)
        lw, lh = bb[2] - bb[0], bb[3] - bb[1]
        mask = Image.new('L', (max(1, lw), max(1, lh)), 0)
        ImageDraw.Draw(mask).text((-bb[0], -bb[1]), ch, font=f, fill=255)
        slot = slots[k % len(slots)]
        ph = sl['photos'][slot] if slot < len(sl['photos']) else None
        fillim = c.photo(ph, lw, lh, '').convert('RGBA')
        fillim.putalpha(mask)
        px, py = ox + bx + (cw - lw) / 2, by + (chh - lh) / 2
        if e.get('shadow'):
            sh = Image.new('RGBA', (lw + 60, lh + 60), (0, 0, 0, 0))
            sh.paste((0, 0, 0, e['shadow']), (30, 30), mask)
            paste(cv, sh.filter(ImageFilter.GaussianBlur(10)), px - 30 + 6, py - 30 + 8)
        ow = int(e['outline'][1]) if e.get('outline') else 0
        shape = mask
        if ow:                                   # a coloured outline round each letter (postcard block letters)
            shape = Image.new('L', (lw + 2 * ow, lh + 2 * ow), 0)
            shape.paste(mask, (ow, ow))
            shape = shape.filter(ImageFilter.MaxFilter(2 * ow + 1))
        if e.get('extrude'):                     # a solid 3D side, stepped down-right
            dx, dy, steps, col = e['extrude']
            solid = Image.new('RGBA', shape.size, tuple(col) + (255,))
            solid.putalpha(shape)
            for st in range(int(steps), 0, -1):
                paste(cv, solid, px - ow + dx * st / steps, py - ow + dy * st / steps)
        if ow:
            ol = Image.new('RGBA', shape.size, tuple(e['outline'][0]) + (255,))
            ol.putalpha(shape)
            paste(cv, ol, px - ow, py - ow)
        paste(cv, fillim, px, py)
        if k < len(slots):
            boxes.append({'i': slot, 'slide': j, 'rect': [px, py, px + lw, py + lh], 'rot': 0})


def _draw_mosaic(cv, ox, e, c, sl, j, T, boxes):
    """Many photos in a grid, turned at an angle (the 'decoding' mosaic)."""
    x, y, w, h = e['rect']
    cols, rows, gap, rot = e.get('cols', 3), e.get('rows', 3), e.get('gap', 14), e.get('rot', -12)
    tw, th = e.get('tile', (420, 520))
    big = Image.new('RGBA', (cols * tw + (cols - 1) * gap, rows * th + (rows - 1) * gap), (0, 0, 0, 0))
    slots = e['slots']
    for k in range(cols * rows):
        slot = slots[k % len(slots)]
        ph = sl['photos'][slot] if slot < len(sl['photos']) else None
        big.paste(c.photo(ph, tw, th, ''), ((k % cols) * (tw + gap), (k // cols) * (th + gap)))
    big = big.rotate(rot, resample=Image.BICUBIC, expand=True)
    cx, cy = ox + x + w / 2, y + h / 2
    paste(cv, big, cx - big.width / 2, cy - big.height / 2)
    r = math.radians(rot)
    gw, gh = cols * tw + (cols - 1) * gap, rows * th + (rows - 1) * gap
    for k, slot in enumerate(slots[:cols * rows]):
        tx, ty = (k % cols) * (tw + gap) + tw / 2 - gw / 2, (k // cols) * (th + gap) + th / 2 - gh / 2
        qx, qy = tx * math.cos(r) + ty * math.sin(r), -tx * math.sin(r) + ty * math.cos(r)
        bx, by = cx + qx, cy + qy
        boxes.append({'i': slot, 'slide': j, 'rect': [bx - tw / 2, by - th / 2, bx + tw / 2, by + th / 2], 'rot': rot})


def _draw_swatches(cv, ox, e, c, sl):
    """Five colours taken from the photo, with their hex codes (moodboard palette)."""
    x, y, w, h = e['rect']
    slot = e['slot']
    ph = sl['photos'][slot] if slot < len(sl['photos']) else None
    im = c.raw(ph)
    if im is None:
        return
    q = im.resize((120, 120)).quantize(colors=6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:18]
    counts = sorted(q.getcolors(), reverse=True)
    cols = [tuple(pal[i * 3:i * 3 + 3]) for _, i in counts][:5]
    cols.sort(key=lambda cc: sum(cc))
    n = len(cols)
    sw = (w - (n - 1) * 14) / max(1, n)
    d = ImageDraw.Draw(cv)
    f = font('consola.ttf', 20)
    for k, col in enumerate(cols):
        bx = ox + x + k * (sw + 14)
        d.rounded_rectangle((bx, y, bx + sw, y + h - 40), radius=10, fill=col + (255,))
        hx = '#%02X%02X%02X' % col
        d.text((bx + sw / 2 - f.getlength(hx) / 2, y + h - 30), hx, font=f, fill=tuple(e.get('color', (60, 56, 50))) + (255,))


def _draw_route(cv, ox, e, j, n):
    """A dashed travel route from this slide to the next (follow-the-line / travelling-icon carousels)."""
    if j >= n - 1:
        return
    (x0, y0), (x1, y1) = e['a'], e['b']
    p0, p3 = (ox + x0, y0), (ox + W + x1, y1)
    pts = _bezier(p0, (p0[0] + 260, p0[1] + e.get('bend', 260)), (p3[0] - 260, p3[1] - e.get('bend', 260)), p3)
    d = ImageDraw.Draw(cv)
    col = tuple(e.get('color', (120, 96, 72))) + (255,)
    for k in range(0, len(pts) - 1, 2):
        d.line((pts[k], pts[k + 1]), fill=col, width=4)
    mid = pts[len(pts) // 2]
    f = font('seguisym.ttf', 54)
    draw_text(cv, (mid[0] - ox, mid[1]), '✈', f, fill=col[:3], anchor='mm', shadow=0)  # drawn in strip space below
    return


def _draw_bg(cv, ox, bg, c, sl, j, T, boxes, width=W):
    if bg is None:
        return
    if isinstance(bg, tuple) and len(bg) in (3, 4) and all(isinstance(v, int) for v in bg):
        ImageDraw.Draw(cv).rectangle((ox, 0, ox + width, H), fill=tuple(bg[:3]) + (255,))
    elif bg[0] == 'paper':
        paste(cv, paper(width, H, tuple(bg[1]) if len(bg) > 1 else (240, 234, 222), seed=7), ox, 0)
    elif bg[0] == 'grad':
        a, b = np.array(bg[1], np.float32), np.array(bg[2], np.float32)
        t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        arr = np.broadcast_to(a + (b - a) * t, (H, width, 3))
        paste(cv, Image.fromarray(arr.astype(np.uint8)).convert('RGBA'), ox, 0)
    elif bg[0] == 'linen':                  # linen-finish postcard card: fine woven texture
        tone = np.array(bg[1] if len(bg) > 1 else (238, 226, 200), np.float32)
        rng = np.random.default_rng(9)
        arr = np.broadcast_to(tone, (H, width, 3)).copy()
        arr *= (1 - 0.05 * (np.arange(H) % 3 == 0))[:, None, None]
        arr *= (1 - 0.035 * (np.arange(width) % 3 == 0))[None, :, None]
        arr += rng.normal(0, 5, (H, width, 1))
        paste(cv, Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA'), ox, 0)
    elif bg[0] == 'blur':
        slot, dim = bg[1], bg[2] if len(bg) > 2 else 0.45
        ph = sl['photos'][slot] if slot < len(sl['photos']) else None
        im = c.photo(ph, width // 6, H // 6, '').filter(ImageFilter.GaussianBlur(5)).resize((width, H), Image.BICUBIC)
        im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), dim)
        paste(cv, im.convert('RGBA'), ox, 0)


def r_generic(c, T):
    out, boxes = _r_generic(c, T)
    if T.get('grain'):
        out = [_grain(s, T['grain'], 11 + j) for j, s in enumerate(out)]
    return out, boxes


def _r_generic(c, T):
    spec = c.spec
    slides = _with_globals(spec['slides'])
    n = len(slides)
    strip = T.get('strip')
    boxes = [[] for _ in slides]
    if strip:
        canvas = Image.new('RGBA', (n * W, H), (18, 18, 20, 255))
        if T.get('bg') is not None:
            _draw_bg(canvas, 0, T['bg'], c, slides[0] if slides else None, 0, T, None, width=n * W)
        sbox = []
        for e in T.get('strip_els', []):     # things that run the whole length of the carousel (a film strip)
            e = dict(e)
            if 'rect' in e and e['rect'][2] == -1:
                e['rect'] = (e['rect'][0], e['rect'][1], n * W, e['rect'][3])
            _draw_el(canvas, 0, e, c, slides[0], 0, T, sbox, n)
        for z in (0, 1, 2):
            for j, sl in enumerate(slides):
                K = T['kinds'][sl['kind']]
                if z == 0 and K.get('bg') is not None:
                    _draw_bg(canvas, j * W, K['bg'], c, sl, j, T, sbox)
                for e in K['els']:
                    if e.get('z', 1) == z:
                        _draw_el(canvas, j * W, e, c, sl, j, T, sbox, n)
        out = [canvas.crop((j * W, 0, (j + 1) * W, H)) for j in range(n)]
        for b in sbox:
            for j in range(n):
                x0, x1 = b['rect'][0] - j * W, b['rect'][2] - j * W
                if x1 > 0 and x0 < W:
                    boxes[j].append(dict(b, rect=[x0, b['rect'][1], x1, b['rect'][3]]))
        return out, boxes
    out = []
    for j, sl in enumerate(slides):
        K = T['kinds'][sl['kind']]
        cv = Image.new('RGBA', (W, H), (18, 18, 20, 255))
        _draw_bg(cv, 0, K['bg'] if K.get('bg') is not None else T.get('bg', (18, 18, 20)), c, sl, j, T, boxes[j])
        for e in K['els']:
            _draw_el(cv, 0, e, c, sl, j, T, boxes[j], n)
        out.append(cv)
    return out, boxes


def _draw_el(cv, ox, e, c, sl, j, T, boxes, n):
    t = e['t']
    if t == 'photo':
        _draw_photo(cv, ox, e, c, sl, j, T, boxes)
    elif t == 'text':
        _draw_text(cv, ox, e, sl)
    elif t == 'rect':
        _draw_rect(cv, ox, e)
    elif t == 'line':
        _draw_line(cv, ox, e)
    elif t == 'tape':
        _draw_tape(cv, ox, e)
    elif t == 'torn':
        _draw_torn(cv, ox, e, j)
    elif t == 'stamp':
        _draw_stamp(cv, ox, e, sl)
    elif t == 'film':
        _draw_film(cv, ox, e)
    elif t == 'mask':
        _draw_masktext(cv, ox, e, c, sl, j, T, boxes)
    elif t == 'mosaic':
        _draw_mosaic(cv, ox, e, c, sl, j, T, boxes)
    elif t == 'swatch':
        _draw_swatches(cv, ox, e, c, sl)
    elif t == 'route':
        if j < n - 1:
            (x0, y0), (x1, y1) = e['a'], e['b']
            p0, p3 = (ox + x0, y0), (ox + W + x1, y1)
            bend = e.get('bend', 260)
            pts = _bezier(p0, (p0[0] + 300, p0[1] + bend), (p3[0] - 300, p3[1] - bend), p3)
            d = ImageDraw.Draw(cv)
            col = tuple(e.get('color', (120, 96, 72))) + (255,)
            for k in range(0, len(pts) - 1, 2):
                d.line((pts[k], pts[k + 1]), fill=col, width=4)
            if e.get('icon', True):
                mid = pts[len(pts) // 2]
                draw_text(cv, (mid[0], mid[1]), '✈', font('seguisym.ttf', 54), fill=col[:3], anchor='mm', shadow=0, rot=e.get('irot', -20))
    elif t == 'pill':
        _draw_pill(cv, ox, e, sl)
    elif t == 'chips':
        _draw_chips(cv, ox, e, sl)
    elif t == 'spark':
        _draw_spark(cv, ox, e)
    elif t == 'badge':
        _draw_badge(cv, ox, e, sl)
    elif t == 'waves':
        _draw_waves(cv, ox, e)
    elif t == 'ellipse':
        _draw_ellipse(cv, ox, e)
    elif t == 'flap':
        _draw_flap(cv, ox, e, sl)
    elif t == 'ransom':
        _draw_ransom(cv, ox, e, sl)
    elif t == 'poly':
        _draw_poly(cv, ox, e)
    elif t == 'ticket':
        _draw_ticket(cv, ox, e)
    elif t == 'topo':
        _draw_topo(cv, ox, e)
    elif t == 'profile':
        _draw_profile(cv, ox, e, sl)
    elif t == 'ruled':
        _draw_ruled(cv, ox, e)
    elif t == 'bgphoto':
        _draw_bg(cv, ox, ('blur', e['slot'], e.get('dim', 0.45)), c, sl, j, T, boxes)
    elif t == 'shade':                      # soft dark gradient so text reads on a busy photo
        x, y, w, h = e['rect']
        col = tuple(e.get('color', (0, 0, 0)))
        a = np.linspace(e.get('a0', 0), e.get('a1', 170), int(h), dtype=np.float32)[:, None]
        lay = np.zeros((int(h), int(w), 4), np.uint8)
        lay[..., :3] = col
        lay[..., 3] = np.broadcast_to(a, (int(h), int(w))).astype(np.uint8)
        paste(cv, Image.fromarray(lay, 'RGBA'), ox + x, y)
    elif t == 'chars':                      # one letter of a word per given x position (letter strips)
        letters = [ch for ch in _text_of(e, sl) if not ch.isspace()]
        f = font(e['font'], e['size'])
        for k, xx in enumerate(e['xs']):
            if k < len(letters):
                draw_text(cv, (ox + xx, e['y']), letters[k], f, fill=e.get('color', (255, 255, 255)), anchor='mt',
                          shadow=e.get('shadow', 150), blur=8)


RENDERERS = {'pair': r_pair, 'frames3': r_frames3, 'postcards': r_postcards}
TEMPLATES = {}


def register(tpls):
    """Add generic templates (from carousel_templates.py) to the formats Carousel Studio offers."""
    for T in tpls:
        TEMPLATES[T['key']] = T
        FORMATS[T['key']] = {'label': T['label'], 'about': T['about'], 'look': T.get('look', ('natural', 0.8)),
                             'group': T.get('group', 'More'), 'ref': T.get('ref', ''), 'new': bool(T.get('new')),
                             'kinds': {k: {'label': K['label'], 'photos': K['photos'], 'fields': [[f[0], f[1]] for f in K.get('fields', [])],
                                           'defaults': {f[0]: (f[2] if len(f) > 2 else '') for f in K.get('fields', [])}}
                                       for k, K in T['kinds'].items()},
                             'default': T['default']}
        RENDERERS[T['key']] = (lambda TT: (lambda c: r_generic(c, TT)))(T)


for _k, _g, _r in (('pair', 'Your references', '@travelwith_surbhi'), ('frames3', 'Your references', '@ogik_jatmiko'),
                   ('postcards', 'Your references', 'mahemac / untitled.storiez')):
    FORMATS[_k].update(group=_g, ref=_r)
FORMATS['pair']['default'] = ['pair'] * 5
FORMATS['frames3']['default'] = ['cover'] + ['triptych'] * 5
FORMATS['postcards']['default'] = ['strips'] + ['card'] * 6 + ['end']
try:
    import carousel_templates
    register(carousel_templates.TEMPLATES)
except ImportError:
    pass
# Later collections (new=True, shown first): the 11 design systems and wave 2 from Carousels\Inspiration library,
# the Canva/SCRL-styled set (carousel_templates_pro) and colour/type versions of the best of them.
for _mod in ('carousel_templates_systems', 'carousel_templates_wave2', 'carousel_templates_pro', 'carousel_templates_variants'):
    try:
        register(__import__(_mod).TEMPLATES)
    except ImportError as _e:
        print(_mod, 'not loaded:', _e)

# The gallery groups templates by style, whichever batch they came from.
STYLES = ['Your references', 'Editorial & magazine', 'Cinematic', 'Minimal & journal', 'Vintage & postcards', 'Scrapbook & polaroid',
          'Film & analog', 'Guides & itineraries', 'Seamless & panorama', 'Bold type & posters', 'Adventure & outdoor',
          'Collage & experimental', 'Grids & photo dumps', 'Fun & story']
_STYLE_OF_GROUP = {'Polaroids & paper': 'Scrapbook & polaroid', 'Seamless': 'Seamless & panorama', 'Guides & tips': 'Guides & itineraries',
                   'Editorial & minimal': 'Editorial & magazine', 'Postcards & stamps': 'Vintage & postcards', 'Fun & story': 'Fun & story',
                   'Grids & collages': 'Grids & photo dumps', 'New · Seamless': 'Seamless & panorama', 'New · Bold type': 'Bold type & posters',
                   'New · Editorial': 'Editorial & magazine', 'New · Scrapbook': 'Scrapbook & polaroid', 'New · Guides & fun': 'Guides & itineraries',
                   'New · Grids': 'Grids & photo dumps', 'Seamless (cross the edges)': 'Seamless & panorama'}
_STYLE_OF_KEY = {'sys_broadsheet': 'Editorial & magazine', 'sys_still_frame': 'Cinematic', 'sys_quiet_journal': 'Minimal & journal',
                 'sys_greetings_from': 'Vintage & postcards', 'sys_ticket_diary': 'Scrapbook & polaroid', 'sys_contact_sheet': 'Film & analog',
                 'sys_field_guide': 'Guides & itineraries', 'sys_giant_word': 'Seamless & panorama', 'sys_poster_series': 'Bold type & posters',
                 'sys_expedition': 'Adventure & outdoor', 'sys_riso_collage': 'Collage & experimental', 'typewriter_notes': 'Minimal & journal',
                 'arch_windows': 'Minimal & journal', 'gallery_wall': 'Minimal & journal', 'moments_chrome': 'Cinematic', 'torn_quote': 'Scrapbook & polaroid'}
for _k, _F in FORMATS.items():
    _TT = TEMPLATES.get(_k) or {}
    _F['group'] = (_TT.get('style') or _STYLE_OF_KEY.get(_k) or _STYLE_OF_KEY.get(_TT.get('base', '')) or
                   _STYLE_OF_GROUP.get(_TT.get('group', _F.get('group')), _F.get('group')))
    _F['batch'] = _TT.get('batch', '')
_rlock = threading.Lock()


def render(folder, spec, full=False):
    """Render every slide. full=False uses smaller copies of the photos (quick previews)."""
    spec = clean_spec(spec)
    with _rlock:
        slides, boxes = RENDERERS[spec['format']](Ctx(folder, spec, None if full else 1600))
    return [s.convert('RGB') for s in slides], boxes


def export(folder, spec):
    """Full-size slides 01.jpg, 02.jpg ... in the carousel folder, plus _preview.jpg."""
    slides, _ = render(folder, spec, full=True)
    for f in os.listdir(folder):
        if re.fullmatch(r'\d\d\.jpg', f):
            os.remove(os.path.join(folder, f))
    names = []
    for i, s in enumerate(slides, 1):
        fn = f'{i:02d}.jpg'
        s.save(os.path.join(folder, fn), quality=95, subsampling=0)
        names.append(fn)
    tw = 270
    th = int(tw * H / W)
    pv = Image.new('RGB', (len(slides) * (tw + 8) + 8, th + 16), (18, 18, 20))
    for i, s in enumerate(slides):
        pv.paste(s.resize((tw, th), Image.LANCZOS), (8 + i * (tw + 8), 8))
    pv.save(os.path.join(folder, '_preview.jpg'), quality=90)
    return names
