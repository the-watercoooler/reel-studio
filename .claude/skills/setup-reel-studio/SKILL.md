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

## 5. A 5-line tour
- **📁 menu** (top left): switch folders, or **＋ Add a folder…**.
- **Click a shot** on the timeline, then a clip on the left. Drag the teal box to pick which part plays.
- **T** adds a text. Double-click it on the video to type.
- **🎨** colour looks · **Format** 9:16 / 4:5 / 1:1 / 16:9.
- **Export reel** saves to a `Reels` folder inside their footage folder.

Offer the next steps:
- **describe-clips**: so search finds "sunset" or "cheers".
- **make-template**: turn a reel they like into a beat to cut to.
