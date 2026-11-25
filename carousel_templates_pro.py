"""The 2026-11 template collection for Carousel Studio.

Styled on what the best travel carousels on Canva and SCRL do (studied 23 Nov 2026), rebuilt as our own designs:
  - one long canvas that flows across slides, thin even gutters, a photo that crosses every seam (SCRL)
  - off-white / paper / one deep colour as the background, never plain black
  - huge title + tiny labels; a bold font with a script word overlapping it
  - small 'app' details: page numbers, an @handle on every slide, pills, sparkles, round badges, postmarks
  - arch and circle photo shapes, offset outline frames, taped and torn paper, light film grain
Fonts are the ones already on this PC (Sitka Banner, Bahnschrift, Cooper Black, Century Gothic, Brush Script, Bradley Hand, Courier).
Drop better fonts into Reel Studio\\fonts\\ and change the names below to upgrade every template at once.
"""
from carousel_templates import P, RC, LN, SHADE, TAPE, K, W, H, arrow
from carousel_templates import T as _T

# ------------------------------------------------------------------ type
SERIF, SERIF_SB, SERIF_B = 'SitkaVF.ttf#Banner', 'SitkaVF.ttf#Banner Semibold', 'SitkaVF.ttf#Banner Bold'
SERIF_I = 'SitkaVF-Italic.ttf#Banner Italic'
BELL_I = 'BELLI.TTF'
COOPER = 'COOPBL.TTF'
COND, COND_SB = 'bahnschrift.ttf#Bold Condensed', 'bahnschrift.ttf#SemiBold Condensed'
BAHN, BAHN_SB = 'bahnschrift.ttf#Regular', 'bahnschrift.ttf#SemiBold'
GEO, GEO_B = 'GOTHIC.TTF', 'GOTHICB.TTF'
BLACK = 'seguibl.ttf'
ROUND = 'BRLNSDB.TTF'
SCRIPT = 'BRUSHSCI.TTF'
HAND = 'BRADHITC.TTF'
TYPE = 'cour.ttf'
SANS, SANS_SB = 'segoeui.ttf', 'seguisb.ttf'
SYM = 'seguisym.ttf'

# ------------------------------------------------------------------ colour
WHITE, INK, MUTED = (255, 255, 255), (34, 31, 28), (128, 120, 110)
OFF, PAPER, CREAM, IVORY = (243, 240, 235), (241, 234, 221), (240, 232, 214), (246, 240, 230)
BLUE, RED, SALMON, TERRA = (38, 70, 160), (214, 72, 56), (236, 150, 124), (184, 96, 62)
TEAL, GOLD = (24, 60, 62), (214, 182, 120)
FOREST, BUTTER = (30, 52, 40), (236, 204, 112)
WINE, YELLOW, LIME = (176, 34, 40), (252, 214, 80), (205, 255, 64)
LAV, PURPLE, HILITE = (226, 218, 242), (72, 48, 120), (250, 236, 120)
PEACH, SAND = (234, 180, 150), (236, 226, 212)

HANDLE = ('g_handle', 'Your @handle', '@yourname')


def T(*a, **kw):
    kw.setdefault('new', True)
    return _T(*a, **kw)


def tx(field, x, y, fnt, size, col=INK, **kw):
    """Words from a field you can edit (no shadow unless asked)."""
    kw.setdefault('shadow', 0)
    return dict(t='text', field=field, xy=(x, y), font=fnt, size=size, color=col, **kw)


def st(text, x, y, fnt, size, col=INK, **kw):
    """Fixed words ({no} = slide number, {of} = number of slides)."""
    kw.setdefault('shadow', 0)
    return dict(t='text', text=text, xy=(x, y), font=fnt, size=size, color=col, **kw)


def PILL(x, y, fnt, size, text=None, field=None, **kw):
    d = dict(t='pill', xy=(x, y), font=fnt, size=size, **kw)
    d.update({'text': text} if field is None else {'field': field})
    return d


def SPARK(x, y, r=34, col=WHITE, **kw):
    return dict(t='spark', xy=(x, y), r=r, color=col, **kw)


def BADGE(x, y, r, text, fnt, size, col=INK, **kw):
    return dict(t='badge', xy=(x, y), r=r, text=text, font=fnt, size=size, color=col, **kw)


def WAVES(x, y, w, h, col=BLUE, **kw):
    return dict(t='waves', rect=(x, y, w, h), color=col, **kw)


def ELL(x, y, w, h, **kw):
    return dict(t='ellipse', rect=(x, y, w, h), **kw)


def TORN(x, y, w, h, rot=0, col=(250, 246, 236), **kw):
    return dict(t='torn', rect=(x, y, w, h), rot=rot, color=col, **kw)


def STAMP(x, y, r, text, col=RED, rot=-12, **kw):
    return dict(t='stamp', xy=(x, y), r=r, text=text, color=col, rot=rot, **kw)


def FRAME(slot, x, y, w, h, b=16, rot=0, sh=110, **kw):
    """A photo with a white border and a soft shadow."""
    return P(slot, x, y, w, h, border=b, rot=rot, shadow=sh, sblur=kw.pop('sblur', 16), **kw)


TEMPLATES = []
add = TEMPLATES.append
G_SEAM, G_BOLD, G_EDIT, G_SCRAP, G_GUIDE, G_GRID = ('New · Seamless', 'New · Bold type', 'New · Editorial',
                                                    'New · Scrapbook', 'New · Guides & fun', 'New · Grids')

# ================================================================== New · Seamless (one long canvas)
# Every slide hands a photo over the seam: it ends 300 px into the next slide, so each kind keeps x < 300 free.
g, top, bot = 18, 48, 1302
add(T('gallery_wall', 'Gallery wall (seamless)', G_SEAM,
      'Clean off-white canvas, thin even gutters and a tall photo crossing every seam. Small typewriter lines in the gaps.',
      'SCRL / Canva minimal seamless collage', ('milky', 0.55),
      {'open': K('Cover', ['Top left', 'Bottom left', 'Tall photo (runs into slide 2)'],
                 [('words', 'Lines (one per row)', "life doesn't\nwait\nfor you\nto be ready."), ('badge', 'Round badge', 'EUROPE · SUMMER 2026 · '), HANDLE],
                 [P(0, 48, top, 470, 560, z=1), tx('words', 518, 642, TYPE, 32, anchor='rt', lh=1.38), P(1, 48, 902, 470, 400, z=1),
                  P(2, 536, top, 844, 1254, z=1), dict(t='badge', xy=(860, 250), r=96, field='badge', font=GEO_B, size=17, color=WHITE, ring=False,
                                                       center='✦', cfont=SYM, csize=44, z=2)]),
       'grid': K('Two + tall', ['Top', 'Bottom', 'Tall photo (runs into the next slide)'], [],
                 [P(0, 318, top, 380, 610, z=1), P(1, 318, top + 610 + g, 380, 626, z=1), P(2, 716, top, 664, 1254, z=1)]),
       'note': K('Words + photo', ['Small photo', 'Tall photo (runs into the next slide)'], [('words', 'Lines', 'it’s time\nto find\nthe magic')],
                 [tx('words', 508, 300, TYPE, 34, anchor='mt', lh=1.4), P(0, 318, 700, 380, 602, z=1), P(1, 716, top, 664, 1254, z=1)]),
       'wide': K('Wide on top', ['Wide photo (runs into the next slide)', 'Small photo', 'Photo (runs into the next slide)'], [],
                 [P(0, 318, top, 1062, 600, z=1), P(1, 318, top + 600 + g, 380, 636, z=1), P(2, 716, top + 600 + g, 664, 636, z=1)]),
       'end': K('Closing', ['Photo'], [('words', 'Closing lines', 'see you\nsomewhere\nnew.')],
                [P(0, 318, top, 714, 860, z=1), tx('words', 675, 990, TYPE, 36, anchor='mt', lh=1.4), tx('g_handle', 675, 1268, GEO, 22, MUTED, anchor='mb', track=3)])},
      ['open', 'grid', ('note', {'words': 'mornings\nstart slow\nhere'}), 'wide', 'grid', 'end'], strip=True, bg=OFF))

