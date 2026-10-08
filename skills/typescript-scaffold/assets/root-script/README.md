# {{PROJECT}}

## Setup

```bash
corepack enable     # provides the pnpm version pinned in package.json
pnpm install        # also installs the lefthook git hooks
```

## Run

```bash
pnpm start          # node src/main.ts
```

## Checks

Every hook runs the whole project, so these are the same thing:

```bash
pnpm check          # all checks (biome, typecheck, vitest, dependency-cruiser, knip)
pnpm test           # just unit tests
```

## Commands

Entry points and what each is for. One block per command, with its cost levers
and the artifact it writes — `module-design`'s merge step routes usage here, so
a command that only documents itself in `--help` is half-documented.

_Nothing here yet._

## Layout

```
src/main.ts     entry point; composes the layers
src/<layer>/    one directory per architectural layer
```

TypeScript runs on Node directly, with no build step: imports carry the `.ts` extension, and
syntax Node cannot strip (enums, parameter properties) is a type error.

Import direction is enforced by `.dependency-cruiser.cjs`; the layer comments there explain
why each boundary exists.
