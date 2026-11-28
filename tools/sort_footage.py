"""Sort a footage folder into tidy sub-folders (by moment / place / day), with an undo log. Nothing is deleted or renamed.

    python tools/sort_footage.py plan  "<footage folder>" [--gap 45] [--orientation] [--short 3]
    python tools/sort_footage.py apply "<plan.json>"
    python tools/sort_footage.py undo  "<footage folder>"

plan   reads every video and photo (including sub-folders), finds when each was recorded (DJI file name, the video's
       own creation time, photo EXIF, else the file date) and groups them into "sessions": a new session starts after
       a gap of --gap minutes. It writes a plan (JSON) and one contact sheet per session, and prints both.
       Edit the plan - rename "folder" values to real names ("1 Cocktail shoot - 15 Nov"), merge or split groups,
       add "notes" - then apply it.
       --orientation  also split each group into Portrait / Landscape sub-folders
       --short N      put videos shorter than N seconds into an "Under N seconds" sub-folder (kept, just set aside)
apply  moves the files as planned (never overwrites), moves DJI .LRF preview files to "_LRF proxies", writes
       "_sorting log.csv" (every move, for undo) and "_Clip list.csv" (file, folder, time, length, shape, notes).
undo   moves every file back to where it was, using "_sorting log.csv".
"""
import argparse, csv, io, json, os, re, shutil, subprocess, sys, time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP)
import fontfind  # noqa: E402

VIDEO = ('.mp4', '.mov', '.m4v')
PHOTO = ('.jpg', '.jpeg', '.png', '.heic', '.dng')
LOG, LIST, LRF_DIR = '_sorting log.csv', '_Clip list.csv', '_LRF proxies'
LIST_OLD = '_Clip list (before sorting).csv'


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def probe(path):
    j = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height:stream_side_data=rotation:format=duration:format_tags=creation_time', '-of', 'json', path]).stdout or '{}')
    s = (j.get('streams') or [{}])[0]
    w, h = s.get('width', 0), s.get('height', 0)
    if any(abs(int(sd.get('rotation', 0))) in (90, 270) for sd in s.get('side_data_list', []) or []):
        w, h = h, w
    fmt = j.get('format') or {}
    return float(fmt.get('duration', 0) or 0), w, h, (fmt.get('tags') or {}).get('creation_time')


def when(path, created=None):
    m = re.search(r'(20\d{6})_?(\d{6})', os.path.basename(path))
    if m:
        return datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
    if created:
        try:
            return datetime.fromisoformat(created.replace('Z', '+00:00')).astimezone().replace(tzinfo=None)
        except ValueError:
            pass
    if path.lower().endswith(('.jpg', '.jpeg')):
        try:
            dt = Image.open(path).getexif().get(306)
            if dt:
                return datetime.strptime(str(dt)[:19], '%Y:%m:%d %H:%M:%S')
        except Exception:
            pass
    return datetime.fromtimestamp(os.path.getmtime(path))


def scan(root):
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = sorted(d for d in dns if not d.startswith(('_', '.')) and d != 'Reels')
        for fn in sorted(fns):
            ext = os.path.splitext(fn)[1].lower()
            if ext not in VIDEO + PHOTO or fn.startswith(('.', '~')):
                continue
            p = os.path.join(dp, fn)
            if ext in VIDEO:
                d, w, h, ct = probe(p)
            else:
                d, ct = 0.0, None
                try:
                    with Image.open(p) as im:
                        w, h = im.size
                except Exception:
                    w = h = 0
            out.append({'rel': os.path.relpath(p, root), 'kind': 'video' if ext in VIDEO else 'photo', 'd': round(d, 2),
                        'w': w, 'h': h, 'shape': 'Portrait' if h > w else 'Landscape', 't': when(p, ct)})
    return sorted(out, key=lambda e: (e['t'], e['rel']))


