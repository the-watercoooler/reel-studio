"""Carousel templates built from the 11 design systems in Carousels\\Inspiration library (24 Nov 2026).

One template family per system: Broadsheet, Still Frame, Quiet Journal, Greetings From, Cut & Tape (ticket diary),
Contact Sheet, Field Guide, Panorama Run (giant word), Poster Type, Expedition and Cut-up (riso).
Each uses the moves listed for its system in the library; fonts are the ones on this PC.
"""
from carousel_templates import P, RC, LN, SHADE, TAPE, K, W, H
from carousel_templates_pro import (T as _T, tx, st, PILL, SPARK, BADGE, WAVES, ELL, TORN, STAMP, FRAME,
                                    SERIF, SERIF_SB, SERIF_B, SERIF_I, COOPER, COND, COND_SB, GEO, GEO_B, BLACK,
                                    SCRIPT, HAND, SANS, SANS_SB, SYM, WHITE, INK, MUTED)

MONO, IMPACT, GARA = 'consola.ttf', 'impact.ttf', 'GARA.TTF'
G = 'Design systems'
HANDLE = ('g_handle', 'Your @handle', '@yourname')
TEMPLATES = []
add = TEMPLATES.append


def T(key, label, about, ref, look, kinds, default, **kw):
    return _T(key, label, G, about, 'Inspiration library · ' + ref, look, kinds, default, **kw)


# ================================================================== 1. Broadsheet (editorial & magazine)
NEWS, RED_N, MUT_N = (241, 238, 230), (176, 30, 36), (112, 106, 98)


def folio(col=INK):
    return [LN([(60, 1272), (1020, 1272)], color=col, width=2),
            st('{no}', 60, 1290, GEO_B, 18, col, anchor='lt', track=3),
            tx('g_mast', 540, 1290, GEO_B, 18, col, anchor='mt', track=6, case='upper'),
            tx('g_date', 1020, 1290, GEO_B, 18, col, anchor='rt', track=3, case='upper')]


add(T('sys_broadsheet', 'Broadsheet feature',
      'A carousel that reads like a magazine feature: masthead cover, contents, feature pages with two text columns, a pull quote and a folio on every slide.',
      'Broadsheet (Condé Nast Traveller, Odyssey, The Travel Almanac)', ('natural', 0.6),
      {'cover': K('Cover', ['Cover photo'], [('g_mast', 'Masthead (every slide)', 'The Wanderer'), ('g_date', 'Issue line (every slide)', 'Summer 2026'),
                                              ('cap', 'Photo caption', 'The 7:40 to Porto, somewhere past Coimbra.'),
                                              ('head', 'Headline', 'Three weeks, one rail pass, no plan at all'),
                                              ('deck', 'Standfirst', 'How we crossed the continent slowly, and why we would do it again.')],
                  [tx('g_mast', 540, 38, SERIF_B, 170, INK, anchor='mt', fit=980, case='upper'),
                   LN([(60, 214), (1020, 214)], color=INK, width=5), LN([(60, 226), (1020, 226)], color=INK, width=1),
                   st('No. 07', 60, 240, GEO_B, 20, INK, anchor='lt', track=4), tx('g_date', 540, 240, GEO_B, 20, INK, anchor='mt', track=6, case='upper'),
                   st('EUROPE EDITION', 1020, 240, GEO_B, 20, INK, anchor='rt', track=4), LN([(60, 278), (1020, 278)], color=INK, width=1),
                   P(0, 60, 300, 960, 600), tx('cap', 60, 912, SERIF_I, 22, MUT_N, anchor='lt', wrap=960),
                   tx('head', 60, 956, SERIF_B, 74, INK, anchor='lt', wrap=960, lh=1.02),
                   tx('deck', 60, 1140, SERIF_I, 31, MUT_N, anchor='lt', wrap=960, lh=1.3), *folio()]),
       'contents': K('Contents', ['Photo strip'], [(f'c{i}', f'Story {i}', s) for i, s in enumerate(
           ['The night train to Vienna', 'Lisbon, slowly', 'Ten bakeries, ranked', 'Lake Bled at 6 a.m.', 'What we would skip next time'], 1)],
           [st('In this issue', 60, 84, SERIF_B, 84, INK, anchor='lt'), LN([(60, 206), (1020, 206)], color=INK, width=3),
            *[e for i in range(5) for e in (st(f'{i + 1:02d}', 60, 250 + i * 196, SERIF_B, 70, RED_N, anchor='lt'),
                                             tx(f'c{i + 1}', 180, 262 + i * 196, SERIF, 38, INK, anchor='lt', wrap=560, lh=1.15),
                                             LN([(60, 422 + i * 196), (760, 422 + i * 196)], color=(190, 184, 172), width=1))],
            P(0, 800, 250, 220, 990), *folio()]),
       'feature': K('Feature page', ['Photo'], [('kicker', 'Section', 'Dispatch — Portugal'), ('cap', 'Caption', 'Tram 28 at the top of Graça.'),
                                                ('head', 'Headline', 'Where the tram line ends'),
                                                ('b1', 'Column 1', 'We rode the old yellow tram to the end of the line, then kept walking. The streets narrowed, the tiles got older and the cafés got smaller.'),
                                                ('b2', 'Column 2', 'By noon we had found a bench with a view of the whole river. Nobody asked us to move. We stayed until the light went gold.')],
                    [tx('kicker', 60, 64, GEO_B, 20, RED_N, anchor='lt', track=6, case='upper'), P(0, 60, 104, 960, 600),
                     tx('cap', 60, 716, SERIF_I, 22, MUT_N, anchor='lt', wrap=960), tx('head', 60, 762, SERIF_B, 64, INK, anchor='lt', wrap=960, lh=1.02),
                     LN([(540, 930), (540, 1236)], color=(190, 184, 172), width=1),
                     tx('b1', 60, 930, GARA, 28, INK, anchor='lt', wrap=450, lh=1.42), tx('b2', 570, 930, GARA, 28, INK, anchor='lt', wrap=450, lh=1.42), *folio()]),
       'quote': K('Pull quote', ['Photo'], [('quote', 'Quote', 'Nobody in this town is in a hurry, and after a week, neither were we.'), ('who', 'Attribution', '— notes, day nine')],
                  [st('“', 48, 30, SERIF_B, 380, RED_N, anchor='lt'), tx('quote', 60, 380, SERIF_I, 74, INK, anchor='lt', wrap=940, lh=1.08),
                   tx('who', 60, 800, GEO_B, 22, MUT_N, anchor='lt', track=5, case='upper'), P(0, 620, 870, 400, 360), *folio()]),
       'end': K('Next issue', ['Photo'], [('next', 'Next issue', 'The Alps, by bus'), HANDLE],
                [st('NEXT ISSUE', 60, 110, GEO_B, 24, RED_N, anchor='lt', track=6), tx('next', 60, 156, SERIF_B, 110, INK, anchor='lt', wrap=960, lh=0.98),
                 LN([(60, 470), (1020, 470)], color=INK, width=3), st('WORDS & PICTURES', 60, 500, GEO_B, 20, MUT_N, anchor='lt', track=5),
                 tx('g_handle', 60, 534, SERIF, 46, INK, anchor='lt'), P(0, 60, 650, 960, 590), *folio()])},
      ['cover', 'contents', 'feature', 'quote', ('feature', {'kicker': 'Dispatch — Slovenia', 'head': 'Six in the morning at Lake Bled',
                                                              'cap': 'The church on the island, before the boats.'}), 'end'],
      bg=('paper', NEWS), grain=3))

