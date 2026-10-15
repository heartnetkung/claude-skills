---
name: open-pr
description: Open a pull request whose description carries the evidence a reviewer needs — screenshots of every changed screen at each supported device size for UI work, and the REST API diff plus the persistence-layer changes for backend work. Use when opening a PR for ticket work, or when asked to write or improve a PR description.
---

# A PR the reviewer can judge without checking it out

The description is the review's input. The reviewer should be able to see what changed on
screen, on the wire and in storage from the description alone, and reach for the diff only to
check how.

## 1. Read the ticket and the diff

Read the ticket the branch implements and `git diff main...HEAD`. Keep the ticket's done-when
lines beside you: every one is either met by the diff or listed under "Where it departs from
the ticket". Take every claim in the description from the diff, not from memory of the session.

Then collect evidence by what the diff touches: UI, backend, or both.

## 2. UI — every changed screen at every supported size

The screens side by side at each size are how the reviewer checks responsive design at a
glance, without resizing a browser. A single desktop screenshot hides exactly the bugs this
exists to catch.

**The sizes come from the project's responsive design policy in its README**: a list of named
sizes with their pixel dimensions. If the README has none, ask the user which sizes the project
supports, offering laptop 1440×900, tablet landscape 1180×820, tablet portrait 820×1180 and
mobile portrait 390×844 as the default, and write the answer into the README before shooting.
Never choose the sizes yourself: they are a product decision, and the next PR must use the
same ones.

**Shoot with the project's screenshot helper**, as its README documents. If it has none, add
one to the browser test suite the project already has — one function that takes a screen name
and writes one image per size — and document it beside the policy.

Shoot each screen and each state the ticket added or changed: an open menu or dialog, an empty
list and an error are screens of their own.

**Commit the images, link them by SHA, then delete them:**

1. Commit the images alone, in one commit. Note its SHA.
2. Link each image in the description as
   `https://github.com/<owner>/<repo>/blob/<sha>/<path>?raw=true`. A link by SHA still resolves
   after the file is deleted and after the branch is gone, because GitHub keeps a PR's commits.
3. Delete the images in the PR's last commit.

The repository must squash-merge for this to keep the images out of `main`'s history. With a
merge commit they stay there for good; say so in the hand-off if
`gh api repos/{owner}/{repo} --jq .allow_merge_commit` prints `true`.

## 3. Backend — what changed on the wire and in storage

Both lists are derived from the diff: the route definitions, and the schema or migration
files. Write "None" under a heading that has nothing, so the reviewer knows it was checked.

**REST API diff.** One row per route, marked added, changed or removed. For a changed route,
say what changed in the request or the response — a field added, renamed, retyped, removed, or
a new status code — and whether an existing client breaks.

**Persistence diff.** Everything that changes what is stored, or where:

- Database: tables, columns, indexes and constraints added, changed or removed, taken from the
  migration or from the schema definition. Say whether existing rows need a backfill.
- Object storage: each new or changed path pattern (such as
  `gs://<bucket>/decks/{deckId}/revisions/{n}.pptx`), what is written there and what writes it.
- Any other store the diff touches — a cache key, a queue, a file on disk — the same way.

## 4. Write the description

In this order. Drop a section that has nothing to say, except the two backend headings above.

```markdown
Closes #<ticket>. <One or two sentences: what this PR is, and what it leaves to which ticket.>

## What is here
<One bullet per thing a user or a caller can now do, bold lead word.>

## Where it departs from the ticket
<One bullet per departure, each with its reason. A done-when line met another way goes here.>

## Decisions
<Important obvious questions decided after the plan was approved, one bullet each: where
(UI part, route, how the edge case happens, or which principle and requirement), the problem,
the choice, and why — with the preference that would flip it.>

## Also changed
<Changes outside the ticket's scope, each with why it was needed.>

## Checks
<The commands run and their real results. A skipped or failing check is stated as such.>

## API
| | Route | Change |
|---|---|---|
| added | `POST /decks/{deckId}/revisions` | … |

## Persistence
<Database, then object storage, as in step 3.>

## Screens
<The sizes, and the SHA of the commit that holds the images.>

**<Screen name>**

| <Size 1> | <Size 2> | <Size 3> | <Size 4> |
|---|---|---|---|
| ![](<link>) | ![](<link>) | ![](<link>) | ![](<link>) |
```

## 5. Open it

Push the branch — the image commit must be on GitHub before its links resolve — and open the PR
with `gh pr create --body-file`. Do not merge it: the user reviews and merges.

## 6. Keep it mergeable

Resolve merge conflicts without asking, for two hours after opening the PR.

**Poll.** Right after `gh pr create`, start a background `Monitor` with an until-loop that runs
`gh pr view <n> --json state,mergeable` every 60 seconds and exits when `mergeable` is
`CONFLICTING`, when `state` is not `OPEN`, or when two hours have passed since the PR was
opened. `UNKNOWN` means GitHub is still computing; keep polling.

**Fix.** On a conflict, on the PR branch:

1. `git fetch origin main && git merge origin/main`. Merge, never rebase: the repo
   squash-merges, so the merge commit never reaches `main`, and no force-push is needed.
2. Resolve each conflicted file by the intent of both sides, read from `git log origin/main`
   for the commits that touched it.
3. Run the project's check command (its README or CLAUDE.md names it), commit the merge, push.
4. Comment on the PR: the conflicted files and how each was resolved.

Then start the loop again with the time left.

**Stop and ask instead** when both sides changed the same logic and keeping both is not
possible, or when the check fails after the merge. Leave the merge uncommitted and explain
the conflict to the user with choices.

The loop ends when the PR is merged or closed, or after two hours.

## 7. Clean up after the last PR

When the loop ends with `state` `MERGED`, clean up — but only after the ticket's last PR. If
`gh pr list --state open --search "#<ticket>"` lists another PR for the ticket, stop here.

1. Delete the remote branch: `git push origin --delete <branch>`. Already gone means GitHub
   deleted it on merge; move on.
2. Remove the worktree: `ExitWorktree` if this session is inside it, else
   `git worktree remove <path>`.
3. Delete the local branch with `git branch -D <branch>`. A squash merge leaves it looking
   unmerged, so `-d` refuses; `gh` has just confirmed the merge.
4. `git switch main && git pull && git fetch --prune`.

Report each thing removed, one line each.
