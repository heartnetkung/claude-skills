---
name: typescript-scaffold
description: Scaffold a new TypeScript project with strict tooling — pnpm, Biome, tsc strict, Vitest, dependency-cruiser layer enforcement, knip, and a 5-job lefthook gate — in one of four scopes: fullstack (Hono API + Vite/React web + Playwright), back only, front only, or scripting only. Use when starting a new TypeScript or Node project, repo, web app, API server, or script package from scratch, or when asked to set up TypeScript project structure, linting, type checking, or architectural boundaries for a fresh codebase. Greenfield only.
---

# Scaffold a TypeScript project

Produces a project where the architecture is enforced by tooling rather than by
memory, and where a fresh clone passes every check on the first run.

**Greenfield only.** Retrofitting an existing project means merging config
rather than writing it, and merging a `package.json` or a dependency-cruiser
rule set badly is worse than leaving them alone.

Assets live in `assets/` and are *frozen*: `scaffold.sh` copies them
byte-for-byte and substitutes two placeholders. Do not retype them, and do not
improvise variants of them.

Four scopes, one skill:

| Scope | Shape | What it emits |
|---|---|---|
| `fullstack` | pnpm workspace | `apps/server`, `apps/web`, `packages/interface`, `e2e` |
| `back` | pnpm workspace | `apps/server`, `packages/interface` |
| `front` | pnpm workspace | `apps/web`, `e2e` |
| `script` | flat package | `src/` |

The three app scopes share every root config file, so adding the missing half to
a `back` or `front` project later is additive: the import rules for it are
already there.

**No database, in any scope.** Which one is a per-project decision. The server
ships `models/` with mock data wired through a service and a route, so the
place a database goes is already a layer with a rule around it.

---

## Step 0 — Guard

Abort if `package.json`, `pnpm-workspace.yaml`, `apps/`, or `src/` exists in
the target directory. Say what was found and stop. Do not offer to merge.

An existing `.git` is fine — scaffolding into a freshly-cloned empty repo is
normal.

## Step 1 — Interview

**Two `AskUserQuestion` calls: four questions, then four (three for
`script`).** `AskUserQuestion` takes at most four per call, so they cannot all
go out at once. Two calls, not eight turns: a scaffold interview that dribbles one question per turn is what
this is guarding against.

The split is not arbitrary — scope is in the first call because the second
call's first question depends on its answer.

First call:

1. **Scope** — fullstack, back only, front only, or scripting only. One line
   each on what it emits, from the table above.
2. **Project name** — the root `package.json` name and the README title.
   Lowercase, hyphens allowed.
3. **CI** — add `.github/workflows/checks.yml`? Default yes. It runs
   `pnpm check`, the same thing the commit hook runs.
4. **GitHub repo** — is it created and set as `origin`? If not, ask the user to
   create it now (`gh repo create`), or to say the project will not be on GitHub.
   Step 4 reads the answer.

Second call:

5. For `fullstack`, `back`, `front`: **npm scope** — the `acme` in
   `@acme/server`. Lowercase, no `@`. Offer the project name as the default.
   For `script`: **Layers** — see Step 2. Give it room.
6. **Rigor stance** — normal (default) or explicitly experimental. Default emits
   nothing; see the rule bank on why this is never inferred.
7. **Skills** — which shared skills to enable in this project? Multi-select
   (`multiSelect: true`), one option per skill:
   - `module-design` — default yes. The `CLAUDE.md` module rules route to it.
   - `open-pr` — default yes. The `CLAUDE.md` git rule routes to it.
   - `markdown-check` — default no.
8. For `fullstack`, `back`, `front` only: **Extra packages** — anything that
   should be its own package beside the apps, such as a rendering engine or a
   parser? Default none. See Step 2 for what to ask about each.

Do not ask about a Node version, a database, a UI library, or end-to-end tests
in the gate. Those are decided: see the last section.

## Step 2 — Layers

The rule, in every scope:

> A layer may import anything below it, never above.

### fullstack, back, front — fixed, no question

The layers are frozen in `assets/workspace/dot-dependency-cruiser.cjs`, with the
reasoning for each written above the rules:

```
apps/server/src            apps/web/src
  main.ts, app.ts  entry     main.tsx        entry
  routes/          HTTP      routes/         pages
  services/        logic     components/     shared components
  models/          data      components/ui/  shadcn, imports only lib/
  lib/             helpers   lib/            hooks, API client, pure logic
```

