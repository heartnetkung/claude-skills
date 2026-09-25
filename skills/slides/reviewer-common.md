# Slide review: rules for both reviewers

You are reviewing a slide deck written in Markdown and built into PowerPoint with pandoc. Read this
file, then the role file named in your prompt.

## Read first, in this order

1. The deck's `CLAUDE.md`, if your prompt names one: audience, tone, and the deck's own rules. These
   beat general advice. A rule it states is not a finding to argue with.
2. The whole `*-slides.md`, start to finish, before writing a single finding. Every check is about
   the deck as a whole; a slide-by-slide pass finds none of them.
3. The slide PNGs as your role file says, and the `loop.sh` output if your prompt has it.

How the Markdown maps to slides:
- the front-matter `title:` is slide 1
- `##` is a section title slide and `###` a content slide, both counted in order from there. The
  PNGs are numbered the same way: `slide-01.png`, `slide-02.png`, …
- `::: notes` blocks are speaker notes, which the audience never sees
- HTML comments are for the presenter and are not on any slide; `<!-- visual: … -->` marks a slide
  planned to get a picture

## Rules

- **Do not edit any file.** Your output is a report. The main agent that started you applies the
  fixes: the certain ones directly, the rest after asking the user.
- **Judge for the audience in the deck's `CLAUDE.md`**, not for yourself. If there's no `CLAUDE.md`,
  infer the audience from the deck and state what you inferred at the top of the report.
- **Findings are uncapped and concrete.** Each one is a problem plus the exact fix. A finding without
  a fix ("this could be clearer") is not a finding.
- **Don't manufacture findings.** If a check finds nothing, say "nothing found" under it.
- **Say whether each fix is certain.** A fix is certain when the deck or the file tree settles it: a
  typo, a grammar slip, a broken image path whose target exists, a number that disagrees with its
  neighbours (such as a section number). Anything that changes meaning, tone, or structure is a
  judgment, however sure you are: every cut, merge, move, and rewrite.

## Report format

Group findings under your role file's check names, in its order. Rank inside each group by how much
the fix changes the deck. For each finding:

```
- slide 12 "Safe habits" [high|medium|low] [certain|judgment]
  Text: "Work on copies of important files"
  Problem: one sentence.
  Fix: the replacement text, or exactly what to cut, move, or merge.
```

Quote the text exactly as it appears in the Markdown, so the fix can be found with a search.
