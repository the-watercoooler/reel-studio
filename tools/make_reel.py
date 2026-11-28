"""Build a whole reel from a template and a list of clips, save it in Reel Studio and open it there.
Reel Studio must be running (it checks every clip and saves the reel).

    python tools/make_reel.py templates                       every template: key, title, length, number of shots
    python tools/make_reel.py shots <template>                each shot: when it starts, how long, words on screen
    python tools/make_reel.py clips [<folder key>] [--find sunset] [--portrait] [--min 2.5]
                                                              clips to choose from: id, seconds, shape, folder, description
    python tools/make_reel.py build <template> --name "Dinner reel" --clips 1000004,1000012,... [--grade warm]
    python tools/make_reel.py build <template> --name "..." --picks picks.json
    python tools/make_reel.py build <template> --name "..." --auto <folder key>

--clips  one clip id per shot, in order (a clip may be used twice). Each shot uses the middle of its clip.
--picks  a JSON list, one entry per shot: {"clip": id, "in": seconds, "cx": 0.5, "cy": 0.5, "zoom": 1.0}
         "in" is where in the clip the shot starts; cx/cy move the 9:16 crop (0..1), zoom >= 1 punches in.
--auto   spread the folder's clips over the shots in the order they were filmed (a quick first draft).
Opens http://localhost:<port>/?reel=<id>. Add --no-open to only print the link.
"""
import argparse, json, sys, urllib.request, webbrowser

FPS = 30
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')          # Windows consoles: titles have dashes and emoji
except Exception:
    pass


def api(port, path, body=None):
    req = urllib.request.Request(f'http://localhost:{port}{path}', data=None if body is None else json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode('utf-8')).get('error')
        except Exception:
            msg = str(e)
        sys.exit('Reel Studio said: ' + str(msg))
    except OSError:
        sys.exit(f'Reel Studio is not running on port {port}. Start it first (Start Reel Studio), then try again.')


def shots(T):
    b = [0] + list(T['cuts']) + [T['total']]
    return [(b[i], b[i + 1] - b[i]) for i in range(len(b) - 1)]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--port', type=int, default=8777)
    s = p.add_subparsers(dest='cmd', required=True)
    s.add_parser('templates')
    s.add_parser('shots').add_argument('template')
    c = s.add_parser('clips'); c.add_argument('col', nargs='?'); c.add_argument('--find', default='')
    c.add_argument('--portrait', action='store_true'); c.add_argument('--min', type=float, default=0)
    b = s.add_parser('build'); b.add_argument('template'); b.add_argument('--name', required=True)
    g = b.add_mutually_exclusive_group(required=True)
    g.add_argument('--clips'); g.add_argument('--picks'); g.add_argument('--auto')
    b.add_argument('--grade'); b.add_argument('--no-open', action='store_true')
    a = p.parse_args()

    d = api(a.port, '/api/init')
    T = d['templates']
    if a.cmd == 'templates':
        for k, t in T.items():
            print(f"{k:12} {t['total'] / FPS:5.1f}s  {len(t['cuts']) + 1:3} shots  {'song' if t.get('song') else 'silent'}  {t['title']}")
        return
    if a.cmd in ('shots', 'build') and a.template not in T:
        sys.exit(f"No template '{a.template}'. Templates: {', '.join(T)}")
    if a.cmd == 'shots':
        t = T[a.template]
        print(f"{t['title']}: {t['total'] / FPS:.1f} s, {len(t['cuts']) + 1} shots")
        for i, (f0, n) in enumerate(shots(t), 1):
            words = ' / '.join(L['text'].replace('\n', ' ') for L in t.get('texts', []) if L['f0'] < f0 + n and L['f1'] > f0)
            print(f"  shot {i:2}  at {f0 / FPS:5.2f}s  {n / FPS:4.2f}s" + (f'   words: {words}' if words else ''))
        return
    lib = [x for x in d['library'] if x.get('n', 1) > 0]
    if a.cmd == 'clips':
        cols = {c['key']: c.get('name', c['key']) for c in d.get('collections', [])}
        rows = [x for x in lib if (not a.col or x.get('col') == a.col) and (not a.portrait or x.get('o') == 'portrait')
                and (x.get('kind') == 'photo' or x.get('d', 0) >= a.min)
                and a.find.lower() in (x.get('s', '') + ' ' + x.get('l', '') + ' ' + x['f'] + ' ' + ' '.join(x.get('t', []))).lower()]
        rows.sort(key=lambda x: (x.get('col', ''), x.get('r', ''), x['f']))
        for x in rows:
            ln = 'photo' if x.get('kind') == 'photo' else f"{x.get('d', 0):.1f}s"
            print(f"{x['id']:>8}  {ln:>6}  {x.get('o', '')[:4]:4}  "
                  f"{x.get('l', '')[:28]:28}  {x['f'][:34]:34}  {x.get('s', '')}")
        print(f"{len(rows)} clips" + ('' if a.col else f"  (folders: {', '.join(f'{k} = {v}' for k, v in cols.items())})"))
        return

    t, byid = T[a.template], {x['id']: x for x in lib}
    sh = shots(t)
    if a.auto:
        vids = sorted([x for x in lib if x.get('col') == a.auto and x.get('kind') != 'photo'], key=lambda x: (x.get('r', ''), x['f']))
        if not vids:
            sys.exit(f"No videos in folder '{a.auto}'.")
        picks = [{'clip': vids[int(i * len(vids) / len(sh))]['id']} for i in range(len(sh))]
    elif a.clips:
        picks = [{'clip': int(v)} for v in a.clips.replace(' ', '').split(',') if v]
    else:
        picks = json.load(open(a.picks, encoding='utf-8'))
    if len(picks) != len(sh):
        sys.exit(f'This template has {len(sh)} shots but {len(picks)} clips were given. Give exactly one per shot.')
    slots, notes = [], []
    for i, ((f0, n), pk) in enumerate(zip(sh, picks), 1):
        x = byid.get(int(pk['clip']))
        if not x:
            sys.exit(f"Shot {i}: there is no clip {pk['clip']}.")
        need, dur = n / FPS, x.get('d', 0)
        if x.get('kind') == 'photo':
            start = 0.0
        else:
            if dur < need:
                notes.append(f'shot {i}: clip {x["id"]} is {dur:.1f}s, shorter than the shot ({need:.1f}s); it will hold its last frame')
            start = pk.get('in', dur / 2 - need / 2)
            start = round(max(0.0, min(float(start), dur - need)), 2)
        slots.append({'clip': x['id'], 'in': start, 'cx': float(pk.get('cx', 0.5)), 'cy': float(pk.get('cy', 0.5)),
                      'zoom': max(1.0, float(pk.get('zoom', 1.0))), 'reverse': False})
    proj = json.loads(json.dumps(d['starters'][a.template]))
    proj.update(id='', name=a.name, slots=slots)
    if a.grade:
        proj['grade'] = a.grade
    r = api(a.port, '/api/project', proj)
    url = f"http://localhost:{a.port}/?reel={r['id']}"
    for n in notes:
        print('Note:', n)
    print(f'Made "{a.name}": {len(slots)} shots, {t["total"] / FPS:.1f} s.  Open: {url}')
    if not a.no_open:
        webbrowser.open(url)


if __name__ == '__main__':
    main()
