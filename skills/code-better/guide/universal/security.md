# Security

Input, output, secrets, authentication, external calls, and dependencies.

## Input
- All external input is hostile until validated: user data, query strings, headers,
  files, environment variables, third-party responses.
- Validate with an allow-list (what is permitted), not a deny-list (what is blocked).
- Enforce size limits on every input that is stored or processed.

## Output and injection
- Never build queries, commands, paths, or markup by concatenating input. Use
  parameterised queries, argument arrays, path-joining APIs, and context-aware escaping.
- Encode output for the context it lands in (HTML, attribute, URL, shell, SQL).
- Path input is normalised and checked to stay inside the intended directory.

## Secrets
- Never in code, configuration files committed to version control, logs, error
  messages, or URLs. Load from a secret store or the runtime's secret mechanism.
- Rotate on suspicion. Design so rotation needs no code change.

## Authentication and authorisation
- Deny by default. Every entry point checks both *who* the caller is and *whether*
  they may do this to this resource.
- Sessions and tokens: short-lived, revocable, regenerated on privilege change.
- Passwords are hashed with a slow, salted algorithm designed for passwords; never
  with a general-purpose hash.

## External calls
- Requests to user-supplied destinations are checked against an allow-list of hosts.
- Every outbound call has a timeout and a bounded retry.
- Use encrypted transport by default; do not disable certificate verification.

## Dependencies
- Pin versions. Review what a new dependency pulls in. Run the project's audit tool
  when adding or upgrading.
- Do not deserialise untrusted data with mechanisms that can execute code.
