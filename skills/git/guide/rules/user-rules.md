# User rules

The developer's own rules: preferences about how commits are grouped, written, and
pushed. Highest precedence among the guide's layers — except the constraints and
confirmation gates in `PROCEDURE.md`, which no rule relaxes.

Format (see `LEARNING.md`, "Rule format") — one bullet, one rule, provenance on the
next line:

- Rule stated as an instruction. *Why:* the reason, in one clause.
  <!-- added YYYY-MM-DD · lesson: <one clause> -->

Rules added by hand may omit the provenance comment.

---

<!-- Rules start below this line. -->

- Ground the commit subject's verb in the exact operation the diff performs, not an approximate or euphemistic description of the outcome. *Why:* a vague-but-plausible verb misrepresents what the code actually does and disrespects the real change, even when it reads as roughly correct to a user.
  <!-- added 2026-09-23 · lesson: describing a fix by its perceived symptom (e.g. "hide") instead of the literal operation the code performs (e.g. an explicit `.remove()` call) produces a less accurate commit message than checking the diff's own vocabulary first -->

