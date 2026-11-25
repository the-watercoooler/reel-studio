"""Carousel templates for Carousel Studio.

Each template = slide kinds; each kind = a list of elements drawn in order (see carousel_engine.r_generic).
Sources: a set of saved reference carousels and common travel-carousel formats on the web
(seamless panoramas and scrapbooks, taped polaroids, notebook dumps, itineraries, "instead of X try Y").
Coordinates are on the 1080 x 1350 slide. Add a template by appending to TEMPLATES.
"""
W, H = 1080, 1350

# ------------------------------------------------------------------ fonts and colours
SERIF, SERIF_I, BASK, BODONI, BELL = 'GARA.TTF', 'GARAIT.TTF', 'BASKVILL.TTF', 'BOD_PSTC.TTF', 'BELL.TTF'
SANS, SANS_L, SANS_B = 'segoeui.ttf', 'segoeuil.ttf', 'segoeuib.ttf'
GOTH, GOTH_B, COOPER, BERLIN, IMPACT = 'GOTHIC.TTF', 'GOTHICB.TTF', 'COOPBL.TTF', 'BRLNSB.TTF', 'impact.ttf'
HAND, HAND_B, INK_F, SCRIPT, SCRIPT_B = 'segoepr.ttf', 'segoeprb.ttf', 'Inkfree.ttf', 'segoesc.ttf', 'segoescb.ttf'
MONO, SYM = 'consola.ttf', 'seguisym.ttf'

WHITE, CREAM, INK, MUTED = (255, 255, 255), (246, 240, 228), (34, 31, 28), (120, 112, 100)
YELLOW, ORANGE, RED, GREEN = (245, 200, 40), (226, 120, 48), (190, 52, 44), (46, 128, 84)
SAGE, TERRA, OLIVE, NAVY = (199, 206, 186), (170, 88, 58), (80, 90, 60), (32, 42, 66)
PAPER, OFFWHITE, BODY = (240, 234, 222), (247, 245, 240), (86, 80, 72)


# ------------------------------------------------------------------ element helpers
def P(slot, x, y, w, h, **kw):
    return dict(t='photo', slot=slot, rect=(x, y, w, h), **kw)


def FULL(slot=0, **kw):
    return P(slot, 0, 0, W, H, **kw)


def TX(field, x, y, fnt, size, **kw):
    return dict(t='text', field=field, xy=(x, y), font=fnt, size=size, **kw)


def ST(text, x, y, fnt, size, **kw):
    return dict(t='text', text=text, xy=(x, y), font=fnt, size=size, **kw)


def RC(x, y, w, h, fill, **kw):
    return dict(t='rect', rect=(x, y, w, h), fill=fill, **kw)


def LN(pts, **kw):
    return dict(t='line', pts=pts, **kw)


def SHADE(y, h, a0=0, a1=180, x=0, w=W, **kw):
    return dict(t='shade', rect=(x, y, w, h), a0=a0, a1=a1, **kw)


def TAPE(x, y, w=170, h=46, rot=0, **kw):
    return dict(t='tape', rect=(x, y, w, h), rot=rot, **kw)


def K(label, photos, fields, els, bg=None):
    return dict(label=label, photos=photos, fields=fields, els=els, bg=bg)


def T(key, label, group, about, ref, look, kinds, default, **kw):
    return dict(key=key, label=label, group=group, about=about, ref=ref, look=look, kinds=kinds, default=default, **kw)


def ink(**kw):            # dark text on light backgrounds: no shadow
    d = dict(color=INK, shadow=0)
    d.update(kw)
    return d


def arrow(x0, y0, x1, y1, col=INK, w=4):
    """A hand-drawn style arrow."""
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    h1 = (x1 - 26 * math.cos(a - 0.5), y1 - 26 * math.sin(a - 0.5))
    h2 = (x1 - 26 * math.cos(a + 0.5), y1 - 26 * math.sin(a + 0.5))
    mid = ((x0 + x1) / 2 + 30, (y0 + y1) / 2 - 30)
    return [LN([(x0, y0), mid, (x1, y1)], color=col, width=w), LN([h1, (x1, y1), h2], color=col, width=w)]


