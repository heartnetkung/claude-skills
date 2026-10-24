---
name: start-ticket
description: Start work on a ticket — read it, explore the code, decide the obvious questions yourself and ask the rest, and get the plan approved, including how it splits into PRs. Use when starting work on a ticket or GitHub issue, as soon as you read it and before drafting the plan or spec.
---

# Starting a ticket

## 1. Read the ticket

Read the ticket and its comments in full. Then show it on the status line:
`bash .claude/skills/start-ticket/set-status.sh <ticket> "<title>" preparation`.

## 2. Explore the codebase

Find the code the ticket touches and what it can reuse, before asking anything: a question the
code answers is not one to put to the user.

## 3. Settle the open questions

List what you need to get the intention and the details right. Sort each question:

- **Obvious** — one answer follows from the ticket, the code or the project's principles.
  Decide it yourself and report the decision.
- **Not obvious** — ask the user.

Both start the same way, explained step by step from what a user of the product would see,
not in implementation terms:

- **Where:** UI — which part of the screen; backend — which route; edge case — how it
  happens; principle violation — which principle and which requirement.
- **Problem:** what is unsettled, in user terms.

A decision then gives:

- **Decision:** the choice made.
- **Why:** the reason, and the preference that would flip it — "the simplest design, unless
  correctness in every edge case is preferred" — so the user sees the tradeoff.

A question to the user then gives labeled choices (a, b, c), each with a concrete example —
input and result, or for timing and concurrency a short lane timeline in a code block — the
principles it keeps or bends, and its cost in one line. Ask one question at a time, in plain
text, and invite a free-form answer; it is often a principle that makes a third option.

## 4. Choose the design route

Use the `module-design` skill for every change except trivial ones like a rename.

## 5. Plan and get approval

Show the plan to the user and wait for approval before coding. Obvious questions that come up
after approval are decided and reported the same way; the important ones also go in the PR
description.

The plan includes the PR split. Decide it yourself: 1 to 4 PRs. Do not ask the user how to
split the ticket; they review the split in the plan and can object there. Each PR can be
reviewed and merged on its own and leaves `main` working. The PRs go one at a time, each based on
`main` and opened after the previous one merges, never stacked (`open-pr` says why). Prefer fewer PRs; split only where
one PR would touch too many files to review, or where an early PR unblocks the rest. Give one
line per PR: its scope and the files it touches.

When starting work on each PR, run `bash .claude/skills/start-ticket/set-status.sh <ticket> "<title>" <i> <total>`;
after the last PR merges, run `bash .claude/skills/start-ticket/set-status.sh clear`.
