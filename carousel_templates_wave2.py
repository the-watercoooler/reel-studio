"""Wave 2 of the inspiration-library templates (24 Nov 2026): 30 new layouts.

Sources (see Carousels\\Inspiration library): national-park and Swiss posters, Accidentally Wes Anderson, Wallpaper* City
Guides, Paula Scher's word maps, punk fanzine guides, Slim Aarons poolside colour, the Kia Kia walking-tour kit, passport
and stamp ephemera, departure boards, photo booths, exhibitions, newspaper clippings, record sleeves, Swiss/Bauhaus
graphics, moodboards, notes apps, food diaries, bingo cards, colour negatives, instant film, calendars, A–Z guides,
washi lines, countdowns, letters home and disposable-camera date stamps.
"""
from carousel_templates import P, RC, LN, SHADE, TAPE, K, W, H
from carousel_templates_pro import (T as _T, tx, st, PILL, SPARK, BADGE, WAVES, ELL, TORN, STAMP, FRAME,
                                    SERIF, SERIF_SB, SERIF_B, SERIF_I, BELL_I, COOPER, COND, COND_SB, BAHN, BAHN_SB, GEO, GEO_B,
                                    BLACK, ROUND, SCRIPT, HAND, TYPE, SANS, SANS_SB, SYM, WHITE, INK, MUTED)

MONO, MONO_B, IMPACT, GARA = 'consola.ttf', 'consolab.ttf', 'impact.ttf', 'GARA.TTF'
HANDLE = ('g_handle', 'Your @handle', '@yourname')
TEMPLATES = []
add = TEMPLATES.append


def T(key, label, style, about, ref, look, kinds, default, **kw):
    return _T(key, label, style, about, 'Inspiration library · ' + ref, look, kinds, default, style=style, batch='Wave 2', **kw)


# ------------------------------------------------------------------ 1. National park poster (screen print)
PARK_CREAM, PARK_BROWN = (240, 228, 196), (70, 46, 30)
PARK_PALS = {'dusk': [(38, 44, 62), (92, 70, 98), (200, 112, 82), (238, 178, 112), (246, 228, 188)],
             'forest': [(28, 44, 36), (52, 96, 70), (120, 150, 90), (214, 196, 120), (242, 236, 204)],
             'lake': [(20, 40, 70), (40, 100, 140), (90, 160, 170), (220, 200, 150), (246, 238, 214)],
             'desert': [(70, 30, 24), (150, 64, 40), (210, 120, 60), (240, 186, 110), (250, 234, 200)]}


def park(name):
    pal = PARK_PALS[name]
    return K(f'Poster ({name})', ['Photo'], [('top', 'Top band', 'See the Alps'), ('place', 'Place', 'Triglav'), ('sub', 'Small line', 'National park · Slovenia')],
             [RC(36, 36, W - 72, H - 72, None, outline=pal[0], width=8), RC(36, 36, W - 72, 190, pal[0]),
              tx('top', 540, 131, COND, 96, pal[-1], anchor='mm', case='upper', track=8),
              P(0, 70, 260, 940, 760, flat=pal), tx('place', 540, 1046, COND, 150, pal[0], anchor='mt', case='upper', fit=920),
              tx('sub', 540, 1222, GEO_B, 26, pal[1], anchor='mt', track=8, case='upper')], bg=pal[-1])


add(T('w_park_poster', 'National park posters', 'Vintage & postcards',
      'Screen-print travel posters: each photo reduced to five flat inks, a solid top band, a framed border and a condensed place name.',
      'Library of Congress WPA posters, Ben Fowler, Swiss tourism posters', ('natural', 0.5),
      {f'p_{n}': park(n) for n in PARK_PALS},
      [('p_dusk', {'top': 'See the Alps', 'place': 'Triglav', 'sub': 'National park · Slovenia'}),
       ('p_forest', {'top': 'Visit the forest', 'place': 'Plitvice', 'sub': 'Lakes national park · Croatia'}),
       ('p_lake', {'top': 'Take the boat', 'place': 'Lake Bled', 'sub': 'Julian Alps · Slovenia'}),
       ('p_desert', {'top': 'Go south', 'place': 'Algarve', 'sub': 'Coast & cliffs · Portugal'}),
       ('p_dusk', {'top': 'Stay a while', 'place': 'Dolomites', 'sub': 'South Tyrol · Italy'})], grain=5))

# ------------------------------------------------------------------ 2. Pastel symmetry
PASTELS = {'pink': ((244, 204, 204), (120, 50, 60)), 'mint': ((198, 228, 212), (30, 80, 66)),
           'butter': ((246, 228, 166), (110, 76, 20)), 'sky': ((192, 214, 236), (30, 56, 100))}


def pastel(n):
    bgc, ink = PASTELS[n]
    return K(f'Photo ({n})', ['Photo'], [('place', 'Place', 'Hotel Bellevue'), ('where', 'Where', 'Zermatt, Switzerland')],
             [st('N° {no}', 540, 92, GEO_B, 20, ink, anchor='mt', track=8), P(0, 150, 170, 780, 940, border=26, bcolor=(255, 255, 255), shadow=50, sblur=20),
              tx('place', 540, 1180, GEO_B, 28, ink, anchor='mt', track=8, case='upper'), tx('where', 540, 1228, SERIF_I, 28, ink, anchor='mt')], bg=bgc)


add(T('w_pastel_symmetry', 'Pastel symmetry', 'Minimal & journal',
      'Centred, symmetrical photos on candy pastel grounds with a numbered caption — one colour story per slide.',
      'Accidentally Wes Anderson', ('pastel', 0.6),
      {f'q_{n}': pastel(n) for n in PASTELS},
      [('q_pink', {}), ('q_mint', {'place': 'Funicular do Bica', 'where': 'Lisbon, Portugal'}), ('q_butter', {'place': 'Casa Amarela', 'where': 'Burano, Italy'}),
       ('q_sky', {'place': 'Lido baths', 'where': 'Vienna, Austria'}), ('q_pink', {'place': 'Rue Crémieux', 'where': 'Paris, France'})]))

# ------------------------------------------------------------------ 3. City guide cover (one colour per city)
CG, CGBG, CGI = (226, 82, 58), (248, 246, 240), (30, 30, 30)


def cg_list(label, d):
    els = [RC(0, 0, W, 210, CG), tx('sec', 70, 105, BAHN_SB, 86, WHITE, anchor='lm'), tx('g_city', 1010, 105, GEO_B, 22, WHITE, anchor='rm', track=6, case='upper')]
    for i in range(3):
        y = 270 + i * 340
        els += [P(i, 70, y, 300, 300), tx(f'n{i + 1}', 400, y + 10, BAHN_SB, 42, CGI, anchor='lt', wrap=600),
                tx(f'a{i + 1}', 400, y + 74, MONO, 22, (130, 126, 118), anchor='lt', wrap=600),
                tx(f'd{i + 1}', 400, y + 118, SERIF_I, 30, CGI, anchor='lt', wrap=600, lh=1.25), LN([(70, y + 320), (1010, y + 320)], color=(220, 214, 204), width=2)]
    fields = [('sec', 'Section', label)] + [f for i in range(3) for f in ((f'n{i + 1}', f'Name {i + 1}', d[i][0]), (f'a{i + 1}', f'Address {i + 1}', d[i][1]), (f'd{i + 1}', f'Note {i + 1}', d[i][2]))]
    return K(label, ['Photo 1', 'Photo 2', 'Photo 3'], fields, els, bg=CGBG)


add(T('w_city_guide', 'City guide (one colour)', 'Guides & itineraries',
      'A pocket city guide: a solid one-colour cover with only the city name, a panorama with numbered landmarks, then Stay / Eat / See listings.',
      'Wallpaper* City Guides, Herb Lester', ('natural', 0.55),
      {'cover': K('Cover', [], [('g_city', 'City (every slide)', 'Lisbon'), ('label', 'Small line', 'City guide'), ('chip', 'Colour line', 'Colour No. 17')],
                  [tx('label', 80, 100, GEO_B, 26, WHITE, anchor='lt', track=8, case='upper'), tx('g_city', 74, 1150, BAHN_SB, 170, WHITE, anchor='lb'),
                   LN([(80, 1190), (1000, 1190)], color=WHITE, width=2), tx('chip', 1000, 1250, MONO, 22, WHITE, anchor='rb')], bg=CG),
       'pano': K('Panorama + landmarks', ['Panorama'], [('t1', 'Landmark 1', 'Castelo de São Jorge'), ('t2', 'Landmark 2', 'Sé Cathedral'), ('t3', 'Landmark 3', 'Ponte 25 de Abril')],
                 [tx('g_city', 70, 100, BAHN_SB, 70, CGI, anchor='lt'), P(0, 0, 260, W, 640),
                  *[e for i, (x, y) in enumerate([(240, 420), (560, 560), (880, 700)]) for e in (
                      ELL(x - 26, y - 26, 52, 52, fill=CG), st(str(i + 1), x, y, BAHN_SB, 28, WHITE, anchor='mm'))],
                  *[e for i in range(3) for e in (ELL(70, 980 + i * 90, 40, 40, fill=CG), st(str(i + 1), 90, 1000 + i * 90, BAHN_SB, 22, WHITE, anchor='mm'),
                                                  tx(f't{i + 1}', 130, 1000 + i * 90, BAHN, 36, CGI, anchor='lm'))]], bg=CGBG),
       'stay': cg_list('Stay', [('Memmo Alfama', 'Tv. Merceeiras 27', 'Rooftop pool over the river.'), ('Casa Balthazar', 'R. do Duque 26', 'Six rooms, one garden.'),
                                ('The Lumiares', 'R. do Diário de Notícias 142', 'Apartments with kitchens.')]),
       'eat': cg_list('Eat', [('Taberna da Rua das Flores', 'R. das Flores 103', 'No bookings; worth the queue.'), ('Manteigaria', 'R. do Loreto 2', 'The best custard tarts, warm.'),
                              ('O Velho Eurico', 'Largo de São Cristóvão 3', 'Loud, local, cheap.')]),
       'see': cg_list('See', [('Gulbenkian Museum', 'Av. de Berna 45A', 'Art and a quiet garden.'), ('MAAT', 'Av. Brasília', 'River-front architecture.'),
                              ('LX Factory', 'R. Rodrigues de Faria 103', 'Sunday market and books.')])},
      ['cover', 'pano', 'stay', 'eat', 'see']))

