# E2E variant — Playwright Test

## Detect

`@playwright/test` in `package.json` dependencies or devDependencies.

## Find

`playwright.config.*` (`testDir`, `use.baseURL`, `projects` for browsers and viewports, `webServer`
that starts the app, `retries`), the spec folder, fixtures (`test.extend`), page objects, auth setup
(`storageState`, setup projects), and the `package.json` scripts.

## Real backend vs mocked

- Real backend first — the only layer that catches contract drift between frontend and API. Use the
  environment the existing specs use, and create test data the way they do (API calls in fixtures or
  setup projects).
- Stub with `page.route(url, route => route.fulfill({ status, json }))` only for what cannot be real:
  third-party services, server errors and timeouts, data that cannot be seeded. Record why in the spec.
- Wait on `page.waitForResponse(...)` or web-first assertions (`await expect(locator).toBeVisible()`),
  never `page.waitForTimeout`.

## Selectors

`getByRole`, `getByLabel`, `getByText` first; `getByTestId` (with the repo's `testIdAttribute`) when no
accessible locator is stable. Never CSS classes.

## Targeted run

`npx playwright test <file> [--project=<name>]`. `webServer` in the config starts the app; ask before
running against a shared environment.

## Pitfalls

- Each test gets a fresh context; share login through `storageState`, not test order.
- Credentials belong in environment variables or the CI secret store, never in specs or config.
