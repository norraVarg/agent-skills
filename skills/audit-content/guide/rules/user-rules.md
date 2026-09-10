# User rules

The developer's own rules: preferences about content quality that apply everywhere.
Highest precedence among the guide's layers.

Format (see `LEARNING.md`, "Rule format") — one bullet, one rule, provenance on the
next line:

- Rule stated as an instruction. *Why:* the reason, in one clause.
  <!-- added YYYY-MM-DD · lesson: <one clause> -->

Rules added by hand may omit the provenance comment.

---

<!-- Rules start below this line. -->

- Do not use abbreviations unless they are widely known; spell out terms in full when in
  doubt. *Why:* an unexplained abbreviation makes content harder to understand than it
  needs to be.
  <!-- added 2026-09-10 · lesson: migrated from ~/.claude/CLAUDE.md, "Language" -->

- Re-read every comment as a stranger would, and flag any that only restates the code
  next to it. *Why:* a comment that repeats what the code already says adds nothing and
  clutters the read.
  <!-- added 2026-09-10 · lesson: migrated from ~/.claude/CLAUDE.md, "Code" -->

- Flag a proposal or message that bundles multiple asks, buries the actual question in
  surrounding analysis, or makes the reader review several findings, tables, or
  trade-offs at once instead of deciding one thing. *Why:* a message doing several
  things at once prevents a decision instead of informing it.
  <!-- added 2026-09-10 · lesson: migrated from ~/.claude/CLAUDE.md, "Proposals & Questions" -->

- Flag related fixes or changes presented as several separate asks when they could be
  one bundled unit. *Why:* enumerating each for separate approval is more friction than
  one combined decision.
  <!-- added 2026-09-10 · lesson: migrated from ~/.claude/CLAUDE.md, "Proposals & Questions" -->

- Flag a question that is not simple, clear, and well structured: plain wording, one
  question at a time, options laid out as a short list rather than buried in prose.
  *Why:* a hard-to-parse question is itself a piece of unclear content.
  <!-- added 2026-09-10 · lesson: migrated from ~/.claude/CLAUDE.md, "Proposals & Questions" -->
