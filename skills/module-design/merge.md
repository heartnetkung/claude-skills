# Phase 2 — at merge / commit / push

`spec.md` and `boundary.md` are deleted here. Deletion is unconditional, so there is no
per-section judgment. What remains is capturing what could not be written in advance.

1. **Does the shipped module match the boundary it was reviewed against?** Diff `boundary.md`'s
   *Public interface* and *Libraries considered* lists against what actually exists — the module's
   exports, and the manifest. Every divergence is either a bug to fix in the code or a decision to
   record in `contract.md`. This is the only step where the design review binds the code: without
   it a module can name a library, pass both reviewers, hand-roll it anyway during implementation,
   and have the evidence deleted at step 7.
2. **What did building this teach you that is unwritten?** → `contract.md`. The step that cannot
   be front-loaded: failure modes found by running it, a fallback that mattered more than
   expected, a missed ordering constraint. Expect little here if the code is already well
   commented — then step 4 is where the value is. Re-read `boundary.md` here too: a cost or
   compatibility constraint that turned out to be real is a contract clause, not a deleted line.
3. **Is the contract now saying what a docstring already says?** For each clause the contract
   gained or changed, read its `Sites:` line and then read the docstrings and comments there. Where
   both carry the same mechanism, cut the contract back to the caller's assumption and leave the
   mechanism at the site. This is the only step that can catch it: at design time there was no code
   to compare against, so both reviewers were blind to it, and every edit afterwards sees one side
   at a time. While you are in the clause, check its `Sites:` still resolve — a renamed symbol
   leaves a citation that reads fine and points at nothing.
4. **Any "don't fix this" still only in your head?** → comment at the call site, with its revisit
   condition. Typically a rejected alternative and the condition that would justify revisiting it.
   One with no call site to sit at goes in the commit message, not the contract.
   *Tiebreaker vs. the contract: does the reader need the rule, or the history? The history loses
   even where the reader would never open the file — a reader who never opens it cannot act on why
   something there was rejected.*
5. **Usage** — invocations, flags, cost levers → `--help` and the root README's command index.
6. **Fix references** — grep for both doomed filenames; package docstrings and entry-point scripts
   commonly cite them.
7. **Delete the spec and the boundary** (`git rm` both), in the same commit as the implementation.

Then re-read `contract.md` whole: still self-contained, under the cap, citing nothing deleted.
`removal.md`, next to this file, is the pass — it runs on every edit to a contract, here and on any
later one, and over the whole file rather than the touched clauses once its prose passes ~180
lines.
