# E2E variant — Cypress

## Detect

`cypress` in `package.json` dependencies or devDependencies.

## Find

`cypress.config.*` (baseUrl, specPattern, env, viewport, retries), the spec folder (`cypress/e2e/`),
support files (`cypress/support/` commands, global hooks), page objects or helpers, fixtures, and the
`package.json` scripts that start the app and Cypress for each environment.

## Real backend vs mocked

- Real backend first — the only layer that catches contract drift between frontend and API. Use the
  environment the existing specs use (a test/staging environment or a local backend), and create test
  data the way they do.
- Stub with `cy.intercept(method, url, { fixture | body | statusCode })` only for what cannot be real:
  third-party services, server errors and timeouts, data that cannot be seeded. Record why in the spec.
- Use `cy.intercept` without a response just to alias and wait: `cy.wait('@alias')`, never fixed
  `cy.wait(ms)`.

## Selectors

The repo's convention (often `data-cy` or `data-testid`, sometimes via shared constants), then
accessible text and roles. Never CSS classes.

## Targeted run

`npx cypress run --spec <file>[,<file>]`, through the repo's script if it starts the app first (check
`package.json`). Ask before running against a shared environment.

## Pitfalls

- Specs must not depend on each other's state; reset in `beforeEach`, the way the support file does.
- Credentials belong in environment variables or the CI secret store, never in specs, fixtures or
  `cypress.config.*`; flag any you find.
