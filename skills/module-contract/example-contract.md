<!-- Worked example for the module-contract skill: a snapshot of a real contract.md, kept
     frozen as a teaching artifact. Read it for calibration and voice, not as a template —
     it exercises five of the seven kinds because that is what this module earned. -->

# mcpip.query_gen — contract

What a caller of `QueryGen.generate` is entitled to assume, and the rules that keep those
assumptions true. An arm that satisfies the type signature but breaks one of these is not done.

## The returned map is total over the dataset

`generate(dataset)` returns exactly one entry per input row, keyed by `DatasetQuery.id`. A row
whose call failed or whose reply never parsed gets a stand-in query — never a missing key.

Two consumers depend on it. `Experiment.evaluate` (`interface/pipeline.py`) searches and scores
whatever keys it is handed, so dropping failed rows would remove the hardest queries from the
benchmark and quietly *raise* the score a generation failure should have cost.
`run_query_gen.write_inspection` indexes `queries[row.id]` per dataset row, so a missing key is a
`KeyError` after the tokens are already spent.

It is also what fixes the denominator: `invalid=N/total` only means anything when `total` is the
row count.

Tests: `test_generate_writes_a_null_query_and_warns_when_the_reply_never_parses`,
`test_generate_writes_a_null_query_and_warns_when_the_call_fails`.

## A returned query is well-typed, not necessarily valid

Every value is an `IntentQuery` and type-checks; it may still fail
`interface.validate.validate_query`. Stand-ins fail it by construction, and a query that breaks a
rule twice is kept rather than dropped.

A consumer that needs validity must call `validate_query` itself — `run_query_gen.report_invalid`
does, and prints the residue. Do not infer validity from the type, or from the absence of a
warning.

Tests: `test_generate_keeps_the_best_effort_when_validation_fails_twice`,
`test_generate_keeps_the_best_effort_when_the_retry_batch_fails`.

## Only `DatasetQuery.query` reaches the model

`instruction`, `labels`, `category` and `subset` are eval ground truth. A generator that reads
them is scoring itself, and every number the pipeline produces afterwards is meaningless.

This binds every `QueryGen` arm, not just `SonnetQueryGen`. It is why the contract takes whole
`DatasetQuery` rows rather than bare strings — the arm is trusted to look at one field — and it
is the only rule here whose violation is invisible downstream: leaked ground truth shows up as a
*better* score, not as a failure.

Test: `test_generate_shows_the_model_only_the_query`.

## A row buys exactly one corrective retry

A reply that will not parse, or that parses and breaks a rule, is re-asked once with the problem
quoted back. A second failure is kept as it is.

This gap is deliberate: one stubborn row must not abort a corpus-sized run, and further retries
buy tokens rather than quality. The residue is therefore expected to be non-zero on a large run —
`run_query_gen` reports it as `invalid=N/total`. Treat a rising N as a prompt or schema problem,
not as a reason to raise the retry count.

Test: `test_generate_keeps_the_best_effort_when_validation_fails_twice`.

## Generation bills per row and is not reproducible

`generate` spends real tokens on every row it is handed, requires credentials
(`config.Settings`), and returns different queries on different runs from the same input.

Three consequences for callers: scope a run before spending it — `run_query_gen` refuses a full
synchronous run for this reason; persist the output and re-read it instead of regenerating, which
is why `Experiment` splits the generation phases from `evaluate`; and never diff two runs
expecting equality.

Review-only — no test asserts this.
