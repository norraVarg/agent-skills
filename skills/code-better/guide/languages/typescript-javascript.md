# TypeScript and JavaScript

Loaded for `.ts` `.tsx` `.mts` `.cts` `.d.ts` `.js` `.jsx` `.mjs` `.cjs` files and the
script blocks of `.vue` `.svelte` `.astro` files. Rules marked **TS** apply to TypeScript
files only; a `.js` file in a TypeScript project follows the remaining rules.
Browser-specific and server-specific concerns live in `domains/`; framework-specific rules
live in the domain file under the framework's heading.

## Project tooling comes first
- Respect the project's `tsconfig`, ESLint, and Prettier configuration exactly. Never
  add a disable comment or loosen a compiler option to make a change pass.
- Use the project's package manager (detect from the lockfile) and its existing
  scripts. Do not introduce a second one.
- Match the module system the project uses (ESM or CommonJS). Do not mix.

## Types (TS)
- `unknown` at boundaries, never `any`. Narrow with type guards before use.
- No non-null assertions (`!`) and no type assertions (`as`) without a comment that
  says why the compiler cannot know. Prefer a guard or a redesign.
- Model alternatives as discriminated unions with a literal `kind` or `type` field,
  not as boolean flags or optional fields that are "sometimes present".
- `switch` over a union is exhaustive; the `default` branch asserts `never`.
- Prefer `readonly` properties and `ReadonlyArray`; use `as const` for literal
  tables.
- Derive types from a single source (`typeof`, `ReturnType`, schema inference)
  rather than writing the same shape twice.
- Public function signatures declare their types explicitly; local variables let
  inference work.
- No `enum`; use a union of string literals or an `as const` object.

## Asynchrony
- `async`/`await` over raw promise chains. Never mix the two in one function.
- No floating promises: every promise is awaited, returned, or explicitly handled.
- Independent asynchronous work runs concurrently (`Promise.all`, or `allSettled`
  when partial failure is acceptable), not in a sequential loop.
- Errors from `await` are handled where they can be acted on; do not wrap every
  call in `try`/`catch` only to rethrow.
- Every external call has a timeout (an `AbortSignal` or the client's timeout
  option).

## Errors
- Throw `Error` (or a subclass), never a string or a plain object. Include a
  message that states what failed and with what input.
- Custom error classes carry a stable machine-readable `code` so callers can branch
  on it without parsing messages.
- `catch (error)` treats `error` as `unknown` and narrows before reading properties.
- When rethrowing as a different error, preserve the original via `{ cause: err }`
  so the stack does not stop at the rethrow.

## Modules and imports
- `import type` for type-only imports.
- No barrel files (`index.ts` re-exporting everything) that create import cycles or
  pull in unused modules.
- Prefer named exports. A default export only when the framework requires it.
- Node built-ins are imported with the `node:` prefix.

## Data and functions
- `const` by default; `let` only when reassignment is needed; never `var`.
- Strict equality (`===`) always.
- Prefer `map`/`filter`/`reduce` and `for…of` over index loops; never mutate the
  array being iterated.
- Optional chaining and nullish coalescing (`?.`, `??`) instead of manual null
  checks; `??` rather than `||` when `0` or `""` are valid values. `?.` is for a
  value that is legitimately absent — using it to skip an operation that could fail
  hides an error instead of handling it.
- Objects are not mutated after creation; produce a new object with spread.
- Dates are handled with a single library or the `Intl` and `Temporal` APIs; never
  arithmetic on milliseconds by hand for calendar concepts.

## Runtime and environment (Node)
- Environment variables are read once at start, validated with a schema, and
  exposed as a typed configuration object. No `process.env` access elsewhere.
- Never use `eval`, `new Function`, or dynamic `require` with user input.
- File paths are built with `path.join`/`path.resolve` and checked to stay inside
  the intended directory.

## Tests
- Use the project's runner (Jest, Vitest, or node:test — detect, do not choose).
- Test files sit where the project puts them (`*.test.ts` beside the source, or
  `__tests__/`), named after the module under test.
- Replace external boundaries (network, filesystem, clock, database) with the runner's
  mocking mechanism at the module that wraps them; do not mock internal modules or reach
  into implementation internals.
- Type-check test files with the same strictness as source.
