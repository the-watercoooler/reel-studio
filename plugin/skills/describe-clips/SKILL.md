---
name: describe-clips
description: Look at every clip in a Reel Studio footage folder and write a short description of each (what happens, who/what is in it), so the library search and tags work. Use when the user asks to describe, tag or catalogue their clips (to sort files into folders, use sort-footage), or says search doesn't find things.
---

# Describe the clips in a folder

**First, find Reel Studio's folder** (this skill can be used from any folder):
1. Read the file `.reel-studio` in the user's home folder. It holds the folder's path, written by the setup script.
2. If there is no such file, look for `Reel Studio` in the home folder: a folder holding `studio.py`.
3. If it's still not found, ask the user. If it isn't installed yet, use **setup-reel-studio** first.

Run every command below from that folder, with its Python:
- Windows: `.venv\Scripts\python.exe`
- Mac: `.venv/bin/python`

The result is a `_Clip list.csv` at the top of their footage folder. Reel Studio reads it for the text under each clip,
for search and for the tag chips.

1. **Which folder?** List the folders: read `collections.json`, which has a name, key and path for each. Ask which one if
   there are several.
2. **Ask before writing into their footage folder.** Say: "I'll add one small file, `_Clip list.csv`, to your folder. It
   only holds descriptions; nothing else changes." If they say no, write it into Reel Studio's own
   `cache/notes/<key>.csv` instead and tell them search won't use it yet.
3. **Make contact sheets.** Run `python tools/contact_sheets.py "<folder name or key>"`, using `.venv`'s Python. It prints
   sheet image paths (10 clips per sheet, 4 frames each) and the file names in order.
4. **Look at every sheet.** For each clip write **one plain sentence** about what happens and who or what is in it:
   - Example: "Group of friends clink glasses around a candlelit table".
   - Example: "Slow pan over a beach at sunset, waves in front".
   - Note camera moves and how good the shot is ("shaky", "blurry start").
   - Don't guess names or identities of people. Say "a woman in a white top", not a name.
   - For people who aren't the user, describe only what's visible.
5. **Write the CSV with Python, not PowerShell**, in UTF-8. Columns:
   - `File`: the exact file name.
   - `What happens`: your sentence.
   - `Good for`: optional short tags such as `*close-up`, `*people`, `*sunset`, `*cheers`. `*` marks a strong reel shot.
   - Include every clip, in the sheet order.
6. **Apply it.**
   - If Reel Studio is running:
     ```
     curl -X POST http://localhost:8777/api/collections/rescan -H "Content-Type: application/json" -d "{\"key\":\"<key>\"}"
     ```
     Or in PowerShell: `Invoke-RestMethod -Method Post -ContentType 'application/json' -Body '{"key":"<key>"}' http://localhost:8777/api/collections/rescan`.
     Then tell them to reload the page.
   - If it's not running: `python studio.py --scan <key>`.
7. **Report back:** how many clips were described. Offer a few "best shots" picks from the `*` tags.

Big folders: work through all the sheets. Don't stop after the first few, and tell the user how far you are every few sheets.
