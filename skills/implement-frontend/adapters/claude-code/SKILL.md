---
name: implement-frontend
description: "Manual invocation only — never invoke this skill on your own. Implements a frontend task end to end in any project: reads the requirement from an issue tracker (Jira, GitHub Issues) or from text, a design or screenshots given directly, analyses the design (Figma, images) and the repo, asks grouped clarifying questions until nothing is assumed, writes a refined requirement spec for approval, implements test-first (component and e2e tests red, then green), checks visual fidelity against the design, and reports coverage per acceptance criterion. Scope today is React + TypeScript; trackers, design tools, test runners and frameworks plug in as variants. Load it only when the user explicitly types /implement-frontend."
argument-hint: "<issue key or URL | requirement text> [design URL or image paths ...]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, Skill, ReadMcpResourceTool, mcp__atlassian__getJiraIssue, mcp__atlassian__searchJiraIssuesUsingJql, mcp__atlassian__listJiraIssueComments, mcp__figma__create_session, mcp__figma__get_design_context, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_variable_defs, mcp__figma__get_comments, mcp__playwright__browser_navigate, mcp__playwright__browser_resize, mcp__playwright__browser_snapshot, mcp__playwright__browser_evaluate, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_click, mcp__playwright__browser_hover, mcp__playwright__browser_type, mcp__playwright__browser_press_key, mcp__playwright__browser_wait_for
---

# implement-frontend

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, `PROCEDURE.md`'s placeholders and Step 0 capabilities map to:

- **`<spec-dir>`** — `~/.claude/frontend-specs`.
- **`<profile-dir>`** — `~/.claude/frontend-profiles`.
- **Ask and wait** — the `AskUserQuestion` tool for a structured choice: up to 4 questions per call,
  2–4 options each, and an automatic "Other" option for free text. A plain message for open-ended
  questions.
- **Issue tracker access** — Jira: `mcp__atlassian__getJiraIssue` (pass `view: evidence` or the
  custom field IDs when the acceptance criteria field is missing from the compact view),
  `mcp__atlassian__listJiraIssueComments`, and `mcp__atlassian__searchJiraIssuesUsingJql` for the
  epic and linked issues. GitHub Issues: the `gh` CLI through the `Bash` tool. If the Atlassian MCP is
  not connected, the user can connect it with `/mcp`; otherwise use the no-tracker fallback.
- **Design tool access** — Figma: first load the `figma-design-to-code` skill (through the `Skill`
  tool if it is listed, otherwise read `skill://figma/figma-design-to-code/SKILL.md` with
  `ReadMcpResourceTool`); then `mcp__figma__create_session`, and for each node
  `mcp__figma__get_design_context`, `mcp__figma__get_screenshot`, `mcp__figma__get_metadata`,
  `mcp__figma__get_variable_defs` and `mcp__figma__get_comments`. If the Figma MCP is not connected,
  the user can connect it with `/mcp`; otherwise use the images fallback.
- **Run commands** — the `Bash` tool.
- **Reading the repo** (Step 2) — the `Read`, `Grep` and `Glob` tools.
- **Browser automation** — the Playwright MCP tools: `mcp__playwright__browser_navigate`,
  `browser_resize`, `browser_click`, `browser_hover`, `browser_type`, `browser_press_key` and
  `browser_wait_for` to reach a state; `browser_take_screenshot` for the comparison;
  `browser_evaluate` with `getComputedStyle` for exact values; `browser_snapshot` to find elements.
- **A diff or preview** — the `Edit` tool's own diff view; for a new file, show its full text.

**Input:** `$ARGUMENTS` is the request `PROCEDURE.md` describes under "Input".

Do not summarise `guide/PROCEDURE.md` or the files it points to from memory. Read them.
