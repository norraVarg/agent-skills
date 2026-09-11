---
name: code-better
description: "Guide the agent to produce code that follows industry best practice and your own customized coding principles. Reviews everything not yet committed — staged, unstaged, and untracked files — against your coding guide, universal correctness/security/testing rules, frontend/backend conventions, language idioms, and your personal rules, verifies each finding independently before trusting it, then helps fix what you approve. Invoke manually after making changes."
argument-hint: "[optional: a concern to focus on, or files to limit the review to]"
allowed-tools: Read, Edit, Bash, Agent, ReportFindings
---

# code-better

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, the capabilities `PROCEDURE.md` step 0 asks you to detect are all
available:

- **Independent check (steps 3 and 4).** The `Agent` tool. In step 3, run the safety
  pass and the style pass as two separate `Agent` calls. In step 4, make one separate
  `Agent` call per candidate finding, giving it only the file and the quoted rule, not
  the reasoning that produced the finding. Ask it to try to refute the finding and
  return exactly one of `CONFIRMED`, `PLAUSIBLE`, or `REFUTED`. Keep confirmed and
  plausible; drop refuted.
- **Structured report (step 5).** Call the `ReportFindings` tool once with the
  surviving findings, most severe first.
- **Diff/preview (step 6).** The `Edit` tool's own diff view.

**Input:** `$ARGUMENTS` is the optional extra context `PROCEDURE.md`'s intro paragraph
refers to.

Do not summarise `guide/PROCEDURE.md` or `guide/RULE-LAYERS.md` from memory. Read them.
