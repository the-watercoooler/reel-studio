# Reel Studio

A small editor that runs on your own computer and turns **your own clips** into Instagram reels cut to the beat, with
texts, colour looks and 2K/4K export. **Carousel Studio** (at `/carousel`) does the same for 4:5 photo carousels.

> **Early days.** This is a personal project shared with friends. It runs on **Windows 10/11** only for now, and setup is
> meant to be done by **Claude Code** for you.

Everything stays on your PC. Reel Studio only *reads* the footage folders you give it. Its previews, reels and settings
live in its own folder, and none of that is ever uploaded (see `.gitignore`).

---

## Set it up with Claude Code (recommended)

1. Install [Claude Code](https://claude.com/claude-code) and open it.
2. Paste this message:

   > Set up Reel Studio for me from https://github.com/the-watercoooler/reel-studio. Put it in a folder called
   > "Reel Studio" in my home folder and follow the instructions in its CLAUDE.md.

3. Claude will:
   - check that Python and FFmpeg are installed, and ask before installing anything
   - ask where your videos are, then read that folder (it asks your permission first)
   - start Reel Studio, which opens in your browser at http://localhost:8777

### For Claude Code: getting the code
- Put it where the user asked (default: `%USERPROFILE%\Reel Studio`).
- If `git` is installed, run `git clone https://github.com/the-watercoooler/reel-studio "<folder>"`.
- If not, ask before downloading. Then get
  `https://github.com/the-watercoooler/reel-studio/archive/refs/heads/main.zip` (a few hundred KB) and unzip it into the folder.
- Then open `CLAUDE.md` in that folder and follow **First-time setup**.

---

## Set it up by hand

1. Install Python 3.10 or newer, and FFmpeg (the full build):
   ```powershell
   winget install -e --id Python.Python.3.12
   ```
   ```powershell
   winget install -e --id Gyan.FFmpeg
   ```
2. In this folder, install the two Python packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Double-click **Start Reel Studio.bat**. Your browser opens. Paste the path of your footage folder, and Reel Studio reads
   it and starts "My first reel".

Keep the black **Reel Studio** window open while you edit. Close it to stop.

## Using it
- **📁 menu** (top left): switch footage folders, or **＋ Add a folder…** for another trip or event.
- **Templates** (reel menu): *Blank* is a 15-second reel with a cut every 1.5 s. More templates (from inspiration reels)
  are files in `templates\`. Ask Claude to make one from a reel you like.
- **Click a shot**, then pick a clip on the left. Drag the teal box to choose which part plays.
- **Texts**: press `T` to add one, then double-click it on the video to type.
- **🎨** colour looks · **Format** 9:16 / 4:5 / 1:1 / 16:9 · **Export reel** (2K by default). Reels are saved in a `Reels`
  folder inside your footage folder.

## Updating
```powershell
git pull
```
Then close the black window and start **Start Reel Studio.bat** again. An open page shows **Reload now**.
