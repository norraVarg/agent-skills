# Runner variant — Vitest

## Detect

`vitest` in `package.json` dependencies or devDependencies.

## Find

- Config: the `test:` block in `vite.config.ts` or `vitest.config.ts` — environment (`jsdom` or
  `happy-dom`), `globals`, `setupFiles`, include patterns, aliases.
- Setup file (`setupFiles`): jest-dom matchers, MSW server start, browser API mocks.
- Test naming and location from existing files (`*.spec.tsx` vs `*.test.tsx`, colocated vs `__tests__/`
  vs a top-level `tests/`) — follow what the touched area does.
- The custom render helper and fixtures, usually under `src/tests/`, `tests/utils/` or `test-utils.tsx`.

## Network mocking

If MSW is present, reuse its handlers file and override per test with `server.use(...)` for error and
edge responses. Without MSW, mock at the API client module with `vi.mock`, the way existing tests in
the area do. Use `vi.fn`, `vi.spyOn`, `vi.useFakeTimers` for the rest.

## Targeted run

`npx vitest run <file> [<file> ...]`, or the repo's test script with file arguments if it adds flags
(check `package.json`). Never run without file arguments — that is the full suite.

## Pitfalls

- `globals: false` means `describe`/`it`/`expect` must be imported from `vitest`.
- Module mocks with `vi.mock` are hoisted; variables they use must be defined with `vi.hoisted`.
