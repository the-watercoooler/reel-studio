---
name: sort-footage
description: Sort a messy folder of videos and photos (straight off a phone, DJI or camera) into tidy sub-folders by moment, place or day, with an undo log and a clip list. Use when the user asks to sort, organise or tidy their footage or clips into folders, or says a folder is a mess. Files are only moved after they say yes; nothing is deleted or renamed.
---

# Sort a footage folder

**First, find Reel Studio's folder** (this skill can be used from any folder):
1. Read the file `.reel-studio` in the user's home folder. It holds the folder's path, written by the setup script.
2. If there is no such file, look for `Reel Studio` in the home folder: a folder holding `studio.py`.
3. If it's still not found, ask the user. If it isn't installed yet, use **setup-reel-studio** first.

Run every command below from that folder, with its Python:
- Windows: `.venv\Scripts\python.exe`
- Mac: `.venv/bin/python`

The tool is `tools/sort_footage.py`. It **moves** files inside the footage folder. It never deletes, renames or
overwrites anything, and it keeps a log so every move can be undone.

1. **Which folder?** Ask for the footage folder's path, or use one from `collections.json`. Ask if they want two extras:
   - **Portrait / Landscape** sub-folders in each group (handy for reels: portrait is ready to use).
   - **Short clips set aside**: clips under 3 seconds go in an "Under 3 seconds" sub-folder (kept, just out of the way).
2. **Make a plan.** Run `python tools/sort_footage.py plan "<folder>"`, adding `--orientation` and/or `--short 3`.
   - It groups files by when they were filmed. A new group starts after 45 minutes without filming; change that with
     `--gap 90` (a day out) or `--gap 20` (a busy party).
   - It prints each group and the path of its contact sheet, then the path of `plan.json`.
   - If it says the folder was sorted before, stop and ask: undo first, or sort a sub-folder.
3. **Look at every contact sheet.** Work out what each group is: a place, a moment, an activity ("Dinner on the
   terrace", "Old town walk", "Cocktail shoot"). Groups that are clearly the same moment can be merged; one group that
   is clearly two moments can be split.
4. **Propose the folders to the user** as a short list: `1 Old town walk - 12 Jun (34 files)`. Keep the number at the
   front so the folders stay in order. Ask: "Shall I move the files like this?" They can rename, merge or change
   anything. **Don't move anything until they say yes.**
5. **Edit the plan with Python** (UTF-8). In `plan.json`:
   - Set each group's `"folder"` to the agreed name.
   - To merge, move the `"files"` of one group into another and delete the empty group. To split, make a new group.
   - Optional: `"notes"` maps a file name to `["what happens", "good for"]`. These go into the clip list.
   - Leave `"_meta"` alone.
6. **Apply it.** Run `python tools/sort_footage.py apply "<plan.json>"`. It checks everything first and moves nothing
   if a file is missing or a name would clash. It writes two files at the top of the footage folder:
   - `_sorting log.csv`: every move, used for undo.
   - `_Clip list.csv`: file, folder, time, length, shape, plus your notes. Reel Studio reads it.
   DJI `.LRF` preview files go to `_LRF proxies`. Reel Studio still uses them for fast previews.
7. **Update Reel Studio.** If this folder is already in Reel Studio, rescan it; clips keep their ids, so existing reels
   still work:
   ```
   curl -X POST http://localhost:8777/api/collections/rescan -H "Content-Type: application/json" -d "{\"key\":\"<key>\"}"
   ```
   Or, if it's not running: `python studio.py --scan <key>`. If the folder isn't in Reel Studio yet, offer
   **add-footage-folder**. Then offer **describe-clips** so search works.
8. **Report back:** how many files went into which folders, and how to undo:
   `python tools/sort_footage.py undo "<folder>"` puts every file back where it was.
