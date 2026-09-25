---
name: slow-pytest-maintenance
description: Record a pytest suite that has grown too slow as a GitHub issue, then stop. Use when a pytest run reports a suite total over 15s. Files one issue and returns to the original task — it never optimizes the tests.
---

# A slow suite is a filing, not a detour

A pytest summary crossed 15s while you were doing something else. Record it and go back —
do not fix or skip the test.

Run `file-issue.sh`, next to this file — `.claude/skills/slow-pytest-maintenance/file-issue.sh`
in the project first, then `~/.claude/skills/slow-pytest-maintenance/file-issue.sh`. Check those
paths directly rather than globbing: the skill directory is usually a symlink, which a glob may
not follow.

    <resolved path>/file-issue.sh <total, e.g. 18.2s>
