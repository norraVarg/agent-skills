# Stage 7 — tuning a description so the skill actually fires

Run when the user asks, or when a skill demonstrably fails to fire on prompts it should own. Needs the
evaluation harness; `<review-page>` and `<tuning-loop>` below are its files and commands, listed in
`<format>`'s "Evaluation harness" section.

## How triggering works

An agent sees each skill as its name plus description, and that pair is the whole basis for deciding
whether to consult it. Two consequences shape the eval queries:

- An agent only reaches for a skill on tasks it cannot comfortably handle alone. A one-step prompt like
  "read this file" will not trigger a skill however well the description matches, so such prompts are
  useless as test cases.
- Descriptions compete. In a large collection of skills in overlapping territory, the realistic failure
  is not vague wording but two descriptions both claiming the same phrase.

## Step 1 — Build the eval set

20 queries, roughly half should-trigger and half should-not:

```json
[
  { "query": "the user prompt", "should_trigger": true },
  { "query": "another prompt", "should_trigger": false }
]
```

Queries must read like something actually typed — file paths, names, column names, a bit of backstory,
occasional lowercase and typos, varied length. Aim at edge cases rather than obvious ones.

Bad: `"Format this data"`, `"Create a chart"`

Good: `"ok so my manager just sent me this xlsx file (its in my downloads, called something like 'Q4
sales final FINAL v2.xlsx') and wants a column showing profit margin as a percentage. revenue is column C
and costs are column D i think"`

**For the 8–10 should-trigger queries:** cover different phrasings of the same intent, formal and
casual. Include cases where the user never names the skill or the file type but clearly needs it, some
uncommon uses, and some where this skill competes with another and should win.

**For the 8–10 should-not-trigger queries, draw them from the user's other skills.** Generic negatives
("write a fibonacci function") test nothing. Real negatives are the near-misses: read the descriptions
of every other skill in `<skills-root>`, take the phrases neighbouring skills claim, and write queries
that sit just on their side of the line — a general code-review skill against a language-specific
review skill, a commit skill against a commit-message checker. If a negative query would plausibly fool
a keyword matcher, it is a good negative.

## Step 2 — Review with the user

Bad queries produce a bad description, so this review is not a formality. Fill `<review-page>` with the
eval set, the skill's name and its current description, open it for the user, and let them edit
queries, toggle should-trigger, and add or remove entries. They export the edited set; take the newest
export if there are several.

## Step 3 — Run the loop

Tell the user this takes a while and runs in the background, then start `<tuning-loop>` with the eval
set, the skill's path, at most five iterations, and the model that powers the current session — so the
measured triggering matches what the user experiences rather than another model's behaviour.

The loop splits the set 60% train / 40% held-out test, runs each query three times to get a stable
trigger rate rather than a single noisy sample, proposes a better description based on what failed, and
re-evaluates on both splits. It selects the best description by the held-out score, not the training
score — which stops it producing a description tuned to the exact queries it optimized against.

Check the output periodically and tell the user which iteration it is on and how the scores are moving.

## Step 4 — Apply

Take the best description from the loop's output, show the user before and after with both scores, and
apply it through the normal confirm gate.

Two things to check before accepting it, because the optimizer only knows about the one skill it was
given:

- **Re-check overlap.** An optimized description often broadens to catch more true positives, which can
  put it back in conflict with a neighbouring skill that was not part of this eval set.
- **Keep the trigger phrases the user relies on by habit.** If they type "fix the skill" out of habit
  and the optimizer dropped that phrasing, add it back and note the small score cost.
