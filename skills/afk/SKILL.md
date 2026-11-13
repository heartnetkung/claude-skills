---
name: afk
description: Work unattended until the PR is open — every approval is pre-granted and every question is decided by Claude, then filed as a `question` ticket for the user to review.
disable-model-invocation: true
argument-hint: <ticket number or task>
---

# Away from keyboard

The user is away. Carry `$ARGUMENTS` through to an open PR without stopping for them.

## Every approval is pre-granted

Wherever an instruction — CLAUDE.md, `start-ticket`, `module-design`, `open-pr`, or any other
skill — says to show a plan or spec and wait, ask the user to decide, or confirm before acting,
treat it as approved and continue. Still write the plan, spec and docs those steps produce; only
the wait is skipped. Never use AskUserQuestion and never end a turn on a question.

Run the usual chain end to end: `start-ticket` → `module-design` → red-green TDD → `/simplify`
→ code review → commit → `open-pr`. Stop once the PR is open.

## Decide every question yourself

For each question you would have asked, pick the choice that keeps the most project principles
and is cheapest to reverse, then continue. Log it as you go, in `start-ticket`'s shape:

- **Where** and **Problem**, in user terms;
- **Decision** and **Why**, with the preference that would flip it;
- **Rejected:** the other choices, one line each.

## Still off limits

The pre-approval covers decisions, not risk. Do not write to production, use production
credentials, force-push, or delete what you did not create. If the work needs one of these,
work around it, log it as a question, and open the PR as a draft.

## After the PR opens

If anything was logged, file one ticket for it:

```bash
gh label create question --color d876e3 2>/dev/null || true
gh issue create --label question --title "Questions from PR #<pr>: <ticket title>" --body-file <file>
```

The body links the PR and the ticket, then lists each logged decision, numbered, ending with
"Reply with the number and a choice to flip it." Add the issue's link to the PR description.
Report the PR and the question ticket as the final message.
