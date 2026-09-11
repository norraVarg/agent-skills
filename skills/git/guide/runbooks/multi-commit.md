# Runbook — multiple commit groups

Read this before following `commit.md` when `PROCEDURE.md` step 1 determined there is more
than one commit group. The commit runbook is written for a single commit, so apply these
adjustments across every group.

---

## Staging

Before each group, clear the index (`git reset`) and stage only that group's paths
(`git add <paths>`). The runbook's "both staged and unstaged changes" question does not apply —
the unstaged remainder is the later groups, so proceed with the staged group without asking.

## Confirmation

Compose every group's message first and show them together for one confirmation, then commit
the groups in order. This keeps the confirm-before-commit gate while avoiding a round trip per
commit.

---

Everything else in `commit.md` — the convention detection, the message conventions, the comment
check, the signed commit, the prettier/lint retry — applies unchanged to each group. Convention
detection (step 1) is already once-per-run rather than once-per-group; `commit.md` step 1 is the
rule, this file does not change it.
