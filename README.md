# Agent Skills

A personal set of skills for AI coding agents. Each skill is agent-neutral: the
actual procedure and rules are plain Markdown that names no specific tool, so the same
content works with any AI agent. A thin per-provider adapter maps that procedure
onto one platform's concrete mechanisms. Claude Code is the first provider supported.

## Skills

- [audit-content](skills/audit-content/README.md)
- [code-better](skills/code-better/README.md)
- [git](skills/git/README.md)

## How to install a skill

Two commands:

```bash
git clone <repository-url> ~/agent-skills
```

```bash
~/agent-skills/install.sh <skill-name> claude-code
```

The installer reports what it changed.

## Adding a skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the rules and structure every skill in
this repository follows.

## Keeping skills updated

```bash
git pull
```

Updates any skill already installed on a machine — `install.sh` symlinks rather than
copies.

```bash
~/agent-skills/install.sh <skill-name> claude-code
```

Also run this for a skill that machine doesn't have yet.

## Privacy

See [CONTRIBUTING.md](CONTRIBUTING.md#privacy)'s Privacy section for what may not appear in
this repository.
