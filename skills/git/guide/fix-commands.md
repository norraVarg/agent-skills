# Learned fix-commands store

Per-repo commands that fix a pre-commit hook failure (prettier/lint) so the commit can be
retried. The commit runbook reads this table before trying to discover a command. When it has
to discover one for a repo not listed here, it asks the developer to confirm, then appends a
row.

**Repo identifier:** the git remote URL, or — if there is no remote — the repository root folder
name. Stable across machines; never an absolute path.

| Repo identifier | prettier fix | lint fix |
| --- | --- | --- |

<!-- Rows are appended here as commit-fix-on-failure.md discovers and confirms them. -->
