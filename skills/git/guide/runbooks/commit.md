# Runbook — commit

Compose a commit message following the repo's own conventions, confirm it, and create a
signed commit. Before composing, check the staged changes for redundant or unnecessary
comments and let the developer decide whether to remove them. If the commit fails on a
pre-commit hook (prettier/lint), auto-fix and retry once.

**Constraints:** Subject line is always a single line, in the format from step 4. A body
is rare — add one only when step 4's why-body rule calls for it, and keep it to wrapped
prose (no bullet points). No emojis anywhere.

---

## Step 1 — Determine the repo's commit convention

Before anything else, work out two things about this specific repo: whether it uses
ticket-prefixed commit subjects, and whether it commits directly on the default branch
or requires a feature branch first. Do not assume either — infer them from the repo's
own history, and ask only when the history doesn't make it clear.

```bash
git log --oneline -15
git rev-parse --abbrev-ref HEAD
```

**Ticket prefix:** Look for a leading `type(TICKET): ...` pattern (e.g.
`feat(OB-4729): ...`) in recent subjects.
- Present in most recent commits → this repo uses ticket-prefixed subjects. Extract the
  ticket for this commit from the current branch name (the leading `LETTERS-DIGITS`
  pattern, e.g. `OB-4729-some-description` → `OB-4729`). If the branch itself carries no
  ticket pattern, ask for the ticket number before continuing.
- Absent from recent commits → this repo does not use ticket-prefixed subjects. Drop the
  `(TICKET)` scope from the subject format in step 4 entirely.
- Mixed, or too little history to tell → ask directly: does this repo use
  ticket-prefixed commits, and if so, what's the ticket for this change?

**Branch requirement:** Check whether recent commits on the default branch look like
direct commits (varied, self-contained subjects, no merge commits) or merges from
feature branches (merge-commit subjects, PR-squash patterns).
- Evidence of direct commits on the default branch → committing directly on the current
  branch, even if it is the default branch, matches this repo's convention; do not
  create a feature branch in step 6.
- Evidence of a feature-branch/PR workflow → if currently on the default branch, create
  a feature branch before committing (step 6).
- Unclear → ask directly, once, rather than assuming either way.

Keep both answers for the rest of this run; do not re-derive them per commit group.

---

## Step 2 — Inspect the staged changes

Run together:

```bash
git diff --staged --stat
git diff --staged
git status --short
```

- If the working tree is clean and nothing is staged, stop and tell the developer there
  is nothing to commit.
- **If nothing is staged but there are unstaged changes**, stage this group's paths
  (`git add <paths>`, or `git add -A` when the group is everything uncommitted), then
  re-run `git diff --staged` so the later steps see the changes. Do not ask — an
  unstaged working tree is the ordinary starting state.
- **If there are BOTH staged and unstaged changes**, present both as labeled lists
  before asking — split the paths from `git status --short` by their status-code column
  (column 1 marks staged, column 2 marks unstaged/untracked) and list each group one
  path per line, e.g.:

  ```
  Staged:
    src/pages/Profile/AvatarUpload.tsx
    src/store/actions/profileActions.ts

  Unstaged:
    src/languages/de_DE.json
    src/languages/default_EN.json
  ```

  Then ask whether to include the unstaged ones. If yes, stage them and re-run
  `git diff --staged` before composing. If no, proceed with the staged changes only.
- **Record the set of staged file paths** — they are re-staged after an auto-fix in
  step 6.

---

## Step 3 — Check for redundant or unnecessary comments

Scan the staged diff from step 2 for comments that add no value. Only consider comments
on lines this commit **adds or modifies** — never flag pre-existing comments the diff
leaves untouched. Flag a comment when it is:

- **Redundant** — restates what the code already says (e.g. `// increment i` above
  `i++`, `// return the result` above a `return`).
- **Noise** — narrates self-evident code or labels a trivial block.
- **Leftover** — commented-out code, debugging leftovers, or placeholder/TODO stubs that
  do not belong in the commit.
- **Stale** — describes behaviour the code no longer has.

If none are found, proceed to step 4.

