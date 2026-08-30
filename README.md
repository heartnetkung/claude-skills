# claude-skills

Personal Claude Code skills, packaged as one plugin.

| Skill | What it does |
|---|---|
| `python-scaffold` | Scaffolds a greenfield Python project — uv, `src/` layout, ruff, pyright strict, tach layers, deptry, vulture, 8-hook pre-commit gate |
| `module-design` | Designs a module before coding it — `contract.md` (permanent) vs `spec.md`/`boundary.md` (deleted when the module lands), then two parallel review agents |
| `slow-pytest-maintenance` | Files a GitHub issue when a pytest suite crosses 15s, then returns to the interrupted task — it never optimizes the tests |

## Install

```bash
claude
> /plugin marketplace add ~/Documents/claude-skills
> /plugin install claude-skills@claude-skills
```

Edits here are live — no re-vendoring needed for the skills themselves.

## Layout

```
.claude-plugin/
  marketplace.json      this repo as a marketplace
  plugin.json           this repo as a plugin
skills/
  python-scaffold/
    SKILL.md            the procedure
    assets/             files copied into scaffolded projects
  module-design/
    SKILL.md            entry point; routes to one phase file, never both
    design.md           phase 1 — contract, spec, boundary, the two reviewers
    merge.md            phase 2 — six steps, ending in deleting the build docs
    removal.md          cutting an over-length contract back under the cap
    reviewer-common.md  rules both review agents read first
    reviewer-simplification.md  reviewer 1's rubric
    reviewer-design.md  reviewer 2's rubric
    example-contract.md worked example, read for calibration; a frozen snapshot
                        of one real project's contract, deliberately not generic
    design-philosophy.md  reference file, not a skill; only the design reviewer
                          agent is handed this path
    LICENSE-design-philosophy  upstream MIT text, travels with the copy
  slow-pytest-maintenance/
    SKILL.md            the threshold and the stop rule
    file-issue.sh       the one issue it files, with client-side dedupe
```

`module-design` and `slow-pytest-maintenance` are copied into projects that want them
without a plugin install. **Both copies are sources of truth** — edit whichever you are
sitting in and mirror the change to the other. Neither carries a "vendored from" banner,
because there is no one direction to point it.

`slow-pytest-maintenance` assumes pytest, `uv`, `gh`, and a `maintenance` label in the
repo; it hardcodes 15s. A project that wants a different threshold edits its own copy.

## Assets: frozen vs. generated

`python-scaffold/assets/` splits by how much of each file is project-specific.
Getting this wrong in either direction is the main failure mode — freeze too
much and every project inherits another project's accidents; generate too much
and there is no guarantee a fresh scaffold passes its own checks.

| Asset | Treatment | Why |
|---|---|---|
| `gitignore`, `python-version`, `vscode-settings.json`, `conftest.py`, `env.example`, `claude-settings.json`, `pre-commit-config.yaml`, `ci.yml` | frozen | no project-specific content at all |
| `pyproject-tools.toml` | frozen | the `[tool.*]` half of pyproject transfers intact; `[project]` does not and is generated |
| `claude-md-rules.md` | rule bank | some rules can't be universally true — see the file |
| `tach.toml` | generated | layer names are the whole content, and they're per-project |

## Backporting

Nothing here reads from a live project. Improvements move by hand: change a
scaffolded project, decide whether the change is project-agnostic, and if so
edit `assets/` here.

The test is whether the change would still be right in a project sharing none
of the current one's dependencies.
