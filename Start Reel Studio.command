#!/bin/bash
# macOS: double-click to start Reel Studio (keep this window open while you edit; close it to stop).
SELF="$0"
while [ -L "$SELF" ]; do SELF="$(readlink "$SELF")"; done      # started from the Desktop link: go to the app folder
cd "$(dirname "$SELF")" || exit 1
for b in /opt/homebrew/bin /usr/local/bin; do [ -d "$b" ] && PATH="$b:$PATH"; done
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
exec "$PY" studio.py "$@"
