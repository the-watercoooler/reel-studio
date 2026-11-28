"""Find fonts on Windows and macOS (and Linux) by their Windows file names.

Reel Studio's text styles and carousel templates name Windows fonts (e.g. 'GOTHIC.TTF', 'SitkaVF.ttf#Banner').
On Windows those files are used as they are. Elsewhere - or when one is missing - each name maps to the closest
font that comes with macOS, or to a font placed in Reel Studio's own fonts\\ folder (which always wins).
load() never raises: the last resort is Pillow's built-in font, so a missing font can never stop a render.

Stand-ins are written 'File.ext' or 'Collection.ttc|Style', where Style picks a face inside a .ttc collection
(matched against the face's own style name, e.g. 'Bold', 'Italic', 'Light').
"""
import os, sys
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(HERE, 'fonts')

# The helper tools in tools\ all import this module and call 'ffmpeg' / 'ffprobe' by name. On a Mac, a shell may not
# have Homebrew's folder on PATH (and on Windows a fresh winget install may not be on it yet), so add those folders.
_ff = ['/opt/homebrew/bin', '/usr/local/bin', '/opt/local/bin']
if sys.platform.startswith('win'):
    _la = os.environ.get('LOCALAPPDATA', '')
    _ff = [os.path.join(_la, 'Microsoft', 'WinGet', 'Links')]
for _d in _ff:
    if os.path.isdir(_d) and _d not in os.environ.get('PATH', '').split(os.pathsep):
        os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + _d


def font_dirs(platform=None):
    p = platform or sys.platform
    if p.startswith('win'):
        return [BUNDLED, os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts')]
    if p == 'darwin':
        return [BUNDLED, '/System/Library/Fonts/Supplemental', '/System/Library/Fonts', '/Library/Fonts',
                os.path.expanduser('~/Library/Fonts')]
    return [BUNDLED, '/usr/share/fonts/truetype', '/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.local/share/fonts')]


# Windows font file -> stand-ins tried in order (only when the file itself isn't found)
SERIF = ['InstrumentSerif-Regular.ttf', 'Didot.ttc|Regular', 'Bodoni 72.ttc|Book', 'Georgia.ttf', 'DejaVuSerif.ttf']
SERIF_I = ['InstrumentSerif-Italic.ttf', 'Didot.ttc|Italic', 'Bodoni 72.ttc|Book Italic', 'Georgia Italic.ttf', 'DejaVuSerif-Italic.ttf']
SANS = ['HelveticaNeue.ttc|Regular', 'Avenir Next.ttc|Regular', 'Arial.ttf', 'DejaVuSans.ttf']
SANS_LIGHT = ['HelveticaNeue.ttc|Light', 'Avenir Next.ttc|Regular', 'Arial.ttf', 'DejaVuSans.ttf']
SANS_BOLD = ['HelveticaNeue.ttc|Bold', 'Avenir Next.ttc|Bold', 'Arial Bold.ttf', 'DejaVuSans-Bold.ttf']
SCRIPT = ['Snell Roundhand.ttc|Regular', 'Zapfino.ttf', 'Brush Script.ttf']
HAND = ['Bradley Hand Bold.ttf', 'Noteworthy.ttc|Bold', 'Chalkboard.ttc|Regular']
STAND_INS = {
    'times.ttf': ['Times New Roman.ttf', 'Times.ttc|Roman'] + SERIF,
    'SitkaVF.ttf': SERIF, 'SitkaVF-Italic.ttf': SERIF_I,
    'BOOKOSI.TTF': ['Palatino.ttc|Italic'] + SERIF_I,
    'BASKVILL.TTF': ['Baskerville.ttc|Regular', 'Big Caslon.ttf'] + SERIF,
    'BELL.TTF': ['Baskerville.ttc|Regular'] + SERIF, 'BELLI.TTF': ['Baskerville.ttc|Italic'] + SERIF_I,
    'BOD_PSTC.TTF': ['Bodoni 72 Smallcaps Book.ttf', 'Bodoni 72.ttc|Book'] + SERIF,
    'GARA.TTF': ['Hoefler Text.ttc|Regular', 'Baskerville.ttc|Regular'] + SERIF,
    'GARAIT.TTF': ['Hoefler Text.ttc|Italic', 'Baskerville.ttc|Italic'] + SERIF_I,
    'GOTHIC.TTF': ['Futura.ttc|Medium', 'Avenir Next.ttc|Regular'] + SANS,
    'GOTHICB.TTF': ['Futura.ttc|Bold', 'Avenir Next.ttc|Bold'] + SANS_BOLD,
    'segoeui.ttf': SANS, 'segoeuil.ttf': SANS_LIGHT, 'segoeuisl.ttf': SANS_LIGHT,
    'segoeuib.ttf': SANS_BOLD, 'seguisb.ttf': ['HelveticaNeue.ttc|Medium', 'Avenir Next.ttc|Demi Bold'] + SANS_BOLD,
    'seguibl.ttf': ['Avenir Next.ttc|Heavy', 'Arial Black.ttf'] + SANS_BOLD,
    'bahnschrift.ttf': ['Avenir Next Condensed.ttc|Regular', 'DIN Condensed Bold.ttf', 'Arial Narrow.ttf'] + SANS,
    'BRLNSB.TTF': ['Futura.ttc|Bold', 'Arial Rounded Bold.ttf'] + SANS_BOLD,
    'BRLNSDB.TTF': ['Futura.ttc|Condensed ExtraBold', 'Arial Rounded Bold.ttf'] + SANS_BOLD,
    'impact.ttf': ['Impact.ttf', 'Arial Black.ttf'] + SANS_BOLD,
    'COOPBL.TTF': ['Cooper Black.ttf', 'Rockwell.ttc|Bold', 'Arial Rounded Bold.ttf'] + SANS_BOLD,
    'VLADIMIR.TTF': SCRIPT, 'KUNSTLER.TTF': SCRIPT, 'BRUSHSCI.TTF': ['Brush Script.ttf'] + SCRIPT,
    'segoesc.ttf': SCRIPT, 'segoescb.ttf': ['Snell Roundhand.ttc|Bold'] + SCRIPT,
    'segoepr.ttf': HAND, 'segoeprb.ttf': HAND, 'BRADHITC.TTF': HAND, 'Inkfree.ttf': HAND,
    'consola.ttf': ['Menlo.ttc|Regular', 'Courier New.ttf', 'DejaVuSansMono.ttf'],
    'consolab.ttf': ['Menlo.ttc|Bold', 'Courier New Bold.ttf', 'DejaVuSansMono-Bold.ttf'],
    'cour.ttf': ['Courier New.ttf', 'Courier.ttc|Regular', 'DejaVuSansMono.ttf'],
    'courbd.ttf': ['Courier New Bold.ttf', 'Courier.ttc|Bold', 'DejaVuSansMono-Bold.ttf'],
    'seguisym.ttf': ['Apple Symbols.ttf', 'Arial Unicode.ttf', 'DejaVuSans.ttf'],
    'seguiemj.ttf': [],      # colour emoji only work through Windows' font here; elsewhere emoji use the text font
}
LAST_RESORT = SERIF + SANS
_found, _fonts = {}, {}


