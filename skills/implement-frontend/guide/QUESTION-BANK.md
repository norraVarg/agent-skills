# Question bank — definition of ready

Used in Step 3. Ask only what the requirement, design and code do not already answer, and say where
you looked. Group questions in this order.

## Requirements and behaviour

- What problem does this solve and for which user (locale or region, customer type, role)?
- Is each acceptance criterion testable as written? Rewrite vague ones ("should be user friendly")
  into observable behaviour and ask the user to confirm the rewrite.
- What triggers the feature, and what is the exit/next step in the flow?
- Which API endpoints are involved? Do they exist, and are request/response shapes confirmed? What
  do error responses look like?
- Validation rules: required fields, formats, limits, when validation runs (blur, change, submit).
- What happens on refresh, back navigation, session expiry, or a second tab?
- Does this change or remove existing behaviour? Who relies on the current behaviour?
- Feature flag, rollout, and locales or regions in scope; anything explicitly out of scope?
- Analytics events required?

## Design gaps

- Which states from the fidelity checklist have no frame or image in the design?
- Which breakpoints have no frame, and how should the layout behave there?
- Are design values on-token? If a value has no matching token, use the nearest token or the literal?
- Does the design use a library component, or a version of it the library does not have?
- Copy: is the design text final, and does it exist in every translation file?
- Contradictions between the design, the requirement and current production UI — which wins?
- Unresolved designer comments or notes.

## Test approach

- Which existing tests will change because behaviour changes intentionally?
- For e2e: can this flow run against the real backend (test env or local), and with what test data
  or user? If not, which calls must be stubbed and why?
- If the repo has no e2e framework: add tooling, or cover with extra integration tests?
- Any flow that needs a specific locale, flag state or user type set up for tests?
