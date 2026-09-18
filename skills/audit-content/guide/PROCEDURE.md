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

If one of the optional capabilities is unclear or unavailable, use its stated fallback
and say so in the report; do not silently skip the step it enables.

Ask and wait is not optional. Without it, steps 1 and 5 cannot be honoured: never guess
a target and never apply a fix. Report the findings, say what you would have asked, and
stop there.

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

Run the checklist in two separate passes over each document, rather than one
unified read — a single read tends to under-apply the wording-focused categories,
since attention gravitates toward the more consequential structural ones.

- **Structural pass**: check only for categories 1 (unused, irrelevant,
  unnecessary), 3 (conflicting), and 4 (misleading, wrong).
- **Wording pass**: check only for categories 2 (redundant, repeated) and 5
  (unclear, poorly worded) — sentence by sentence. Test each individual sentence
  against "could this be deleted or shortened without losing information the
  reader needs," not the comment or paragraph as a whole. A comment can pass as a
  whole (it contains a real, non-obvious reason) while still having one
  sentence — often a lead-in restating what's already inferable from context —
  that fails this test on its own.

This split is a finding-completeness fix (catching more real issues on the first
pass), not a verification/refutation step — it does not need a second independent
check of each candidate the way `code-better`'s step 4 does, since the gap it
targets is under-recall (real issues missed), not over-reporting (false positives
flagged). Do not port `code-better`'s per-finding refutation mechanism here; it
solves a different failure mode than the one observed.

Judge both passes against the content itself and its own stated purpose —
internal consistency only, not against outside facts (see `CHECKLIST.md`,
"Misleading, wrong"). Then load `rules/user-rules.md` and apply its rules on top,
with the highest precedence.

When the target is a set, run the two passes above within each document on its
own, then run a separate, unsplit pass across the set as a whole — comparing
claims and sections between documents is not a sentence-level exercise, so the
wording pass's technique does not transfer to it. For the set-level pass the set
is "itself" — a claim in one document and a duplicate or contradicting claim in
another are both in scope. Anything outside the set still is not.

If there is nothing to audit — the content is empty, or genuinely has no issues — say so
and stop. Do not manufacture findings to have something to report.

## Step 4 — Report

Present every finding, most severe first. Use a structured, itemised mechanism if one
exists; otherwise a clearly labelled list. Each finding states: the category from
`CHECKLIST.md`, the exact location or a short quoted excerpt, and — when there is an
obvious one — a proposed fix.

State why it's a problem in the same plain style `CHECKLIST.md`'s own "unclear,
poorly worded" category asks of the audited content itself: front-load the point,
keep one idea per sentence, and gloss any technical or domain term the first time
it appears, e.g. "prop drilling (passing a value through several components that
don't use it themselves)". The quoted excerpt grounds the finding in the actual
text; it is not a substitute for saying in plain words what's wrong with it.

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

When any fixes were applied, also report an approximate token-cost reduction for the
content, e.g. `💰 ~150 tokens saved per use (~12% shorter)`. Estimate from before/after
content length (not an exact tokenizer count) and label it clearly as approximate.

## Step 6 — Learn, optionally

If a finding reveals a genuine gap in the guide, the same category of issue recurring
across separate audit runs, or a disagreement with the developer that reveals a rule
was wrong or missing, follow `LEARNING.md` to propose a rule. Most audits will not
reach this step; it is not required to run every time.
