# Learning loop

The guide improves from what an audit finds. When an audit turns up something a rule
would have prevented, the agent proposes a rule. The agent proposes; the developer
decides. The agent never writes a rule unasked.

## What counts as a gap worth a rule

- **A recurring finding.** The same category of issue is found in more than one
  separate audit run — a one-off finding is an audit result, not evidence of a gap.
- **A disagreement that reveals a wrong or missing rule.** The developer disputes a
  finding, and the dispute shows the rule was too strict, wrongly scoped, or genuinely
  absent, not that the audit misapplied a rule that was already right.
- **A repeated developer instruction.** The developer states the same preference more
  than once across separate audits or sessions.

A single finding accepted and fixed without complaint is not a gap. Most audits will
not reach this loop.

## Procedure

Run this after the audit has been reported and reacted on, never before.

1. **Would a rule have prevented this for similar content in future?** If not, stop
   silently. One-off decisions are not rules.
2. **Is it already covered?** Search `CHECKLIST.md`, `rules/user-rules.md`, and
   `rules/candidates.md`.
   - Covered by a rule in force → the problem is enforcement, not a gap. Say so in one
     line and stop.
   - Matches a candidate → the lesson has recurred. Propose promoting that candidate
     (step 4) instead of drafting a new rule.
3. **Draft the rule.** One sentence, general (not tied to one document or project),
   actionable, not in conflict with `CHECKLIST.md`. Attach a *why* that names the
   lesson, not the document it came from. It always targets `rules/user-rules.md` —
   content-audit has no other rule layer to choose between.
4. **Propose it in one short message:** the rule, the why. Then wait. The developer
   answers:
   - **promote** — write the rule into `rules/user-rules.md`, in the rule format below.
   - **candidate** — write it into `rules/candidates.md` in the rule format below.
   - **drop** — write nothing and do not propose it again this session.
   - anything else (a reworded rule) — apply the developer's version and treat the
     answer as promote or candidate, as indicated.
5. A new rule is in force from the **next** audit run. The developer commits and
   pushes it; the agent does not commit. Other machines receive it on their next pull.

## Rule format

One bullet, one rule, one provenance comment on the following line:

    - Rule stated as an instruction. *Why:* the reason, in one clause.
      <!-- added YYYY-MM-DD · lesson: <one clause> -->

Same format in `rules/candidates.md` — there is only one target file, so no `*Target:*`
field is needed.

## Quality gates

A proposal is made only if it is: general, actionable, not a duplicate, not in conflict
with `CHECKLIST.md`, and accompanied by a why. Proposals that fail a gate are not made.
The loop must stay quiet enough that every proposal gets read.

## What never goes into a rule

Names of people, employers, repositories, machine paths, or anything that identifies a
specific project. Rules describe lessons, not their origin.