# ================================================================== 2. Still Frame (cinematic)
SUB = (250, 242, 205)


def bars():
    return [RC(0, 0, W, 120, (0, 0, 0)), RC(0, H - 120, W, 120, (0, 0, 0))]


add(T('sys_still_frame', 'Still frame',
      'Every slide is a film still: letterbox bars, a timecode and frame count, real subtitle captions, an opening title card and closing credits.',
      'Still Frame (Lune, Alex Strohl, National Geographic)', ('cinematic', 0.75),
      {'title': K('Title card', ['Background still'], [('pre', 'Small line above', 'a film by @yourname'), ('title', 'Title', 'Lisboa'),
                                                       ('sub', 'Line below', 'nine frames from a slow week')],
                  [P(0, 0, 120, W, H - 240, dim=0.5), *bars(), tx('pre', 540, 520, GEO, 22, (215, 215, 215), anchor='mt', track=10, case='upper', shadow=120),
                   tx('title', 540, 566, SERIF, 128, WHITE, anchor='mt', track=8, shadow=140, sblur=10), tx('sub', 540, 740, SERIF_I, 36, (220, 220, 220), anchor='mt', shadow=120),
                   st('SWIPE  →', 540, H - 60, GEO, 18, (150, 150, 150), anchor='mm', track=8, shadow=0)]),
       'still': K('Still + subtitle', ['Still'], [('tc', 'Timecode', '00:14:07:12'), ('sub', 'Subtitle', 'I think we missed the last tram.')],
                  [P(0, 0, 120, W, H - 240), *bars(), tx('tc', 50, 60, MONO, 24, (190, 190, 190), anchor='lm'),
                   st('FRAME {no} / {of}', 1030, 60, MONO, 24, (190, 190, 190), anchor='rm'),
                   tx('sub', 540, H - 168, SANS_SB, 40, SUB, anchor='mb', wrap=900, lh=1.2, valign='bottom', shadow=255, sblur=3)]),
       'dialogue': K('Still + two lines', ['Still'], [('tc', 'Timecode', '00:31:52:04'), ('l1', 'Line 1', '— Where to next?'), ('l2', 'Line 2', '— Anywhere with a view.')],
                     [P(0, 0, 120, W, H - 240), *bars(), tx('tc', 50, 60, MONO, 24, (190, 190, 190), anchor='lm'),
                      st('FRAME {no} / {of}', 1030, 60, MONO, 24, (190, 190, 190), anchor='rm'),
                      tx('l1', 540, H - 224, SANS_SB, 40, SUB, anchor='mb', shadow=255, sblur=3), tx('l2', 540, H - 168, SANS_SB, 40, SUB, anchor='mb', shadow=255, sblur=3)]),
       'credits': K('Credits', [], [('r1', 'Role 1', 'Directed by'), ('n1', 'Name 1', '@yourname'), ('r2', 'Role 2', 'Shot on'), ('n2', 'Name 2', 'a phone and a borrowed Fuji'),
                                    ('r3', 'Role 3', 'Locations'), ('n3', 'Name 3', 'Lisbon · Sintra · Cascais'), ('end', 'Last line', 'The End')],
                    [*[e for i in range(3) for e in (tx(f'r{i + 1}', 540, 326 + i * 190, GEO_B, 22, (175, 175, 175), anchor='mt', track=8, case='upper'),
                                                     tx(f'n{i + 1}', 540, 366 + i * 190, SERIF, 44, (235, 235, 235), anchor='mt'))],
                     tx('end', 540, 1000, SERIF_I, 64, WHITE, anchor='mt')], bg=(8, 8, 10))},
      ['title', 'still', 'dialogue', ('still', {'tc': '00:22:41:09', 'sub': 'Every street here goes uphill. Both ways.'}),
       ('still', {'tc': '00:47:03:18', 'sub': 'We stayed until the lights came on.'}), 'credits'],
      bg=(8, 8, 10), grain=7))

# ================================================================== 3. Quiet Journal (minimal)
QJ, QI, QM = (244, 242, 238), (42, 40, 37), (140, 134, 124)


def qnum(x, y):
    return st('({no})', x, y, GEO, 18, QM, anchor='lt', track=2)