add(T('pano_frames', 'Panorama + framed photos (seamless)', G_SEAM,
      'One wide photo runs under every slide; white-framed photos sit on top and cross the seams.', 'SCRL panorama template', ('mediterranean', 0.6),
      {'cover': K('Cover', ['Panorama (runs under every slide)', 'Framed photo (crosses into slide 2)'],
                  [('label', 'Small label', 'Amalfi · 2026'), ('title', 'Title', 'the coast,\nslowly.'), HANDLE],
                  [SHADE(0, 640, 150, 0), tx('label', 84, 104, GEO_B, 24, WHITE, anchor='lt', track=7, case='upper', shadow=90),
                   tx('title', 78, 150, SERIF, 132, WHITE, anchor='lt', lh=0.98, shadow=120, sblur=10),
                   FRAME(1, 660, 560, 560, 700, rot=-3, z=2), st('swipe  →', 84, 1272, GEO, 24, WHITE, anchor='lb', track=4, shadow=120)]),
       'frame': K('Framed photo', ['Framed photo (crosses the edge)'], [('caption', 'Handwritten caption', 'lemons the size of your fist')],
                  [FRAME(0, 700, 300, 560, 720, rot=3, z=2), TORN(250, 1110, 520, 160, rot=-2, z=1),
                   tx('caption', 282, 1140, HAND, 40, INK, anchor='lt', rot=-2, wrap=440, lh=1.1, z=1)]),
       'frame_low': K('Framed photo (low)', ['Framed photo (crosses the edge)'], [('caption', 'Handwritten caption', 'we swam before breakfast')],
                      [FRAME(0, 560, 640, 660, 500, rot=-2, z=2), TORN(260, 160, 540, 160, rot=2, z=1),
                       tx('caption', 292, 190, HAND, 40, INK, anchor='lt', rot=2, wrap=460, lh=1.1, z=1)]),
       'end': K('Closing', [], [('words', 'Closing line', 'same sea,\ndifferent light.')],
                [SHADE(380, 600, 0, 120), SHADE(980, 370, 120, 0), tx('words', 540, 560, SERIF_I, 86, WHITE, anchor='mt', lh=1.05, shadow=140, sblur=10),
                 tx('g_handle', 540, 1260, GEO, 24, WHITE, anchor='mb', track=3, shadow=120)])},
      ['cover', 'frame', 'frame_low', ('frame', {'caption': 'the bus driver sang the whole way'}), 'end'],
      strip=True, bg=OFF, strip_els=[P(0, 0, 0, -1, H, z=0)]))

add(T('postcard_bold', 'Postcard · bold letters (seamless)', G_SEAM,
      'Cream paper, a two-colour country title, an offset frame, postmark waves and stamps that cross the seams.', 'Canva “France 2026” postcard carousel', ('riviera', 0.6),
      {'cover': K('Cover', ['Big photo', 'Small photo (crosses into slide 2)'],
                  [('title', 'Country', 'ITALIA'), ('year', 'Year', '2026'), ('line', 'Small line', 'postcards from the south  →'), HANDLE],
                  [ELL(-170, -170, 470, 470, fill=BLUE), RC(96, 150, 600, 680, None, outline=SALMON, width=10),
                   P(0, 130, 186, 600, 680, z=1), WAVES(760, 110, 400, 86, BLUE, n=5, width=6, z=2),
                   P(1, 820, 600, 400, 470, border=14, rot=5, shadow=100, z=2),
                   tx('year', 70, 896, COND, 120, RED, anchor='lt', track=6),
                   tx('title', 64, 1010, COND, 236, BLUE, anchor='lt', track=4, case='upper'),
                   tx('line', 70, 1296, GEO_B, 24, INK, anchor='lb', track=5, case='upper'),
                   STAMP(940, 1180, 84, 'POSTE · EUROPA · 2026', RED, rot=-14, z=2)]),
       'card': K('Postcard', ['Postcard photo', 'Small photo (crosses the edge)'], [('caption', 'Handwritten note', 'the lemons were\nthe size of fists')],
                 [FRAME(0, 250, 120, 740, 560, b=18, rot=-2, sh=90), tx('caption', 270, 790, HAND, 56, INK, anchor='lt', rot=-2, lh=1.15),
                  WAVES(60, 1160, 380, 80, BLUE, n=5, width=6), P(1, 820, 600, 400, 470, border=14, rot=5, shadow=100, z=2)]),
       'pair': K('Two photos', ['Photo A', 'Photo B'], [('caption', 'Handwritten note', 'two days, one swimsuit')],
                 [FRAME(0, 240, 120, 580, 500, rot=-3, sh=90), FRAME(1, 400, 610, 540, 560, rot=3), tx('caption', 250, 1250, HAND, 50, INK, anchor='lb', rot=-3),
                  STAMP(1080, 300, 96, 'VIA AEREA · PAR AVION', BLUE, rot=-8, z=2)]),
       'end': K('Closing', ['Photo'], [('words', 'Closing words', 'wish you\nwere here')],
                [tx('words', 560, 150, SCRIPT, 150, BLUE, anchor='mt', lh=0.95, rot=-4), FRAME(0, 330, 560, 480, 560, b=16, rot=3, sh=90),
                 WAVES(640, 1170, 360, 80, RED, n=4, width=5), tx('g_handle', 300, 1270, GEO_B, 24, INK, anchor='mb', track=4)])},
      ['cover', 'card', 'pair', ('card', {'caption': 'nobody here is\nin a hurry'}), 'end'], strip=True, bg=('paper', (245, 238, 226)), grain=4))

add(T('slant_resort', 'Slanted strips · resort (seamless)', G_SEAM,
      'Deep teal, tall rounded photo strips leaning across the seams, a quiet serif title and gold labels.', 'Canva luxury resort carousel', ('emerald', 0.55),
      {'cover': K('Cover', ['Strip 1', 'Strip 2', 'Strip 3 (crosses into slide 2)'],
                  [('kicker', 'Small label', 'The lakes · Italy'), ('title', 'Title', 'Places worth\nslowing down for'), HANDLE],
                  [tx('kicker', 80, 104, GEO_B, 22, GOLD, anchor='lt', track=8, case='upper'), tx('title', 76, 150, SERIF, 92, CREAM, anchor='lt', lh=1.04),
                   st('swipe to explore  ›', 1004, 108, SERIF_I, 30, CREAM, anchor='rt'),
                   P(0, 110, 470, 290, 760, radius=34, rot=-8, shadow=120, z=1), P(1, 450, 540, 290, 760, radius=34, rot=-8, shadow=120, z=1),
                   P(2, 800, 610, 290, 760, radius=34, rot=-8, shadow=120, z=1)]),
       'strips': K('Three strips', ['Strip 1', 'Strip 2', 'Strip 3 (crosses the edge)'], [('caption', 'Caption', 'mornings on the water')],
                  [P(0, 200, 120, 290, 900, radius=34, rot=-8, shadow=120, z=1), P(1, 540, 200, 290, 900, radius=34, rot=-8, shadow=120, z=1),
                   P(2, 880, 280, 290, 900, radius=34, rot=-8, shadow=120, z=1), tx('caption', 90, 1276, SERIF_I, 40, CREAM, anchor='lb')]),
       'quote': K('Quote', ['Photo'], [('quote', 'Quote', '“The lake was so still\nyou could hear\nthe bells across it.”')],
                 [tx('quote', 330, 520, SERIF_I, 52, CREAM, anchor='mt', lh=1.2), LN([(250, 470), (410, 470)], color=GOLD, width=2),
                  P(0, 640, 190, 330, 980, radius=34, rot=-8, shadow=120, z=1)]),
       'end': K('Closing', [], [('title', 'Closing title', 'Take the\nslow boat.'), ('sub', 'Small line', 'Save this for your next trip')],
                [tx('title', 540, 470, SERIF, 110, CREAM, anchor='mt', lh=1.02), LN([(460, 760), (620, 760)], color=GOLD, width=2),
                 tx('sub', 540, 800, GEO_B, 22, GOLD, anchor='mt', track=6, case='upper'), tx('g_handle', 540, 1270, GEO, 24, CREAM, anchor='mb', track=3)])},
      ['cover', 'strips', 'quote', ('strips', {'caption': 'lunch took three hours'}), 'end'], strip=True, bg=TEAL, grain=4))