Across packages: `packages/interface` imports nothing internal, web imports
server for types only, server never imports web. Below `routes/`, the server
may not import `hono`.

There is no question because the frameworks already fix the directories:
TanStack Router owns `routes/`, shadcn owns `components/ui/`. A rule for a
directory that does not exist yet costs nothing, so the one file covers all
three scopes.

### Extra packages — only if question 8 named any

For each package, get three things:

- its **name** — becomes `packages/<name>/` and `@<npm-scope>/<name>`;
- one line on **what lives in it**;
- **which apps import it**: server, web, or both.

Every package already has a place in the frozen rules: below both apps, above
`packages/interface`. A package never imports an app; `interface` never imports
a package. So a package that both apps import needs no new rule at all.

Rewire only for a package that one app must *not* import. Insert one rule per
forbidden app into `.dependency-cruiser.cjs`, directly after the rule named
`interface-imports-nothing-internal`, with the reason in `comment`:

```js
    {
      name: 'web-not-to-engine',
      comment: 'The engine reads font files from disk; it cannot run in a browser.',
      severity: 'error',
      from: { path: '^apps/web/' },
      to: { path: '^packages/engine/' },
    },
```

Then add each package to the "Across packages" comment at the top of that
file — what it holds and who may import it — and one line to the `Layout`
block of `README.md`.

A package that is split inside — one half for the browser, one for Node — gets
the same rule shape with a subdirectory in `to.path`. Ask before writing that
one; it is a design decision about the package, not about the scaffold.

`scaffold.sh` creates each package empty: a `package.json`, a `tsconfig.json`
and a `src/index.ts` that exports nothing. Do **not** add the package to an
app's dependencies yet. knip reports a dependency nothing imports, so the
`workspace:*` line goes in with the first import.

### script — ask

Ask for an **ordered list, top to bottom**, with one line on what lives in
each. Verify the ordering by asking which layer would be hardest to delete —
that one is usually the bottom.

A reasonable starting shape, offered as an example and not a default to accept
silently:

```
app    composes everything, owns the commands
core   the work, siblings that don't know about each other
util   pure helpers, depend on nothing internal
```

Each layer is a directory under `src/`. `src/main.ts` is the entry point and
sits above all of them.

`scaffold.sh` writes `.dependency-cruiser.cjs` with two markers. Replace them:

- `// {{LAYER_COMMENT}}` — the layer list, top to bottom, with what each is for
  and which specific mistake the boundary prevents. That prose is the part a
  reader cannot reconstruct from the rules, and it is what stops someone from
  "temporarily" relaxing a rule two years later.
- `    // {{LAYER_RULES}}` — one entry rule, then one rule per layer except the
  top one, each forbidding every layer above it:

```js
    {
      name: 'layers-not-to-entry',
      comment: 'Only src/main.ts composes the layers.',
      severity: 'error',
      from: { path: '^src/[^/]+/' },
      to: { path: '^src/main\\.ts$' },
    },
    {
      name: 'core-not-up',
      severity: 'error',
      from: { path: '^src/core/' },
      to: { path: '^src/(app)/' },
    },
    {
      name: 'util-not-up',
      severity: 'error',
      from: { path: '^src/util/' },
      to: { path: '^src/(app|core)/' },
    },
```

Create no empty layer directories. Git does not keep them, and the rules apply
from the first file.

**One caveat to state, not to act on:** modules in the *same* layer can freely
import each other. Sibling isolation needs a rule per pair. Mention this only
if the user described siblings that must not know about one another; otherwise
it is premature.

## Step 3 — Write

One command copies every frozen file. `<skill-dir>` is the "Base directory for
this skill" that Claude Code printed when it loaded:

```bash
<skill-dir>/scaffold.sh <fullstack|back|front|script> <target-dir> <project> [<npm-scope>] \
    [--ci] [--package <name>]...
```

`<npm-scope>` is required for every scope but `script`. Pass `--ci` if the
interview accepted CI, and one `--package <name>` per extra package. The script refuses to overwrite: if any file it would
write exists, it lists them and writes nothing.

Then write by hand the things that are not frozen:

| Target | Source | Treatment |
|---|---|---|
| `CLAUDE.md` | `assets/claude-md-rules.md` | assemble from bank |
| `.dependency-cruiser.cjs` | Step 2 | `script`: replace the two markers. Extra packages: insert their rules and comment lines |
| `README.md` | Step 2 | extra packages only: one `Layout` line each |

What the script places, so a failure can be traced to an asset:

