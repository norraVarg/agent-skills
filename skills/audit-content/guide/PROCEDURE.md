# Audit content procedure

This is the whole procedure for auditing a piece of content for a human reader. It is
written for any agent to follow, on any platform: it names no specific tool, because no
specific tool exists on every platform. Each provider's entry point
(`adapters/<provider>/`) tells you what concretely fulfils the capabilities named in
step 0, on that platform. Everything else below is identical everywhere.

## Step 0 — Detect capabilities

Before anything else, establish what you actually have to work with:

- **A way to ask and wait.** Something that can put a question to the user and get their
  answer back before continuing — needed to disambiguate the target (step 1) and to
  confirm before applying any fix (step 5).
- **A structured reporting mechanism.** A way to present findings as discrete, itemised
  results rather than only prose. Optional — falls back to a clearly labelled plain list.
- **A diff or preview mechanism.** A way to show a proposed edit against the original
  before it is applied. Optional — falls back to showing the before and after text
  inline.

If a capability is unclear or unavailable, proceed as if it does not exist and say so in
the report; do not silently skip the step it enables.

## Step 1 — Identify the target

- If the user's own words already name, paste, or link the content, that is the target.
- A target may be one document or a set of related documents read as one body of work —
  a directory, a skill, a guide. When the user names the set, the set is the target; do
  not silently narrow it to the one file that looks most relevant.
- When the target is a single document, check whether it belongs to a set before
  auditing it alone: the other files its parent document loads alongside it, a summary
  or index that covers it, a template it was copied from, the siblings a single reader
  reads as a unit. If any exist, name them and ask whether to widen the target. Widen
  only on a yes, and propose the smallest set that genuinely shares the purpose.
- Otherwise, look at what the session has just produced or referenced — a draft message,
  a file just written, a ticket being discussed, an artifact just published. If exactly
  one such candidate exists, use it.
- If more than one plausible candidate exists — several unrelated candidates, not the
  several files of one named set — or none is obvious, ask the user which content to
  audit. Never guess silently.

## Step 2 — Resolve the source

Fetch the target's raw text using `SOURCES.md`. If the fetch needs a capability that is
not available (no ticket-system access, a broken link, a file that does not exist), say
so and stop. Do not fabricate content to audit.

## Step 3 — Run the checklist

Apply every category in `CHECKLIST.md` to the raw text, judging it against itself and
its own stated purpose — internal consistency only, not against outside facts (see
`CHECKLIST.md`, "Misleading, wrong"). Then load `rules/user-rules.md` and apply its
rules on top, with the highest precedence.

When the target is a set, run the checklist twice: once within each document on its own,
then once across the set as a whole. For the second pass the set is "itself" — a claim in
one document and a duplicate or contradicting claim in another are both in scope.
Anything outside the set still is not.

If there is nothing to audit — the content is empty, or genuinely has no issues — say so
and stop. Do not manufacture findings to have something to report.

## Step 4 — Report

Present every finding, most severe first. Use a structured, itemised mechanism if one
exists; otherwise a clearly labelled list. Each finding states: the category from
`CHECKLIST.md`, the exact location or a short quoted excerpt, why it is a problem for
this specific content, and — when there is an obvious one — a proposed fix.

An empty list is a valid outcome; report it plainly.

## Step 5 — React

Ask how to proceed: fix everything found, fix specific ones, or discuss first. Never
apply a fix without being told to.

When more than one finding is being fixed, work through them one at a time: show that
finding's diff or before/after (per step 0's diff capability), wait for explicit
confirmation, apply it, then move to the next — rather than presenting every diff at
once for a single round of approval. If a new issue turns up while fixing one (not
part of the reported findings), surface it separately and ask before adding it to the
queue, rather than folding it in silently.

Skip a finding instead of forcing a fix if applying it would change the content's
intended meaning, reach outside the content under audit, or turns out on closer
inspection to be a false positive — note the skip plainly rather than arguing for the
original finding.

After acting, state the outcome of each finding that was addressed: fixed, skipped, or
no change needed.

## Step 6 — Learn, optionally

If a finding reveals a genuine gap in the guide, the same category of issue recurring
across separate audit runs, or a disagreement with the developer that reveals a rule
was wrong or missing, follow `LEARNING.md` to propose a rule. Most audits will not
reach this step; it is not required to run every time.
