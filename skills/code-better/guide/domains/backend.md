# Backend

Loaded when the file being edited runs on a server, in a function runtime, or as a
job. These rules hold across frameworks and runtimes.

## API contracts
- The contract (request and response shape, status codes, error format) is explicit
  and versioned. Changing it is a deliberate act with a compatibility plan.
- One consistent error format across the service: a machine-readable code, a
  human-readable message, and a correlation identifier. Never a stack trace.
- Use status codes for what they mean. A failed validation is a client error, not a
  server error and not a success with an error body.
- Endpoints are idempotent where the operation allows it; unsafe operations that may
  be retried accept an idempotency key.

## Validation and boundaries
- Every request is validated against a schema at the edge before any logic runs:
  shape, types, ranges, sizes. Unknown fields are rejected or stripped, never passed
  through.
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

## Reliability
- Every outbound call has a timeout, a bounded retry with backoff, and a decided
  behaviour when the dependency is down.
- Handlers are stateless between requests. Anything that must survive lives in a
  store, not in process memory.
- Background jobs are idempotent and safe to run twice; they record progress so a
  restart resumes rather than repeats.
- Resources (connections, files, handles) are released on every path, including
  failure.

## Observability
- Structured logging (key–value, not free text), with a correlation identifier that
  follows a request across services.
- Log at the boundary: what came in, what went out, how long it took, what failed.
  Not every function call.
- Never log secrets, credentials, tokens, or personal data. Redact at the logging
  layer, not by remembering to.
- Emit metrics for the things you would page on: error rate, latency, queue depth,
  dependency health.

## Security on the server
- Authenticate and authorise every entry point, including internal and
  administrative ones. Deny by default.
- Secrets come from the runtime's secret mechanism at start or on demand, never from
  code or committed configuration.
- Rate-limit authentication, password reset, and any expensive or abusable endpoint.
- Outbound requests to user-supplied destinations are checked against an allow-list.

## Configuration
- Configuration is read once at start, validated, and typed. A missing or invalid
  value fails start-up loudly rather than failing a request later.
- Environments differ by configuration only, never by code paths.
