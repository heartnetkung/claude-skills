# Review: two reviewers, then one list for the user

Two agents review the deck in parallel, each against its own rubric: an **editor** (wording, audience,
the deck's rules, slide limits, images) and a **flow reviewer** (the story, cutting, merging,
simplifying). You merge their reports, fix what's certain, and ask about the rest.

## 1. Prepare

```bash
<skill-dir>/scripts/loop.sh DECK_DIR/NAME-slides.md --png SCRATCH/slides-png
```

`SCRATCH` is your scratchpad directory, or a new temporary directory if you have none. Keep the
full `loop.sh` output for the editor: the linter's limit warnings, and `check.py`'s overflow report,
which measures what the PNGs don't show, such as text 1 mm past its box.

## 2. Start both reviewers in one message

Two `Agent` calls in **one message** so they run concurrently, `subagent_type: general-purpose`.
Each prompt contains only:

- the rubric files to read, in order, as absolute paths:
  - editor: `<skill-dir>/reviewer-common.md`, then `<skill-dir>/reviewer-editor.md`
  - flow: `<skill-dir>/reviewer-common.md`, then `<skill-dir>/reviewer-flow.md`, then
    `<skill-dir>/visual-rules.md`
- the deck: absolute paths to `NAME-slides.md`, the deck folder's `CLAUDE.md` (if it exists), and
  the PNG folder
- editor only: the `loop.sh` output, pasted. The flow reviewer judges structure, not layout.

**Don't summarize a rubric into the prompt.** Naming the file is the whole mechanism. An agent that
didn't read its rubric still returns a confident report about nothing.

## 3. Merge

1. **Dedup.** The same problem from both reviewers is one finding.
2. **Cuts first.** If the flow reviewer proposes cutting or merging a slide, the editor's findings
   on that slide depend on that answer. Ask the cut, and apply the editor's findings only if the slide
   survives.
3. **Split certain from uncertain.** A fix is certain when the deck or the file tree settles it: a
   typo, a grammar slip, a broken image path whose target exists, a number that disagrees with its
   neighbours (such as a section number). Anything that changes meaning, tone, or structure is a
   judgment, however sure you are: every cut, merge, move, and rewrite. The same sentence is in
   `reviewer-common.md`; keep the two identical. **The reviewers' `certain` tags are a hint; you
   decide.** Check each one against this rule, since reviewers tend to mark cuts as certain.

## 4. Fix what's certain

Apply the certain fixes directly in `NAME-slides.md`. Keep the author's voice and vocabulary. Never
add a fact the deck didn't already carry.

## 5. Report, then ask

First list what you changed: one line per fix, grouped by check, naming the slide and what changed.
No counts and no summary of how much better it is. A check that found nothing: say so in three words.

Then the questions, as **plain text at the end of your reply, not AskUserQuestion**.

**Ask the top 10 only.** Rank every open finding across all checks by how much it changes the deck:
cuts, restructuring, and contradictions before wording tweaks. The top 10 become questions. Group
them by check, in this order:

**Flow:** Story, Coherence, Concision, Correctness-only wording, Stale references, Visuals
**Editor:** Wording, Audience words, Deck rules, Limits and layout, Images

Number straight through the groups (don't restart per group). For each question give:

- the number, the slide number and title, and the exact text quoted;
- one sentence on what's wrong;
- two or three options lettered `A`, `B`, `C`, concrete enough to pick without reopening the deck.
  The last option is always leaving it as it is.

```
**Concision**

3. slide 12 "Safe habits" — "Work on copies of important files"
   Slide 54 makes the same point with more context.
   A) cut the bullet here
   B) cut it on slide 54 and keep this one
   C) leave as is

Reply with the picks, e.g. 1A 2C 3B.
```

Rank inside each group by how much the deck changes.

**Nothing is dropped.** After the questions, list the rest under **Also found**: one line each with
the slide number, what's wrong, and the proposed fix, but no options. End with: "Reply `more` for the
next 10 as questions." Findings that depend on an unanswered cut stay in that list until the cut is
decided.

## 6. Apply the picks

Apply the chosen options, then run the loop in `SKILL.md` (build, check, reload). Record nothing
about rejected findings.
