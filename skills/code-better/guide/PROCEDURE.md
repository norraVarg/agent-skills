# Review procedure

This is the whole procedure for reviewing a set of code changes against the guide.
It is written for any agent to follow, on any platform: it names no specific tool,
because no specific tool exists on every platform. Each provider's entry point
(`adapters/<provider>/`) tells you what concretely fulfils the capabilities named
in step 0, on that platform. Everything else below is identical everywhere.

If the developer supplies extra context up front — a concern to focus on, or a subset of
the changes to look at — fold it into step 1's gather and step 3's find. It narrows what
is reviewed; it never relaxes a rule or skips a step.

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

If the target is remote — a pull request, a branch, a commit range — fetch its
unified diff directly rather than cloning the repository; fetch a file's full content
only when a hunk's surrounding lines are not enough to judge a rule, and fetch it once,
not once per later step that needs it.

Read the diff into the context that will do the finding in step 3. By default that
is this same context — step 3 finds directly here, so read it once, now, and reuse
it. Only gather a by-reference hand-off instead (file paths, per-file change stats,
not full content) when step 3 actually shards the diff out to delegated contexts
because of its size — in that case each shard fetches its own slice once. Content
read into one context and then handed to another gets read twice for no benefit;
read it once, in whichever context ends up doing the finding.

If there is nothing to review, say so and stop. Do not manufacture findings to have
something to report.

## Step 2 — Classify and load

For each changed file, classify its language and domain using the tables in
`RULE-LAYERS.md`, and load the layers it ranks:

1. `rules/user-rules.md` — always.
2. Every file in `universal/` — always. The layer is small enough to hold in full, and
   a rule that does not apply to this diff simply produces no finding.
3. The matched `domains/*.md`.
4. The matched `languages/*.md`.

A diff touching several files may need several different combinations of layers, one
per file or per small group of related files. Do not average them into one generic
pass.

When step 3 delegates to a fresh context, hand it these files' paths rather than
pasting their contents into the prompt — the guide already exists on disk, and
copying it into every delegated prompt duplicates content the delegate can read
itself for free.

## Step 3 — Find

Look for violations of the loaded rules in the diff. For every candidate, quote the
exact rule it violates, the file it lives in, and the line, not a vague description
like "doesn't follow conventions." A finding that cannot point at a specific quoted
rule is not a finding yet.

**Do this in the current context by default.** The diff and the loaded guide layers
are already here from steps 1-2; reasoning over them again in this same context
costs only output tokens, not another content load. Delegating to a fresh context
(a subagent, a separate session) is not free — it pays a new context's fixed cost
(system prompt, tool schemas) and must re-fetch whatever diff and guide layers it
needs, so reserve it for when it earns that cost.

**Delegate, sharded by size, only when the diff genuinely does not fit one context.**
A rough ceiling: a few thousand changed lines, or enough files that holding them all
together would crowd out careful reasoning — adjust to the platform's actual context
budget. Below that ceiling, do the whole find pass right here, in one combined pass
covering every loaded rule, safety rules first (correctness, security, testing — the
rules `RULE-LAYERS.md` marks as holding everywhere) before style rules (simplicity,
naming, domain and language idioms — the rules a project's existing conventions can
outweigh). At or above the ceiling, split the diff into shards at that size, grouping
by Step 2's layer signature where convenient so a shard doesn't mix unrelated rule
sets, and run each shard as its own delegated call — one call per shard, each still
covering every rule that shard's files loaded in a single pass, issued in parallel
rather than in sequence. Do not add a second delegated call over the same shard for a
different rule category: that re-pays the fixed cost of a new context to re-read
content the first call already has open, for no benefit over reasoning through both
categories in the pass it's already running.

Find by reading and reasoning, not by running code. Writing and executing a script to
prove a hypothesis is verification-grade work — it belongs to step 4, not here, and
doing it during find is why a pass can quietly balloon to many tool calls and minutes
of runtime over a single diff.

A delegated shard reads only its own slice of the diff and the files it names — it
does not explore the rest of the repository unless a specific rule requires checking
a caller or a config file the diff doesn't show.

Safety-rule scrutiny belongs to files that execute — source and test code.
Documentation, changesets, and lockfiles cannot violate a correctness or security
rule; give them only the style layer's own doc-accuracy check (a comment or doc that
no longer matches the code it now describes), and do that lightly — skim for drift,
not line-by-line.

## Step 4 — Verify

Every candidate finding gets checked before it is trusted, in a context separate
from whichever one found it. Unlike step 3, this delegation is not a size
trade-off — independence is the actual requirement, so this step always uses
step 0's independent check when one exists.

**Batch by file, cap by count, run batches in parallel.** A candidate's file has to
be read to judge it; when several candidates land in the same file, reading it once
per candidate is pure waste. Group candidates by file — several small files can
share a batch — cap each batch at roughly ten candidates so no single call gets
overloaded, and issue the batches as parallel calls to the independent check rather
than one call per candidate. A lone candidate is simply a batch of one; nothing
about a small diff changes.

If an independent check is available: give each batch the file(s) and, for every
candidate in it, the quoted rule and line — never the reasoning that produced it —
and have it try to refute each one, judging every candidate on its own terms so a
verdict on one does not colour its verdict on another in the same batch. It returns
one verdict per candidate: confirmed, plausible, or refuted. Keep confirmed and
plausible; drop refuted.

Reasoning from the file and the quoted rule is the default here too. Reach for
actually executing a small, self-contained script only when that reasoning is
genuinely inconclusive — not as a matter of course — since running code costs far
more time and tokens than reading it.

If no independent check is available: re-examine each candidate yourself, adopting a
deliberately skeptical, refute-first stance. Score each one for confidence, 0 to
100 — whether it is a real defect in this diff rather than a stylistic preference, a
pre-existing condition, or a guess. Keep what scores 80 or above; drop the rest.
State in the report that this weaker self-check ran instead of an independent one.

## Step 5 — Report

Assign each surviving finding a severity: **High** (breaks something now, or is
exploitable in production), **Medium** (fine today but will silently break under a
plausible future change or edge case), or **Low** (style, clarity, or non-functional
— docs/tests/comments — with no runtime impact). Present findings ordered by
severity, most severe first.

Use a structured, itemised mechanism if one exists; otherwise a clearly labelled
list. Each finding states the file and line, its severity, and a short paragraph
covering the concrete defect and its real-world consequence — not a rule citation
(step 3's quoted rule is for grounding the finding internally, not for the report).

Word that paragraph to ASD-STE100 (Simplified Technical English) conventions
first: front-load the defect, keep one idea per sentence, prefer active voice with
a stated actor, keep each sentence under roughly 20-25 words, use one consistent
term for a given concept rather than cycling synonyms, avoid idioms and phrasal
verbs so the finding reads clearly for a non-native English speaker, and gloss any
technical term the first time it appears, e.g. "prop drilling (passing a value
through several components that don't use it themselves)". The file/line citation,
the severity tag, and the verdict badge are structure added on top of that
wording — and so is any field this step gains later: it must still produce
ASD-STE100-compliant prose, not trade that discipline away for a new requirement.

Whether the finding was independently confirmed or only plausible must stay visibly
distinct in the presentation — a badge, a prefix, or whatever mechanism the platform
gives you — rather than a fixed wording, since the concrete mechanism is
adapter-specific.

An empty list is a valid outcome; report it plainly rather than treating a clean
review as incomplete.

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
