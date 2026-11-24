# Design variant — images and screenshots

## Detect

Image paths (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`) in the request, images pasted into the
conversation, or images attached to the issue.

## Fetch

Read each image. For each, note which screen, state and approximate viewport it shows; ask in Step 3
when that is not obvious. Images pasted into the conversation may not survive a resumed session —
copy their paths into the spec's Sources section, and ask the user to save pasted ones to disk if
needed.

## Tokens and states

Images carry no token values. Match what you see to the design system's existing tokens and
components, and list every value you could not match as a Step 3 question rather than eyeballing a
pixel value. Every state without an image is a question.

## Fidelity source

The image matching each state × viewport cell. Compare layout, hierarchy, alignment, copy and
relative spacing; exact pixel values are approximate because screenshots may be scaled — say so in
the report.

## Pitfalls

- Screenshots of an existing app show current behaviour, not necessarily the desired one — ask which.
