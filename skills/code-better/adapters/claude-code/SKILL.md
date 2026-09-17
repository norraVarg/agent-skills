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
  surviving findings, ordered most severe first. For each finding: `short_summary`
  is the compressed plain-language hook, ending with the severity tag in brackets
  ("... [High]", "... [Medium]", "... [Low]") — keep the hook itself to roughly
  45-50 characters so the tag still fits inside the tool's 60-character limit;
  `summary` is one plain sentence stating the defect, with jargon glossed inline on
  first use, no quoted rule text, and no severity prefix (the tag already lives in
  `short_summary`, so it isn't repeated here); `failure_scenario` is the short,
  plain-language real-world consequence;
  `category` stays the finding-type slug as the tool defines it; `verdict` stays
  `CONFIRMED`/`PLAUSIBLE` from step 4 — the tool already renders this as a visible
  badge, which is what keeps plausible findings visibly distinct from confirmed
  ones. An empty findings list is a valid, complete call — don't skip it or pad it
  with a manufactured finding.
- **Diff/preview (step 6).** The `Edit` tool's own diff view.

**Input:** `$ARGUMENTS` is the optional extra context `PROCEDURE.md`'s intro paragraph
refers to.

Do not summarise `guide/PROCEDURE.md` or `guide/RULE-LAYERS.md` from memory. Read them.
