---
name: slow-pytest-maintenance
description: Record a pytest suite that has grown too slow as a GitHub issue, then stop. Use when a pytest run reports a suite total over 15s. Files one issue and returns to the original task — it never optimizes the tests.
---

# A slow suite is a filing, not a detour

A pytest summary crossed 15s while you were doing something else. Record it and go back —
do not fix or skip the test.

Run `file-issue.sh`, next to this file — glob `**/skills/slow-pytest-maintenance/file-issue.sh`,
project `.claude/skills/` first, then `~/.claude/plugins/`. Its directory is not knowable from
this text: the body arrives with no path attached when the skill is loaded from a plugin.

    <resolved path>/file-issue.sh <total, e.g. 18.2s>
