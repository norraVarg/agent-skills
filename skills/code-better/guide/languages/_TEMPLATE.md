# <Language name>

<!--
How to add a language:
1. Copy this file to `languages/<language-name>.md` (lowercase, hyphenated).
2. Replace the heading and fill the sections below. Delete sections that do not
   apply; add sections only for concerns unique to this language.
3. Add one row to the Language table in `PROCEDURE.md` Step 1 with the manifest
   files and file extensions that identify this language.
4. Remove this comment block.
Rules here must not contradict `universal/` or `domains/`. Keep to what is specific
to the language: its type system, error model, concurrency model, module system,
idioms, and tooling. General principles already live in `universal/`.
-->

Loaded when the file being edited is <extensions>.

## Project tooling comes first
- <The formatter, linter, and type-checker the project already uses; the package or
  build tool detected from its lockfile or manifest. Never introduce a second one.>

## Types and data
- <How to model data safely in this language; what to avoid.>

## Errors
- <The language's error model and how to use it: exceptions, result types, error
  values.>

## Concurrency and asynchrony
- <The language's concurrency primitives and the rules for using them.>

## Modules and dependencies
- <Import conventions, visibility, and how dependencies are declared.>

## Idioms
- <Constructs to prefer and constructs to avoid, with one-line reasons.>

## Tests
- <The runner and layout the project uses; how to detect them; naming.>
