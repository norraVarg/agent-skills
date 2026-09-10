# audit-content

Audits a piece of content for unused, redundant, conflicting, misleading, or unclear
material. It checks the content against itself only — its own purpose and internal
consistency — never against outside facts.

- Works on any piece of content: a draft, a Jira ticket, a skill, a code comment, a
  message, a PR description.
- Resolves the target from whatever's already in the session, the clipboard, a link,
  a file, a GitHub PR/issue, a Jira ticket, or a Confluence page — asking when it's
  unclear which one you mean.
- A fixed **checklist** (`guide/CHECKLIST.md`): unused/irrelevant/unnecessary,
  redundant/repeated, conflicting, misleading/wrong, unclear/poorly worded.
- Your **own rules** (`guide/rules/user-rules.md`) apply on top, with the highest
  precedence.
- Never applies a fix without being told to; shows a diff or before/after first.
- A **learning loop**: when a finding recurs, or a disagreement reveals a rule was
  wrong or missing, the skill proposes a rule. You decide whether it is kept.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for
how `guide/` and `adapters/` relate to each other; this file only covers what
`audit-content` itself does.

## How to install

From the repository root:

```bash
~/agent-skills/install.sh audit-content claude-code
```

## How to use it

Invoke the skill with a piece of content in mind — a draft, a ticket, a file, a link,
whatever needs a pass. It:

1. Identifies the target — from your own words, or what the session just produced.
2. Resolves it to raw text, and stops rather than fabricating content if the source
   isn't reachable.
3. Runs `guide/CHECKLIST.md`'s categories against the text, then applies
   `guide/rules/user-rules.md` on top, with the highest precedence.
4. Reports every finding, most severe first.
5. Asks how to proceed — fix everything, fix specific ones, or discuss first — and
   shows each fix as a diff before applying it. Never applies a fix without being
   told to.
6. Occasionally proposes a rule, when a finding reveals a genuine gap.

**When it proposes a rule**, it sends one short message: the rule and why —
audit-content has only one rule layer, so there is no target to choose. Answer with
one word:

| Answer | Effect |
| --- | --- |
| `promote` | The rule is written into `rules/user-rules.md` and is in force from the next audit. |
| `candidate` | The rule is parked in `guide/rules/candidates.md`. If the lesson recurs, the skill points at it and proposes promotion. |
| `drop` | Nothing is written. |

**To add a rule by hand**, append a bullet to `guide/rules/user-rules.md` in the format
the file describes.

**Review `guide/rules/candidates.md` occasionally.** Promote what has recurred; delete
what has not earned its place.

## How to extend

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map
`guide/PROCEDURE.md`'s capabilities onto whatever that provider actually has.
