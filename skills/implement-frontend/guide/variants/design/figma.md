# Design variant — Figma

## Detect

A `figma.com/design/...`, `figma.com/file/...` or `figma.com/make/...` URL in the request or the issue.
Parse `fileKey` and `node-id` from the URL (convert `-` to `:` in the node ID; for
`/design/<fileKey>/branch/<branchKey>/` use the branch key).

## Fetch

1. If the platform provides Figma's own design-to-code guidance (the adapter names it), load it before
   reading design context. It defines how to adapt Figma's generated code to the repo instead of
   pasting it.
2. Open a session on the file, if the platform's Figma access needs one, with the file key and a
   one-line task description.
3. For each node read: the design context (structure and styles, a reference to adapt, not final
   code), a screenshot (the visual truth), the metadata (to find sibling frames for other states and
   breakpoints), the variable definitions (tokens), and the comments (designer notes, often unresolved
   decisions).
4. Without design tool access, use Step 0's fallback.

## Tokens and states

Map every colour, spacing, radius and type value to a design-system token via the variable
definitions. A value with no matching token is a Step 3 question (nearest token, or the literal?).
Look for component variants and sibling frames for each state in the fidelity checklist; a state with
no frame is a question.

## Fidelity source

The screenshot of the frame matching each state × viewport cell, compared at the frame's own width.

## Pitfalls

- Frames are often drawn at one width only; behaviour between breakpoints must be asked, not inferred.
- Figma text may be placeholder copy — confirm it is final before adding translations.