| Asset directory | Lands in | Scopes |
|---|---|---|
| `shared/` | project root | all |
| `workspace/` | project root | fullstack, back, front |
| `root-<scope>/` | project root | one each |
| `interface/` | `packages/interface/` | fullstack, back |
| `server/` | `apps/server/` | fullstack, back |
| `web/`, then `web-<scope>/` | `apps/web/` | fullstack, front |
| `e2e/`, then `e2e-<scope>/` | `e2e/` | fullstack, front |
| `package/` | `packages/<name>/` | once per `--package` |
| `ci.yml` | `.github/workflows/checks.yml` | with `--ci` |

An asset named `dot-<name>` lands as `.<name>`; a real dotfile inside `assets/`
would be hidden, or would act on this repo.

`.claude/settings.json` keeps `pnpm-lock.yaml` out of context with a
`PreToolUse` hook on `Read`, not a `permissions.deny` rule. A deny matches on
the file, not the tool, so it also stops any `grep -rn ... .` that would walk
past the lockfile. The hook sees the tool name: reading the lockfile whole is
blocked, grepping it stays free.

## Step 4 — Bootstrap and verify

```bash
git init            # skip if already a repo
pnpm install        # also installs the lefthook hooks, through the root `prepare` script
git add -A
pnpm check
```

**If `origin` is on GitHub, make squash the only way to merge a PR:**

```bash
gh api -X PATCH repos/{owner}/{repo} \
  -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false
```

`open-pr` commits screenshots to the PR branch and deletes them in its last
commit; only a squash keeps them out of `main`'s history. `gh` fills in
`{owner}/{repo}` from the remote. With no GitHub remote, skip this and say so in
one line.

**`git add -A` is not optional.** `pnpm check` runs lefthook with
`--all-files`, which means every *tracked* file. With nothing tracked, every
job reports "skip" and the command exits 0 — a pass that checked nothing.
Read the summary: it must list five jobs, each with a check mark.

For `fullstack` and `front`, also prove the slice in a browser:

```bash
pnpm --filter @<npm-scope>/e2e exec playwright install chromium
pnpm e2e
```

For `back`, start the server once (`pnpm --filter @<npm-scope>/server start`)
and fetch `/api/health`. For `script`, run `pnpm start`.

**Both must pass clean.** A scaffold that arrives failing its own checks
teaches the user to ignore them, which costs more than the scaffold saves. If a
job fails, fix the scaffold and rerun — never hand over with a caveat, and never
disable the job that caught it.

Things that look like failures and are not, and one that is:

- **Biome reports formatting** in a file that carries the npm scope or project
  name: a long name pushed a line past 100 columns. Run
  `pnpm exec biome check --write .` and rerun. That is the only case where
  rewriting a frozen file is the fix.
- **A check fails on an untouched asset**: the dependency ranges are carets, so
  a fresh install can resolve a newer release than the one the assets were
  verified against. Fix it in the project, then backport — see the last section.
- **Chromium fails to launch for missing system libraries**: tell the user to
  run `pnpm --filter @<npm-scope>/e2e exec playwright install-deps chromium`
  themselves. It needs root; do not run it for them.
- `apps/web/src/routeTree.gen.ts` is frozen for the one route the slice has.
  Vite regenerates it on the next `pnpm dev`; it is excluded from Biome and
  from coverage for that reason.

## Step 5 — Enable the shared skills

How depends on where this skill itself was loaded from: the "Base directory for
this skill" that Claude Code printed when it loaded. **If there is no such line,
stop and ask the user where `claude-skills` is.** Never guess a path.

**Installed as a plugin** (the base directory contains `/plugins/cache/`):
enable each skill selected in question 7 as a project-scope plugin. This writes
`extraKnownMarketplaces` and `enabledPlugins` into `.claude/settings.json` and
keeps the frozen hook and permissions already there:

```bash
claude plugin marketplace add heartnetkung/claude-skills --scope project
claude plugin install module-design@heartnetkung-skills --scope project
```

Repeat the `install` line for each other selected skill. Never symlink into the
plugin cache: its folder is named after a commit, and an update replaces it.
Because the settings file is committed, a teammate who opens the project is
offered the same plugins; nothing depends on their disk layout.

**A `claude-skills` clone** (any other base directory): symlink each selected
skill into `.claude/skills/`. The links are relative, so they survive moving or
renaming the parent directory together with `claude-skills`:

```bash
SKILLS=$(dirname "$(readlink -f "<skill-dir>")")
mkdir -p .claude/skills
ln -s "$(realpath --relative-to=.claude/skills "$SKILLS/module-design")" .claude/skills/module-design
```

