"""Colour and type versions of the strongest templates (24 Nov 2026).

Each version copies a base template and swaps its colours (exact RGB matches) and/or fonts, and can change the look and
the sample words. The layout stays the same, so a version is one line to add: append a V(...) call below.
"""
import carousel_templates_pro as PRO
import carousel_templates_systems as SYS
import carousel_templates_wave2 as WV

BASES = {t['key']: t for t in PRO.TEMPLATES + SYS.TEMPLATES + WV.TEMPLATES}
TEMPLATES = []

COOPER, BLACK, COND, SERIF, SERIF_B, SERIF_I = 'COOPBL.TTF', 'seguibl.ttf', 'bahnschrift.ttf#Bold Condensed', 'SitkaVF.ttf#Banner', 'SitkaVF.ttf#Banner Bold', 'SitkaVF-Italic.ttf#Banner Italic'
INK, WHITE = (34, 31, 28), (255, 255, 255)


def _map(o, cm, fm):
    if isinstance(o, dict):
        return {k: _map(v, cm, fm) for k, v in o.items()}
    if isinstance(o, list):
        return [_map(v, cm, fm) for v in o]
    if isinstance(o, tuple):
        if len(o) in (3, 4) and all(isinstance(v, int) for v in o) and tuple(o[:3]) in cm:
            return tuple(cm[tuple(o[:3])]) + tuple(o[3:])
        return tuple(_map(v, cm, fm) for v in o)
    if isinstance(o, str) and o in fm:
        return fm[o]
    return o


def V(base, key, label, about, cmap=None, fmap=None, look=None, words=None):
    B = BASES[base]
    T = _map(B, {tuple(k): tuple(v) for k, v in (cmap or {}).items()}, fmap or {})
    T.update(key=key, label=label, about=about + ' A version of “' + B['label'] + '”.', base=base, new=True, batch='Versions')
    if look:
        T['look'] = look
    if words:
        out = []
        for item in T['default']:
            kind, over = (item, {}) if isinstance(item, str) else (item[0], dict(item[1]))
            if kind in words:
                over.update(words[kind])
            out.append((kind, over) if over else kind)
        T['default'] = out
    TEMPLATES.append(T)


# ------------------------------------------------------------------ design systems
V('sys_broadsheet', 'v_broadsheet_night', 'Broadsheet · night edition', 'Dark newsprint with cream type and gold rules.',
  {(241, 238, 230): (22, 24, 28), INK: (236, 230, 216), (176, 30, 36): (212, 170, 90), (112, 106, 98): (150, 146, 138), (190, 184, 172): (70, 70, 74)}, look=('moody', 0.6))
V('sys_broadsheet', 'v_broadsheet_salmon', 'Broadsheet · pink paper', 'Salmon newsprint with navy accents, like a weekend finance paper.',
  {(241, 238, 230): (244, 214, 196), (176, 30, 36): (30, 60, 120)})
V('sys_broadsheet', 'v_broadsheet_sunday', 'Broadsheet · Sunday supplement', 'Heavy retro serif headlines and orange accents.',
  {(176, 30, 36): (232, 87, 46)}, {SERIF_B: COOPER, SERIF_I: 'BELLI.TTF'})
V('sys_still_frame', 'v_still_golden', 'Still frame · golden hour', 'Warm golden grade with amber subtitles.', {(250, 242, 205): (255, 206, 110)}, look=('golden', 0.7))
V('sys_still_frame', 'v_still_noir', 'Still frame · noir', 'Black-and-white film stills with white subtitles.', {(250, 242, 205): WHITE}, look=('noir', 0.9))
V('sys_still_frame', 'v_still_seventies', 'Still frame · 70s film', 'Seventies grade, chunky title type and yellow subtitles.',
  {(250, 242, 205): (250, 190, 80)}, {SERIF: COOPER, 'seguisb.ttf': 'BRLNSDB.TTF'}, look=('seventies', 0.7))
V('sys_quiet_journal', 'v_quiet_ink', 'Quiet journal · ink', 'The quiet journal on near-black.',
  {(244, 242, 238): (24, 24, 26), (42, 40, 37): (232, 228, 220), (140, 134, 124): (140, 138, 132)}, look=('matte', 0.5))
V('sys_quiet_journal', 'v_quiet_sage', 'Quiet journal · sage', 'Soft sage ground with deep green captions.',
  {(244, 242, 238): (220, 228, 214), (42, 40, 37): (36, 52, 42), (140, 134, 124): (100, 116, 104)}, look=('mist', 0.5))
