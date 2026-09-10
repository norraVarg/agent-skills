# Simplicity

Loaded when a change adds structure: new functions, modules, abstractions, or names.

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

## Naming
- Names describe the thing, not its type or implementation. `users`, not `userArray`;
  `retryDelay`, not `delayNumber`.
- Booleans read as questions: `isReady`, `hasAccess`, `canRetry`.
- Functions are verbs, values are nouns, and the same concept gets the same name
  everywhere in the codebase.
- No abbreviations unless they are universal (`id`, `url`, `html`).

## Comments
- Explain *why*, never *what*. If the *what* needs a comment, rename or restructure.
- Record decisions and constraints that are invisible in code: workarounds, external
  requirements, deliberate deviations from a rule.
- No commented-out code, no "TODO" without an owner or reference, no comments that
  merely repeat the function name.

## Files and modules
- Group by feature or concept, not by technical kind, unless the project already does
  otherwise.
- Keep public surface minimal; export what is used elsewhere, nothing else.
