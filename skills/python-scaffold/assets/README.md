# {{PROJECT}}

## Setup

```bash
uv sync
uv run pre-commit install     # required — hooks are not active until this runs
```

## Checks

Every hook runs the whole project, so these are the same thing:

```bash
uv run pre-commit run --all-files    # all checks
uv run pytest                        # just tests
```

## Commands

Entry points and what each is for. One block per command, with its cost levers
and the artifact it writes — `module-design`'s merge step routes usage here, so
a command that only documents itself in `--help` is half-documented.

_Nothing here yet._

## Layout

```
src/{{PKG}}/     source, one package per architectural layer
tests/           mirrors src/
typings/         hand-written stubs for untyped deps — see typings/README.md
```

Import direction is enforced by `tach.toml`; the layer comments there explain
why each boundary exists.
