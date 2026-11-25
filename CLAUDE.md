# Reel Studio: instructions for Claude

Reel Studio is a local reel editor that runs on **Windows and macOS**:
- `studio.py` is a Python standard-library web server driving FFmpeg and Pillow.
- `studio.html` is the editor page.
- `carousel*.py` and `carousel.html` are Carousel Studio at `/carousel`.

The person you're helping is probably not a developer. Explain in plain words, and **ask before installing or
downloading anything**.

## Skills: use these for the common jobs
| Skill | When |
|---|---|
| `setup-reel-studio` | first-time setup on a new computer: Python, FFmpeg, packages, shortcut, first folder |
| `add-footage-folder` | bring in a folder of clips (a trip, an event) |
| `describe-clips` | look at the clips and write descriptions so search and tags work |
| `make-template` | turn an inspiration reel they saved into a template: same song, cuts and words |
| `update-reel-studio` | get the newest version from GitHub |

**Already set up?** If `.venv/` and `collections.json` (or `library.json`) exist here, setup is done.

## When someone is new
**Not set up yet:**
1. Introduce Reel Studio in about 5 lines (see "For Claude Code" in README.md).
2. Offer to set it up.
3. Follow **setup-reel-studio** all the way to their first exported reel.

**Already set up:**
- If they ask "what can you do?", offer: make or edit a reel, add a footage folder, describe clips, make a template
  from a reel they saved, update.
- Help them do it in Reel Studio. Make sure it's running (`/api/version`); start it if not.

## Rules
- **Never commit personal data.** These are git-ignored on purpose, so don't force-add them:
  - `collections.json`, `projects/`, `templates/`, `audio/`, `insp/`, `cache/`, `.venv/`
  - the user's own footage folders, which are never inside this folder
- **Don't edit `projects/*.json` while Reel Studio is open in a browser.** The page autosaves its own copy and will
  overwrite yours. Make a new project file instead, or ask the user to close the tab.
- **Write JSON and CSV from Python**, UTF-8. PowerShell's `Set-Content` adds a byte-order mark. Quote paths that contain spaces.
- **Keep the app "Python + FFmpeg, double-click to start":**
  - no new packages without asking
  - nothing Windows-only or Mac-only without a fallback for the other
  - fonts go through `fontfind.py`
  - opening Explorer or Finder goes through `open_in_files()`
- **After changing `studio.py`, restart the server.** Starting it again makes a newer copy take over the port. For
  `studio.html` changes, a page reload is enough. Open pages show "Reload now".

## How it fits together
| Where | What |
|---|---|
| `collections.json` | footage folders: key, name, root, out (export folder), skip, base (each folder's block of 1,000,000 clip ids) |
| `cache/collections/<key>.json` | a folder's clip index: id, path, length, size, orientation, description, tags, recorded time |
| `cache/thumbs`, `cache/proxies` | library thumbnails, and 960 px preview copies (DJI `.LRF` files are used when present) |
| `projects/<id>.json` | a reel: template, cuts (frames at 30 fps), slots (clip, in, cx, cy, zoom, speed, look…), texts |
| `templates/<key>.json` + `.m4a` + `.mp4` | a beat to cut to: total frames, cuts, grade, texts, `song`, optional `starter` (copied to `audio/` and `insp/` at start) |
| `Blank` (built into `studio.py`) | 15 s, a cut every 45 frames, silent |
| `fontfind.py` | fonts by Windows file name, with Mac stand-ins; a `fonts/` folder here wins |
| `setup/` | `setup-windows.ps1`, `setup-mac.sh`, the app icon |
| `tools/` | `contact_sheets.py` (for describe-clips), `make_template.py` (for make-template) |

**Command lines.** Use `.venv`'s Python when it exists:
- `python studio.py --add-folder "<path>" --name "<name>"`
- `python studio.py --scan <key>`
- `python studio.py --port 8790 --no-browser`, a test copy

**Server endpoints you may call:**
- `POST /api/collections/rescan {"key": …}`
- `POST /api/templates/reload`
- `GET /api/version`
