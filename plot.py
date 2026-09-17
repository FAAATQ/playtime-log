# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

The numbers: hours recorded per game, from my own playtime log.

The picture: the 25 games I have spent the most hours in, longest first. Bar
length is hours; bar colour is the platform I played it on. One message — where
the time actually went.

Why a bar chart: the data has one number (hours) and one label (the game), so
length-against-category is the transformation that fits it. There is no date
column in this file, so there is no line to draw.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "games.generated.json"
PICTURE = "plot.png"
TOP = 25                       # how many games make it onto the picture

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"

# One colour per platform. Anything unlisted falls back to the last entry.
PLATFORM_COLOURS = {
    "PC": "#d6591d",
    "Switch": "#2f6f9f",
    "Console": "#6b8f3a",
    "Mobile": "#8a5aa8",
}
FALLBACK = "#8a8580"

INK = "#1a1a1a"
MUTED = "#6f6a64"


def load(path):
    """The raw export, as a list of game records."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)["games"]


def in_the_picture(games):
    """Only records the owner chose to show, and only ones with hours on them.

    `rollupMode` marks a card whose hours live in a series card instead, so it is
    skipped rather than counted twice. In this file no visible record is marked
    that way, but the check stays: it is the rule the data is maintained under.
    """
    kept = []
    for game in games:
        if game.get("visible") != 1:
            continue
        if game.get("rollupMode") == "series":
            continue
        if not (game.get("hours") or 0) > 0:
            continue
        kept.append(game)
    return kept


def platform_of(game):
    """The first platform listed, or a dash if the record names none."""
    platforms = game.get("platforms") or []
    return platforms[0] if platforms else "—"


def qualifier_mark(game):
    """Hours are not all equally exact. Say so on the label rather than hide it."""
    return {"approx": "~", "minimum": "≥"}.get(game.get("hoursQualifier"), "")


def main():
    games = in_the_picture(load(DATA))
    games.sort(key=lambda g: g["hours"], reverse=True)
    top = games[:TOP]

    total = sum(g["hours"] for g in games)
    print(f"{DATA.name}: {len(games)} games with hours on them, {total}h in total")
    for game in top[:5]:
        print(f"   {game['titleEn']}: {game['hours']}h ({platform_of(game)})")

    # Oldest at the top of the picture, biggest at the bottom of the list.
    top.reverse()

    names = [g["titleEn"] for g in top]
    hours = [g["hours"] for g in top]
    colours = [PLATFORM_COLOURS.get(platform_of(g), FALLBACK) for g in top]

    fig, ax = plt.subplots(figsize=(11, 9))
    bars = ax.barh(names, hours, color=colours, height=0.72)

    for bar, game in zip(bars, top):                 # the loop over the numbers
        ax.text(bar.get_width() + max(hours) * 0.012,
                bar.get_y() + bar.get_height() / 2,
                f"{qualifier_mark(game)}{game['hours']}h",
                va="center", ha="left", fontsize=9, color=INK)

    ax.set_xlabel("hours recorded", fontsize=11, color=INK)
    ax.set_xlim(0, max(hours) * 1.14)
    ax.text(0, 1.012, f"Bar length is hours played · bar colour is the platform · "
                      f"{total:,}h across {len(games)} games in the log",
            transform=ax.transAxes, fontsize=10, color=MUTED, va="bottom")
    ax.set_title("The 25 games I have put the most hours into",
                 fontsize=15, color=INK, pad=34, loc="left")

    seen = []
    for game in top:
        name = platform_of(game)
        if name not in seen:
            seen.append(name)
    handles = [plt.Rectangle((0, 0), 1, 1,
                             color=PLATFORM_COLOURS.get(p, FALLBACK)) for p in seen]
    ax.legend(handles, seen, title="platform", frameon=False,
              loc="lower right", fontsize=9, title_fontsize=9)

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#d8d4ce")
    ax.spines["bottom"].set_color("#d8d4ce")
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(axis="x", color="#e8e4de", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
