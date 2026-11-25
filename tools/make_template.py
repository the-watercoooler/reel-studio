"""Turn an inspiration reel (a video file) into a Reel Studio template: its length, its cut points, its sound, and the
reel itself as the "Original reel" shown beside your edit. On-screen words are added afterwards (see the
make-template skill), because reading them needs eyes.

    python tools/make_template.py "<reel.mp4>" --key goa1 --title "Golden hour" [--threshold 0.3]

Writes templates/<key>.json, templates/<key>.m4a (the sound) and templates/<key>.mp4 (a small copy of the reel),
plus cache/template_frames/<key>/shots.jpg: the middle frame of every shot, labelled, for reading its words.
--threshold: scene-change sensitivity (lower finds more cuts; 0.2-0.4 suits most reels).
Then reload templates:  POST http://localhost:8777/api/templates/reload  (or restart Reel Studio).
"""
import argparse, json, os, re, subprocess, sys
from PIL import Image, ImageDraw

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP)
import fontfind  # noqa: E402
FPS = 30


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', p],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    j = json.loads(r.stdout or '{}')
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), {})
    return float(j.get('format', {}).get('duration', 0)), v.get('width', 0), v.get('height', 0), any(
        s.get('codec_type') == 'audio' for s in j.get('streams', []))


def scene_cuts(p, thr, total):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-vf', f"select='gt(scene,{thr})',showinfo", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    ts = [float(m) for m in re.findall(r'pts_time:([0-9.]+)', r.stderr or '')]
    cuts = sorted({int(round(t * FPS)) for t in ts})
    out = []
    for c in cuts:                                          # drop cuts at the very ends and doubles a frame apart
        if 2 <= c <= total - 2 and (not out or c - out[-1] >= 2):
            out.append(c)
    return out


def main():
    a = argparse.ArgumentParser(); a.add_argument('video'); a.add_argument('--key', required=True); a.add_argument('--title', required=True)
    a.add_argument('--threshold', type=float, default=0.3)
    o = a.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,32}', o.key):
        sys.exit('--key: letters, digits, - or _ only (max 32)')
    if not os.path.isfile(o.video):
        sys.exit('Video not found: ' + o.video)
    tdir = os.path.join(APP, 'templates'); os.makedirs(tdir, exist_ok=True)
    if os.path.exists(os.path.join(tdir, o.key + '.json')):
        sys.exit(f'templates/{o.key}.json already exists - choose another --key, or delete it first.')
    d, w, h, has_audio = probe(o.video)
    if d <= 0:
        sys.exit('Could not read that video.')
    total = int(round(d * FPS))
    cuts = scene_cuts(o.video, o.threshold, total)
    m4a, mp4 = os.path.join(tdir, o.key + '.m4a'), os.path.join(tdir, o.key + '.mp4')
    if has_audio:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', o.video, '-vn', '-c:a', 'aac', '-b:a', '192k', m4a], check=True)
    else:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{d:.3f}', '-c:a', 'aac', m4a], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', o.video, '-vf', 'scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2',
                    '-r', str(FPS), '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', mp4], check=True)
    T = {'key': o.key, 'title': o.title, 'song': True, 'col': '', 'total': total, 'cuts': cuts, 'grade': 'natural', 'texts': [],
         'audio': o.key + '.m4a', 'insp': o.key + '.mp4'}
    json.dump(T, open(os.path.join(tdir, o.key + '.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    # the middle frame of every shot, for reading the on-screen words
    b = [0] + cuts + [total]
    fdir = os.path.join(APP, 'cache', 'template_frames', o.key); os.makedirs(fdir, exist_ok=True)
    f = fontfind.load('segoeuib.ttf', 18)
    tiles = []
    for i in range(len(b) - 1):
        mid = (b[i] + b[i + 1]) / 2 / FPS
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{mid:.3f}', '-i', o.video, '-frames:v', '1', '-vf', 'scale=270:480:force_original_aspect_ratio=decrease',
                            '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        try:
            from io import BytesIO
            im = Image.open(BytesIO(r.stdout)).convert('RGB')
        except Exception:
            im = Image.new('RGB', (270, 480), (40, 40, 40))
        tiles.append((f'shot {i + 1}: frames {b[i]}-{b[i + 1]} ({b[i] / FPS:.2f}-{b[i + 1] / FPS:.2f}s)', im))
    cols = 6
    tw, thh = 270, 480 + 26
    S = Image.new('RGB', (cols * (tw + 6), ((len(tiles) + cols - 1) // cols) * (thh + 6)), 'white'); dr = ImageDraw.Draw(S)
    for i, (lab, im) in enumerate(tiles):
        x, y = (i % cols) * (tw + 6), (i // cols) * (thh + 6)
        S.paste(im, (x, y + 22)); dr.text((x + 2, y + 2), lab, fill='black', font=f)
    sheet = os.path.join(fdir, 'shots.jpg'); S.save(sheet, quality=85)
    print(f'Template "{o.title}" ({o.key}): {d:.2f}s = {total} frames, {len(cuts)} cuts -> {len(cuts) + 1} shots')
    print('  cuts (frames):', cuts)
    print('  files: templates/%s.json, .m4a, .mp4' % o.key)
    print('  shot frames for reading the words:', sheet)
    if len(cuts) == 0:
        print('  No cuts found: one long shot, or try a lower --threshold (e.g. 0.2).')


if __name__ == '__main__':
    main()
