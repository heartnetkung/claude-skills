# Review: two reviewers, then one list for the user

Two agents review the deck in parallel, each against its own rubric: an **editor** (wording, audience,
the deck's rules, slide limits, images) and a **flow reviewer** (the story, cutting, merging,
simplifying). You merge their reports, fix what's certain, and ask about the rest.

## 1. Prepare

```bash
<skill-dir>/scripts/build.sh DECK_DIR/NAME-slides.md
/usr/bin/python3 <skill-dir>/scripts/check.py DECK_DIR/NAME.pptx --png SCRATCH/slides-png
```

`SCRATCH` is your scratchpad directory, or a new temporary directory if you have none. Keep the
`check.py` output: both reviewers get it.

## 2. Start both reviewers in one message

Two `Agent` calls in **one message** so they run concurrently, `subagent_type: general-purpose`.
Each prompt contains only:

- the rubric files to read, in order, as absolute paths:
  - editor: `<skill-dir>/reviewer-common.md`, then `<skill-dir>/reviewer-editor.md`
  - flow: `<skill-dir>/reviewer-common.md`, then `<skill-dir>/reviewer-flow.md`
- the deck: absolute paths to `NAME-slides.md`, the deck folder's `CLAUDE.md` (if it exists), and
  the PNG folder
- the `check.py` output, pasted

**Don't summarize a rubric into the prompt.** Naming the file is the whole mechanism. An agent that
didn't read its rubric still returns a confident report about nothing.

## 3. Merge

1. **Dedup.** The same problem from both reviewers is one finding.
2. **Cuts first.** If the flow reviewer proposes cutting or merging a slide, the editor's findings
   on that slide depend on that answer. Ask the cut, and apply the editor's findings only if the slide
   survives.
3. **Split certain from uncertain.** A fix is *certain* when the deck or the file tree settles it:
   a typo, a grammar slip, a broken image path whose target you can find, a section number that
   drifted from its neighbours. Anything that changes meaning, tone, or structure is not certain,
   however good the suggestion.

## 4. Fix what's certain

Apply the certain fixes directly in `NAME-slides.md`. Keep the author's voice and vocabulary. Never
add a fact the deck didn't already carry.

## 5. Report, then ask

First list what you changed: one line per fix, grouped by check, naming the slide and what changed.
No counts and no summary of how much better it is. A check that found nothing: say so in three words.

Then the questions, as **plain text at the end of your reply, not AskUserQuestion**. Group them by
check, in this order:

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

Rank inside each group by how much the deck changes. Ask about everything: nothing is dropped for
length.

## 6. Apply the picks

Apply the chosen options, then run the loop in `SKILL.md` (build, check, reload). Record nothing
about rejected findings.
