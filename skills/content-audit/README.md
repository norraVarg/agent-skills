# content-audit

Audits a piece of content for unused, redundant, conflicting, misleading, or unclear
material, judging it only against itself — its own stated purpose and internal
consistency — never against outside facts.

- Works on any piece of content: a draft, a Jira ticket, a skill, a code comment, a
  message, a PR description.
- Resolves the target from whatever's already in the session, the clipboard, a link,
  a file, a GitHub PR/issue, a Jira ticket, or a Confluence page — asking when it's
  ambiguous which one you mean.
- A fixed **checklist** (`guide/CHECKLIST.md`): unused/irrelevant/unnecessary,
  redundant/repeated, conflicting, misleading/wrong, unclear/poorly worded.
- Your **own rules** (`guide/rules/user-rules.md`) apply on top, with the highest
  precedence.
- Never applies a fix without being told to; shows a diff or before/after first.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md) for how `guide/`
and `adapters/` relate to each other; this file only covers what `content-audit`
itself does.

## Install

From the repository root:

```bash
~/agent-skills/install.sh content-audit claude-code
```

## Using it

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

## How to extend

**Add or change a rule.** Append a bullet to `guide/rules/user-rules.md` in the
format the file describes.

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md); map `guide/PROCEDURE.md`'s three
capabilities onto whatever that provider actually has.