def frame(root, e, h=240):
    p = os.path.join(root, e['rel'])
    if e['kind'] == 'video':
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{e['d'] / 2:.2f}", '-i', p, '-frames:v', '1', '-vf', f'scale=-2:{h}',
                            '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        try:
            return Image.open(io.BytesIO(r.stdout)).convert('RGB')
        except Exception:
            pass
    else:
        try:
            im = Image.open(p).convert('RGB'); im.thumbnail((h * 2, h)); return im
        except Exception:
            pass
    return Image.new('RGB', (h * 9 // 16, h), (60, 60, 60))


def sheet(root, items, title, out):
    f, fb = fontfind.load('segoeui.ttf', 15), fontfind.load('segoeuib.ttf', 22)
    cells = [(e, frame(root, e)) for e in items[:40]]
    rows, row, x, W = [], [], 0, 1900
    for e, im in cells:
        if row and x + im.width > W:
            rows.append(row); row, x = [], 0
        row.append((e, im)); x += im.width + 6
    if row:
        rows.append(row)
    H = 44 + sum(240 + 40 for _ in rows)
    S = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(S)
    d.text((8, 8), title + ('' if len(items) <= 40 else f'  (first 40 of {len(items)})'), fill='black', font=fb)
    y = 44
    for row in rows:
        x = 6
        for e, im in row:
            S.paste(im, (x, y))
            fits = max(4, im.width // 8)                                    # keep labels inside their own cell
            name = os.path.basename(e['rel'])
            d.text((x, y + 242), name if len(name) <= fits else '…' + name[-(fits - 1):], fill='black', font=f)
            d.text((x, y + 260), f"{e['t']:%H:%M}" + (f"  {e['d']:.0f}s" if e['d'] else ''), fill='#555', font=f)
            x += im.width + 6
        y += 280
    S.save(out, quality=80)


def cmd_plan(a):
    root = os.path.abspath(a.folder)
    if not os.path.isdir(root):
        sys.exit('Folder not found: ' + root)
    if os.path.exists(os.path.join(root, LOG)):
        sys.exit(f'This folder was sorted before ({LOG} exists). Undo first, or sort a sub-folder.')
    items = scan(root)
    if not items:
        sys.exit('No videos or photos found.')
    groups, cur = [], []
    for e in items:
        if cur and (e['t'] - cur[-1]['t']) > timedelta(minutes=a.gap):
            groups.append(cur); cur = []
        cur.append(e)
    groups.append(cur)
    work = os.path.join(APP, 'cache', 'sort', re.sub(r'[^A-Za-z0-9]+', '-', os.path.basename(root)).strip('-') or 'folder')
    os.makedirs(work, exist_ok=True)
    plan = {'root': root, 'orientation': a.orientation, 'short': a.short, 'groups': []}
    for i, g in enumerate(groups, 1):
        t0, t1 = g[0]['t'], g[-1]['t']
        name = f"{i} {t0:%d %b %H.%M}" + (f"-{t1:%H.%M}" if t1.date() == t0.date() and t1 != t0 else (f" - {t1:%d %b}" if t1.date() != t0.date() else ''))
        shp = os.path.join(work, f'group_{i:02d}.jpg')
        sheet(root, g, f'Group {i}: {t0:%a %d %b %H:%M} - {t1:%H:%M}  ({len(g)} files)', shp)
        plan['groups'].append({'folder': name, 'sheet': shp, 'files': [e['rel'] for e in g],
                               'from': f'{t0:%Y-%m-%d %H:%M}', 'to': f'{t1:%Y-%m-%d %H:%M}'})
    plan['notes'] = {}
    meta = {e['rel']: {k: (str(v) if k == 't' else v) for k, v in e.items()} for e in items}
    plan['_meta'] = meta
    pp = os.path.join(work, 'plan.json')
    json.dump(plan, open(pp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'{len(items)} files in {len(groups)} groups (a new group after {a.gap} min without filming).')
    for g in plan['groups']:
        print(f"  {g['folder']:28} {len(g['files']):4} files  {g['from']} -> {g['to'][-5:]}   sheet: {g['sheet']}")
    print('\nPlan:', pp)


def cmd_apply(a):
    plan = json.load(open(a.plan, encoding='utf-8'))
    root, meta, notes = plan['root'], plan.get('_meta', {}), plan.get('notes', {})
    if os.path.exists(os.path.join(root, LOG)):
        sys.exit(f'{LOG} already exists here: this folder is already sorted. Undo first.')
    moves = []
    for g in plan['groups']:
        folder = re.sub(r'[<>:"/\\|?*]', '', g['folder']).strip().rstrip('.')
        for rel in g['files']:
            m = meta.get(rel, {})
            sub = [folder]
            if plan.get('orientation') and m.get('shape'):
                sub.append(m['shape'] if m.get('kind') == 'video' else 'Photos')
            if plan.get('short') and m.get('kind') == 'video' and 0 < m.get('d', 0) < plan['short']:
                sub.append(f"Under {plan['short']:g} seconds")
            dst = os.path.join(*sub, os.path.basename(rel))
            if os.path.normcase(dst) != os.path.normcase(rel):
                moves.append((rel, dst))
            lrf = os.path.splitext(rel)[0] + '.LRF'
            if os.path.exists(os.path.join(root, lrf)):
                moves.append((lrf, os.path.join(LRF_DIR, os.path.basename(lrf))))
    for src, dst in moves:
        if not os.path.exists(os.path.join(root, src)):
            sys.exit('Missing (nothing moved): ' + src)
        if os.path.exists(os.path.join(root, dst)):
            sys.exit('Would overwrite (nothing moved): ' + dst)
    if len({d.lower() for _, d in moves}) != len(moves):
        sys.exit('Two files would land on the same name (nothing moved). Rename one group first.')
    done = []
    try:
        for src, dst in moves:
            os.makedirs(os.path.dirname(os.path.join(root, dst)), exist_ok=True)
            shutil.move(os.path.join(root, src), os.path.join(root, dst)); done.append((src, dst))
    finally:
        with open(os.path.join(root, LOG), 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh); w.writerow(['From', 'To']); w.writerows(done)
    for src in sorted({os.path.dirname(s) for s, _ in done if os.path.dirname(s)}, key=len, reverse=True):
        p = os.path.join(root, src)                                  # old folders the sort emptied (undo makes them again)
        while os.path.normcase(p) != os.path.normcase(root) and os.path.isdir(p) and not os.listdir(p):
            os.rmdir(p); p = os.path.dirname(p)
    final = {s: d for s, d in done}
    lst, had = os.path.join(root, LIST), {}
    if os.path.exists(lst):                                          # keep descriptions written earlier, and the old file
        try:
            for r in csv.DictReader(open(lst, encoding='utf-8-sig')):
                if r.get('File'):
                    had[r['File'].lower()] = [r.get('What happens') or '', r.get('Good for') or '']
        except Exception:
            pass
        shutil.copy2(lst, os.path.join(root, LIST_OLD))
    notes = {**{k: v for k, v in had.items()}, **{k.lower(): v for k, v in notes.items()}}
    with open(os.path.join(root, LIST), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh)
        w.writerow(['File', 'Folder', 'Recorded', 'Seconds', 'Shape', 'What happens', 'Good for'])
        for g in plan['groups']:
            for rel in g['files']:
                m, n = meta.get(rel, {}), notes.get(os.path.basename(rel).lower()) or notes.get(rel.lower()) or ['', '']
                n = n if isinstance(n, list) else [n, '']
                dst = final.get(rel, rel)
                w.writerow([os.path.basename(rel), os.path.dirname(dst), m.get('t', '')[:16], m.get('d', ''), m.get('shape', ''), n[0], n[1] if len(n) > 1 else ''])
    folders = sorted({os.path.dirname(d) for _, d in done})
    print(f'Moved {len(done)} files into {len(folders)} folders. Undo log: {LOG}; clip list: {LIST}')
    for f in folders:
        print('  ' + f)


def cmd_undo(a):
    root = os.path.abspath(a.folder)
    lp = os.path.join(root, LOG)
    if not os.path.exists(lp):
        sys.exit('No ' + LOG + ' here: nothing to undo.')
    rows = list(csv.DictReader(open(lp, encoding='utf-8')))
    back = 0
    for r in reversed(rows):
        src, dst = os.path.join(root, r['To']), os.path.join(root, r['From'])
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst) or root, exist_ok=True); shutil.move(src, dst); back += 1
    for dp, dns, fns in sorted(os.walk(root), key=lambda x: -len(x[0])):          # remove folders the sort made, if now empty
        if dp != root and not os.listdir(dp):
            os.rmdir(dp)
    lst, old = os.path.join(root, LIST), os.path.join(root, LIST_OLD)
    if os.path.exists(old):                                          # the clip list as it was before sorting
        os.replace(old, lst)
    elif os.path.exists(lst):
        os.remove(lst)
    os.replace(lp, lp.replace('.csv', f' (undone {time.strftime("%Y-%m-%d %H.%M")}).csv'))
    print(f'Moved {back} of {len(rows)} files back.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)
    a = s.add_parser('plan'); a.add_argument('folder'); a.add_argument('--gap', type=float, default=45)
    a.add_argument('--orientation', action='store_true'); a.add_argument('--short', type=float, default=0)
    s.add_parser('apply').add_argument('plan')
    s.add_parser('undo').add_argument('folder')
    a = p.parse_args()
    {'plan': cmd_plan, 'apply': cmd_apply, 'undo': cmd_undo}[a.cmd](a)


if __name__ == '__main__':
    main()
