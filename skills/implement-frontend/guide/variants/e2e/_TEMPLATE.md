# E2E variant — <name>

<!--
How to add an end-to-end framework:
1. Copy this file to `e2e/<framework>.md`, e.g. `e2e/webdriverio.md` (lowercase,
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

<The `package.json` dependency or config file that identifies this framework.>

## Find

<Its config, spec folder, helpers or page objects, fixtures, auth setup and the scripts that
start the app.>

## Real backend vs mocked

<How to run against the real backend first, and how to stub only what cannot be real,
recording why.>

## Selectors

<The selector order to use with this framework, following the repo's convention.>

## Targeted run

<The exact command that runs only the given spec files, and when to ask before running
against a shared environment.>

## Pitfalls

<Framework behaviours that cause flaky or order-dependent tests.>