def grid(slots, x0, y0, cols, cw, ch, gx, gy, **kw):
    return [P(s, x0 + (i % cols) * (cw + gx), y0 + (i // cols) * (ch + gy), cw, ch, **kw) for i, s in enumerate(slots)]


PH = lambda n, word='Photo': [f'{word} {i + 1}' for i in range(n)]   # noqa: E731
TEMPLATES = []
add = TEMPLATES.append

# ================================================================== From your references
add(T('contrast_pair', 'Grass is greener (pairs)', 'Your references',
      'Two photos per slide with a small line on each: “When I was here… I wanted to be there.”', '@_nargisfarheena_', ('natural', 0.8),
      {'pair': K('Two photos', ['Top photo', 'Bottom photo'], [('a', 'Top line', 'When I was in the mountains'), ('b', 'Bottom line', 'I wanted to see the ocean')],
                 [P(0, 0, 0, W, 675), P(1, 0, 675, W, 675),
                  TX('a', 540, 318, SERIF, 40, shadow=170, sblur=8), TX('b', 540, 993, SERIF, 40, shadow=170, sblur=8)])},
      [('pair', {'a': 'When I was in the mountains', 'b': 'I wanted to see the ocean'}),
       ('pair', {'a': 'When I was by the ocean', 'b': 'I wanted to explore a new city'}),
       ('pair', {'a': 'When I was in a new city', 'b': 'I wanted to be somewhere quiet'}),
       ('pair', {'a': 'When I was somewhere quiet', 'b': 'I wanted to be around people'}),
       ('pair', {'a': 'We always think the grass is greener…', 'b': 'Don’t forget to enjoy what’s in front of you'})]))

add(T('running_sentence', 'Running sentence (cinematic)', 'Your references',
      'Two photos per slide; one sentence runs across the slides and meets at the middle of each one.', '@timavisual', ('cinematic', 0.7),
      {'pair': K('Two photos', ['Top photo', 'Bottom photo'], [('a', 'Line on the top photo', 'sometimes the road is longer'), ('b', 'Line on the bottom photo', 'but maybe that’s the point')],
                 [P(0, 0, 0, W, 675), P(1, 0, 675, W, 675),
                  TX('a', 540, 640, SANS_L, 34, anchor='mb', shadow=170), TX('b', 540, 712, SERIF_I, 40, shadow=170)])},
      [('pair', {'a': 'sometimes the road is longer', 'b': 'but maybe that’s the point'}),
       ('pair', {'a': 'beautiful days don’t just arrive', 'b': 'you find them along the way'}),
       ('pair', {'a': 'we didn’t plan most of it', 'b': 'we just let it happen'}),
       ('pair', {'a': 'every turn looked like a postcard', 'b': 'so we stopped at all of them'}),
       ('pair', {'a': 'so we stayed on the road', 'b': 'a little longer'})]))

add(T('stack3', 'Three stacked, tiny captions', 'Your references',
      'Three photos stacked on each slide with small, conversational lowercase captions.', '@youknowprateek', ('greenfilm', 0.7),
      {'stack': K('Three photos', ['Top', 'Middle', 'Bottom'], [('c1', 'Caption 1', 'how can i describe my life to you?'), ('c2', 'Caption 2', 'i take a lot of pictures and listen to music'), ('c3', 'Caption 3', 'and i keep finding places like this')],
                  [P(0, 0, 0, W, 450), P(1, 0, 450, W, 450), P(2, 0, 900, W, 450),
                   TX('c1', 540, 408, SANS_L, 28, anchor='mb', shadow=170), TX('c2', 540, 858, SANS_L, 28, anchor='mb', shadow=170), TX('c3', 540, 1308, SANS_L, 28, anchor='mb', shadow=170)])},
      [('stack', {}), ('stack', {'c1': 'mornings start slow here', 'c2': 'coffee, then the lake', 'c3': 'then nothing at all'}),
       ('stack', {'c1': 'i wrote down every place', 'c2': 'so i’d never forget', 'c3': 'how it felt'}),
       ('stack', {'c1': 'some days were loud', 'c2': 'most days were quiet', 'c3': 'all of them were good'})]))

add(T('decoding', 'Decoding a place (one word per photo)', 'Your references',
      'A cover question, a tilted mosaic, then one photo per slide with a single small word, ending on a sentence.', 'camera_avenger / himalayas.in', ('alpine', 0.7),
      {'cover': K('Cover', ['Cover photo'], [('place', 'Place', 'the Alps'), ('question', 'Question', 'What makes the MOUNTAINS unforgettable?')],
                  [FULL(0), SHADE(0, 520, 150, 0), ST('D E C O D I N G', 540, 108, GOTH, 24, track=6), TX('place', 540, 150, BASK, 84, track=14, case='upper'),
                   SHADE(900, 450, 0, 200), TX('question', 540, 1180, SANS_B, 44, wrap=920, valign='bottom'),
                   ST('swipe to see what i learned  >>>', 540, 1250, SANS, 24, color=(225, 225, 225))]),
       'mosaic': K('Tilted mosaic', PH(9), [], [dict(t='mosaic', slots=list(range(9)), rect=(0, 0, W, H), cols=3, rows=3, rot=-14, tile=(400, 500), gap=14)], bg=(14, 14, 16)),
       'word': K('One word', ['Photo'], [('word', 'Word', 'Silence')], [FULL(0), TX('word', 540, 675, SERIF_I, 48, anchor='mm', shadow=180, sblur=8)]),
       'end': K('Closing line', ['Photo'], [('line', 'Closing line', 'everything that makes you feel alive.  >>>')], [FULL(0), SHADE(0, 420, 140, 0), TX('line', 540, 150, SERIF_I, 42, wrap=900)])},
      ['cover', 'mosaic', ('word', {'word': 'Silence'}), ('word', {'word': 'Scale'}), ('word', {'word': 'Stillness'}), ('word', {'word': 'Cowbells'}), ('word', {'word': 'Thin air'}), 'end']))

add(T('big_word', 'Big word poster', 'Your references',
      'Full photo, a small lead-in and one huge chunky word: “you need to TRAVEL because…”, continued across slides.', '@sliceofmumbai', ('summer', 0.8),
      {'poster': K('Poster', ['Photo'], [('lead', 'Small line above', 'you need to'), ('word', 'Big word', 'travel'), ('tail', 'Small line below', 'because…')],
                   [FULL(0), SHADE(0, 640, 130, 0), TX('lead', 540, 150, SANS_L, 46), TX('word', 540, 205, COOPER, 210, color=YELLOW, fit=980, shadow=150, sblur=10),
                    TX('tail', 540, 455, SANS_L, 42)])},
      [('poster', {}), ('poster', {'lead': 'your soul needs', 'word': 'new air', 'tail': ''}), ('poster', {'lead': 'you need to escape the', 'word': 'usual', 'tail': ''}),
       ('poster', {'lead': 'new places bring new', 'word': 'perspectives', 'tail': ''}), ('poster', {'lead': 'but don’t forget to', 'word': 'travel responsibly', 'tail': ''})]))

add(T('quote_parts', 'One quote across slides', 'Your references',
      'A well-known saying split over the slides, one playful phrase per photo.', '@muskansafar_', ('warm', 0.8),
      {'part': K('Phrase', ['Photo'], [('small', 'Small words', 'there is a'), ('big', 'Big words', 'saying')],
                 [FULL(0), SHADE(0, 560, 120, 0), TX('small', 540, 150, INK_F, 66, color=CREAM), TX('big', 540, 232, BERLIN, 172, color=CREAM, fit=980, case='upper', shadow=160, sblur=10)])},
      [('part', {}), ('part', {'small': 'yesterday is', 'big': 'history'}), ('part', {'small': 'tomorrow is a', 'big': 'mystery'}),
       ('part', {'small': 'today is a', 'big': 'gift'}), ('part', {'small': 'that is why it is called', 'big': 'the present'})]))

add(T('city_letters', 'City letters (visual diary)', 'Your references',
      'A cover with the place name in giant letters filled with photos, then a labelled contact sheet and collage pages.', '@ayazafe', ('faded', 0.6),
      {'cover': K('Letters cover', PH(6, 'Letter') + ['Portrait'], [('place', 'Place (up to 6 letters)', 'PARIS'), ('side', 'Small vertical words', 'MEMORIES FROM')],
                  [P(6, 470, 50, 560, 1250, radius=8), dict(t='mask', field='place', slots=[0, 1, 2, 3, 4, 5], rect=(40, 50, 400, 1250), font=IMPACT, dir='v'),
                   TX('side', 452, 675, GOTH, 20, anchor='mm', rot=90, case='spaced', **ink())], bg=OFFWHITE),
       'sheet': K('Contact sheet', PH(9), [(f'l{i}', f'Label {i + 1}', '[ place ]') for i in range(9)],
                  grid(range(9), 60, 90, 3, 300, 330, 30, 72) + [TX(f'l{i}', 60 + (i % 3) * 330 + 150, 90 + (i // 3) * 402 + 338, MONO, 20, **ink(color=MUTED)) for i in range(9)], bg=OFFWHITE),
       'collage': K('Collage', PH(3), [('note', 'Note', 'the best of times')],
                    [P(0, 70, 90, 560, 700, rot=-4, shadow=90), P(1, 520, 520, 500, 620, rot=5, shadow=90), P(2, 110, 880, 360, 360, border=14, rot=-8, shadow=90),
                     TX('note', 780, 1210, INK_F, 44, rot=4, **ink())], bg=OFFWHITE)},
      ['cover', 'sheet', 'collage', ('collage', {'note': 'a visual diary'}), 'sheet']))

add(T('contact_sheet', 'Contact sheet with labels', 'Your references',
      'A clean 3×3 sheet of photos with small bracketed place labels, like a photographer’s contact print.', '@ayazafe', ('natural', 0.8),
      {'sheet': K('Sheet', PH(9), [('title', 'Title', 'a visual diary')] + [(f'l{i}', f'Label {i + 1}', '[ place ]') for i in range(9)],
                  [TX('title', 540, 52, GOTH, 26, track=8, case='upper', **ink())] + grid(range(9), 60, 120, 3, 300, 330, 30, 66) +
                  [TX(f'l{i}', 60 + (i % 3) * 330 + 150, 120 + (i // 3) * 396 + 338, MONO, 20, **ink(color=MUTED)) for i in range(9)], bg=OFFWHITE)},
      [('sheet', {'title': 'a visual diary'}), ('sheet', {'title': 'part two'}), ('sheet', {'title': 'part three'})]))

add(T('grid9', 'Photo dump 3×3', 'Your references',
      'Nine photos per slide in a tight grid, each slide one mood (water, old towns, mountains…).', '@reispackers', ('natural', 0.8),
      {'grid': K('Nine photos', PH(9), [], grid(range(9), 0, 0, 3, 357, 447, 4, 4), bg=(10, 10, 10))},
      ['grid'] * 4))

add(T('frame_in_frame', 'Frame in frame', 'Your references',
      'A full photo with a white-bordered second photo laid over it in matching colours.', '@picsbydash', ('moody', 0.7),
      {'ff': K('Frame in frame', ['Background photo', 'Framed photo'], [('caption', 'Caption (optional)', '')],
               [FULL(0), P(1, 150, 300, 520, 680, border=18, shadow=120), TX('caption', 540, 1240, SERIF_I, 36, shadow=170)])},
      ['ff'] * 6))

add(T('polaroid_inset', 'Polaroid on a photo', 'Your references',
      'A full photo with a tilted polaroid and a handwritten note on it.', '@_nikhiiiil_ / @elleshungry', ('warmfilm', 0.8),
      {'pi': K('Photo + polaroid', ['Background photo', 'Polaroid'], [('note', 'Note on the polaroid', 'hello, europe :)')],
               [FULL(0), P(1, 600, 800, 360, 360, border=18, pb=70, rot=-6, shadow=130), TX('note', 760, 1222, HAND, 30, anchor='mm', rot=-6, **ink())])},
      [('pi', {}), ('pi', {'note': 'best day'}), ('pi', {'note': 'wish you were here'}), ('pi', {'note': 'again, please'}), ('pi', {'note': 'golden hour'})]))

add(T('film_strip', '35mm film frames (seamless)', 'Your references',
      'One film strip with sprocket holes runs through every slide; each slide is one frame.', 'crsel.app', ('warmfilm', 0.9),
      {'frame': K('Film frame', ['Frame photo'], [('num', 'Frame number', '14'), ('caption', 'Caption (optional)', '')],
                  [P(0, 40, 330, 1000, 700), TX('num', 60, 1038, MONO, 22, anchor='lt', color=(232, 150, 60), shadow=0),
                   ST('EUROPE  400TX', 1020, 1038, MONO, 22, anchor='rt', color=(232, 150, 60), shadow=0), TX('caption', 540, 1190, SERIF_I, 36, **ink())])},
      [('frame', {'num': str(12 + i)}) for i in range(6)], strip=True, bg=('paper', (232, 226, 214)),
      strip_els=[dict(t='film', rect=(0, 230, -1, 890), hole=(232, 226, 214))]))

add(T('build_up', 'Build-up word (sooo…)', 'Your references',
      'One stretched word runs across the slides over your photos, and the last slide pays it off.', '@slaythestrategy.agency', ('moody', 0.7),
      {'start': K('Start (the long word)', ['Photo'], [('word', 'The long word', 'we were sooooooooooooo')],
                  [FULL(0, dim=0.3), TX('word', 80, 520, COOPER, 230, anchor='lt', color=CREAM, z=2, shadow=150, sblur=12)]),
       'photo': K('Photo', ['Photo'], [], [FULL(0, dim=0.3)]),
       'payoff': K('Payoff', ['Photo'], [('payoff', 'Payoff line', '…in love with Europe.')], [FULL(0, dim=0.3), TX('payoff', 540, 640, SERIF_I, 84, wrap=900, valign='middle')])},
      ['start', 'photo', 'photo', 'payoff'], strip=True))

add(T('script_place', 'Big handwritten place name', 'Your references',
      'A full photo with the place name in big handwriting and a small polaroid peeking in.', '@_nikhiiiil_ (jaipur)', ('golden', 0.7),
      {'cover': K('Cover', ['Photo', 'Small polaroid'], [('place', 'Place', 'dubrovnik')],
                  [FULL(0), TX('place', 540, 330, SCRIPT, 176, rot=7, fit=1000, shadow=160, sblur=10), P(1, 770, 60, 250, 250, border=12, pb=40, rot=8, shadow=120)]),
       'photo': K('Photo', ['Photo'], [('note', 'Note', 'hello, dubrovnik :)')], [FULL(0), TX('note', 540, 1230, HAND, 38, shadow=170)])},
      ['cover', 'photo', ('photo', {'note': 'the old town at night'}), ('photo', {'note': 'sea days'}), ('photo', {'note': 'see you again'})]))

add(T('pixel_stretch', 'Pixel-stretch dump', 'Your references',
      'Photos with their edge pixels stretched into bands of colour, with a big script title on the cover.', '@zaps_design (Rome dump)', ('vivid', 0.6),
      {'cover': K('Cover', ['Photo'], [('place', 'Place', 'Paris'), ('word', 'Second word', 'dump')],
                  [P(0, 0, 0, W, H, stretch=('right', 0.3)), TX('place', 470, 230, SCRIPT, 190, shadow=150), TX('word', 600, 430, BODONI, 140, shadow=150)]),
       'two': K('Two photos', ['Left photo', 'Right photo'], [], [P(0, 0, 0, 540, H, stretch=('right', 0.35)), P(1, 540, 0, 540, H, stretch=('left', 0.35))])},
      ['cover', 'two', 'two', 'two', 'two']))

add(T('panorama', 'Panorama across slides', 'Your references',
      'One wide photo cut across two or three slides, so the swipe feels like turning your head.', '@youknowprateek', ('natural', 0.8),
      {'pano3': K('Panorama over 3 slides', ['Wide photo'], [('caption', 'Caption', 'there are a lot of places waiting to be photographed')],
                  [P(0, 0, 0, 3 * W, H), SHADE(1050, 300, 0, 150, w=3 * W), TX('caption', 80, 1250, SERIF_I, 40, anchor='lb', shadow=170)]),
       'pano2': K('Panorama over 2 slides', ['Wide photo'], [('caption', 'Caption', '')], [P(0, 0, 0, 2 * W, H), TX('caption', 80, 1250, SERIF_I, 40, anchor='lb', shadow=170)]),
       'cont': K('…panorama continues', [], [], [])},
      ['pano3', 'cont', 'cont', 'pano2', 'cont'], strip=True))

add(T('story_notes', 'Handwritten story', 'Your references',
      'Dark, moody photos with a short story in white handwriting, one thought per slide.', '@theresa.notes', ('moody', 0.8),
      {'note': K('Story slide', ['Photo'], [('text', 'Words', 'Most people skip this town on the way to the lakes…')],
                 [FULL(0, dim=0.45), TX('text', 110, 170, INK_F, 56, anchor='lt', wrap=860, lh=1.3, shadow=130)])},
      [('note', {}), ('note', {'text': 'but we stayed for three nights.'}), ('note', {'text': 'The magic wasn’t in the sights. It was in the slow mornings.'}),
       ('note', {'text': 'Nobody was in a hurry. Not even us.'}), ('note', {'text': 'So here’s my advice: stay one more night. →'})]))

add(T('skip_stay', 'Skip vs stay', 'Your references',
      'Two photos side by side, the one people scroll past and the one they stop for, with a short “why”.', '@camilaatunoni', ('natural', 0.8),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'Photos they skip vs. stay for'), ('sub', 'Small line', 'travel edition')],
                  [P(0, 290, 520, 500, 620, radius=16, rot=-3, shadow=90), TX('title', 540, 150, COOPER, 86, wrap=900, **ink(color=RED)), TX('sub', 540, 1220, GOTH_B, 26, track=6, case='upper', **ink())],
                  bg=('paper', (246, 240, 228))),
       'pair': K('Skip / stay', ['Skip photo', 'Stay photo'], [('label', 'Topic', 'Travel highlights'), ('why', 'Why?', 'The second one has a person in it, so it feels like a moment, not a postcard.')],
                 [TX('label', 540, 80, GOTH, 24, track=8, case='upper', **ink()), ST('Skip', 290, 160, SERIF_I, 70, **ink(color=RED)), ST('Stay', 790, 160, SERIF_I, 70, **ink(color=RED)),
                  P(0, 60, 270, 460, 600, radius=14, shadow=60), P(1, 560, 270, 460, 600, radius=14, shadow=60), ST('Why?', 540, 920, SERIF_I, 56, **ink()),
                  TX('why', 540, 1010, SANS, 32, wrap=860, **ink(color=BODY))], bg=('paper', (246, 240, 228)))},
      ['cover', 'pair', ('pair', {'label': 'Mountain views', 'why': 'Shoot through something (a window, trees) and the view gets depth.'}),
       ('pair', {'label': 'Old towns', 'why': 'Golden hour light beats noon light, every time.'}), ('pair', {'label': 'Lakes', 'why': 'A still reflection doubles the scene for free.'})]))

add(T('before_after', 'Before / after edit', 'Your references',
      'Your unedited photo next to your edit, split down the middle — great for showing your editing.', '@fizzaandalgorithm (ugly vs viral)', ('none', 0.0),
      {'ba': K('Before / after', ['Before (unedited)', 'After (edited)'], [('caption', 'Caption', '')],
               [P(0, 0, 0, 538, H), P(1, 542, 0, 538, H), RC(538, 0, 4, H, WHITE), RC(30, 40, 190, 56, (0, 0, 0, 150), radius=28), ST('BEFORE', 125, 52, GOTH_B, 24, track=4, shadow=0),
                RC(860, 40, 190, 56, (0, 0, 0, 150), radius=28), ST('AFTER', 955, 52, GOTH_B, 24, track=4, shadow=0), TX('caption', 540, 1250, SERIF_I, 36, shadow=170)])},
      ['ba'] * 5))

add(T('myth_fact', 'Myth vs fact', 'Your references',
      'A photo on top and a cream card below busting a common travel myth.', '@ig.aryaman', ('natural', 0.8),
      {'mf': K('Myth / fact', ['Photo'], [('myth', 'Myth', 'Switzerland is only for big budgets'), ('fact', 'Fact', 'Trains, picnics and free viewpoints make it far cheaper than you think.')],
               [P(0, 0, 0, W, 780), RC(0, 780, W, 570, CREAM), ST('MYTH', 90, 830, GOTH_B, 30, track=6, anchor='lt', **ink(color=RED)),
                TX('myth', 90, 880, SERIF, 48, anchor='lt', wrap=900, **ink()), ST('FACT', 90, 1060, GOTH_B, 30, track=6, anchor='lt', **ink(color=GREEN)),
                TX('fact', 90, 1110, SANS, 34, anchor='lt', wrap=900, **ink(color=BODY))])},
      [('mf', {}), ('mf', {'myth': 'You need a car to see the Alps', 'fact': 'Trains and cable cars reach almost every view worth seeing.'}),
       ('mf', {'myth': 'Old towns are only busy in summer', 'fact': 'Go early in the morning and you have them to yourself, any month.'}),
       ('mf', {'myth': 'Good photos need a big camera', 'fact': 'Light and patience matter more than the gear.'})]))

add(T('lessons', 'Lessons I learned (numbered)', 'Your references',
      'A big number and one lesson per photo, with a cover that promises the list.', '@ig.aryaman (lessons & advice)', ('cinematic', 0.7),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'Lessons I learned travelling Europe')],
                  [FULL(0), SHADE(700, 650, 0, 210), TX('title', 540, 1100, GOTH_B, 70, wrap=920, valign='bottom'), ST('swipe  →', 540, 1240, SANS, 26)]),
       'lesson': K('Lesson', ['Photo'], [('num', 'Number', '01'), ('lesson', 'Lesson', 'Stay one more night than you planned.')],
                   [FULL(0), SHADE(650, 700, 0, 210), TX('num', 80, 110, BODONI, 220, anchor='lt', alpha=235), TX('lesson', 80, 1010, SERIF, 54, anchor='lt', wrap=920)])},
      ['cover', ('lesson', {}), ('lesson', {'num': '02', 'lesson': 'The best views are usually a short walk from the crowd.'}),
       ('lesson', {'num': '03', 'lesson': 'Golden hour is worth the early alarm.'}), ('lesson', {'num': '04', 'lesson': 'Pack half the clothes, bring twice the memory cards.'}),
       ('lesson', {'num': '05', 'lesson': 'Put the phone down for the best moment. Then take the photo.'})]))

add(T('hot_take', 'Hot take', 'Your references',
      'A bold, slightly controversial travel opinion in big type over a dimmed photo.', '@ig.aryaman (hot takes)', ('drama', 0.7),
      {'take': K('Hot take', ['Photo'], [('take', 'Hot take', 'The best views in Switzerland are free')],
                 [FULL(0, dim=0.4), ST('H O T   T A K E', 540, 200, GOTH_B, 26, color=ORANGE), TX('take', 540, 620, IMPACT, 104, wrap=920, valign='middle', case='upper', lh=1.05),
                  ST('agree?', 540, 1170, HAND, 44)])},
      [('take', {}), ('take', {'take': 'Sunrise beats sunset, every time'}), ('take', {'take': 'Slow travel is better than seeing it all'}), ('take', {'take': 'A lake town beats a big city'})]))

add(T('cheat_sheet', 'Trip cheat sheet', 'Your references',
      'A save-worthy sheet of quick tips for one place, with a round photo — fill in your own facts.', '@ig.aryaman (cheat sheet)', ('natural', 0.8),
      {'sheet': K('Cheat sheet', ['Round photo'], [('title', 'Title', 'Dubrovnik cheat sheet')] + [(f'k{i}', f'Label {i}', l) for i, l in enumerate(['Best time', 'Getting around', 'Must do', 'Must eat', 'My tip'], 1)] +
                  [(f'v{i}', f'Tip {i}', '[your tip here]') for i in range(1, 6)],
                  [TX('title', 80, 90, GOTH_B, 58, anchor='lt', case='upper', wrap=620, **ink()), P(0, 770, 70, 250, 250, radius=125, shadow=60)] +
                  sum([[TX(f'k{i}', 80, 420 + (i - 1) * 172, GOTH_B, 26, anchor='lt', track=3, case='upper', **ink(color=ORANGE)),
                        TX(f'v{i}', 80, 462 + (i - 1) * 172, SANS, 34, anchor='lt', wrap=920, **ink()),
                        LN([(80, 560 + (i - 1) * 172), (1000, 560 + (i - 1) * 172)], color=(205, 195, 180), width=2)] for i in range(1, 6)], []),
                  bg=('paper', (246, 240, 228))),
       'photo': K('Photo', ['Photo'], [('caption', 'Caption', '')], [FULL(0), TX('caption', 540, 1240, SERIF_I, 38, shadow=170)])},
      ['sheet', 'photo', 'photo']))

add(T('do_dont', 'Do’s and don’ts', 'Your references',
      'Top photo: what not to do. Bottom photo: what to do instead.', '@fizzaandalgorithm', ('natural', 0.8),
      {'dd': K('Don’t / do', ['Don’t photo', 'Do photo'], [('dont', 'Don’t…', 'rush through the old town at noon'), ('do', 'Do…', 'come back at golden hour')],
               [P(0, 0, 0, W, 675), P(1, 0, 675, W, 675), RC(40, 40, 210, 62, RED + (235,), radius=31), ST('DON’T', 145, 54, GOTH_B, 28, track=4, shadow=0),
                TX('dont', 540, 600, SERIF, 46, wrap=940, valign='bottom', shadow=180, sblur=8),
                RC(40, 715, 150, 62, GREEN + (235,), radius=31), ST('DO', 115, 729, GOTH_B, 28, track=4, shadow=0), TX('do', 540, 1270, SERIF, 46, wrap=940, valign='bottom', shadow=180, sblur=8)])},
      [('dd', {}), ('dd', {'dont': 'stand where everyone stands', 'do': 'walk five minutes further'}),
       ('dd', {'dont': 'shoot straight into harsh sun', 'do': 'turn around and shoot with the light'}), ('dd', {'dont': 'skip the small villages', 'do': 'stay a night in one'})]))

add(T('finger_down', 'Put a finger down (travel edition)', 'Your references',
      'An interactive list: “put a finger down if you…”, one relatable travel moment per photo.', '@yoursocialteam', ('summer', 0.7),
      {'fd': K('One line', ['Photo'], [('line', 'Line', 'missed a train in Switzerland')],
               [FULL(0, dim=0.35), ST('put a finger down if you…', 540, 170, HAND, 44, color=CREAM), TX('line', 540, 650, BERLIN, 90, wrap=920, valign='middle'),
                ST('T R A V E L   E D I T I O N', 540, 1225, GOTH, 22)])},
      [('fd', {}), ('fd', {'line': 'ate gelato before breakfast'}), ('fd', {'line': 'cried at a view'}), ('fd', {'line': 'took 300 photos of one lake'}),
       ('fd', {'line': 'got lost in an old town on purpose'})]))

add(T('swipe_puzzle', 'Swipe puzzle (one photo in tiles)', 'Your references',
      'One photo spread over three slides and cut into tiles; it only comes together as you swipe.', '@yoursocialteam (swipe puzzle)', ('natural', 0.8),
      {'puzzle': K('Puzzle (3 slides)', ['Big photo'], [], [P(0, 60, 60, 3 * W - 120, H - 120)] +
                   [RC(x - 9, 0, 18, H, CREAM, z=1) for x in (540, 1080, 1620, 2160, 2700)] + [RC(0, 666, 3 * W, 18, CREAM, z=1)]),
       'cont': K('…puzzle continues', [], [], [])},
      ['puzzle', 'cont', 'cont'], strip=True, bg=CREAM))

add(T('reveal', 'Swipe to reveal', 'Your references',
      'A blurred teaser slide (“guess where we woke up”), then the same photo, sharp.', '@yoursocialteam (swipe to reveal)', ('natural', 0.8),
      {'tease': K('Teaser (blurred)', ['Photo (shown blurred)'], [('tease', 'Teaser', 'guess where we woke up today')],
                  [FULL(0, blur=30, dim=0.2), TX('tease', 540, 620, SERIF_I, 68, wrap=880, valign='middle'), ST('swipe to reveal  →', 540, 1180, GOTH, 26, track=4)]),
       'reveal': K('Reveal', ['Photo'], [('caption', 'Caption', 'Lake Bled, 7am')], [FULL(0), TX('caption', 540, 1240, SERIF_I, 40, shadow=170)])},
      ['tease', 'reveal', ('tease', {'tease': 'and where we had dinner'}), ('reveal', {'caption': 'Dubrovnik old town'})]))

add(T('route_line', 'Follow the route (seamless)', 'Your references',
      'A dashed travel route with a little plane runs from slide to slide, linking one photo card per stop.', '@yoursocialteam (follow the line / travelling icon)', ('faded', 0.7),
      {'cover': K('Cover', [], [('title', 'Title', 'our route through Europe'), ('sub', 'Small line', '17 places · one summer')],
                  [TX('title', 540, 420, COOPER, 100, wrap=900, **ink(color=TERRA)), TX('sub', 540, 760, HAND, 40, **ink(color=MUTED)),
                   dict(t='route', a=(640, 900), b=(230, 560), bend=200, z=0, color=(150, 110, 80))]),
       'up': K('Stop (high)', ['Photo'], [('place', 'Place', 'Bled'), ('when', 'When', 'day 3')],
               [P(0, 230, 160, 620, 760, radius=18, shadow=90), TX('place', 540, 965, GOTH_B, 44, case='upper', track=4, **ink()), TX('when', 540, 1030, HAND, 32, **ink(color=MUTED)),
                dict(t='route', a=(850, 540), b=(230, 720), bend=220, z=0, color=(150, 110, 80))]),
       'down': K('Stop (low)', ['Photo'], [('place', 'Place', 'Dubrovnik'), ('when', 'When', 'day 6')],
                 [P(0, 230, 330, 620, 760, radius=18, shadow=90), TX('place', 540, 1135, GOTH_B, 44, case='upper', track=4, **ink()), TX('when', 540, 1200, HAND, 32, **ink(color=MUTED)),
                  dict(t='route', a=(850, 710), b=(230, 540), bend=-220, z=0, color=(150, 110, 80))]),
       'end': K('End', [], [('end', 'Closing line', 'where should we go next?')], [TX('end', 540, 620, SERIF_I, 76, wrap=900, valign='middle', **ink())])},
      ['cover', ('up', {'place': 'Lucerne', 'when': 'day 1'}), ('down', {'place': 'Mürren', 'when': 'day 3'}), ('up', {'place': 'Bled', 'when': 'day 6'}),
       ('down', {'place': 'Dubrovnik', 'when': 'day 9'}), ('up', {'place': 'Paris', 'when': 'day 14'}), 'end'], strip=True, bg=('paper', (238, 232, 220))))

add(T('strips_cover', 'Letter strips + full photos', 'Your references',
      'A cover of vertical photo strips with one letter on each, then full photos with spaced captions.', 'mahemac / untitled.storiez', ('faded', 0.85),
      {'strips': K('Letter strips cover', PH(6, 'Strip'), [('letters', 'Letters (one per strip)', 'EUROPE'), ('sub', 'Small line', 'P O S T C A R D S')],
                   [P(i, i * 180 + 2, 0, 176, H) for i in range(6)] + [dict(t='chars', field='letters', xs=[90 + i * 180 for i in range(6)], y=800, font=SANS_L, size=64),
                                                                         TX('sub', 540, 900, GOTH, 24, track=4, shadow=170)], bg=(20, 18, 16)),
       'photo': K('Photo', ['Photo'], [('caption', 'Caption', 'BLED · SLOVENIA')], [FULL(0), SHADE(1080, 270, 0, 150), TX('caption', 540, 1240, GOTH, 24, track=8, case='upper')])},
      ['strips', ('photo', {'caption': 'LUCERNE · SWITZERLAND'}), ('photo', {'caption': 'MÜRREN · SWITZERLAND'}), ('photo', {'caption': 'DUBROVNIK · CROATIA'}),
       ('photo', {'caption': 'BLED · SLOVENIA'}), ('photo', {'caption': 'PARIS · FRANCE'})]))

add(T('scrapbook', 'Scrapbook pages', 'Your references',
      'Paper background, tilted photos with tape and a handwritten note.', '@millieameliacreates / @deepwithocean', ('vintage', 0.6),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'our europe scrapbook')],
                  [TX('title', 540, 200, SCRIPT_B, 104, rot=-3, wrap=900, **ink()), P(0, 240, 520, 600, 640, border=16, rot=2, shadow=90), TAPE(455, 498, rot=-4)], bg=('paper', (236, 228, 212))),
       'page': K('Page', ['Photo 1', 'Photo 2'], [('note', 'Handwritten note', 'the day we got lost (on purpose)')],
                 [P(0, 70, 90, 600, 720, border=16, rot=-3, shadow=90), TAPE(290, 72, rot=-6), P(1, 520, 640, 480, 560, border=16, rot=4, shadow=90), TAPE(690, 620, rot=8),
                  TX('note', 290, 1060, HAND, 40, rot=3, wrap=430, **ink())] + arrow(330, 1180, 500, 1110), bg=('paper', (236, 228, 212)))},
      ['cover', 'page', ('page', {'note': 'best gelato of the trip'}), ('page', {'note': 'we could live here'}), ('page', {'note': 'missing this already'})]))

