---
name: slow-pytest-maintenance
description: Record a pytest suite that has grown too slow as a GitHub issue, then stop. Use when a pytest run reports a suite total over 15s. Files one issue and returns to the original task — it never optimizes the tests.
---

# A slow suite is a filing, not a detour

A pytest summary crossed 15s while you were doing something else. Record it and go back —
do not fix or skip the test.

Run `file-issue.sh`, next to this file. The skill directory is the "Base directory for this
skill" that Claude Code printed when this skill loaded — the same line whether it came from a
plugin or a symlink.

    <skill-dir>/file-issue.sh <total, e.g. 18.2s>
