---
name: slides
description: Build PowerPoint decks from a Markdown source with pandoc, reloading LibreOffice Impress after every change. Use when asked to make a presentation, slide deck, or .pptx; when editing a *-slides.md deck; when asked to review a deck (`/slides review`); or when asked to add diagrams or visuals to slides (`/slides visuals`).
---

# Slides: Markdown in, PowerPoint out

The Markdown file is the deck. The `.pptx` is built from it and never edited by hand. Every change
is: edit the `.md` → build → check → reload LibreOffice.

**Resolve the skill directory first.** It is the base directory Claude Code printed when this skill
loaded (a symlink path is fine). Every path below written `<skill-dir>/…` means that directory, made
absolute. The deck folder is where the deck's `*-slides.md` lives; pass it absolute too.

## Route to one phase file

Read the argument and open **one** of these, next to this file:

| Request | File |
|---|---|
| A new deck, or no `*-slides.md` exists yet | `outline.md`, which drafts the first full deck from an approved outline |
| `review`, or "review / check / critique the slides" | `review.md` |
| `visuals`, or "add diagrams / images / visuals" | `visuals.md` |
| Anything else: an edit, a rebuild, a fix | nothing more; the loop below is the whole job |

## Files in a deck folder

| File | Lifetime |
|---|---|
| `NAME-slides.md` | the deck, permanent |
| `NAME.pptx` | built output, rebuilt every change |
| `NAME-outline.md` | short-lived: exists from the outline until the first draft is complete |
| `CLAUDE.md` | the deck's own rules: audience, tone, numbering, banned words |
| `reference.pptx` | frozen copy of `<skill-dir>/assets/reference.pptx`, so the deck builds even if the skill changes |
| `template.pptx` | optional: a company or Google Slides template; wins over `reference.pptx` |
| `images/` | `*.svg` sources and their rendered `*.png` |

**Read the deck folder's `CLAUDE.md` before editing a deck.** Its rules beat the general ones below.

## The loop, after every edit

```bash
<skill-dir>/scripts/build.sh DECK_DIR/NAME-slides.md          # lint + pandoc → NAME.pptx
/usr/bin/python3 <skill-dir>/scripts/check.py DECK_DIR/NAME.pptx   # overflow report
/usr/bin/python3 <skill-dir>/scripts/reload.py DECK_DIR/NAME.pptx  # show it in LibreOffice
```

- **Lint errors stop the build.** Fix the Markdown, don't work around the linter.
- **Check `error:` means content runs off the slide; `warning:` means text runs past its box**, which
  in practice is text touching the bottom edge. Fix both: cut words, split the slide, or move detail
  to speaker notes. To see a slide, add `--png DIR` (a scratch directory) and read `DIR/slide-NN.png`.
- **Always run `reload.py` last**, even if you think nothing visible changed.
- Use `/usr/bin/python3` for `check.py` and `reload.py`: the `uno` module comes from the system
  LibreOffice package.

### LibreOffice safety

`reload.py` talks to LibreOffice through a local pipe (`claude_slide`). It starts LibreOffice if
nothing is listening, and otherwise closes and reopens only this deck's window.

- **Never open the deck with `xdg-open`**: that LibreOffice has no pipe, so later reloads can't reach it.
- **If LibreOffice is running without the pipe** (`pgrep -a soffice` shows no `--accept`), don't
  kill it; the user may have unsaved work. Ask them to close it, then run `reload.py`.
- `check.py` runs its own headless LibreOffice with a throwaway profile, so it's safe at any time.

## Markdown structure

- `##` makes a section title slide, `###` a content slide. Never `#`.
- **Never two title slides in a row.** The front-matter title slide and every `##` must be followed
  by a `###`. The linter enforces this.
- `::: notes` … `:::` is speaker notes, not shown on the slide.
- An HTML comment (`<!-- … -->`) isn't converted. The one at the top of the deck is for the
  presenter: how to convert, open questions.
- Side by side: `:::::: {.columns}` holding two `::: {.column}` blocks.
- Images live in `images/`. Credit every image from outside the project in that slide's notes
  (source and license).

## Writing limits

- About 6 bullets per slide, tables of 7 rows or fewer. The linter warns past both.
- A slide says one thing. Detail the presenter needs goes in the notes, not on the slide.
- When a slide explains a process, comparison, cycle, or timeline, it probably wants a visual
  (`visuals.md`).

## Requirements

- `pandoc` on the `PATH`. If missing, install without sudo from the static release:
  `curl -L https://github.com/jgm/pandoc/releases/download/<v>/pandoc-<v>-linux-amd64.tar.gz | tar xz --strip-components 2 -C ~/.local/bin pandoc-<v>/bin/pandoc`
- LibreOffice Impress with Python UNO (`/usr/bin/python3 -c "import uno"`), and `pdftocairo` (poppler-utils) for `--png`.
- For `visuals.md`: Google Chrome or Chromium (falls back to LibreOffice, which renders fonts worse).
