#!/usr/bin/env python3
"""Check a Markdown deck's structure before pandoc builds it.

Errors (exit 1): a `#` heading, two title slides in a row, a deck ending on a
section title, an image path that doesn't exist.
Warnings: more than 6 top-level bullets on a slide, more than 7 table body rows.
"""
import os
import re
import sys

MAX_BULLETS = 6
MAX_TABLE_ROWS = 7


def slides(lines):
    """Yield (kind, title, line_no, body_lines); kind is 'title', 'section' or 'content'."""
    i = 0
    if lines and lines[0].strip() == "---":
        end = next((j for j in range(1, len(lines)) if lines[j].strip() in ("---", "...")), 0)
        if any(re.match(r"title:\s*\S", l) for l in lines[1:end]):
            yield "title", "(title slide)", 1, []
        i = end + 1
    current = None
    in_fence = in_comment = in_notes = False
    for n in range(i, len(lines)):
        line = lines[n]
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
        if in_comment or (s.startswith("<!--") and "-->" not in s):
            in_comment = "-->" not in s
            continue
        if not in_fence and re.match(r"^:{3,}\s*notes", s):
            in_notes = True
            continue
        if in_notes and re.match(r"^:{3,}\s*$", s):
            in_notes = False
            continue
        if in_fence or in_notes:
            if current:
                current[3].append("")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if current:
                yield tuple(current)
            level = len(m.group(1))
            kind = {1: "h1", 2: "section"}.get(level, "content")
            current = [kind, m.group(2).strip(), n + 1, []]
        elif current:
            current[3].append(line)
    if current:
        yield tuple(current)


def main(path):
    deck_dir = os.path.dirname(os.path.abspath(path))
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    errors, warnings = [], []
    items = list(slides(lines))
    prev = None
    for kind, title, line_no, body in items:
        where = f"line {line_no} \"{title}\""
        if kind == "h1":
            errors.append(f"{where}: `#` heading; use `##` for a section, `###` for a slide")
        if kind in ("title", "section") and prev in ("title", "section"):
            errors.append(f"{where}: two title slides in a row; add a content slide before it")
        prev = kind
        text = "\n".join(body)
        bullets = sum(1 for l in body if re.match(r"^([-*+]|\d+\.)\s", l))
        if bullets > MAX_BULLETS and "{.columns}" not in text:
            warnings.append(f"{where}: {bullets} top-level bullets (max {MAX_BULLETS})")
        rows = [l for l in body if l.lstrip().startswith("|")]
        if len(rows) > MAX_TABLE_ROWS + 2:
            warnings.append(f"{where}: {len(rows) - 2} table rows (max {MAX_TABLE_ROWS})")
        for img in re.findall(r"!\[[^\]]*\]\(([^)\s]+)", text):
            if not re.match(r"https?://", img) and not os.path.exists(os.path.join(deck_dir, img)):
                errors.append(f"{where}: image not found: {img}")
    if prev == "section":
        errors.append(f"deck ends on section title \"{items[-1][1]}\"; add a content slide after it")
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: lint_deck.py DECK.md")
    sys.exit(main(sys.argv[1]))
