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

**Two `AskUserQuestion` calls, four questions then three.** `AskUserQuestion`
takes at most four per call, so seven cannot go out at once. Two calls, not
seven turns: a scaffold interview that dribbles one question per turn is what
this is guarding against.

The split is not arbitrary — CI is in the first call because the last question
of the second reads its answer.

First call:

1. **Package name** — becomes `src/<pkg>/`. Must be a valid identifier:
   lowercase, underscores, no hyphens. The *project* name (PyPI/repo name) may
   differ and may use hyphens.
2. **Python version** — offer the two most recent stable releases. Default to
   the newest.
3. **Layers** — see Step 2. This is the question that matters; give it room.
4. **CI** — add `.github/workflows/checks.yml`? Default yes.

Second call:

5. **Git workflow** — solo (default) or team. Selects a `claude-md-rules.md`
   ASK rule.
6. **Rigor stance** — normal (default) or explicitly experimental. Default emits
   nothing; see the rule bank on why this is never inferred.
7. **Skills** — which shared skills to enable in this project? Multi-select
   (`multiSelect: true`), one option per skill:
   - `module-design` — default yes. The `CLAUDE.md` module rules route to it.
   - `slow-pytest-maintenance` — default yes when CI was accepted above. It files
     a GitHub issue when the suite crosses 15s, so it needs a GitHub remote;
     without one `gh issue create` fails and the skill is decoration.
   - `markdown-check` — default no.

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
| `.claude/skills/<skill>/` or `.claude/settings.json` | each skill selected | symlink or project plugin; see Step 5 |

`claude-settings.json` keeps `uv.lock` out of context with a `PreToolUse` hook on
`Read`, not a `permissions.deny` rule. `module-design`'s reviewer rules ask for the
same thing in prose; the hook is the half an agent cannot forget. It is config and
not a comment, so the reason lives here.

A deny rule is the wrong instrument: `Read(./uv.lock)` matches on the file, not the
tool, so it also stops any `grep -rn ... .` that would walk past the lockfile — and
because a deny is absolute, that grep prompts even under bypass permissions. The
hook sees the tool name instead: reading the lockfile whole is blocked, grepping it
costs only the matching lines and stays free. It tests `file_path` against the raw
hook JSON with `grep`, so it needs no `jq` on the machine.

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

## Step 5 — Enable the shared skills

How depends on where this skill itself was loaded from: the "Base directory for
this skill" that Claude Code printed when it loaded. **If there is no such line,
stop and ask the user where `claude-skills` is.** Never guess a path.

**Installed as a plugin** (the base directory contains `/plugins/cache/`):
enable each skill selected in question 7 as a project-scope plugin. This writes
`extraKnownMarketplaces` and `enabledPlugins` into `.claude/settings.json` and
keeps the frozen hook and permissions already there:

```bash
claude plugin marketplace add heartnetkung/claude-skills --scope project
claude plugin install module-design@heartnetkung-skills --scope project
```

Repeat the `install` line for each other selected skill. Never symlink into the
plugin cache: its folder is named after a commit, and an update replaces it.
Because the settings file is committed, a teammate who opens the project is
offered the same plugins; nothing depends on their disk layout.

**A `claude-skills` clone** (any other base directory): symlink each selected
skill into `.claude/skills/`. The links are relative, so they survive moving or
renaming the parent directory together with `claude-skills`:

```bash
SKILLS=$(dirname "$(readlink -f "<skill-dir>")")
mkdir -p .claude/skills
ln -s "$(realpath --relative-to=.claude/skills "$SKILLS/module-design")" .claude/skills/module-design
```

Repeat the `ln -s` line for each other selected skill. `readlink -f` resolves the
base directory to the real `claude-skills/skills/` directory, even when it was
loaded through a symlink.

Link, don't copy. `claude-skills` is the only copy of each skill, so a fix there
reaches every project, and there is nothing to keep in sync.

The cost: a committed link is broken in any clone that lacks `claude-skills` at
the same relative path, and the skill silently disappears there. Say so in the
hand-off if the interview chose the team git workflow.

## Step 6 — Hand off

Show the layer diagram and the bootstrap commands, then point at
`module-design` for the first module — it runs the whole design sequence before any code.

If `slow-pytest-maintenance` was enabled, say that it files nothing until the
repo has a GitHub remote. It creates its own `maintenance` label on first use.

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
