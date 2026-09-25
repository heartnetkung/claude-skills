# Visuals: diagrams you draw, photos you find

Three kinds of picture, made three different ways:

- **Diagrams** (processes, cycles, comparisons, before/after, timelines, hierarchies, charts from
  numbers the deck already has): you draw them as SVG and render them to PNG.
- **Photos** (people at work, objects, places, anything real): scout agents search freely licensed
  sources, and the best one goes on the slide.
- **Screenshots**: a text-based screen, such as a terminal or command output, is drawn as a
  diagram from the real output. A graphical screen comes from the user (the Screenshots rule in
  `visual-rules.md`).

## 1. Pick the slides

Apply `visual-rules.md` to every slide: which slides get a diagram, which
get a photo (and which of the four photo cases), and the photo cap. Every `<!-- visual: … -->`
marker in the deck is a candidate too, but it still has to pass those rules.

Show the list as plain text, numbered, one line per slide: `diagram:`, `photo (CASE):`, or
`screenshot:`, and what the picture would show. The user picks (`1 3 4`, or "all").

## 2. Diagrams

Follow `svg-style.md`. For each picked diagram:

1. Write `images/DIAGRAM.svg` in the deck folder (kebab-case `DIAGRAM` from the slide title).
2. Render it: `<skill-dir>/scripts/render.sh DECK_DIR/images/DIAGRAM.svg` → `images/DIAGRAM.png`.
3. **Read the PNG and look at it.** Check for clipped or overlapping text, arrows that don't touch
   their boxes, uneven spacing, and labels too small to read. Fix the SVG and render again until it's
   clean. Never place a PNG you haven't looked at.
4. Notes line: `Diagram source: images/DIAGRAM.svg (render with the slides skill's render.sh)`.

## 3. Photos

### Start one scout per slide, all in one message

`Agent` calls with `subagent_type: general-purpose`, all in **one message** so they run
concurrently. Each prompt gives:

- the rubric to read first, as an absolute path: `<skill-dir>/image-scout.md`
- the slide's Markdown, pasted, the photo case from `visual-rules.md` (recognition, analogy, quote,
  or example), and one line on what the picture should get across
- the deck's `CLAUDE.md` path, if it exists (for the audience)
- its own scratch directory (`SCRATCH/scout-N`, where `SCRATCH` is your scratchpad directory, or a
  new temporary directory if you have none) and the path `<skill-dir>/scripts/find_image.py`
- the image names already used in the deck's `images/`, so the scouts don't reuse a name. Scouts
  running at the same time can still pick the same name; if two do, rename one before copying.

Don't summarize the rubric into the prompt.

### Keep every pick in the deck, place #1 without asking

For each scout's report:

1. **Copy the scout's picks (up to 5) into `images/`** as
   `{two_word_name}_{rank}_{cv|ci}.{png|jpg}`, e.g. `new-colleague_1_cv.jpg` …
   `new-colleague_5_ci.jpg`. `cv` means commercial use is allowed (commercial_valid), `ci` means it
   isn't (commercial_invalid). There's no section in the name, so reordering the deck never makes a
   name wrong. To find the slide that uses an image, search the Markdown for its name. They all stay
   in `images/`, flat, including the ones not placed.
2. **Record every pick in `images/CREDITS.md`**, one table row each:
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

### Show the user the candidates

Per slide, a numbered list of the candidates (up to 5), each with its file name, one line on what it
gets across, and its **license**: the license name, cv or ci, and what it requires (credit,
share-alike, no edits). Mark the one that's placed. **If the placed one is `ci`, say so plainly**
and name the best cv alternative, since a ci image can't be used in anything commercial. Close with
how to swap: "slide 14 → 3".

**If the scout found fewer than 5, or no cv image, say so** and give the user the choices: supply an
image, drop the photo, or search again with different words (a new scout, only if asked).

A swap changes the image path in the Markdown and replaces the credit line in the notes with that
file's row from `images/CREDITS.md`. The other files stay in `images/`.