# ================================================================== From the web (travel carousel trends)
add(T('taped_polaroids', 'Taped polaroids on a faded photo', 'Polaroids & paper',
      'Three tilted, taped polaroids over a soft, faded street photo, with a script note.', 'web: Orshot travel layout', ('faded', 0.8),
      {'page': K('Page', ['Faded background', 'Polaroid 1', 'Polaroid 2', 'Polaroid 3'], [('note', 'Script note', 'summer in Europe')],
                 [FULL(0), RC(0, 0, W, H, (250, 246, 238, 120)), P(1, 100, 120, 420, 420, border=16, pb=80, rot=-7, shadow=110), TAPE(225, 100, rot=-12),
                  P(2, 560, 360, 420, 420, border=16, pb=80, rot=6, shadow=110), TAPE(690, 340, rot=8), P(3, 190, 760, 420, 420, border=16, pb=80, rot=-2, shadow=110), TAPE(320, 742, rot=3),
                  TX('note', 820, 1180, SCRIPT, 52, rot=-6, **ink())])},
      [('page', {}), ('page', {'note': 'little moments'}), ('page', {'note': 'slow days'}), ('page', {'note': 'until next time'})]))

add(T('sage_polaroids', 'Two polaroids on sage paper', 'Polaroids & paper',
      'A sage textured page with two tilted polaroids, handwritten marker captions and a hand-drawn arrow.', 'web: Orshot sage layout', ('natural', 0.7),
      {'page': K('Page', ['Polaroid 1', 'Polaroid 2'], [('c1', 'Caption 1', 'first coffee by the lake'), ('c2', 'Caption 2', 'and then this view')],
                 [P(0, 90, 140, 520, 540, border=18, pb=90, rot=-5, shadow=100), P(1, 470, 640, 500, 500, border=18, pb=90, rot=6, shadow=100),
                  TX('c1', 330, 790, HAND, 34, rot=-5, **ink()), TX('c2', 740, 1250, HAND, 34, rot=6, **ink())] + arrow(560, 820, 660, 900), bg=('paper', SAGE))},
      [('page', {}), ('page', {'c1': 'morning walk', 'c2': 'worth every step'}), ('page', {'c1': 'the old town', 'c2': 'at golden hour'})]))

