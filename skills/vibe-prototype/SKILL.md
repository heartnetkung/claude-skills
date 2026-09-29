---
name: vibe-prototype
description: Build a throwaway, locally-running UI prototype with realistic dummy data to decide what to build, then hand it off as a spec with screenshots. Use when asked to prototype, mock up, wireframe, or vibe code a UI, dashboard, or tool before building it for real, or to continue or hand off an existing prototype.
---

# Vibe prototype

A vibe prototype is a clickable UI that runs locally, uses fake-but-realistic data, and exists to **decide what to build**. The code is disposable; the decisions are not.

What you build:

- **A plain Vite + React app** on seeded dummy data.
- **A state panel**: a floating "⚙ Prototype state" pill, bottom-left, that expands on hover and flips the whole app between states (empty / midway / mature data, run counts, roles, gates…). Every state is also a URL parameter, so the user sees any state of any page in seconds instead of clicking through a workflow to reach it.
- **A screenshot-verified loop**: each change is built and looked at before it's reported.
- **A handoff**: once the UI is settled, a spec with screenshots captures the decisions and the reasons behind them, so nothing is lost when the code is thrown away.

Expect many small iterations driven by the user's reactions. Most of the value comes from those rounds, so optimize for fast, verified, low-drama changes.

**Resolve the skill directory first.** It is the base directory Claude Code printed when this skill loaded. Every path below written `<skill-dir>/…` means that directory, made absolute.

## 1. Clarify the context, then build

The user usually knows the goal but not yet the details: the actual process, the exact inputs and outputs, what each screen needs. Working those out is what the prototype is for. So split what you need to know into two kinds:

- **Context: ask.** These are things the user already knows and you can't guess well, and a wrong guess sends the whole prototype the wrong way:
  - Purpose: what problem it solves and what decision the prototype should help make.
  - Users and setting: who uses it, and whether it's a production (customer-facing) product or an internal back-office tool. This sets the polish, density and tone of the UI.
  - Inputs and outputs, at a high level: what goes in (data sources, uploads, manual entry) and what comes out (a report, a decision, an export, a change in another system).
  - Surrounding context: existing tools or processes it replaces or plugs into, and any hard constraints.

  Skip whatever the user already told you or pointed at. Ask the rest in one short round, grouped, with your best guess for each so they can just confirm.
- **Details: don't ask, show.** The actual process steps, the exact inputs and outputs, and the fields, layouts, states and wording are worked out by prototyping and iterating: the user decides by seeing and reacting, not by answering in the abstract. A question they can't answer without seeing the screen is a question the prototype should answer instead. Make a sensible choice, build it, and mention the choice in one line so the user can redirect.

What to work out on your own before building:

- Read whatever the user points at (a process doc, a feature description, a screenshot). Extract: the user's goal, the stages/pages, and the entities.
- List the **state dimensions** the panel will need. Typical ones: page/stage, data progress preset (e.g. `fresh` / `midway` / `mature`), counts that change layout (e.g. number of runs, 0/1/many), role, feature gates. Every dimension should change something visible.

## 2. Scaffold

Put it in `prototype/` (or wherever the user says) — a plain Vite + React app, plain CSS, no UI or chart libraries (inline SVG for charts). Make it responsive from the start: desktop and phone (about 390px wide). Tablet isn't a target. Keep the file layout small and predictable:

```
prototype/
  package.json  vite.config.js  index.html  .gitignore (node_modules, dist)
  src/main.jsx
  src/data.js      # seeded dummy data, presets, page/stage definitions, domain templates
  src/App.jsx      # layout, navigation, URL state, state panel
  src/<Pages>.jsx  # one file per page group
  src/ui.jsx       # small shared pieces
  src/styles.css   # CSS variables, light theme
```

**Dummy data** (`data.js`):
- Deterministic: use a seeded PRNG (mulberry32). Don't use a bare LCG — consecutive seeds give correlated first draws and the "random" data comes out in obvious patterns.
- Realistic domain content: real-sounding names, prompts, errors, notes. Hand-write a handful of templates per case (good / each failure type) and generate volume from them.
- Worst cases too: a few long names and large numbers in every list and table, so text overflow shows up in the prototype rather than in production.
- Make the numbers tell a story (e.g. a baseline that misses the target, then improves, then a regression) — check the aggregates with a quick `node -e` before wiring UI.
- Presets build the whole workspace: `makeWorkspace(preset)` returns everything the UI needs. User edits are kept per preset in a cache, with a reset button in the panel.

