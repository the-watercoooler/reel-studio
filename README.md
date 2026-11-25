# Reel Studio

A small editor that runs on your own computer and turns **your own clips** into Instagram reels cut to the beat, with
texts, colour looks and 2K/4K export. **Carousel Studio** (at `/carousel`) does the same for 4:5 photo carousels.

Works on **Windows 10/11 and macOS**.

> **Early days.** This is a personal project shared with friends, and setup is meant to be done by **Claude Code** for you.
> The Mac version is new, so tell us what breaks.

Everything stays on your computer. Reel Studio only *reads* the footage folders you give it. Its previews, reels and
settings live in its own folder, and none of that is ever uploaded (see `.gitignore`).

---

## Set it up with Claude Code (recommended)

1. Install [Claude Code](https://claude.com/claude-code) and open it.
2. Paste this message:

   > Set up Reel Studio for me from https://github.com/the-watercoooler/reel-studio. Put it in a folder called
   > "Reel Studio" in my home folder, then follow its CLAUDE.md.

3. Claude will:
   - download it
   - install Python and FFmpeg if they're missing (asking first)
   - ask where your videos are
   - put a **Reel Studio** icon on your desktop

### For Claude Code: getting the code
- Put it where the user asked (default: a `Reel Studio` folder in their home folder).
- If `git` works, run `git clone https://github.com/the-watercoooler/reel-studio "<folder>"`.
- If not, ask before downloading. Then get `https://github.com/the-watercoooler/reel-studio/archive/refs/heads/main.zip`
  (under 1 MB) and unzip it there.
- Then continue in that folder. Its `CLAUDE.md` and the **setup-reel-studio** skill have the steps.

---

## Set it up by hand

**Windows:** double-click **Set up Reel Studio.bat**.
- It checks Python and FFmpeg, offers to install what's missing (with winget), and puts **Reel Studio** on your Desktop
  and in the Start menu.

**Mac:** double-click **Set up Reel Studio.command**.
- The first time, right-click it and choose **Open** if macOS warns.
- It needs [Homebrew](https://brew.sh), which installs Python and FFmpeg, and puts **Reel Studio** on your Desktop.

Then start **Reel Studio** from the Desktop. Your browser opens and asks for the folder where your videos are. Keep the
black window (Windows) or Terminal window (Mac) open while you edit.

## Using it
- **📁 menu** (top left): switch footage folders, or **＋ Add a folder…** for another trip or event.
- **Templates** (reel menu): *Blank* is a 15-second reel with a cut every 1.5 s. Ask Claude to **make a template** from a
  reel you like: same song, same cuts, same words.
- **Click a shot**, then pick a clip on the left. Drag the teal box to choose which part plays.
- **Texts**: press `T` to add one, then double-click it on the video to type.
- **🎨** colour looks · **Format** 9:16 / 4:5 / 1:1 / 16:9 · **Export reel** (2K by default). Reels are saved in a `Reels`
  folder inside your footage folder.
- Ask Claude to **describe your clips**, so search finds "sunset", "cheers" and so on.

## Updating
Ask Claude to **update Reel Studio**, or run `git pull` in this folder. Then start it again. An open page shows **Reload now**.