add(T('notebook_dump', 'Spiral notebook photo dump', 'Polaroids & paper',
      'A lined notebook page over a blurred photo, with polaroids and a handwritten diary line.', 'web: Orshot notebook dump', ('warmfilm', 0.6),
      {'page': K('Notebook page', ['Background (blurred)', 'Photo 1', 'Photo 2'], [('date', 'Date', 'oct 3'), ('note', 'Diary line', 'we said one more day, and stayed three')],
                 [dict(t='bgphoto', slot=0, dim=0.3), RC(110, 100, 900, 1150, (251, 249, 242), radius=12, shadow=130)] +
                 [LN([(150, y), (980, y)], color=(196, 214, 232), width=2) for y in range(240, 1220, 52)] +
                 [RC(82, y, 56, 22, (196, 196, 202), radius=11) for y in range(140, 1220, 74)] +
                 [P(1, 190, 210, 340, 340, border=12, pb=50, rot=-4, shadow=80), P(2, 560, 300, 360, 360, border=12, pb=50, rot=5, shadow=80),
                  TX('date', 870, 140, HAND, 30, **ink(color=(150, 60, 50))), TX('note', 560, 900, HAND, 46, rot=-2, wrap=720, **ink(color=(40, 60, 120)))])},
      [('page', {}), ('page', {'date': 'oct 6', 'note': 'the water was this colour, really'}), ('page', {'date': 'oct 9', 'note': 'best meal of the trip'})]))