add(T('sys_quiet_journal', 'Quiet journal',
      'White space as the material: one photo per slide at 50–80% width, a tiny number and a one-line caption, pacing wide → detail → wide.',
      'Quiet Journal (Cereal, Kinfolk, Tabi no Arubamu)', ('faded', 0.45),
      {'cover': K('Cover', ['Photo'], [('kicker', 'Small label', 'Journal — 04'), ('title', 'Title', 'Notes from a slow week in Sintra'),
                                        ('meta', 'Place and month', 'Portugal · October'), HANDLE],
                  [tx('kicker', 90, 110, GEO_B, 18, QM, anchor='lt', track=6, case='upper'), st('({no})', 990, 110, GEO, 18, QM, anchor='rt'),
                   P(0, 230, 290, 620, 780), tx('title', 230, 1112, SERIF_I, 46, QI, anchor='lt', wrap=620, lh=1.15),
                   tx('meta', 90, 1270, GEO_B, 18, QM, anchor='lb', track=5, case='upper'), tx('g_handle', 990, 1270, GEO, 18, QM, anchor='rb')]),
       'portrait': K('Tall photo', ['Photo'], [('cap', 'Caption', 'The garden at nine, before anyone else.')],
                     [P(0, 270, 190, 540, 770), qnum(270, 1000), tx('cap', 270, 1032, SERIF_I, 30, QI, anchor='lt', wrap=540, lh=1.25)]),
       'landscape': K('Wide photo', ['Photo'], [('cap', 'Caption', 'Fog until noon, then gold.')],
                      [P(0, 140, 390, 800, 540), qnum(140, 970), tx('cap', 140, 1002, SERIF_I, 30, QI, anchor='lt', wrap=800)]),
       'detail': K('Small detail', ['Photo'], [('cap', 'Caption', 'Tiles, counted twice.')],
                   [P(0, 390, 420, 300, 390), qnum(390, 846), tx('cap', 390, 878, SERIF_I, 28, QI, anchor='lt', wrap=420)]),
       'pair': K('Two photos', ['Left', 'Right'], [('cap', 'Caption', 'Two windows on the same street.')],
                 [P(0, 140, 220, 380, 500), P(1, 560, 560, 380, 500), qnum(140, 750), tx('cap', 140, 782, SERIF_I, 28, QI, anchor='lt', wrap=380, lh=1.25)]),
       'closing': K('Closing line', [], [('line', 'Closing sentence', 'We came for the palaces and stayed for the fog.')],
                    [tx('line', 540, 560, SERIF_I, 54, QI, anchor='mt', wrap=720, lh=1.2), tx('g_handle', 540, 1270, GEO_B, 18, QM, anchor='mb', track=5)])},
      ['cover', 'portrait', 'landscape', 'detail', 'pair', ('landscape', {'cap': 'The last train back, nearly empty.'}), 'closing'],
      bg=QJ, grain=2))

# ================================================================== 4. Greetings From (vintage postcards)
LINEN, PRED, PNAVY, CARD = (236, 224, 198), (198, 58, 44), (34, 52, 110), (250, 246, 236)
LETTERS = ['Letter 1', 'Letter 2', 'Letter 3', 'Letter 4', 'Letter 5', 'Letter 6']

add(T('sys_greetings_from', 'Greetings from',
      'A stack of linen-era postcards: a cover with big 3D block letters filled with photos, postcard fronts with postmarks, and a written postcard back.',
      'Greetings From (large-letter postcards, Library of Congress posters, Pescalemoria)', ('vintage', 0.6),
      {'cover': K('Big-letter cover', LETTERS, [('g1', 'Script line', 'Greetings from'), ('place', 'Place (up to 7 letters)', 'LISBON'),
                                                ('sub', 'Small line', 'The Portuguese coast'), HANDLE],
                  [RC(20, 20, W - 40, H - 40, None, outline=(250, 248, 242), width=22),
                   tx('g1', 540, 118, SCRIPT, 134, PRED, anchor='mt', rot=-5),
                   dict(t='mask', field='place', rect=(56, 340, 968, 560), font=IMPACT, slots=list(range(6)),
                        extrude=(14, 16, 14, PNAVY), outline=((255, 250, 240), 7)),
                   tx('sub', 540, 970, GEO_B, 30, PNAVY, anchor='mt', track=10, case='upper'),
                   STAMP(880, 1150, 92, 'LISBOA · 2026 · CORREIO', PRED, rot=-14), tx('g_handle', 70, 1262, GEO_B, 20, PNAVY, anchor='lb', track=4)], bg=('linen', LINEN)),
       'front': K('Postcard front', ['Postcard photo'], [('cap', 'Caption', 'Praça do Comércio, Lisbon')],
                  [P(0, 90, 110, 900, 1000, border=22, pb=96, bcolor=CARD, shadow=90, sblur=14), tx('cap', 116, 1160, GEO_B, 24, PNAVY, anchor='lt', track=4, case='upper'),
                   WAVES(620, 150, 380, 74, PNAVY, n=5, width=5, alpha=200), STAMP(900, 216, 80, 'LISBOA · OCT 2026', PRED, rot=12)], bg=('linen', LINEN)),
       'back': K('Postcard back', ['Stamp photo'], [('msg', 'Message', 'Dear you, the tiles here are every colour. We eat custard tarts for breakfast. Back soon, x'),
                                                    ('to', 'Address line', 'To: you, wherever you are')],
                 [RC(60, 170, 960, 1010, CARD, radius=6, shadow=80), st('P O S T   C A R D', 540, 214, GEO_B, 26, PNAVY, anchor='mt'),
                  LN([(540, 290), (540, 1120)], color=(185, 175, 155), width=2),
                  tx('msg', 100, 300, HAND, 40, (40, 42, 62), anchor='lt', wrap=410, lh=1.35),
                  RC(842, 262, 146, 176, None, outline=(190, 180, 160), width=2), P(0, 850, 270, 130, 160, border=6, bcolor=(255, 255, 255)),
                  WAVES(600, 290, 210, 80, (70, 70, 100), n=4, width=4, alpha=180), STAMP(800, 340, 66, 'LISBOA · OCT 2026', PRED, rot=-10),
                  tx('to', 586, 664, HAND, 40, (40, 42, 62), anchor='lt', wrap=400),
                  *[LN([(580, y), (980, y)], color=(170, 160, 140), width=2) for y in (760, 840, 920, 1000)]], bg=('linen', LINEN)),
       'end': K('Closing', ['Photo'], [('line', 'Closing script', 'Wish you\nwere here'), HANDLE],
                [RC(20, 20, W - 40, H - 40, None, outline=(250, 248, 242), width=22), tx('line', 540, 130, SCRIPT, 150, PRED, anchor='mt', lh=0.95, rot=-4),
                 P(0, 260, 520, 560, 600, border=18, pb=70, bcolor=CARD, rot=3, shadow=90), STAMP(830, 1130, 88, 'POSTE · EUROPA · 2026', PNAVY, rot=12),
                 tx('g_handle', 70, 1262, GEO_B, 20, PNAVY, anchor='lb', track=4)], bg=('linen', LINEN))},
      ['cover', 'front', 'back', ('front', {'cap': 'Torre de Belém'}), ('front', {'cap': 'Sintra, from the castle'}), 'end'], grain=3))