If any are found, list each one with its file path, line number, the comment text, and a
brief reason it is redundant. Then ask the developer whether to remove or keep them:

- **Remove (all or some)** — edit the files to delete the chosen comments, re-stage the
  affected paths (`git add <paths>`), then proceed to step 4.
- **Keep** — proceed to step 4 without changes.

---

## Step 4 — Compose the message

Build a single-line title. When step 1 found this repo uses ticket-prefixed subjects:

```
type(TICKET): short description
```

Otherwise, drop the scope entirely:

```
type: short description
```

Rules:
- **Conventional Commit type** from the actual changes: `feat` (new behaviour), `fix`
  (bug fix), `chore` (maintenance, deps, config), `refactor`, `docs`, `test`, `style`,
  `build`, `ci`, `perf`.
  - `fix` means correcting a bug in already-merged/released behaviour. It does not mean
    "makes the branch build/typecheck again." If this commit completes or continues
    work split across commits on the same unmerged branch — e.g. wiring in a prop that
    an earlier commit on this branch made required — use that earlier commit's type
    instead, even though the intermediate state between the two commits was transiently
    broken and never shipped.
- **Description convention:**
  - **Lowercase start** — no leading capital (`rename lottie icons`, not `Rename lottie
    icons`). Acronyms and identifiers keep their natural case (e.g. `fi_FI`, `TOC`,
    `DE`).
  - **Imperative present tense** — `add`, `fix`, `rename`, `update`; not past tense or
    gerund. Reads as "if applied, this commit will <description>".
  - **No trailing period.**
- Cover all the important points of the staged changes while staying short and simple —
  one clear line.
- **Length** — target 6–10 words for the description, 12 as a hard ceiling. Name the
  core change, not an inventory of every changed aspect — if it's creeping past that
  because several things changed, name the change that matters most and let the diff
  carry the rest.
- **Never** add a `[FE]` / `[BE]` prefix — the repo is already one or the other, so it
  is redundant.

### When to add a body

**Default to no body.** Almost every commit is subject-only. The subject says what
changed and the diff shows how; prose restating either earns nothing.

The test: without a body, would a future reader reasonably think this commit was a
mistake, or undo it? Only then write one. A non-obvious tradeoff, a workaround for a
specific bug, or a constraint that makes an otherwise arbitrary-looking decision
necessary can clear that bar. "It adds useful context" does not — nor do renames,
dependency bumps, formatting, config changes, or a feature or fix the subject already
covers.

When a body genuinely is warranted:
- Blank line after the subject, then one sentence — two at most — wrapped at roughly 72
  characters per line.
- **Length** — target 15–25 words, 35 as a hard ceiling. State the single reason that
  matters most; do not list every one.
- Explain why, not what or how — the diff already shows those.
- No bullet points, no restating the subject, no emojis.

---

## Step 5 — Confirm the message (always)

Show the message (subject, and body if one was added) and ask the developer to confirm
before committing. If they request changes, revise it (re-applying step 4's rules) and
show it again until they confirm. Only commit once confirmed.

---

## Step 6 — Commit, with prettier/lint auto-fix

Commit, signed. If step 1 found this repo requires a feature branch and the current
branch is the default branch, create one first.

Subject only (adjust the format to step 1's convention):

```bash
git commit -S -m "type(TICKET): short description"
```

Subject plus body — use a heredoc so the blank line and wrapping are preserved exactly
as confirmed in step 5:

```bash
git commit -S -m "$(cat <<'EOF'
type(TICKET): short description

Why line one, wrapped at ~72 chars.
EOF
)"
```

**If the commit fails** (e.g. a pre-commit prettier/lint check), read
`commit-fix-on-failure.md` (in this same `runbooks/` directory) and follow it — it
covers classifying the failure, resolving a fix command, retrying once, and offering to
store a newly-discovered fix command. It expects the staged paths recorded in step 2.

---

## Output

Report the final commit message (subject, and body if one was added), plus the commit
result (hash/branch) or the reason it stopped.

When invoked as the first half of a commit-and-push flow, hand back to the push
runbook.
