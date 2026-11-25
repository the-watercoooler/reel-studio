# Reel Studio: instructions for Claude

Reel Studio is a local reel editor:
- `studio.py` is a Python standard-library web server driving FFmpeg and Pillow.
- `studio.html` is the editor page.
- `carousel*.py` and `carousel.html` are Carousel Studio.

It runs on Windows only (Windows fonts, Explorer, `os.startfile`). The person you're helping is probably not a
developer. Explain in plain words, and ask before installing or downloading anything.

## First-time setup (someone just got this folder)

**Skip this section** if `collections.json` or `library.json` already exists here: setup is already done.

Do these in order. Tell the user what you're doing in one line per step.

1. **Check Windows.** If the OS isn't Windows, say Reel Studio doesn't support it yet and stop.
2. **Python 3.10+.** Run `python --version`.
   - If it's missing or older, ask the user. Then run `winget install -e --id Python.Python.3.12`.
   - A newly installed `python` may only be found in a new terminal. If so, use its full path:
     `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`.
3. **FFmpeg, full build.** Run `ffmpeg -version`, and check that `ffmpeg -hide_banner -filters` lists `cas` and `lut3d`.
   - If FFmpeg is missing, ask the user. Then run `winget install -e --id Gyan.FFmpeg`.
   - It installs under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\...\bin`. If `ffmpeg` still isn't found,
     add that folder to the user's PATH (ask first), or open a new terminal.
4. **Packages.** Run `python -m pip install -r requirements.txt` in this folder.
5. **Footage folder.** Ask: *"Which folder are your videos in? Sub-folders are included."*
   - The user may not know the full path. Offer to look in their Videos, Pictures, Desktop or Downloads folders, or on
     another drive.
   - Claude Code asks their permission before reading a folder outside this one.
   - List a few files to confirm the path: MP4 or MOV videos, and/or JPG or PNG photos.
   - Then run, quoting the paths:
     `python studio.py --add-folder "<full path>" --name "<short name, e.g. Goa trip>"`
   - This reads every clip and makes thumbnails, about 1 second per clip. For more than about 200 clips, run it in the
     background and tell the user.
   - It also starts "My first reel" on the Blank template.
   - Add more folders the same way, or later in the app (📁 menu → ＋ Add a folder…).
   - **Optional:** a `_Clip list.csv` at the top of a footage folder, with `File` and `What happens` columns, gives every
     clip a searchable description. If the user wants, you can write it by looking at frames of their clips.
6. **Start it.** Tell the user to double-click **Start Reel Studio.bat** and keep the black window open. It opens
   http://localhost:8777 in their browser.
   - If you start it yourself, run `python studio.py` in the background.
   - Check that `http://localhost:8777/api/version` answers.
7. **Show them around** in 4–5 short lines (see "Using it" in README.md):
   - the 📁 menu
   - click a shot, then a clip
   - `T` for text
   - 🎨 colour looks
   - Export reel: files go to `<footage folder>\Reels`

## Rules
- **Never commit personal data.** The user's folders, `collections.json`, `projects/`, `templates/`, `audio/`, `insp/` and
  `cache/` are git-ignored on purpose. Don't force-add them.
- **Don't edit `projects/*.json` while Reel Studio is open in a browser.** The page autosaves its own copy and will
  overwrite yours. Make a new project file instead, or ask the user to close the tab.
- **Write JSON from Python, not PowerShell** (`Set-Content` adds a byte-order mark). Quote Windows paths that contain spaces.
- **Use Pillow and FFmpeg as they are.** No new dependencies without asking. The app should stay "Python + FFmpeg, double-click to start".
- **After changing `studio.py`, restart the server.** Run the .bat again; a newer copy takes over the port from an older one.
  For `studio.html` changes, a page reload is enough. Open pages show "Reload now".

## How it fits together
| Where | What |
|---|---|
| `collections.json` | the footage folders: key, name, root, out (export folder), skip, base (each folder's id block of 1,000,000) |
| `cache/collections/<key>.json` | each folder's clip index: id, path, length, size, orientation, description, tags, recorded time |
| `cache/thumbs`, `cache/proxies` | library thumbnails, and 960 px preview copies (DJI `.LRF` files are used when present) |
| `projects/<id>.json` | a reel: template, cuts (frames, 30 fps), slots (clip, in, cx, cy, zoom, speed, look…), texts |
| `templates/<key>.json` (+ `audio/<key>.m4a`, `insp/<key>.mp4`) | a beat to cut to: total frames, cuts, grade, texts, `song`, optional `starter` |
| `Blank` (built into `studio.py`) | 15 s, a cut every 45 frames, silent |

A template made from an inspiration reel holds:
- its cut points, found from scene changes
- its on-screen texts: position, size and timing, in 1080×1920 units
- its sound, as `audio/<key>.m4a`
- the reel itself, as `insp/<key>.mp4`, shown beside the edit as "Original reel"

Copy the song and words exactly. These files are personal and stay out of git.

Useful command lines:
- `python studio.py --add-folder "<path>" --name "<name>"`
- `python studio.py --scan <key>` re-reads a folder.
- `python studio.py --port 8790 --no-browser` runs a test copy.
