# Runner variant — <name>

<!--
How to add a unit/component test runner:
1. Copy this file to `runners/<runner>.md`, e.g. `runners/mocha.md` (lowercase, hyphenated).
2. Replace the heading and fill every section below. Keep the section names: the
   procedure reaches into variants by them.
3. Add one row for it to the variants table in `PROCEDURE.md`, Step 0, with the signal
   that selects it.
4. Remove this comment block.
Name tools, commands and file layouts here; name no agent tool — those belong in the
adapter.
-->

## Detect

<The `package.json` dependency or config file that identifies this runner.>

## Find

<Where its config, setup files, render helper, fixtures and test files live, and how test
files are named.>

## Network mocking

<How tests mock the network with this runner, following the repo's existing tests.>

## Targeted run

<The exact command that runs only the given test files — never the full suite.>

## Pitfalls

<Runner behaviours that make tests fail for reasons unrelated to the code.>
