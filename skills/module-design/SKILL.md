---
name: module-design
description: How to design a new module before coding it, and how to retire its build docs afterwards. Use when starting a new module or package (contract.md, then spec.md, then boundary.md, then two parallel review agents for simplification/reuse and design quality), and again when that module's implementation is about to be committed or pushed (promote what building taught you, then delete the spec and boundary). Also use when asked to prune, retire, or clean up an existing spec or module README.
---

# Module docs: contract.md is permanent, the build docs are not

- **`contract.md`** — what the rest of the system may assume of this module, and the rules keeping
  it true. Permanent. Written *before* the spec.
- **`spec.md`** — scaffolding for writing the code. **Deleted when the module lands.** Never
  named `README.md`: a doomed file must not wear a durable name.
- **`boundary.md`** — everything the module touches on the outside. Written *after* the spec, in a
  separate pass. **Deleted when the module lands**, alongside the spec.

**Default home for a durable fact is the code it is about** — call-site comment, test, docstring,
`--help`. `contract.md` is the narrow exception; when in doubt it is not a clause.

**One-way citation:** the doomed files may cite the contract, never the reverse. A contract citing
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

### Then boundary.md, in a second pass

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
  reason. Writing it needs a named reason; see the library rule below. Read the dependency
  manifest first — something already installed beats a new dependency — then look the candidates
  up. Maintenance and popularity are facts about the world today, not recall: a candidate named or
  rejected from memory is how a review that appears to have happened still ships a hand-rolled
  wheel.

The spec says *how to build*, the boundary says *what it touches*. A line that appears in both
gets deleted from the spec. **When the two disagree, the boundary is right** — it was derived from
the contract and the code rather than from the spec.

### Then two reviewers, in parallel

Both `Agent` calls go out in **one message** so they run concurrently — `general-purpose`,
`run_in_background: false`. They run for **every** new module. There is no size exemption: the
design is a page and the code it produces is thousands of lines, so a pass that finds nothing is
still cheap, and "this one is too small to bother" is the judgment call that would void the step.

Every prompt opens with the same read-first list, in order, before the agent proposes anything:
root `README.md` (what the project is ultimately for), `CLAUDE.md` (the rules binding any change
here), the dependency manifest (what is already paid for), then the module's `contract.md`,
`spec.md`, `boundary.md`.

**Never read the lockfile.** It is generated, it is often tens of thousands of tokens, and it
answers exactly one question — "is this package already here?" — which is a grep for the name.

Rules both prompts carry. The first is what the other two sections are for; the rest are how the
reports come back.

- **Maintainability comes first, and simplicity is how it is bought.** Not token cost, not line
  count, not cleverness — what the next reader has to hold in their head to change this safely.
  A design that trades simplicity away for anything else names the consumer buying it. Two things
  that read as free and are not: a *concept* costs more than the lines implementing it, so count
  concepts; and a number that decays — a tuned threshold, a measured band, a limit copied from a
  vendor's docs — is a standing obligation to re-measure, and nothing fails visibly when it goes
  stale.
- **Neither agent edits a file.** The output is a report.
- **Findings are uncapped**, ranked, severity-tagged, and concrete: file → what to cut or replace
  → why. Never drop a minor one — several minor findings seen side by side are usually one
  misconception, and that is visible only when all of them are reported.
- **Questions are ranked and listed separately**, and only for what changes the recommendation.
  Anything below that bar is reported as a flagged assumption ("assumed X; wrong if Y") instead.
- **A contract clause may be challenged only while it is uncommitted** — `git status --porcelain
  <absolute path to contract.md>` prints something (`??` untracked, `A`/`M` staged or modified).
  Not `git diff HEAD`: that is silent for an untracked file, which is what a brand-new module's
  contract is, and the rule would disable itself in the exact case it exists for. Spell the path
  out in the prompt; a bare `contract.md` matches nothing from the repo root. A committed clause
  is accepted and out of scope, even when the file around it changed in this branch. A challenge
  is advisory: it is raised for the user to decide, never applied by the agent.

**Reviewer 1 — simplification and reuse.** The one that earns its keep; extend it as new failure
modes show up.

- **Does this need to exist yet?** Ask it of every capability before asking whether it is small.
  Name the observation that makes it necessary and say whether it has happened; "we will want
  this once X lands" means X is the consumer, and X has not landed. Then price the deferral:
  what would adding it later cost, and is anything lost that cannot be reconstructed from what
  the project already retains? **Cheap-to-add-later plus nothing-lost is a defer, not a build** —
  and the reverse is what keeps this from deferring everything. A capability that gets harder or
  impossible to add once data stops being kept is a build, now.
