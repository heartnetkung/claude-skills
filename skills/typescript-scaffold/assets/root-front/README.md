# {{PROJECT}}

## Setup

```bash
corepack enable     # provides the pnpm version pinned in package.json
pnpm install        # also installs the lefthook git hooks
pnpm --filter @{{SCOPE}}/e2e exec playwright install chromium   # browser for e2e tests
```

## Run

```bash
pnpm dev            # web on :3001
```

## Checks

Every hook runs the whole project, so these are the same thing:

```bash
pnpm check          # all checks (biome, typecheck, vitest, dependency-cruiser, knip)
pnpm test           # just unit tests
```

## End-to-end tests

Playwright is not part of `pnpm check` or the commit hook: a full run gets slow as the app
grows. It runs on demand.

```bash
pnpm e2e                          # the whole suite
pnpm e2e tests/home.spec.ts       # one spec
```

A new page or flow gets a spec in `e2e/tests/`; run that spec once to see the feature work
in a real browser. Run the whole suite when you want a regression pass.

It starts its own Vite server on :3002, so it never collides with `pnpm dev`.

## Commands

Entry points and what each is for. One block per command, with its cost levers
and the artifact it writes — `module-design`'s merge step routes usage here, so
a command that only documents itself in `--help` is half-documented.

_Nothing here yet._

## Layout

```
apps/web/             Vite + React + TanStack Router + Tailwind/shadcn:
                      routes/ -> components/ -> lib/
e2e/                  Playwright tests against the running web app
```

Import direction is enforced by `.dependency-cruiser.cjs`; the comments there explain why
each boundary exists.
