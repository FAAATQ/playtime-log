# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Put the numbers in data/, once, and never touch them again.

    uv run fetch.py

The numbers are my own game playtime records. They live in a Feishu sheet
("游戏履历") that a sync script exports to JSON for my personal website. This
file takes that exported JSON and copies it into data/ byte for byte, so the
repository carries its own copy and every later script reads the local file.

The raw file is committed, so on any other machine (or with the wifi off) this
script finds data/games.generated.json already present, says so, and stops.
SOURCE only matters on the machine that produced the export.
"""

import shutil
from pathlib import Path

# Where the export lands on my machine. Not needed once data/ is committed.
SOURCE = Path.home() / "Documents/AICoworks/FatQPersonalWebsite/data/games.generated.json"

FILE = "games.generated.json"
HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(source, path):
    """Copy the export in once. If it is already in data/, do nothing."""
    if path.exists():
        print(f"data/{path.name} is already here ({path.stat().st_size // 1024} KB). "
              "Delete it to copy it in again.")
        return path

    if not source.exists():
        raise SystemExit(
            f"data/{path.name} is missing and the export is not at {source}.\n"
            "The committed copy is what the scripts read; restore it with:\n"
            f"    git checkout data/{path.name}"
        )

    DATA.mkdir(exist_ok=True)
    shutil.copyfile(source, path)
    print(f"copied data/{path.name} ({path.stat().st_size // 1024} KB). Now: git add data")
    return path


if __name__ == "__main__":
    fetch(SOURCE, DATA / FILE)
