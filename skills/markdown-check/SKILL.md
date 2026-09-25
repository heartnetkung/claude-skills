---
name: markdown-check
description: Edit a markdown document for coherence, concision, unambiguous technical terms, and live references — auto-fixing what is certain and asking about what is not. Use when asked to check, review, tighten, or clean up a .md file (a contract, spec, README, design doc, or notes).
---

# Checking a markdown document

The document is the deliverable, not a summary of it. You are editing the file in place, then
reporting what you changed and asking about what you could not decide alone.

Take the target from the invocation argument. If none was given, list the markdown files changed
in the working tree (`git status --porcelain -- '*.md'`) and ask which one — do not pick for the
user.

**Read the whole file before changing a line of it.** Every check below is about the file as a
whole; a pass done paragraph by paragraph finds none of them.

## The checks

Go through all five in one reading pass. They overlap — the same sentence is often both padding
and a hedge — so decide the fix once.

**1. Coherence.** Two passages that cannot both be true. A term introduced under one name and
continued under another. A section that promises something the rest never delivers, or delivers
something the framing never promised. An ordering where a paragraph depends on one further down.
Fix by making the two agree; if you cannot tell which side is right, ask.

**2. Concision.** Cut a sentence that restates its heading, a paragraph that restates the one
above it, a preamble that announces what the section will say, a second example that carries the
same case as the first, and any word doing no work in its sentence. Cutting is the only fix — a
concision pass that ends with more words than it started has failed.

**3. Ambiguous technical words.** A term with more than one referent in this document's domain,
used where the reader cannot pin it down: "the config", "the client", "run", "handler", "state".
If the document itself settles it elsewhere, fix it by naming the thing. If it does not, that
ambiguity may be hiding an unmade decision — flag it, do not guess.

**4. Justification written for technical correctness.** Prose that exists so no reader can call
the sentence wrong, rather than to tell them something: hedges around a case nobody hits,
parenthetical corrections to the claim just made, "note that this is not strictly...", "for
completeness", defensive restatement of scope. Delete it. A caveat survives only when a reader
acting on the sentence without it would do the wrong thing.

**5. Stale references.** Check every one against the tree — `ls` the paths, grep the symbols and
function names, open the linked files, run the commands named as runnable. Dead link, moved file,
renamed symbol, flag that no longer exists, a step describing a workflow that changed. Fix a
reference whose target you can locate; flag one you cannot. Two are stale by construction and go
without checking: a citation by section number (§4, "step 3 above" — numbering shifts silently),
which is replaced by naming the thing, and a measured figure nothing regenerates.

## Fixing

Fix what you are sure of, directly in the file. "Sure" means the document or the tree settles it —
not that you have a good guess.

- Never add a fact the document did not already carry.
- Keep the author's voice and vocabulary. You are cutting and correcting, not rewriting.
- Leave structure alone unless a check names it. Reordering a document nobody asked you to
  reorganize destroys the diff that makes your work reviewable.

## Asking

Everything you were unsure of comes back as plain text at the end of your reply. **Do not use
AskUserQuestion or any other tool for this.** Number the items, and for each one give:

- the item's number and, on the same line, the line number and the exact text, quoted;
- one sentence on what is wrong with it;
- two or three options lettered `A`, `B`, `C`, concrete enough to pick without reading the file
  again, with the last one always leaving the text as it is.

**Group the items by check**, under the check's name, in the order the checks are listed above —
the same grouping the report uses, so the two read against each other. Numbering runs straight
through the groups rather than restarting in each, and every option is lettered, so the user can
answer in one line: `1A, 2C, 3B`. Close with that instruction.

```
**Coherence**

1. line 12 — "the run directory is written under $TMPDIR"
   Line 88 of the same file says it is fixed under ~/runs.
   A) make line 12 agree with line 88
   B) make line 88 agree with line 12
   C) leave as is

**Ambiguous technical words**

2. line 47 — "the handler retries until the client gives up"
   Two clients in this file: the HTTP client and the sync client.
   A) name it the HTTP client
   B) name it the sync client
   C) leave as is

Reply with the picks, e.g. 1A 2C.
```

Ask about substance, not about permission to make an edit you were sure of.

## Reporting

Before the questions, list what you changed — one line per fix, grouped by check, naming the line
and what went. No line counts, no word counts, no summary of how much better the document is now.
If a check found nothing, say so in three words; do not manufacture a finding to fill it.
