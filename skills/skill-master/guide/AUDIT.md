# Stage A — audit the skills you already have

Read this when the run is an audit: the request said `audit`, or the user asked to review or check
their skills generally. A create or update run never needs it.

An audit is a health check across everything at once, which is what makes it different from Stage 3R.
3R reviews one skill against itself; the cross-skill checks below catch failures that are invisible from
inside a single file. Every command comes from `<format>`'s "Validation" section.

## 1. Metadata pass, per skill

Run the validator on every skill in `<skills-root>` and print one line per skill: its name and the
validator's first line of output.

## 2. Body-level audit, across every skill

Run the body audit. It reports undeclared tools the body reaches for, declarations the body never
uses, unresolvable step references, mixed argument placeholders, and fragile descriptions.

**Findings prefixed `advisory:` are robustness notes, not defects.** Do not "fix" them by deleting
declarations without first confirming from the skill's files that the capability is genuinely unused.
Removing a needed permission breaks the skill at its next invocation, while a spare declaration merely
widens permissions — so the evidence bar for removal is higher than the checker can enforce on its own.

**A declaration used only from a bundled file will look unused.** The body audit reads the entry file
and nothing else, so a skill that pushed detail into bundled files shows findings for every tool called
from there. That is a sign of good progressive disclosure, not a defect. Run the reference check on that
skill, or read its bundled files, before touching the declaration.

## 3. Size pass, across every skill

For every skill, print its entry file's line count and estimated tokens (bytes / 4), sorted largest
first.

The entry file is the only file that matters here — it loads in full on every trigger, unlike bundled
files, which cost nothing unless a step actually reads them.

The table is a ranking, not a pass/fail list: size is a budget set by complexity, so a large skill is a
question rather than a finding. Take the largest few and ask, of each, whether the body carries
mode-specific detail that only some invocations need. Where it does, that is the finding — not the
number.

This pass exists because a skill written once and never touched again gets no other chance to be
caught — Stage 3R's version of this check only runs while a skill is being edited. For each skill that
does not survive the question, name the specific block to extract (a failure path, an edge case, an
optional variant) before handing it to Stages 2U → 5. A size warning has to be actionable, not just a
number.

## 4. Harden unquoted descriptions in bulk

Where `<format>` requires quoted descriptions, run its description-quoting command as a dry run first,
then with `--apply`. It picks the quote style that needs no escaping and refuses to write unless the
re-parsed value is byte-identical. Multi-line values are skipped and reported for manual handling.

## 5. Privacy pass, shareable skills only

Decide each skill's sharing level as PROCEDURE.md Stage 0 "Sharing" describes, then read `PRIVACY.md`
once and run its pass on every shareable skill. Unresolved hits are ❌ findings in that skill's row.
Personal skills are skipped; list them so the user can name any that should be shareable.

## 6. Apply the 3R checklist to each skill that failed

Then add these cross-skill checks, which only make sense in aggregate:

- **Trigger overlap.** Two skills whose descriptions claim the same phrases will compete, and which one
  wins is not something you can predict from the text. Run the overlap report, list every overlapping
  pair and say which skill should own each contested phrase.
- **Metadata fragility.** Metadata that parses today only because the agent is lenient — an unquoted
  value containing a colon and a space, for instance — breaks under stricter tools. Fix it the way
  `<format>` says.
- **Dead metadata.** Keys the agent does not read are inert and misleading. `<format>` lists the keys it
  reads; remove the rest.

## 7. Report and fix

Report as a table, one row per skill, each row's status carried by the marker set defined in
PROCEDURE.md → Stage 2A ("Status markers"). Then ask which fixes to apply. Fix them through Stages
2U → 5, one skill at a time, so each change still passes the confirm gate. Auditing many skills is not a
licence to batch-edit them without review.