add(T('journal_scrap', 'Travel journal scrapbook (seamless)', G_SCRAP,
      'Dotted paper, taped photos that cross the seams, torn notes, a doodled arrow and a bold + script title.', 'Canva “My travel journal” carousel', ('warmfilm', 0.6),
      {'cover': K('Cover', ['Main photo', 'Photo 2', 'Photo 3 (crosses into slide 2)'],
                  [('t1', 'Title', 'MY TRAVEL'), ('t2', 'Script word', 'journal'), ('note', 'Note', 'europe, summer 2026'), HANDLE],
                  [tx('t1', 72, 96, COND, 200, INK, anchor='lt', case='upper', track=2), tx('t2', 640, 250, SCRIPT, 160, TERRA, anchor='mt', rot=-6),
                   FRAME(0, 96, 500, 500, 620, b=14, rot=-4, sh=90, z=1), TAPE(270, 486, rot=-8, z=2),
                   FRAME(1, 590, 560, 390, 470, b=14, rot=5, sh=90, z=1), TAPE(720, 545, rot=7, z=2),
                   FRAME(2, 880, 1000, 440, 300, b=14, rot=-3, sh=90, z=2), TAPE(1060, 980, rot=-4, z=2),
                   TORN(96, 1170, 520, 112, rot=-2, z=2), tx('note', 130, 1196, HAND, 44, INK, anchor='lt', rot=-2, z=2),
                   SPARK(560, 470, 30, TERRA, z=2)]),
       'page': K('Page', ['Photo 1', 'Photo 2', 'Photo 3 (crosses the edge)'], [('note', 'Note', 'got lost on purpose'), ('tag', 'Tag', 'DAY 03')],
                 [FRAME(0, 150, 110, 500, 640, b=14, rot=-3, sh=90, z=1), TAPE(330, 92, rot=-6, z=2),
                  FRAME(1, 610, 250, 380, 480, b=14, rot=4, sh=90, z=1), TAPE(730, 236, rot=5, z=2),
                  TORN(190, 830, 470, 120, rot=2, z=2), tx('note', 220, 860, HAND, 44, INK, anchor='lt', rot=2, z=2),
                  *[dict(e, z=2) for e in arrow(680, 900, 790, 760, INK, 4)],
                  PILL(700, 150, GEO_B, 24, field='tag', fill=TERRA, color=WHITE, track=4, anchor='lt', rot=3, z=2),
                  FRAME(2, 880, 1000, 440, 300, b=14, rot=-3, sh=90, z=2), TAPE(1060, 980, rot=-4, z=2)]),
       'single': K('One big photo', ['Photo', 'Photo (crosses the edge)'], [('note', 'Note', 'this view, every evening')],
                   [FRAME(0, 190, 110, 720, 840, b=16, rot=2, sh=90, z=1), TAPE(220, 110, 150, 44, rot=-40, z=2), TAPE(800, 110, 150, 44, rot=40, z=2),
                    TORN(200, 1030, 520, 112, rot=-2, z=2), tx('note', 230, 1056, HAND, 44, INK, anchor='lt', rot=-2, z=2),
                    FRAME(1, 880, 1000, 440, 300, b=14, rot=-3, sh=90, z=2), TAPE(1060, 980, rot=-4, z=2)]),
       'end': K('Closing', ['Photo'], [('words', 'Closing words', 'to be\ncontinued…')],
                [TORN(240, 220, 620, 360, rot=-2, z=1), tx('words', 550, 270, HAND, 92, INK, anchor='mt', lh=1.05, rot=-2, z=1),
                 FRAME(0, 330, 640, 420, 500, b=14, rot=4, sh=90, z=1), TAPE(470, 624, rot=-5, z=2),
                 STAMP(870, 1140, 90, 'EUROPA · 2026', TERRA, rot=12, z=2), tx('g_handle', 300, 1270, HAND, 40, INK, anchor='mb', z=2)])},
      ['cover', 'page', 'single', ('page', {'note': 'the best meal of the trip', 'tag': 'DAY 05'}), 'end'],
      strip=True, bg=('paper', (238, 228, 210)), grain=4,
      strip_els=[dict(t='ruled', rect=(0, 0, -1, H), kind='dots', step=48, color=(120, 100, 80), alpha=70)]))

# ================================================================== New · Bold type
add(T('dump_bold', 'Photo dump · bold + script', G_BOLD,
      'Huge white lowercase title with a yellow script word over it, sparkles, and overlapping white frames inside.', 'Canva “travel photo dump” / “June photo dump”', ('summer', 0.6),
      {'cover': K('Cover', ['Cover photo', 'Small framed photo'], [('t1', 'Title', 'travel\nphoto\ndump'), ('t2', 'Script word', "summer '26"), HANDLE],
                  [P(0, 0, 0, W, H), SHADE(0, 760, 150, 0), tx('t1', 64, 70, BLACK, 200, WHITE, anchor='lt', lh=0.84, shadow=70, sblur=12),
                   tx('t2', 500, 470, SCRIPT, 124, YELLOW, anchor='lt', rot=7, shadow=110, sblur=8),
                   SPARK(930, 150, 46), SPARK(1000, 236, 22), SPARK(110, 700, 28),
                   P(1, 650, 820, 330, 380, border=14, pb=56, rot=6, shadow=140, sblur=18),
                   tx('g_handle', 64, 1286, GEO_B, 24, WHITE, anchor='lb', track=3, shadow=130)]),
       'two': K('Two frames', ['Background (blurred)', 'Photo A', 'Photo B'], [('caption', 'Script caption', 'golden hour')],
                [FRAME(1, 80, 100, 560, 700, b=14, rot=-4, sh=150), FRAME(2, 450, 500, 540, 620, b=14, rot=4, sh=170),
                 SPARK(900, 210, 40), SPARK(960, 300, 20), tx('caption', 80, 1300, SCRIPT, 96, WHITE, anchor='lb', rot=-4, shadow=150)], bg=('blur', 0, 0.2)),
       'full': K('Full photo', ['Photo'], [('caption', 'Label', 'Lisbon, Portugal')],
                 [P(0, 0, 0, W, H), PILL(64, 1286, BAHN_SB, 30, field='caption', fill=WHITE, color=INK, anchor='lb', shadow=60), SPARK(990, 100, 30)]),
       'trio': K('Three frames', ['Background (blurred)', 'Photo A', 'Photo B', 'Photo C'], [],
                 [FRAME(1, 70, 90, 470, 600, b=12, rot=-5, sh=150), FRAME(2, 540, 210, 470, 600, b=12, rot=4, sh=150),
                  FRAME(3, 260, 650, 560, 620, b=12, rot=-2, sh=170), SPARK(150, 1180, 36), SPARK(960, 1000, 26)], bg=('blur', 0, 0.2)),
       'end': K('Closing', ['Photo'], [('t1', 'Big words', "that's a\nwrap"), ('t2', 'Script word', 'for now')],
                [P(0, 0, 0, W, H, dim=0.25), tx('t1', 540, 420, BLACK, 170, WHITE, anchor='mt', lh=0.86, shadow=80),
                 tx('t2', 640, 700, SCRIPT, 160, YELLOW, anchor='mt', rot=-6, shadow=110), SPARK(260, 360, 40), SPARK(850, 340, 24),
                 tx('g_handle', 540, 1270, GEO_B, 24, WHITE, anchor='mb', track=3, shadow=120)])},
      ['cover', 'two', 'full', 'trio', ('full', {'caption': 'Sintra'}), 'end'], grain=3))

