# Twenty-two years of games, counted

![Twenty-five games as horizontal bars, longest first, coloured by platform](out/plot.png)

## What this is

Every game I have played for long enough to keep a record of, with the hours I
put into each one. The log exists because I write about games and design them,
and "I play a lot of shooters" is a claim that gets more useful once it has
numbers under it.

## Where the numbers come from

The record is my own playtime log. No single platform knows about all of it, so
the hours are collected from three places and assembled by hand:

- **Steam**, through the `IPlayerService/GetOwnedGames` endpoint of the Steam Web
  API (<https://developer.valvesoftware.com/wiki/Steam_Web_API>), which returns
  total minutes for every owned game. 65 of the timed records are tagged
  `hoursSource: steam`, and 70 of them carry the `steamAppId` they were matched by.
- **Nintendo Switch**, from the console's own playtime export. 74 records are
  tagged `hoursSource: switch-export`.
- **Everything else** — PlayStation, Xbox and mobile titles, where no usable API
  exists — is typed in by hand and tagged `hoursSource: manual`. That covers 12
  records, including the series cards that roll several titles into one row
  (Call of Duty, Battlefield, Halo, Borderlands, BioShock) so their hours are not
  counted twice.

Genres for the Steam titles are filled in from the Store's own `appdetails`
response rather than guessed, because `GetOwnedGames` does not report a genre.

`data/games.generated.json` is that assembled export, committed here byte for
byte, and it is the only thing the scripts read.

The file holds 224 game records. A record is one game: an English and Chinese
title, the platforms I played it on, its genres, and `hours` — the time played,
**in hours**, as an integer. 208 records are marked visible and 151 of those
carry a non-zero hour count; the rest are records I have kept but not shown, or
entries still waiting for a time to be filled in.

Each record also carries a `hoursQualifier`, because not every number is equally
exact. `exact` means the platform counted it. `approx` and `minimum` mean I
estimated it by hand, and the picture marks those bars with `~` and `≥` instead
of pretending the precision is the same.

## What the picture shows

Bar length is hours played; bar colour is the platform; the 25 longest are
shown, longest at the top. One message: where the time actually went. The top
three are series cards that roll several titles into one row, and the drop from
2,000 hours to 637 is not a gentle curve — it is a cliff, which is the honest
shape of a playtime log.

**What it hides.** It hides the 126 games outside the top 25, which together
account for a little over a thousand of the 9,114 hours. It hides genre
entirely, so a bar labelled *VRChat* gives no hint that it is not a shooter. It
flattens `approx` and `minimum` into the same bar length as `exact`, with only a
one-character mark to warn you. And the axis stops at 2,000, so the four series
cards at the top visually dominate a distribution that is mostly games under
50 hours.

## Run it

```
uv run fetch.py
uv run plot.py
```

`fetch.py` copies the export into `data/` if it is not already there; the file is
committed, so with the wifi off it simply reports that it is present.
`plot.py` reads `data/` and writes `out/plot.png`.
