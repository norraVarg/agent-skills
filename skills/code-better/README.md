# code-better

Guides an AI coding agent to write code that follows industry best practice and your
own principles. It reviews everything not yet committed — staged, unstaged, and
untracked — against a portable coding guide.

- A **universal core** that applies to all languages and both frontend and backend work.
- **Domain** rules (frontend, backend) and **language** rules (TypeScript/JavaScript
  today), selected automatically from the files under review.
- Every finding is checked before it is trusted, not just accepted from a single read —
  by an independent pass where the platform has one, otherwise by a deliberately
  skeptical second look that the report says it used.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for
how `guide/` and `adapters/` relate to each other; this file only covers what
`code-better` itself does.

## How to install

From the repository root:

```bash
./install.sh code-better claude-code
```

## How to use it

Invoke the skill after making changes, staged, unstaged, or both. It:

1. Gathers everything not yet committed.
2. Classifies each changed file (language, domain) and loads the matching guide layers.
3. Finds candidate rule violations, quoting the exact rule for each.
4. Checks every candidate independently before trusting it.
5. Reports the survivors, most severe first.
6. Asks how to proceed, never applies a fix without being told to.

## How to extend

**Add a universal rule file.** Drop a new `.md` into `guide/universal/`. Every file in
that folder is loaded on every review (`guide/PROCEDURE.md`, step 2), so nothing else
changes — no template, no table row. Give it a heading and a one-line subtitle naming
what it covers, as the existing five do. Prefer a new section in an existing file; a new
file earns its place only when the subject fits none of them.

**Add a language.** Copy `guide/languages/_TEMPLATE.md` to `guide/languages/<name>.md`,
fill it in, and add one row to the Language table in `guide/RULE-LAYERS.md`.

**Add a domain.** Same with `guide/domains/_TEMPLATE.md` and the Domain table.

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map
`guide/PROCEDURE.md`'s capabilities onto whatever that provider actually has.