add(T('one_day_in', 'One day in…', G_BOLD,
      'Blurred photo background, “one day in” in white with the place in a big yellow script, a framed photo and times of day.', 'Canva “one day in my life” carousel', ('golden', 0.6),
      {'cover': K('Cover', ['Background (blurred)', 'Framed photo'], [('t1', 'Top words', 'one day in'), ('t2', 'Place (script)', 'Lisbon'),
                                                                     ('blurb', 'Small text', 'one day, no plan — just trams, tiles and too many pastéis'), HANDLE],
                  [tx('t1', 540, 96, ROUND, 116, WHITE, anchor='mt', shadow=90), tx('t2', 560, 196, SCRIPT, 210, YELLOW, anchor='mt', rot=-5, shadow=110, sblur=8),
                   FRAME(1, 190, 500, 700, 600, b=14, sh=150), RC(190, 1150, 728, 140, (18, 14, 10, 150), radius=10),
                   tx('blurb', 554, 1220, GEO_B, 23, WHITE, anchor='mm', wrap=640, lh=1.45, track=2, case='upper', valign='middle')], bg=('blur', 0, 0.35)),
       'moment': K('Moment', ['Background (blurred)', 'Framed photo'], [('time', 'Time', '08:30'), ('what', 'What happened (script)', 'first coffee')],
                   [tx('time', 540, 90, COND, 124, WHITE, anchor='mt', shadow=90, track=4), tx('what', 560, 214, SCRIPT, 112, YELLOW, anchor='mt', rot=-4, shadow=110),
                    FRAME(1, 150, 420, 780, 860, b=14, sh=150)], bg=('blur', 0, 0.35)),
       'end': K('Closing', ['Background (blurred)', 'Framed photo'], [('t1', 'Top words', 'see you'), ('t2', 'Script', 'tomorrow')],
                [FRAME(1, 240, 140, 600, 700, b=14, rot=-3, sh=150), tx('t1', 540, 930, ROUND, 116, WHITE, anchor='mt', shadow=90),
                 tx('t2', 560, 1030, SCRIPT, 170, YELLOW, anchor='mt', rot=-5, shadow=110), tx('g_handle', 540, 1300, GEO_B, 22, WHITE, anchor='mb', track=3, shadow=110)],
                bg=('blur', 0, 0.35))},
      ['cover', 'moment', ('moment', {'time': '11:00', 'what': 'tram 28'}), ('moment', {'time': '14:00', 'what': 'lunch by the river'}),
       ('moment', {'time': '19:40', 'what': 'sunset, miradouro'}), 'end'], grain=3))

add(T('wrap_red', "That's a wrap · ivory & red", G_BOLD,
      'Ivory paper, a heavy red retro title, taped polaroids with handwritten captions — a trip recap.', 'Canva “And that’s a wrap!” photo dump', ('vintage', 0.55),
      {'cover': K('Cover', ['Polaroid photo'], [('title', 'Title', "And\nthat's a\nwrap!"),
                                                ('body', 'Small text', "Here's to the trains we nearly missed, the views we didn't plan and everyone we met along the way."), HANDLE],
                  [P(0, 610, 70, 360, 380, border=18, pb=72, rot=8, shadow=80), TAPE(720, 60, rot=-6),
                   tx('title', 64, 400, COOPER, 172, WINE, anchor='lt', lh=0.94), tx('body', 70, 1090, GEO, 27, INK, anchor='lt', wrap=600, lh=1.5),
                   st('>>', 1010, 1280, COOPER, 64, WINE, anchor='rb'), tx('g_handle', 70, 1280, GEO_B, 22, MUTED, anchor='lb', track=3)]),
       'polaroid': K('Polaroid', ['Photo'], [('caption', 'Handwritten caption', 'the night train to Vienna')],
                     [P(0, 170, 130, 740, 800, border=26, pb=150, rot=-3, shadow=80), TAPE(450, 108, 190, 52, rot=4),
                      tx('caption', 540, 1060, HAND, 58, INK, anchor='mt', rot=-3), st('{no}', 1010, 1280, COOPER, 64, WINE, anchor='rb')]),
       'two': K('Two polaroids', ['Photo A', 'Photo B'], [('c1', 'Caption A', 'gelato #1'), ('c2', 'Caption B', 'gelato #6')],
                [P(0, 70, 140, 460, 520, border=20, pb=110, rot=-5, shadow=80), P(1, 550, 560, 460, 520, border=20, pb=110, rot=4, shadow=80),
                 TAPE(220, 120, rot=-8), TAPE(700, 540, rot=6), tx('c1', 300, 795, HAND, 48, INK, anchor='mt', rot=-5), tx('c2', 780, 1215, HAND, 48, INK, anchor='mt', rot=4),
                 st('{no}', 1010, 1280, COOPER, 64, WINE, anchor='rb')]),
       'list': K('Best bits', ['Photo'], [('head', 'Heading', 'Best\nbits'),
                                          ('items', 'List (one per line)', '01  the night train\n02  a swim at 7am\n03  pasta, twice a day\n04  getting lost in Porto\n05  that sunset')],
                 [tx('head', 64, 100, COOPER, 130, WINE, anchor='lt', lh=0.92), tx('items', 70, 470, GEO, 38, INK, anchor='lt', lh=1.75),
                  P(0, 660, 860, 330, 330, border=16, pb=60, rot=6, shadow=80), TAPE(760, 846, rot=-8)]),
       'end': K('Closing', [], [('title', 'Closing words', 'Until\nnext\ntime.')],
                [tx('title', 64, 300, COOPER, 210, WINE, anchor='lt', lh=0.92), tx('g_handle', 70, 1280, GEO_B, 24, INK, anchor='lb', track=3),
                 st('♥', 1000, 1280, SYM, 54, WINE, anchor='rb')])},
      ['cover', 'polaroid', ('polaroid', {'caption': 'Hallstatt, before the crowds'}), 'two', 'list', 'end'], bg=('paper', IVORY), grain=4))

add(T('neon_collage', 'Neon collage', G_BOLD,
      'Tilted photos filling the slide with a chunky lime title repeated twice and a sparkle between.', 'Canva neon “photo dump” collage', ('vivid', 0.5),
      {'cover': K('Cover', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4', 'Photo 5'], [('t1', 'Line 1', 'EUROPE'), ('t2', 'Line 2', 'PHOTO DUMP'), ('sub', 'Small line', 'swipe for the summer  →')],
                  [P(0, -50, -40, 600, 700, border=10, rot=6, shadow=120), P(1, 520, -70, 640, 660, border=10, rot=-5, shadow=120),
                   P(2, -70, 650, 620, 760, border=10, rot=-4, shadow=120), P(3, 500, 610, 660, 800, border=10, rot=5, shadow=120),
                   P(4, 330, 420, 440, 520, border=12, rot=-3, shadow=170),
                   tx('t1', 540, 230, COND, 168, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3), tx('t2', 540, 390, COND, 168, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3),
                   SPARK(540, 680, 56, LIME), tx('t1', 540, 790, COND, 168, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3),
                   tx('t2', 540, 950, COND, 168, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3),
                   tx('sub', 540, 1280, GEO_B, 24, WHITE, anchor='mb', track=4, case='upper', shadow=200)]),
       'collage': K('Collage', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4'], [('tag', 'Label', 'week two: the coast')],
                    [P(0, 40, 60, 540, 660, border=10, rot=-4, shadow=130), P(1, 520, 120, 520, 600, border=10, rot=5, shadow=130),
                     P(2, 60, 680, 520, 600, border=10, rot=3, shadow=130), P(3, 500, 700, 540, 560, border=10, rot=-5, shadow=140),
                     PILL(540, 660, COND, 52, field='tag', fill=LIME, color=INK, track=2, rot=-3, shadow=120, pad=(34, 10)), SPARK(980, 80, 36, LIME)]),
       'end': K('Closing', ['Photo 1', 'Photo 2', 'Photo 3'], [('t1', 'Line 1', 'SEE YOU'), ('t2', 'Line 2', 'NEXT SUMMER')],
                [P(0, -40, 120, 560, 700, border=10, rot=5, shadow=120), P(1, 540, 80, 560, 700, border=10, rot=-6, shadow=120),
                 P(2, 200, 720, 680, 640, border=10, rot=3, shadow=140), tx('t1', 540, 470, COND, 180, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3),
                 tx('t2', 540, 640, COND, 150, LIME, anchor='mt', shadow=220, sblur=10, case='upper', track=3), SPARK(540, 860, 48, LIME)])},
      ['cover', 'collage', ('collage', {'tag': 'week three: the alps'}), 'collage', 'end'], bg=(20, 20, 22)))