V('sys_quiet_journal', 'v_quiet_typewriter', 'Quiet journal · typewriter', 'The same calm layout set entirely in typewriter type.',
  {(244, 242, 238): (238, 234, 224)}, {SERIF_I: 'cour.ttf', 'GOTHIC.TTF': 'cour.ttf', 'GOTHICB.TTF': 'courbd.ttf'})
V('sys_greetings_from', 'v_greetings_sunset', 'Greetings from · sunset', 'Orange script and plum block letters on warm linen.',
  {(198, 58, 44): (232, 96, 40), (34, 52, 110): (90, 30, 80), (236, 224, 198): (246, 214, 170)})
V('sys_greetings_from', 'v_greetings_riviera', 'Greetings from · Riviera', 'Sea-blue script and red letters on pale linen, for the French Riviera.',
  {(198, 58, 44): (20, 110, 170), (34, 52, 110): (200, 60, 40), (236, 224, 198): (232, 236, 230)},
  words={'cover': {'place': 'NICE', 'sub': 'The French Riviera'}, 'front': {'cap': 'Promenade des Anglais'}})
V('sys_greetings_from', 'v_greetings_noir', 'Greetings from · black & gold', 'Gold script and letters on black linen.',
  {(236, 224, 198): (34, 34, 36), (198, 58, 44): (222, 184, 100), (34, 52, 110): (120, 90, 40)})
V('sys_ticket_diary', 'v_ticket_mint', 'Ticket stub diary · mint', 'Mint paper with teal and coral inks.',
  {(226, 212, 186): (206, 226, 214), (190, 60, 45): (214, 90, 60), (40, 80, 150): (30, 90, 80)})
V('sys_ticket_diary', 'v_ticket_blush', 'Ticket stub diary · blush', 'Blush paper with plum and raspberry inks.',
  {(226, 212, 186): (240, 214, 208), (40, 80, 150): (120, 50, 90), (190, 60, 45): (190, 40, 70)})
V('sys_contact_sheet', 'v_contact_lighttable', 'Contact sheet · light table', 'Negatives and prints on a white light table with dark grease marks.',
  {(18, 18, 18): (236, 236, 230), (230, 224, 210): (40, 40, 40), WHITE: (25, 25, 25), (170, 170, 170): (90, 90, 90), (150, 150, 150): (90, 90, 90),
   (232, 150, 60): (200, 90, 30)})
V('sys_contact_sheet', 'v_contact_bw', 'Contact sheet · black & white', 'A black-and-white roll with yellow grease pencil.',
  {(232, 150, 60): (240, 240, 240), (222, 44, 40): (250, 210, 40)}, look=('bw', 1.0))
V('sys_field_guide', 'v_field_terracotta', 'Field guide · terracotta', 'Terracotta and sand instead of green.',
  {(46, 125, 107): (184, 84, 52), (242, 181, 68): (240, 200, 120), (250, 247, 240): (247, 240, 230)})
V('sys_field_guide', 'v_field_navy', 'Field guide · navy', 'Navy and sunshine yellow on cool white.',
  {(46, 125, 107): (30, 52, 110), (242, 181, 68): (255, 200, 90), (250, 247, 240): (240, 243, 248)})
V('sys_field_guide', 'v_field_retro', 'Field guide · retro', 'Chunky seventies headlines in orange on cream.',
  {(46, 125, 107): (214, 90, 40), (250, 247, 240): (246, 236, 214)}, {SERIF_B: COOPER})
V('sys_giant_word', 'v_giant_black', 'Giant word · heavy', 'The giant word in an extra-heavy sans.', fmap={COND: BLACK})
V('sys_giant_word', 'v_giant_retro', 'Giant word · retro', 'The giant word in a soft retro serif.', fmap={COND: COOPER}, words={'cover': {'word': 'PORTO'}})
V('sys_poster_series', 'v_posters_primary', 'City poster series · primaries', 'Red, blue, black and yellow with extra-heavy type.',
  {(232, 87, 46): (214, 40, 36), (34, 70, 176): (20, 60, 160), (236, 214, 110): (246, 200, 30)}, {COND: BLACK})
V('sys_poster_series', 'v_posters_sunset', 'City poster series · sunset', 'Tangerine, plum and peach colourways.',
  {(232, 87, 46): (240, 140, 60), (34, 70, 176): (140, 40, 90), (24, 24, 24): (60, 20, 40), (236, 214, 110): (255, 190, 120)})
V('sys_expedition', 'v_exped_desert', 'Expedition log · desert', 'Sandstone browns and sun orange.',
  {(28, 35, 33): (60, 40, 28), (217, 108, 63): (240, 170, 80), (230, 225, 211): (244, 232, 210)}, look=('desert', 0.6))
