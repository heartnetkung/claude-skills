# Phase 1 — starting a module

## contract.md, first

It is the spec's acceptance criteria: *a design that satisfies the spec but breaks the contract
is not done.* Worked example: `example-contract.md`, next to this file — read it for calibration,
not as a template; a different module earns a different subset of the kinds below.

**Gate: name the consumer before writing a clause** — the module, file, and function that will
read it. No named consumer, no clause; anything else is speculative plumbing in prose. The answer
is not discarded once the gate passes: it is the clause's `Sites:` line below, which is what lets a
later reader check the consumer is still there.

**Closed list — seven kinds, nothing else.** Anything unmatched goes to the code, even when true,
durable, and hard-won. Resist growing this list; the closure is what makes the gate work, and a
candidate that cannot name its consumer is speculation however true it sounds. Note what is *not*
on it: why an alternative was rejected, and how the module came to be the way it is. Both are
durable, which is what makes them feel contract-shaped; neither is a rule, and a contract that
takes them on becomes a history log — one that argues, and that carries numbers someone now has to
keep true.

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
  by tooling, script walkthroughs. Delete rather than relocate. Recognise it by shape as well as by
  category: an ASCII directory tree, a table of paths, of flags, of mounts, of environment
  variables. Those earn their place in `spec.md` and `boundary.md` while you are drafting, and they
  are deleted with those files once the thing they picture exists to be read instead.
- Machine-checkable schema → the type definitions and validators.
- Test *case lists* → the test file, as data. Never prose.
- Why *this line* is what it is, including "don't 'fix' this" → a comment at that line. The most
  common mistake: rationale is durable, which makes it feel contract-shaped, but it belongs to a
  call site, not the boundary.
- A rejected alternative, or how the module came to be this way → the commit message that made the
  change, or a comment at the line when a later reader could undo it by accident. A contract states
  the rule that holds now; the moment it argues for the rule it acquires a history to keep current,
  and the figures that argument leans on go stale with nothing to catch them.

**Each clause names its enforcing test, or admits it has none** (review-only is legitimate), and
**names its sites** — the code that clause binds — on a `Sites:` line beside `Tests:`:

```
Tests: `test_an_unopenable_submission_is_a_mismatch`.
Sites: `interface/grading.py:compare`, `score/grade.py`.
```

A site is wherever someone could break the clause, which is not always Python: a Dockerfile, a
prompt file, a data file all count. **Where the code that could break it and the consumer that
would suffer are different code, name both, and say which is which** — an invariant is broken by
its producer and depended on by its readers, and the two answer different questions later. The
producer is what question 1 of `removal.md` greps; the consumer is what its question 5 checks has
not left. List the dangerous ones, not every symbol the clause mentions — this is a grep target,
not a second import graph. **`Sites: none` is an answer**, and a meaningful
one: it says the fact has no home in code, which is what a contract is for, and it marks the clause
as one a later pass must not "move somewhere better".

The two lines divide the clause's prose as well as locating it. **The contract states the caller's
assumption; the docstring at the site states the mechanism.** A clause that restates what its
site's docstring already says is the most expensive duplication there is — it reads as courtesy
from both ends, and it drifts from both ends.

**Cap ~180 lines of prose**, counting the clauses only — `Tests:` and `Sites:` lines do not count
toward it, because the cap protects the argument a reader follows and not the citations they grep.
No measured number survives in a contract: not with a date beside it, not with
a script named beside it. A figure your own run produced is a claim nothing keeps honest, and it
decays in silence because nothing fails when it goes stale. The one exception is a constant you do
not maintain and could not have found by reading the code — a vendor's cap, a retention window, a
protocol limit. That is the rule itself, not a measurement of it.

Encode test policy so violating it fails the build. Parametrize over the **closed set of cases**,
not over the fixture collection — iterating fixtures can never detect a missing one:

```python
@pytest.mark.parametrize("case", list(Case))  # every case, always
def test_derivation(case):
    sample = FIXTURES[case]  # KeyError = the gap
```

Thresholds are code; why the threshold is what it is stays prose.

## Then spec.md, marked doomed

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