add(T('moments_chrome', 'Small moments · header & footer', G_BOLD,
      'Full photos framed by a thin brand header and an @handle + slide-number footer; a yellow title with a script line.', 'Canva “Small travel moments” carousel', ('cinematic', 0.6),
      {'cover': K('Cover', ['Photo'], [('t1', 'Title', "Small travel\nmoments I'll"), ('t2', 'Script line', 'always remember'),
                                        ('g_brand', 'Brand line', 'Europe diaries'), HANDLE],
                  [P(0, 0, 0, W, H), SHADE(0, 260, 140, 0), SHADE(640, 710, 0, 200),
                   tx('g_brand', 60, 58, GEO_B, 22, WHITE, anchor='lt', track=6, case='upper', shadow=90), st('2026', 1020, 58, GEO_B, 22, WHITE, anchor='rt', track=6, shadow=90),
                   LN([(60, 100), (1020, 100)], color=WHITE, width=2, alpha=190),
                   tx('t1', 60, 790, BLACK, 104, YELLOW, anchor='lt', lh=0.98, shadow=90), tx('t2', 70, 1010, SCRIPT, 120, WHITE, anchor='lt', rot=-3, shadow=110),
                   SPARK(930, 760, 38, YELLOW), SPARK(985, 830, 18, YELLOW),
                   LN([(60, 1244), (1020, 1244)], color=WHITE, width=2, alpha=190), tx('g_handle', 60, 1290, GEO, 22, WHITE, anchor='lb', track=3, shadow=90),
                   st('SLIDE {no}', 1020, 1290, GEO_B, 22, WHITE, anchor='rb', track=5, shadow=90)]),
       'moment': K('Moment', ['Photo'], [('caption', 'Caption', 'the 6am ferry'), ('script', 'Script word', 'quiet')],
                   [P(0, 0, 0, W, H), SHADE(0, 220, 130, 0), SHADE(800, 550, 0, 190),
                    tx('g_brand', 60, 58, GEO_B, 22, WHITE, anchor='lt', track=6, case='upper', shadow=90), st('2026', 1020, 58, GEO_B, 22, WHITE, anchor='rt', track=6, shadow=90),
                    LN([(60, 100), (1020, 100)], color=WHITE, width=2, alpha=190),
                    tx('script', 70, 1040, SCRIPT, 96, YELLOW, anchor='lb', rot=-3, shadow=110), tx('caption', 60, 1180, BLACK, 64, WHITE, anchor='lb', shadow=90),
                    LN([(60, 1244), (1020, 1244)], color=WHITE, width=2, alpha=190), tx('g_handle', 60, 1290, GEO, 22, WHITE, anchor='lb', track=3, shadow=90),
                    st('SLIDE {no}', 1020, 1290, GEO_B, 22, WHITE, anchor='rb', track=5, shadow=90)])},
      ['cover', 'moment', ('moment', {'caption': 'bread, still warm', 'script': 'simple'}), ('moment', {'caption': 'rain in Bruges', 'script': 'slow'}),
       ('moment', {'caption': 'the last train home', 'script': 'tired'}), ('moment', {'caption': 'and this view', 'script': 'always'})], grain=3))

# ================================================================== New · Editorial
add(T('typewriter_notes', 'Typewriter notes', G_EDIT,
      'Warm off-white, underlined typewriter lines, “(01)” page marks and big clean photos.', 'Canva “the little moments I was grateful for”', ('softlight', 0.55),
      {'cover': K('Cover', ['Photo'], [('words', 'Lines', 'the little moments\ni was grateful for\non this trip:'), HANDLE],
                  [st('({no})', 60, 60, TYPE, 26, INK, anchor='lt'), tx('g_handle', 1020, 60, TYPE, 26, INK, anchor='rt'),
                   tx('words', 60, 200, TYPE, 56, INK, anchor='lt', lh=1.45, ul=(INK, 2)), P(0, 0, 600, W, 750)]),
       'note': K('Photo + note', ['Photo'], [('words', 'Note', '01. the 6am bakery queue')],
                 [st('({no})', 60, 60, TYPE, 26, INK, anchor='lt'), tx('g_handle', 1020, 60, TYPE, 26, INK, anchor='rt'),
                  P(0, 60, 130, 960, 940), tx('words', 60, 1136, TYPE, 42, INK, anchor='lt', lh=1.5, ul=(INK, 2), wrap=940)]),
       'twin': K('Two photos + note', ['Left', 'Right'], [('words', 'Note', '04. two coffees, one view')],
                 [st('({no})', 60, 60, TYPE, 26, INK, anchor='lt'), tx('g_handle', 1020, 60, TYPE, 26, INK, anchor='rt'),
                  P(0, 60, 130, 470, 800), P(1, 550, 130, 470, 800), tx('words', 60, 1000, TYPE, 42, INK, anchor='lt', lh=1.5, ul=(INK, 2), wrap=940)]),
       'end': K('Closing', ['Photo'], [('words', 'Closing lines', '& a hundred\nmore like these.')],
                [st('({no})', 60, 60, TYPE, 26, INK, anchor='lt'), tx('g_handle', 1020, 60, TYPE, 26, INK, anchor='rt'),
                 tx('words', 540, 260, TYPE, 54, INK, anchor='mt', lh=1.5, ul=(INK, 2)), P(0, 290, 620, 500, 620)])},
      ['cover', 'note', ('note', {'words': '02. a swim before breakfast'}), ('note', {'words': '03. getting lost (on purpose)'}), 'twin', 'end'],
      bg=('paper', (244, 240, 232)), grain=3))

add(T('arch_windows', 'Arch windows', G_EDIT,
      'Sand paper, photos shaped like arched windows and circles, an italic serif title and small spaced capitals.', 'Canva arch-frame travel templates', ('terracotta', 0.55),
      {'cover': K('Cover', ['Arch photo'], [('kicker', 'Small label', 'Amalfi coast · 2026'), ('title', 'Title', 'a slow week\nin the south')],
                  [tx('kicker', 540, 92, GEO_B, 22, TERRA, anchor='mt', track=8, case='upper'), tx('title', 540, 140, SERIF_I, 84, INK, anchor='mt', lh=1.04),
                   P(0, 210, 400, 660, 860, shape='arch'), st('—   swipe   —', 540, 1316, GEO, 20, MUTED, anchor='mb', track=6)]),
       'two': K('Two arches', ['Left arch', 'Right arch'], [('caption', 'Caption', 'lemons, salt and very long lunches')],
                [P(0, 80, 140, 440, 760, shape='arch'), P(1, 560, 360, 440, 760, shape='arch'),
                 tx('caption', 80, 960, SERIF_I, 46, INK, anchor='lt', wrap=430, lh=1.15), st('N° {no}', 1000, 1250, GEO_B, 20, TERRA, anchor='rb', track=6)]),
       'side': K('Arch + words', ['Arch photo'], [('label', 'Small label', 'Positano'), ('words', 'Words', 'the steps are steep, the view is worth it')],
                 [P(0, 70, 130, 520, 1090, shape='arch'), tx('label', 650, 520, GEO_B, 22, TERRA, anchor='lt', track=7, case='upper'),
                  tx('words', 650, 570, SERIF_I, 56, INK, anchor='lt', wrap=360, lh=1.12), LN([(650, 490), (740, 490)], color=TERRA, width=2),
                  st('N° {no}', 1000, 1250, GEO_B, 20, TERRA, anchor='rb', track=6)]),
       'circle': K('Circle', ['Circle photo'], [('caption', 'Caption', 'Ravello, at 7pm')],
                   [P(0, 170, 220, 740, 740, shape='circle'), tx('caption', 540, 1040, SERIF_I, 58, INK, anchor='mt'),
                    st('N° {no}', 540, 1250, GEO_B, 20, TERRA, anchor='mb', track=6)]),
       'end': K('Closing', ['Small arch'], [('title', 'Closing line', 'until we\nmeet again'), HANDLE],
                [tx('title', 540, 200, SERIF_I, 96, INK, anchor='mt', lh=1.04), P(0, 370, 560, 340, 520, shape='arch'),
                 tx('g_handle', 540, 1230, GEO_B, 22, TERRA, anchor='mb', track=6)])},
      ['cover', 'two', 'side', 'circle', ('two', {'caption': 'every door a different blue'}), 'end'], bg=('paper', SAND), grain=3))

