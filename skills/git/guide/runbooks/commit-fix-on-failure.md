# Runbook — commit fix-on-failure

Read this only when step 6's commit attempt in `commit.md` fails. It classifies the failure,
resolves a fix command, and retries once.
Refers back to `commit.md` step 2's recorded staged paths.

---

## Step 1 — Classify the failure

Capture the output and classify the cause:
- **prettier** — output mentions prettier / `prettier:test` / `Code style issues` / `[warn]`.
- **lint** — output mentions eslint / lint errors.
- **other** — typecheck (`tsc`) errors, or anything else.

---

## Step 2 — Resolve the fix command

Discover it:
- Detect the package manager: `yarn.lock` → `yarn`, `pnpm-lock.yaml` → `pnpm`, else `npm`.
- prettier → the `package.json` script whose command contains `prettier --write` (fallback
  script name `prettier:write`).
- lint → the script whose command contains `eslint` with `--fix` (fallback `lint:fix`).
- Build the command as `<pm> run <script>`. If no matching script exists, treat as **other**.

---

## Step 3 — Retry once

If a fix command was resolved: run it, re-stage the originally-staged paths from `commit.md`
step 2 (`git add <paths>`), and **retry the commit once**.

If the cause is **other**, no fix command could be resolved, or the single retry still fails: do
**not** loop — show the captured output and stop so the developer can resolve it.
