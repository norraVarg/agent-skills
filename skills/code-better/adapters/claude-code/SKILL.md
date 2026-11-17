---
name: code-better
description: "Guide the agent to produce code that follows industry best practice. Reviews everything not yet committed — staged, unstaged, and untracked files — or a whole pull request when given its link, against your coding guide, universal correctness/security/testing rules, frontend/backend conventions, and language idioms, verifies each finding independently before trusting it, then helps fix what you approve. Invoke manually after making changes."
argument-hint: "[optional: a PR link to review the whole PR, a concern to focus on, or files to limit the review to]"
allowed-tools: Read, Edit, Bash, Agent, ReportFindings
---

# code-better

The guide lives at `${CLAUDE_SKILL_DIR}/guide/`. Read
`${CLAUDE_SKILL_DIR}/guide/PROCEDURE.md` and follow it exactly, step by step.

On this platform, the capabilities `PROCEDURE.md` step 0 asks you to detect are all
available:

- **Independent check (step 4).** The `Agent` tool, one call per batch as
  `PROCEDURE.md` step 4 describes, issued in parallel. Ask each batch for the
  verdict labels `CONFIRMED`, `PLAUSIBLE`, or `REFUTED`.
- **Finding (step 3).** Directly in this conversation. When `PROCEDURE.md` step 3
  says to delegate, use one `Agent` call per shard, issued in parallel.
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
- **PR comments (step 6).** Post every confirmed comment in one call to
  `gh api repos/<owner>/<repo>/pulls/<n>/reviews --method POST`, with event
  `COMMENT`, the PR's head SHA as `commit_id`, and each comment's `path`, `line`
  and `side: RIGHT`. Ask in the closing
  question with `AskUserQuestion`, so the developer can pick "comment on the PR",
  "apply fixes", or "discuss first" without having to type it.

**Input:** `$ARGUMENTS` is either a review target (a PR link or number, a branch, a
commit range — see `PROCEDURE.md` step 1) or the optional extra context its intro
paragraph refers to, or both.

Do not summarise `guide/PROCEDURE.md` or `guide/RULE-LAYERS.md` from memory. Read them.
