# Backend

Loaded when the file being edited runs on a server, in a function runtime, or as a
job. These rules hold across frameworks and runtimes.

## API contracts
- The contract (request and response shape, status codes, error format) is explicit
  and versioned. Changing it is a deliberate act with a compatibility plan.
- One consistent error format across the service: a machine-readable code, a
  human-readable message, and a correlation identifier. Never a stack trace.
- Use status codes for what they mean. A failed validation is a client error, not a
  server error and not a success with an error body. `403` versus `404` is chosen
  deliberately — the difference discloses whether the resource exists.
- Endpoints are idempotent where the operation allows it; unsafe operations that may
  be retried accept an idempotency key.

## Validation and boundaries
- Every request is validated against a schema at the edge before any logic runs:
  shape, types, ranges, sizes. Unknown fields are rejected or stripped, never passed
  through.
- Validate at the boundary even when a caller is internal. Internal callers change,
  and an assumption about who calls a function is not enforced by anything.
- Data leaving the service (responses, messages, logs) is shaped explicitly; never
  return an internal record as-is.

## Persistence
- Schema changes are migrations: versioned, forward-only, reversible where possible,
  and safe to run on a live system (add before remove, backfill before enforce).
- Every query is parameterised. Every query that can grow is paginated or bounded.
- Transactions wrap operations that must succeed or fail together, and are as short
  as possible. No calls to external services inside a transaction.
- Indexes exist for every access pattern the code relies on; a new query pattern
  comes with a look at the indexes.
- Watch for the N+1 pattern — a query inside a loop over query results. It passes
  every test on ten rows and fails in production on ten thousand.
- A migration that drops or rewrites data is irreversible in practice: confirm
  before applying it, and make it separately reviewable rather than folding it into
  a feature change.

## Reliability
- Every outbound call has a timeout, a bounded retry with backoff, and a decided
  behaviour when the dependency is down.
- Retry only what is safe to retry. Retrying a non-idempotent write duplicates it.
- Handlers are stateless between requests. Anything that must survive lives in a
  store, not in process memory.
- Background jobs are idempotent and safe to run twice; they record progress so a
  restart resumes rather than repeats.
- Handle poison messages explicitly, with a dead-letter path. A message that fails
  forever blocks the queue behind it.
- Resources (connections, files, handles) are released on every path, including
  failure.

## Observability
- Structured logging (key–value, not free text), with a correlation identifier that
  follows a request across services.
- Propagate to a central handler rather than catching in each handler. Per-endpoint
  error handling drifts until each endpoint reports failures differently.
- Log at the boundary: what came in, what went out, how long it took, what failed.
  Not every function call.
- Use the levels honestly: `error` for something needing attention, `warn` for
  something recoverable, `info` for events worth keeping. Everything logged at
  `error` means nothing is.
- Never log secrets, credentials, tokens, or personal data. Redact at the logging
  layer, not by remembering to — the same rule extends to error payloads returned
  to clients, which are easier to forget because they are not called logs.
- Emit metrics for the things you would page on: error rate, latency, queue depth,
  dependency health.

## Security on the server
- Authenticate and authorise every entry point, including internal and
  administrative ones. Deny by default.
- Authorise the specific resource, not just the route. Checking that the caller is
  authenticated says nothing about whether this record is theirs — that gap is the
  most commonly exploited access-control bug there is.
- Issue a new session identifier on login, and set cookies `HttpOnly`, `Secure`,
  and `SameSite=Strict`.
- Secrets come from the runtime's secret mechanism at start or on demand, never from
  code or committed configuration.
- Rate-limit authentication, password reset, and any expensive or abusable endpoint.
- Outbound requests to user-supplied destinations are checked against an allow-list.
- Turn off verbose errors and debug endpoints outside development. Set
  `Content-Security-Policy`, `Strict-Transport-Security`, and
  `X-Content-Type-Options`.

## Configuration
- Configuration is read once at start, validated, and typed. A missing or invalid
  value fails start-up loudly rather than failing a request later.
- Environments differ by configuration only, never by code paths.
