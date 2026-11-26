# Skills that talk to the user during a run

Read in Stage 3 or Stage 3R when the skill asks questions, waits for the user, or reports progress
while it runs. A one-shot skill that takes input and returns one result does not need this file.
Question style is not here: PROCEDURE.md's "Asking the user" covers it.

**Embed, do not point.** The skill's own body is all the model has at run time. Write each rule that
applies into the skill's body, in its own words and its own step names, and keep it short. Do not
tell the skill to "read" this file. Each rule gives its reason, so the author can adapt it.

## 1. Keep the chat quiet

The user reads the chat to decide something, not to follow the work. Noise hides the one line that
needs an answer.

- Say nothing between tool calls. No "now I will...", no counters, no "next I will...".
- A question holds only the question and what the user needs to answer it. No progress summary,
  no results of earlier checks, no list of coming steps.
- Show a value once per message. Show internal details (paths, IDs, commands) only where the user
  acts on them, usually at the end.
- Put commands, raw values and log lines in the run log (rule 7), not in the chat.
- The closing message holds the verdict, the link to the full report and the log path. It does not
  repeat what the report holds.

## 2. Name the run states

A skill that is always in one of a few named states, each with a fixed signal, lets the user see
the state at a glance.

- Running: the task-list item is in progress, with no chat text.
- Done: one result line, and the item is ticked off.
- Waiting for the user: a line that starts `WAITING`. It says what to do and which reply ends the wait.
- Paused on a problem: a failure line, `Done so far / Stopped at`, at most 5 lines of evidence, any
  fix command in its own code block, then a Retry / Skip / Stop question.

Give each finished step or case one result line of a fixed shape, for example
`<id n/total>  <RESULT>  <what was proven, 15 words at most>; <duration>`. Fold sub-steps (retries,
log lines) into the parent line. Define a small result vocabulary in the skill and say which results
pause the run. A test-style skill might use PASS, KNOWN (a documented gap), FAIL (pause) and CHECK
(unexpected, pause). A skill of another kind needs its own words.

Use the host's progress views when the host has them (a task list, chapters per phase). Without
them, the result lines alone carry the progress. Flag a soft problem, such as a slow case, on its
result line and in the report. Do not stop the run for it.

## 3. Find answers before asking

A question the skill could answer itself wastes a round trip.

- Derive candidates from context first (current branch, open pull requests, config), then validate
  them (the host resolves, the deploy is green).
- Let the number of valid candidates choose the form: one gives a yes/no line, two to four give a
  choice question, more give a choice question with the most likely few, none gives a plain
  message that says what was found and why it was dropped, followed by an open question.
- Run a typed answer through the same validation.
- Write down how each derived value is computed, so the user can predict it.

## 4. Hand over what the user must copy

- Put anything the user must paste or run (a config line, SQL, a command) in its own fenced code
  block, so the host shows a copy button.
- Where the host has a clipboard tool, also copy it there, and copy every link the run produces.
  The skill's Stage 0 names the fallback when there is none: the code block alone.
- Frame the hand-over as a reminder or a `WAITING` line, not as instructions in prose.

## 5. Check preconditions first

Check every precondition the user controls (sign-ins, local config, running servers) before the first
costly or user-dependent step. A failure found at the start costs nothing. The same failure found at
the end loses the work. Repeat a cheap check later when the state can change in between.

## 6. Pause only on surprises

- A step that needs no user decision runs without a confirmation.
- Pause on a failure or on a finding the user should know about. Nothing else stops the run.
- Write known, expected results into the skill (a documented gap, a known error) so they do not
  stop the run. They go in the report as known.

## 7. Keep a run log

A run can outlast the context: the session may compact or close.

- Write one log file per run, named with a UTC timestamp, so names never collide and sort in run
  order. Never overwrite or append to an earlier run's log.
- Keep the log outside the skill's directory and outside any repository. A shareable skill's log
  may hold private detail.
- Write each finding to the log when it comes up. Later steps (report, hand-over) read the log,
  not memory.

## 8. Learn from each run

- Keep two lists in the run log: fixes (a problem solved with the user during the run) and
  improvements (ideas that would improve the skill).
- At the end, offer each item with the exact change to the skill (file and section) in one
  multi-select question.
- Route every accepted change through skill-master's update path, so it gets the snapshot, the
  review, the regression check and, for a shareable skill, the privacy pass. A run log holds real
  detail, so strip it from a change to a shareable skill before it lands. Do not let the skill edit
  its own files directly.

## 9. Keep modes in step

When a skill has modes or variants (for example API and UI), a case that differs between them is
the usual source of drift.

- Define the shared cases once, in one table with IDs. Each mode's table adds only its own action
  and expected result, keyed by those IDs.
- Give every mode the same assertion depth on the shared layer.
- Guard drift at run time: before the first case, check that every shared ID has a row in the chosen
  mode's table. Pause if one is missing; do not run a shorter test.
- Guard drift at edit time: state in the skill that a change to a case edits the shared table and
  every mode table in one diff.
- A difference that belongs to one layer is intended, not drift.

## 10. End with a report

Where the host can publish a shareable page, end the run with a report. Otherwise write a file.
Use the same IDs as the run: one row per case, the evidence, the findings, screenshots when there
is a UI, and the log path. Do not put secrets on it.

## 11. Keep secrets out

A token or a code that reaches the chat, the log or the report is out of the user's control.

- Do not print tokens, one-time codes or full personal data in the chat, the log or the report.
  Mask them, for example to the last 3 digits.
- Keep secrets in scratch files with owner-only permissions, and read them into variables.

## Review checks for this kind of skill

Add these to Stage 3R when the skill is of this kind.

- Each rule above that applies is in the skill's body, in its own words. None is a pointer to this file.
- The skill names its run states, its result vocabulary and which results pause the run.
- No step asks for something the skill could derive, and no question carries a progress summary.
- Preconditions are checked before the first costly step.
- The skill writes a run log with a timestamped name, outside the skill directory.
- A skill with modes has one shared case table with IDs, a run-time guard and an edit-time rule.
- Nothing in the skill prints a secret.
