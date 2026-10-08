# {{PROJECT}}

## Setup

```bash
corepack enable     # provides the pnpm version pinned in package.json
pnpm install        # also installs the lefthook git hooks
pnpm --filter @{{SCOPE}}/e2e exec playwright install chromium   # browser for e2e tests
```

## Run

```bash
pnpm dev            # server on :8787, web on :3001 (proxies /api)
```

API docs: http://localhost:3001/api/docs (spec at `/api/openapi.json`). The server reads `PORT`.

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

It starts its own servers on :3002 and :8788, so it never collides with `pnpm dev`.

## Commands

Entry points and what each is for. One block per command, with its cost levers
and the artifact it writes — `module-design`'s merge step routes usage here, so
a command that only documents itself in `--help` is half-documented.

_Nothing here yet._

## Layout

```
packages/interface/   zod schemas shared at runtime by server and web
apps/server/          Hono API: routes/ -> services/ -> models/ -> lib/
apps/web/             Vite + React + TanStack Router/Query + Tailwind/shadcn:
                      routes/ -> components/ -> lib/
e2e/                  Playwright tests against the running web app + server
```

`apps/server/src/models/` holds mock data. A real database replaces the body of those files
and nothing above them.

TypeScript runs on Node directly, with no build step for the server: imports there carry the
`.ts` extension, and syntax Node cannot strip (enums, parameter properties) is a type error.

Import direction is enforced by `.dependency-cruiser.cjs`; the comments there explain why
each boundary exists.
