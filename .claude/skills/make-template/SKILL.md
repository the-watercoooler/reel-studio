---
name: make-template
description: Turn an inspiration reel (a video the user saved) into a Reel Studio template - same song, same cut points, same on-screen words - so they can remake it with their own clips. Use when the user shares a reel they like, says "make a template", "copy this reel" or "use this song/edit".
---

# Make a template from an inspiration reel

A template is a beat to cut to: the reel's length, where every cut falls, its sound, and its on-screen words. Their own
clips then fill the shots. **Copy the original exactly**: same song, same cuts, same words and timing. The user
only swaps in their footage.

1. **Get the video file.** Ask the user to save the reel to their computer (e.g. an Instagram reel they downloaded or
   screen-recorded). Then ask where it is. Don't download from Instagram or other sites yourself.
2. **Make the base.** Pick a short `--key` (letters, digits, `-` or `_`) and a title, then run with `.venv`'s Python:
   ```
   python tools/make_template.py "<reel.mp4>" --key <key> --title "<title>"
   ```
   It finds the cuts (scene changes) and writes three files:
   - `templates/<key>.json`
   - `templates/<key>.m4a`, the sound
   - `templates/<key>.mp4`, the reel, shown as "Original reel"

   It also prints the path of a sheet with the middle frame of every shot.
   - **Too few cuts** (fast-cut reels): run again with `--threshold 0.2`. Delete the three files first.
   - **Too many** (flashes, fast camera moves): use `--threshold 0.4`.
   - For exact checking, extract frames around a suspicious cut with FFmpeg and look at them.
3. **Read the words.** Look at the shot sheet and, where words change mid-shot, at extra frames. Add each on-screen
   text to `"texts"` in `templates/<key>.json`, using Python with UTF-8:
   ```json
   {"text": "the words", "f0": 0, "f1": 45, "x": 0.5, "y": 0.2, "size": 80, "style": "clean",
    "color": "#ffffff", "anim_in": "none", "anim_out": "none", "lh": 1.15}
   ```
   - `f0`/`f1`: first and last frame at 30 fps.
   - `x`/`y`: the centre of the text, as a share of width and height.
   - `size`: font pixels on a 1080-wide reel.
   - `style`: one of `lyric serif hand bold arc script clean impact hp_serif hp_italic hp_text hp_num hp_caps hp_script`.
     Pick the closest look. See the styles in `studio.py`, `STYLES`.
   - `anim_in`: `fade`, `type` (letter by letter) or `words` (word by word).
   - `"\n"` makes a new line.
4. **Load it.** If Reel Studio is running, call `POST http://localhost:8777/api/templates/reload` and ask the user to
   reload the page. If it's not running, it loads on the next start.
5. **Start a reel on it.** In the reel menu, the user picks **+ New reel on "<title>"**. It starts with their newest
   clips, then they swap shots. Compare against **Original reel** beside the edit.

The sound and the original video are the creator's. They stay on this computer: `templates/` is git-ignored and
never shared.
