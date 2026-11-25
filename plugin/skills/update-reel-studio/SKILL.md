---
name: update-reel-studio
description: Update Reel Studio to the newest version from GitHub (the-watercoooler/reel-studio). Use when the user asks to update/upgrade Reel Studio, or a feature they heard about is missing.
---

# Update Reel Studio

**First, find Reel Studio's folder** (this skill can be used from any folder):
1. Read the file `.reel-studio` in the user's home folder. It holds the folder's path, written by the setup script.
2. If there is no such file, look for `Reel Studio` in the home folder: a folder holding `studio.py`.
3. If it's still not found, ask the user. If it isn't installed yet, use **setup-reel-studio** first.

Run every command below from that folder, with its Python:
- Windows: `.venv\Scripts\python.exe`
- Mac: `.venv/bin/python`

Their reels, folders, templates and settings live in git-ignored files. An update never touches them.

1. **Check how it was installed.**
   - **A `.git` folder exists:**
     1. Run `git status --short`. Only untracked or ignored personal files should show.
     2. If code files were changed locally, ask before discarding anything.
     3. Then run `git pull --ff-only`. Git for Windows may be at `%LOCALAPPDATA%\Programs\Git\cmd\git.exe` if `git`
        isn't on PATH.
   - **No `.git` (it came as a ZIP):**
     1. Ask first.
     2. Download `https://github.com/the-watercoooler/reel-studio/archive/refs/heads/main.zip` into a new, empty temp folder.
     3. Copy its files over the app folder.
     4. Never delete `projects/`, `templates/`, `audio/`, `insp/`, `cache/`, `collections.json`, `library.json` or `.venv/`.
2. **Refresh packages.** Run the setup script again. It's quick when nothing is missing:
   - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File setup\setup-windows.ps1 -Yes -NoShortcuts`
   - Mac: `bash setup/setup-mac.sh --yes --no-shortcut`
3. **Restart.** Tell the user to close the Reel Studio window and start it again from its shortcut. A newer copy also takes
   over from an older one by itself. Open pages show **Reload now**.
4. **Say what's new** in a line or two, from `git log --oneline` since the last version.