# ------------------------------------------------------------------ 4. Word map (typographic)
WM_BG, WM_C = (246, 240, 228), [(214, 58, 46), (34, 70, 160), (30, 28, 26), (220, 150, 40)]
WM_POS = [(80, 120, 150, -4), (600, 160, 90, 6), (130, 380, 110, 3), (560, 420, 170, -5), (90, 640, 80, -8),
          (420, 700, 130, 2), (120, 920, 120, 5), (640, 930, 90, -3), (300, 1120, 100, -2), (760, 1150, 70, 7)]
WM_NAMES = ['Lisboa', 'Porto', 'Sintra', 'Cascais', 'Évora', 'Lagos', 'Coimbra', 'Braga', 'Faro', 'Nazaré']

add(T('w_word_map', 'Word map', 'Bold type & posters',
      'A country drawn only with place names: big and small, tilted, in four inks. Then photo slides with an outlined place name over each picture.',
      'Paula Scher maps', ('punchy', 0.5),
      {'map': K('Word map', [], [(f'm{i + 1}', f'Place {i + 1}', n) for i, n in enumerate(WM_NAMES)] + [('title', 'Title', 'Portugal, roughly')],
                [*[tx(f'm{i + 1}', x, y, COND if i % 3 else SERIF_B, int(s * 1.45), WM_C[i % 4], anchor='lt', rot=r, case='upper' if i % 2 == 0 else None,
                      fit=1040 - x)
                   for i, (x, y, s, r) in enumerate(WM_POS)],
                 RC(0, 1270, W, 80, (30, 28, 26)), tx('title', 540, 1310, GEO_B, 26, WM_BG, anchor='mm', track=10, case='upper')], bg=WM_BG),
       'photo': K('Photo + outlined name', ['Photo'], [('place', 'Place', 'Sintra'), ('coords', 'Coordinates', '38.80° N  9.38° W')],
                  [P(0, 0, 0, W, H), SHADE(700, 650, 0, 150), tx('place', 540, 980, COND, 260, WHITE, anchor='mt', fit=1000, case='upper', outline=True, stroke=4, shadow=0),
                   tx('coords', 540, 1260, MONO, 26, WHITE, anchor='mt', shadow=120)])},
      ['map', 'photo', ('photo', {'place': 'Porto', 'coords': '41.15° N  8.61° W'}), ('photo', {'place': 'Lagos', 'coords': '37.10° N  8.67° W'}), 'map']))

# ------------------------------------------------------------------ 5. Punk fanzine guide
ZINE = (236, 234, 228)
add(T('w_fanzine', 'Punk fanzine guide', 'Collage & experimental',
      'A city guide as a photocopied fanzine: xerox photos, ransom-note headlines cut from different "magazines", tape, staples and marker notes.',
      'Punkxegut London guide, GET LOST!', ('none', 0.0),
      {'cover': K('Cover', ['Cover photo'], [('title', 'Ransom title', 'LISBON\nUNDERGROUND'), ('issue', 'Marker note', 'issue #1 — free')],
                  [P(0, 60, 330, 960, 760, xerox=True, rot=-2, shadow=60), dict(t='ransom', field='title', xy=(60, 60), size=80, maxw=960, seed=3),
                   TAPE(120, 310, rot=-30), TAPE(900, 1060, rot=-25), tx('issue', 1010, 1150, HAND, 62, INK, anchor='rt', rot=-6),
                   LN([(30, 40), (30, 110)], color=(120, 120, 120), width=5), LN([(30, 1240), (30, 1310)], color=(120, 120, 120), width=5)]),
       'spot': K('Spot', ['Photo'], [('name', 'Ransom name', 'TASCA DO CHICO'), ('addr', 'Address', 'R. do Diário de Notícias 39'),
                                     ('note', 'Marker note', 'fado every night.\nget there by 9 or forget it')],
                 [dict(t='ransom', field='name', xy=(70, 70), size=80, maxw=940, seed=11), P(0, 90, 310, 900, 620, xerox=True, rot=2, shadow=60), TAPE(440, 290, rot=4),
                  RC(70, 980, 600, 70, (20, 20, 20)), tx('addr', 90, 1015, MONO, 26, ZINE, anchor='lm'),
                  tx('note', 70, 1090, HAND, 50, INK, anchor='lt', rot=-2, lh=1.1, wrap=900)]),
       'list': K('Do / don\'t', [], [('head', 'Ransom heading', "DON'T MISS"), *[(f'l{i}', f'Line {i}', s) for i, s in enumerate(
           ['the 28 tram at 7am, before the crowds', 'ginjinha from a plastic cup', 'the flea market on Saturday', 'skip the Santa Justa queue', 'walk home via the river'], 1)]],
                 [dict(t='ransom', field='head', xy=(70, 70), size=100, maxw=940, seed=21),
                  *[e for i in range(5) for e in (st('✓' if i < 4 else '✗', 80, 330 + i * 170, SYM, 54, (200, 30, 30), anchor='lt'),
                                                  tx(f'l{i + 1}', 160, 334 + i * 170, HAND, 50, INK, anchor='lt', wrap=840, rot=-1))]]),
       'end': K('Closing', ['Photo'], [('word', 'Ransom word', 'SEE YA'), HANDLE],
                [P(0, 160, 380, 760, 620, xerox=True, rot=-3, shadow=60), dict(t='ransom', field='word', xy=(120, 120), size=150, maxw=900, seed=5),
                 tx('g_handle', 540, 1150, HAND, 64, INK, anchor='mt', rot=-4)])},
      ['cover', 'spot', ('spot', {'name': 'LX FACTORY', 'addr': 'R. Rodrigues de Faria 103', 'note': 'sunday market.\nthe bookshop with the bikes'}), 'list', 'end'],
      bg=('paper', ZINE), grain=8))

# ------------------------------------------------------------------ 6. Poolside retro
AQUA, CORAL, PCREAM, PDEEP = (96, 196, 204), (240, 120, 96), (248, 238, 220), (24, 64, 90)


def awning(c1=CORAL, c2=PCREAM):
    els = [RC(i * 90, 0, 90, 150, c1 if i % 2 == 0 else c2) for i in range(12)]
    els += [ELL(i * 90, 105, 90, 90, fill=c1 if i % 2 == 0 else c2) for i in range(12)]
    return els


add(T('w_poolside', 'Poolside retro', 'Vintage & postcards',
      'Seventies poolside colour: a scalloped awning, round-cornered photos, a chunky retro headline and a script line.',
      'Slim Aarons, Pescalemoria', ('seventies', 0.6),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'Poolside'), ('sub', 'Script line', "diaries, summer '26")],
                  [*awning(), P(0, 90, 260, 900, 820, radius=60), tx('title', 540, 1104, COOPER, 112, PDEEP, anchor='mt'),
                   tx('sub', 540, 1232, SCRIPT, 66, CORAL, anchor='mt')], bg=PCREAM),
       'photo': K('Photo', ['Photo'], [('cap', 'Caption', 'Lunch, then a nap, then lunch')],
                  [*awning(AQUA, PCREAM), P(0, 90, 260, 900, 860, radius=60), tx('cap', 540, 1170, COOPER, 54, PDEEP, anchor='mt', wrap=900)], bg=PCREAM),
       'two': K('Two photos', ['Left', 'Right'], [('cap', 'Caption', 'his & hers sun loungers')],
                [*awning(), P(0, 70, 270, 455, 760, radius=50), P(1, 555, 270, 455, 760, radius=50), tx('cap', 540, 1110, SCRIPT, 76, CORAL, anchor='mt')], bg=PCREAM),
       'end': K('Closing', [], [('title', 'Title', 'See you\npoolside'), HANDLE],
                [*awning(AQUA, PCREAM), tx('title', 540, 460, COOPER, 140, PDEEP, anchor='mt', lh=0.95), tx('g_handle', 540, 900, SCRIPT, 70, CORAL, anchor='mt'),
                 ELL(390, 1040, 300, 300, fill=(246, 196, 80))], bg=PCREAM)},
      ['cover', 'photo', 'two', ('photo', {'cap': 'The water was exactly this blue'}), 'end'], grain=4))