V('sys_expedition', 'v_exped_glacier', 'Expedition log · glacier', 'Deep ice blue with glacier cyan.', {(28, 35, 33): (16, 30, 46), (217, 108, 63): (120, 200, 230)}, look=('glacier', 0.6))
V('sys_expedition', 'v_exped_forest', 'Expedition log · forest', 'Pine green with moss accents.', {(28, 35, 33): (20, 36, 26), (217, 108, 63): (200, 220, 120)}, look=('lush', 0.6))
V('sys_riso_collage', 'v_riso_orange', 'Riso collage · green & orange', 'Two-ink riso in green and orange.',
  {(255, 72, 166): (255, 110, 40), (0, 112, 190): (0, 140, 100), (0, 92, 170): (0, 120, 80), (200, 30, 110): (220, 80, 20)})
V('sys_riso_collage', 'v_riso_red', 'Riso collage · red & teal', 'Two-ink riso in red and teal.',
  {(255, 72, 166): (230, 40, 60), (0, 112, 190): (0, 150, 160), (0, 92, 170): (0, 120, 130), (200, 30, 110): (200, 20, 40)})
V('sys_riso_collage', 'v_riso_purple', 'Riso collage · purple & orange', 'Two-ink riso in purple and orange with mint.',
  {(0, 112, 190): (110, 50, 160), (255, 72, 166): (255, 150, 0), (0, 92, 170): (90, 40, 150), (200, 30, 110): (230, 120, 0), (255, 226, 0): (170, 230, 210)})

# ------------------------------------------------------------------ Canva / SCRL-styled set
V('gallery_wall', 'v_gallery_dark', 'Gallery wall · dark', 'The seamless gallery wall on charcoal.',
  {(243, 240, 235): (24, 24, 26), INK: (230, 226, 218), (128, 120, 110): (150, 146, 140)}, look=('matte', 0.5))
V('gallery_wall', 'v_gallery_sand', 'Gallery wall · sand', 'The seamless gallery wall on warm sand.', {(243, 240, 235): (236, 226, 210)})
V('postcard_bold', 'v_postcard_greece', 'Postcard bold · Greece', 'Aegean blue, sun yellow and sky blue.',
  {(38, 70, 160): (20, 90, 170), (214, 72, 56): (240, 170, 40), (236, 150, 124): (120, 190, 230), (245, 238, 226): (246, 246, 240)},
  words={'cover': {'title': 'HELLAS', 'line': 'postcards from the islands  →'}})
V('postcard_bold', 'v_postcard_maroc', 'Postcard bold · Morocco', 'Terracotta, teal and saffron.',
  {(38, 70, 160): (170, 60, 40), (214, 72, 56): (30, 110, 100), (236, 150, 124): (240, 190, 120), (245, 238, 226): (244, 228, 206)},
  words={'cover': {'title': 'MAROC', 'line': 'postcards from the medina  →'}})