add(T('vertical_title', 'Vertical title · portfolio', G_EDIT,
      'A tall serif word running up the left edge, a big photo, a script line crossing it and tiny captions.', 'Canva minimal editorial portfolio', ('faded', 0.55),
      {'cover': K('Cover', ['Photo'], [('title', 'Vertical word', 'EUROPE'), ('script', 'Script line', 'summer notes'), ('foot', 'Small line', 'Vol. 01 — 2026'), HANDLE],
                  [P(0, 250, 110, 770, 1030), tx('title', 128, 625, SERIF, 210, INK, anchor='mm', rot=90, track=14, case='upper'),
                   tx('script', 700, 1050, SCRIPT, 116, TERRA, anchor='mt', rot=-4, shadow=60),
                   tx('foot', 1020, 1290, GEO_B, 20, INK, anchor='rb', track=6, case='upper'), tx('g_handle', 250, 1290, GEO, 20, INK, anchor='lb', track=3)]),
       'page': K('Page', ['Photo'], [('place', 'Vertical place name', 'LISBOA'), ('caption', 'Caption', 'yellow trams and blue tiles')],
                 [P(0, 250, 110, 770, 1030), tx('place', 128, 625, SERIF, 96, INK, anchor='mm', rot=90, track=16, case='upper'),
                  tx('caption', 250, 1200, SERIF_I, 40, INK, anchor='lt'), st('{no} / {of}', 1020, 1290, GEO_B, 20, INK, anchor='rb', track=6)]),
       'pair': K('Two photos', ['Left', 'Right'], [('place', 'Vertical place name', 'PORTO'), ('caption', 'Caption', 'port, slowly')],
                 [P(0, 250, 110, 375, 1030), P(1, 645, 110, 375, 1030), tx('place', 128, 625, SERIF, 96, INK, anchor='mm', rot=90, track=16, case='upper'),
                  tx('caption', 250, 1200, SERIF_I, 40, INK, anchor='lt'), st('{no} / {of}', 1020, 1290, GEO_B, 20, INK, anchor='rb', track=6)])},
      ['cover', 'page', ('page', {'place': 'SINTRA', 'caption': 'fog until noon, then gold'}), 'pair', ('page', {'place': 'ALGARVE', 'caption': 'the sea did the rest'})],
      bg=OFF, grain=3))

add(T('forest_italic', 'Deep green · italic serif', G_EDIT,
      'Forest green with a butter-yellow italic serif headline, a small brand line, and photos in thin cream frames.', 'Canva “Photo dump of my favorite moments lately”', ('lush', 0.55),
      {'cover': K('Cover', [], [('g_brand', 'Brand line', 'Notes from the road · by @yourname'), ('title', 'Headline', 'Photo dump of my\nfavourite moments\nlately.'),
                                 ('body', 'Small text', 'Slowing down made room for the good stuff — the little moments that stay with you the longest.')],
                  [tx('g_brand', 540, 70, SERIF_I, 30, CREAM, anchor='mt'), tx('title', 540, 380, SERIF_I, 100, BUTTER, anchor='mt', lh=1.06),
                   tx('body', 540, 820, GEO, 27, CREAM, anchor='mt', wrap=700, lh=1.6), st('swipe  →', 540, 1270, GEO_B, 22, BUTTER, anchor='mb', track=6)]),
       'photo': K('Photo', ['Photo'], [('caption', 'Caption', 'Tuesday, nowhere to be')],
                  [tx('g_brand', 540, 70, SERIF_I, 30, CREAM, anchor='mt'), P(0, 90, 150, 900, 1010, border=10, bcolor=CREAM),
                   tx('caption', 90, 1230, SERIF_I, 50, BUTTER, anchor='lt'), st('{no}', 990, 1236, GEO_B, 22, CREAM, anchor='rt', track=4)]),
       'pair': K('Two photos', ['Left', 'Right'], [('caption', 'Caption', 'a table for two, twice')],
                 [tx('g_brand', 540, 70, SERIF_I, 30, CREAM, anchor='mt'), P(0, 90, 150, 440, 680, border=10, bcolor=CREAM),
                  P(1, 550, 400, 440, 680, border=10, bcolor=CREAM), tx('caption', 90, 900, SERIF_I, 50, BUTTER, anchor='lt', wrap=420, lh=1.1)]),
       'end': K('Closing', [], [('title', 'Closing line', 'More soon.\nMore slowly.'), HANDLE],
                [tx('title', 540, 480, SERIF_I, 110, BUTTER, anchor='mt', lh=1.06), tx('g_handle', 540, 1270, GEO_B, 22, CREAM, anchor='mb', track=5)])},
      ['cover', 'photo', 'pair', ('photo', {'caption': 'the long way round'}), ('photo', {'caption': 'and breakfast, always'}), 'end'], bg=FOREST, grain=4))

add(T('offset_frame', 'Offset outline frame', G_EDIT,
      'A photo with a coloured outline frame offset behind it, big serif capitals with a script word overlapping.', 'Canva “VACATION time” carousel', ('peach', 0.55),
      {'cover': K('Cover', ['Photo'], [('t1', 'Big word', 'SUMMER'), ('t2', 'Script word', 'in Europe'), ('foot', 'Small line', 'June — August 2026')],
                  [RC(70, 270, 820, 900, None, outline=SALMON, width=8), P(0, 150, 340, 820, 900),
                   tx('t1', 540, 70, SERIF_SB, 160, INK, anchor='mt', track=12, case='upper'),
                   tx('t2', 700, 210, SCRIPT, 140, SALMON, anchor='mt', rot=-6, shadow=40),
                   tx('foot', 540, 1310, GEO_B, 22, INK, anchor='mb', track=7, case='upper')]),
       'photo': K('Framed (down-right)', ['Photo'], [('caption', 'Caption', 'every evening, the same bench')],
                  [RC(160, 150, 830, 960, None, outline=SALMON, width=8), P(0, 90, 80, 830, 960), tx('caption', 90, 1200, SERIF_I, 48, INK, anchor='lt'),
                   st('{no}', 1000, 1290, GEO_B, 22, SALMON, anchor='rb', track=4)]),
       'photo2': K('Framed (up-left)', ['Photo'], [('caption', 'Caption', 'peaches from the market')],
                   [RC(90, 90, 830, 960, None, outline=SALMON, width=8), P(0, 160, 160, 830, 960), tx('caption', 990, 1210, SERIF_I, 48, INK, anchor='rt'),
                    st('{no}', 80, 1290, GEO_B, 22, SALMON, anchor='lb', track=4)]),
       'end': K('Closing', ['Photo'], [('t1', 'Big word', 'SEE YOU'), ('t2', 'Script word', 'next summer'), HANDLE],
                [RC(260, 380, 560, 620, None, outline=SALMON, width=8), P(0, 300, 420, 560, 620), tx('t1', 540, 120, SERIF_SB, 140, INK, anchor='mt', track=10, case='upper'),
                 tx('t2', 640, 250, SCRIPT, 120, SALMON, anchor='mt', rot=-6), tx('g_handle', 540, 1260, GEO_B, 22, INK, anchor='mb', track=5)])},
      ['cover', 'photo', 'photo2', ('photo', {'caption': 'the yellow house'}), 'photo2', 'end'], bg=('paper', (246, 238, 228)), grain=3))

