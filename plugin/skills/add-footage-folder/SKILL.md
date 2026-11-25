---
name: add-footage-folder
description: Add a folder of videos/photos (a trip, an event, a party) to Reel Studio's library. Use when the user wants to bring in new footage, mentions a folder of clips, or Reel Studio shows no footage yet.
---

# Add a footage folder

**First, find Reel Studio's folder** (this skill can be used from any folder):
1. Read the file `.reel-studio` in the user's home folder. It holds the folder's path, written by the setup script.
2. If there is no such file, look for `Reel Studio` in the home folder: a folder holding `studio.py`.
3. If it's still not found, ask the user. If it isn't installed yet, use **setup-reel-studio** first.

Run every command below from that folder, with its Python:
- Windows: `.venv\Scripts\python.exe`
- Mac: `.venv/bin/python`

1. **Ask where the videos are.** Use their words: "Which folder are your videos in? Sub-folders count too."
   - If they're unsure, offer to look in the usual places: Videos, Pictures, Desktop, Downloads, an external drive.
     On a Mac also check `~/Movies`.
   - Claude Code asks their permission before reading a folder outside Reel Studio. That's expected.
2. **Check the folder.** List a few files to confirm it holds videos: `.mp4`, `.mov`, `.m4v`, plus `.jpg` or `.png` photos.
   - Phone videos in **HEVC/H.265** work.
   - **HEIC photos and raw .DNG files are not read yet.** Say so if those are all they have.
   - Sub-folders starting with `_` are skipped, as is any folder listed in `skip` in `collections.json`.
3. **Pick a short name** with them ("Goa trip", "House Party 03").
4. **Add it.** Read Reel Studio's own folder first, then run (quote the paths):
   - Windows: `.venv\Scripts\python.exe studio.py --add-folder "<full path>" --name "<name>"`
   - Mac: `.venv/bin/python studio.py --add-folder "<full path>" --name "<name>"`
   - (Without a `.venv`, use `python` or `python3`.)
   - It reads every clip and makes thumbnails, about 1 second per clip. For more than ~200 clips, run it in the
     background and tell the user it's working.
   - The very first folder also starts "My first reel".
5. **If Reel Studio is already open in a browser**, the user can instead pick **📁 → ＋ Add a folder…** and paste the
   path. Or tell them to reload the page after the command finishes.
6. **Exports** from this folder's clips go to `<folder>\Reels`. Offer **describe-clips** next, so search works.

Never move, rename or delete anything in their footage folder. Reel Studio only reads it. The only thing written
there is the `Reels` folder, on export, plus `_Clip list.csv` if they agree in describe-clips.