add(T('seamless_scrapbook', 'Seamless scrapbook', 'Seamless (cross the edges)',
      'Scrapbook pages where photos sit across the slide edges, with tape, notes and doodled arrows.', 'web: ivorymix seamless scrapbook guide', ('vintage', 0.6),
      {'page': K('Page', ['Photo', 'Photo across the edge'], [('note', 'Note', 'day one')],
                 [P(0, 80, 160, 560, 700, border=16, rot=-4, shadow=90), TAPE(300, 140, rot=-8), P(1, 780, 520, 520, 620, border=16, rot=5, shadow=90), TAPE(990, 500, rot=6),
                  TX('note', 330, 1000, HAND, 44, rot=-3, **ink())] + arrow(420, 1100, 700, 1030)),
       'last': K('Last page', ['Photo'], [('note', 'Note', 'the end (for now)')],
                 [P(0, 240, 200, 600, 760, border=16, rot=2, shadow=90), TAPE(470, 180, rot=-4), TX('note', 540, 1080, SCRIPT, 56, rot=-2, **ink())])},
      [('page', {'note': 'day one'}), ('page', {'note': 'getting lost'}), ('page', {'note': 'found this'}), ('page', {'note': 'and this'}), 'last'],
      strip=True, bg=('paper', (236, 228, 212))))

add(T('itinerary', 'X days in a place (itinerary)', 'Guides & tips',
      'A cover (“3 days in…”), one slide per day with morning/afternoon/evening, and a save-this ending. Add your own facts.', 'web: Carouselmaker / Moda itineraries', ('natural', 0.8),
      {'cover': K('Cover', ['Photo'], [('days', 'Days', '3 days in'), ('place', 'Place', 'Lucerne')],
                  [FULL(0), SHADE(0, 640, 140, 0), TX('days', 540, 200, GOTH, 32, track=12, case='upper'), TX('place', 540, 250, BODONI, 180, fit=980, case='upper'),
                   SHADE(1050, 300, 0, 160), ST('save this for your trip', 540, 1235, SANS, 28)]),
       'day': K('Day', ['Photo'], [('day', 'Day', 'Day 1'), ('title', 'Title', 'Old town & the lake'),
                                   ('plan', 'Plan', 'Morning — [first stop]\nAfternoon — [lunch spot], then a slow walk\nEvening — sunset at [viewpoint]')],
                [P(0, 0, 0, W, 800), RC(0, 800, W, 550, CREAM), TX('day', 80, 850, GOTH_B, 28, anchor='lt', track=8, case='upper', **ink(color=ORANGE)),
                 TX('title', 80, 900, SERIF, 62, anchor='lt', wrap=920, **ink()), TX('plan', 80, 1010, SANS, 30, anchor='lt', wrap=920, lh=1.45, **ink(color=BODY))]),
       'end': K('Save it', ['Photo'], [('cta', 'Closing line', 'Save this for your trip'), ('sub', 'Small line', 'and send it to your travel buddy')],
                [FULL(0, dim=0.4), TX('cta', 540, 600, SERIF_I, 80, wrap=900, valign='middle'), TX('sub', 540, 760, SANS_L, 34)])},
      ['cover', ('day', {}), ('day', {'day': 'Day 2', 'title': 'Up the mountain'}), ('day', {'day': 'Day 3', 'title': 'Lakeside villages'}), 'end']))

add(T('micro_itinerary', 'One perfect day (timeline)', 'Guides & tips',
      'A single day as a vertical timeline: times, places and round photos.', 'web: micro-itinerary carousels', ('natural', 0.8),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'One perfect day in Bled')], [FULL(0), SHADE(800, 550, 0, 200), TX('title', 540, 1200, GOTH_B, 72, wrap=920, valign='bottom')]),
       'day': K('Timeline', PH(4, 'Stop'), [('title', 'Title', 'the plan')] + sum([[(f't{i}', f'Time {i + 1}', tm), (f'd{i}', f'Stop {i + 1}', dd)] for i, (tm, dd) in
                                                                                  enumerate([('08:00', 'Coffee by the lake'), ('11:00', 'Walk up to the viewpoint'), ('14:00', 'Lunch in the village'), ('19:00', 'Sunset from the shore')])], []),
                 [TX('title', 80, 80, GOTH_B, 50, anchor='lt', case='upper', **ink()), LN([(200, 230), (200, 1240)], color=(195, 185, 170), width=3)] +
                 sum([[P(i, 120, 250 + i * 250, 160, 160, radius=80, shadow=60), TX(f't{i}', 320, 270 + i * 250, GOTH_B, 30, anchor='lt', **ink(color=ORANGE)),
                       TX(f'd{i}', 320, 316 + i * 250, SERIF, 44, anchor='lt', wrap=680, **ink())] for i in range(4)], []), bg=CREAM)},
      ['cover', 'day']))

add(T('alternatives', 'Instead of X, try Y', 'Guides & tips',
      'Side-by-side alternatives to a famous, crowded spot, with why the quieter one is worth it.', 'web: “alternatives to a famous attraction” idea', ('natural', 0.8),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'Skip the crowds: try these instead')],
                  [TX('title', 540, 160, COOPER, 88, wrap=900, **ink(color=TERRA)), P(0, 240, 560, 600, 640, radius=16, shadow=90)], bg=('paper', (246, 240, 228))),
       'alt': K('Instead / try', ['Instead of…', 'Try…'], [('a', 'The famous spot', 'the crowded viewpoint'), ('b', 'The alternative', 'the quiet lake next door'), ('why', 'Why', 'Same mountains, a tenth of the people, and a bench all to yourself.')],
                [ST('INSTEAD OF', 285, 80, GOTH_B, 26, track=6, **ink(color=MUTED)), ST('TRY', 795, 80, GOTH_B, 26, track=6, **ink(color=ORANGE)),
                 P(0, 50, 140, 470, 640, radius=14, shadow=60, mono=True), P(1, 560, 140, 470, 640, radius=14, shadow=60),
                 ST('→', 540, 460, SYM, 70, anchor='mm', **ink(color=ORANGE)), TX('a', 285, 810, SERIF, 42, wrap=440, **ink()), TX('b', 795, 810, SERIF, 42, wrap=440, **ink()),
                 TX('why', 540, 1010, SANS, 32, wrap=900, **ink(color=BODY))], bg=('paper', (246, 240, 228)))},
      ['cover', 'alt', ('alt', {'a': 'the busiest old-town street', 'b': 'the lane one block behind it', 'why': 'Same stone, same light — and you can actually stop for a photo.'}), 'alt']))

add(T('top_list', 'Top list (numbered places)', 'Guides & tips',
      'A cover promising a list, then one place per slide with a big outlined number.', 'web: listicle carousels', ('vivid', 0.6),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', '7 places in Europe that felt unreal')], [FULL(0), SHADE(700, 650, 0, 210), TX('title', 540, 1190, GOTH_B, 74, wrap=920, valign='bottom')]),
       'item': K('Place', ['Photo'], [('num', 'Number', '01'), ('place', 'Place', 'Lake Bled'), ('line', 'One line', 'the church on the island, at sunrise')],
                 [FULL(0), SHADE(650, 700, 0, 210), TX('num', 80, 760, GOTH_B, 200, anchor='lt', outline=True, stroke=3, shadow=0),
                  TX('place', 80, 1030, GOTH_B, 58, anchor='lt', case='upper', wrap=920), TX('line', 80, 1110, SERIF_I, 38, anchor='lt', wrap=920)])},
      ['cover', ('item', {}), ('item', {'num': '02', 'place': 'Mürren', 'line': 'a village on a cliff above the clouds'}),
       ('item', {'num': '03', 'place': 'Dubrovnik', 'line': 'walls, sea and golden streets'}), ('item', {'num': '04', 'place': 'Lucerne', 'line': 'the wooden bridge and the lake'})]))