V('slant_resort', 'v_slant_sunset', 'Slanted strips · sunset', 'Deep terracotta with sand-gold labels.', {(24, 60, 62): (120, 46, 38), (214, 182, 120): (240, 200, 140)})
V('slant_resort', 'v_slant_midnight', 'Slanted strips · midnight', 'Midnight navy with silver-blue labels.', {(24, 60, 62): (18, 22, 40), (214, 182, 120): (180, 190, 230)})
V('journal_scrap', 'v_journal_blue', 'Travel journal · blue notebook', 'Pale blue dotted paper and navy script.', {(238, 228, 210): (214, 226, 236), (184, 96, 62): (40, 80, 150)})
V('dump_bold', 'v_dump_pink', 'Photo dump · pink script', 'The bold photo dump with a pink script word.', {(252, 214, 80): (255, 140, 190)})
V('dump_bold', 'v_dump_condensed', 'Photo dump · condensed lime', 'Condensed capitals and a lime script.', {(252, 214, 80): (205, 255, 64)}, {BLACK: COND})
V('one_day_in', 'v_oneday_pink', 'One day in · pink', 'Pink script place name.', {(252, 214, 80): (255, 150, 200)})
V('one_day_in', 'v_oneday_retro', 'One day in · retro', 'Retro serif with peach script.', {(252, 214, 80): (255, 200, 120)}, {'BRLNSDB.TTF': COOPER})
V('wrap_red', 'v_wrap_green', "That's a wrap · green", 'Bottle-green headlines on ivory.', {(176, 34, 40): (30, 100, 70)})
V('wrap_red', 'v_wrap_blue', "That's a wrap · blue", 'Cobalt headlines on cool white.', {(176, 34, 40): (30, 60, 150), (246, 240, 230): (240, 242, 246)})
V('neon_collage', 'v_neon_pink', 'Neon collage · pink', 'Hot-pink capitals over the collage.', {(205, 255, 64): (255, 80, 180)})
V('neon_collage', 'v_neon_orange', 'Neon collage · orange', 'Safety-orange capitals over the collage.', {(205, 255, 64): (255, 140, 30)})
V('moments_chrome', 'v_moments_white', 'Small moments · all white', 'White title instead of yellow.', {(252, 214, 80): WHITE})
V('moments_chrome', 'v_moments_coral', 'Small moments · coral', 'Coral title and sparkles.', {(252, 214, 80): (255, 128, 100)})
V('typewriter_notes', 'v_type_dark', 'Typewriter notes · dark', 'Typewriter notes on near-black.', {(244, 240, 232): (28, 28, 30), INK: (232, 228, 220)}, look=('matte', 0.5))
V('typewriter_notes', 'v_type_blue', 'Typewriter notes · blue ink', 'Typed in blue ink.', {INK: (30, 60, 140)})
V('arch_windows', 'v_arch_sage', 'Arch windows · sage', 'Sage ground and olive labels.', {(236, 226, 212): (214, 222, 204), (184, 96, 62): (70, 100, 70)})
V('arch_windows', 'v_arch_blush', 'Arch windows · blush', 'Blush ground and raspberry labels.', {(236, 226, 212): (240, 220, 214), (184, 96, 62): (170, 70, 90)})
V('vertical_title', 'v_vertical_dark', 'Vertical title · dark', 'The vertical portfolio title on charcoal.',
  {(243, 240, 235): (26, 26, 28), INK: (236, 232, 224), (184, 96, 62): (222, 170, 100)}, look=('matte', 0.5))
V('forest_italic', 'v_burgundy_italic', 'Deep burgundy · italic serif', 'Burgundy ground with peach italics.', {(30, 52, 40): (70, 20, 30), (236, 204, 112): (240, 200, 170)})
V('forest_italic', 'v_navy_italic', 'Deep navy · italic serif', 'Navy ground with powder-blue italics.', {(30, 52, 40): (18, 30, 60), (236, 204, 112): (170, 200, 240)})
V('offset_frame', 'v_offset_mint', 'Offset outline frame · mint', 'Mint frames on cool paper.', {(236, 150, 124): (90, 170, 150), (246, 238, 228): (238, 244, 240)})
V('offset_frame', 'v_offset_cobalt', 'Offset outline frame · cobalt', 'Cobalt frames and script.', {(236, 150, 124): (40, 80, 200)})
V('notebook_spots', 'v_notebook_mint', 'Notebook · mint', 'Mint squared paper with green ink.',
  {(226, 218, 242): (214, 238, 226), (72, 48, 120): (30, 100, 80), (140, 120, 190): (110, 170, 140), (70, 60, 92): (40, 80, 64)})
V('notebook_spots', 'v_notebook_butter', 'Notebook · butter', 'Butter-yellow squared paper with brown ink.',
  {(226, 218, 242): (250, 240, 200), (72, 48, 120): (150, 80, 20), (140, 120, 190): (200, 170, 100), (70, 60, 92): (110, 70, 30)})
V('checker_dump', 'v_checker_sage', 'Checkerboard dump · sage', 'Sage squares between the photos.', {(234, 180, 150): (190, 206, 186)})
V('checker_dump', 'v_checker_cobalt', 'Checkerboard dump · cobalt', 'Cobalt squares between the photos.', {(234, 180, 150): (60, 90, 200)})
V('torn_quote', 'v_torn_black', 'Torn paper quote · black paper', 'White handwriting on black torn paper.', {(250, 246, 236): (30, 30, 30), INK: (240, 236, 228)})
V('month_chips', 'v_chips_blue', 'Month recap · cool blue', 'The chips recap on cool blue paper.', {(246, 242, 236): (232, 240, 248)})
V('magazine_cover', 'v_magazine_bodoni', 'Magazine cover · Bodoni', 'A tall compressed Bodoni masthead and a black badge.', {(176, 34, 40): (20, 20, 20)}, {SERIF_B: 'BOD_PSTC.TTF'})

