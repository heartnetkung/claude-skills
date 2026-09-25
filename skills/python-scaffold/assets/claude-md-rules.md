# CLAUDE.md rule bank

Not a template — a bank. Assemble the generated `CLAUDE.md` from ALWAYS plus
whichever ASK rules the interview selected. Emit as a flat bullet list, no
headings, no "(always)" annotations.

The reason this is a bank and not a file to copy: a rule that is merely *true
here* becomes a silent default for every project ever scaffolded. "Don't worry
about security" is fine in a research spike and wrong in anything that touches
a user. Rules that cannot be universally true must be chosen out loud.

---

## ALWAYS — universal preference, or tied to a tool the scaffold installs

```
- Be Concise in your answer.
- Be minimalist in your design.
  - Add a field, class, parameter, or column only when something reads it now. No speculative plumbing — reintroduce it when a consumer lands.
- Comments describe code that exists.
  - No roadmap comments ("Phase 2 field", "every later arm keeps this", "v2 axis"). Usually a symptom — delete the code if it violates minimalist principle, not just the comment.
  - Cite contract.md in the same package, nothing else. Never a section number: §5b renumbers silently and no tool checks it.
- Do not edit tach rules. If not editing the rules introduce significant boilerplate, stop and ask user.
- Use red-green TDD.
- Prioritize code reuse. Refactor existing shared code to support new use case if need be.
- Always draft spec or show plan to the user prior to coding, so that user can confirm. Spec is for large implementation and plan is for the small. Both should include key logic of what it is doing and in which file/module.
  - For a new module under `src/{{PKG}}/`, invoke the `module-design` skill first — it governs the whole pre-code sequence (`contract.md`, `spec.md`, `boundary.md`, then two review agents) and the build docs' deletion at merge.
- Editing a `contract.md`: read the `module-design` skill's `removal.md` first and make the pass it describes over the clauses you touched — every time, not on a threshold. Most of what bloats a contract is added by changes that never load the skill, so a trigger those changes cannot miss is the only one that works. Once the file's prose passes ~180 lines — clauses only, not the `Tests:`/`Sites:` lines — that pass covers the whole file instead.
- When you ask the user to decide something, always provide context and a few choices for user to choose.
- Before committing a non-trivial change under `src/{{PKG}}/`: run `/simplify`, then code review, then commit (before precommit hook fires).
  - Never ask the user to type `/code-review`. Invoke it yourself from the repo root as a background subprocess: `claude -p "/code-review" --allowedTools "Read Grep Glob Bash(git *)"`. It runs in a fresh session, reads the working tree and this file, and prints findings to stdout — relay them. Expect minutes on a large diff.
- extensively log important information across branches execution flow. If something goes wrong, this information will be given to LLM to figure out what's wrong.
```

Each earns its place by pairing with something installed:

| Rule | Enforced by |
|---|---|
| no speculative plumbing | `vulture` (`min_confidence = 80`) |
| no roadmap comments | `vulture`, for the code the comment justifies |
| cite contract.md, never a section number | vendored `module-design` skill |
| do not edit tach rules | `tach check` in pre-commit |
| red-green TDD | `pytest` + coverage `branch = true` |
| contract before spec | vendored `module-design` skill |
| removal pass on every contract edit | vendored `module-design` skill (`removal.md`) |
| `/simplify` then review before commit | both are built-in Claude Code skills |

The comment rules are the one pair no tool checks directly, and that is the
point of writing them down: `vulture` deletes unreachable code but has nothing
to say about a comment promising a version that never ships. The rule survives
by routing to a test rather than asserting a verdict: the comment is a signal,
and the minimalism rule above decides whether the code it describes should go.
Deleting the sentence and keeping an unread field is the failure mode it names.

Drop the tach rule if the user declined layers. Drop all three `module-design`
lines — the contract.md citation rule, the spec sub-bullet, and the contract-edit
rule — if the skill was not vendored. Otherwise a rule points at something that
is not there, and the whole file starts reading as decoration.

The contract-edit rule is the only thing that ever opens `removal.md`. Vendoring the
skill without it ships a file nothing routes to.

The `/simplify` sub-bullet is not padding: without it the model reports the
review as the user's next step and stops, which is the failure the rule exists
to prevent. `.claude/settings.json` allows `Bash(claude -p:*)` so the subprocess
does not prompt.

---

## ASK — genuinely contextual, no safe default

### Git workflow

- **solo** (default — matches how this scaffold is normally used):
  ```
  - Commit and push in main branch. Never generate non-main branch on the server side.
  ```
- **team**:
  ```
  - Branch from main and open a PR. Never push directly to main.
  ```

### Rigor stance

- **default: emit nothing.** Silence means normal care.
- Only if the user explicitly asks for it:
  ```
  - this is an experimental project and not production. Don't worry too much about security and compliance.
  ```

Never infer this one from the project sounding research-y. Opting out of
security thinking is a decision a person makes, not a vibe a scaffolder reads.
