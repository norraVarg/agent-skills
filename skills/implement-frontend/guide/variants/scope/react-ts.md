# Scope variant — React + TypeScript

## Detect

`package.json` depends on `react` and `typescript` (or has a `tsconfig.json`), and the touched code is
`.tsx`/`.ts`.

## Implementation

- Follow the repo's existing patterns for components, hooks, state (Redux, Zustand, React Query,
  context) and styling (CSS modules, styled-components, Tailwind, the design system's props) — match
  the nearest similar component rather than introducing a new pattern.
- Extend design-system components through props or composition, not by copying their source.
- Type props and API responses explicitly; no `any`. Derive types from existing API types or schemas
  where the repo has them.
- Keep logic that can be pure (formatting, validation, mapping) out of components, so it gets unit
  tests of its own.
- Use the repo's i18n API for every user-visible string; add keys to every locale file the repo has.
- Accessibility comes from semantics first: native elements, labels tied to inputs, ARIA only where
  no native element fits.

## Component tests

- Render with the repo's custom render helper (it wraps providers such as store, router, i18n,
  theme), never bare `render`, or providers silently go missing.
- Query by what the user perceives, in this order: `getByRole` (with `name`), `getByLabelText`,
  `getByPlaceholderText`, `getByText`, then `getByTestId` as the last resort.
- Use `userEvent` (with `setup()`), not `fireEvent`, so focus and keyboard behave like a browser.
- Use `findBy*` / `waitFor` for async UI; never fixed sleeps.
- Do not mock the component's own hooks or child components unless existing tests in that area do —
  that tests implementation, not behaviour.

## Pitfalls

- `act(...)` warnings mean an update happened after the test stopped waiting — await the UI change
  instead of silencing the warning.
- Strict-mode double effects in development can hide or create bugs that tests do not show.
