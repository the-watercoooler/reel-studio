"""Contact sheets of a footage folder's clips, so Claude (or you) can look at many clips at once and describe them.

    python tools/contact_sheets.py <folder key or name>        e.g.  python tools/contact_sheets.py "Goa trip"

Each clip is one row of 4 frames, labelled with its file name and length; 10 clips per sheet. Uses the thumbnails
Reel Studio already made, so it is quick. Sheets go to cache/sheets/<key>/ and their paths are printed, followed by
the list of file names in sheet order (handy for writing the folder's _Clip list.csv).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP)
import fontfind  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    want = sys.argv[1].lower()
    cols = json.load(open(os.path.join(APP, 'collections.json'), encoding='utf-8-sig')) if os.path.exists(os.path.join(APP, 'collections.json')) else []
    C = next((c for c in cols if want in (c['key'].lower(), c['name'].lower())), None)
    if not C:
        print('No such folder. Known:', ', '.join(f"{c['name']} ({c['key']})" for c in cols) or 'none yet'); sys.exit(1)
    items = json.load(open(os.path.join(APP, 'cache', 'collections', C['key'] + '.json'), encoding='utf-8'))
    vids = sorted([c for c in items if c.get('kind') != 'photo'], key=lambda c: (c['l'], c['f']))
    out = os.path.join(APP, 'cache', 'sheets', C['key']); os.makedirs(out, exist_ok=True)
    f = fontfind.load('segoeuib.ttf', 20)
    per, tw, th = 10, 180, 320
    paths = []
    for s in range(0, len(vids), per):
        group = vids[s:s + per]
        rows = []
        for c in group:
            ims = []
            for k in range(c.get('n', 4)):
                p = os.path.join(APP, 'cache', 'thumbs', f"{c['id']:04d}_{k:02d}.jpg")
                im = Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (tw, th), (40, 40, 40))
                im.thumbnail((tw, th)); ims.append(im)
            rows.append((c, ims))
        rh = max(max(i.height for i in ims) for _, ims in rows) + 34
        W = max(sum(i.width + 4 for i in ims) for _, ims in rows) + 8
        S = Image.new('RGB', (max(W, 760), rh * len(rows) + 6), 'white'); d = ImageDraw.Draw(S)
        for r, (c, ims) in enumerate(rows):
            y = r * rh + 4; x = 4
            d.text((x, y), f"{s + r + 1}. {c['f']}  ·  {c['d']:.1f}s  ·  {c['l'].replace(chr(92), ' / ')}", fill='black', font=f)
            for im in ims:
                S.paste(im, (x, y + 28)); x += im.width + 4
        p = os.path.join(out, f'sheet_{s // per + 1:02d}.jpg'); S.save(p, quality=82); paths.append(p)
    print(f"{C['name']}: {len(vids)} clips on {len(paths)} sheets")
    for p in paths:
        print('  ' + p)
    print('\nFiles in sheet order:')
    for i, c in enumerate(vids, 1):
        print(f"  {i}. {c['f']}")


if __name__ == '__main__':
    main()
