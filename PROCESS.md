# Process

## Tools

- **Claude Code** for `plot.py`, and for `fetch.py`. I described the picture I
  wanted and the dimension I wanted it to use, and it wrote the first version of
  both files. It also changed `fetch.py` from the template's "download a URL"
  shape into "copy a local export", because my numbers are not behind a URL.
- **uv** to run everything, so neither script needs an environment set up first.
- **matplotlib** for the drawing. Nothing else — the file reads JSON with the
  standard library and adds no data library on top.

## Kept

The template's `rows()`-style separation: reading the file, choosing the records,
and drawing are three separate functions. It matters here because "which records
count" turned out to be the only genuinely hard question in the whole script.
`in_the_picture()` is where the answer lives, and it is one function I can point
at and argue with, rather than a filter buried in a plotting call.

I also kept the `hoursQualifier` marks. The first version dropped them and drew
every bar as if all the numbers were measured the same way, which would have
made the picture claim more than the data does.

## Rejected

**A genre breakdown instead of a game ranking.** The obvious second chart was
hours per genre, and I rejected it because the file's `genres` field is a list,
not a value: a game tagged `FPS` and `Action` and `Adventure` would have its
hours counted three times. That is defensible if you say so out loud, but it
makes the chart's totals stop adding up to the hours on the first chart, and two
pictures in one repository that disagree about the total is a worse outcome than
one picture that does not answer the genre question at all.

**A time axis.** The file has `startYear` and `endYear` fields, and every one of
the 224 records has them empty. A line chart over time was the first thing I
wanted to make and there is no data in it, so the picture is a bar chart
instead. Worth writing down: the shape of the data chose the chart, not the
other way round.

## Week 4 interaction

I added one browser interaction: when I choose a genre, the page shows the games
and recorded hours associated with it. The browser fetches the committed JSON
once when the page loads, then keeps the eligible records in memory; changing
the selector only filters and redraws them. A game can have more than one genre,
so the page calls each total “associated hours” rather than suggesting genre
totals add up to 9,114 hours.

## Corrected

Smaller things a model got wrong and I kept or fixed on purpose:

- The first render put the subtitle text on top of the title. Fixed by setting
  the title's padding instead of eyeballing the offset.
- I checked the `rollupMode` rule against the data before trusting it: the file
  marks one visible record as `series`, and that record holds 0 hours, so nothing
  is double-counted today. The guard stayed in the code anyway, because it is the
  rule the log is maintained under and the next export could change that.
