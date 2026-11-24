# Scope variant — <name>

<!--
How to add a framework:
1. Copy this file to `scope/<framework>-<language>.md`, e.g. `scope/vue-ts.md` (lowercase,
   hyphenated).
2. Replace the heading and fill every section below. Keep the section names: the
   procedure reaches into variants by them.
3. Add one row for it to the variants table in `PROCEDURE.md`, Step 0, with the signal
   that selects it.
4. Remove this comment block.
Name tools, commands and file layouts here; name no agent tool — those belong in the
adapter.
-->

## Detect

<The signals that identify this framework and language: `package.json` dependencies, config
files, file extensions.>

## Implementation

<How code in this framework is written in an existing repo: following its component, state
and styling patterns, reusing the design system, typing data, keeping pure logic out of
components, i18n, accessibility from semantics first.>

## Component tests

<How component tests are written for this framework: the render helper, the query priority,
user-event simulation, waiting for async UI, what not to mock.>

## Pitfalls

<Framework behaviours that have caused real breakage.>
