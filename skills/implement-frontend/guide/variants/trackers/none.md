# Tracker variant — no tracker

## Detect

No issue key or issue URL. The requirement arrives as text in the request, as a design (Figma link
or screenshots) alone, or as a combination.

## Fetch

- Text: treat the request (minus design links and image paths) as the requirement. Quote it verbatim
  in the spec's Sources section — it is the only record of what was asked.
- Design only: the design is the requirement. Derive candidate acceptance criteria from what each
  frame or screenshot shows, and present them in Step 3 as questions to confirm — a picture shows
  layout, not behaviour, so every interaction, validation and error path needs the user's answer.

## Related items

None to fetch. Ask in Step 3 whether there is earlier work, a related page, or existing behaviour this
should match.

## Spec key

Propose a short kebab-case slug from the requirement (`checkout-address-form`) and confirm it.

## Pitfalls

- Thin requirements produce long question lists. That is expected — say so when announcing the count.
