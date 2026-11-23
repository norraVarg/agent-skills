# Stage 5V — regression check after an update

Read this at the end of Stage 5 in update mode, once the files are written and the size reported. An
update is judged on what it introduced, so every check compares the written skill against the Stage 2U
snapshot in `<workspace>/skill-snapshot/`. Nothing is written in this stage.

## 1. Mechanical passes

From `<format>`'s "Validation" section, run: the validator on the skill; the reference check on the
skill with `--baseline <workspace>/skill-snapshot`; the body audit; and the overlap report. For a
shareable skill, also run the privacy scan without `--baseline`: Stage 3R left the draft with no hits,
so any hit now — new or inherited from a once-personal version — means a fix was lost between draft
and write.

The reference check covers what the body audit cannot, because it reads every bundled file rather than
the entry file alone: missing bundled files, Step/Stage and section references that resolve to nothing,
and tools named anywhere but not declared. Only findings tagged `NEW` count against the update; a
pre-existing one is reported, not blamed on it. From the body audit and the overlap report read only
this skill's rows, and treat a finding as a regression only if the snapshot would not have produced it.

## 2. Change impact

Diff `<workspace>/skill-snapshot` against the written skill, recursively.

For each hunk, name what it changed — a step, a rule, an ordering, a tool, a file, an output format, a
question — then search the whole skill for everything that refers to or depends on it. Confirm each
dependent still holds: a step that now runs later than something that reads its result, a renamed
section with an old pointer, a rule moved to a file that is no longer read on that path. This is where
most breakage hides, because the edited lines themselves were reviewed and their neighbours were not.

## 3. Scenario trace

Pick two to four realistic invocations that together pass through every branch the diff touched, plus
the skill's main path. For each, walk the skill step by step as the model would and check:

- every input a step needs has been gathered by the time the step runs;
- every pointer it follows (file, section, step, script) exists and says what the step expects;
- no branch dead-ends, loops without exit, or contradicts another instruction;
- questions follow the house style for asking, and every gate still waits where it should.

State each scenario in one line and its verdict, naming the step where it fails.

## 4. Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━ REGRESSION CHECK ━━━━━━━━━━━━━━━━━━━━━━━━━
Skill: <skill-name>

| Check | Result |
| Validator | ✅ / ❌ |
| References (new only) | ✅ / ❌ <n new> |
| Body audit, this skill (new only) | ✅ / ❌ |
| Trigger overlap | ✅ / ⚔️ |
| Privacy, shareable only (any hit) | ✅ / ❌ <n hits> |
| Change impact | ✅ / ❌ <hunk> |
| Scenario: <one line> | ✅ / ❌ <step> |

Pre-existing issues (not caused by this update)
<list, or "none">

Limits: static read-through, not a live run.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use the status markers from PROCEDURE.md Stage 2A. If anything is ❌, ask "Fix these now?" and on a yes
take the fixes through Stages 2U → 5 again — keep the original snapshot as the baseline rather than
taking a new one, so the next check still measures against the pre-update skill. Pre-existing issues are
offered separately and never fixed silently.
