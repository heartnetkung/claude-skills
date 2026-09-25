# New deck: interview, outline, approval, first draft

The outline is to a deck what a plan is to code: short-lived, cheap to change, and deleted once the
first draft exists. Nothing in the deck ever refers to it.

## 1. Set up the folder

**One deck per folder, and the folder belongs to the deck.** A deck's `CLAUDE.md`, `reference.pptx`,
and `images/` would collide with another deck's or a project's.

Pick `NAME` in kebab-case from the topic; check with the user if it's not obvious. Then the deck
folder is:

- the current directory's `NAME/` if the user didn't name a folder;
- the folder the user named, if it's new or empty;
- otherwise a new subfolder `NAME/` inside it. This covers a project folder with its own
  `CLAUDE.md` or another deck. The project's `CLAUDE.md` still applies to the deck from there.

**Never edit a `CLAUDE.md` this skill didn't create.** In the deck folder:

- copy `<skill-dir>/assets/reference.pptx` → `reference.pptx`
- copy `<skill-dir>/assets/outline-skeleton.md` → `NAME-outline.md`

## 2. Interview the user

Get the intent right before writing a single slide line. A wrong audience or goal means every slide
gets rewritten; a wrong outline line costs one line.

Ask with `AskUserQuestion`, in **two rounds** of up to 4 questions, most important first. **Skip a
question the request already answers. Where you can make a good guess, offer it as the first option
marked "(Recommended)"** so the user can confirm with one click. Every question automatically gets
an "Other" option for free text.

**Round 1: what the deck is for**

| Question | Options |
|---|---|
| **Audience:** who is in the room? | Offer 3–4 guesses from the request, e.g. non-technical staff / a technical team / managers / customers |
| **Goal:** what should they be able to do afterwards? Single choice. | **Teach a skill:** do something new (steps, exercises, a recap) · **Explain an idea:** understand it (concept → examples → implications, more diagrams) · **Get a decision:** approve, choose or fund (problem → options → recommendation → the ask) · **Report progress:** know where things stand (headline result first, then details, risks, next steps) |
| **Length** | e.g. ~10 min / ~20–30 min / ~45–60 min / 90+ min |
| **Delivery** | Presented live (short bullets, full speaker notes) / Sent to read on its own (fuller sentences on the slides) / Both |

**Round 2: how to build it**

| Question | Options |
|---|---|
| **Style:** tone and jargon together | Formal, plain words / Conversational, plain words / Technical: the audience knows the terms |
| **Source material** | Files the user will point to / A link / None: draft from general knowledge |
| **Look** | The default template / A company or Google Slides `template.pptx` / An example deck or slide to match |

**Not asked:** the presenter is the user unless they say otherwise. The language is the request's
language. The one sentence the audience should remember is proposed in the outline, where the user
reviews it anyway.

**Act on the answers:**
- Read every source the user points to before writing the outline. When there's no source, anything
  factual in the draft is a claim to check: list those claims under Open questions in the outline.
- Copy a template the user gives into the deck folder as `template.pptx`. Look at an example deck
  or slide and match its density and style.
- Write every answer into the header of `NAME-outline.md`.

## 3. Write the outline

Fill in the sections of `NAME-outline.md`, shaped by the goal. Propose the one sentence the audience
should remember at the top.

- **Each top-level bullet is one section.** It becomes a `##` title slide in the draft.
- Under each section, one line per content slide: what the slide is for, not its bullets.
- Mark slides that want a picture with `visual:` and a few words on what it shows. Apply
  `visual-rules.md`: a diagram wherever items connect (steps, branches, loops), a photo only in its
  four cases.
- Time per section, adding up to the length.
- **Get a decision:** the last section ends on a slide stating the ask: what to decide, by when.

Show the outline and iterate on it until the user approves.

## 4. Draft the whole deck from the approved outline

Copy `<skill-dir>/assets/skeleton.md` → `NAME-slides.md` and write the first draft in one pass. The
structure is fixed:

1. **Title slide:** front matter `title:` and `subtitle:`. No Markdown needed.
2. **One agenda slide:** `### What we'll cover`, listing the sections (a table if there are times).
3. **Per outline section:** `## Section title`, then its content slides as `###`, fully drafted:
   real bullets, not placeholders, plus speaker notes for each. A section always has at least one
   content slide.
4. **One closing slide:** `### Thank you! Questions?` It lists the 3–5 questions this audience is
   most likely to ask, with a short answer to each in the speaker notes.

Write to the interview's answers: its style on the slides, in the request's language. For a deck
sent to read on its own, write fuller sentences on the slides. For a live talk, write short bullets
and put the explanation in the notes. When someone else presents, write notes they can deliver
without having written the deck.

For each `visual:` line, add a comment in that slide: `<!-- visual: what it shows -->`. That's where
`visuals.md` starts. Don't draw the visuals now.

Then run the loop in `SKILL.md` and fix anything `check.py` reports.

## 5. Retire the outline

Once every outline line has its slide, the outline is done. Before deleting it, move what's still
needed:

- **Audience, goal, the one sentence, delivery, presenter, style, language** → a new `CLAUDE.md` in
  the deck folder, from `<skill-dir>/assets/deck-claude-md.md`. Every later edit follows them.
- **Open questions and claims to check** → the HTML comment at the top of `NAME-slides.md`.
- **Section times** → the agenda slide, if they're not already there.

Then delete `NAME-outline.md`.
