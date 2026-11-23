# skill-master

Creates, updates, audits and measures agent skills, and keeps them from breaking as they change.

- **Create** a skill from a short interview: purpose, trigger, steps, tools, input, output.
- **Update** a skill from a change request, then run a regression check against the pre-update
  snapshot before calling it done.
- **Audit** one skill or the whole collection: metadata, undeclared or unused tool permissions,
  broken references, size against a complexity budget, and trigger overlap between skills.
- **Measure** on request: run real prompts with and without the skill, grade the results, and tune the
  description so the skill fires when it should.
- **Keeps shareable skills generic.** A skill is personal or shareable; a shareable one — any skill in a
  repository whose rules forbid identifying information, or one you mark shareable — gets a privacy
  pass before you see the draft: a scan for your own private terms, email addresses, home paths, IP
  addresses and secrets, then a manual review of examples. Your private-terms list stays outside every
  repository.
- Shows every draft and waits for confirmation before it writes a skill file.
- A **house style** (`guide/HOUSE-STYLE.md`) for shape, size, writing and asking the user, and a
  **format file** per target agent (`guide/formats/`) for that agent's skill format.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for how `guide/` and
`adapters/` relate to each other; this file only covers what `skill-master` itself does.

## How to install

From the repository root:

```bash
./install.sh skill-master claude-code
```

## How to use it

Invoke the skill with one of:

- a skill name — audits that skill and reports before changing anything;
- a skill name plus a change — updates it;
- a name and purpose for a skill that does not exist yet — creates it;
- `audit` — checks every skill you have, including overlap between them.

It:

1. Detects what the platform can do, picks the target agent's format file, and routes the request.
2. Interviews you when creating, or applies the change or agreed audit fixes when updating.
3. Drafts the skill, reviews the draft against `guide/REVIEW-CHECKLIST.md`, validates its metadata,
   and — for a shareable skill — runs the privacy pass in `guide/PRIVACY.md`.
4. Shows the draft and waits for your confirmation.
5. Writes it, reports the size impact, and — after an update — runs a regression check.
6. Offers measured testing when the skill's output is checkable, or recommends a dry run when the skill
   needs your answers partway through.

The scripts in `guide/scripts/` need `python3`; all but `check_refs.py` and `scan_private.py` also need
PyYAML, which the procedure supplies through `uv` when the system Python lacks it. Measured testing and description
tuning need the evaluation harness the format file names.

## How to extend

**Add a target format.** Copy `guide/formats/_TEMPLATE.md` to `guide/formats/<agent>.md` and fill every
section. No other guide file changes.

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map `guide/PROCEDURE.md`'s
placeholders and capabilities onto whatever that provider actually has.