# ------------------------------------------------------------------ 7. Walking tour kit
WT_BG, WT_G = (232, 226, 212), (46, 110, 90)
WT_ROUTE = [(200, 420), (380, 560), (300, 760), (560, 860), (760, 700), (860, 960)]
add(T('w_walking_tour', 'Walking tour cards', 'Guides & itineraries',
      'A walking tour as a deck of cards: a route cover with distance and time, then one card per stop with its number, photo and minutes to the next stop.',
      'Kia Kia Penang walking-tour kit', ('natural', 0.55),
      {'cover': K('Route cover', [], [('title', 'Title', 'Alfama\non foot'), ('meta', 'Route line', '2.4 km · 90 min · 6 stops')],
                  [tx('title', 70, 80, SERIF_B, 110, INK, anchor='lt', lh=0.98), PILL(70, 340, MONO, 26, field='meta', fill=WT_G, color=WHITE, anchor='lm'),
                   LN(WT_ROUTE, color=WT_G, width=7, dash=(16, 12)),
                   *[e for i, (x, y) in enumerate(WT_ROUTE) for e in (ELL(x - 30, y - 30, 60, 60, fill=WHITE, outline=WT_G, width=5),
                                                                       st(str(i + 1), x, y, BAHN_SB, 30, WT_G, anchor='mm'))],
                   st('START', 200, 470, GEO_B, 20, WT_G, anchor='mt', track=4), st('FINISH', 860, 1010, GEO_B, 20, WT_G, anchor='mt', track=4)], bg=WT_BG),
       'stop': K('Stop card', ['Photo'], [('num', 'Stop number', '1'), ('name', 'Name', 'Miradouro de Santa Luzia'),
                                          ('desc', 'Note', 'Tiles, bougainvillea and the whole river below. Come back at sunset.'), ('next', 'To next stop', 'NEXT STOP → 6 MIN')],
                 [RC(100, 100, 880, 1150, WHITE, radius=28, shadow=70), P(0, 140, 140, 800, 640, radius=18),
                  ELL(116, 116, 110, 110, fill=WT_G), tx('num', 171, 171, BAHN_SB, 52, WHITE, anchor='mm'),
                  tx('name', 140, 820, SERIF_B, 54, INK, anchor='lt', wrap=800, lh=1.05), tx('desc', 140, 960, SANS, 32, (80, 80, 80), anchor='lt', wrap=800, lh=1.35),
                  LN([(140, 1150), (940, 1150)], color=(220, 214, 204), width=2), tx('next', 140, 1196, MONO, 24, WT_G, anchor='lm')], bg=WT_BG),
       'end': K('Finish', [], [('title', 'Title', 'Tour complete'), HANDLE],
                [STAMP(540, 520, 230, 'ALFAMA · WALKED · 2026', WT_G, rot=-10), tx('title', 540, 860, SERIF_B, 90, INK, anchor='mt'),
                 tx('g_handle', 540, 1000, MONO, 28, WT_G, anchor='mt')], bg=WT_BG)},
      ['cover', 'stop', ('stop', {'num': '2', 'name': 'Sé Cathedral', 'desc': 'Twelfth-century and fortress-like. The tram squeals past the door.'}),
       ('stop', {'num': '3', 'name': 'Feira da Ladra', 'desc': 'The thieves’ market: Tuesdays and Saturdays, from early.'}), 'end']))

# ------------------------------------------------------------------ 8. Passport stamps
PP_PAGE, PP_NAVY, PP_GOLD = (226, 232, 222), (24, 40, 72), (212, 178, 104)


def guilloche():
    return [WAVES(-40, 60 + i * 120, 1160, 60, (150, 170, 150), n=3, amp=14, period=110, width=2, alpha=70) for i in range(11)]


add(T('w_passport', 'Passport pages', 'Vintage & postcards',
      'A passport for the trip: a navy cover with a gold seal, then pages of entry stamps over a fine guilloche pattern, with a visa photo and a machine-readable line.',
      'ZINE Art Traveler Passport, passport ephemera', ('natural', 0.55),
      {'cover': K('Passport cover', [], [('title', 'Title', 'Passport'), ('sub', 'Line', 'of a slow traveller')],
                  [BADGE(540, 560, 190, 'EUROPE · TRAVEL DOCUMENT · 2026 · ', GEO_B, 22, PP_GOLD, ring=True, ringw=3, center='✦', cfont=SYM, csize=110),
                   tx('title', 540, 860, GEO_B, 70, PP_GOLD, anchor='mt', track=24, case='upper'), tx('sub', 540, 970, SERIF_I, 38, PP_GOLD, anchor='mt')], bg=PP_NAVY),
       'stamps': K('Stamp page', [], [('s1', 'Stamp 1', 'LISBOA · 04 OCT 2026'), ('s2', 'Stamp 2', 'ARRIVED · PORTO'), ('s3', 'Stamp 3', 'SINTRA · 09 OCT'),
                                      ('s4', 'Stamp 4', 'DEPARTED · FARO')],
                  [*guilloche(), dict(t='stamp', xy=(300, 340), r=130, field='s1', color=(190, 40, 50), rot=-12),
                   RC(540, 250, 420, 210, None, outline=(40, 120, 80), width=7, rot=8), tx('s2', 750, 355, GEO_B, 40, (40, 120, 80), anchor='mm', rot=8),
                   dict(t='stamp', xy=(760, 760), r=150, field='s3', color=(40, 70, 160), rot=10),
                   RC(110, 900, 460, 190, None, outline=(150, 60, 140), width=7, rot=-6), tx('s4', 340, 995, GEO_B, 40, (150, 60, 140), anchor='mm', rot=-6),
                   st('{no}', 1000, 1290, MONO, 22, (110, 120, 110), anchor='rb')], bg=PP_PAGE),
       'visa': K('Visa page', ['Visa photo'], [('dest', 'Destination', 'PORTUGAL'), ('date', 'Dates', '04 OCT – 25 OCT 2026'), ('stay', 'Stay', '21 DAYS · NO PLAN'),
                                               ('mrz', 'Machine line', 'P<EUR<<SLOW<<TRAVELLER<<<<<<<<<<<<<<<<<<')],
                [*guilloche(), RC(80, 260, 920, 720, (240, 244, 236), radius=8, outline=(120, 140, 120), width=2),
                 st('VISA', 120, 300, GEO_B, 40, PP_NAVY, anchor='lt', track=12), P(0, 120, 380, 300, 380, border=8, bcolor=WHITE),
                 st('DESTINATION', 470, 390, GEO_B, 18, (110, 120, 110), anchor='lt', track=5), tx('dest', 470, 420, MONO_B, 40, PP_NAVY, anchor='lt'),
                 st('DATES', 470, 520, GEO_B, 18, (110, 120, 110), anchor='lt', track=5), tx('date', 470, 550, MONO, 32, PP_NAVY, anchor='lt'),
                 st('PURPOSE', 470, 640, GEO_B, 18, (110, 120, 110), anchor='lt', track=5), tx('stay', 470, 670, MONO, 32, PP_NAVY, anchor='lt'),
                 tx('mrz', 120, 880, MONO, 30, PP_NAVY, anchor='lt'), dict(t='stamp', xy=(880, 900), r=110, text='APPROVED · EUROPA', color=(190, 40, 50), rot=-16)], bg=PP_PAGE),
       'end': K('Closing stamp', [], [('word', 'Stamp', 'ARRIVED HOME · 2026'), HANDLE],
                [*guilloche(), dict(t='stamp', xy=(540, 560), r=280, field='word', color=(190, 40, 50), rot=-8),
                 tx('g_handle', 540, 1100, MONO, 30, PP_NAVY, anchor='mt')], bg=PP_PAGE)},
      ['cover', 'stamps', 'visa', ('stamps', {'s1': 'MADRID · 26 OCT 2026', 's2': 'ARRIVED · SEVILLA', 's3': 'GRANADA · 30 OCT', 's4': 'DEPARTED · MÁLAGA'}), 'end'],
      grain=3))

# ------------------------------------------------------------------ 9. Departure board
FLAP_Y = (250, 210, 60)
DEST = [('07:15', 'PORTO'), ('08:40', 'SINTRA'), ('09:05', 'COIMBRA'), ('11:30', 'FARO'), ('13:50', 'MADRID'), ('16:20', 'SEVILLA')]
STAT = ['ON TIME', 'BOARDING', 'ON TIME', 'DELAYED', 'ON TIME', 'CANCELLED']
add(T('w_departures', 'Departure board', 'Fun & story',
      'Split-flap station boards: a departures cover listing every stop of the trip, photo slides with a "next" board, and an ARRIVED end card.',
      'Travel ephemera, Wallpaper* City Guides', ('cinematic', 0.6),
      {'board': K('Departures board', [], [*[f for i, (tm, d) in enumerate(DEST) for f in ((f't{i + 1}', f'Time {i + 1}', tm), (f'd{i + 1}', f'Destination {i + 1}', d))]],
                  [dict(t='flap', text='DEPARTURES', xy=(60, 80), size=84, cols=10, color=WHITE), st('LISBOA · SANTA APOLÓNIA', 60, 200, MONO, 24, (150, 150, 150), anchor='lt'),
                   *[e for i in range(6) for e in (dict(t='flap', field=f't{i + 1}', xy=(60, 290 + i * 150), size=72, cols=5, color=FLAP_Y),
                                                   dict(t='flap', field=f'd{i + 1}', xy=(370, 290 + i * 150), size=72, cols=10, color=FLAP_Y),
                                                   st(STAT[i], 1020, 380 + i * 150, MONO_B, 20, (120, 220, 120) if STAT[i] in ('ON TIME', 'BOARDING') else (240, 100, 80), anchor='rt'))]],
                  bg=(18, 18, 20)),
       'next': K('Photo + next board', ['Photo'], [('dest', 'Next destination', 'PORTO'), ('gate', 'Details', 'PLATFORM 3 · 07:15 · CAR 4')],
                 [P(0, 0, 0, W, H), RC(0, 0, W, 300, (18, 18, 20, 230)), st('NEXT', 60, 70, MONO_B, 28, (150, 150, 150), anchor='lt', track=4),
                  dict(t='flap', field='dest', xy=(60, 120), size=96, cols=8, color=FLAP_Y), tx('gate', 60, 250, MONO, 26, WHITE, anchor='lm', shadow=0)]),
       'end': K('Arrived', ['Photo'], [('word', 'Board word', 'ARRIVED'), HANDLE],
                [P(0, 0, 0, W, H, dim=0.45), dict(t='flap', field='word', xy=(115, 560), size=130, cols=7, color=FLAP_Y),
                 tx('g_handle', 540, 1250, MONO, 28, WHITE, anchor='mb', shadow=120)])},
      ['board', 'next', ('next', {'dest': 'SINTRA', 'gate': 'PLATFORM 1 · 08:40'}), ('next', {'dest': 'FARO', 'gate': 'PLATFORM 6 · 11:30 · DELAYED'}), 'end'], grain=3))

# ------------------------------------------------------------------ 10. Luggage tag
MANILA = (232, 196, 120)


