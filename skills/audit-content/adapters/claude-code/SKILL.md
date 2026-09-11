---
name: audit-content
description: "Audit content — a draft, a Jira ticket, a skill, a code comment, a message, a PR description, or a whole directory or guide read as one set — for unused, irrelevant, unnecessary, redundant, repeated, conflicting, misleading, wrong, unclear, or poorly worded material. Figures out what to audit from what is already in the session, or from the clipboard, a link, a file, a set of related files, a GitHub PR/issue, a Jira ticket, or a Confluence page, asking for confirmation when the target is ambiguous. Reports every finding, then fixes only what is confirmed. Invoke manually."
argument-hint: "[optional: what to audit — a name, path, link, or ticket key]"
---

# audit-content

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, step 0's capabilities map to:

- **Ask and wait** — the `AskUserQuestion` tool, for disambiguating the target (step 1)
  and confirming fixes (step 5). For a plain yes/no or open question, asking directly in
  a message and waiting for the reply also satisfies this.
- **Structured reporting** — the `ReportFindings` tool, called once with every finding,
  most severe first. There is no verification stage to survive; an empty list is a valid
  call.
- **Diff/preview** — the `Edit` tool's own diff view for local files; for content that
  lives elsewhere (a Jira ticket, a Confluence page, a PR description), show the
  proposed before/after as text before calling that platform's own update mechanism
  (`editJiraIssue`, `updateConfluencePage`, `gh pr edit`, etc.).

Step 2's sources (`guide/SOURCES.md`) map to these concrete mechanisms:

| Source | Concrete mechanism |
| --- | --- |
| Something already in the session | Re-read it from the conversation directly |
| The system clipboard | `pbpaste` via the Bash tool |
| A link | The `WebFetch` tool |
| A local file | The `Read` tool |
| A set of related documents | `find`/`ls` via the Bash tool to enumerate the set, then the `Read` tool on every file in it — not a sample |
| A GitHub PR/issue and its comments | The `gh` CLI via the Bash tool (`gh pr view`, `gh issue view`, `gh api .../comments`) |
| A Jira ticket | `mcp__atlassian__getJiraIssue` and related Atlassian MCP tools |
| A Confluence page | `mcp__atlassian__getConfluencePage` and related Atlassian MCP tools |
| An artifact already published in this session | The `Artifact` tool, action `read` |
| The agent's own not-yet-sent draft | The draft text itself, before it is sent |

**Input:** `$ARGUMENTS` is the target named in the user's own words that
`PROCEDURE.md` step 1 refers to.

Do not summarise `guide/PROCEDURE.md` or `guide/CHECKLIST.md` from memory. Read them.
