# Making changes

The scope of an edit, and the project it lands in.

## Scope of a change
- Make the smallest change that fully solves the request. Nothing speculative, nothing
  "while I am here".
- Match the surrounding code: naming, structure, formatting, error style. Consistency
  beats personal preference.
- Matching a convention is not endorsing it. When the surrounding pattern has a real
  drawback — not merely differing from this guide — say what the drawback is and let
  the developer decide, rather than propagating it silently in one more file.
- Do not reformat, reorder, or rename code you were not asked to change.

## Dependencies and tooling
- Prefer the standard library. Add a dependency only when it removes real complexity,
  and prefer well-maintained ones.
- Respect the project's linter, formatter, and type-checker configuration. Never disable
  a rule to make a change pass; fix the cause or explain why the rule is wrong.
- Write code already formatted to the project's rules; do not rely on a later
  formatting pass that may not happen.