add(T('cheat_grid', 'Packing / tips checklist', 'Guides & tips',
      'A checklist slide on paper (packing list, tips) between your photos.', 'web: saveable guide carousels', ('natural', 0.8),
      {'list': K('Checklist', [], [('title', 'Title', 'what I’d pack again')] + [(f'i{i}', f'Item {i + 1}', it) for i, it in
                                                                                enumerate(['comfy walking shoes', 'a light rain jacket', 'a power bank', 'a reusable bottle', 'one nice outfit', 'spare memory cards'])],
                 [TX('title', 90, 100, SCRIPT_B, 80, anchor='lt', **ink())] + sum([[RC(100, 330 + i * 150, 46, 46, None, outline=INK, width=4, radius=8),
                                                                                    ST('✓', 123, 353 + i * 150, SYM, 40, anchor='mm', **ink(color=GREEN)),
                                                                                    TX(f'i{i}', 180, 328 + i * 150, HAND, 40, anchor='lt', **ink())] for i in range(6)], []),
                 bg=('paper', (246, 240, 228))),
       'photo': K('Photo', ['Photo'], [], [FULL(0)])},
      ['photo', 'list', 'photo']))

# ================================================================== Frames, borders & editorial
add(T('gallery_mat', 'Gallery mat (minimal)', 'Editorial & minimal',
      'Each photo framed with a wide off-white mat and a small caption, like a print on a gallery wall.', 'classic minimal', ('natural', 0.8),
      {'print': K('Print', ['Photo'], [('caption', 'Caption', 'Bled, Slovenia'), ('meta', 'Small right text', 'October 2026')],
                  [P(0, 140, 150, 800, 960, shadow=40), TX('caption', 140, 1160, SERIF_I, 38, anchor='lt', **ink()), TX('meta', 940, 1170, GOTH, 20, anchor='rt', track=6, case='upper', **ink(color=MUTED))],
                  bg=(244, 241, 235))},
      [('print', {}), ('print', {'caption': 'Mürren, Switzerland'}), ('print', {'caption': 'Dubrovnik, Croatia'}), ('print', {'caption': 'Lucerne, Switzerland'}), ('print', {'caption': 'Paris, France'})]))

add(T('quote_card', 'Quote cards between photos', 'Editorial & minimal',
      'Full photos broken up by solid-colour quote slides.', 'classic', ('warmfilm', 0.7),
      {'photo': K('Photo', ['Photo'], [], [FULL(0)]),
       'olive': K('Quote (olive)', [], [('quote', 'Quote', 'Not all those who wander are lost.'), ('by', 'Who said it', 'J. R. R. Tolkien')],
                  [TX('quote', 540, 620, SERIF_I, 74, wrap=860, valign='middle', color=CREAM, shadow=0), TX('by', 540, 1000, GOTH, 22, track=8, case='upper', color=(222, 216, 198), shadow=0)], bg=OLIVE),
       'terra': K('Quote (terracotta)', [], [('quote', 'Quote', 'Take only memories, leave only footprints.'), ('by', 'Who said it', 'travel saying')],
                  [TX('quote', 540, 620, SERIF_I, 74, wrap=860, valign='middle', color=CREAM, shadow=0), TX('by', 540, 1000, GOTH, 22, track=8, case='upper', color=(240, 222, 206), shadow=0)], bg=TERRA)},
      ['photo', 'olive', 'photo', 'photo', 'terra', 'photo']))

add(T('editorial', 'Editorial spread (1 big + 2 small)', 'Editorial & minimal',
      'Magazine-style page: one large photo, two small ones, a headline and a few lines.', 'classic magazine layout', ('natural', 0.8),
      {'spread': K('Spread', ['Large photo', 'Small photo 1', 'Small photo 2'], [('head', 'Headline', 'Three days in the mountains'), ('body', 'Text', 'Slow mornings, long walks and the kind of quiet you can hear.')],
                   [P(0, 60, 60, 640, 900), P(1, 730, 60, 290, 430), P(2, 730, 520, 290, 440), TX('head', 60, 1010, BASK, 66, anchor='lt', wrap=960, **ink()),
                    TX('body', 60, 1160, SERIF, 32, anchor='lt', wrap=960, lh=1.35, **ink(color=BODY))], bg=OFFWHITE)},
      ['spread'] * 4))

add(T('magazine', 'Magazine cover + features', 'Editorial & minimal',
      'A magazine cover with a big masthead and cover lines, then feature pages.', 'classic magazine', ('cinematic', 0.6),
      {'cover': K('Cover', ['Cover photo'], [('mast', 'Masthead', 'EUROPE'), ('issue', 'Issue line', 'Issue 01 · Autumn 2026'), ('lines', 'Cover lines', '17 places\n2,199 clips\none summer'), ('quote', 'Quote', '“the trip we’ll talk about forever”')],
                  [FULL(0), SHADE(0, 420, 120, 0), TX('mast', 540, 30, BODONI, 240, fit=1010, case='upper', shadow=90), TX('issue', 540, 300, GOTH, 22, track=10, case='upper'),
                   TX('lines', 70, 820, GOTH_B, 42, anchor='lt', wrap=560, lh=1.25, case='upper', shadow=160), SHADE(1100, 250, 0, 150), TX('quote', 540, 1235, SERIF_I, 38, shadow=170)]),
       'feature': K('Feature page', ['Photo'], [('kicker', 'Small label', 'Switzerland'), ('head', 'Headline', 'Above the clouds'), ('body', 'Text', 'A village on a cliff, a cable car and an afternoon that didn’t want to end.')],
                    [P(0, 0, 0, W, 760), TX('kicker', 70, 810, GOTH_B, 22, anchor='lt', track=8, case='upper', **ink(color=ORANGE)), TX('head', 70, 860, BODONI, 100, anchor='lt', wrap=940, lh=1.0, **ink()),
                     TX('body', 70, 1090, SERIF, 32, anchor='lt', wrap=940, lh=1.35, **ink(color=BODY))], bg=OFFWHITE)},
      ['cover', 'feature', ('feature', {'kicker': 'Croatia', 'head': 'Golden streets', 'body': 'The old town after dark, when the stone glows and the crowds are gone.'}), 'feature']))

add(T('cinematic_bars', 'Cinematic letterbox + subtitles', 'Editorial & minimal',
      'Wide-screen black bars with a film-subtitle line under each frame.', 'film stills trend', ('cinematic', 0.8),
      {'scene': K('Scene', ['Frame'], [('scene', 'Scene label', 'SCENE 01'), ('sub', 'Subtitle', '“we’re not leaving yet, are we?”')],
                  [P(0, 0, 449, W, 452), TX('scene', 80, 420, MONO, 22, anchor='lb', color=(150, 150, 150), shadow=0), TX('sub', 540, 940, SANS, 32, wrap=980, color=(255, 236, 160), shadow=0)], bg=(0, 0, 0))},
      [('scene', {'scene': f'SCENE 0{i + 1}', 'sub': s}) for i, s in enumerate(['“we’re not leaving yet, are we?”', '“five more minutes.”', '“okay, ten.”', '“…let’s just stay.”'])]))

add(T('diptych', 'Side by side (diptych)', 'Editorial & minimal',
      'Two tall photos side by side with a thin gap — pair a view with a detail.', 'split screens (@inhouse_pr)', ('natural', 0.8),
      {'two': K('Two photos', ['Left photo', 'Right photo'], [], [P(0, 24, 24, 510, 1302), P(1, 546, 24, 510, 1302)], bg=OFFWHITE)},
      ['two'] * 5))

add(T('grid4', 'Four-photo grid', 'Editorial & minimal',
      'Four photos in a 2×2 grid with white gaps and a small caption.', 'classic', ('natural', 0.8),
      {'four': K('Four photos', PH(4), [('cap', 'Caption', 'a day in the old town')],
                 grid(range(4), 40, 40, 2, 490, 600, 20, 20) + [TX('cap', 540, 1286, SERIF_I, 32, **ink())], bg=OFFWHITE)},
      ['four'] * 4))

add(T('coordinates', 'Coordinates (minimal)', 'Editorial & minimal',
      'A full photo with the place name in big outlined letters and its coordinates.', 'minimal travel', ('nordic', 0.7),
      {'place': K('Place', ['Photo'], [('place', 'Place', 'Bled'), ('coords', 'Coordinates', '46.37° N · 14.11° E'), ('date', 'Date', 'October 2026')],
                  [FULL(0), TX('place', 540, 560, GOTH, 130, case='upper', track=24, outline=True, stroke=2, fit=1000, shadow=60), TX('coords', 540, 720, MONO, 30, track=4),
                   TX('date', 540, 1240, GOTH, 22, track=10, case='upper')])},
      [('place', {}), ('place', {'place': 'Mürren', 'coords': '46.56° N · 7.89° E'}), ('place', {'place': 'Dubrovnik', 'coords': '42.65° N · 18.09° E'}),
       ('place', {'place': 'Lucerne', 'coords': '47.05° N · 8.31° E'}), ('place', {'place': 'Paris', 'coords': '48.86° N · 2.35° E'})]))

add(T('timestamps', 'Timestamps (a day in hours)', 'Editorial & minimal',
      'A big thin time in the corner of each photo and what was happening — a day told hour by hour.', 'day-in-the-life', ('golden', 0.7),
      {'hour': K('Moment', ['Photo'], [('time', 'Time', '06:12'), ('what', 'What', 'sunrise · lake bled')],
                 [FULL(0), SHADE(0, 420, 130, 0), TX('time', 80, 80, SANS_L, 150, anchor='lt'), TX('what', 88, 270, GOTH, 26, anchor='lt', track=6, case='upper')])},
      [('hour', {}), ('hour', {'time': '09:30', 'what': 'coffee & croissants'}), ('hour', {'time': '13:05', 'what': 'swim in the lake'}),
       ('hour', {'time': '17:40', 'what': 'golden hour walk'}), ('hour', {'time': '21:15', 'what': 'dinner by the water'})]))

add(T('palette', 'Colour palette (moodboard)', 'Editorial & minimal',
      'Each photo with five colours taken from it and their hex codes — a travel moodboard.', 'moodboard trend', ('natural', 0.8),
      {'pal': K('Photo + palette', ['Photo'], [('name', 'Name', 'Lake Bled')],
                [P(0, 60, 60, 960, 980, radius=10), TX('name', 60, 1068, SERIF_I, 36, anchor='lt', **ink()), dict(t='swatch', slot=0, rect=(60, 1130, 960, 190))], bg=(246, 243, 237))},
      [('pal', {}), ('pal', {'name': 'Dubrovnik'}), ('pal', {'name': 'Mürren'}), ('pal', {'name': 'Paris at night'})]))

