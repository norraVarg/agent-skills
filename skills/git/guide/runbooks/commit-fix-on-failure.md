# Runbook — commit fix-on-failure

Read this only when step 6's commit attempt in `commit.md` fails. It classifies the failure,
resolves a fix command, retries once, and offers to store a newly-discovered fix command.
Refers back to `commit.md` step 2's recorded staged paths.

---

## Step 1 — Classify the failure

Capture the output and classify the cause:
- **prettier** — output mentions prettier / `prettier:test` / `Code style issues` / `[warn]`.
- **lint** — output mentions eslint / lint errors.
- **other** — typecheck (`tsc`) errors, or anything else.

---

## Step 2 — Resolve the fix command

Read `../fix-commands.md` (this skill's guide-level fix-commands store) and match the repo by
its identifier (git remote URL, else repo root folder name). The store is machine-local and
never committed — it names specific repositories, which skill content must not. If the file
does not exist, treat it as empty and carry on:
- If a row exists for this repo and failure type, **use the stored command directly**.
- Otherwise **discover** it:
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

---

## Step 4 — Offer to save a newly-discovered fix command

If the fix command was discovered (not read from the store) and the retry succeeded: ask the
developer to confirm saving it. On yes, append a row for this repo to `../fix-commands.md`
(repo identifier, prettier fix cmd, lint fix cmd) so future runs use it directly, creating the
file if it is absent, with this shape:

    # Learned fix-commands store

    Machine-local, never committed: it names specific repositories, which skill content
    must not. The repo identifier is the git remote URL, or the repository root folder
    name when there is no remote — never an absolute path.

    | Repo identifier | prettier fix | lint fix |
    | --- | --- | --- |
