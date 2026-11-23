# Stage 3R — review checklist

Run this end to end before showing any draft, in create and update mode alike, even when the change was
a single line. Most of the defects this catches are introduced by small edits, not large ones. Read
`<format>`'s "Review checks" section alongside it — those are this list's format-specific half.

## Consistency — fix silently

- Every tool the skill uses is declared the way `<format>`'s "Tool permissions" section requires, and
  nothing is declared that the skill never uses.
- The description is quoted where `<format>` requires it, and covers every trigger phrase the body
  implies.
- Every step referenced by name or number actually exists, and jump instructions ("proceed to Stage
  2U") point at real steps with matching titles.
- The user's input is referenced with `<format>`'s one placeholder, consistently.
- No step depends on information that has not been gathered by the time control reaches it.
- No placeholders, no TODOs, no template braces left unfilled.
- **A skill that asks more than a single confirm carries PROCEDURE.md's "Asking the user" rules in its
  own body**: questions kept apart from information, the count announced first, choices through a
  structured-choice mechanism with a recommended option, `[n/N] Topic —` numbering, and one
  dependency-ordered group per dialog. Above all, check the closing rule, because it is the one most
  often missing: a group stays open until every answer is resolved — free text is read for what it
  actually says, a question back is answered and the original asked again, a vague answer gets a
  follow-up, and new information re-opens any earlier answer it changes. A skill without it moves on
  past unanswered questions.
- **Working identifiers stay out of deliverables.** If the skill invents identifiers for its own
  bookkeeping — requirement or finding numbers, question numbers, step names, working-file paths —
  no instruction writes them into what it delivers to others: code, tests and their titles or IDs,
  comments, fixtures, commit messages, pull requests, tickets. The same holds for this procedure's
  own stage names and question numbers in the skills it writes. An instruction such as "name each
  test after its requirement ID" is a defect, because the next reader cannot look the ID up; the
  skill keeps that mapping in its working file instead.
- **When a change touches a recurring element — a template, a field name, a table format, a step
  reference, an output format — revisit every step and update all occurrences.** Leaving one section
  updated and its siblings stale is the most common way skills rot, and it is invisible in a small
  diff.

## Structure

- **Apply the how-often-does-it-fire test to every step or rule in the draft, on every review — not
  only once the entry file has already grown past the size budget below.** Content that runs on every
  invocation stays in the body; content that fires rarely (a failure path, an edge case, an optional
  variant) moves to a bundled file behind an explicit "read X when Y" pointer, regardless of how small
  the file currently is. Token cost is cheaper to design in at this stage than to retrofit.
- **Check each existing pointer's read fraction, not only each rule's.** For every bundled file, find
  every pointer that reaches it and ask what fraction of runs hit one. A file reached unconditionally
  on the main path is not progressive disclosure — inline it, or record why density rather than tokens
  justifies the split.
- **No rule appears in both the body and a bundled file.** Two copies drift and the model ends up
  holding two versions of one instruction. Keep one and point at it.
- **No bundled file points at another bundled file for content to read.** Pointing at a script is
  fine, since a script runs without loading; a file that triggers a second read cancels the saving.
- The entry file fits its complexity budget — ~300 lines or ~4,000 estimated tokens as a working
  figure. Past that is not a defect: check the body states in one line what complexity earns the
  length, and if it does not, find the mode-specific block that belongs behind a pointer. Treat this
  as a backstop, not the primary test — the first bullet should already have caught most of it.
- Every file in `references/`, `scripts/` or `assets/` is reachable from the entry file — directly, or
  via a bundled file the entry file points at. An unreachable file will never be read. A script cited
  only from the one file that uses it is correct progressive disclosure, not a defect; a script cited
  from nowhere is dead weight.
- Bundled files over 300 lines or ~4,000 estimated tokens open with a table of contents.
- Repeated procedural logic that could be a script is a script.

## Improvements — apply only when clearly beneficial

Do not over-engineer. A skill that works is better than a skill that is elegant.

- Every "wait for the user" gate genuinely needs to be there. Remove gates that only add round trips —
  but never remove the confirm-before-write gate.
- Output formatting is consistent throughout rather than drifting between prose and code blocks.
- The final step ends with "Stop. No closing remarks." when the skill should terminate cleanly.
- Bare imperatives that would fail in an unanticipated situation get their reasoning restored. Capital
  ALWAYS and NEVER are a symptom of this.

## Structural validation

Run `<format>`'s validator on the draft (its "Validation" section has the command). It checks the
entry file's metadata only — it does not read the body, so it complements this checklist rather than
replacing it.

## Cross-skill checks

These only apply when auditing more than one skill, and they catch the failure mode that single-skill
review cannot see: two skills claiming the same trigger phrases. Which one wins is not predictable from
the text, so overlaps have to be resolved by narrowing one description, not by hoping. List every
overlapping pair and name the owner for each contested phrase.
