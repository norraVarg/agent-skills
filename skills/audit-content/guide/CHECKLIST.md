# Checklist

Five categories, checked in this order — covering content that is unused,
irrelevant, unnecessary, redundant, repeated, conflicting, misleading, wrong,
unclear, or written in a way that's hard for a human reader to follow.
`rules/user-rules.md` applies on top of all of them, with the highest precedence.

## Unused, irrelevant, unnecessary

Content that does not serve what the document is trying to do: a leftover placeholder, a
tangent, a caveat nobody asked for, a paragraph explaining something the reader already
knows from context.

- Avoid: a Jira ticket description that spends a paragraph restating the epic it belongs
  to before saying anything about the ticket itself.
- Flag any sentence, bullet, or section that could be deleted without losing information
  the reader needs.
- Avoid: content under a heading that isn't actually about what the heading promises, or
  that contradicts it — check each section against its own heading, not only the
  document as a whole. The mismatch could mean the content is misplaced, or that the
  heading itself is wrong; flag it without assuming which.
- Avoid: content aimed at a different audience than the document actually serves — a
  user-facing document carrying contributor or implementation detail, or the reverse.
  Accurate, well-written content can still not belong, because it's answering a
  question this document's actual reader never asked.

## Redundant, repeated

The same point made more than once, in the same words or different ones. Includes
elegant variation (cycling synonyms for the same thing instead of just naming it once)
and padding sentences that restate what was already said. On a set of documents it also
covers the same point made in two different files, where the question is not only
whether it repeats but whether the repetition was meant and whether the copies still
agree.

- Avoid: calling the same entity "the lender," then "the applicant," then "the
  financing seeker" in three consecutive sentences — name it once and keep using that
  name.
- Avoid: a closing paragraph that just repeats the opening in different words.
- Across a set of documents, the same claim or rule in two places is not automatically a
  defect. Establish first whether the duplication is deliberate — a digest, index,
  summary, or quick-reference layer over a fuller one.
- Deliberate duplication changes what the finding is: check that the relationship is
  stated where a reader will see it, and that the copies still agree. Report a copy that
  has fallen behind its source as drift, and prefer declaring the relationship over
  deleting either copy.

## Conflicting

Two statements in the same piece of content that cannot both be true, or that give
contradictory instructions.

- Example: a ticket's acceptance criteria says "must support both email and SMS," while
  an earlier paragraph says "email only for this phase."

## Misleading, wrong

A claim the content itself does not support: an absolute statement ("this fixes X,"
"this ensures Y") with nothing in the content backing it up, a vague attribution ("teams
generally agree"), or a claim that contradicts something else stated as fact in the same
content.

- An absolute claim needs a reason, a mechanism, or a citation present in the content
  itself. If none is there, flag it — do not assume it is true, and do not verify it
  against outside sources; that is out of scope for this pass (`PROCEDURE.md`, step 3).
- A hedge with no content is also a smell: "this should probably work in most cases"
  says nothing verifiable.

## Unclear, poorly worded

Wording that makes a competent reader work harder than the content warrants: a buried
lead, multiple ideas chained into one sentence, walls of text, inconsistent structure
across parallel sections, unexplained abbreviations or jargon.

- Front-load the point: the most important fact should not be the last sentence of a
  paragraph.
- One idea per sentence: split sentences chained together with "and," "but," or "which"
  if they are really two separate points.
- Break up any block of prose that runs past a natural reading pause without a paragraph
  break or a list.
- List three or more items as bullets, not comma-separated prose.
- Keep parallel sections in parallel form; do not mix prose and bullets arbitrarily for
  sections that are otherwise doing the same job.
- Spell out abbreviations that are not widely known.
