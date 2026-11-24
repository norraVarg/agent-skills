# Testing strategy

Read in Step 4 to write the spec's test plan; applied in Steps 5 and 6 together with the runner, e2e
and scope variants, which hold the tool-specific mechanics. The repo's own conventions win over
anything here — copy the nearest existing test's structure, helpers and naming.

## Choosing the layer

| Layer | Use for |
| --- | --- |
| Unit | Pure functions: formatting, validation, mapping, reducers |
| Component / integration | Most behaviour: rendering per state, user interaction, API success and error handling, validation messages, accessible names and focus |
| E2E | The requirement's main user journey across pages, routing, auth, and real backend integration |

Most of the weight goes to component/integration tests — they are fast, test behaviour the way users
see it, and catch most regressions. E2E covers journeys, not every state; unit tests cover logic, not
rendering.

## Component and integration tests

- Mock the network, not the code under test: at the HTTP layer where the repo can (MSW or similar),
  otherwise at the API client module the way existing tests do.
- Cover each state in the spec's matrix that is reachable in a DOM-only environment; layout and pixel
  detail are left to the Step 7 fidelity pass, because jsdom-style environments have no layout engine.
- Assert accessibility basics: accessible names, errors linked to fields, focus after actions.

## E2E tests

Follow the e2e variant read in Step 2. The spec's test plan records which flows run against the real
backend and why each stub exists.

## Existing tests

- When an existing test fails because behaviour changed intentionally, update it and record it in the
  spec's test mapping against its AC — not in the test itself. When it fails for any other reason, it
  is a regression — fix the code, not the test.
- Delete a test only when the behaviour it covers is removed by the spec.