Repeat the `ln -s` line for each other selected skill. `readlink -f` resolves the
base directory to the real `claude-skills/skills/` directory, even when it was
loaded through a symlink.

Link, don't copy. `claude-skills` is the only copy of each skill, so a fix there
reaches every project, and there is nothing to keep in sync.

The scaffolded `.gitignore` ignores `.claude/skills/`: a link only resolves where
`claude-skills` sits at the same relative path. The cost: a fresh clone has no
skills until the links are made again. Say so in the hand-off.

After a plugin install, run `pnpm check` once more: `.claude/settings.json` is
tracked and has changed.

## Step 6 — Hand off

Show the layer diagram and the commands (`pnpm dev` or `pnpm start`,
`pnpm check`, and `pnpm e2e` where it exists), then point at `module-design`
for the first module — it runs the whole design sequence before any code.

Say these, each in one line:

- `apps/server/src/models/` is mock data; a real database replaces those file
  bodies and nothing above them (fullstack, back).
- End-to-end tests are outside the commit hook and CI. A new page gets its own
  spec, run once; the whole suite runs when asked (fullstack, front).
- Each extra package is empty, and which apps may import it. An app lists it
  as a `workspace:*` dependency with its first import.
- The placeholder slice — the items route and page, or `greeting.ts` — is there
  to prove the wiring. Delete it when the first real module lands.

---

## Adding a package later

The one thing this skill does after day one. When a project scaffolded here
grows a new package — a proof of concept graduating into an engine, say — do
not hand-write it:

```bash
<skill-dir>/scaffold.sh package <project-dir> <name> <npm-scope>
pnpm install
```

It writes the same empty `packages/<name>/` as `--package` and refuses if the
directory already has those files. The frozen rules already place it below both
apps, so it is usable at once.

If one app must not import it, that needs a new rule, and the project's
`CLAUDE.md` forbids editing `.dependency-cruiser.cjs` without the user. Show the
rule from Step 2 and ask; add it only on a yes.

---

## Decisions already made

Each of these was chosen once, on purpose. Do not reopen them in the interview,
and do not "improve" them while scaffolding.

- **Node runs the TypeScript, with no `tsx` and no build step** for the server
  and for scripts. So imports that Node executes carry the `.ts` extension, and
  `erasableSyntaxOnly` makes `tsc` reject enums and parameter properties, which
  Node cannot strip. `.tsx` files exist only in the web app, where Vite handles
  them.
- **Playwright is outside the gate.** The commit hook and CI run five jobs:
  biome, typecheck, vitest, dependency-cruiser, knip. A full browser run gets
  slow as an app grows, and a slow gate gets bypassed. There is no `CLAUDE.md`
  rule about it either.
- **Biome runs its `recommended` preset**, nothing more.
- **dependency-cruiser gets a private TypeScript 6** through `packageExtensions`
  in `pnpm-workspace.yaml`. It parses with the TypeScript JS API, which
  TypeScript 7 no longer ships.
- **dependency-cruiser excludes only the project's own `dist/`.** A bare
  `/dist/` pattern also drops every npm package that resolves into its own
  `dist/` — `hono` among them — and silently disables any rule about them.
- **`biome.json` points `$schema` at the installed package**, so a patch
  release of Biome does not produce a schema-version notice.
- **Biome skips `.claude/skills/`.** Step 5 links skills from outside the project,
  and Biome crashes on a symlink that leaves the repository instead of
  reporting it.
- **API docs**: `hono-openapi` generates `/api/openapi.json`; Scalar renders it
  at `/api/docs`.
- **TanStack Query ships only in `fullstack`.** `front` has nothing to fetch.

## Backporting

This skill is deliberately **not** coupled to any live project. A living
codebase accumulates workarounds and disabled hooks, and coupling would let
every one of them infect the next project with no review step.

So it goes the other way, by hand: when you improve tooling in a scaffolded
project and the change is project-agnostic, edit `assets/` here and commit.
Project-specific fixes stay where they are.

The test for "agnostic" is whether the change would still be right in a project
with none of the current one's features. Biome settings, hook shape, and
version bumps of what the scaffold already installs usually pass. A new
dependency usually does not: unlike the Python scaffold, this one names
frameworks, so every addition is one more thing each new project must delete.

After any edit to `assets/`, scaffold all four scopes into a scratch directory
and run Step 4 on each. The assets overlap, so a fix for one scope can break
another.
