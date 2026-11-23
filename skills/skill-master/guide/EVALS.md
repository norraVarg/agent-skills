# Stage 6 — testing and measuring a skill

Run only when the user has asked for it. Needs fresh contexts and the evaluation harness (PROCEDURE.md
Stage 0). The names in angle brackets below — `<schemas>`, `<grader>`, `<aggregate>`, `<analyzer>`,
`<viewer>`, `<comparator>` — are the harness's files and commands, listed in `<format>`'s "Evaluation
harness" section.

The point of this stage is that a skill's quality is not visible by reading it. Two descriptions that
look equally good can differ by a wide margin in whether the skill fires, and two bodies that read well
can differ in whether the model actually follows them. So run the thing and look at the output.

## Where the results live

Under `<workspace>`, with one subdirectory per iteration (`iteration-1/`, `iteration-2/`) and one per
test case inside that. Create directories as you go rather than all at once.

## Step 1 — Write test prompts

Two or three realistic prompts — the kind the user would actually type, with concrete detail: file
paths, names, actual column headers, some casual phrasing. Abstract prompts test nothing.

Show them to the user before running: "Here are the test cases I'd like to try. Do these look right, or
do you want to add more?"

Save them to `<workspace>/evals/evals.json`. Prompts only at this point, no assertions yet:

```json
{
  "skill_name": "example-skill",
  "evals": [
    { "id": 1, "prompt": "User's task prompt", "expected_output": "Description of expected result", "files": [] }
  ]
}
```

Full schema: `<schemas>`.

## Step 2 — Start every run at once

For each test case, start two fresh-context runs together — one with the skill, one baseline. Starting
them together matters; staggering them wastes wall-clock and skews the timing comparison.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** — same prompt, but what "baseline" means depends on the situation:

- **New skill** → no skill at all, saved to `without_skill/outputs/`.
- **Update** → the Stage 2U snapshot at `<workspace>/skill-snapshot/`, saved to `old_skill/outputs/`.
  Comparing an update against nothing tells you the skill beats no skill, which you already knew.

Write an `eval_metadata.json` per test case, named for what it tests rather than `eval-0`:

```json
{ "eval_id": 0, "eval_name": "descriptive-name-here", "prompt": "The user's task prompt", "assertions": [] }
```

## Step 3 — Draft assertions while the runs are in flight

Do not idle. Write objectively verifiable assertions with descriptive names, so they read clearly in
the viewer. Update `eval_metadata.json` and `evals.json` once drafted, and explain to the user what each
one checks.

Subjective qualities — tone, layout, whether the wording feels right — are for the human to judge. Do
not manufacture assertions for them; a passing assertion that measures nothing is worse than no
assertion, because it inflates the score.

## Step 4 — Capture timing as each run finishes

Record each run's token count and duration as soon as it finishes — on many platforms the completion
notice is the only place that data appears — in `timing.json` in the run directory:

```json
{ "total_tokens": 84852, "duration_ms": 23332, "total_duration_seconds": 23.3 }
```

## Step 5 — Grade, aggregate, show

1. **Grade** — follow `<grader>`, writing `grading.json` per run directory with the field names the
   format specifies. Where an assertion can be checked programmatically, write a script instead of
   eyeballing it; it is faster, repeatable across iterations, and not subject to wishful reading.
2. **Aggregate** with `<aggregate>`. It produces a benchmark with pass rate, time and tokens per
   configuration, mean ± standard deviation, and the delta. Put each with-skill entry immediately
   before its baseline counterpart.
3. **Look past the averages** — `<analyzer>` covers what to look for. The useful signals are assertions
   that pass regardless of the skill (they discriminate nothing and should be replaced), evals with high
   variance across runs (flaky, so their deltas mean little), and cases where the skill improves quality
   but costs a lot more time or tokens.
4. **Open the viewer before forming your own opinion** with `<viewer>`, adding the previous iteration
   from iteration 2 onward. Use the harness's viewer rather than writing custom HTML. Tell the user how
   to move through it and how to submit their reviews.
5. **Read the feedback** when they say they are finished. Empty feedback means that case was fine;
   concentrate on the ones with specific complaints. Then stop the viewer.

## Step 6 — Improve, then repeat

- **Generalize from the feedback.** You and the user are iterating on three examples, but the skill
  will run on hundreds of prompts. A fix that satisfies these three examples and nothing else is not a
  fix. When something is stubborn, try a different framing or a different pattern of working rather
  than piling on constraints.
- **Read the transcripts, not just the outputs.** If the model wasted effort, the instruction that sent
  it there is the thing to cut.
- **Cut every instruction that does not change the result.**
- **Watch for repeated work.** If all three runs independently wrote a similar helper script, that
  script belongs in `scripts/`.

Apply improvements through the normal confirm gate (Stage 4), then rerun into `iteration-<N+1>/`,
baselines included. Stop when the user is satisfied, when all feedback comes back empty, or when
iterations stop producing meaningful change.

## Optional — blind comparison

For a rigorous answer to "is the new version actually better", `<comparator>` describes handing two
outputs to an independent fresh context that is not told which is which, followed by `<analyzer>` to
explain the result. Most changes do not need this; the human review loop is usually enough.
