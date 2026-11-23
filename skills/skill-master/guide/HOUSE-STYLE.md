# House style for skills

Read in Stage 2 and kept in context for Stage 3. Format-specific rules — the entry file's template,
metadata keys, naming, permissions, argument placeholder — live in `<format>`, not here. A repository's
own contribution rules outrank this file for skills that live in that repository (PROCEDURE.md
Stage 0).

## Gather the behaviour (Stage 2)

Six questions, one group. Announce `6 questions`, ask 1 as a structured choice (it has fixed options),
then list 2–6 as `[n/6]` plain text under `Need your input`, following "Asking the user" below:

1. **Verification** — is the output objectively checkable (a file transform, a created ticket, a fixed
   sequence of steps), or is it a judgement call (tone, layout, wording)? Stages 6–7 can measure checkable
   skills; for judgement skills they usually show little. Suggest the default, let the user decide.
2. **Trigger** — when should this fire? What will you actually type?
3. **Steps** — the main steps, in order.
4. **Tools** — which tools it needs: shell, file access, questions to the user, other skills, external
   services.
5. **Input** — does it take arguments, and in what shape?
6. **Output** — what it produces or displays at the end.

Wait for the answers, then decide the shape below and draft.

## Decide the shape before writing prose

A skill is a directory, not necessarily one file:

```
skill-name/
├── <entry file>      (required — metadata + instructions; `<format>` names it)
├── scripts/          (deterministic or repetitive work; runs without loading into context)
├── references/       (docs read on demand)
└── assets/           (templates, icons, fonts used in output)
```

Content loads in three levels, and that is what makes bundling worth it: **the name and description
are always in context, the entry file's body loads whenever the skill fires, and bundled files load only
when something reaches for them.** So push detail outward, and when the body starts carrying a lot, add
a layer of hierarchy with explicit pointers telling the model which file to read and when.

**Size is a budget, not a limit.** What a body earns depends on how many distinct modes and decisions
it serves — an eight-stage skill routing three modes legitimately needs more than a single-workflow one,
and a 200-line skill doing one thing may still be bloated. The working budget is ~300 lines or ~4,000
estimated tokens (roughly 13 tokens per line of dense instruction prose, so the two halves are one
figure rather than two tests). Past it nothing is wrong yet: state in one line near the top of the body
what complexity earns the extra length. If you cannot, the body is carrying something that belongs
behind a pointer.

Because the entry file loads in full on every trigger, its size cannot be amortised across modes the
way a bundled file's can — which makes the read-fraction test below the real check on body size. A
block serving one of three modes costs the other two on every run, whatever the line count says. A
bundled file past the same figure is a different concern: it wants a table of contents, for
navigability rather than cost.

The budget is stated here once and restated bare by the review checklist and the audit — change it
here, then search for the copies.

The test for what stays inline is **how often a rule fires**. Something that applies on every run, or
to every item the skill produces, belongs in the body. Something consulted once per run, or only when
the situation is unusual, belongs in a bundled file behind a pointer that names its trigger: "read X
when Y", never "see X for detail".

Extraction only pays when the bundled file goes unread. A file reached on nearly every run costs its
full size plus a read round trip, which is worse than leaving it inline — so estimate the fraction of
runs that will hit each pointer and keep anything above roughly half in the body. Split above that
fraction only for a reason other than tokens, such as keeping the body dense enough to be followed
reliably, and say so where the pointer sits. Three rules follow:

- **Decision criteria stay in the body.** Whatever decides which file to read cannot itself live in a
  bundled file, or the model must read the file to learn whether it needed to.
- **Do not extract below roughly 300 lines total.** A small skill split across files buys extra round
  trips and more chances to skip a step. Reaching the budget is what triggers extraction, not a target
  to aim at.
- **A bundled file that is mostly lookup data — a table, an enumeration, a field map — should be a
  script.** Reading the file costs all of it; a script that returns the matching rows costs the rows.

If a skill spans several variants — cloud providers, markets, frameworks, tools — put the shared
workflow in the entry file and one bundled file per variant, so only the relevant one gets read. Give
every variant file of one kind the same sections, so adding a variant is one new file plus one routing
entry.

## Naming

- Follow `<format>`'s naming rules. Name the skill for what invoking it does where that reads
  naturally — verb first, then what it acts on — or after the tool or domain it wraps.
- When updating, preserve the existing directory name and name field exactly. Never emit a `-v2`.

## Writing style

Numbered steps are the house convention — they make many skills feel like one system and they make a
diff reviewable. Keep them.

Inside a step, though, explain *why*, not just what. The model reading these instructions is capable
of judgement, and a step that explains its own purpose survives situations the author never
anticipated, where a bare imperative fails. If you find yourself writing ALWAYS or NEVER in capitals,
treat it as a signal that the reasoning has gone missing — state the reason instead, and the rule
usually follows on its own. Reserve hard MUSTs for things with real consequences, like a confirm gate
before a write.

Other rules that hold up:

- Prefer the imperative for actions. "Read the file", not "you should read the file".
- Steps must be numbered and unambiguous, and every cross-reference must point at a step that exists.
- Never ship a placeholder or a TODO.
- Reference the user's input with the one placeholder `<format>` defines, consistently.
- Ask questions the way "Asking the user" below describes.
- Write the skill general, not narrow to the examples that prompted it. A skill tuned to three
  examples is worthless on the fourth.
- Draft, then reread with fresh eyes and cut what does not add value. Length is a cost paid on
  every invocation.

## Asking the user

A question is only as good as how easily it can be answered. Any skill that asks more than a single
yes/no confirm writes these rules into its own body, because its body is all the model has at run
time:

- **Questions apart from information.** Only items that need a decision become questions. Findings the
  user merely needs to know go into the skill's output, not the question list, or the user has to hunt
  for what actually needs an answer.
- **Announce the size first**, in one line: `7 questions in 3 groups — requirements (4), design (1),
  tests (2).` An interview of unknown length feels endless.
- **Choices go through the structured-choice mechanism**: 2–4 options, the recommended one first and
  labelled "(Recommended)", each with a one-line consequence. Open-ended questions (a name, a path, how
  to reach a screen) follow as numbered plain text under the heading `Need your input`.
- **Number and label each question** `[n/N] Topic —` and keep it self-contained in two sentences:
  what was found, then the question. A dialog may hide earlier text.
- **One group per dialog, in dependency order**, within the mechanism's per-call limit (`<format>`
  names it), with the next group written only after the previous one is answered, so it builds on
  those decisions.
- **Close a group before the next.** A clear answer is resolved. A vague one gets a follow-up rather
  than an interpretation. A question back gets answered, then the original is asked again. New
  information triggers a fresh ask of any earlier answer it changes. Re-ask open questions labelled
  `(follow-up)` with their original numbers, and update the count out loud.

A single confirm gate ("Does this look right?") needs none of this.

## Defining output formats

Show the shape rather than describing it:

```markdown
## Report structure
Use this template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

## Examples

Concrete input/output pairs beat explanation:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## When to bundle a script

If the same helper keeps getting written from scratch on each invocation — a chart builder, a document
generator, a parser — write it once into `scripts/` and point the skill at it. This is the single
biggest lever on both speed and consistency, because a script produces the same result every time and
never has to be loaded into context to run.
