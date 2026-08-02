---
name: python-scaffold
description: Scaffold a new Python project with strict tooling — uv, src layout, ruff, pyright strict, tach layer enforcement, deptry, vulture, and an 8-hook pre-commit gate. Use when starting a new Python project, repo, or package from scratch, or when asked to set up Python project structure, linting, type checking, or architectural boundaries for a fresh codebase. Greenfield only.
---

# Scaffold a Python project

Produces a project where the architecture is enforced by tooling rather than by
memory, and where a fresh clone passes every check on the first run.

**Greenfield only.** Retrofitting an existing project means merging config
rather than writing it, and merging `pyproject.toml` tool sections badly is
worse than leaving them alone.

Assets live in `assets/`. Files marked *frozen* are copied byte-for-byte; do not
improvise variants of them.

---

## Step 0 — Guard

Abort if `pyproject.toml`, `src/`, or `setup.py` exists in the target directory.
Say what was found and stop. Do not offer to merge.

An existing `.git` is fine — scaffolding into a freshly-cloned empty repo is
normal.

## Step 1 — Interview

One `AskUserQuestion` call, all questions together. Do not ask them one at a
time across turns.

1. **Package name** — becomes `src/<pkg>/`. Must be a valid identifier:
   lowercase, underscores, no hyphens. The *project* name (PyPI/repo name) may
   differ and may use hyphens.
2. **Python version** — offer the two most recent stable releases. Default to
   the newest.
3. **Layers** — see Step 2. This is the question that matters; give it room.
4. **Git workflow** — solo (default) or team. Selects a `claude-md-rules.md`
   ASK rule.
5. **Rigor stance** — normal (default) or explicitly experimental. Default emits
   nothing; see the rule bank on why this is never inferred.
6. **CI** — add `.github/workflows/checks.yml`? Default yes.

## Step 2 — Layers, the part worth slowing down for

Ask for an **ordered list, top to bottom**, with one line on what lives in each.
The rule to state plainly:

> A layer may import anything below it, never above.

That single sentence is the whole model. Verify the ordering by asking which
layer would be hardest to delete — that one is usually the bottom.

A reasonable starting shape, offered as an example and not a default to accept
silently:

```
app / eval      composes everything, owns entry points
implementation  concrete work, siblings that don't know about each other
interface       contracts and value objects
util            pure helpers, depend on nothing internal
```

**Emit layers only. No `depends_on`.** Tach enforces direction from layer
ordering alone — an upward import fails with no per-module dependency lists
anywhere. Hand-mapping every module against every other is a maintenance tax
that buys nothing here:

```toml
source_roots = ["src"]
forbid_circular_dependencies = true
root_module = "ignore"          # <pkg>/__init__.py is a namespace shell

[[layers]]
name = "implementation"

[[layers]]
name = "interface"

[[layers]]
name = "util"

[[modules]]
path = "<pkg>.util"
layer = "util"
```

Write the *reasoning* above the config as a comment — what each layer is for and
which specific mistake the boundary prevents. That prose is the part a reader
cannot reconstruct from the config, and it is what stops someone from
"temporarily" relaxing a rule two years later.

**One caveat to state, not to act on:** modules in the *same* layer can freely
import each other. Sibling isolation needs explicit `depends_on` on each module.
Mention this only if the user described siblings that must not know about one
another; otherwise it is premature.

## Step 3 — Write

Create, substituting `{{PKG}}` `{{PROJECT}}` `{{PY}}` `{{PY_NODOT}}` (e.g. `3.13`
→ `313`):

| Target | Source | Treatment |
|---|---|---|
| `.gitignore` | `assets/gitignore` | frozen |
| `.pre-commit-config.yaml` | `assets/pre-commit-config.yaml` | frozen |
| `.python-version` | `assets/python-version` | frozen |
| `.vscode/settings.json` | `assets/vscode-settings.json` | frozen |
| `.claude/settings.json` | `assets/claude-settings.json` | frozen |
| `tests/conftest.py` | `assets/conftest.py` | frozen |
| `tests/test_smoke.py` | `assets/test_smoke.py` | substitute |
| `.env.example` | `assets/env.example` | frozen |
| `typings/README.md` | `assets/typings-README.md` | frozen |
| `README.md` | `assets/README.md` | substitute |
| `pyproject.toml` | `assets/pyproject-tools.toml` | generate head, append frozen tail |
| `CLAUDE.md` | `assets/claude-md-rules.md` | assemble from bank |
| `tach.toml` | Step 2 | generate |
| `.github/workflows/checks.yml` | `assets/ci.yml` | frozen, if opted in |
| `.claude/skills/module-contract/` | `../module-contract/` | vendor, see Step 5 |

`pyproject.toml` head — generated, everything below is the frozen tool block:

```toml
[project]
name = "{{PROJECT}}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">={{PY}}"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{{PKG}}"]

[dependency-groups]
dev = ["ruff", "pyright", "pytest", "pytest-cov", "tach", "deptry", "hypothesis", "vulture", "pre-commit"]
```

Then one empty `__init__.py` per layer package, plus `tests/fixtures/.gitkeep`.

## Step 4 — Bootstrap and verify

```bash
git init            # skip if already a repo
uv sync
uv run pre-commit install
uv run pre-commit run --all-files
```

**The last command must pass clean.** A scaffold that arrives failing its own
checks teaches the user to ignore them, which costs more than the scaffold
saves. If a hook fails, fix the scaffold and rerun — never hand over with a
caveat, and never disable the hook that caught it.

`tests/test_smoke.py` exists because `pytest` exits 5 on an empty suite. It is
a placeholder with a docstring saying so — do not "fix" an empty suite by
muffling the exit code instead.

`ruff format --check` covers Python inside Markdown fences, so a code sample in
a `.md` asset has to be formatter-clean like any other code.

`tach check` warns "No first-party imports were found" on a scaffold with no
code yet. It passes; the warning goes away with the first real import. Do not
chase it by editing source roots.

## Step 5 — Vendor `module-contract`

Copy this plugin's `skills/module-contract/` into the new project's
`.claude/skills/module-contract/`, and add to the top of its `SKILL.md`:

```
<!-- Vendored from claude-skills. Edit there, then re-vendor. -->
```

It is copied, not linked. Git stores a symlink as its target path, so a link to
your home directory dangles in every clone and the skill silently disappears.
The copy makes the project self-contained; the header stops you from editing
the wrong one.

Improvements do not flow backward into already-scaffolded projects. That is the
normal cost of a template, and it is cheaper than the alternative.

## Step 6 — Hand off

Show the layer diagram and the bootstrap commands, then point at
`module-contract` for the first module — `contract.md` before any code.

---

## Backporting

This skill is deliberately **not** coupled to any live project. A living
codebase accumulates workarounds and disabled hooks, and coupling would let
every one of them infect the next project with no review step.

So it goes the other way, by hand: when you improve tooling in a scaffolded
project and the change is project-agnostic, edit `assets/` here and commit.
Project-specific fixes stay where they are.

The test for "agnostic" is whether the change would still be right in a project
with none of the current one's dependencies. Ruff rule additions and pre-commit
hook shape usually pass. Anything naming a library usually does not.