- The smallest thing that satisfies the contract. Propose cuts to the spec and to the boundary
  surface: an export nobody calls, a flag with one caller, a config knob never turned.
  **Smallest is counted at the callers, not in the diff.** A one-line change to shared code is
  not smaller than an optional parameter if it changes what existing callers get; the parameter
  whose default is today's behavior is the smaller change, however many lines it threads.
- **Is this a solved problem?** Before accepting a bespoke procedure, name the established method
  for the problem class — a statistical test, a known algorithm, a standard protocol — and say why
  the hand-built version beats it. An empty package search is not evidence that no method exists:
  the method is often a few lines of stdlib once you know its name, which is exactly the case a
  library search cannot surface.
- **Reuse before writing.** Search the repo for code that already does this and propose refactoring
  it to fit, rather than a second implementation beside it. Search by symbol and filename over the
  packages the boundary's Upstream names — not a read of the tree.
- **Library before hand-rolling.** A battle-tested library is more robust and more flexible than
  code written this week; the default is to import. Only three rejections count: unmaintained, no
  real user base, or it drags in far more than the module needs. These are *not* rejections —
  "we'd only use 10% of it", "I could write it in 50 lines", "one more dependency". All three
  admissible rejections are claims about the world today, so look them up rather than recalling
  them: "unmaintained" cites a last-release date. Look up only the candidates you end up naming
  in a finding — one lookup each, not a survey of the field.
- A proposed dependency is a proposed edit to the dependency manifest and whatever gates it
  (lockfile, layering rules, unused-dependency checks). Name that cost in the finding; `CLAUDE.md`
  says what is off-limits.

**Reviewer 2 — design quality.** The prompt tells it to `Read` `design-philosophy.md` *first*, then
judge against it: deep modules, information hiding, complexity as something that accumulates one
small decision at a time.

Resolve that file's **absolute path before spawning** — the agent starts cold and cannot resolve
"next to the skill you were spawned from", and neither can you when this skill is loaded from a
plugin rather than a vendored copy, because the body arrives as text with no path attached. Glob
`**/skills/module-design/design-philosophy.md`, project `.claude/skills/` first, then
`~/.claude/plugins/`. **If it is not found, say so and skip Reviewer 2** — never spawn it with a
guessed path. An agent that cannot read its rubric still returns a confident-looking report about
nothing, which is worse than the review not happening.

**Where they collide:** wrap-vs-expose. "Deep module" argues for hiding a library behind a narrow
interface; "use the library" argues for exposing it. Neither agent can see this — they run in
parallel and each knows only its own report — so it is resolved at reconcile, not in the prompts.

### Then reconcile

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

---

## Phase 2 — at merge / commit / push

Deletion is unconditional, so there is no per-section judgment. What remains is capturing what
could not be written in advance.

1. **Does the shipped module match the boundary it was reviewed against?** Diff `boundary.md`'s
   *Public interface* and *Libraries considered* lists against what actually exists — the module's
   exports, and the manifest. Every divergence is either a bug to fix in the code or a decision to
   record in `contract.md`. This is the only step where the design review binds the code: without
   it a module can name a library, pass both reviewers, hand-roll it anyway during implementation,
   and have the evidence deleted at step 6.
2. **What did building this teach you that is unwritten?** → `contract.md`. The step that cannot
   be front-loaded: failure modes found by running it, a fallback that mattered more than
   expected, a missed ordering constraint. Expect little here if the code is already well
   commented — then step 3 is where the value is. Re-read `boundary.md` here too: a cost or
   compatibility constraint that turned out to be real is a contract clause, not a deleted line.
3. **Any "don't fix this" still only in your head?** → comment at the call site, with its revisit
   condition. Typically a rejected alternative and the condition that would justify revisiting it.
   *Tiebreaker vs. the contract: could the reader plausibly never open this file?*
4. **Usage** — invocations, flags, cost levers → `--help` and the root README's command index.
5. **Fix references** — grep for both doomed filenames; package docstrings and entry-point scripts
   commonly cite them.
6. **Delete the spec and the boundary** (`git rm` both), in the same commit as the implementation.

Then re-read `contract.md` whole: still self-contained, under the cap, citing nothing deleted.