# ================================================================== 5. Cut & Tape: ticket stub diary (scrapbook)
KRAFT, TINK, TBLUE, TRED, TF = (226, 212, 186), (45, 36, 30), (40, 80, 150), (190, 60, 45), (246, 239, 224)

add(T('sys_ticket_diary', 'Ticket stub diary',
      'The trip as a scrapbook of tickets: an "admit one" cover, taped polaroids with handwritten captions, train stubs and a boarding pass.',
      'Cut & Tape (HANOI diary, Gold Coast editorial, travel-journal boards)', ('warmfilm', 0.55),
      {'cover': K('Cover', ['Polaroid 1', 'Polaroid 2'], [('t1', 'Title on the ticket', 'Europe by rail'), ('t2', 'Route line', 'LISBON → VIENNA · 21 DAYS'),
                                                          ('no', 'Ticket number', 'No. 0426'), ('note', 'Handwritten note', 'keep every ticket stub'), HANDLE],
                  [P(0, 640, 70, 360, 380, border=16, pb=64, rot=8, shadow=80), TAPE(770, 58, rot=-6),
                   dict(t='ticket', rect=(70, 480, 940, 380), fill=TF, stub=0.76, shadow=90),
                   st('ADMIT ONE', 118, 522, GEO_B, 22, TRED, anchor='lt', track=8), tx('t1', 112, 566, COND, 116, TINK, anchor='lt', case='upper', fit=640),
                   tx('t2', 118, 730, MONO, 26, TINK, anchor='lt'), tx('no', 905, 670, MONO, 26, TRED, anchor='mm', rot=90),
                   P(1, 80, 920, 360, 360, border=16, pb=60, rot=-6, shadow=80), TAPE(210, 905, rot=4),
                   tx('note', 520, 1010, HAND, 46, TINK, anchor='lt', rot=-2, wrap=480)]),
       'day': K('Day page', ['Polaroid'], [('cap', 'Caption on the polaroid', 'the yellow tram'), ('day', 'Day', 'Day 03'), ('route', 'Route', 'LIS – OPO'),
                                           ('time', 'Ticket details', '07:39 · CAR 3 · 12A'), ('note', 'Handwritten note', '3 hours, one window seat, too many pastries')],
                [P(0, 130, 100, 620, 660, border=22, pb=120, rot=-3, shadow=80), TAPE(380, 82, rot=3), tx('cap', 444, 812, HAND, 52, TINK, anchor='mt', rot=-3),
                 dict(t='ticket', rect=(560, 930, 450, 240), fill=(226, 236, 244), stub=0.72, notch=18, shadow=70),
                 tx('day', 590, 962, GEO_B, 20, TBLUE, anchor='lt', track=6, case='upper'), tx('route', 588, 1000, COND, 64, TINK, anchor='lt', case='upper', fit=290),
                 tx('time', 590, 1088, MONO, 22, TINK, anchor='lt'), st('{no}', 950, 1050, COND, 50, TBLUE, anchor='mm'),
                 tx('note', 110, 1000, HAND, 40, TINK, anchor='lt', wrap=400, rot=-2, lh=1.15)]),
       'pass': K('Boarding pass', ['Photo'], [('carrier', 'Carrier', 'Night train'), ('from', 'From (3 letters)', 'LIS'), ('to', 'To (3 letters)', 'VIE'),
                                              ('det', 'Details', 'DATE 04 OCT   CAR 3   DEP 21:40'), ('seat', 'Seat', '12A')],
                 [FRAME(0, 110, 100, 860, 620, b=18, rot=2, sh=80), TAPE(450, 84, rot=-3),
                  dict(t='ticket', rect=(70, 820, 940, 420), fill=(250, 250, 248), band=((34, 60, 120), 84), stub=0.76, shadow=90),
                  st('BOARDING PASS', 110, 862, GEO_B, 24, WHITE, anchor='lm', track=8), tx('carrier', 760, 862, GEO_B, 20, WHITE, anchor='rm', track=4, case='upper'),
                  tx('from', 108, 930, COND, 130, TINK, anchor='lt', case='upper'), st('→', 400, 1000, SANS, 64, TINK, anchor='mm'),
                  tx('to', 450, 930, COND, 130, TINK, anchor='lt', case='upper'), tx('det', 110, 1130, MONO, 24, (90, 90, 90), anchor='lt'),
                  st('SEAT', 888, 930, GEO_B, 18, MUTED, anchor='mt', track=5), tx('seat', 888, 960, COND, 64, (34, 60, 120), anchor='mt')]),
       'end': K('Closing', [], [('words', 'Handwritten line', 'to be\ncontinued…'), ('ret', 'Return ticket word', 'Home'), HANDLE],
                [TORN(200, 250, 680, 320, rot=-2), tx('words', 540, 290, HAND, 96, TINK, anchor='mt', lh=1.05, rot=-2),
                 dict(t='ticket', rect=(240, 700, 600, 260), fill=TF, stub=0.72, shadow=80),
                 st('RETURN TICKET', 280, 738, GEO_B, 22, TRED, anchor='lt', track=8), tx('ret', 276, 784, COND, 90, TINK, anchor='lt', case='upper', fit=380),
                 st('VALID: ANY TIME', 280, 900, MONO, 22, TINK, anchor='lt'),
                 STAMP(850, 1150, 90, 'EUROPA · 2026', TRED, rot=12), tx('g_handle', 120, 1262, HAND, 42, TINK, anchor='lb')])},
      ['cover', 'day', 'pass', ('day', {'cap': 'Porto from the bridge', 'day': 'Day 05', 'route': 'OPO – MAD', 'note': 'the river was the colour of tea'}), 'end'],
      bg=('paper', KRAFT), grain=4))

# ================================================================== 6. Contact Sheet (film & analog)
FILMBG, EDGE, GREASE, FPALE = (18, 18, 18), (232, 150, 60), (222, 44, 40), (230, 224, 210)
FRAMES = [f'Frame {i}' for i in range(1, 13)]


def sheet_grid():
    els = []
    for i in range(12):
        c, r = i % 3, i // 3
        x, y = 60 + c * 330, 140 + r * 250
        els += [P(i, x, y, 300, 200), st(f'{10 + i}{"A" if i % 2 else ""}', x, y + 210, MONO, 20, EDGE, anchor='lt')]
    return els


