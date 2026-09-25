# New deck: outline, approval, first draft

The outline is to a deck what a plan is to code: short-lived, cheap to change, and deleted once the
first draft exists. Nothing in the deck ever refers to it.

## 1. Set up the folder

In the deck folder (ask where if the user didn't say):

- copy `<skill-dir>/assets/reference.pptx` → `reference.pptx`
- copy `<skill-dir>/assets/outline-skeleton.md` → `NAME-outline.md`

Pick `NAME` in kebab-case from the topic. Check with the user if it's not obvious.

## 2. Write the outline

Fill `NAME-outline.md`. Ask about what you can't infer: audience, the one thing they should leave
with, length, the presenter. Don't guess the audience: it decides the wording of every slide.

- **Each top-level bullet is one section.** It becomes a `##` title slide in the draft.
- Under each section, one line per content slide: what the slide is for, not its bullets.
- Mark slides that want a picture with `visual:` and a few words on what it shows (a process, a
  comparison, a cycle). Aim for one per section; text-only decks are the default failure.
- Time per section, if the talk has a slot.

Show the outline and iterate on it until the user approves. Restructuring here costs one line; after
the draft it costs slides.

## 3. Draft the whole deck from the approved outline

Copy `<skill-dir>/assets/skeleton.md` → `NAME-slides.md` and write the first draft in one pass. The
structure is fixed:

1. **Title slide:** front matter `title:` and `subtitle:`. No Markdown needed.
2. **One agenda slide:** `### What we'll cover`, listing the sections (a table if there are times).
3. **Per outline section:** `## Section title`, then its content slides as `###`, fully drafted:
   real bullets, not placeholders, plus speaker notes for each. A section always has at least one
   content slide.
4. **One closing slide:** `### Thank you! Questions?` It lists the 3–5 questions this audience is
   most likely to ask, with a short answer to each in the speaker notes.

Never two title slides in a row: title → agenda, and every `##` → a `###`.

For each `visual:` line, add a comment in that slide: `<!-- visual: what it shows -->`. That's where
`visuals.md` starts. Don't draw the visuals now.

Then run the loop in `SKILL.md` (build, check, reload) and fix anything `check.py` reports.

## 4. Retire the outline

Once every outline line has its slide, the outline is done. Before deleting it, move what's still
needed:

- **Audience, tone, and wording rules** → the deck folder's `CLAUDE.md` (start from
  `<skill-dir>/assets/deck-claude-md.md` if there isn't one).
- **Open questions for the presenter** → the HTML comment at the top of `NAME-slides.md`.
- **Section times** → the agenda slide, if they're not already there.

Then delete `NAME-outline.md`.

## 5. Suggest a review, once

Tell the user the first draft is complete and suggest `/slides review`. **Suggest it; don't run it.**
The review starts two agents, and the user may want to read the draft first. Don't repeat the
suggestion on later edits.