add(T('magazine_cover', 'Magazine cover + features', G_EDIT,
      'A full-bleed magazine cover with a huge masthead, cover lines and a round badge, then clean editorial feature pages.', 'Editorial magazine covers (Canva)', ('cinematic', 0.55),
      {'cover': K('Cover', ['Cover photo'], [('mast', 'Masthead', 'EUROPA'), ('issue', 'Issue line', 'Issue 07 · Summer 2026'),
                                              ('lines', 'Cover story', 'The slow\ntrain south'), ('sub', 'Small cover line', '+ 12 places to eat alone')],
                  [P(0, 0, 0, W, H), SHADE(0, 520, 140, 0), SHADE(700, 650, 0, 150),
                   tx('mast', 540, 30, SERIF_B, 270, WHITE, anchor='mt', fit=1010, shadow=50, case='upper'),
                   tx('issue', 60, 340, GEO_B, 22, WHITE, anchor='lt', track=5, case='upper', shadow=90),
                   tx('lines', 60, 820, SERIF_I, 78, WHITE, anchor='lt', lh=1.0, shadow=110), tx('sub', 60, 1010, GEO_B, 24, WHITE, anchor='lt', track=4, case='upper', shadow=110),
                   BADGE(910, 1170, 112, 'THE TRAVEL ISSUE · ', GEO_B, 19, WHITE, fill=WINE, ring=False, center='26', cfont=SERIF_B, csize=70)]),
       'feature': K('Feature page', ['Main photo', 'Small photo'], [('kicker', 'Small label', 'Chapter one'), ('head', 'Headline', 'Where the road runs out'),
                                                                    ('body', 'Text', 'We took the slowest train we could find and got off wherever the light looked good.')],
                    [P(0, 0, 0, W, 740), tx('kicker', 60, 800, GEO_B, 22, TERRA, anchor='lt', track=7, case='upper'),
                     tx('head', 60, 850, SERIF, 80, INK, anchor='lt', lh=1.0, wrap=600), tx('body', 60, 1080, 'GARA.TTF', 32, (86, 80, 72), anchor='lt', wrap=560, lh=1.45),
                     P(1, 700, 800, 320, 440), st('{no}', 1020, 1300, GEO_B, 20, INK, anchor='rb', track=4)]),
       'quote': K('Pull quote', ['Photo'], [('quote', 'Quote', '“Nobody here\nis in a hurry.”')],
                  [P(0, 0, 0, W, H, dim=0.3), st('“', 540, 260, SERIF_B, 260, WHITE, anchor='mt', shadow=0, alpha=210),
                   tx('quote', 540, 560, SERIF_I, 92, WHITE, anchor='mt', lh=1.05, shadow=110)])},
      ['cover', 'feature', 'quote', ('feature', {'kicker': 'Chapter two', 'head': 'Three days, one bakery', 'body': 'By the third morning the baker knew our order.'}),
       ('feature', {'kicker': 'Chapter three', 'head': 'The view from the top', 'body': 'Four hundred steps, one bench, no regrets.'})], bg=OFF, grain=3))

# ================================================================== New · Scrapbook
add(T('torn_quote', 'Torn paper quote', G_SCRAP,
      'Full photos with a torn strip of paper taped on, carrying a handwritten line.', 'Canva “go where the wind takes you”', ('instant', 0.55),
      {'quote': K('Quote in the middle', ['Photo'], [('words', 'Handwritten line', 'go where the\nwind takes you')],
                  [P(0, 0, 0, W, H), TORN(90, 520, 900, 300, rot=-2), TAPE(460, 500, 170, 48, rot=4),
                   tx('words', 540, 580, HAND, 72, INK, anchor='mt', lh=1.12, rot=-2)]),
       'low': K('Quote low', ['Photo'], [('words', 'Handwritten line', 'collect moments,\nnot things')],
                [P(0, 0, 0, W, H), TORN(110, 1000, 860, 250, rot=2), TAPE(160, 990, 150, 44, rot=-30), TAPE(830, 990, 150, 44, rot=30),
                 tx('words', 540, 1048, HAND, 64, INK, anchor='mt', lh=1.12, rot=2)]),
       'high': K('Quote high', ['Photo'], [('words', 'Handwritten line', 'stay a little longer')],
                 [P(0, 0, 0, W, H), TORN(140, 120, 800, 180, rot=-3), TAPE(470, 100, 160, 46, rot=-3),
                  tx('words', 540, 170, HAND, 66, INK, anchor='mt', rot=-3)]),
       'photo': K('Just the photo', ['Photo'], [('caption', 'Small handwriting', 'Lake Bled, 6:40am')],
                  [P(0, 0, 0, W, H), tx('caption', 70, 1280, HAND, 44, WHITE, anchor='lb', shadow=160, sblur=8)])},
      ['quote', 'photo', 'low', 'photo', 'high'], grain=4))

# ================================================================== New · Guides & fun
add(T('place_cards', 'Best spots · place cards', G_GUIDE,
      'A guide where each slide is one place: full photo with a white app-style card (name, stars, tip, Save button).', 'Canva UX/UI travel recap cards', ('vivid', 0.45),
      {'cover': K('Cover', ['Cover photo'], [('kicker', 'Small label', 'Save for your trip'), ('title', 'Title', 'Best spots\nin Lisbon'), ('btn', 'Button', "5 places I'd go back to  →")],
                  [P(0, 0, 0, W, H), SHADE(0, 820, 170, 0), tx('kicker', 70, 110, GEO_B, 26, WHITE, anchor='lt', track=7, case='upper', shadow=90),
                   tx('title', 66, 160, BLACK, 128, WHITE, anchor='lt', lh=0.95, shadow=90), PILL(70, 480, SANS_SB, 32, field='btn', fill=WHITE, color=INK, anchor='lt', shadow=60)]),
       'place': K('Place', ['Photo'], [('num', 'Number', '1'), ('name', 'Place', 'Miradouro da Graça'), ('meta', 'Rating · type · area', '4.9 · Viewpoint · Graça'),
                                       ('tip', 'Tip', 'Go at sunset and grab a drink from the kiosk.')],
                 [P(0, 0, 0, W, H), SHADE(820, 530, 0, 120), ELL(60, 60, 96, 96, fill=WHITE), tx('num', 108, 108, BLACK, 46, INK, anchor='mm'),
                  RC(60, 940, 960, 350, (255, 255, 255), radius=38, shadow=90), tx('name', 110, 985, SANS_SB, 50, INK, anchor='lt', fit=640),
                  st('★★★★★', 110, 1062, SYM, 30, (240, 160, 40), anchor='lt', track=3), tx('meta', 330, 1060, SANS, 30, MUTED, anchor='lt'),
                  tx('tip', 110, 1120, SANS, 31, (70, 66, 62), anchor='lt', wrap=860, lh=1.35),
                  PILL(970, 990, SANS_SB, 26, text='+ Save', fill=INK, color=WHITE, anchor='rt')]),
       'end': K('Closing', ['Photo'], [('title', 'Question', 'Which one\nfirst?'), ('btn', 'Button', 'Save this for later')],
                [P(0, 0, 0, W, H, dim=0.35), tx('title', 540, 470, BLACK, 130, WHITE, anchor='mt', lh=0.95, shadow=90),
                 PILL(540, 900, SANS_SB, 34, field='btn', fill=WHITE, color=INK, shadow=60)])},
      ['cover', 'place', ('place', {'num': '2', 'name': 'Time Out Market', 'meta': '4.6 · Food hall · Cais do Sodré', 'tip': 'Go before noon and share plates.'}),
       ('place', {'num': '3', 'name': 'LX Factory', 'meta': '4.7 · Shops & cafés · Alcântara', 'tip': 'Sunday market, then the bookshop with the bike.'}),
       ('place', {'num': '4', 'name': 'Belém Tower', 'meta': '4.5 · Landmark · Belém', 'tip': 'Walk the river from Cais do Sodré instead of the tram.'}), 'end']))