**Run it**: `npm install`, then start `npm run dev` in the background and give the user the URL.

## 3. The state panel and URL state

- Bottom-left pill "⚙ Prototype state"; hovering expands a dark panel; a **pin** checkbox keeps it open.
- One segmented control per state dimension, plus prototype-only shortcuts (e.g. "fill reference data", "force unlock") and "Reset edits".
- Prototype-only shortcuts belong **in the panel, never in the real UI** — they aren't part of the product and will confuse the spec.
- Every dimension is also a URL parameter (`?page=…&preset=…&runs=…`), read once as initial state. Plus:
  - `panel=1` → panel open and pinned; `panel=0` → panel hidden (clean screenshots).
- URL params make every state reproducible: for your own screenshots and for the user to share.
- Build the hover with CSS alone (`.devpanel:hover .body, .devpanel.pinned .body { display: block }`) and hide the pill while the body shows. Tapping the pill toggles pin, so the panel works on a phone. `position: fixed` bottom-left, above everything.
- Keep all dimensions in one state object, initialised from the URL.
- Keep the workspace per preset: `makeWorkspace(preset)` is the starting point, user edits go into a cache keyed by preset, and "Reset edits" deletes that preset's entry.

## 4. The iteration loop

For every change:

1. Make the edit (small, targeted; match the existing code style).
2. `npx vite build` — catches syntax/import errors immediately.
3. **Look at it** before reporting: headless Chrome screenshot of the affected page/state, then read the image. Use this skill's `scripts/shot.sh`, saving to the scratchpad rather than the project:
   ```bash
   <skill-dir>/scripts/shot.sh <out.png> "<url-query>" [width] [height]
   ```
   For text-level checks (a label exists / was removed, list order), dump the rendered DOM instead, with the same Chrome binary and flags `shot.sh` uses. Keep `--virtual-time-budget`: without it Chrome dumps the page before React renders.
   ```bash
   chrome="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || echo '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')"
   "$chrome" --headless=new --disable-gpu --no-sandbox --virtual-time-budget=5000 --dump-dom "http://localhost:5173/?<url-query>" 2>/dev/null | grep …
   ```
4. Report briefly: what changed, what you verified, and anything you noticed but didn't change. If you verified with a screenshot, say so; if you didn't, say that.

**Check for word wrap in every screenshot.** Text that breaks onto a second line is almost always unwanted: labels, badges, chips, buttons, hints, table headers, tile captions, IDs. Look at desktop width and at phone width (390px). Fix it by shortening the text first; if the text must stay, keep the element on one line (`white-space: nowrap`, fixed-width badge, shrinking or ellipsizing the neighbour) rather than letting it wrap. Only free-form content (notes, descriptions, prompts) may wrap.

**Data overflows too.** For each data field, decide whether it truncates with an ellipsis (the full value still reachable) or wraps. Never leave it to chance. Check with the worst-case dummy values: nothing spills out of its container, overlaps a neighbour, or makes the page scroll sideways.

**Hover doesn't exist on a phone.** Anything reached by hover (tooltips, full values of truncated text) needs a tap equivalent.

Also check every time: labels overlapping in charts, dropdown values that aren't in the option list, leftover text/CSS/props after removing a feature.

## 5. Working with the user's feedback

- **Questions are questions.** "Why do we need X?", "Is this Y?" — answer with a recommendation and offer the change; don't edit code until they say so.
- **Give a recommendation, not a survey.** When they ask for suggestions, offer 2–3 options with an ASCII mockup if layout is involved, and say which you'd pick and why.
- **Point out knock-on effects** of their decision (a target that stops making sense, a filter that becomes redundant, two pages that now overlap), then let them decide.
- **Removing is a feature.** When something is dropped, remove it fully — UI, state, handlers, CSS, dummy data, stale tips — and re-check other pages for references. Offer a dead-code sweep when things settle.

UI conventions (defaults, not laws):
- One concept per card or tile group; don't mix unrelated stats.
- No duplicated information on a page — if two widgets say the same number, drop one.
- Lists newest-first (reverse chronological); left-to-right timelines stay chronological.
- Progress/targets are local to the page (and to the selected scope, e.g. run) — don't show them in global navigation.
- Look-only pages (dashboards) get no tips and no targets; action pages get short tips and a target.
- Don't put controls next to page headings; put scope pickers inside the card they scope.
- Prefer one-trace/one-item deep views plus one big-picture view over several overlapping list views.

## 6. Wording

Wording changes a lot during a prototype session — labels are where the user's mental model becomes visible. Treat copy as part of the design, not decoration:

