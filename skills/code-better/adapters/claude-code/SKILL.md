---
name: code-better
description: Guide the agent to produce code that follows industry best practice and your own customized coding principles. Reviews the staged and unstaged changes against your coding guide, universal correctness/security/testing rules, frontend/backend conventions, language idioms, and your personal rules, verifies each finding independently before trusting it, then helps fix what you approve. Invoke manually after making changes.
---

# code-better

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/REVIEW.md` and follow it exactly, step by step.

On this platform, the two capabilities `REVIEW.md` step 0 asks you to detect are both
available:

- **Independent check (step 4).** For each candidate finding, make one separate
  `Agent` tool call, giving it only the file and the quoted rule, not the reasoning
  that produced the finding. Ask it to try to refute the finding and return exactly
  one of `CONFIRMED`, `PLAUSIBLE`, or `REFUTED`. Keep confirmed and plausible; drop
  refuted.
- **Structured report (step 5).** Call the `ReportFindings` tool once with the
  surviving findings, most severe first.

Do not summarise `guide/REVIEW.md` or `guide/PROCEDURE.md` from memory. Read them.
