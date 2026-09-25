# Visuals: diagrams you draw, photos you find

Two kinds of picture, made two different ways:

- **Diagrams** (processes, cycles, comparisons, before/after, timelines, hierarchies, charts from
  numbers the deck already has): you draw them as SVG and render them to PNG. Also use a diagram for
  an app screenshot (Terminal, Claude Code): run the real command and draw a mockup of its output.
- **Photos** (people at work, objects, places, anything real): scout agents search freely licensed
  sources, and the best one goes on the slide.

## 1. Pick the slides

Apply `visual-rules.md` to every slide: which slides get a diagram, which
get a photo (and which of the four photo cases), and the photo cap. Every `<!-- visual: … -->`
marker in the deck is a candidate too, but it still has to pass those rules.

Show the list as plain text, numbered, one line per slide: `diagram:` or `photo (CASE):` and what
the picture would show. The user picks (`1 3 4`, or "all").

## 2. Diagrams

Follow `svg-style.md`. For each picked diagram:

1. Write `images/NAME.svg` in the deck folder (kebab-case `NAME` from the slide title).
2. Render it: `<skill-dir>/scripts/render.sh DECK_DIR/images/NAME.svg` → `images/NAME.png`.
3. **Read the PNG and look at it.** Check for clipped or overlapping text, arrows that don't touch
   their boxes, uneven spacing, and labels too small to read. Fix the SVG and render again until it's
   clean. Never place a PNG you haven't looked at.
4. Notes line: `Diagram source: images/NAME.svg (render with the slides skill's render.sh)`.

## 3. Photos

### Start one scout per slide, all in one message

`Agent` calls with `subagent_type: general-purpose`, all in **one message** so they run
concurrently. Each prompt gives:

- the rubric to read first, as an absolute path: `<skill-dir>/image-scout.md`
- the slide's Markdown, pasted, the photo case from `visual-rules.md` (recognition, analogy, quote,
  or example), and one line on what the picture should get across
- the deck's `CLAUDE.md` path (for the audience)
- its own scratch directory (`SCRATCH/scout-N`) and the path `<skill-dir>/scripts/find_image.py`
- the image names already used in the deck's `images/`, so the scouts don't reuse a name. Scouts
  running at the same time can still pick the same name; if two do, rename one before copying.

Don't summarize the rubric into the prompt.

### Keep all 5 in the deck, place #1 without asking

For each scout's report:

1. **Copy the top 5 into `images/`** as `{two_word_name}_{rank}_{cv|ci}.{png|jpg}`, e.g.
   `new-colleague_1_cv.jpg` … `new-colleague_5_ci.jpg`. `cv` means commercial use is allowed
   (commercial_valid), `ci` means it isn't (commercial_invalid). There's no section in the name, so
   reordering the deck never makes a name wrong. To find the slide that uses an image, search the
   Markdown for its name.
   All 5 stay in `images/`, flat. Only the one the Markdown references goes into the `.pptx`, so
   the alternatives cost disk space in the deck folder, not deck size.
2. **Record all 5 in `images/CREDITS.md`**, one table row each:
   `| File | Title | Creator | License | cv/ci | Source |`. That's where a later swap gets its credit.
3. **Put #1 on the slide** without asking. Use the scout's layout: full-width `![](images/…)`, or a
   `{.columns}` block with the text. Credit it in the slide's notes:
   `Photo: "TITLE" by CREATOR, LICENSE, SOURCE_URL`.
4. **Never crop or edit** an image marked no-derivatives (ND). Resizing it to fit the slide is fine.

Then run the loop in `SKILL.md` (build, check, reload) with `--png`, and look at each changed slide.

### Text beside a picture

A `{.columns}` slide gives the text half the width, so bullets that fit before will run off the
slide. When a picture moves into a column, cut the text to about 4 bullets of 8 words or fewer.
Keep the bold lead-ins and move the rest of each bullet into the notes. This applies to diagrams in
a column too.

### Show the user all 5

Per slide, a numbered list of the 5, each with its file name, one line on what it gets across, and
its **license**: the license name, cv or ci, and what it requires (credit, share-alike, no edits).
Mark the one that's placed. **If the placed one is `ci`, say so plainly** and name the best cv
alternative, since a ci image can't be used in anything commercial. Close with how to swap:
"slide 14 → 3".

A swap changes the image path in the Markdown and replaces the credit line in the notes with that
file's row from `images/CREDITS.md`. The other files stay in `images/`.