def _locate(file, dirs):
    for d in dirs:
        p = os.path.join(d, file)
        if os.path.exists(p):
            return p
        if os.path.isdir(d) and d.startswith(('/usr', os.path.expanduser('~/.local'))):
            for root, _, files in os.walk(d):              # Linux keeps fonts in sub-folders
                if file in files:
                    return os.path.join(root, file)
    return None


def _face_index(path, style):
    """Index of the face whose style name matches `style` inside a .ttc collection (0 when not found)."""
    want = style.lower()
    best = None
    for i in range(0, 40):
        try:
            fam, st = ImageFont.truetype(path, 10, index=i).getname()
        except Exception:
            break
        st = (st or '').lower()
        if st == want:
            return i
        if best is None and all(w in st for w in want.split()):
            best = i
    return best or 0


def find(name, platform=None):
    """(path, index, is_original) for a Windows font name ('file.ttf' or 'file.ttf#Instance'), or None."""
    base = name.split('#')[0]
    key = (base, platform)
    if key in _found:
        return _found[key]
    dirs = font_dirs(platform)
    out = None
    p = _locate(base, dirs)
    if p:
        out = (p, 0, True)
    else:
        for alt in STAND_INS.get(base, []):
            file, _, style = alt.partition('|')
            p = _locate(file, dirs)
            if p:
                out = (p, _face_index(p, style) if style else 0, False)
                break
    _found[key] = out
    return out


def available(name):
    return find(name) is not None


def path(name):
    """A font file usable by FFmpeg's drawtext (or None)."""
    f = find(name) or next((find(n) for n in ('times.ttf', 'segoeui.ttf') if find(n)), None)
    return f[0] if f else None


def load(name, size):
    """ImageFont for a Windows font name at a pixel size. Never raises."""
    size = max(6, int(size))
    k = (name, size)
    f = _fonts.get(k)
    if f is not None:
        return f
    base, _, inst = name.partition('#')
    hit = find(name)
    try:
        if hit:
            f = ImageFont.truetype(hit[0], size, index=hit[1])
            if inst and hit[2]:                                # named style of a variable font (only on the original)
                try:
                    f.set_variation_by_name(inst)
                except Exception:
                    pass
    except Exception:
        f = None
    if f is None:
        for alt in LAST_RESORT:
            file, _, style = alt.partition('|')
            p = _locate(file, font_dirs())
            if p:
                try:
                    f = ImageFont.truetype(p, size, index=_face_index(p, style) if style else 0)
                    break
                except Exception:
                    pass
    if f is None:
        try:
            f = ImageFont.load_default(size)
        except TypeError:                                      # very old Pillow
            f = ImageFont.load_default()
    if len(_fonts) > 1500:
        _fonts.clear()
    _fonts[k] = f
    return f
