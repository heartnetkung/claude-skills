---
name: module-design
description: How to design a new module before coding it, and how to retire its build docs afterwards. Use when starting a new module or package (contract.md, then spec.md, then boundary.md, then two parallel review agents for simplification/reuse and design quality), and again when that module's implementation is about to be committed or pushed (promote what building taught you, then delete the spec and boundary). Also use when asked to prune, retire, or clean up an existing spec or module README.
---

# Module docs: contract.md is permanent, the build docs are not

- **`contract.md`** — what the rest of the system may assume of this module, and the rules keeping
  it true. Permanent. Written *before* the spec.
- **`spec.md`** — scaffolding for writing the code. **Deleted when the module lands.** Never
  named `README.md`: a doomed file must not wear a durable name.
- **`boundary.md`** — everything the module touches on the outside. Written *after* the spec, in a
  separate pass. **Deleted when the module lands**, alongside the spec.

**Default home for a durable fact is the code it is about** — call-site comment, test, docstring,
`--help`, or the commit message that made the change. `contract.md` is the narrow exception; when in doubt it is not a clause.

**One-way citation:** the doomed files may cite the contract, never the reverse. A contract citing
`spec.md §Foo` breaks when the spec is deleted.

## Resolve this skill's directory first

The rest of this skill is in files next to this one, and the reviewers are spawned with their
rubrics named by path. **Resolve the directory to an absolute path now** — an agent starts cold
and cannot resolve "next to the skill you were spawned from", and neither can you when this skill
is loaded from a plugin rather than a project copy, because the body arrives as text with no path
attached. Glob `**/skills/module-design/SKILL.md`, project `.claude/skills/` first, then
`~/.claude/plugins/`. **If it is not found, stop and tell the user** — never guess a path.

---

## Phase 1 — starting a module

`contract.md`, then `spec.md`, then `boundary.md`, then two review agents, then reconcile.
**Read `design.md` now**, before writing any of them. No implementation code until that sequence
has finished.

## Phase 2 — at merge / commit / push

The build docs are deleted here, but only after what could not be written in advance is captured —
and that is the part that gets skipped when it is done from memory. **Read `merge.md` and follow
its seven steps.**
