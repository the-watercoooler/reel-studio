# Reel Studio

**Turn your own videos into Instagram reels, cut to the beat, on your own computer.** Windows 10/11 and macOS.

**To start: paste this page's link into [Claude Code](https://claude.com/claude-code).** That's all. Claude explains what
Reel Studio does, sets it up with you, and helps you make your first reel.

---

## For Claude Code: someone just pasted this link

The person wants to try Reel Studio. They're probably not technical, so keep every step plain and short, and ask before
installing or downloading anything.

**Start talking right away; don't wait to be asked.** The whole visit is one guided flow. The person shares a
folder, shares a reel they love, and says which clips. You set things up, build the reel and open it in Reel Studio.

**1. Introduce it in about 5 lines, then ask your first question:** "Shall I set it up? It takes about 5 minutes and I'll
ask before installing anything." What to say it does:
- **Copies a reel they love with their own clips:** they save a reel; you match its song, cuts and words, pick
  their best clips for every shot, and open the finished edit.
- **Tweak and export:** swap shots, edit words, colour looks, then export in 2K/4K for Instagram.
- **Sorts and describes footage:** tidies a camera dump into folders (only after a yes) and describes every clip, so
  they can search "sunset" or "cheers".
- **Carousels too:** 4:5 photo carousels.
- **Private:** everything runs on their computer. Videos are never uploaded; files only move if they ask to sort them.

**2. Get the code** (after they say yes):
- Folder: suggest `C:\Users\<name>\Reel Studio` (Windows) or `~/Reel Studio` (Mac), and confirm it with them.
- If `git` works: `git clone https://github.com/the-watercoooler/reel-studio "<folder>"`.
- Otherwise download `https://github.com/the-watercoooler/reel-studio/archive/refs/heads/main.zip` (under 1 MB) into
  that folder and unzip it there.

**3. Install the Reel Studio plugin.** This gives Claude its Reel Studio skills in every folder from now on: make a reel,
setup, sort footage, add footage, describe clips, copy a reel, update. Run these yourself:
```
claude plugin marketplace add the-watercoooler/reel-studio
claude plugin install reel-studio@reel-studio
```
If `claude` isn't a command on this computer (for example in the desktop app), ask the user to type these two lines
into the chat themselves:
```
/plugin marketplace add the-watercoooler/reel-studio
/plugin install reel-studio@reel-studio
```
Claude Code asks them to confirm the new plugin source. That's expected.

**4. Set it up.** New skills may need a restart to show up, so don't wait for them. Read
`plugin/skills/setup-reel-studio/SKILL.md` in the downloaded folder and follow it: install Python and FFmpeg if
missing (ask first), add their footage folder, start Reel Studio.

**5. Make their first reel.** Go straight on with `plugin/skills/make-reel/SKILL.md`, one question at a time:
1. "Is there a reel you'd love to copy? Save it to your computer and tell me where it is."
2. "Which clips should I use?"
3. Build the reel, open it in Reel Studio, and show them how to tweak and export it.

---

## What a friend sees
1. Paste the link into Claude Code. Claude explains Reel Studio and asks to set it up.
2. Say yes. Claude adds the Reel Studio plugin, installs what's missing (asking first) and asks where your videos are.
3. Claude asks for a reel you'd love to copy. Save it to your computer and say where it is.
4. Claude asks which clips to use, builds the whole reel (every shot, the song, the words) and opens it in Reel Studio.
5. Watch it, swap any shot, export it for Instagram. A **Reel Studio** icon is on your desktop for next time.

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
Ask Claude to **update Reel Studio**. It uses `git pull`, or downloads the newest ZIP if you installed without git, and
never touches your reels. Then start it again. An open page shows **Reload now**.
