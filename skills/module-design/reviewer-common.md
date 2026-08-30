# Module design review — rules for every reviewer

You are reviewing a new module's design documents before any implementation code is written.
Read this file, then the role file named in your prompt.

## Read first, in this order

Before proposing anything:

1. Root `README.md` — what the project is ultimately for.
2. `CLAUDE.md` — the rules binding any change here.
3. The dependency manifest — what is already paid for.
4. The module's `contract.md`, `spec.md`, `boundary.md`.

**Never read the lockfile.** It is generated, it is often tens of thousands of tokens, and it
answers exactly one question — "is this package already here?" — which is a grep for the name.

## Rules

The first is what your role file is for; the rest are how your report comes back.

- **Maintainability comes first, and simplicity is how it is bought.** Not token cost, not line
  count, not cleverness — what the next reader has to hold in their head to change this safely.
  A design that trades simplicity away for anything else names the consumer buying it. Two things
  that read as free and are not: a *concept* costs more than the lines implementing it, so count
  concepts; and a number that decays — a tuned threshold, a measured band, a limit copied from a
  vendor's docs — is a standing obligation to re-measure, and nothing fails visibly when it goes
  stale.
- **Do not edit any file.** Your output is a report.
- **Findings are uncapped**, ranked, severity-tagged, and concrete: file → what to cut or replace
  → why. Never drop a minor one — several minor findings seen side by side are usually one
  misconception, and that is visible only when all of them are reported.
- **Questions are ranked and listed separately**, and only for what changes the recommendation.
  Anything below that bar is reported as a flagged assumption ("assumed X; wrong if Y") instead.
- **A contract clause may be challenged only while it is uncommitted** — `git status --porcelain
  <absolute path to contract.md>` prints something (`??` untracked, `A`/`M` staged or modified).
  Not `git diff HEAD`: that is silent for an untracked file, which is what a brand-new module's
  contract is, and the rule would disable itself in the exact case it exists for. A committed
  clause is accepted and out of scope, even when the file around it changed in this branch. A
  challenge is advisory: raise it for the user to decide, never apply it yourself.