add(T('sys_contact_sheet', 'Contact sheet',
      'The roll of film is the layout: a 12-frame contact sheet with grease-pencil picks, enlarged selects between sprocket bands, a three-frame strip and "end of roll".',
      'Contact Sheet (Portugal on film, LOOKSLIKEFILM, Bryan Garris)', ('warmfilm', 0.7),
      {'sheet': K('Contact sheet', FRAMES, [('roll', 'Roll label', 'ROLL 03 · LISBON · OCT 2026'), ('title', 'Title', 'Contact sheet'), ('pick', 'Grease-pencil note', 'circled = keepers'), HANDLE],
                  [tx('roll', 60, 80, MONO, 22, (170, 170, 170), anchor='lm'), st('400  ·  35MM', 1020, 80, MONO, 22, (170, 170, 170), anchor='rm'),
                   *sheet_grid(), ELL(370, 372, 340, 240, outline=GREASE, width=7),
                   LN([(736, 656), (1004, 826)], color=GREASE, width=7), LN([(1004, 656), (736, 826)], color=GREASE, width=7),
                   tx('title', 60, 1160, COND, 100, WHITE, anchor='lt', case='upper'), tx('pick', 1020, 1196, HAND, 44, GREASE, anchor='rt', rot=-3)]),
       'select': K('Enlarged select', ['Frame'], [('fr', 'Frame number', '14A'), ('cap', 'Caption', '14A — Alfama at 7:40 pm'), ('note', 'Grease-pencil note', 'print this one')],
                   [dict(t='film', rect=(0, 150, W, 90), hole=(232, 228, 218)), P(0, 40, 240, 1000, 666), dict(t='film', rect=(0, 906, W, 90), hole=(232, 228, 218)),
                    tx('fr', 90, 195, MONO, 22, EDGE, anchor='lm'), st('400', 990, 951, MONO, 22, EDGE, anchor='rm'),
                    tx('cap', 60, 1060, MONO, 30, FPALE, anchor='lt', wrap=640), tx('note', 1010, 1050, HAND, 50, GREASE, anchor='rt', rot=-4),
                    st('{no} / {of}', 1020, 1290, MONO, 20, (150, 150, 150), anchor='rb')]),
       'strip': K('Three-frame strip', ['Frame 1', 'Frame 2', 'Frame 3'], [('cap', 'Caption', '15–17 — the walk up to the castle')],
                  [dict(t='film', rect=(0, 330, W, 560), hole=(232, 228, 218)), P(0, 30, 400, 330, 420), P(1, 375, 400, 330, 420), P(2, 720, 400, 330, 420),
                   st('15', 30, 908, MONO, 20, EDGE, anchor='lt'), st('16', 375, 908, MONO, 20, EDGE, anchor='lt'), st('17', 720, 908, MONO, 20, EDGE, anchor='lt'),
                   tx('cap', 60, 1010, MONO, 30, FPALE, anchor='lt', wrap=960), st('{no} / {of}', 1020, 1290, MONO, 20, (150, 150, 150), anchor='rb')]),
       'end': K('End of roll', [], [('count', 'Frame count', '36 / 36')],
                [st('END OF ROLL', 540, 470, COND, 150, WHITE, anchor='mt'), tx('count', 540, 670, MONO, 40, EDGE, anchor='mt'),
                 dict(t='film', rect=(0, 860, W, 130), hole=(232, 228, 218)), tx('g_handle', 540, 1230, MONO, 26, (170, 170, 170), anchor='mb')])},
      ['sheet', 'select', 'strip', ('select', {'fr': '21', 'cap': '21 — the last tram, from the back', 'note': 'yes!'}), 'end'],
      bg=FILMBG, grain=7))

# ================================================================== 7. Field Guide: day by day (destination guides)
FG, FINK, FGREEN, FMUST, FMUT = (250, 247, 240), (31, 42, 48), (46, 125, 107), (242, 181, 68), (120, 126, 124)
ROUTE = [(190, 330), (430, 540), (300, 800), (650, 900), (860, 1130)]

