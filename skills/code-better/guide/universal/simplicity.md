# Simplicity

How code is shaped and named: size, functions, naming, comments, module layout.

## Size and shape
- Delete before you add.
- Duplication is cheaper than the wrong abstraction. Extract only when three or more
  call sites share behaviour *and* would change together.
- No configuration, parameters, or extension points for needs that do not exist yet.
- Depth over breadth: a module with a small interface and a deep implementation beats
  many thin layers that each add a name and nothing else.

## Functions
- One function, one purpose, one level of abstraction. If a name needs "and", split.
- Return early for guard conditions; keep the main path unindented.
- Prefer pure functions. Side effects live at the edges and are named for what they do.
- Arguments: few, in a stable order; group related ones into a single object when
  there are more than three.
- Choose clarity over brevity. Dense one-liners and nested ternaries cost more in
  reading time than they save in space. Wrap a complex inline expression — nested
  min/max, a compound conditional, a multi-step calculation — in one named variable
  describing the outcome.

## Naming
- Names describe the thing, not its type or implementation. `users`, not `userArray`;
  `retryDelay`, not `delayNumber`.
- Booleans read as questions: `isReady`, `hasAccess`, `canRetry`.
- Functions are verbs, values are nouns, and the same concept gets the same name
  everywhere in the codebase.
- No abbreviations unless they are universal (`id`, `url`, `html`).

## Comments
- Default to no comment. Add one only where a competent reader of this language would
  otherwise be left guessing; a correct, well-phrased comment on self-evident code is
  still noise to read and still rots.
- Explain *why*, never *what*. If the *what* needs a comment, rename or restructure.
- Record decisions and constraints that are invisible in code: workarounds, external
  requirements, deliberate deviations from a rule.
- A comment that earns its place is as short as its point allows: one idea, plain
  words, no repeating what a nearby comment already says and no contradicting one.
  Shortening a comment must not drop a constraint it was carrying.
- No commented-out code, no "TODO" without an owner or reference, no comments that
  merely repeat the function name.
- Describe the code as it stands, never the edit that produced it. No `now uses`,
  `added for`, `changed to`, `previously`; that history belongs in the commit message
  and is wrong the moment the code is touched again.
- Check any comment kept near edited code still matches what the code now does.

## Files and modules
- Group by feature or concept, not by technical kind, unless the project already does
  otherwise.
- Keep public surface minimal; export what is used elsewhere, nothing else.
