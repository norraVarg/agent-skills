# Runner variant — Jest

## Detect

`jest` in `package.json` dependencies or devDependencies (also via `react-scripts`, which bundles it).

## Find

- Config: `jest.config.*` or the `jest` key in `package.json` — `testEnvironment` (must be `jsdom` for
  components), `setupFilesAfterEnv`, `moduleNameMapper` (path aliases, CSS and
  asset stubs), `transform` (babel-jest, ts-jest or swc).
- Setup file: jest-dom matchers, MSW server start, browser API mocks.
- Test naming and location from existing files — follow what the touched area does.
- The custom render helper and fixtures.

## Network mocking

If MSW is present, reuse its handlers and override per test with `server.use(...)`. Without MSW, mock
the API client module with `jest.mock`, the way existing tests in the area do. Use `jest.fn`,
`jest.spyOn`, `jest.useFakeTimers` for the rest.

## Targeted run

`npx jest <file> [<file> ...]`, or `npm test -- <file>` for CRA (`react-scripts test` watches by
default — add `--watchAll=false`). Never run without file arguments — that is the full suite.

## Pitfalls

- ESM-only dependencies need `transformIgnorePatterns` exceptions; a syntax error in `node_modules` is
  config, not the test.
- MSW v2 under Jest needs the `undici`/fetch polyfills the repo's setup file provides — reuse it.
