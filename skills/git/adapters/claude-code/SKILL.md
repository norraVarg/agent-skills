---
name: git
description: "Run git commit and push work following the repo's own conventions, whether that is one commit or several split by topic. Use whenever asked to commit, write/create/generate a commit message, make/create a commit, push, push changes, push to remote, push the branch, git push, git commit, commit and push, ship the current changes, or to split changes across more than one commit — 'in two commits', 'split into commits', 'a separate commit for X', 'commit X separately'. Invoke manually."
argument-hint: "[optional: extra context about the change]"
allowed-tools: Read, Bash
---

# git

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, step 0's capability maps to:

- **Ask and wait** — asking directly in a message and waiting for the reply. Use the
  `AskUserQuestion` tool for a structured choice; a plain message works for a simple
  yes/no or open question.

**Re-invoke on every request.** A commit or push request must enter through the Skill
tool, even when this file and the guide are already in context from an earlier
invocation this session — see `PROCEDURE.md`'s own note on why a prior run doesn't
cover a later request.

**Input:** `$ARGUMENTS` is the optional extra context `PROCEDURE.md`'s intro paragraph
refers to.

Do not summarise `guide/PROCEDURE.md` or its runbooks from memory. Read them.
