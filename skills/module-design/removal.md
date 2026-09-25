# Cutting a contract back

A contract is read by someone deciding whether their change is safe, and one they stop reading
stops binding anything. Two things bring you here. They are the same seven questions over
different amounts of the file.

**Every edit to a `contract.md`, always — over the clauses the diff touches.** Added, reworded or
moved: run the questions on those and no others. It is a few greps per clause, and it is the only
pass most clauses will ever get. A contract is born under this skill and then edited for months by
changes that never load it; every one appends, none re-reads the whole, and nothing else asks
whether a clause still earns its place.

**Prose over ~180 lines — the whole file.** Count the clauses only; `Tests:` and `Sites:` lines do
not count. At that size the page has grown past one sitting, and question 3 is why this pass has to
cover all of it: a clause can only be caught repeating another by reading both.

**The warning goes next to the dangerous site. Always.** That is the one principle under every
check below, and it decides direction rather than count: a fact belongs wherever someone could
break it, even if that means writing it in two places. Two contracts carrying the same cross-module
rule are both correct — each binds a reader who would never open the other. What goes is the copy
sitting where nothing dangerous happens.

**That is a test each copy passes on its own, and not a licence for a third.** A module that could
break the rule states it. A module that merely *obeys* it names it in a line and stops — "this is
`x`'s word, and this module does not get a second one" is the whole of the second copy. Judge every
clause by whether a reader of *this* file could break the rule; one that needs the other file's
argument to justify its length is arguing rather than binding.

Go clause by clause and ask these in order, stopping at the first yes.

**1. Does the code already say it?** Read the clause's `Sites:` line, grep those symbols along with
any others the clause names, and read what you find. The
default home for a durable fact is the code it is about, so a fact already there is deleted, not
relocated — you are removing the second copy.

**2. Do the code and the contract cite each other?** The most expensive duplication is
bidirectional and reads as courtesy from both ends: a docstring cites `contract.md` for the
invariant while the contract restates that function's mechanism. Split it by danger — the
mechanism can only be broken in the code, the caller's assumption only outside it — and cut each
side to a pointer at the other.

**3. Does another clause in this same file already say it?** The one duplication with no defence:
both copies bind the same reader, so the second is noise the first has to be read past. Across
files is different and often right — this is only about repetition within the page.

**4. Is it a reported number?** Delete it. A measured figure is not a clause, and relocating it is
not the fix — a contract states what holds. Neither a date beside it nor a script named beside it
saves it: a figure kept by hand is a claim nothing keeps honest, and it decays silently because
nothing fails when it goes stale. A cited external constant is exempt — a vendor's cap, a retention
window, a protocol limit. You do not maintain those, they are the rule itself, and they are the one
kind a reader could not have found by reading the code. What goes is the figure your own run
produced.

**5. Has the clause's named consumer landed?** A clause addressed to a future builder is correct
when written and becomes duplication the moment that builder writes its own contract. Nothing else
catches this, because at authoring time it passed every gate.

**6. Is it a rejected alternative, or a "don't fix this"?** Rationale for why *this line* is what
it is goes in a comment at that line. It feels contract-shaped because it is permanent, but the
test is whether a reader who never opens that file needs it.

**7. Does the citation still resolve?** Headings get reworded, files deleted, symbols renamed. A
citation by section number is always wrong — numbers renumber silently. Name the thing instead. The
`Sites:` line rots the same way and is checked the same way; a site that no longer resolves is
either a renamed symbol to fix or a consumer that left, and the second one is question 5.

## Then compress what survived

Two paragraphs is already a lot for one clause. A section past that is nearly always argument
rather than rule: the case for the clause, the alternatives weighed, the history that produced it.
Keep the rule and the direction of error it guards; cut the case that was made for it.

## What to do with what you cut

**Move rather than drop**, except for numbers. Confirm the fact sits at its dangerous site before
deleting it here; if it has no such site in code, it stays however long the file is. A fact with
no call site to hold it is what a contract is for.

**Sweep for danglers.** Deleting a clause orphans whatever pointed at it — grep the package for
`contract.md` and for the heading you removed. Code that deferred to a section you deleted needs
that reasoning inlined where it deferred.

**Do not report a line count as the outcome.** The outcome is which facts moved and which were
written twice. A contract that reaches 180 by cutting a clause with nowhere else to live is worse
than one that stays at 200.
