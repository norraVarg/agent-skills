---
name: skill-master
description: "Manual invocation only — never invoke this skill on your own. Creates, updates, audits, and measures agent skills: drafts a new skill from a short interview, applies a change request, audits one skill or the whole collection for defects, size and trigger overlap, checks every update for regressions, and on request tests a skill against real prompts and tunes its description. Do NOT load it because the user mentioned creating, updating, editing, auditing, reviewing, testing, or fixing a skill; handle those requests directly instead. Load it only when the user explicitly types /skill-master."
argument-hint: "[skill name, a change request for it, a description of a new skill, or 'audit']"
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Agent
---

# skill-master

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, `PROCEDURE.md`'s placeholders and Stage 0 capabilities map to:

- **`<guide>`** — `${CLAUDE_SKILL_DIR}/guide`.
- **`<workspace>`** — `~/.claude/skill-workspaces/<skill-name>/`.
- **`<private-terms>`** — `~/.config/skill-master/private-terms.txt`.
- **Format** — `guide/formats/claude-code.md`, unless the user is writing a skill for another agent.
- **Ask and wait** — the `AskUserQuestion` tool for a structured choice; a plain message for an
  open-ended question.
- **Run scripts** — the `Bash` tool. Test `python3 -c 'import yaml'` to choose `<py>` as Stage 0
  describes.
- **A diff or preview** — the `Edit` tool's own diff view; for a new file, show its full text.
- **Write files** — the `Write` tool for a new file or a whole-file rewrite; the `Edit` tool for
  targeted changes to an existing file.
- **Fresh contexts** — the `Agent` tool, used only in Stage 6, one call per run, all runs for an
  iteration issued in the same turn.
- **An evaluation harness** — as the format file's "Evaluation harness" section describes.

**How a typed skill name arrives.** Claude Code expands `/other-skill` into an invocation of that
skill, so the token is consumed before the skill's arguments exist — `/skill-master /other-skill`
loads both bodies and leaves the arguments empty. Recognise that case by what got loaded, not by what
was typed: if another skill's body was loaded into this turn and carried no instruction of its own,
that skill is the audit target (Stage 2A). Do not ask which mode was meant; a bare name means audit.

**Input:** `$ARGUMENTS` is the request `PROCEDURE.md` routes in Stage 0.

Do not summarise `guide/PROCEDURE.md` or the files it points to from memory. Read them.
