# Testing

Loaded when a change adds, modifies, or should be accompanied by tests.

## What to test
- Behaviour visible to the caller: inputs → outputs, side effects, errors raised.
  Not private helpers, not implementation details.
- Every branch that matters: the success path, each failure path, and the edge cases
  listed in `correctness.md`.
- Do not test the framework, the language, or the library. Test your code.

## Structure
- One behaviour per test. The name states the scenario and the expected result:
  `returns empty list when no items match`.
- Arrange, act, assert — visually separated, in that order, with one assertion
  concept per test.
- Tests are independent: no shared mutable state, no order dependence, no reliance
  on wall-clock time or real network unless the test is explicitly an integration test.

## Test doubles
- Fake the boundary (network, filesystem, clock, database), not the code under test.
- Prefer simple hand-written fakes over deep mocking frameworks when the interface is
  small.
- A test that mirrors the implementation line by line tests nothing; if the
  implementation changes and behaviour does not, the test must still pass.

## Test code quality
- Same standards as production code: clear names, no duplication that hides intent,
  no dead tests, no skipped tests without a linked reason.
- When code needs a hook for testing, inject the dependency instead of adding a
  test-only code path.
- Follow the project's existing test layout, runner, and naming. Do not introduce a
  second test framework.
