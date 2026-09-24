#!/bin/zsh

cd "$(dirname "$0")/.." || exit 1

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Run: brew install uv"
  read "?Press Return to close..."
  exit 1
fi

echo "Starting the playtime genre page..."
echo "Keep this Terminal window open while using the page."
echo "Press Control+C here to stop the server."
echo
uv run start.py
