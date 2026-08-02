---
name: module-contract
description: How to write a module's contract.md and retire its build spec. Use when starting a new module or package (write contract.md, then spec.md), and again when that module's implementation is about to be committed or pushed (promote what building taught you, then delete the spec). Also use when asked to prune, retire, or clean up an existing spec or module README.
---

# Module docs: contract.md is permanent, the spec is not

- **`contract.md`** — what the rest of the system may assume of this module, and the rules keeping
  it true. Permanent. Written *before* the spec.
- **`spec.md`** — scaffolding for writing the code. **Deleted when the module lands.** Never
  named `README.md`: that name promises a durable entry point. Only the repo root keeps one.

**Default home for a durable fact is the code it is about** — call-site comment, test, docstring,
`--help`. `contract.md` is the narrow exception; when in doubt it is not a clause.

**One-way citation:** the spec may cite the contract, never the reverse. A contract citing
`spec.md §Foo` breaks when the spec is deleted.

---

## Phase 1 — starting a module

### contract.md, first

It is the spec's acceptance criteria: *a design that satisfies the spec but breaks the contract
is not done.* Worked example: `example-contract.md`, next to this file — read it for calibration,
not as a template; a different module earns a different subset of the kinds below.

**Gate: name the consumer before writing a clause** — the module, file, and function that will
read it. No named consumer, no clause; anything else is speculative plumbing in prose.

**Closed list — seven kinds, nothing else.** Anything unmatched goes to the code, even when true,
durable, and hard-won. Resist growing this list; the closure is what makes the gate work, and a
candidate that cannot name its consumer is speculation however true it sounds:

- **Invariants a caller depends on**, with the reason — "the returned map has one entry per input
  row; a failed row gets a stand-in, never a missing key," because a consumer indexes it by key
  and a scorer would otherwise silently drop the hardest rows.
- **I/O properties types cannot state** — unbounded and long-tailed, results arrive in any order,
  failures contained per item rather than per batch, estimated here but exact in production.
- **The direction of error that hurts** — which way a rule may be wrong, and why the other way is
  worse. "The wrong credential is worse than no credential, because the caller will try it."
- **Known gaps deliberately accepted**, with their cost and an explicit "do not paper over this by
  loosening the rule."
- **Cost and side effects of running it** — bills money, mutates external state, non-deterministic,
  rate-limited, slow. Name the *consequence*, never the mechanism: "requires credentials and bills
  per row; see the settings module," not the variable's name, its default, or how to set it.
  Config names and env policy live with the config code; restating them here is how this rots.
- **Test policy** — what counts as evidence and why weaker evidence does not. "A real sample from
  every source, not one per adapter — adapters are fewer than sources, and the risk is a source
  that looks like its adapter until it doesn't. The negative case counts."
- **Obligations on downstream builders** — a rule the consumer must follow to keep this module's
  guarantee intact, and why. Gate on the structural property, not on a name that encodes it.

**Goes to the code instead:**

- What the code already states — layout, field tables, flag lists, import/layering rules enforced
  by tooling, script walkthroughs. Delete rather than relocate.
- Machine-checkable schema → the type definitions and validators.
- Test *case lists* → the test file, as data. Never prose.
- Why *this line* is what it is, including "don't 'fix' this" → a comment at that line. The most
  common mistake: rationale is durable, which makes it feel contract-shaped, but it belongs to a
  call site, not the boundary.

**Each clause names its enforcing test, or admits it has none** (review-only is legitimate).
**Cap ~150 lines.** Numbers with a shelf life get a date or a script that regenerates them.

Encode test policy so violating it fails the build. Parametrize over the **closed set of cases**,
not over the fixture collection — iterating fixtures can never detect a missing one:

```python
@pytest.mark.parametrize("case", list(Case))  # every case, always
def test_derivation(case):
    sample = FIXTURES[case]  # KeyError = the gap
```

Thresholds are code; why the threshold is what it is stays prose.

### Then spec.md, marked doomed

```markdown
# <module> — build spec (DELETED AT MERGE)

**Blocked by:** <what must land first>    ← omit the line entirely when nothing blocks it

Scaffolding only. Not a source of truth, never cited from code or contract.md.
Any claim that should outlive the implementation belongs in contract.md now, not here.
```

It carries layout, build order, draft algorithms, what to do first. A "why" paragraph appearing
here is in the wrong file — move it immediately.

Write the spec while the idea is hot even when the work is blocked — that is the cheapest moment
to capture it. Name the blocker so the next reader does not rediscover it. Nothing to maintain:
the line is a fact at authoring time, not a status to flip, and the spec is deleted at merge.

---

## Phase 2 — at merge / commit / push

Deletion is unconditional, so there is no per-section judgment. What remains is capturing what
could not be written in advance.

1. **What did building this teach you that is unwritten?** → `contract.md`. The step that cannot
   be front-loaded: failure modes found by running it, a fallback that mattered more than
   expected, a missed ordering constraint. Expect little here if the code is already well
   commented — then step 2 is where the value is.
2. **Any "don't fix this" still only in your head?** → comment at the call site, with its revisit
   condition. Typically a rejected alternative and the condition that would justify revisiting it.
   *Tiebreaker vs. the contract: could the reader plausibly never open this file?*
3. **Usage** — invocations, flags, cost levers → `--help` and the root README's command index.
4. **Fix references** — grep for the spec's filename; package docstrings and entry-point scripts
   commonly cite it.
5. **Delete the spec** (`git rm`), in the same commit as the implementation.

Then re-read `contract.md` whole: still self-contained, under the cap, citing nothing deleted.