## Then boundary.md, in a second pass

Same header block as the spec, with `boundary` in the title and no Blocked-by line — the
"scaffolding only, never cited from code or contract.md" disclaimer carries over verbatim.
Roughly one page.

**Enumerate from `contract.md` and the repo, not from `spec.md`.** That is what makes this a
second pass rather than a second filename: read the callers that will import this module, the
config and manifest files, the services it will talk to, and derive each section from them. Then
diff the result against the spec and reconcile. Re-reading the spec and transcribing it is the
failure mode — it inherits every blind spot the spec already has, and the enumeration stops being
a check.

Six sections, always in this order. Answer each or write "none"; never drop one. The fixed order
and fixed count are what make a boundary skimmable at a glance, and a silently omitted section is
exactly where unnoticed surface hides.

- **Public interface** — every name the module exports, and the caller that needs it. No caller,
  no export.
- **CLI / HTTP surface** — commands, flags, routes. Each with the one thing it is for.
- **Upstream** — modules called, env vars and config keys read, files/DB/services touched. Any
  of them this change *modifies*: name the other callers that will see the change, and whether
  their `contract.md` speaks to the behavior being changed.
- **Downstream** — who consumes the output, and in what format.
- **Nonfunctional constraints** — latency, throughput, cost per run, compatibility, determinism.
  A number, or "unconstrained". "Fast" is not an answer.
- **Libraries considered** — per unit of work: the candidate library, and import-or-write with the
  reason. Writing it needs a named reason, and only three count — they are the library rule in
  `reviewer-simplification.md`, next to this file, which is what Reviewer 1 will judge this section
  against. Read the dependency manifest first — something already installed beats a new dependency
  — then look the candidates up. Maintenance and popularity are facts about the world today, not
  recall: a candidate named or rejected from memory is how a review that appears to have happened
  still ships a hand-rolled wheel.

The spec says *how to build*, the boundary says *what it touches*. A line that appears in both
gets deleted from the spec. **When the two disagree, the boundary is right** — it was derived from
the contract and the code rather than from the spec.

## Then two reviewers, in parallel

Both `Agent` calls go out in **one message** so they run concurrently — `general-purpose`,
`run_in_background: false`. They run for **every** new module. There is no size exemption: the
design is a page and the code it produces is thousands of lines, so a pass that finds nothing is
still cheap, and "this one is too small to bother" is the judgment call that would void the step.

The prompts themselves live next to this file, so each agent reads its own rubric rather than
receiving it inline:

- **Reviewer 1 — simplification and reuse:** `reviewer-common.md`, then `reviewer-simplification.md`.
  The one that earns its keep; extend it as new failure modes show up.
- **Reviewer 2 — design quality:** `reviewer-common.md`, then `reviewer-design.md`.

Each prompt is two things: the rubric files to read, in that order, given as **absolute paths**
under the skill directory already resolved in `SKILL.md`, and the module under review, also
absolute — a bare `contract.md` matches nothing from the repo root. Do not summarize a rubric into
the prompt; naming the file is the whole mechanism. An agent that cannot read its rubric still
returns a confident-looking report about nothing, which is worse than the review not happening.

**Where they collide:** wrap-vs-expose. "Deep module" argues for hiding a library behind a narrow
interface; "use the library" argues for exposing it. Neither agent can see this — they run in
parallel and each knows only its own report — so it is resolved at reconcile, not in the prompts.

## Then reconcile

1. **Merge and dedup.** The reviewers overlap; the same finding from both is one finding.
2. **Resolve wrap-vs-expose**, if both reports touch it. The contract decides where it speaks to
   the question; where it is silent, that is a question for the user.
3. **Merge the question lists** and rank across both by how much the answer changes the
   recommendation — the axis the reviewers were asked to rank on. Ask the top **8**, two rounds of
   four. Everything past 8 joins the written findings list. Nothing is dropped for being over
   budget.
4. **Apply what the user accepts** to `contract.md`, `spec.md`, `boundary.md`. Record nothing
   about what they reject — a rebuttal log is one more file that would need deleting.
5. **No implementation code until this is done.**