def tag(x, y, w=380, h=500, col=MANILA):
    return [LN([(x + w / 2, 0), (x + w / 2 - 40, y / 2), (x + w / 2, y + 40)], color=(240, 240, 240), width=4, alpha=220),
            RC(x, y, w, h, col, radius=34, shadow=110), ELL(x + w / 2 - 26, y + 34, 52, 52, fill=(250, 248, 240), outline=(200, 170, 110), width=6),
            LN([(x + 30, y + 130), (x + w - 30, y + 130)], color=(160, 120, 60), width=2)]


add(T('w_luggage_tag', 'Luggage tags', 'Fun & story',
      'A manila luggage tag hangs over each photo with FROM / TO and a handwritten name — the trip told as a stack of tagged bags.',
      'Travel ephemera, Envato ticket mockups', ('warm', 0.55),
      {'tag': K('Photo + tag', ['Photo'], [('from', 'From', 'LISBOA'), ('to', 'To', 'PORTO'), ('name', 'Handwritten name', 'the blue suitcase')],
                [P(0, 0, 0, W, H), *tag(620, 700), st('FROM', 650, 860, GEO_B, 18, (120, 90, 40), anchor='lt', track=5),
                 tx('from', 650, 888, COND, 64, INK, anchor='lt', case='upper', fit=320), st('TO', 650, 980, GEO_B, 18, (120, 90, 40), anchor='lt', track=5),
                 tx('to', 650, 1008, COND, 64, INK, anchor='lt', case='upper', fit=320), tx('name', 810, 1120, HAND, 38, (60, 60, 120), anchor='mt', rot=-3)]),
       'cover': K('Cover', ['Photo'], [('title', 'Title', 'Packed\n& tagged'), ('sub', 'Line', '21 days · 1 carry-on')],
                  [P(0, 0, 0, W, H, dim=0.25), *tag(300, 360, 480, 640), tx('title', 540, 560, COND, 120, INK, anchor='mt', lh=0.92, case='upper'),
                   tx('sub', 540, 860, MONO, 28, INK, anchor='mt')])},
      ['cover', 'tag', ('tag', {'from': 'PORTO', 'to': 'MADRID', 'name': 'still the blue suitcase'}), ('tag', {'from': 'MADRID', 'to': 'HOME', 'name': 'heavier now'})], grain=3))

# ------------------------------------------------------------------ 11. Photo booth strips
CURTAIN = (176, 34, 44)


def curtain():
    return [RC(i * 60, 0, 30, H, (150, 24, 34)) for i in range(18)]


def strip(x, y, slots, cap_field=None):
    els = [RC(x, y, 300, 1160, WHITE, radius=6, shadow=110)]
    els += [P(s, x + 20, y + 20 + i * 270, 260, 250) for i, s in enumerate(slots)]
    if cap_field:
        els.append(tx(cap_field, x + 150, y + 1110, HAND, 34, INK, anchor='mm'))
    return els


add(T('w_photobooth', 'Photo booth strips', 'Scrapbook & polaroid',
      'Four-frame photo-booth strips on a red curtain, each with a handwritten date at the bottom.',
      'Instant photo ephemera, photo-dump boards', ('instant', 0.6),
      {'cover': K('Two strips', [f'Frame {i}' for i in range(1, 9)], [('c1', 'Caption 1', 'porto, 04.10'), ('c2', 'Caption 2', 'lisbon, 09.10')],
                  [*curtain(), *strip(150, 95, [0, 1, 2, 3], 'c1'), *strip(630, 95, [4, 5, 6, 7], 'c2')], bg=CURTAIN),
       'one': K('Strip + photo', [f'Frame {i}' for i in range(1, 5)] + ['Big photo'], [('c1', 'Caption', 'sintra, 12.10'), ('note', 'Note', 'four tries, one good one')],
                [*curtain(), *strip(80, 95, [0, 1, 2, 3], 'c1'), FRAME(4, 440, 260, 560, 720, b=16, rot=3, sh=130),
                 tx('note', 720, 1100, HAND, 50, WHITE, anchor='mt', rot=-3, shadow=150)], bg=CURTAIN)},
      ['cover', 'one', ('cover', {'c1': 'faro, 18.10', 'c2': 'lagos, 20.10'}), 'one'], grain=4))