# ------------------------------------------------------------------ wave 2
_RAMP_BLUE = [(16, 30, 60), (30, 70, 130), (70, 130, 190), (160, 200, 230), (240, 244, 248)]
_RAMP_SUN = [(50, 20, 50), (130, 40, 80), (220, 90, 70), (250, 170, 90), (252, 236, 200)]
V('w_park_poster', 'v_park_blue', 'National park posters · blue print', 'Every poster printed in five blues.',
  {c: _RAMP_BLUE[i] for p in WV.PARK_PALS.values() for i, c in enumerate(p)})
V('w_park_poster', 'v_park_sunset', 'National park posters · sunset print', 'Every poster printed in plum-to-peach inks.',
  {c: _RAMP_SUN[i] for p in WV.PARK_PALS.values() for i, c in enumerate(p)})
V('w_pastel_symmetry', 'v_pastel_bold', 'Symmetry · bold colours', 'Saturated grounds with white captions.',
  {(244, 204, 204): (232, 110, 110), (198, 228, 212): (60, 170, 130), (246, 228, 166): (232, 180, 40), (192, 214, 236): (70, 120, 210),
   (120, 50, 60): WHITE, (30, 80, 66): WHITE, (110, 76, 20): WHITE, (30, 56, 100): WHITE})
V('w_city_guide', 'v_cityguide_green', 'City guide · green', 'Bottle green, for Porto.', {(226, 82, 58): (40, 120, 90)}, words={'cover': {'g_city': 'Porto', 'chip': 'Colour No. 04'}})
V('w_city_guide', 'v_cityguide_blue', 'City guide · blue', 'Cobalt, for Madrid.', {(226, 82, 58): (40, 80, 170)}, words={'cover': {'g_city': 'Madrid', 'chip': 'Colour No. 29'}})
V('w_fanzine', 'v_fanzine_pink', 'Punk fanzine · pink paper', 'Photocopies on hot-pink paper.', {(236, 234, 228): (250, 196, 218)})
V('w_poolside', 'v_poolside_mint', 'Poolside retro · mint', 'Mint and pink awnings with forest-green type.',
  {(240, 120, 96): (80, 170, 140), (96, 196, 204): (240, 150, 180), (24, 64, 90): (30, 60, 50)})
V('w_passport', 'v_passport_burgundy', 'Passport pages · burgundy', 'A burgundy passport cover.', {(24, 40, 72): (100, 20, 36)})
V('w_passport', 'v_passport_green', 'Passport pages · green', 'A dark green passport cover.', {(24, 40, 72): (20, 60, 40)})
V('w_departures', 'v_departures_white', 'Departure board · white flaps', 'White split-flap letters.', {(250, 210, 60): (245, 245, 240)})
V('w_photobooth', 'v_photobooth_blue', 'Photo booth · blue curtain', 'Strips on a blue velvet curtain.', {(176, 34, 44): (30, 60, 140), (150, 24, 34): (24, 48, 116)})
V('w_swiss_grid', 'v_swiss_blue', 'Swiss grid · blue', 'International style with blue instead of red.', {(226, 32, 40): (20, 70, 200)})
V('w_bauhaus', 'v_bauhaus_pastel', 'Bauhaus shapes · pastel', 'The Bauhaus shapes in soft pastels.', {(214, 48, 40): (222, 104, 92), (240, 190, 30): (250, 214, 120), (30, 70, 160): (110, 150, 215)})
V('w_vinyl', 'v_vinyl_cream', 'Trip soundtrack · cream sleeve', 'The record set on a cream background.',
  {(24, 22, 26): (240, 232, 216), WHITE: (30, 28, 26), (60, 58, 62): (210, 200, 186), (200, 196, 190): (90, 86, 80)})
V('w_countdown', 'v_countdown_red', 'Countdown · red', 'Red outlined numbers.', {(255, 196, 60): (240, 70, 60)})
V('w_datestamp', 'v_datestamp_blue', 'Disposable camera · blue box', 'A blue camera box.', {(250, 204, 40): (60, 150, 230)})
V('w_a_to_z', 'v_atoz_red', 'A–Z of a city · red', 'Brick-red giant letters.', {(36, 84, 160): (200, 50, 40), (244, 238, 228): (246, 238, 226)})
V('w_calendar', 'v_calendar_dark', 'Calendar month · dark', 'The calendar on charcoal with coral dates.',
  {(247, 244, 238): (24, 24, 26), INK: (236, 232, 224), (220, 214, 204): (60, 60, 64), (214, 58, 46): (240, 120, 90)})
V('w_instax', 'v_instax_brights', 'Instant wide · brights', 'Instant prints on bright grounds.',
  {(246, 214, 196): (250, 170, 120), (204, 224, 240): (120, 190, 240), (210, 224, 204): (160, 210, 120)})