add(T('notebook_spots', 'Notebook · best spots', G_GUIDE,
      'Lavender squared paper, typewriter headings with a yellow highlighter, taped photos and a round “save this” badge.', 'Canva “Best spots in Boracay” notebook', ('pastel', 0.55),
      {'cover': K('Cover', ['Photo'], [('t1', 'Top line', 'best spots in'), ('t2', 'Place (highlighted)', 'Lisbon')],
                  [tx('t1', 120, 150, TYPE, 64, PURPLE, anchor='lt'), tx('t2', 120, 240, TYPE, 96, PURPLE, anchor='lt', hl=(HILITE, 10, 0)),
                   BADGE(860, 250, 112, 'SAVE THIS POST · ', GEO_B, 18, PURPLE, fill=HILITE, ring=False, center='✦', cfont=SYM, csize=60, rot=-10),
                   FRAME(0, 150, 470, 760, 780, b=16, rot=-2, sh=70), TAPE(450, 450, rot=-4)]),
       'spot': K('Spot', ['Photo'], [('name', 'Name', '1. Time Out Market'), ('tip', 'Tip', 'go early, share plates, skip the custard queue')],
                 [FRAME(0, 150, 100, 780, 720, b=16, rot=2, sh=70), TAPE(450, 84, rot=3),
                  tx('name', 140, 930, TYPE, 56, PURPLE, anchor='lt', hl=(HILITE, 8, 0)), tx('tip', 140, 1030, TYPE, 36, (70, 60, 92), anchor='lt', wrap=820, lh=1.5)]),
       'end': K('Closing', [], [('words', 'Closing lines', 'which one\nare you trying\nfirst?'), HANDLE],
                [tx('words', 540, 420, TYPE, 72, PURPLE, anchor='mt', lh=1.35), SPARK(540, 860, 40, PURPLE), tx('g_handle', 540, 1230, TYPE, 32, PURPLE, anchor='mb')])},
      ['cover', 'spot', ('spot', {'name': '2. LX Factory', 'tip': 'sunday market, then the bookshop with the bicycle'}),
       ('spot', {'name': '3. Alfama at dusk', 'tip': 'follow the fado, not the map'}), 'end'],
      bg=LAV, grain=3))
for _k in TEMPLATES[-1]['kinds'].values():          # squared paper + spiral rings under every notebook page
    _k['els'] = ([dict(t='ruled', rect=(0, 0, W, H), kind='grid', step=54, color=(140, 120, 190), alpha=55)] +
                 [ELL(22, y, 34, 34, outline=(120, 110, 140), width=5) for y in range(70, H - 40, 92)] + _k['els'])

add(T('month_chips', 'Month recap · chips', G_GUIDE,
      'Light paper, a friendly rounded title, colourful pill chips for the highlights and rounded photos.', 'Canva monthly recap with chips', ('peach', 0.5),
      {'cover': K('Cover', ['Photo A', 'Photo B'], [('kicker', 'Small label', 'Monthly recap'), ('title', 'Title', 'my month\nin Europe'),
                                                    ('c1', 'Chip 1', 'pasta'), ('c2', 'Chip 2', 'night trains'), ('c3', 'Chip 3', 'sunsets'), ('c4', 'Chip 4', 'gelato'),
                                                    ('c5', 'Chip 5', 'museums'), ('c6', 'Chip 6', 'too many photos')],
                  [tx('kicker', 70, 100, GEO_B, 26, MUTED, anchor='lt', track=7, case='upper'), tx('title', 64, 150, ROUND, 124, INK, anchor='lt', lh=0.96),
                   dict(t='chips', fields=['c1', 'c2', 'c3', 'c4', 'c5', 'c6'], xy=(70, 450), font=SANS_SB, size=30, color=INK, maxw=940,
                        fills=[(250, 214, 165), (198, 222, 246), (246, 196, 206), (206, 232, 196), (232, 214, 246), (252, 236, 160)]),
                   P(0, 70, 690, 455, 590, radius=30), P(1, 555, 690, 455, 590, radius=30)]),
       'photo': K('Photo + chips', ['Photo'], [('c1', 'Chip 1', 'coffee count: 41'), ('c2', 'Chip 2', 'Rome'), ('c3', 'Chip 3', 'week 2')],
                  [P(0, 70, 70, 940, 1020, radius=34),
                   dict(t='chips', fields=['c1', 'c2', 'c3'], xy=(70, 1140), font=SANS_SB, size=30, color=INK, maxw=940,
                        fills=[(250, 214, 165), (198, 222, 246), (246, 196, 206)])]),
       'stats': K('In numbers', ['Photo'], [('n1', 'Number 1', '9'), ('l1', 'Label 1', 'cities'), ('n2', 'Number 2', '41'), ('l2', 'Label 2', 'coffees'),
                                           ('n3', 'Number 3', '3'), ('l3', 'Label 3', 'trains missed')],
                 [st('in numbers', 70, 90, ROUND, 84, INK, anchor='lt'),
                  tx('n1', 70, 230, ROUND, 160, INK, anchor='lt'), PILL(330, 330, SANS_SB, 40, field='l1', fill=(250, 214, 165), color=INK, anchor='lm', pad=(36, 16)),
                  tx('n2', 70, 430, ROUND, 160, INK, anchor='lt'), PILL(330, 530, SANS_SB, 40, field='l2', fill=(198, 222, 246), color=INK, anchor='lm', pad=(36, 16)),
                  tx('n3', 70, 630, ROUND, 160, INK, anchor='lt'), PILL(330, 730, SANS_SB, 40, field='l3', fill=(246, 196, 206), color=INK, anchor='lm', pad=(36, 16)),
                  P(0, 70, 900, 940, 380, radius=30)]),
       'end': K('Closing', ['Photo'], [('title', 'Closing line', 'next month:\nthe Alps?'), HANDLE],
                [tx('title', 540, 180, ROUND, 120, INK, anchor='mt', lh=0.98), P(0, 240, 520, 600, 640, radius=34),
                 tx('g_handle', 540, 1260, SANS_SB, 28, MUTED, anchor='mb')])},
      ['cover', 'photo', 'stats', ('photo', {'c1': 'swims: daily', 'c2': 'Amalfi', 'c3': 'week 3'}), 'end'], bg=('paper', (246, 242, 236)), grain=2))

# ================================================================== New · Grids
CW, CH = 360, 450
add(T('checker_dump', 'Checkerboard dump', G_GRID,
      'A 3×3 grid with no gaps: photos alternate with soft colour squares; one square holds a brush-script title.', 'Canva “Year-End photo dump” checkerboard', ('warm', 0.5),
      {'cover': K('Cover', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4'], [('title', 'Title (script)', 'Europe\nphoto dump'), ('sub', 'Small line', '2026')],
                  [RC(0, 0, CW, CH, PEACH), RC(2 * CW, 0, CW, CH, PEACH), RC(0, 2 * CH, CW, CH, PEACH), RC(2 * CW, 2 * CH, CW, CH, PEACH),
                   RC(CW, CH, CW, CH, (247, 240, 230)),
                   P(0, CW, 0, CW, CH), P(1, 0, CH, CW, CH), P(2, 2 * CW, CH, CW, CH), P(3, CW, 2 * CH, CW, CH),
                   tx('title', 540, 660, SCRIPT, 96, INK, anchor='mm', lh=1.0, valign='middle', fit=320),
                   tx('sub', 540, 800, GEO_B, 20, TERRA, anchor='mt', track=8), SPARK(180, 225, 30, WHITE), SPARK(900, 1125, 30, WHITE)]),
       'grid': K('Grid', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4', 'Photo 5'], [('word', 'Word (script)', 'sun')],
                 [P(0, 0, 0, CW, CH), P(1, 2 * CW, 0, CW, CH), P(2, CW, CH, CW, CH), P(3, 0, 2 * CH, CW, CH), P(4, 2 * CW, 2 * CH, CW, CH),
                  RC(CW, 0, CW, CH, PEACH), RC(0, CH, CW, CH, (247, 240, 230)), RC(2 * CW, CH, CW, CH, PEACH), RC(CW, 2 * CH, CW, CH, (247, 240, 230)),
                  tx('word', 540, 225, SCRIPT, 96, INK, anchor='mm', fit=320), SPARK(180, 675, 26, TERRA), SPARK(540, 1125, 26, TERRA)])},
      ['cover', ('grid', {'word': 'sun'}), ('grid', {'word': 'sea'}), ('grid', {'word': 'slow'})], bg=(247, 240, 230)))