- **Clarity over brevity: two words beat one.** Qualify a bare noun so it's clear on its own — "Failure taxonomy" over "Taxonomy", "User prompt" over "Instruction", "Failure labeling" over "Labeling". A clear two-word label is worth the extra width; shorten sentences and hints instead (see word wrap under *The iteration loop*).
- **One term per concept, everywhere.** Keep a running wording table (use / not) in your head. When a term changes, grep the whole prototype — page titles, subtitles, tips, filter options, dropdown placeholders, progress labels, empty states, tooltips, dummy data, the state panel — and change every occurrence in the same edit.
- **The user's words, not the method's jargon.** Use the domain's plain terms on screen ("Note", "User prompt") rather than process jargon ("open-coding note", "instruction"). Jargon can live in tips if at all.
- **Names must not claim more or less than they cover.** "Initial …" implies it's done once; "Latest progress" contradicts a run picker; "Eval set · user prompts" miscounts if each sample has two prompts. When scope changes, re-check the names.
- **Page and tab names are noun phrases** ("Failure labeling", "Maintenance log"); buttons are verbs ("Submit", "Add").
- **Consistent across pages.** The same status, filter option or concept reads the same on every page.
- **Minimal microcopy.** Don't add helper text that restates what the UI already shows ("click ⚐ to mark…", "no note = you confirm the pass"). Keep hints for things that block the user (why a button is disabled).
- **Suggest, then defer.** When the user proposes a name, point out an ambiguity once and offer an alternative; if they still prefer theirs, use it as given.

## 7. Handoff: spec + screenshots

When the user is happy ("ready to implement", "hand off", "wrap up"), capture the work:

1. **Screenshots** of every page in its key states, at desktop width only (no phone screenshots; mobile is covered by the spec's Definition of success), into `doc/spec/images/` (or next to the user's docs), named `NN-<page>-<state>.png` with `NN` in reading order, using `panel=0`. Pick the window height per page to avoid large empty areas. Look at each one before using it — fix small UI nits you spot (truncated placeholders, overlaps) and retake.
2. **Find the hidden interactions in the code, not from memory.** Go through the prototype for every `onClick` / `onChange`, `disabled=` condition, `:hover` rule, `title=` and conditional render. Each one becomes a hidden-interaction item in the spec's Definition of success, or is left out on purpose (prototype-only controls).
3. **Spec** at `doc/spec/<name>.md`, with these sections:
   - **Scope**: what the tool is for; the must-have goals the user accomplishes with it, high-level only (a few end-to-end outcomes, not per-screen features, which live in Pages); what was deliberately dropped.
   - **Data model**, only if the entities aren't obvious from the pages.
   - **Pages**: a nav sketch first; then per page: screenshots, layout, controls with exact options and defaults, empty states.
   - **Behaviour rules**: a table of rule | why.
   - **Definition of success**: a formal, exhaustive checklist; every item is pass/fail.
     1. *End-to-end flows*: one per must-have goal, mapping 1:1 to an e2e test: start state described as data ("4 runs, the latest regressed"), numbered steps naming controls by their on-screen label, and the expected result. Add an edge-case flow only when a behaviour rule depends on it.
     2. *Hidden interactions*: everything a screenshot can't show — hover and tooltip content, disabled states and their conditions, what changes after each action, what persists after a reload, sorting and filtering, keyboard use, confirmations.
     3. *Screenshot match*: one item per screenshot, naming its file (`images/03-labeling-mature.png`) — that page in that state matches the layout, and the wording is exact.
     4. *Behaviour rules*: every rule in the table holds.
     5. *Text overflow*: with the longest realistic data, no text spills out of its container, overlaps, or widens the layout; every truncated field shows its full value somewhere.
     6. *Mobile*: at 390px, no page scrolls sideways, every end-to-end flow completes, and everything reached by hover has a tap equivalent.

   State that the on-screen wording in the screenshots is final: implement it exactly.

   The spec must stand alone: nothing in it may need the prototype to run or be read (no URL params, no pointers into its code). The prototype is thrown away, not handed over, so the implementation carries only what the spec formally declares, never the prototype's unintentional details. It also keeps the spec portable: any section or checklist item can be pasted into a ticket and still make sense. The screenshots are part of the spec, not the prototype: every page section, flow step or checklist item they illustrate names the screenshot file, so a ticket can attach it.
4. The "why" column matters most: it's the part that lives only in the conversation, and it stops an implementer from undoing a deliberate decision.
5. Don't commit unless asked; offer it (new branch by default).