# ================================================================== Postcards, tickets & stamps
add(T('greetings_from', 'Greetings from (vintage postcard)', 'Postcards & stamps',
      'A vintage “Greetings from” cover with the place name in big letters filled with photos, then stamped photos.', 'vintage postcard', ('vintage', 0.6),
      {'cover': K('Cover', PH(6, 'Letter'), [('greet', 'Top words', 'Greetings from'), ('place', 'Place (up to 6 letters)', 'EUROPE'), ('sub', 'Bottom line', 'EUROPE · 2026')],
                  [RC(50, 50, 980, 1250, None, outline=(170, 60, 40), width=6, radius=8), TX('greet', 540, 150, SCRIPT_B, 96, rot=4, **ink(color=(170, 60, 40))),
                   dict(t='mask', field='place', slots=[0, 1, 2, 3, 4, 5], rect=(80, 380, 920, 560), font=IMPACT, dir='h', shadow=110),
                   TX('sub', 540, 1080, GOTH_B, 30, track=10, case='upper', **ink(color=(170, 60, 40)))], bg=('paper', (238, 226, 200))),
       'photo': K('Stamped photo', ['Photo'], [('stamp', 'Stamp text', 'BLED · SLOVENIA · 2026')], [FULL(0), dict(t='stamp', field='stamp', xy=(880, 1150), r=120, color=(180, 50, 40), rot=-12)])},
      ['cover', ('photo', {}), ('photo', {'stamp': 'MÜRREN · SWITZERLAND · 2026'}), ('photo', {'stamp': 'DUBROVNIK · CROATIA · 2026'}), ('photo', {'stamp': 'PARIS · FRANCE · 2026'})]))

add(T('boarding_pass', 'Boarding pass', 'Postcards & stamps',
      'A boarding-pass cover (from → to, date, seat), then photos with a ticket-stub label.', 'travel ticket trend', ('natural', 0.8),
      {'ticket': K('Ticket cover', ['Background (blurred)', 'Photo on the ticket'], [('from', 'From (code)', 'ZRH'), ('fromc', 'From (city)', 'Zurich'), ('to', 'To (code)', 'DBV'), ('toc', 'To (city)', 'Dubrovnik'),
                                                                               ('date', 'Date', '08 OCT'), ('seat', 'Seat', '12A'), ('gate', 'Gate', 'B7')],
                   [dict(t='bgphoto', slot=0, dim=0.35), RC(90, 240, 900, 870, (250, 248, 243), radius=28, shadow=150), P(1, 120, 270, 840, 360, radius=16),
                    ST('B O A R D I N G   P A S S', 150, 664, GOTH_B, 22, anchor='lt', **ink(color=MUTED)), TX('from', 150, 700, GOTH_B, 120, anchor='lt', **ink()), ST('✈', 540, 770, SYM, 74, anchor='mm', **ink(color=ORANGE)),
                    TX('to', 930, 700, GOTH_B, 120, anchor='rt', **ink()), TX('fromc', 150, 850, GOTH, 24, anchor='lt', case='upper', track=3, **ink(color=MUTED)), TX('toc', 930, 850, GOTH, 24, anchor='rt', case='upper', track=3, **ink(color=MUTED)),
                    LN([(120, 910), (960, 910)], dash=(14, 10), color=(190, 180, 165), width=3),
                    ST('DATE', 150, 945, GOTH, 20, anchor='lt', track=4, **ink(color=MUTED)), TX('date', 150, 975, GOTH_B, 36, anchor='lt', **ink()),
                    ST('SEAT', 480, 945, GOTH, 20, anchor='lt', track=4, **ink(color=MUTED)), TX('seat', 480, 975, GOTH_B, 36, anchor='lt', **ink()),
                    ST('GATE', 760, 945, GOTH, 20, anchor='lt', track=4, **ink(color=MUTED)), TX('gate', 760, 975, GOTH_B, 36, anchor='lt', **ink())]),
       'photo': K('Photo + stub', ['Photo'], [('stub', 'Stub title', 'Dubrovnik'), ('stub2', 'Stub small line', 'ARRIVAL · DAY 6')],
                  [FULL(0), RC(60, 1140, 560, 150, (250, 248, 243, 238), radius=20), TX('stub', 100, 1172, GOTH_B, 36, anchor='lt', case='upper', **ink()),
                   TX('stub2', 100, 1226, GOTH, 22, anchor='lt', track=3, **ink(color=MUTED))])},
      ['ticket', 'photo', ('photo', {'stub': 'Old town', 'stub2': 'DAY 7'}), ('photo', {'stub': 'Lokrum', 'stub2': 'DAY 8'})]))

add(T('stamps', 'Passport stamps', 'Postcards & stamps',
      'A photo on paper with inky passport stamps on its corners.', 'passport / travel journal', ('vintage', 0.5),
      {'page': K('Stamped page', ['Photo'], [('stamp', 'Big stamp', 'BLED · SLOVENIA · 2026'), ('stamp2', 'Small stamp', 'ARRIVED · OCT')],
                 [P(0, 120, 140, 840, 1000, border=20, rot=-1.5, shadow=90), dict(t='stamp', field='stamp', xy=(850, 1130), r=130, color=(40, 80, 150), rot=-14),
                  dict(t='stamp', field='stamp2', xy=(230, 250), r=96, color=(170, 50, 40), rot=10)], bg=('paper', (236, 228, 212)))},
      [('page', {}), ('page', {'stamp': 'DUBROVNIK · CROATIA · 2026'}), ('page', {'stamp': 'LUCERNE · SWITZERLAND · 2026'}), ('page', {'stamp': 'PARIS · FRANCE · 2026'})]))

add(T('map_pin', 'Location pin label', 'Postcards & stamps',
      'Full photos with a clean white location pill and the coordinates at the bottom.', 'location-tag trend', ('natural', 0.8),
      {'pin': K('Photo + pin', ['Photo'], [('place', 'Place', 'Bled, Slovenia'), ('coords', 'Coordinates', '46.37° N, 14.11° E')],
                [FULL(0), RC(60, 70, 520, 76, (255, 255, 255, 238), radius=38, shadow=60), RC(88, 98, 22, 22, ORANGE, radius=11),
                 TX('place', 126, 86, GOTH_B, 30, anchor='lt', **ink()), TX('coords', 60, 1280, MONO, 24, anchor='lb', shadow=150)])},
      [('pin', {}), ('pin', {'place': 'Mürren, Switzerland', 'coords': '46.56° N, 7.89° E'}), ('pin', {'place': 'Dubrovnik, Croatia', 'coords': '42.65° N, 18.09° E'}),
       ('pin', {'place': 'Paris, France', 'coords': '48.86° N, 2.35° E'})]))

add(T('torn_paper', 'Torn paper notes', 'Polaroids & paper',
      'A torn strip of paper across each photo with a handwritten line.', 'scrapbook trend', ('faded', 0.7),
      {'torn': K('Photo + torn note', ['Photo'], [('text', 'Note', 'the day we didn’t check the time')],
                 [FULL(0), dict(t='torn', rect=(-20, 980, 1120, 250), color=(246, 240, 228), rot=-2), TX('text', 540, 1062, HAND, 46, rot=-2, wrap=900, **ink())])},
      [('torn', {}), ('torn', {'text': 'found our favourite bench'}), ('torn', {'text': 'ice cream for dinner'}), ('torn', {'text': 'we’ll be back'})]))

add(T('diary', 'Travel diary (day by day)', 'Polaroids & paper',
      'A journal page per day: the date in handwriting, a taped photo and a few lines.', 'travel journal', ('warmfilm', 0.6),
      {'entry': K('Diary page', ['Photo'], [('date', 'Day & place', 'day 03 — bled'), ('note', 'Diary lines', 'Woke up before the alarm. The lake was glass. We walked all the way round without saying much.')],
                  [TX('date', 90, 80, HAND, 44, anchor='lt', **ink(color=(150, 60, 50))), P(0, 120, 190, 840, 700, border=14, rot=1.5, shadow=80), TAPE(465, 168, rot=-4),
                   TX('note', 100, 960, HAND, 38, anchor='lt', wrap=880, lh=1.35, **ink())], bg=('paper', (242, 236, 224)))},
      [('entry', {}), ('entry', {'date': 'day 04 — bohinj', 'note': 'Quieter than Bled. Cold water, warm sun, the best sandwich of the trip.'}),
       ('entry', {'date': 'day 07 — dubrovnik', 'note': 'Walked the walls at 8am, before the crowds. Then slept all afternoon.'})]))

# ================================================================== Fun & story
add(T('expect_reality', 'Expectation vs reality', 'Fun & story',
      'The postcard version on top, what actually happened below.', 'classic meme format', ('natural', 0.8),
      {'er': K('Expectation / reality', ['Expectation', 'Reality'], [('cap', 'Caption', 'worth it anyway')],
               [P(0, 0, 0, W, 675), P(1, 0, 675, W, 675), RC(40, 40, 330, 60, (255, 255, 255, 225), radius=30), ST('EXPECTATION', 205, 53, GOTH_B, 24, track=4, **ink()),
                RC(40, 715, 250, 60, (20, 20, 20, 200), radius=30), ST('REALITY', 165, 728, GOTH_B, 24, track=4, shadow=0), TX('cap', 540, 1250, HAND, 38, shadow=170)])},
      [('er', {}), ('er', {'cap': 'still the best day'}), ('er', {'cap': 'the rain made it better'})]))

