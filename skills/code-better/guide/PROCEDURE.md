# Review procedure

This is the whole procedure for reviewing a set of code changes against the guide.
It is written for any agent to follow, on any platform: it names no specific tool,
because no specific tool exists on every platform. Each provider's entry point
(`adapters/<provider>/`) tells you what concretely fulfils the capabilities named
in step 0, on that platform. Everything else below is identical everywhere.

## Step 0 — Detect capabilities

Before anything else, establish what you actually have to work with:

- **An independent check.** Something that did not produce a candidate finding and can
  genuinely try to disprove it — a separate call, a separate context, a fresh pass, not
  the same reasoning re-reading its own conclusion and agreeing with itself.
- **A structured reporting mechanism.** A way to present findings as discrete,
  itemised results rather than only prose.
- **A diff or preview mechanism.** A way to show a proposed edit against the original
  before it is applied. Optional — falls back to showing the before and after text
  inline.

If a capability is unclear or unavailable, proceed as if it does not exist: without an
independent check, do the finding and verifying in one careful pass instead of two;
without a structured reporting mechanism, report in a clearly labelled plain list.
State plainly, in the final report, which mode actually ran. A weaker
review that says so is trustworthy; a weaker review presented as if it were the full
pipeline is not.

## Step 1 — Gather the diff

Collect everything not yet committed: staged changes, unstaged changes to tracked
files, and untracked files. Untracked files are included — skipping brand-new files
would miss most of what a real change usually contains.

If there is nothing to review, say so and stop. Do not manufacture findings to have
something to report.

## Step 2 — Classify and load

For each changed file, classify its language and domain using the tables in
`CLASSIFY.md`, and load the matching layers:

1. `rules/user-rules.md` — always.
2. Every file in `universal/` — always. The layer is small enough to hold in full, and
   a rule that does not apply to this diff simply produces no finding.
3. The matched `domains/*.md`.
4. The matched `languages/*.md`.

A diff touching several files may need several different combinations of layers, one
per file or per small group of related files. Do not average them into one generic
pass.

## Step 3 — Find

Look for violations of the loaded rules in the diff. For every candidate, quote the
exact rule it violates, the file it lives in, and the line, not a vague description
like "doesn't follow conventions." A finding that cannot point at a specific quoted
rule is not a finding yet.

If step 0's independent check can also run separate finding passes, run at least two:
one looking for safety-rule violations (correctness, security, testing — the rules
`CLASSIFY.md` marks as holding everywhere), one looking for style-rule violations
(simplicity, naming, domain and language idioms — the rules that yield to a project's
existing conventions). If it cannot, cover both in one pass, safety first.

## Step 4 — Verify

Every candidate finding gets checked before it is trusted.

If an independent check is available: for each candidate, have it try to refute the
finding using only the file and the quoted rule, no prior knowledge of why the finding
was raised. It returns one of confirmed, plausible, or refuted. Keep confirmed and
plausible; drop refuted.

If no independent check is available: re-examine each candidate yourself, adopting a
deliberately skeptical, refute-first stance. Score each one for confidence, 0 to
100 — whether it is a real defect in this diff rather than a stylistic preference, a
pre-existing condition, or a guess. Keep what scores 80 or above; drop the rest.
State in the report that this weaker self-check ran instead of an independent one.

## Step 5 — Report

Present the surviving findings, most severe first. Use a structured, itemised
mechanism if one exists; otherwise a clearly labelled list. Each finding states: the
file and line, the quoted rule it violates, why it matters for this specific change,
and its verdict from step 4.

State plainly whether step 0's independent-check and structured-reporting capabilities
were actually available, and which mode ran.

## Step 6 — React

Ask how to proceed: fix everything found, fix specific ones, or discuss first. Never
apply a fix without being told to.

When more than one finding is being fixed, work through them one at a time: show that
finding's diff or before/after (per step 0's diff capability), wait for explicit
confirmation, apply it, then move to the next — rather than presenting every diff at
once for a single round of approval. If a new issue turns up while fixing one (not
already among the reported findings), surface it separately and ask before adding it
to the queue, rather than folding it in silently.

When fixing a finding, skip it instead if the fix would change intended behaviour,
would reach outside the files under review, or turns out on closer inspection to be a
false positive, noting the skip plainly rather than arguing for the original finding.
After acting, state the outcome of each finding that was addressed: fixed, skipped, or
no change needed.

## Step 7 — Learn, optionally

If a finding reveals a genuine gap in the guide, the same category of issue recurring
across separate review runs, or a disagreement with the developer that reveals a rule
was wrong or missing, follow `LEARNING.md` to propose a rule. Most reviews will not
reach this step; it is not required to run every time.
