# audit-content

Audits content for unused, redundant, conflicting, misleading, or unclear material —
one document, or a set of related documents read as one body of work. It checks the
content against itself only — its own purpose and internal consistency — never against
outside facts.

- Works on any content: a draft, a Jira ticket, a skill, a code comment, a message, a
  PR description — or a whole directory, guide, or docs tree audited as one set.
- Resolves the target from whatever's already in the session, the clipboard, a link, a
  file, a set of related files, a GitHub PR/issue, a Jira ticket, a Confluence page, a
  published artifact, or its own unsent draft — asking when it's unclear which you mean.
- On a set it also checks **across** the documents: the same rule stated twice, a
  summary that has drifted from what it summarises, two files that contradict.
- A fixed **checklist** (`guide/CHECKLIST.md`): unused/irrelevant/unnecessary,
  redundant/repeated, conflicting, misleading/wrong, unclear/poorly worded.
- Never applies a fix without being told to; shows a diff or before/after first.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for
how `guide/` and `adapters/` relate to each other; this file only covers what
`audit-content` itself does.

## How to install

From the repository root:

```bash
./install.sh audit-content claude-code
```

## How to use it

Invoke the skill with something in mind — a draft, a ticket, a file, a link, or a whole
set of files. It:

1. Identifies the target — from your own words, or what the session just produced — and
   offers to widen a single file to the set it belongs to.
2. Resolves it to raw text, and stops rather than fabricating content if the source
   isn't reachable.
3. Runs `guide/CHECKLIST.md`'s categories against the text.
4. Reports every finding, most severe first.
5. Asks how to proceed — fix everything, fix specific ones, or discuss first — and
   shows each fix as a diff or before/after before applying it. Never applies a fix
   without being told to.

## How to extend

**Keep the two-pass checklist run** (`guide/PROCEDURE.md`, step 3). The separate
structural and wording passes exist to catch more real issues on the first read; they
are not a verification step. Do not add a per-finding refutation pass — it addresses
false positives, a different problem from the missed issues the split targets.

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map
`guide/PROCEDURE.md`'s capabilities onto whatever that provider actually has.
