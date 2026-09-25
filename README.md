# claude-skills

Personal Claude Code skills. Projects symlink the ones they want.

| Skill | What it does |
|---|---|
| `python-scaffold` | Scaffolds a greenfield Python project — uv, `src/` layout, ruff, pyright strict, tach layers, deptry, vulture, 8-hook pre-commit gate |
| `module-design` | Designs a module before coding it — `contract.md` (permanent) vs `spec.md`/`boundary.md` (deleted when the module lands), then two parallel review agents |
| `slow-pytest-maintenance` | Files a GitHub issue when a pytest suite crosses 15s, then returns to the interrupted task — it never optimizes the tests |
| `markdown-check` | Edits a markdown file in place for coherence, concision, ambiguous terms, and stale references; asks about what it cannot settle |
| `slides` | Builds PowerPoint decks from Markdown with pandoc and reloads LibreOffice on every change — outline → first draft, two parallel reviewers (editor, flow), SVG diagrams |

## Install

Symlink each skill a project wants into its `.claude/skills/`. Claude Code puts every
visible skill's description into context and can trigger it, so link only the skills
that apply. The commands below assume the project and `claude-skills` sit side by side:

```bash
mkdir -p .claude/skills
ln -s ../../../claude-skills/skills/module-design           .claude/skills/module-design
ln -s ../../../claude-skills/skills/slow-pytest-maintenance .claude/skills/slow-pytest-maintenance
ln -s ../../../claude-skills/skills/markdown-check          .claude/skills/markdown-check
```

`python-scaffold` runs before a project exists, and `slides` is used wherever a deck happens to
live, so link both at user level instead:

```bash
mkdir -p ~/.claude/skills
ln -s ~/Documents/claude-skills/skills/python-scaffold ~/.claude/skills/python-scaffold
ln -s ~/Documents/claude-skills/skills/slides          ~/.claude/skills/slides
```

Run `/skills` in the project to confirm the links are picked up. A committed link is
broken for anyone who clones the project without `claude-skills` beside it. Gitignore
`.claude/skills/` if that matters.

Edits here are live: they reach every linked project immediately.

## Layout

```
skills/
  python-scaffold/
    SKILL.md            the procedure
    assets/             files copied into scaffolded projects
  module-design/
    SKILL.md            entry point; routes to one phase file, never both
    design.md           phase 1 — contract, spec, boundary, the two reviewers
    merge.md            phase 2 — seven steps, ending in deleting the build docs
    removal.md          the pass run on every contract edit; whole file past ~180 lines
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
  markdown-check/
    SKILL.md            the five checks, what to fix vs. ask, the report format
  slides/
    SKILL.md            entry point: the build → check → reload loop; routes to one phase file
    outline.md          phase — outline, approval, first full draft, then delete the outline
    review.md           phase — two reviewers in parallel, fix what's certain, ask the rest
    visuals.md          phase — pick slides, draw SVG, render, look, place
    reviewer-common.md  rules both review agents read first
    reviewer-editor.md  reviewer 1's rubric: wording, audience, deck rules, layout, images
    reviewer-flow.md    reviewer 2's rubric: story, coherence, concision, stale refs, visuals
    svg-style.md        canvas sizes, text sizes, palette for diagrams
    scripts/            build.sh (lint + pandoc), check.py (overflow + PNGs),
                        reload.py (LibreOffice over a pipe), render.sh (SVG → PNG)
    assets/             frozen: reference.pptx and starters copied into a new deck folder
```

`slides` needs `pandoc`, LibreOffice with Python UNO, poppler-utils, and Chrome or Chromium for
diagrams. The per-deck rules (audience, banned words, numbering) live in each deck folder's
`CLAUDE.md`, not in the skill.

This repo is the only copy of each skill. Projects link to it and don't vendor it, so there is
nothing to keep in sync.

`slow-pytest-maintenance` assumes pytest, `uv`, `gh`, and a `maintenance` label in the
repo; it hardcodes 15s. A symlinked copy is shared, so a project that needs a different
threshold copies the skill in rather than linking it, and that copy is then its own.

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
