---
name: make-reel
description: The guided Reel Studio flow - get the user's footage folder, get an inspiration reel they saved, ask which clips to use, then Claude builds the whole reel (every shot, words, look) and opens it in Reel Studio for them to tweak and export. Use when the user wants a reel made ("make me a reel", "make a reel from my Goa trip", "copy this reel with my clips"), and right after first-time setup.
---

# Make a reel, start to finish

The user does three things: shares a folder, shares a reel they like, and says which clips. **Claude does the rest**
and opens the finished edit in Reel Studio. Ask **one question at a time**, in plain words, and wait for each answer.

**First, find Reel Studio's folder** (this skill can be used from any folder):
1. Read the file `.reel-studio` in the user's home folder. It holds the folder's path, written by the setup script.
2. If there is no such file, look for `Reel Studio` in the home folder: a folder holding `studio.py`.
3. If it's still not found, it isn't installed: follow **setup-reel-studio** first, then come back here.

Run every command from that folder, with its Python (Windows `.venv\Scripts\python.exe`, Mac `.venv/bin/python`).
Make sure Reel Studio is running: `http://localhost:8777/api/version` answers. If not, start `studio.py` in the
background with that Python.

## Step 1. Their footage
Ask: **"Which folder are your videos in? A trip, a party, a day out."**
- If it's already in Reel Studio (`collections.json`), use it. If not, follow **add-footage-folder**.
- If the folder is one big camera dump, offer **sort-footage** first ("Want me to sort these into folders by moment
  first? Nothing moves until you say yes."). It's optional.
- **You need to know what's in the clips** to pick them well. If they have no descriptions yet (the `clips` list
  below shows none), follow **describe-clips** now. Tell them it takes a few minutes and is worth it.

## Step 2. The inspiration reel
Ask: **"Is there a reel you'd love to copy? Save it to your computer and tell me where it is."** How to save one:
- Instagram on a phone: share → **Download**, if it's offered, or use the phone's **screen recording**, then send
  the video to this computer (AirDrop, WhatsApp to yourself, Google Drive).
- On the computer: screen-record it (Windows: Win+Alt+R, or Snipping Tool's video; Mac: Cmd+Shift+5).
- Don't download it from Instagram yourself.

Then follow **make-template** to turn it into a template (same song, cuts and words).
**No reel?** Offer what's already there: `python tools/make_reel.py templates`. `blank` is 15 s, a cut every 1.5 s, silent.

## Step 3. Which clips
Ask: **"Which clips should I use? The whole folder, one part of it (say 'the beach day'), or particular moments
you want in?"** Also ask if the words should stay as in the original or change (say, their place names or date).

## Step 4. Build it
1. `python tools/make_reel.py shots <template>`: every shot's start, length and the words over it.
2. Look at the original shots: the template's shot sheet from make-template, or frames from `templates/<key>.mp4`.
   Note what each shot shows (wide view, close-up, a person, movement, a reveal) and how it moves.
3. `python tools/make_reel.py clips <folder key>` (add `--find beach`, `--portrait`, or `--min 1.5`): the clips to
   choose from, with descriptions.
4. **Pick one clip per shot.** Match what the original shot does. Most of all:
   - **portrait** clips for a 9:16 reel
   - each clip at least as long as its shot
   - no clip twice, unless the folder is small
   - the strongest shots (`*` in Good for) on the first shot and on big beats
   - calm, simple shots under words, so they're readable
   - opening shot: the best "hook" in the folder
   - then a story across the reel (arrive → do → peak → wind down) or the original's order of moments
   - Choose **where in each clip** the shot starts (`in`, in seconds) when the best moment isn't in the middle. To
     check, look at a frame:
     `ffmpeg -ss <s> -i "<clip>" -frames:v 1 -vf scale=-2:480 <scratch>.jpg`
5. Write `picks.json` (one entry per shot, in order) in a scratch folder, not in their footage:
   `[{"clip": 1000004, "in": 2.5}, {"clip": 1000012}, ...]`. Optional per shot: `"cx"`/`"cy"` (0..1) move the
   crop, `"zoom"` (1.0+) punches in.
6. `python tools/make_reel.py build <template> --name "<a short name>" --picks picks.json`.
   It checks every clip, saves the reel and **opens Reel Studio on it**.
   - If they asked for different words: edit the reel's texts in Reel Studio with them, or before building edit
     the template's `texts`. Don't edit `projects/*.json` while the page is open.

## Step 5. Show them
Tell them, in a few lines, what you made: the shots you picked and why the opening shot. Then:
1. **Watch it:** press ▶ under the preview. Compare with **Original reel** beside the edit.
2. **Change a shot:** click it on the timeline, then a clip on the left. Drag the teal box to choose which part plays.
3. **Words:** double-click text on the video to edit it.
4. **Colour:** **🎨**, hover the looks, click one to keep it.
5. **Export reel:** the file lands in a `Reels` folder inside their footage folder. Offer to open it.

Ask if they want any shot swapped. You can rebuild with new picks; it makes a new reel, and the old one stays in the
reel menu.

## Then
Offer another reel from the same template with different clips, or a new inspiration reel. Remind them they can ask
Claude Code from any folder: "make me a reel from my Goa clips".
