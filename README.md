# claude-skills

Claude Code skills, installable one at a time as plugins.

| Skill | What it does |
|---|---|
| [`python-scaffold`](#python-scaffold) | Scaffolds a greenfield Python project — uv, `src/` layout, ruff, pyright strict, tach layers, deptry, vulture, 8-hook pre-commit gate |
| [`module-design`](#module-design) | Designs a module before coding it — `contract.md` (permanent) vs `spec.md`/`boundary.md` (deleted when the module lands), then two parallel review agents |
| [`slow-pytest-maintenance`](#slow-pytest-maintenance) | Files a GitHub issue when a pytest suite crosses 15s, then returns to the interrupted task — it never optimizes the tests |
| [`markdown-check`](#markdown-check) | Edits a markdown file in place for coherence, concision, ambiguous terms, and stale references; asks about what it cannot settle |
| [`slides`](#slides) | Builds PowerPoint decks from Markdown with pandoc and reloads LibreOffice on every change — outline → first draft, two parallel reviewers (editor, flow), SVG diagrams, photo scouts with license-tagged picks |
| [`vibe-prototype`](#vibe-prototype) | Builds a throwaway, locally-running UI prototype on realistic dummy data to decide what to build, then hands it off as a spec with screenshots |

## Install

### Option 1: plugin (one-time install)

```bash
claude plugin marketplace add heartnetkung/claude-skills
claude plugin install slides@heartnetkung-skills
```

### Option 2: clone and symlink (development, easy updates)

```bash
git clone https://github.com/heartnetkung/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/skills/slides ~/.claude/skills/slides
```

## Benefits and tradeoffs

Each skill encodes a workflow I run, with proven usage and lessons learned. Some of them have
preconditions that assume a particular work style or context. Some problems are solved in an
opinionated way, and every rule carries the reasoning behind it.

### python-scaffold
- **Precondition:** new repos only.
- **Benefit:** exhaustive verification for an agentic repo, with proven tools.
- **Tradeoff:** highly opinionated.

### module-design
- **Precondition:** tough modules; spec-driven development.
- **Benefit:** better design, maintainability and simplicity, including simpler requirements.
- **Tradeoff:** more process, so slower; opinionated; some Markdown docs persist in the code.

### slow-pytest-maintenance
- **Precondition:** pytest.
- **Benefit:** flags a pytest suite that passes 15s, without derailing the current task.
- **Tradeoff:** more backlog to handle.

### markdown-check
- **Benefit:** improves the coherence, concision and correctness of any Markdown.
- **Tradeoff:** none.

### slides
- **Precondition:** LibreOffice.
- **Benefit:** faster iteration: write in Markdown, convert to .pptx deterministically;
  diagrams drawn and photos found automatically.
- **Tradeoff:** limited positioning control (pandoc); styling needs fixing afterwards.

### vibe-prototype
- **Precondition:** new requirements only.
- **Benefit:** speeds up iteration on complex UI requirements; the spec includes e2e tests
  and verification.
- **Tradeoff:** none.

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
    outline.md          phase — interview (2 rounds), outline, approval, first full draft, delete the outline
    review.md           phase — two reviewers in parallel, fix what's certain, ask the rest
    visuals.md          phase — diagrams (draw SVG, render, look) and photos (scouts, top 5, place #1)
    visual-rules.md     when a slide gets a diagram or a photo; read by visuals, the flow reviewer, outline
    image-scout.md      the photo scout agent's rubric: search, drop blurred/incomplete, rank
    reviewer-common.md  rules both review agents read first
    reviewer-editor.md  reviewer 1's rubric: wording, audience, deck rules, layout, images
    reviewer-flow.md    reviewer 2's rubric: story, coherence, concision, stale refs, visuals
    svg-style.md        canvas sizes, text sizes, palette for diagrams
    scripts/            loop.sh (build → check → reload in one call), build.sh (lint + pandoc),
                        check.py (overflow + PNGs), reload.py (LibreOffice over a pipe),
                        render.sh (SVG → PNG), find_image.py (Commons + Openverse search,
                        cv/ci tags, blur filter)
    assets/             frozen: reference.pptx and starters copied into a new deck folder
  vibe-prototype/
    SKILL.md            the loop: clarify context → scaffold → state panel → build/screenshot/look → wording → handoff
    scripts/shot.sh     headless-Chrome screenshot of one prototype state
```

`slides` needs `pandoc`, LibreOffice with Python UNO, poppler-utils, the Carlito font (for
`reference.pptx`'s Calibri), Chrome or Chromium for diagrams, and numpy and Pillow for
`find_image.py`. `find_image.py` sends this repo's URL as its User-Agent, because Wikimedia
refuses requests without contact details. The per-deck rules (audience, banned words, numbering)
live in each deck folder's `CLAUDE.md`, not in the skill.

`vibe-prototype` needs Node/npm and Chrome or Chromium (for `shot.sh`).

`slow-pytest-maintenance` assumes pytest, `uv`, and `gh` with a GitHub remote; it creates its
`maintenance` label on first use and hardcodes 15s. For a different threshold, copy the skill into the project's
`.claude/skills/` and edit it there.

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
