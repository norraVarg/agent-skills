# Design fidelity checklist

Used twice: in Step 3 to find what the requirement and design leave unsaid, and in Step 7 to verify
the running UI. Each item either has an answer in the requirement, the design or the code, or
becomes a question.

## States — every interactive element and every data-driven view

- Default, hover, focus-visible, active/pressed, disabled, read-only.
- Loading: initial load, refetch, submitting; skeleton vs spinner; does the layout shift?
- Empty: no data yet, filtered to nothing, first-time user.
- Error: field-level validation, form-level, network/server failure, partial failure, timeout,
  unauthorised/expired session. What copy, where, and how does the user recover?
- Success: confirmation, toast vs inline vs redirect; what happens to the form afterwards?
- Selected/checked/expanded/collapsed; first, middle, last item in a list.

## Layout and responsiveness

- Which breakpoints does the design cover, and what happens between them?
- What stacks, wraps, hides, or becomes scrollable at each breakpoint?
- Max/min widths, sticky elements, safe areas on mobile, behaviour with the virtual keyboard open.
- Spacing and sizing from tokens, not eyeballed pixel values.

## Content edge cases

- Long text: names, translations (German and Finnish run long), numbers with many digits — truncate,
  wrap, or tooltip?
- Short or missing text, missing images/avatars, zero/one/many items, very large lists.
- Currency, date, number and phone formatting per locale.
- Every string exists in every locale file; no hardcoded copy.

## Interaction and motion

- Click/tap targets at least 24x24 CSS px (WCAG 2.2 target size).
- Debounce, double-submit protection, optimistic updates, undo.
- Transitions and animations; respect `prefers-reduced-motion`.
- Navigation: back button, deep links, refresh mid-flow, leaving with unsaved changes.

## Accessibility (WCAG 2.2 AA)

- Semantic elements and roles; every input has a programmatic label.
- Logical focus order, visible focus, focus moved/returned correctly for modals and route changes.
- Everything works by keyboard alone; no keyboard traps.
- Errors announced (`aria-live` / `aria-describedby`), not shown by colour alone.
- Text contrast at least 4.5:1 (3:1 for large text and UI component boundaries).
- Images and icons have alt text or are marked decorative.

## Product wiring

- Analytics/tracking events: which, when, with what properties.
- Feature flag: name, default, behaviour in each flag state, cleanup plan.
- Permissions or locale, region or user-type variations of the screen.

## Verification (Step 7)

- Compare each state × viewport cell against its fidelity source (the design variant's "Fidelity
  source"), at the same viewport width.
- Check in this order, because earlier items cause later ones: layout and alignment, spacing,
  typography (family, size, weight, line height), colour and tokens, iconography, copy, states.
- When a screenshot difference is ambiguous, read the element's computed styles with browser
  automation (`getComputedStyle` in the page) and compare the values with the design.
- Tab through the screen once per viewport to confirm focus order and visible focus.
- Record each mismatch with the cell, the expected value from the design, and the actual value.
