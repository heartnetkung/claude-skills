# Visuals: draw diagrams as SVG, render, check, place

You can't produce photos or illustrations. You can draw **diagrams**: processes, cycles, comparisons,
before/after, timelines, hierarchies, simple icons, and charts from numbers the deck already has. You
write them as SVG, `render.sh` turns them into PNG, and you look at the PNG before it goes on a slide.

If a slide really needs a photo or a screenshot, say so and ask the user to supply one. It goes in
`images/` with a credit (source and license) in the slide's notes.

## 1. Pick the slides

Candidates, in this order:

1. every `<!-- visual: … -->` marker in the deck
2. text-only slides that describe a process, a cycle, a comparison, a before/after, a timeline, or a
   hierarchy
3. tables whose point is a trend or a comparison, which might work better as a chart

Skip slides that are already clear as text. About one visual per section is plenty.

Show the list as plain text, numbered, with one line per slide on what the picture would show, and
let the user pick (`1 3 4`, or "all").

## 2. Draw each one

Read `<skill-dir>/svg-style.md` first, and follow it. Then for each picked slide:

1. Write `images/NAME.svg` in the deck folder (kebab-case `NAME` from the slide title).
2. Render it: `<skill-dir>/scripts/render.sh DECK_DIR/images/NAME.svg` → `images/NAME.png`.
3. **Read the PNG and look at it.** Check for clipped or overlapping text, arrows that don't touch
   their boxes, uneven spacing, and labels too small to read. Fix the SVG and render again until it's
   clean. Never place a PNG you haven't looked at.

## 3. Place it on the slide

- **The picture carries the slide:** replace the bullets with `![](images/NAME.png)`. Move any detail
  the picture doesn't show into speaker notes, so the presenter still has it.
- **Picture plus a few words:** a `:::::: {.columns}` block with the text in one `::: {.column}` and
  the image in the other. Use the column canvas size from `svg-style.md`.
- Remove the `<!-- visual: … -->` marker.
- Add a notes line with the source: `Diagram source: images/NAME.svg (render with the slides skill's render.sh)`.

Then run the loop in `SKILL.md` (build, check, reload) with `--png`, and look at each changed slide's
PNG. The diagram must be readable at slide size, not just on its own.