add(T('sys_field_guide', 'Field guide · day by day',
      'A guide people save: promise on the cover, one timeline slide per day with times and stops, a sketched route map, good-to-know tips and a save slide.',
      'Field Guide (Kia Kia Penang kit, Kyoto guide, Herb Lester, Wallpaper* City Guides)', ('natural', 0.6),
      {'cover': K('Cover', ['Cover photo'], [('kicker', 'Small label', 'Field guide · 3 days'), ('title', 'Title', 'Three days\nin Porto'),
                                              ('c1', 'Chip 1', 'walkable'), ('c2', 'Chip 2', '€€'), ('c3', 'Chip 3', 'best in spring'), ('c4', 'Chip 4', '12 stops'), HANDLE],
                  [tx('kicker', 70, 86, GEO_B, 22, FGREEN, anchor='lt', track=7, case='upper'), tx('title', 64, 136, SERIF_B, 120, FINK, anchor='lt', lh=0.98),
                   dict(t='chips', fields=['c1', 'c2', 'c3', 'c4'], xy=(70, 420), font=SANS_SB, size=28, color=FINK, maxw=940,
                        fills=[(222, 238, 230), (252, 236, 200), (230, 232, 240), (246, 222, 214)]),
                   P(0, 70, 540, 940, 720, radius=26),
                   BADGE(905, 585, 96, 'SAVE FOR YOUR TRIP · ', GEO_B, 17, FINK, fill=FMUST, ring=False, center='✦', cfont=SYM, csize=46, rot=-12)]),
       'day': K('Day timeline', ['Photo 1', 'Photo 2'], [('day', 'Day', 'Day 1'), ('theme', 'Theme', 'Ribeira and the river'),
                                                         ('t1', 'Time 1', '09:00'), ('s1', 'Stop 1', 'Coffee at Majestic Café'),
                                                         ('t2', 'Time 2', '11:30'), ('s2', 'Stop 2', 'Walk down to Ribeira'),
                                                         ('t3', 'Time 3', '14:00'), ('s3', 'Stop 3', 'Port tasting across the river'),
                                                         ('t4', 'Time 4', '19:30'), ('s4', 'Stop 4', 'Sunset at Jardim do Morro')],
                [tx('day', 70, 60, COND, 150, FGREEN, anchor='lt', case='upper'), tx('theme', 72, 244, SERIF_I, 46, FINK, anchor='lt'),
                 LN([(160, 390), (160, 1080)], color=(205, 200, 190), width=4),
                 *[e for i in range(4) for e in (ELL(146, 396 + i * 220, 28, 28, fill=FGREEN), tx(f't{i + 1}', 200, 388 + i * 220, MONO, 24, FMUT, anchor='lt'),
                                                 tx(f's{i + 1}', 200, 420 + i * 220, SANS_SB, 38, FINK, anchor='lt', wrap=500, lh=1.15))],
                 P(0, 730, 380, 290, 360, radius=18), P(1, 730, 770, 290, 360, radius=18), st('{no} / {of}', 1010, 1290, MONO, 20, FMUT, anchor='rb')]),
       'map': K('Route map', [], [('title', 'Title', 'The route'), ('dist', 'Distance line', '6.4 km · mostly downhill')] +
                [(f'm{i}', f'Place {i}', p) for i, p in enumerate(['Majestic Café', 'Livraria Lello', 'Sé Cathedral', 'Ribeira', 'Jardim do Morro'], 1)],
                [dict(t='ruled', rect=(0, 0, W, H), kind='grid', step=60, color=(150, 160, 150), alpha=45),
                 tx('title', 70, 70, SERIF_B, 76, FINK, anchor='lt'), tx('dist', 72, 172, MONO, 26, FMUT, anchor='lt'),
                 LN(ROUTE, color=FGREEN, width=6, dash=(18, 14)),
                 *[e for i, (x, y) in enumerate(ROUTE) for e in (ELL(x - 26, y - 26, 52, 52, fill=FGREEN), st(str(i + 1), x, y, SANS_SB, 28, WHITE, anchor='mm'),
                                                                 tx(f'm{i + 1}', x + 44 if x < 700 else x - 44, y, SANS_SB, 32, FINK,
                                                                    anchor='lm' if x < 700 else 'rm', hl=(FMUST, 8, 2)))]]),
       'tips': K('Good to know', [], [(f'k{i}', f'Tip {i}', t) for i, t in enumerate(
           ['Buy the Andante card for trams and the metro', 'Most museums close on Mondays', 'Book Livraria Lello online to skip the queue',
            'Bring shoes for hills, and more hills', 'Dinner starts late: 8 pm is early'], 1)],
                 [st('Good to know', 70, 84, SERIF_B, 84, FINK, anchor='lt'),
                  *[e for i in range(5) for e in (ELL(72, 276 + i * 180, 24, 24, fill=FMUST), tx(f'k{i + 1}', 120, 264 + i * 180, SANS, 36, FINK, anchor='lt', wrap=860, lh=1.25))]]),
       'end': K('Save slide', [], [('title', 'Title', 'Save this\nfor later'), ('btn', 'Button', 'Send it to your travel buddy →')],
                [tx('title', 540, 380, SERIF_B, 110, FINK, anchor='mt', lh=1.0), PILL(540, 720, SANS_SB, 32, field='btn', fill=FGREEN, color=WHITE),
                 tx('g_handle', 540, 1250, MONO, 26, FMUT, anchor='mb')])},
      ['cover', 'day', ('day', {'day': 'Day 2', 'theme': 'Tiles, books and bridges', 't1': '09:30', 's1': 'Azulejos at São Bento station',
                                't2': '12:00', 's2': 'Lunch at Mercado do Bolhão', 't3': '15:00', 's3': 'Climb the Clérigos Tower',
                                't4': '20:00', 's4': 'Francesinha, obviously'}), 'map', 'tips', 'end'], bg=FG))

# ================================================================== 8. Panorama Run: giant word (seamless)
LINES = [LN([(0, 44), (W, 44)], color=WHITE, width=2, alpha=200, z=1), LN([(0, H - 44), (W, H - 44)], color=WHITE, width=2, alpha=200, z=1)]

add(T('sys_giant_word', 'Giant word panorama (seamless)',
      'One panorama runs under every slide and one giant word stretches across the opening slides, with thin white rules and museum-style labels.',
      'Panorama Run (SCRL, TIME panoramas, magazine spreads)', ('mediterranean', 0.6),
      {'cover': K('Cover (word starts here)', ['Panorama (runs under every slide)'], [('kicker', 'Small line', 'A panorama in five frames'), ('word', 'Giant word', 'LISBOA'), HANDLE],
                  [*LINES, tx('kicker', 76, 120, GEO_B, 26, WHITE, anchor='lt', track=10, case='upper', shadow=130),
                   tx('word', 60, 300, COND, 860, WHITE, anchor='lt', shadow=90, sblur=14, case='upper', z=2),
                   st('swipe  →', 1010, 1278, GEO_B, 22, WHITE, anchor='rb', shadow=130)]),
       'run': K('Panorama only', [], [], [*LINES, st('{no}', 1036, 74, GEO_B, 18, WHITE, anchor='rt', shadow=110)]),
       'label': K('Panorama + label', [], [('place', 'Place', 'Miradouro da Graça'), ('meta', 'Details', '38.716° N · 9.131° W · 6:40 pm')],
                  [*LINES, RC(60, 1080, 560, 160, (250, 248, 242), radius=4, shadow=60),
                   tx('place', 90, 1106, SERIF_B, 40, INK, anchor='lt', fit=500), tx('meta', 90, 1170, MONO, 22, MUTED, anchor='lt')]),
       'end': K('Closing label', [], [('line', 'Closing line', 'one city, one long look')],
                [*LINES, RC(140, 520, 800, 300, (250, 248, 242), radius=4, shadow=60), tx('line', 540, 566, SERIF_I, 54, INK, anchor='mt', wrap=700, lh=1.15),
                 tx('g_handle', 540, 752, MONO, 22, MUTED, anchor='mt')])},
      ['cover', 'run', 'label', 'run', 'end'], strip=True, bg=(30, 30, 32), strip_els=[P(0, 0, 0, -1, H, z=0)]))

# ================================================================== 9. Poster Type: city poster series
CWAYS = {'orange': ((232, 87, 46), INK, ((25, 20, 18), (246, 232, 214)), 'circle'),
         'blue': ((34, 70, 176), (245, 240, 230), ((14, 22, 70), (238, 220, 190)), 'arch'),
         'cream': ((245, 240, 230), INK, ((54, 32, 22), (240, 198, 120)), 'rect'),
         'black': ((24, 24, 24), (236, 214, 110), ((10, 10, 10), (236, 214, 110)), 'circle')}


