# Principles

The core that applies to every language and every domain. Always in context.

## Scope of a change
- Make the smallest change that fully solves the request. Nothing speculative, nothing
  "while I am here".
- Match the surrounding code: naming, structure, formatting, error style. Consistency
  beats personal preference.
- Do not reformat, reorder, or rename code you were not asked to change.

## Correctness
- Handle the failure path with the same care as the success path. No silent failures,
  no swallowed errors, no defaults that hide a problem.
- Validate at boundaries (user input, network, files, environment) and trust inside.
- Prefer immutable data and pure functions where the language allows.
- Make operations idempotent when they can be retried.
- Make illegal states unrepresentable rather than documenting that they are illegal.
  A constraint the type system enforces cannot rot; a comment saying the same thing
  can.

## Simplicity
- Prefer the obvious solution over the clever one. Three similar lines beat a premature
  abstraction.
- One function, one purpose. If describing it needs "and", split it.
- Name things for what they are, not how they are implemented. No abbreviations unless
  universally known.
- Comment the *why* when it is not evident from the code; never restate the *what*.

## Security
- Never hard-code secrets. Never log them. Never put them in URLs.
- Treat all external input as hostile until validated.
- Use the platform's or library's safe API (parameterised queries, escaping helpers)
  rather than building strings by hand.

## Testing
- Tests follow behaviour, not implementation. A refactor that keeps behaviour must not
  break tests.
- Every bug fix comes with a test that fails before the fix and passes after.
- No production code path exists only to make tests pass.

## Dependencies and tooling
- Prefer the standard library. Add a dependency only when it removes real complexity,
  and prefer well-maintained ones.
- Respect the project's linter, formatter, and type-checker configuration. Never disable
  a rule to make a change pass; fix the cause or explain why the rule is wrong.
- Write code already formatted to the project's rules; do not rely on a later
  formatting pass that may not happen.
