#!/bin/bash
# Reel Studio set-up for macOS.
# Checks Homebrew, Python 3.10+ and FFmpeg (installs Python and FFmpeg with Homebrew if you say yes), makes a private
# Python environment (.venv) with the two packages Reel Studio needs, and puts "Reel Studio" on the Desktop.
#
# Double-click "Set up Reel Studio.command", or run:  bash setup/setup-mac.sh
# Options:  --yes (don't ask, install what's missing)   --no-shortcut (skip the Desktop launcher)
# Safe to run again: it only adds what's missing.
set -e
APP="$(cd "$(dirname "$0")/.." && pwd)"
YES=0; SHORTCUT=1
for a in "$@"; do
  case "$a" in --yes) YES=1 ;; --no-shortcut) SHORTCUT=0 ;; esac
done
say() { printf '\n== %s\n' "$1"; }
ok() { printf '   %s\n' "$1"; }
ask() { [ "$YES" = 1 ] && return 0; read -r -p "   $1 [Y/n] " r; [ -z "$r" ] || [[ "$r" =~ ^[Yy] ]]; }

[ "$(uname)" = "Darwin" ] || { echo "This set-up is for macOS. On Windows use 'Set up Reel Studio.bat'."; exit 1; }
echo "Reel Studio set-up"; echo "Folder: $APP"

say "Homebrew (installs the tools below)"
BREW="$(command -v brew || true)"
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  if [ -z "$BREW" ] && [ -x "$b" ]; then BREW="$b"; fi
done
if [ -z "$BREW" ]; then
  echo "   Homebrew is not installed. It is the usual way to install tools on a Mac."
  echo "   1. Open https://brew.sh and copy the one-line install command."
  echo "   2. Paste it into Terminal and press Return (it asks for your Mac password)."
  echo "   3. Run this set-up again."
  exit 2
fi
eval "$("$BREW" shellenv)"
ok "Homebrew found: $BREW"

say "Python 3.10 or newer"
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  p="$(command -v "$c" || true)"
  if [ -n "$p" ] && "$p" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then PY="$p"; break; fi
done
if [ -z "$PY" ]; then
  ask "Python 3.10+ is not installed. Install Python 3.12 with Homebrew now?" || { echo "Python is needed. Stopped."; exit 1; }
  "$BREW" install python@3.12
  PY="$("$BREW" --prefix python@3.12)/bin/python3.12"
fi
ok "Python found: $PY"

say "FFmpeg (cuts and exports the video)"
if ! command -v ffmpeg >/dev/null 2>&1; then
  ask "FFmpeg is not installed. Install it with Homebrew now (a few minutes)?" || { echo "FFmpeg is needed. Stopped."; exit 1; }
  "$BREW" install ffmpeg
fi
ok "FFmpeg found: $(command -v ffmpeg)"

say "Python packages (Pillow, NumPy) in a private environment"
[ -x "$APP/.venv/bin/python" ] || "$PY" -m venv "$APP/.venv"
"$APP/.venv/bin/python" -m pip install --disable-pip-version-check --quiet -r "$APP/requirements.txt"
chmod +x "$APP/Start Reel Studio.command" "$APP/Set up Reel Studio.command" "$APP/setup/setup-mac.sh" 2>/dev/null || true
ok "Packages ready (.venv)"

if [ "$SHORTCUT" = 1 ]; then
  say "Desktop launcher"
  ln -sf "$APP/Start Reel Studio.command" "$HOME/Desktop/Reel Studio.command"
  ok "'Reel Studio' is on your Desktop (double-click it; the first time, right-click > Open if macOS asks)"
fi

# Remember where Reel Studio lives, so Claude's Reel Studio plugin can find it from any folder
printf '%s' "$APP" > "$HOME/.reel-studio"

say "Done"
echo "   Start Reel Studio from the Desktop (or 'Start Reel Studio.command'). Your browser opens and asks for your footage folder."
echo "   Keep the Terminal window open while you edit."