def poster(name):
    bgc, ink, duo, shape = CWAYS[name]
    photo = {'circle': P(0, 190, 160, 700, 700, shape='circle', duo=duo), 'arch': P(0, 210, 140, 660, 770, shape='arch', duo=duo),
             'rect': P(0, 60, 140, 960, 730, duo=duo)}[shape]
    py = {'circle': 900, 'arch': 940, 'rect': 910}[shape]
    return K(f'Poster ({name})', ['Photo'], [('no', 'Number', 'N° 01'), ('place', 'Place', 'Lisboa'), ('coords', 'Coordinates', '38.72° N  9.14° W'), ('year', 'Year', '2026')],
             [tx('no', 60, 52, GEO_B, 22, ink, anchor='lt', track=5), tx('g_series', 1020, 52, GEO_B, 22, ink, anchor='rt', track=5, case='upper'),
              LN([(60, 100), (1020, 100)], color=ink, width=3), photo,
              tx('place', 540, py, COND, 330, ink, anchor='mt', fit=980, case='upper'),
              LN([(60, 1248), (1020, 1248)], color=ink, width=3), tx('coords', 60, 1270, MONO, 24, ink, anchor='lt'), tx('year', 1020, 1270, MONO, 24, ink, anchor='rt')],
             bg=bgc)


SERIES_BLOCKS = [((40, 180), 'orange'), ((550, 180), 'blue'), ((40, 740), 'cream'), ((550, 740), 'black')]
add(T('sys_poster_series', 'City poster series',
      'The place name does the work: one poster per slide in a rotating colourway, duotone photos in circle, arch or band shapes, coordinates in mono.',
      'Poster Type (Curitiba posters, Swiss mountains poster, Paula Scher maps)', ('punchy', 0.5),
      {'cover': K('Series cover', ['Photo 1', 'Photo 2', 'Photo 3', 'Photo 4'],
                  [('g_series', 'Series name (every slide)', 'Europe series'), ('p1', 'Place 1', 'Lisboa'), ('p2', 'Place 2', 'Porto'), ('p3', 'Place 3', 'Sintra'),
                   ('p4', 'Place 4', 'Lagos'), ('count', 'Count line', '5 posters  →')],
                  [tx('g_series', 40, 44, COND, 110, INK, anchor='lt', case='upper', fit=700), tx('count', 1040, 100, GEO_B, 22, INK, anchor='rm', track=4, case='upper'),
                   *[e for i, ((x, y), cw) in enumerate(SERIES_BLOCKS) for e in (
                       RC(x, y, 490, 540, CWAYS[cw][0]), P(i, x + 95, y + 40, 300, 300, shape='circle', duo=CWAYS[cw][2]),
                       tx(f'p{i + 1}', x + 245, y + 380, COND, 96, CWAYS[cw][1], anchor='mt', fit=440, case='upper'))]], bg=(245, 240, 230)),
       **{f'poster_{n}': poster(n) for n in CWAYS}},
      ['cover', ('poster_orange', {'no': 'N° 01', 'place': 'Lisboa', 'coords': '38.72° N  9.14° W'}),
       ('poster_blue', {'no': 'N° 02', 'place': 'Porto', 'coords': '41.15° N  8.61° W'}),
       ('poster_cream', {'no': 'N° 03', 'place': 'Sintra', 'coords': '38.80° N  9.38° W'}),
       ('poster_black', {'no': 'N° 04', 'place': 'Lagos', 'coords': '37.10° N  8.67° W'}),
       ('poster_orange', {'no': 'N° 05', 'place': 'Évora', 'coords': '38.57° N  7.91° W'})], grain=3))

# ================================================================== 10. Expedition (adventure & outdoor)
EXBG, EXP, EXO, EXM = (28, 35, 33), (230, 225, 211), (217, 108, 63), (150, 160, 152)
TRAIL = [(140, 1060), (300, 820), (520, 900), (700, 560), (900, 330)]

