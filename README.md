# Agent Skills

A personal collection of skills for AI coding agents. Each skill is agent-neutral: the
actual procedure and rules are plain Markdown that names no specific tool, so the same
content works with more than one agent. A thin per-provider adapter maps that procedure
onto one platform's concrete mechanisms. Claude Code is the first provider supported.

## Skills

- [`content-audit`](skills/content-audit/) — audits a piece of content (a draft, a
  ticket, a skill, a code comment, a message) for unused, irrelevant, unnecessary,
  redundant, repeated, conflicting, misleading, wrong, unclear, or poorly worded
  material, and reports what it finds.

## Install on a new computer

Two commands:

```bash
git clone <repository-url> ~/agent-skills
```

```bash
~/agent-skills/install.sh <skill-name> claude-code
```

For example: `~/agent-skills/install.sh content-audit claude-code`.

The installer reports what it changed. To update later: `git pull`, then re-run the
same install command. It is idempotent.

## Repository map

```
skills/<skill-name>/
  guide/                      Provider-neutral — the only thing a review/audit checks against
  adapters/<provider>/        Per-provider entry point; may only read guide/, never change it
install.sh                    ./install.sh <skill-name> <provider>
```

## Adding a skill

1. Create `skills/<new-skill-name>/guide/` with the provider-neutral procedure and
   rules.
2. Add `skills/<new-skill-name>/adapters/<provider>/` with that provider's `SKILL.md`,
   an `install.sh`, and a symlink back to `../../guide`.
3. List it under Skills above.
