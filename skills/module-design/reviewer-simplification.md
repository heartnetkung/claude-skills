# Reviewer 1 — simplification and reuse

- **Does this need to exist yet?** Ask it of every capability before asking whether it is small.
  Name the observation that makes it necessary and say whether it has happened; "we will want
  this once X lands" means X is the consumer, and X has not landed. Then price the deferral:
  what would adding it later cost, and is anything lost that cannot be reconstructed from what
  the project already retains? **Cheap-to-add-later plus nothing-lost is a defer, not a build** —
  and the reverse is what keeps this from deferring everything. A capability that gets harder or
  impossible to add once data stops being kept is a build, now.
- The smallest thing that satisfies the contract. Propose cuts to the spec and to the boundary
  surface: an export nobody calls, a flag with one caller, a config knob never turned.
  **Smallest is counted at the callers, not in the diff.** A one-line change to shared code is
  not smaller than an optional parameter if it changes what existing callers get; the parameter
  whose default is today's behavior is the smaller change, however many lines it threads.
- **Is this a solved problem?** Before accepting a bespoke procedure, name the established method
  for the problem class — a statistical test, a known algorithm, a standard protocol — and say why
  the hand-built version beats it. An empty package search is not evidence that no method exists:
  the method is often a few lines of stdlib once you know its name, which is exactly the case a
  library search cannot surface.
- **Reuse before writing.** Search the repo for code that already does this and propose refactoring
  it to fit, rather than a second implementation beside it. Search by symbol and filename over the
  packages the boundary's Upstream names — not a read of the tree.
- **Library before hand-rolling.** A battle-tested library is more robust and more flexible than
  code written this week; the default is to import. Only three rejections count: unmaintained, no
  real user base, or it drags in far more than the module needs. These are *not* rejections —
  "we'd only use 10% of it", "I could write it in 50 lines", "one more dependency". All three
  admissible rejections are claims about the world today, so look them up rather than recalling
  them: "unmaintained" cites a last-release date. Look up only the candidates you end up naming
  in a finding — one lookup each, not a survey of the field.
- A proposed dependency is a proposed edit to the dependency manifest and whatever gates it
  (lockfile, layering rules, unused-dependency checks). Name that cost in the finding; `CLAUDE.md`
  says what is off-limits.
