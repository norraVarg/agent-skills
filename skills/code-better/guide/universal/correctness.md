# Correctness

Failure paths, boundaries, state, concurrency, and data flow.

## Failure paths
- Every operation that can fail has a decided outcome: propagate, recover, or report.
  "Ignore" is not an outcome.
- Fail fast and loud at the point of detection. A wrong value that travels far is
  harder to debug than an early exception.
- Catch exceptions only where you can do something meaningful; otherwise let them
  propagate. Never catch-and-continue without logging *and* a reason in a comment.
- Catch narrowly. Before writing a broad catch, name the unrelated errors it would
  also swallow — if that list is non-empty, narrow it or let them propagate.
- Never fall back to a mock, stub, or fake outside test code.
- Error messages say what went wrong, with which input, and what was expected.
  They never include secrets.

## Boundaries
- Validate shape, type, and range of data at the boundary where it enters (request
  body, file, environment, third-party response). Inside the boundary, trust the types.
- Convert external representations (strings, JSON) to internal ones once, at the
  boundary, not repeatedly through the code.

## State and data
- Make illegal states unrepresentable rather than documenting that they are illegal. A
  constraint the type system enforces cannot rot; a comment saying the same thing can.
- Do not expose mutable internals and then rely on callers to preserve an invariant.
- Prefer immutable values. Return new data instead of mutating arguments.
- Do not share mutable state between units that run concurrently without a clear
  ownership rule.
- Operations that may be retried (network calls, jobs, handlers) must be idempotent:
  running twice produces the same result as running once.
- Time, randomness, and identifiers are injected, not read from globals, so that code
  is testable and results are reproducible.

## Edge cases to check before finishing
- Empty input, single element, maximum size.
- Null, undefined, missing keys, wrong type from an external source.
- Concurrent execution, partial failure, timeout.
- Unicode, time zones, leap days, floating-point comparison — whenever the domain
  involves text, time, or money.
