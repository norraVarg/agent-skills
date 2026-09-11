# Learning loop

The guide improves from what a review finds. When a review turns up something a rule
would have prevented, the agent proposes a rule. The agent proposes; the developer
decides. The agent never puts a rule in force unasked.

## What counts as a gap worth a rule

- **A recurring finding.** The same category of issue is found in more than one
  separate review run — a one-off finding is a review result, not evidence of a gap.
- **A disagreement that reveals a wrong or missing rule.** The developer disputes a
  finding, and the dispute shows the rule was too strict, wrongly scoped, or genuinely
  absent, not that the review misapplied a rule that was already right.
- **A repeated developer instruction.** The developer states the same preference more
  than once across separate reviews or sessions.

A single finding accepted and fixed without complaint is not a gap. Most reviews will
not reach this loop.

A first sighting is not a gap either, but it is the only evidence a later run will
have. When a finding would clear the quality gates below as a rule and is simply too
new to have recurred, write it into `rules/candidates.md` in the rule format below —
no proposal, no question — and say in one line that you parked it. Nothing is in force
until the developer promotes it, and the next run that meets the same lesson finds it
waiting and proposes promotion (step 2).

## Procedure

Run this after the review has been reported and reacted on, never before.

1. **Would a rule have prevented this for similar code in future?** If not, stop
   silently. One-off decisions are not rules.
2. **Is it already covered?** Search the guide and `rules/candidates.md`.
   - Covered by a rule in force → the problem is enforcement, not a gap. Say so in one
     line and stop.
   - Matches a candidate → the lesson has recurred. Propose promoting that candidate
     (step 4) instead of drafting a new rule.
3. **Draft the rule.** One sentence, general (not tied to one file or project),
   actionable, not in conflict with a higher layer. Attach a *why* that names the
   lesson, not the project. Choose the target:
   - a personal preference (the developer's taste, workflow, communication) →
     `rules/user-rules.md`
   - a general truth → the lowest layer where it holds: language → domain → universal
4. **Propose it in one short message:** the rule, the target file, the why. Then wait.
   The developer answers:
   - **promote** — write the rule into the target file, under the best-matching section
     (or at the end of `rules/user-rules.md`), in the rule format below.
   - **candidate** — write it into `rules/candidates.md` in the rule format below.
   - **drop** — write nothing and do not propose it again this session.
   - anything else (a reworded rule, a different target) — apply the developer's version
     and treat the answer as promote or candidate, as indicated.
5. A new rule is in force from the **next** review run. The developer commits and
   pushes it; the agent does not commit. Other machines receive it on their next pull.

## Rule format

One bullet, one rule, one provenance comment on the following line:

    - Rule stated as an instruction. *Why:* the reason, in one clause.
      <!-- added YYYY-MM-DD · lesson: <one clause> -->

In `rules/candidates.md` the bullet also names its intended home:

    - Rule stated as an instruction. *Why:* the reason. *Target:* `path/to/file.md`
      <!-- added YYYY-MM-DD · lesson: <one clause> -->

## Quality gates

A proposal is made only if it is: general, actionable, not a duplicate, not in conflict
with a higher layer, and accompanied by a why. Proposals that fail a gate are not made.
The loop must stay quiet enough that every proposal gets read.

## What never goes into a rule

Names of people, employers, repositories, machine paths, or anything that identifies a
specific project. Rules describe lessons, not their origin.
