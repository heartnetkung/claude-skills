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
  - No roadmap comments ("Phase 2 field", "every later arm keeps this", "v2 axis"). Usually a symptom — delete what one justifies, not just the comment.
  - Cite contract.md in the same package, nothing else. Never a section number: §5b renumbers silently and no tool checks it.
- Do not edit tach rules. If not editing the rules introduce significant boilerplate, stop and ask user.
- Use red-green TDD.
- Prioritize code reuse. Refactor existing shared code to support new use case if need be.
- Always draft spec or show plan to the user prior to coding, so that user can confirm. Spec is for large implementation and plan is for the small. Both should include key logic of what it is doing and in which file/module.
  - For a new module under `src/{{PKG}}/`, invoke the `module-contract` skill first — it governs `contract.md` (written before the spec) and the spec's deletion at merge.
- When you ask the user to decide something, always provide context and a few choices for user to choose.
- extensively log important information across branches execution flow. If something goes wrong, this information will be given to LLM to figure out what's wrong.
```

Each earns its place by pairing with something installed:

| Rule | Enforced by |
|---|---|
| no speculative plumbing | `vulture` (`min_confidence = 80`) |
| no roadmap comments | `vulture`, for the code the comment justifies |
| cite contract.md, never a section number | vendored `module-contract` skill |
| do not edit tach rules | `tach check` in pre-commit |
| red-green TDD | `pytest` + coverage `branch = true` |
| contract before spec | vendored `module-contract` skill |

The comment rules are the one pair no tool checks directly, and that is the
point of writing them down: `vulture` deletes unreachable code but has nothing
to say about a comment promising a version that never ships. The rule survives
by saying which artifact is the real problem — the field, not the sentence
describing it.

Drop the tach rule if the user declined layers. Drop both `module-contract`
lines — the contract.md citation rule and the spec sub-bullet — if the skill
was not vendored. Otherwise a rule points at something that is not there, and
the whole file starts reading as decoration.

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
