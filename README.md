# Agent Skills

A personal collection of skills for AI coding agents. Each skill is agent-neutral: the
actual procedure and rules are plain Markdown that names no specific tool, so the same
content works with more than one agent. A thin per-provider adapter maps that procedure
onto one platform's concrete mechanisms. Claude Code is the first provider supported.

## Skills

- [audit-content](skills/audit-content/README.md)
- [code-better](skills/code-better/README.md)
- [git](skills/git/README.md)

## Install on a new computer

Two commands:

```bash
git clone <repository-url> ~/agent-skills
```

```bash
~/agent-skills/install.sh <skill-name> claude-code
```

For example: `~/agent-skills/install.sh audit-content claude-code`.

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for the rules and structure every skill in
this repository follows.

## Keeping machines in sync

Changes to any skill are ordinary commits. Commit and push from the machine where a
change was made; on every other machine, `git pull` and re-run the install command for
whichever skills you use there.

## Privacy

Nothing in this repository may identify a person, an employer, or a specific
machine, in any skill, in any layer: no names, gendered pronouns describing a
specific person, emails, employers, or machine paths — and no real project detail
smuggled in through a worked example, a file path, a feature name, or a skill's own
accumulated state. This applies to every skill added here, not only the ones already
present. Before committing, search the whole repository for anything that would
identify you.