# ------------------------------------------------------------------ 12. Postage stamps
ALBUM = (240, 234, 222)
add(T('w_stamps', 'Postage stamps', 'Vintage & postcards',
      'Every photo printed as a perforated postage stamp with a value and a country: one big stamp on the cover, then an album page of six.',
      'Greetings-from postcards, travel ephemera', ('vintage', 0.55),
      {'cover': K('Big stamp', ['Stamp photo'], [('country', 'Country', 'Portugal'), ('val', 'Value', '€1.20'), ('title', 'Title', 'Collected\nin 2026')],
                  [P(0, 210, 160, 660, 820, shape='stamp', border=30, bcolor=WHITE, shadow=70, sblur=12),
                   tx('country', 260, 920, GEO_B, 40, WHITE, anchor='lb', track=6, case='upper', shadow=150), tx('val', 820, 230, COOPER, 54, WHITE, anchor='rt', shadow=150),
                   WAVES(560, 120, 420, 90, (40, 40, 60), n=5, width=5, alpha=170), STAMP(880, 240, 90, 'LISBOA · 2026', (190, 50, 40), rot=12),
                   tx('title', 540, 1060, SERIF_B, 84, INK, anchor='mt', lh=1.0)], bg=ALBUM),
       'album': K('Album page', [f'Stamp {i}' for i in range(1, 7)], [('cap', 'Caption', 'the coast set, six values')] + [(f'v{i}', f'Value {i}', v) for i, v in enumerate(['€0.50', '€0.80', '€1.20', '€2', '€0.60', '€3'], 1)],
                 [*[e for i in range(6) for e in (P(i, 86 + (i % 3) * 320, 150 + (i // 3) * 470, 262, 390, shape='stamp', border=16, bcolor=WHITE, shadow=50, sblur=8),
                                                  tx(f'v{i + 1}', 86 + (i % 3) * 320 + 240, 150 + (i // 3) * 470 + 28, COOPER, 30, WHITE, anchor='rt', shadow=150))],
                  tx('cap', 540, 1130, SERIF_I, 44, INK, anchor='mt')], bg=ALBUM)},
      ['cover', 'album', ('album', {'cap': 'the mountain set'}), ('cover', {'country': 'Slovenia', 'val': '€0.90', 'title': 'First day\nof issue'})], grain=3))

# ------------------------------------------------------------------ 13. Exhibition
WALL = (226, 222, 214)


def framed(slot, x, y, w, h):
    return [RC(x - 58, y - 58, w + 116, h + 116, (26, 24, 22), shadow=90), P(slot, x, y, w, h, border=36, bcolor=(250, 248, 244))]


add(T('w_exhibition', 'Exhibition', 'Minimal & journal',
      'The trip hung as a show: wall text with the title, then framed photos with white mats and small museum labels.',
      'LE ARCHIVE, gallery-mat editorial', ('matte', 0.5),
      {'title': K('Wall text', [], [('title', 'Exhibition title', 'Europe: a retrospective'), ('room', 'Room', 'Room 1 — The Coast'), ('dates', 'Dates', '4 October – 25 October 2026')],
                  [tx('title', 120, 440, SERIF, 96, INK, anchor='lt', wrap=840, lh=1.02), LN([(120, 730), (300, 730)], color=INK, width=3),
                   tx('room', 120, 770, GEO_B, 24, INK, anchor='lt', track=6, case='upper'), tx('dates', 120, 816, SERIF_I, 32, MUTED, anchor='lt')], bg=WALL),
       'work': K('Framed work', ['Photo'], [('t', 'Work title', 'Light on water'), ('m', 'Details', 'Lake Bled, 2026. Phone camera, morning light.'), ('c', 'Credit', 'Collection of @yourname')],
                 [*framed(0, 230, 180, 620, 760), RC(640, 1090, 360, 170, (250, 250, 248), shadow=30),
                  tx('t', 664, 1112, SERIF_B, 28, INK, anchor='lt', wrap=320), tx('m', 664, 1160, SANS, 20, MUTED, anchor='lt', wrap=320, lh=1.3),
                  tx('c', 664, 1222, SANS, 18, MUTED, anchor='lt')], bg=WALL),
       'pair': K('Two works', ['Left', 'Right'], [('t', 'Label', 'Two windows, Porto, 2026')],
                 [*framed(0, 120, 300, 360, 480), *framed(1, 600, 300, 360, 480), RC(120, 1000, 420, 100, (250, 250, 248), shadow=30),
                  tx('t', 144, 1050, SERIF_I, 26, INK, anchor='lm', wrap=380)], bg=WALL)},
      ['title', 'work', ('work', {'t': 'The last tram', 'm': 'Lisbon, 2026. After dark.'}), 'pair', ('work', {'t': 'Fog, Sintra', 'm': 'Sintra, 2026. Before noon.'})], grain=2))

# ------------------------------------------------------------------ 14. Newspaper clippings
NEWSP = (238, 236, 228)
add(T('w_clippings', 'Newspaper clippings', 'Scrapbook & polaroid',
      'Torn newspaper clippings with tongue-in-cheek headlines, grainy black-and-white press photos and tape, on kraft paper.',
      'HANOI diary, Broadsheet', ('bw', 0.0),
      {'cover': K('Front page clipping', ['Press photo'], [('paper', 'Paper name', 'The Europe Gazette'), ('head', 'Headline', 'Local traveller finds perfect gelato, refuses to share location'),
                                                         ('b1', 'Text', 'Witnesses say the cone was pistachio. The traveller, who has been on the road for three weeks, declined to comment.')],
                  [TORN(70, 100, 940, 1150, rot=-2, col=NEWSP), tx('paper', 540, 150, SERIF_B, 56, INK, anchor='mt', rot=-2, case='upper'),
                   LN([(120, 240), (960, 210)], color=INK, width=3), tx('head', 120, 260, SERIF_B, 62, INK, anchor='lt', wrap=840, lh=1.02, rot=-2),
                   P(0, 130, 560, 820, 440, mono=True, rot=-2), tx('b1', 130, 1030, GARA, 28, INK, anchor='lt', wrap=820, lh=1.35, rot=-2),
                   TAPE(80, 90, rot=-35), TAPE(900, 1180, rot=-30)]),
       'clip': K('Small clipping', ['Photo', 'Press photo'], [('head', 'Headline', 'Tram 28 "basically a ride", says visitor'), ('b1', 'Text', 'Queue described as "part of the experience".')],
                 [P(0, 0, 0, W, 700), TORN(110, 600, 860, 640, rot=3, col=NEWSP), tx('head', 160, 660, SERIF_B, 54, INK, anchor='lt', wrap=760, lh=1.05, rot=3),
                  P(1, 170, 880, 360, 260, mono=True, rot=3), tx('b1', 570, 900, GARA, 28, INK, anchor='lt', wrap=360, lh=1.35, rot=3), TAPE(450, 590, rot=3)])},
      ['cover', 'clip', ('clip', {'head': 'Area couple eats custard tarts for every meal', 'b1': 'Doctors "not surprised".'}), 'clip'],
      bg=('paper', (214, 196, 166)), grain=5))

# ------------------------------------------------------------------ 15. Trip soundtrack (vinyl)
VB, VA = (24, 22, 26), (232, 87, 46)


def record(x, y, d=720, slot=1):
    els = [ELL(x, y, d, d, fill=(14, 14, 16))]
    els += [ELL(x + k, y + k, d - 2 * k, d - 2 * k, outline=(44, 44, 48), width=2) for k in range(24, d // 2 - 130, 22)]
    els += [P(slot, x + d / 2 - 120, y + d / 2 - 120, 240, 240, shape='circle'), ELL(x + d / 2 - 10, y + d / 2 - 10, 20, 20, fill=(14, 14, 16))]
    return els


add(T('w_vinyl', 'Trip soundtrack', 'Fun & story',
      'The trip as an album: a sleeve with the record sliding out, a side-A tracklist where songs are places, and a slide per track.',
      'Canva December photo-dump record, music ephemera', ('seventies', 0.55),
      {'cover': K('Sleeve + record', ['Sleeve photo', 'Label photo'], [('title', 'Album title', 'Summer\nin Portugal'), ('artist', 'Artist line', '@yourname · 2026')],
                  [*record(400, 200), P(0, 70, 200, 720, 720, shadow=140, sblur=20), tx('title', 90, 960, COOPER, 96, WHITE, anchor='lt', lh=0.95),
                   tx('artist', 94, 1180, MONO, 28, VA, anchor='lt')], bg=VB),
       'tracks': K('Tracklist', ['Small photo'], [('side', 'Side', 'Side A')] + [(f'tr{i}', f'Track {i}', t) for i, t in enumerate(
           ['Lisbon (4 days)', 'Sintra in the fog', 'Porto, slowly', 'The Douro line', 'Lagos sunsets', 'Home (bonus track)'], 1)],
                  [tx('side', 70, 80, COOPER, 90, VA, anchor='lt'), P(0, 760, 90, 250, 250, shape='circle'),
                   *[e for i in range(6) for e in (st(f'{i + 1:02d}', 70, 360 + i * 140, MONO_B, 34, VA, anchor='lt'),
                                                   tx(f'tr{i + 1}', 160, 356 + i * 140, SANS_SB, 44, WHITE, anchor='lt'),
                                                   LN([(70, 450 + i * 140), (1010, 450 + i * 140)], color=(60, 58, 62), width=2))]], bg=VB),
       'track': K('Track', ['Photo'], [('num', 'Track', 'Track 02'), ('name', 'Name', 'Sintra in the fog'), ('line', 'Line', 'the castle came out at noon')],
                 [P(0, 0, 0, W, 900), tx('num', 70, 960, MONO_B, 30, VA, anchor='lt', case='upper'), tx('name', 70, 1010, COOPER, 80, WHITE, anchor='lt'),
                  tx('line', 70, 1120, SERIF_I, 38, (200, 196, 190), anchor='lt')], bg=VB)},
      ['cover', 'tracks', 'track', ('track', {'num': 'Track 05', 'name': 'Lagos sunsets', 'line': 'every evening, the same cliff'}), 'tracks'], grain=4))

# ------------------------------------------------------------------ 16. Swiss grid
SW_BG, SW_R = (240, 240, 236), (226, 32, 40)
add(T('w_swiss_grid', 'Swiss grid', 'Bold type & posters',
      'International-style layouts: a strict grid, flush-left grotesque type, big red numbers, thin rules and asymmetric photos.',
      'Swiss tourism posters, Minimal Swiss Mountains Poster', ('crisp', 0.5),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'Europe\n2026'), ('sub', 'Line', 'Twelve places, one rail pass'), ('no', 'Edition', 'Nr. 1')],
                  [RC(60, 60, 120, 120, SW_R), tx('no', 200, 120, BAHN_SB, 30, INK, anchor='lm'),
                   tx('title', 56, 230, BAHN_SB, 190, INK, anchor='lt', lh=0.9), tx('sub', 60, 640, BAHN, 34, INK, anchor='lt'),
                   LN([(60, 720), (1020, 720)], color=INK, width=3), P(0, 420, 760, 600, 530)], bg=SW_BG),
       'chapter': K('Chapter', ['Photo'], [('num', 'Number', '01'), ('place', 'Place', 'Zermatt'), ('txt', 'Text', 'Car-free village under the Matterhorn. Arrive by train, leave by train.')],
                    [tx('num', 50, 30, BAHN_SB, 320, SW_R, anchor='lt'), tx('place', 60, 430, BAHN_SB, 84, INK, anchor='lt'),
                     LN([(60, 560), (500, 560)], color=INK, width=3), tx('txt', 60, 590, BAHN, 32, INK, anchor='lt', wrap=420, lh=1.35),
                     P(0, 540, 180, 480, 1100), st('{no} / {of}', 60, 1290, BAHN, 22, INK, anchor='lb')], bg=SW_BG),
       'data': K('Data', [], [('head', 'Heading', 'In numbers')] + [f for i, (n, l) in enumerate([('12', 'places'), ('2,840', 'km by train'), ('21', 'days'), ('0', 'flights')], 1)
                                                                    for f in ((f'n{i}', f'Number {i}', n), (f'l{i}', f'Label {i}', l))],
                 [tx('head', 60, 70, BAHN_SB, 64, INK, anchor='lt'), RC(960, 70, 60, 60, SW_R),
                  *[e for i in range(4) for e in (LN([(60, 230 + i * 270), (1020, 230 + i * 270)], color=INK, width=2),
                                                  tx(f'n{i + 1}', 60, 250 + i * 270, BAHN_SB, 170, INK, anchor='lt'),
                                                  tx(f'l{i + 1}', 1020, 400 + i * 270, BAHN, 34, SW_R, anchor='rb'))]], bg=SW_BG)},
      ['cover', 'chapter', ('chapter', {'num': '02', 'place': 'Lucerne', 'txt': 'Wooden bridges, a lake, and the boat to the mountains.'}),
       ('chapter', {'num': '03', 'place': 'Lausanne', 'txt': 'Steep streets down to the water. The metro climbs for you.'}), 'data']))

# ------------------------------------------------------------------ 17. Bauhaus shapes
BH_R, BH_Y, BH_B, BH_K, BH_BG = (214, 48, 40), (240, 190, 30), (30, 70, 160), (24, 24, 24), (240, 234, 220)
add(T('w_bauhaus', 'Bauhaus shapes', 'Collage & experimental',
      'Primary-colour circles, triangles and squares with photos cut into circles and heavy black capitals.',
      'Bauhaus graphics, Places by Andrea Núñez', ('punchy', 0.45),
      {'cover': K('Cover', ['Circle photo'], [('title', 'Title', 'Form\nfollows\ntravel')],
                  [RC(0, 0, 540, 540, BH_R), dict(t='poly', pts=[(540, 0), (1080, 0), (1080, 540)], fill=BH_Y),
                   P(0, 160, 360, 760, 760, shape='circle'), RC(760, 1000, 320, 350, BH_B),
                   tx('title', 50, 56, BLACK, 92, BH_BG, anchor='lt', lh=0.9, case='upper', fit=470)], bg=BH_BG),
       'comp': K('Composition', ['Photo', 'Circle photo'], [('word', 'Word', 'Porto'), ('cap', 'Caption', 'bridges · tiles · port')],
                 [ELL(560, -200, 700, 700, fill=BH_Y), P(0, 60, 200, 560, 760), dict(t='poly', pts=[(560, 1350), (1080, 760), (1080, 1350)], fill=BH_R),
                  P(1, 640, 420, 360, 360, shape='circle'), tx('word', 60, 1000, BLACK, 150, BH_K, anchor='lt', case='upper'),
                  tx('cap', 64, 1196, MONO, 28, BH_B, anchor='lt')], bg=BH_BG),
       'grid': K('Grid', ['Photo 1', 'Photo 2'], [('word', 'Word', 'Lisboa')],
                 [P(0, 0, 0, 540, 675), RC(540, 0, 540, 675, BH_B), ELL(620, 80, 380, 380, fill=BH_Y), RC(0, 675, 540, 675, BH_R),
                  P(1, 540, 675, 540, 675, shape='circle'), tx('word', 270, 1012, BLACK, 110, BH_BG, anchor='mm', case='upper', fit=480)], bg=BH_BG)},
      ['cover', 'comp', 'grid', ('comp', {'word': 'Sintra', 'cap': 'palaces · fog · ferns'}), 'grid']))

# ------------------------------------------------------------------ 18. Moodboard
MB = (246, 244, 240)


def pin(x, y, c=(214, 58, 46)):
    return ELL(x - 12, y - 12, 24, 24, fill=c)


add(T('w_moodboard', 'Moodboard', 'Grids & photo dumps',
      'A masonry moodboard of rounded photos with pins, a palette pulled from the first photo and a row of keyword chips.',
      'Pinterest boards, Savee photo moods, Cosmos collections', ('softlight', 0.5),
      {'board': K('Board', [f'Photo {i}' for i in range(1, 7)], [('title', 'Title', 'Lisbon, a moodboard')],
                  [tx('title', 60, 60, SERIF_I, 60, INK, anchor='lt'),
                   P(0, 60, 170, 310, 420, radius=14), P(1, 385, 170, 310, 300, radius=14), P(2, 710, 170, 310, 480, radius=14),
                   P(3, 60, 605, 310, 360, radius=14), P(4, 385, 485, 310, 480, radius=14), P(5, 710, 665, 310, 300, radius=14),
                   *[pin(x, y) for x, y in ((215, 186), (540, 186), (865, 186), (215, 621), (540, 501), (865, 681))],
                   dict(t='swatch', slot=0, rect=(60, 1010, 960, 160), color=MUTED)], bg=MB),
       'words': K('Keywords', ['Photo'], [('title', 'Title', 'The feeling')] + [(f'k{i}', f'Keyword {i}', k) for i, k in enumerate(
           ['sun on tiles', 'slow mornings', 'yellow trams', 'salt air', 'fado at night', 'pastel façades', 'river light'], 1)],
                  [tx('title', 60, 60, SERIF_I, 60, INK, anchor='lt'), P(0, 60, 170, 960, 640, radius=18), pin(540, 186),
                   dict(t='chips', fields=[f'k{i}' for i in range(1, 8)], xy=(60, 860), font=SANS_SB, size=32, color=INK, maxw=960,
                        fills=[(250, 226, 200), (210, 228, 240), (240, 214, 220), (222, 236, 214), (246, 236, 190)])], bg=MB)},
      ['board', 'words', ('board', {'title': 'Porto, a moodboard'})]))

# ------------------------------------------------------------------ 19. Notes app
NOTE_Y = (226, 160, 20)
add(T('w_notes_app', 'Notes app list', 'Fun & story',
      'Travel tips as a phone note: a yellow back arrow, bold title, date and a ticked checklist — familiar and very saveable.',
      'Notes-to-self travel posts, Canva UX/UI recap', ('natural', 0.5),
      {'note': K('Checklist note', [], [('title', 'Title', 'Lisbon tips'), ('date', 'Date line', '24 October 2026 at 09:41')] + [(f'l{i}', f'Item {i}', s) for i, s in enumerate(
          ['Buy a Viva Viagem card at the metro', 'Tram 28 before 9 am', 'Pastéis de nata: Manteigaria', 'Sunset at Senhora do Monte', 'Pack shoes with grip (hills!)', 'Book Belém tower online'], 1)],
                 [st('‹ Notes', 50, 70, SANS_SB, 40, NOTE_Y, anchor='lt'), st('•••', 1030, 70, SANS_SB, 36, NOTE_Y, anchor='rt'),
                  tx('date', 540, 170, SANS, 26, (150, 150, 150), anchor='mt'), tx('title', 60, 230, SANS_SB, 76, INK, anchor='lt'),
                  *[e for i in range(6) for e in (st('☑' if i < 3 else '☐', 60, 380 + i * 140, SYM, 50, NOTE_Y if i < 3 else (170, 170, 170), anchor='lt'),
                                                  tx(f'l{i + 1}', 140, 386 + i * 140, SANS, 40, INK if i >= 3 else (150, 150, 150), anchor='lt', wrap=880))]], bg=(252, 252, 250)),
       'photo': K('Note with photo', ['Photo'], [('title', 'Title', 'Day 3'), ('body', 'Text', 'Took the train to Sintra. Fog until noon, then the palace came out of the clouds. Worth it.')],
                  [st('‹ Notes', 50, 70, SANS_SB, 40, NOTE_Y, anchor='lt'), tx('title', 60, 170, SANS_SB, 76, INK, anchor='lt'),
                   tx('body', 60, 290, SANS, 38, INK, anchor='lt', wrap=960, lh=1.35), P(0, 60, 560, 960, 700, radius=22)], bg=(252, 252, 250))},
      ['note', 'photo', ('photo', {'title': 'Day 5', 'body': 'Porto. Climbed the tower, ate a francesinha, regretted nothing.'}),
       ('note', {'title': 'Porto tips', 'l1': 'Andante card for the metro', 'l2': 'Livraria Lello: book ahead', 'l3': 'Port in Gaia, not in town',
                 'l4': 'Sunset at Jardim do Morro', 'l5': 'Bolhão market for lunch', 'l6': 'Bring a raincoat'})]))

# ------------------------------------------------------------------ 20. Food diary index cards
add(T('w_recipe_cards', 'Food diary cards', 'Fun & story',
      'Every meal on a ruled index card: dish, where, price and a star rating, with the photo taped above.',
      'Travel journal boards, Food diary', ('warm', 0.6),
      {'card': K('Index card', ['Photo'], [('dish', 'Dish', 'Bacalhau à Brás'), ('where', 'Where', 'Taberna da Rua das Flores'), ('price', 'Price', '€14'),
                                           ('stars', 'Rating', '★★★★☆'), ('note', 'Note', 'eggs, potatoes, cod. order two.')],
                [P(0, 250, 70, 580, 420, border=16, rot=3, shadow=90), TAPE(470, 52, rot=-4),
                 RC(80, 560, 920, 640, (252, 250, 244), radius=6, shadow=90, rot=-2),
                 *[LN([(110, 700 + i * 70), (970, 700 + i * 70 - 30)], color=(150, 180, 220), width=2) for i in range(7)],
                 LN([(110, 640), (970, 610)], color=(220, 80, 80), width=3),
                 tx('dish', 120, 588, HAND, 62, INK, anchor='lt', rot=-2), tx('where', 124, 690, HAND, 40, (60, 60, 120), anchor='lt', rot=-2),
                 tx('price', 960, 600, HAND, 56, (200, 60, 50), anchor='rt', rot=-2), st('{no}', 960, 1140, MONO, 22, MUTED, anchor='rb'),
                 tx('stars', 124, 780, SYM, 52, (230, 160, 40), anchor='lt', rot=-2), tx('note', 124, 880, HAND, 44, INK, anchor='lt', wrap=820, rot=-2)])},
      ['card', ('card', {'dish': 'Pastel de nata', 'where': 'Manteigaria, Chiado', 'price': '€1.30', 'stars': '★★★★★', 'note': 'warm. cinnamon. a second one.'}),
       ('card', {'dish': 'Francesinha', 'where': 'Café Santiago, Porto', 'price': '€12', 'stars': '★★★★☆', 'note': 'a sandwich in a sauce. nap after.'}),
       ('card', {'dish': 'Grilled sardines', 'where': 'a stall in Alfama', 'price': '€8', 'stars': '★★★★★', 'note': 'on bread, with your hands.'})],
      bg=('paper', (196, 166, 130)), grain=4))

# ------------------------------------------------------------------ 21. Travel bingo
BG_BINGO, BINGO_R = (250, 240, 220), (214, 58, 46)
BCELL = [('photo', 0), ('text', 'saw a castle'), ('photo', 1), ('text', 'missed a train'), ('photo', 2), ('text', 'ate 3 desserts'), ('photo', 3), ('text', 'got lost'), ('photo', 4)]
add(T('w_bingo', 'Travel bingo', 'Fun & story',
      'A 3×3 bingo card of trip moments: photo squares and text squares stamped with red dabs, a BINGO! sticker and proof slides.',
      'Fun & story formats, Canva playful photo dumps', ('vivid', 0.45),
      {'card': K('Bingo card', [f'Photo {i}' for i in range(1, 6)], [('title', 'Title', 'Europe bingo')] + [(f'b{i}', f'Square {i}', t) for i, (_, t) in
                                                                                                        enumerate([c for c in BCELL if c[0] == 'text'], 1)],
                 [tx('title', 540, 50, COOPER, 100, BINGO_R, anchor='mt', case='upper'),
                  *[e for i, (kind, v) in enumerate(BCELL) for e in (
                      (P(v, 60 + (i % 3) * 325, 220 + (i // 3) * 340, 310, 320, radius=10),) if kind == 'photo' else
                      (RC(60 + (i % 3) * 325, 220 + (i // 3) * 340, 310, 320, WHITE, radius=10),
                       tx(f'b{[c for c in BCELL if c[0] == "text"].index((kind, v)) + 1}', 215 + (i % 3) * 325, 380 + (i // 3) * 340, COOPER, 40, INK, anchor='mm', wrap=260, valign='middle'),
                       ELL(130 + (i % 3) * 325, 300 + (i // 3) * 340, 170, 170, fill=BINGO_R, alpha=110)))],
                  BADGE(900, 1220, 110, 'BINGO! · BINGO! · ', COOPER, 26, WHITE, fill=BINGO_R, ring=False, center='★', cfont=SYM, csize=70, rot=-12)], bg=BG_BINGO),
       'proof': K('Proof', ['Photo'], [('claim', 'Square', 'saw a castle'), ('note', 'Note', 'Pena Palace, Sintra. It was also yellow.')],
                  [P(0, 0, 0, W, 980), RC(0, 980, W, 370, BG_BINGO), st('✓', 60, 1026, SYM, 72, BINGO_R, anchor='lt'),
                   tx('claim', 150, 1030, COOPER, 72, BINGO_R, anchor='lt', fit=870),
                   tx('note', 60, 1140, SANS, 36, INK, anchor='lt', wrap=960)])},
      ['card', 'proof', ('proof', {'claim': 'missed a train', 'note': 'Porto São Bento. Got the next one. Ate a tart.'}), ('proof', {'claim': 'got lost', 'note': 'Alfama. On purpose, mostly.'})]))

# ------------------------------------------------------------------ 22. Negative to positive
FBASE = (196, 112, 58)
add(T('w_negative', 'Negative to positive', 'Film & analog',
      'Colour negatives on orange film base that "develop" into positives: a strip of three negatives, then each frame half negative, half print.',
      'Contact Sheet, film zines', ('warmfilm', 0.6),
      {'cover': K('Negative strip', ['Frame 1', 'Frame 2', 'Frame 3'], [('title', 'Title', 'Developing…'), ('roll', 'Roll line', 'ROLL 07 · C-41 · 36 EXP')],
                  [RC(0, 300, W, 560, FBASE), dict(t='film', rect=(0, 300, W, 560), hole=(22, 18, 16)),
                   P(0, 30, 370, 330, 420, negative=True), P(1, 375, 370, 330, 420, negative=True), P(2, 720, 370, 330, 420, negative=True),
                   tx('title', 60, 960, COND, 120, (240, 220, 200), anchor='lt'), tx('roll', 64, 1110, MONO, 28, FBASE, anchor='lt')], bg=(22, 18, 16)),
       'half': K('Negative + print', ['Photo'], [('fr', 'Frame', '14'), ('cap', 'Caption', 'Sintra, before and after the lab')],
                 [P(0, 60, 80, 960, 540, negative=True), P(0, 60, 650, 960, 540), tx('fr', 60, 1230, MONO_B, 28, FBASE, anchor='lt'),
                  tx('cap', 160, 1232, MONO, 28, (230, 224, 210), anchor='lt')], bg=(22, 18, 16)),
       'print': K('Print', ['Photo'], [('fr', 'Frame', '15')], [P(0, 60, 60, 960, 1180, border=24, bcolor=(246, 242, 232)), tx('fr', 1020, 1290, MONO_B, 26, FBASE, anchor='rb')],
                  bg=(22, 18, 16))},
      ['cover', 'half', 'print', ('half', {'fr': '21', 'cap': 'Lisbon, negative then print'}), 'print'], grain=6))

# ------------------------------------------------------------------ 23. Instax wide
INSTAX_BG = {'peach': (246, 214, 196), 'sky': (204, 224, 240), 'sage': (210, 224, 204)}


def instax(name):
    bgc = INSTAX_BG[name]
    return K(f'Two instants ({name})', ['Top photo', 'Bottom photo'], [('c1', 'Caption 1', 'porto, golden'), ('c2', 'Caption 2', 'the bridge again')],
             [P(0, 110, 100, 820, 480, border=34, pb=74, bcolor=(252, 252, 250), rot=-3, shadow=90), tx('c1', 520, 628, HAND, 44, INK, anchor='mt', rot=-3),
              P(1, 150, 740, 820, 480, border=34, pb=74, bcolor=(252, 252, 250), rot=2, shadow=90), tx('c2', 560, 1268, HAND, 44, INK, anchor='mt', rot=2)], bg=bgc)


add(T('w_instax', 'Instant wide', 'Scrapbook & polaroid',
      'Wide instant-film prints, two per slide, tilted with marker captions on soft pastel grounds.',
      'Taped polaroids, instant photo boards', ('instant', 0.6),
      {f'i_{n}': instax(n) for n in INSTAX_BG},
      ['i_peach', ('i_sky', {'c1': 'lisbon, 7am', 'c2': 'the 28, of course'}), ('i_sage', {'c1': 'sintra, fog', 'c2': 'and then sun'}), 'i_peach']))

# ------------------------------------------------------------------ 24. Trip dashboard
DB, DCARD, DACC = (16, 20, 28), (30, 36, 48), (110, 200, 255)


def card(x, y, w, h):
    return RC(x, y, w, h, DCARD, radius=26)


add(T('w_dashboard', 'Trip dashboard', 'Fun & story',
      'The trip as an app dashboard: dark cards with big stats, a steps-per-day line chart and a favourites card.',
      'Canva UX/UI travel recap, trip-in-numbers', ('cinematic', 0.5),
      {'dash': K('Dashboard', ['Photo'], [('title', 'Title', 'Trip summary'), ('n1', 'Stat 1', '21'), ('l1', 'Label 1', 'days'), ('n2', 'Stat 2', '312 km'), ('l2', 'Label 2', 'walked'),
                                          ('steps', 'Steps per day (thousands)', '12, 18, 9, 22, 15, 26, 11, 19, 24, 14'), ('fav', 'Favourite', 'Sintra, day 9')],
                 [tx('title', 60, 70, SANS_SB, 60, WHITE, anchor='lt'), card(60, 180, 465, 260), card(555, 180, 465, 260),
                  tx('n1', 100, 220, SANS_SB, 110, WHITE, anchor='lt'), tx('l1', 100, 370, SANS, 30, (150, 160, 180), anchor='lt'),
                  tx('n2', 595, 220, SANS_SB, 96, DACC, anchor='lt'), tx('l2', 595, 370, SANS, 30, (150, 160, 180), anchor='lt'),
                  card(60, 470, 960, 380), st('Steps per day', 100, 505, SANS_SB, 30, (150, 160, 180), anchor='lt'),
                  dict(t='profile', field='steps', rect=(100, 620, 880, 190), color=DACC, tcolor=WHITE, label='{:.0f}k'),
                  card(60, 880, 960, 400), P(0, 90, 910, 340, 340, radius=18), st('Favourite moment', 470, 940, SANS, 28, (150, 160, 180), anchor='lt'),
                  tx('fav', 470, 990, SANS_SB, 50, WHITE, anchor='lt', wrap=520)], bg=DB),
       'detail': K('Day card', ['Photo'], [('day', 'Day', 'Day 9 · Sintra'), ('n', 'Stat', '26,412 steps'), ('note', 'Note', 'Pena Palace, the Moorish castle and the long way down.')],
                   [P(0, 0, 0, W, 760), card(60, 700, 960, 560), tx('day', 100, 740, SANS, 30, (150, 160, 180), anchor='lt'),
                    tx('n', 100, 790, SANS_SB, 96, DACC, anchor='lt'), tx('note', 100, 930, SANS, 36, WHITE, anchor='lt', wrap=880, lh=1.35)], bg=DB)},
      ['dash', 'detail', ('detail', {'day': 'Day 14 · Porto', 'n': '22,980 steps', 'note': 'Clérigos tower, both bridges and a long lunch.'})]))

# ------------------------------------------------------------------ 25. Calendar month
CAL_BG, CAL_R = (247, 244, 238), (214, 58, 46)
CAL_PHOTO_DAYS = {4: 0, 9: 1, 12: 2, 17: 3, 22: 4, 27: 5}


def cal_els():
    els = [tx('month', 60, 50, COND, 150, INK, anchor='lt', case='upper'), tx('year', 1020, 120, MONO, 30, CAL_R, anchor='rm')]
    for i, d in enumerate(['M', 'T', 'W', 'T', 'F', 'S', 'S']):
        els.append(st(d, 60 + i * 140 + 65, 250, MONO_B, 24, MUTED, anchor='mt'))
    start = 2                         # the 1st falls on a Wednesday
    for day in range(1, 32):
        c, r = (start + day - 1) % 7, (start + day - 1) // 7
        x, y = 60 + c * 140, 300 + r * 190
        if day in CAL_PHOTO_DAYS:
            els += [P(CAL_PHOTO_DAYS[day], x + 4, y + 4, 132, 182, radius=8), st(str(day), x + 14, y + 12, MONO_B, 22, WHITE, anchor='lt', shadow=160)]
        else:
            els += [st(str(day), x + 14, y + 12, MONO, 24, INK, anchor='lt'), LN([(x + 4, y + 2), (x + 136, y + 2)], color=(220, 214, 204), width=2)]
    return els


add(T('w_calendar', 'Calendar month', 'Grids & photo dumps',
      'A month as a calendar: photos fill the days that mattered, the rest are plain numbers. Then a slide per photo day.',
      'Canva "August dump" calendar, photo-dump layouts', ('softlight', 0.5),
      {'month': K('Month', [f'Day photo {i}' for i in range(1, 7)], [('month', 'Month', 'October'), ('year', 'Year', '2026')], cal_els(), bg=CAL_BG),
       'day': K('Day', ['Photo'], [('date', 'Date', '09'), ('mon', 'Month', 'October'), ('note', 'Note', 'Sintra in the fog')],
                [tx('date', 60, 40, COND, 260, CAL_R, anchor='lt'), tx('mon', 64, 330, MONO, 30, INK, anchor='lt', case='upper'),
                 tx('note', 1020, 240, SERIF_I, 46, INK, anchor='rb', wrap=560), P(0, 60, 400, 960, 880, radius=12)], bg=CAL_BG)},
      ['month', 'day', ('day', {'date': '17', 'note': 'the night train south'}), ('day', {'date': '27', 'note': 'last swim of the year'})]))

# ------------------------------------------------------------------ 26. A–Z of a city
AZ_BG, AZ_ACC = (244, 238, 228), (36, 84, 160)
add(T('w_a_to_z', 'A–Z of a city', 'Editorial & magazine',
      'A city explained alphabetically: a giant letter, the word it stands for, a short definition and a photo — one letter per slide.',
      'The Travel Almanac, Ernest Journal', ('natural', 0.55),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'The A–Z\nof Lisbon'), ('sub', 'Line', '26 words for one city')],
                  [tx('title', 60, 70, SERIF_B, 130, INK, anchor='lt', lh=0.95), tx('sub', 64, 400, SERIF_I, 40, AZ_ACC, anchor='lt'), P(0, 60, 500, 960, 780)], bg=AZ_BG),
       'letter': K('Letter', ['Photo'], [('l', 'Letter', 'A'), ('word', 'Word', 'Azulejo'), ('def', 'Definition', 'The painted tiles on everything: churches, stations, bakeries, your hotel bathroom.')],
                   [tx('l', 40, -40, SERIF_B, 700, AZ_ACC, anchor='lt', alpha=60), st('IS FOR', 70, 660, GEO_B, 24, AZ_ACC, anchor='lt', track=8),
                    tx('word', 64, 700, SERIF_B, 96, INK, anchor='lt'), tx('def', 70, 840, SERIF_I, 34, INK, anchor='lt', wrap=380, lh=1.3),
                    P(0, 480, 180, 540, 1060)], bg=AZ_BG)},
      ['cover', 'letter', ('letter', {'l': 'B', 'word': 'Bica', 'def': 'A short, strong coffee. Drink it standing at the counter.'}),
       ('letter', {'l': 'F', 'word': 'Fado', 'def': 'Sad, beautiful songs in small rooms. Arrive late, stay quiet.'}),
       ('letter', {'l': 'M', 'word': 'Miradouro', 'def': 'A viewpoint. The city has dozens; each one wins.'}),
       ('letter', {'l': 'T', 'word': 'Tram', 'def': 'Yellow, wooden, squealing up impossible hills.'})], grain=2))

# ------------------------------------------------------------------ 27. Washi line (seamless)
LINE_Y, LINE_Y2 = 150, 760


def hang(slot, x, rot, cap, ly=LINE_Y):
    return [RC(x + 150, ly - 22, 26, 70, (196, 160, 110), radius=4, z=2),
            P(slot, x, ly + 20, 330, 360, border=18, pb=70, rot=rot, shadow=90, z=1), tx(cap, x + 180, ly + 410, HAND, 36, INK, anchor='mt', rot=rot, z=2)]


def string(ly):
    return LN([(0, ly), (540, ly + 40), (W, ly)], color=(120, 100, 80), width=3, z=1)


add(T('w_washi_line', 'Photos on a line (seamless)', 'Scrapbook & polaroid',
      'Polaroids pegged to one string that sags across every slide of the carousel, each with a handwritten caption.',
      'Scrapbook boards, SCRL seamless', ('instant', 0.55),
      {'cover': K('Cover', ['Photo 1', 'Photo 2'], [('title', 'Title', 'hung out\nto dry'), ('c1', 'Caption 1', 'lisbon'), ('c2', 'Caption 2', 'sintra')],
                  [string(LINE_Y), string(LINE_Y2), *hang(0, 90, -4, 'c1'), *hang(1, 620, 3, 'c2', LINE_Y2),
                   tx('title', 80, 900, HAND, 110, INK, anchor='lt', lh=1.0, rot=-3, z=2)]),
       'line': K('Two lines', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4'], [('c1', 'Caption 1', 'porto'), ('c2', 'Caption 2', 'the river'),
                                                                           ('c3', 'Caption 3', 'tiles'), ('c4', 'Caption 4', 'bridge')],
                 [string(LINE_Y), string(LINE_Y2), *hang(0, 90, 3, 'c1'), *hang(1, 620, -3, 'c2'),
                  *hang(2, 120, -2, 'c3', LINE_Y2), *hang(3, 640, 4, 'c4', LINE_Y2)])},
      ['cover', 'line', ('line', {'c1': 'lagos', 'c2': 'cliffs', 'c3': 'boats', 'c4': 'sunset'}), ('line', {'c1': 'faro', 'c2': 'home soon', 'c3': 'last swim', 'c4': 'bye'})],
      strip=True, bg=('paper', (238, 232, 222)), grain=3))

# ------------------------------------------------------------------ 28. Countdown
CD_BG, CD_ACC = (20, 20, 22), (255, 196, 60)
add(T('w_countdown', 'Countdown', 'Bold type & posters',
      'A top-list told backwards: each slide has a giant outlined number behind the photo, the place and one reason.',
      'Big-word posters, Poster Type', ('cinematic', 0.6),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', '5 places\nI’d go\nback to'), ('sub', 'Line', 'counting down →')],
                  [P(0, 0, 0, W, H, dim=0.35), tx('title', 60, 520, COND, 170, WHITE, anchor='lt', lh=0.88, case='upper', shadow=80),
                   tx('sub', 64, 1240, MONO, 30, CD_ACC, anchor='lt')]),
       'num': K('Number', ['Photo'], [('n', 'Number', '05'), ('place', 'Place', 'Lagos'), ('why', 'Reason', 'cliffs, coves and the best sunsets of the trip')],
                [tx('n', 540, -40, COND, 760, CD_ACC, anchor='mt', outline=True, stroke=5, shadow=0), P(0, 120, 600, 840, 470, shadow=150, sblur=20),
                 tx('place', 120, 1100, COND, 100, WHITE, anchor='lt', case='upper'), tx('why', 124, 1222, SANS, 32, (200, 200, 200), anchor='lt', wrap=840)], bg=CD_BG)},
      ['cover', ('num', {'n': '05'}), ('num', {'n': '04', 'place': 'Porto', 'why': 'the river, the bridges, the wine cellars'}),
       ('num', {'n': '03', 'place': 'Sintra', 'why': 'fog, palaces and fern forests'}), ('num', {'n': '02', 'place': 'Évora', 'why': 'Roman temple, empty streets, slow lunches'}),
       ('num', {'n': '01', 'place': 'Lisbon', 'why': 'everything, honestly'})], grain=4))

# ------------------------------------------------------------------ 29. Letters home
LETTER = (250, 246, 236)
add(T('w_letters_home', 'Letters home', 'Vintage & postcards',
      'A handwritten letter on ruled paper with a taped photo, and an airmail envelope with stamps and a postmark.',
      'Greetings-from postcards, travel journals', ('vintage', 0.55),
      {'envelope': K('Envelope', ['Stamp photo'], [('to', 'Address', 'To Ma & Pa\nThe kitchen table\nHome'), ('from', 'Back line', 'par avion')],
                     [RC(70, 290, 940, 640, LETTER, radius=8, shadow=100),
                      *[RC(70 + i * 47, 290, 24, 16, (190, 40, 50) if i % 2 else (40, 70, 160)) for i in range(20)],
                      *[RC(70 + i * 47, 914, 24, 16, (190, 40, 50) if i % 2 else (40, 70, 160)) for i in range(20)],
                      P(0, 840, 340, 130, 160, shape='stamp', border=8, bcolor=WHITE), STAMP(800, 440, 70, 'AIRMAIL · 2026', (40, 40, 60), rot=-12),
                      WAVES(560, 360, 220, 80, (60, 60, 80), n=4, width=4, alpha=180), tx('to', 360, 560, HAND, 50, (40, 42, 62), anchor='lt', lh=1.2),
                      tx('from', 120, 360, SCRIPT, 54, (190, 40, 50), anchor='lt', rot=-6)], bg=('paper', (214, 200, 176))),
       'letter': K('Letter', ['Photo'], [('date', 'Date', 'Lisbon, 9 Oct'), ('greet', 'Greeting', 'Dear Ma,'),
                                         ('body', 'Letter', 'The city is all hills and tiles. We take the tram up and walk down. I have eaten more custard tarts than I will admit. Weather perfect, feet tired. Back soon.'),
                                         ('sign', 'Sign-off', 'love, me x')],
                  [RC(60, 60, 960, 1230, LETTER, radius=4, shadow=80), *[LN([(100, 330 + i * 70), (980, 330 + i * 70)], color=(190, 204, 226), width=2) for i in range(13)],
                   tx('date', 980, 120, HAND, 40, (40, 42, 62), anchor='rt'), tx('greet', 110, 200, HAND, 60, (40, 42, 62), anchor='lt'),
                   tx('body', 110, 284, HAND, 42, (40, 42, 62), anchor='lt', wrap=560, lh=1.67), P(0, 700, 300, 280, 340, border=12, rot=5, shadow=70), TAPE(760, 282, 130, 40, rot=8),
                   tx('sign', 980, 1180, HAND, 54, (40, 42, 62), anchor='rt', rot=-3)], bg=('paper', (214, 200, 176)))},
      ['envelope', 'letter', ('letter', {'date': 'Porto, 15 Oct', 'body': 'Rain today, so we hid in a bookshop and then a café and then another café. The river looks like tea. Tomorrow: the train along the valley.'}),
       'envelope'], grain=4))

# ------------------------------------------------------------------ 30. Disposable camera date stamp
DS_Y, DS_O = (250, 204, 40), (255, 140, 40)
add(T('w_datestamp', 'Disposable camera', 'Film & analog',
      'Single-use camera nostalgia: a yellow camera-box cover, then flash photos with the glowing orange date stamp in the corner.',
      'Travel film photography, LOOKSLIKEFILM', ('expired', 0.65),
      {'box': K('Camera box cover', ['Window photo'], [('title', 'Title', 'Single use'), ('exp', 'Box line', '27 EXP · ISO 400 · FLASH'), ('date', 'Date stamp', "'26 10 09")],
                 [RC(0, 0, W, 160, (20, 20, 20)), st('⚡', 960, 80, SYM, 80, DS_Y, anchor='mm'), tx('title', 60, 200, COND, 200, (20, 20, 20), anchor='lt', case='upper'),
                  tx('exp', 64, 430, MONO_B, 34, (20, 20, 20), anchor='lt'), P(0, 60, 520, 960, 700, radius=24, border=14, bcolor=(20, 20, 20)),
                  tx('date', 990, 1180, MONO_B, 54, DS_O, anchor='rb', shadow=220, sblur=6, scol=DS_O)], bg=DS_Y),
       'shot': K('Flash photo', ['Photo'], [('date', 'Date stamp', "'26 10 09")],
                 [P(0, 0, 0, W, H), tx('date', 1010, 1290, MONO_B, 58, DS_O, anchor='rb', shadow=220, sblur=6, scol=DS_O)]),
       'two': K('Two shots', ['Top', 'Bottom'], [('d1', 'Date 1', "'26 10 12"), ('d2', 'Date 2', "'26 10 13")],
                [P(0, 0, 0, W, 670), P(1, 0, 680, W, 670), tx('d1', 1010, 640, MONO_B, 48, DS_O, anchor='rb', shadow=220, sblur=6, scol=DS_O),
                 tx('d2', 1010, 1320, MONO_B, 48, DS_O, anchor='rb', shadow=220, sblur=6, scol=DS_O)], bg=(10, 10, 10))},
      ['box', 'shot', 'two', ('shot', {'date': "'26 10 17"}), ('two', {'d1': "'26 10 20", 'd2': "'26 10 21"})], grain=9))
