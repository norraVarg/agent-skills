# git

Runs git commit and push work on the developer's behalf, following the repo's own
conventions, whether that is one commit or several split by topic.

- Works out what to commit and whether to push from repo state plus the developer's
  own wording — including splitting unrelated changes into separate commits when they
  are genuinely separate topics.
- Detects each repo's own commit convention (ticket-prefixed subjects or not,
  feature-branch-required or not) from its own history, asking only when it's
  unclear.
- Checks staged changes for redundant or unnecessary comments before committing.
- Auto-fixes and retries once on a failed prettier/lint pre-commit hook, and learns
  the fix command per repo for next time.
- Never commits or pushes without confirmation first.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for
how `guide/` and `adapters/` relate to each other; this file only covers what `git`
itself does.

## How to install

From the repository root:

```bash
./install.sh git claude-code
```

## How to use it

Invoke the skill whenever there's something to commit or push. It:

1. Works out which commits to make and whether to push, from repo state and what you
   said.
2. Proposes a split when the changes span genuinely separate topics, and waits for
   you to confirm the grouping.
3. Follows `guide/runbooks/commit.md` for each commit group — detecting the repo's
   own convention, checking for stale comments, composing the message, confirming it,
   then committing (with an auto-fix-and-retry on a failed prettier/lint hook). With
   more than one group, `guide/runbooks/multi-commit.md` layers on the staging and
   one-confirmation-for-all adjustments first.
4. Follows `guide/runbooks/push.md` if a push was asked for.
5. Reports what was done.

## How to extend

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map
`guide/PROCEDURE.md`'s capability onto whatever that provider actually has.
