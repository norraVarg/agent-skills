# Git commit and push procedure

This is the whole procedure for committing and pushing changes on the developer's
behalf, whether that is one commit or several split by topic. It is written for any
agent to follow, on any platform: it names no specific tool, because no specific tool
exists on every platform. Each provider's entry point (`adapters/<provider>/`) tells
you what concretely fulfils the capabilities named in step 0, on that platform.
Everything else below is identical everywhere.

**Constraints:** No emojis in any output. Never run tests, lint, Prettier, or
typecheck as part of this procedure — not before composing, not before committing,
not to verify afterwards. The one exception is `runbooks/commit-fix-on-failure.md`:
once a pre-commit hook has already failed, running that repo's own fix command a single
time to unblock the commit is part of the retry, not a check of your own initiative.

**Re-run this procedure from the start for every commit or push request**, even when
it was already followed earlier in this session. A prior run does not cover a later
request, and working from what was already read drops steps — step 1's fresh
repo-state read is the usual casualty.

If the developer supplies extra context about the change up front (commit intent the
diff alone can't show), fold it into step 1's judgment.

## Step 0 — Detect capabilities

Before anything else, establish what you actually have to work with:

- **A way to ask and wait.** Something that can put a question to the developer and
  get their answer back before continuing — needed to confirm a commit grouping, a
  commit message, or a push (step 1a, and the runbooks' confirmation gates).

If unavailable, do not guess and do not proceed: confirmation gates every commit
(`runbooks/commit.md` step 5) and every push. Work out what you would commit, treat
everything uncommitted as one group, show the grouping and the message you would use,
and stop there for the developer to run themselves.

## Step 1 — Work out what to commit and whether to push

Load `rules/user-rules.md` first. Those rules outrank this procedure's own defaults on
any judgment call — how to group, how to word a subject, when to split. They never
relax a confirmation gate or a constraint above; those hold regardless.

Inspect repo state and combine it with the developer's own wording:

```bash
git status -sb
git diff HEAD --stat
```

`git diff HEAD --stat` covers staged and unstaged tracked changes; untracked paths
come from `git status`.

Every request reduces to two answers.

**1. Which commits to make** — an ordered list of groups, each one a set of changed
paths.

- Several when the developer says how to divide the work ("in two commits", "a
  separate commit for X", "commit X on its own"). Take the grouping from their
  wording: "the first commit is purely for ExpandableAlert" means that file alone,
  and the remainder falls to the next group. Their wording settles the grouping —
  skip step 1a.
- One group holding everything uncommitted when they say nothing about grouping and
  step 1a finds a single topic.
- Several when they say nothing about grouping but step 1a finds separate topics and
  they accept the proposed split.
- None when there is nothing uncommitted.

**2. Whether to push afterwards** — yes when they ask to push or ship, or when the
point of the request is to get the work out; no when they ask only for a commit.

Read repo state as evidence for both: uncommitted changes mean at least one group,
and commits already ahead of the upstream mean a push is due even when there is
nothing left to commit.

Ask before proceeding if the intent is genuinely ambiguous, or if a grouping the
developer described does not account for every changed path.

## Step 1a — Propose a split when the changes span separate topics

Run this only when step 1 found no grouping in the developer's wording. Skip it when
they described the grouping themselves, when a single path changed, and when they
have already staged a subset of the changes — a deliberate index is their grouping,
and `runbooks/commit.md` step 2's staged/unstaged question handles the remainder.

Judge topics from the paths and the stat first. When they suggest more than one
topic, read the full diff (`git diff HEAD`) before proposing — a grouping built on
filenames alone gets the topics wrong.

**Separate topics** are changes with different reasons behind them, each of which
would still make sense as a commit on its own. The signals worth trusting:

- They would need different Conventional Commit types — a `feat` alongside an
  unrelated `chore`.
- One subject line cannot cover them within the commit runbook's 12-word description
  ceiling without becoming a list of unrelated things.
- One change has no causal link to the rest: nothing in the others required it.

**One topic, however many files it touches** — a change plus the tests, translations,
types, fixtures, or docs that same change required; a rename or signature change
rippling across directories; formatting the edit itself produced. These are not
candidates for a split.

Default to one commit on a close call. A split the developer did not want costs them
a rebase to undo; a split missed costs a slightly broad subject line.

**When the changes are separate topics**, put the proposal to the developer and
wait — stage nothing and commit nothing until they answer. Label each group with the
topic in a few words rather than a full commit message; messages are composed later,
per group, by the commit runbook:

```
The changes look like two topics. Commit as one, or split into two?

  1. user avatar upload
       src/pages/Profile/AvatarUpload.tsx
       src/store/actions/profileActions.ts

  2. dependency bump
       package.json
       package-lock.json
```

Every changed path belongs to exactly one group, so the proposal accounts for the
whole working tree. If they accept, those groups answer step 1's first question; if
they want one commit, or a different grouping, take that instead.

## Step 2 — Load and follow the runbook(s)

Read only the file(s) the answers call for, and follow their steps exactly:

- one or more commit groups → read `runbooks/commit.md` and follow it once per
  group, in order
- a push → read `runbooks/push.md` and follow it once, after any commits

**More than one commit group?** `runbooks/commit.md` is written for a single commit.
Read `runbooks/multi-commit.md` first — it covers staging and confirming across
groups — then follow `runbooks/commit.md` once per group.

## Step 3 — Report the outcome

Report what was done: each commit message created, in order, and the push result (if
pushed). If a runbook stopped early (nothing to commit/push, an unfixable failure, or
awaiting confirmation), relay that. Stop there — no closing remarks beyond this
report.

## Step 4 — Learn, optionally

If a commit run reveals a genuine gap — the same kind of correction to a message or a
grouping recurring across runs, or a disagreement showing a rule here was wrong or
missing — follow `LEARNING.md`. Most runs will not reach this step.
