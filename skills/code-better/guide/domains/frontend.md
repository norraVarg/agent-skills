# Frontend

Loaded when the file being edited renders a user interface. These rules hold across
frameworks; rules that name a browser feature (elements, cookies, local storage,
code-splitting by route) apply only when the target is a browser. Framework-specific
rules, where needed, live below under a heading named after the framework.

## State
- Keep state as close as possible to where it is used. Lift it only when two
  components genuinely share it.
- One source of truth per piece of data. Derive, do not duplicate; compute values
  from state rather than storing copies that can drift.
- Server data and local UI state are different things. Keep them in separate
  mechanisms and never write server data into local state by hand.
- Custom hooks are the unit of reuse for stateful logic, not a base component.

## Rendering
- Every asynchronous view has explicit loading, empty, error, and success states.
  None of them is an afterthought.
- Components are pure with respect to their inputs: same props and state → same
  output. Side effects live in the framework's side-effect mechanism, with cleanup.
- Type props explicitly — they are the component's public contract, the same
  reasoning that puts return types on exported functions.
- Lists render with stable keys derived from the data, never from the index.
- Avoid layout shift: reserve space for content that arrives later.
- Wrap feature boundaries in an error boundary so one failing subtree does not take
  the page with it.

## Accessibility
- Semantic elements first (`button`, `nav`, `label`, headings in order). Add ARIA
  only where no semantic element exists.
- Every interactive element is reachable and operable by keyboard, with a visible
  focus state.
- Every image has alternative text; every form control has a label; colour is never
  the only carrier of meaning.
- Text and controls meet contrast requirements and remain usable at 200% zoom.

## Forms and input
- Validate on the client for feedback, on the server for truth. Never trust the
  client alone.
- Show errors next to the field, in plain language, after the user has finished
  with the field, not on every keystroke.
- Preserve user input on failure. Nothing typed is lost because a request failed.

## Network and errors
- Every request has a timeout and a user-visible outcome. Silent failure is not an
  option.
- Retries are bounded and idempotent; the user can see when something is retrying.
- Errors shown to users say what happened and what they can do; technical detail
  goes to logging, not to the screen.

## Security in the browser
- Never insert untrusted content as markup. Use text APIs; if markup is
  unavoidable, sanitise with a maintained library.
- Never store secrets or long-lived tokens in local storage. Prefer secure,
  same-site cookies managed by the server.
- Do not expose internal identifiers or error stacks in the UI.
- Nothing secret reaches the client bundle. Anything shipped to the browser is
  public, including values in environment variables inlined at build time.
- Authorization decisions belong on the server. Hiding a control in the UI is
  presentation, not access control — the underlying request is still reachable.

## Styling
- Follow the project's existing styling approach rather than introducing a second
  one; two competing systems cost more than either alone.
- Use the design tokens and shared constants the project already defines — colour,
  spacing, typography — so a token change propagates instead of needing a search.
- Responsive by construction: relative units, flex or grid, no fixed width that
  assumes a viewport.

## Performance and size
- Ship what is used: code-split by route, lazy-load below-the-fold content, avoid
  importing whole libraries for one function.
- Measure before optimising. Do not memoise or virtualise without a demonstrated
  need.
- Images are sized, compressed, and served in a modern format.

## Internationalisation
- No user-facing string is hard-coded when the project has a translation mechanism.
- Dates, numbers, and currencies are formatted with locale-aware APIs, never by hand.
- Layouts tolerate text that is twice as long, and right-to-left when the project
  supports it.
