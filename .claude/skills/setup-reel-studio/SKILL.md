---
name: setup-reel-studio
description: First-time setup of Reel Studio on this computer (Windows or Mac). Use when someone has just downloaded or cloned Reel Studio, asks to "set it up", "install it" or "get it running", or when Python, FFmpeg or the .venv folder is missing.
---

# Set up Reel Studio

The person is probably not a developer. Say what each step does in one plain line. **Ask before installing anything**.
The scripts install only after a yes.

**Already set up?** If `.venv/` and `collections.json` (or `library.json`) exist, skip to step 4, then step 5.

## 1. Which computer
- **Windows 10/11**: go on.
- **macOS**: go on.
- **Linux**: it may work but isn't supported. Say so, then try the Mac steps with the system package manager.

## 2. Run the setup script
It checks Python 3.10+ and FFmpeg, installs whichever is missing, creates `.venv` with the two Python packages, and
adds a "Reel Studio" shortcut. It's safe to run again.

**Before running it:**
1. Tell the user what may be installed:
   - **Windows:** Python 3.12 (~30 MB) and FFmpeg (~100 MB), both via winget.
   - **Mac:** the same two via Homebrew.
2. Get their OK, then run it non-interactively with "yes" (because you already asked).

**Windows:**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File setup\setup-windows.ps1 -Yes
```
- If winget shows an admin prompt, tell the user to approve it.
- If Python or FFmpeg is installed but "not found yet", run the script again. It refreshes PATH.

**Mac:**
```bash
bash setup/setup-mac.sh --yes
```
- Exit code 2 means **Homebrew is missing**. Homebrew needs the user's Mac password, so the user must install it themselves:
  1. Open https://brew.sh.
  2. Copy the one-line command and paste it into Terminal. Never type or handle the password for them.
  3. When it finishes, run the script again.
- First launch from Finder may say "unidentified developer": right-click **Reel Studio** on the Desktop, then **Open**.

## 3. Add their footage
Use the **add-footage-folder** skill. It asks where the videos are and reads that folder.

## 4. Start it
- Tell the user to double-click **Reel Studio** on the Desktop:
  - Windows: a black window opens.
  - Mac: a Terminal window opens.
- Keep that window open. Their browser opens http://localhost:8777.
- Or start it yourself in the background:
  - Windows: `.venv\Scripts\python.exe studio.py`
  - Mac: `.venv/bin/python studio.py`
- Check that http://localhost:8777/api/version answers.

## 5. Make the first reel together
"My first reel" is already open, filled with their clips. Walk them through it one step at a time, waiting for each:
1. **Watch it:** press ▶ under the preview.
2. **Swap a shot:** click a shot on the timeline, then click a clip on the left. Drag the teal box to pick which part
   plays.
3. **Add words:** press **T**, then double-click the text on the video and type.
4. **Colour:** click **🎨** and hover the looks; click one to keep it.
5. **Export:** click **Export reel**. The file lands in a `Reels` folder inside their footage folder. Offer to open it.

Also mention:
- the **📁 menu** (top left) for adding another trip or event
- **Format** (9:16 / 4:5 / 1:1 / 16:9)

## 6. Next steps
Offer these two, then let them pick:
- **describe-clips:** "Want me to look through your clips and describe them, so you can search 'sunset' or 'cheers'?"
- **make-template:** "Got a reel you love? Save it to your computer and I'll copy its song, cuts and words so your clips
  can fill it."

Tell them how to come back: open **Reel Studio** from the desktop. For help, open Claude Code in the Reel Studio folder
and just ask, e.g. "make a reel from my Goa clips", "make it warmer", "update Reel Studio".
