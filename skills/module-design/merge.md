# Phase 2 — at merge / commit / push

`spec.md` and `boundary.md` are deleted here. Deletion is unconditional, so there is no
per-section judgment. What remains is capturing what could not be written in advance.

1. **Does the shipped module match the boundary it was reviewed against?** Diff `boundary.md`'s
   *Public interface* and *Libraries considered* lists against what actually exists — the module's
   exports, and the manifest. Every divergence is either a bug to fix in the code or a decision to
   record in `contract.md`. This is the only step where the design review binds the code: without
   it a module can name a library, pass both reviewers, hand-roll it anyway during implementation,
   and have the evidence deleted at step 6.
2. **What did building this teach you that is unwritten?** → `contract.md`. The step that cannot
   be front-loaded: failure modes found by running it, a fallback that mattered more than
   expected, a missed ordering constraint. Expect little here if the code is already well
   commented — then step 3 is where the value is. Re-read `boundary.md` here too: a cost or
   compatibility constraint that turned out to be real is a contract clause, not a deleted line.
3. **Any "don't fix this" still only in your head?** → comment at the call site, with its revisit
   condition. Typically a rejected alternative and the condition that would justify revisiting it.
   *Tiebreaker vs. the contract: could the reader plausibly never open this file?*
4. **Usage** — invocations, flags, cost levers → `--help` and the root README's command index.
5. **Fix references** — grep for both doomed filenames; package docstrings and entry-point scripts
   commonly cite them.
6. **Delete the spec and the boundary** (`git rm` both), in the same commit as the implementation.

Then re-read `contract.md` whole: still self-contained, under the cap, citing nothing deleted.
Over 150 lines — here or on any later edit to an existing contract — read `removal.md`, next to
this file, and make the pass it describes.
