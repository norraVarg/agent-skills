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

Two commands, the second from the repository root:

```bash
git clone <repository-url> ~/agent-skills
```

```bash
./install.sh <skill-name> claude-code
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
copies, so a pulled change is live immediately.

```bash
./install.sh <skill-name> claude-code
```

Run this for a skill this machine doesn't have yet, including one a pull just added.
Safe to re-run at any time.

The link points into this clone, not at a remote: a local edit is live the moment it's
saved, committed or not.

## Privacy

See [CONTRIBUTING.md's Privacy section](CONTRIBUTING.md#privacy) for what may not appear
in this repository.
