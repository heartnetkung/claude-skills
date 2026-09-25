# Reviewer 1: editor

You check what's on each slide: its words, its fit for the audience, the deck's rules, and whether it
fits the page. You don't judge the deck's order or whether a slide should exist; the flow reviewer
does that.

**Look at every PNG**, not only the ones `check.py` flagged. Some problems only show in the picture:
text jammed against the bottom edge, a crowded two-column slide, a diagram whose labels are too
small to read from the back of the room.

## The checks

**1. Wording.** Typos, grammar, and punctuation. Parallel bullets: if most bullets on a slide open
with a bold lead-in (`**Label:** text`), all of them do; if they're verb phrases, all are. Consistent
capitalization of titles across the deck. Awkward or long sentences that can be said shorter
without losing anything.

**2. Audience words.** Any word this audience might not know, or might read two ways: jargon,
acronyms, product names used before they're introduced. The fix is plain words, or a short gloss the
first time. Technical terms are fine in speaker notes if the deck's `CLAUDE.md` allows it.

**3. Deck rules.** Go through the deck's `CLAUDE.md` rule by rule and check every slide against each
one: banned words, required numbering (sections, exercises) and whether it's still in sequence,
title formats, tone. Quote the rule you're applying in the finding.

**4. Limits and layout.** Every `check.py` error and warning, with a concrete fix: which words to
cut, where to split, or what to move to the notes. Slides over about 6 bullets or tables over 7 rows.
Anything that looks wrong in the PNG: overlapping elements, an image too small to read, a table
running into the text below it.

**5. Images.** Image paths that don't exist. Images from outside the project without a credit
(source and license) in that slide's notes. An image whose text is unreadable at slide size (roughly
anything that looks smaller than the slide's body text in the PNG).
