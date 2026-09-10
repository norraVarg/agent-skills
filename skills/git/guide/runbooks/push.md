# Runbook — push

Push the current branch to its remote. Pure push — this runbook never composes a message or
commits; the commit runbook handles that.

**Constraint:** No emojis.

---

## Step 1 — Determine state

```bash
git rev-parse --abbrev-ref HEAD
git status -sb
```

From these, work out: current branch, whether an upstream is set, and how many commits are ahead of
(or behind) the upstream.

---

## Step 2 — Nothing to push

If the branch is not ahead of its upstream (no unpushed commits and upstream is up to date), say so
and stop. Do not create an empty push.

---

## Step 3 — Default-branch guard

If the current branch is the default branch (`main` or `master`), pushing is outward-facing and
higher-risk — require explicit confirmation from the developer before pushing. On a feature branch,
no extra confirmation is needed (the request to push is the authorization).

---

## Step 4 — Push

Show what will be pushed (branch name + count and subjects of the unpushed commits), then push:

```bash
git push                       # if an upstream is already set
git push -u origin <branch>    # if the branch has no upstream yet
```

---

## Step 5 — Handle a rejected push

If the push is rejected by the pre-push hook for an invalid branch name (some repos enforce a
`<prefix>-<ticket>-<name>` format), surface the hook's message clearly and stop. Do not auto-rename
the branch — renaming is the developer's call.

For other rejections (e.g. non-fast-forward), report the git output and stop so the developer can
decide (pull/rebase vs force) — do not force-push automatically.

---

## Output

Report the push result: branch, remote, and whether the upstream was set. End the action here.
