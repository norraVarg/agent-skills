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
- A **learning loop**: when the same correction to a message or a grouping recurs, or a
  disagreement reveals a rule was wrong or missing, the skill proposes a rule. You
  decide whether it is kept.

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
6. Occasionally proposes a rule, when a run reveals a genuine gap.

**When it proposes a rule**, it sends one short message: the rule and why — git has only
one rule layer, so there is no target to choose. Answer with one word:

| Answer | Effect |
| --- | --- |
| `promote` | The rule is written into `rules/user-rules.md` and is in force from the next run. |
| `candidate` | The rule is parked in `guide/rules/candidates.md`. If the lesson recurs, the skill points at it and proposes promotion. |
| `drop` | Nothing is written. |

**To add a rule by hand**, append a bullet to `guide/rules/user-rules.md` in the format
the file describes.

**Review `guide/rules/candidates.md` occasionally.** Promote what has recurred; delete
what has not earned its place. The skill also parks a promising lesson there itself the
first time it meets one — too new to propose, but recorded so a later run recognises
the repeat.

## How to extend

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map
`guide/PROCEDURE.md`'s capabilities onto whatever that provider actually has.