add(T('sys_expedition', 'Expedition log',
      'Route, weather and altitude as design: contour lines over the photos, coordinates, a stage page with an elevation profile, a numbers page and a route map.',
      'Expedition (Chris Burkard, Sidetracked, Another Escape, Ernest Journal)', ('alpine', 0.6),
      {'cover': K('Cover', ['Cover photo'], [('kicker', 'Small line', 'EXPEDITION LOG · 11 DAYS'), ('title', 'Title', 'Tour du\nMont Blanc'),
                                              ('coords', 'Coordinates', '45.8326° N  6.8652° E'), ('alt', 'Highest point', '↑ 2,665 M'), HANDLE],
                  [P(0, 0, 0, W, H, dim=0.25), dict(t='topo', rect=(0, 0, W, H), centers=[(780, 380), (200, 1050)], rings=14, step=46, color=WHITE, alpha=55),
                   SHADE(760, 590, 0, 210), tx('kicker', 60, 70, MONO, 24, EXP, anchor='lt'),
                   tx('title', 56, 920, COND, 190, EXP, anchor='lt', lh=0.88, case='upper', fit=960),
                   tx('coords', 60, 1290, MONO, 24, EXO, anchor='lb'), tx('alt', 1020, 1290, MONO, 24, EXP, anchor='rb')]),
       'stage': K('Stage', ['Stage photo'], [('stage', 'Stage', 'Stage 03'), ('title', 'Title', 'Col de la Seigne'),
                                             ('stats', 'Stats line', '18.4 KM   ↑ 1,240 M   7 H 10'), ('heights', 'Heights along the way (m)', '1650, 1900, 2516, 2200, 1980, 1700, 1560')],
                  [P(0, 0, 0, W, 740), tx('stage', 60, 790, MONO, 24, EXO, anchor='lt', case='upper'),
                   tx('title', 56, 830, COND, 96, EXP, anchor='lt', case='upper', fit=960), tx('stats', 60, 962, MONO, 26, EXM, anchor='lt'),
                   dict(t='profile', field='heights', rect=(60, 1085, 960, 160), color=EXO, tcolor=EXP), st('{no} / {of}', 1020, 1304, MONO, 20, EXM, anchor='rb')]),
       'numbers': K('In numbers', [], [('n1', 'Number 1', '170 km'), ('l1', 'Label 1', 'distance'), ('n2', 'Number 2', '10,000 m'), ('l2', 'Label 2', 'climbed'),
                                       ('n3', 'Number 3', '11'), ('l3', 'Label 3', 'days on foot')],
                    [dict(t='topo', rect=(0, 0, W, H), centers=[(560, 675)], rings=16, step=44, color=EXO, alpha=40),
                     *[e for i in range(3) for e in (tx(f'n{i + 1}', 60, 150 + i * 360, COND, 200, EXP, anchor='lt'),
                                                     tx(f'l{i + 1}', 64, 384 + i * 360, MONO, 26, EXO, anchor='lt', case='upper'))]]),
       'map': K('Route map', [], [('title', 'Title', 'The route')] + [(f'm{i}', f'Point {i}', p) for i, p in
                                                                     enumerate(['Les Houches', 'Col du Bonhomme', 'Courmayeur', 'Champex', 'Chamonix'], 1)],
                [dict(t='topo', rect=(0, 0, W, H), centers=[(300, 420), (780, 900)], rings=13, step=48, color=EXP, alpha=55),
                 tx('title', 60, 70, COND, 96, EXP, anchor='lt', case='upper'), LN(TRAIL, color=EXO, width=6, dash=(18, 12)),
                 *[e for i, (x, y) in enumerate(TRAIL) for e in (ELL(x - 14, y - 14, 28, 28, fill=EXO), tx(f'm{i + 1}', x + 28, y, MONO, 26, EXP, anchor='lm', case='upper'))]]),
       'end': K('Closing', ['Photo'], [('line', 'Closing line', 'Summit\nnot required.')],
                [P(0, 0, 0, W, H, dim=0.4), dict(t='topo', rect=(0, 0, W, H), centers=[(700, 500)], rings=12, step=50, color=WHITE, alpha=45),
                 tx('line', 56, 880, COND, 150, EXP, anchor='lt', lh=0.9, case='upper'), tx('g_handle', 60, 1290, MONO, 24, EXO, anchor='lb')])},
      ['cover', 'stage', ('stage', {'stage': 'Stage 06', 'title': 'Grand Col Ferret', 'stats': '19.5 KM   ↑ 1,320 M   7 H 40',
                                    'heights': '1770, 2050, 2537, 2300, 1900, 1600'}), 'numbers', 'map', 'end'],
      bg=EXBG, grain=5))

# ================================================================== 11. Cut-up: riso collage (collage & experimental)
RPAPER, RPINK, RBLUE, RYEL = (247, 242, 234), (255, 72, 166), (0, 112, 190), (255, 226, 0)
RISO, RISO2 = ((0, 92, 170), (255, 72, 166), (10, 6)), ((200, 30, 110), (0, 112, 190), (-9, 7))

add(T('sys_riso_collage', 'Riso collage',
      'Maximal colour and collision: photos printed as two-ink riso (blue + fluorescent pink, slightly out of register), cut into circles and arches, with dots and stripes.',
      'Cut-up (Pará zine, Places, Eugenia Loli, RECORTES)', ('none', 0.0),
      {'cover': K('Cover', ['Cover photo'], [('title', 'Title', 'Loud\nLisbon'), ('tag', 'Sticker', 'VOL. 3 · RISO EDITION'), HANDLE],
                  [ELL(470, 90, 560, 560, fill=RYEL), P(0, 90, 260, 680, 820, riso=RISO),
                   dict(t='ruled', rect=(620, 760, 420, 420), kind='dots', step=22, color=RPINK, alpha=255),
                   tx('title', 48, 850, BLACK, 210, RBLUE, anchor='lt', lh=0.86, rot=-4, case='upper'),
                   PILL(780, 150, MONO, 24, field='tag', fill=RPINK, color=WHITE, rot=8), SPARK(980, 1180, 40, RPINK), SPARK(936, 1244, 18, RBLUE),
                   tx('g_handle', 1020, 1300, MONO, 22, RBLUE, anchor='rb')]),
       'cut': K('Cut shapes', ['Circle photo', 'Arch photo'], [('word', 'Big word', 'tiles'), ('cap', 'Small caption', 'every wall, every colour')],
                [RC(-120, 600, 1320, 100, RYEL, rot=-12), P(0, 60, 80, 560, 560, shape='circle', riso=RISO), P(1, 480, 500, 540, 720, shape='arch', riso=RISO2),
                 tx('word', 56, 1080, BLACK, 140, RBLUE, anchor='lt', case='upper'), tx('cap', 64, 1250, MONO, 26, RPINK, anchor='lt')]),
       'grid': K('Colour grid', ['Photo 1', 'Photo 2'], [('word', 'Word', 'Pastéis'), ('note', 'Note', '6 a day is normal, right?')],
                 [P(0, 0, 0, 540, 675, riso=RISO), RC(540, 0, 540, 675, RPINK), tx('word', 810, 337, BLACK, 110, WHITE, anchor='mm', case='upper', fit=480),
                  RC(0, 675, 540, 675, RYEL), dict(t='ruled', rect=(0, 675, 540, 675), kind='dots', step=26, color=RBLUE, alpha=90),
                  tx('note', 270, 1012, MONO, 30, RBLUE, anchor='mm', wrap=420, valign='middle'), P(1, 540, 675, 540, 675, riso=RISO2)]),
       'end': K('Closing', ['Photo'], [('word', 'Big word', 'Bye!'), ('tag', 'Sticker', 'SEE YOU IN PORTO')],
                [ELL(140, 180, 800, 800, fill=RPINK), tx('word', 540, 580, BLACK, 260, RYEL, anchor='mm', case='upper', fit=760),
                 P(0, 640, 880, 340, 400, riso=RISO, border=10, bcolor=WHITE, rot=6, shadow=60), PILL(90, 1200, MONO, 26, field='tag', fill=RBLUE, color=WHITE, anchor='lm', rot=-4),
                 tx('g_handle', 60, 1300, MONO, 22, RBLUE, anchor='lb')])},
      ['cover', 'cut', 'grid', ('cut', {'word': 'trams', 'cap': 'yellow, loud, always late'}), 'end'],
      bg=('paper', RPAPER), grain=4))