add(T('trip_stats', 'The trip in numbers', 'Fun & story',
      'A stats slide (places, clips, photos…) over a soft photo, between full photos.', 'recap trend', ('cinematic', 0.7),
      {'stats': K('Stats', ['Background photo'], [('title', 'Title', 'the trip in numbers')] + [(f'n{i}', f'Number {i + 1}', n) for i, n in enumerate(['17', '2,199', '1,582', '1'])] +
                  [(f'l{i}', f'Label {i + 1}', l) for i, l in enumerate(['places', 'video clips', 'photos', 'unforgettable summer'])],
                  [dict(t='bgphoto', slot=0, dim=0.55), TX('title', 540, 130, GOTH, 26, track=10, case='upper')] +
                  sum([[TX(f'n{i}', 300 + (i % 2) * 480, 330 + (i // 2) * 440, BODONI, 170, fit=440), TX(f'l{i}', 300 + (i % 2) * 480, 545 + (i // 2) * 440, GOTH, 24, track=6, case='upper', wrap=420)]
                       for i in range(4)], [])),
       'photo': K('Photo', ['Photo'], [], [FULL(0)])},
      ['stats', 'photo', 'photo', 'photo']))

add(T('food_diary', 'Food diary grid', 'Fun & story',
      'A white page of rounded food photos with little dish labels.', '@ayazafe (food grid)', ('vivid', 0.5),
      {'grid': K('Food grid', PH(9, 'Dish'), [('title', 'Title', 'what we ate')] + [(f'f{i}', f'Dish {i + 1}', 'dish') for i in range(9)],
                 [TX('title', 540, 60, HAND, 54, **ink())] + grid(range(9), 65, 170, 3, 290, 290, 40, 80, radius=24) +
                 [TX(f'f{i}', 65 + (i % 3) * 330 + 145, 170 + (i // 3) * 370 + 302, SANS, 22, **ink(color=MUTED)) for i in range(9)], bg=(252, 251, 248)),
       'photo': K('Photo', ['Photo'], [('caption', 'Caption', '')], [FULL(0), TX('caption', 540, 1240, HAND, 40, shadow=170)])},
      ['grid', 'photo', 'grid']))

add(T('then_now', 'Day vs night', 'Fun & story',
      'The same place by day on top and by night below.', 'classic comparison', ('natural', 0.8),
      {'dn': K('Day / night', ['By day', 'By night'], [('place', 'Place', 'Dubrovnik')],
               [P(0, 0, 0, W, 675), P(1, 0, 675, W, 675), ST('B Y   D A Y', 60, 60, GOTH_B, 24, anchor='lt', shadow=160), ST('B Y   N I G H T', 60, 735, GOTH_B, 24, anchor='lt', shadow=160),
                TX('place', 1020, 1270, SERIF_I, 44, anchor='rb', shadow=170)])},
      [('dn', {}), ('dn', {'place': 'Paris'}), ('dn', {'place': 'Lucerne'})]))

add(T('one_word_poster', 'One word, centre stage', 'Fun & story',
      'A photo with one big word in the middle (CALM, WILD, GOLD…), a quick mood per slide.', 'poster trend', ('cinematic', 0.7),
      {'w': K('One word', ['Photo'], [('word', 'Word', 'CALM'), ('small', 'Small line', 'lake bohinj')],
              [FULL(0, dim=0.2), TX('word', 540, 675, GOTH_B, 220, anchor='mm', track=20, case='upper', fit=1000, alpha=240), TX('small', 540, 820, GOTH, 24, track=10, case='upper')])},
      [('w', {}), ('w', {'word': 'WILD', 'small': 'mürren'}), ('w', {'word': 'GOLD', 'small': 'dubrovnik'}), ('w', {'word': 'GLOW', 'small': 'paris'})]))

add(T('question_hook', 'Question hook + answers', 'Fun & story',
      'A cover that asks a question, then one answer per photo — great for comments.', 'hook trend', ('natural', 0.8),
      {'q': K('Question cover', ['Photo'], [('q', 'Question', 'Which one would you wake up to?'), ('hint', 'Small line', 'tell me 1, 2 or 3')],
              [FULL(0, dim=0.35), TX('q', 540, 600, SERIF_I, 84, wrap=900, valign='middle'), TX('hint', 540, 1150, HAND, 40)]),
       'a': K('Answer', ['Photo'], [('num', 'Number', '1'), ('label', 'Label', 'the lake')],
              [FULL(0), RC(60, 60, 110, 110, (255, 255, 255, 235), radius=55), TX('num', 115, 115, GOTH_B, 60, anchor='mm', **ink()), TX('label', 200, 115, GOTH_B, 40, anchor='lm', case='upper', track=4, shadow=160)])},
      ['q', ('a', {}), ('a', {'num': '2', 'label': 'the mountains'}), ('a', {'num': '3', 'label': 'the sea'})]))

add(T('caption_strip', 'Bottom caption strip', 'Editorial & minimal',
      'Clean full photos with a solid strip at the bottom: place on the left, a line on the right.', 'clean travel', ('natural', 0.8),
      {'p': K('Photo + strip', ['Photo'], [('place', 'Place', 'Lucerne'), ('line', 'Line', 'the wooden bridge, early morning')],
              [P(0, 0, 0, W, 1180), RC(0, 1180, W, 170, (24, 24, 26)), TX('place', 60, 1265, GOTH_B, 40, anchor='lm', case='upper', track=4, shadow=0),
               TX('line', 1020, 1265, SERIF_I, 32, anchor='rm', color=(210, 206, 198), shadow=0)])},
      [('p', {}), ('p', {'place': 'Bled', 'line': 'the island at sunrise'}), ('p', {'place': 'Mürren', 'line': 'the clouds below us'}), ('p', {'place': 'Paris', 'line': 'the tower at night'})]))

add(T('circle_focus', 'Circle focus', 'Editorial & minimal',
      'A round-cropped photo centred on a soft colour, with a small title — calm and minimal.', 'minimal', ('pastel', 0.6),
      {'c': K('Circle', ['Photo'], [('title', 'Title', 'little things'), ('sub', 'Small line', 'bled, slovenia')],
              [P(0, 190, 260, 700, 700, radius=350, shadow=60), TX('title', 540, 110, SERIF_I, 64, **ink()), TX('sub', 540, 1060, GOTH, 24, track=10, case='upper', **ink(color=MUTED))],
              bg=(232, 224, 214))},
      [('c', {}), ('c', {'title': 'slow mornings', 'sub': 'bohinj'}), ('c', {'title': 'golden hours', 'sub': 'dubrovnik'})]))

add(T('three_columns', 'Three tall columns', 'Grids & collages',
      'Three tall photo columns per slide — perfect for portrait shots from one place.', 'triptych (vertical)', ('natural', 0.8),
      {'three': K('Three columns', PH(3), [('cap', 'Caption', '')], grid(range(3), 0, 0, 3, 356, H, 6, 0) + [TX('cap', 540, 1250, SERIF_I, 36, shadow=170)], bg=(250, 248, 244))},
      ['three'] * 4))

add(T('big_small', 'One big, one small', 'Grids & collages',
      'A big photo with a small detail photo tucked in the corner, white-bordered.', 'detail + view pairing', ('natural', 0.8),
      {'bs': K('Big + small', ['Big photo', 'Small detail'], [('cap', 'Caption', '')],
               [FULL(0), P(1, 640, 880, 360, 380, border=14, shadow=120), TX('cap', 70, 1250, SERIF_I, 38, anchor='lb', shadow=170)])},
      ['bs'] * 5))

add(T('collage_mix', 'Mixed collage', 'Grids & collages',
      'An uneven collage of five photos per slide (one big, four small).', 'photo dump collage', ('warmfilm', 0.6),
      {'mix': K('Collage', PH(5), [], [P(0, 0, 0, 720, 900), P(1, 726, 0, 354, 447), P(2, 726, 453, 354, 447), P(3, 0, 906, 537, 444), P(4, 543, 906, 537, 444)], bg=(12, 12, 12))},
      ['mix'] * 4))

add(T('cover_then_dump', 'Title cover + photo dump', 'Grids & collages',
      'A bold title cover (“Europe dump”), then plain full photos — the classic dump.', 'photo dump', ('natural', 0.8),
      {'cover': K('Cover', ['Photo'], [('title', 'Title', 'europe'), ('word', 'Second word', 'dump')],
                  [FULL(0), SHADE(0, 600, 140, 0), TX('title', 540, 150, SCRIPT, 170, fit=980), TX('word', 540, 380, BODONI, 120, case='upper', track=10)]),
       'photo': K('Photo', ['Photo'], [], [FULL(0)])},
      ['cover'] + ['photo'] * 7))

add(T('night_neon', 'Night lights', 'Fun & story',
      'Night photos with glowing neon-style words.', 'night city trend', ('neon', 0.6),
      {'n': K('Night photo', ['Photo'], [('word', 'Neon word', 'after dark')],
              [FULL(0), TX('word', 540, 1080, SCRIPT_B, 120, color=(255, 120, 200), shadow=255, sblur=18, fit=980)])},
      [('n', {}), ('n', {'word': 'city lights'}), ('n', {'word': 'one more night'})]))

add(T('weather_report', 'Postcard weather report', 'Fun & story',
      'A cheeky “weather report” card on each photo: temperature, mood and forecast.', 'playful travel', ('summer', 0.7),
      {'w': K('Photo + weather card', ['Photo'], [('temp', 'Temperature', '24°'), ('place', 'Place', 'Dubrovnik'), ('mood', 'Forecast', 'sunny with a chance of gelato')],
              [FULL(0), RC(60, 60, 420, 300, (255, 255, 255, 230), radius=26, shadow=70), TX('temp', 100, 80, SANS_L, 130, anchor='lt', **ink()),
               TX('place', 100, 245, GOTH_B, 28, anchor='lt', case='upper', track=4, **ink()), TX('mood', 100, 290, SANS, 24, anchor='lt', wrap=360, **ink(color=BODY))])},
      [('w', {}), ('w', {'temp': '12°', 'place': 'Mürren', 'mood': 'cloudy with a chance of cowbells'}), ('w', {'temp': '18°', 'place': 'Paris', 'mood': 'clear skies, croissants likely'})]))
