#!/bin/bash
# macOS: double-click to set up Reel Studio (Python, FFmpeg, packages, Desktop launcher).
cd "$(dirname "$0")" || exit 1
bash setup/setup-mac.sh "$@"
echo
read -r -p "Press Return to close this window. " _
