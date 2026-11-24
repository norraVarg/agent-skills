# Frontend implementation procedure

This is the whole procedure for taking a frontend task from requirement to a tested, design-faithful
change. It names no specific agent tool, so any agent can follow it: each provider's entry point
(`adapters/<provider>/`) maps the capabilities named in Step 0 onto that platform's tools.

Nothing is guessed: every gap between requirement, design and code becomes a question, every answer
lands in a spec file, and every line of the spec is traced to a test and a fidelity check. Everything
specific to one issue tracker, design tool, test runner or framework lives in a variant file chosen in
Step 0. Eight steps, three approval gates and the variant routing justify the length of this file.

**Constraints:**

- **Ask, never assume.** When requirement, design and code disagree or are silent, ask. A guessed
  requirement is the most expensive kind of bug because it passes its own tests.
- **The spec file is the single source of truth** from Step 4 onward. Code and tests change only for
  something the spec says; see "Change control" below.
- **Show a draft diff before writing any file and wait for a yes.** Batch the diffs per step so a gate
  covers a coherent set of files rather than one round trip per file.
- **Run only targeted tests.** Invoking this skill is permission to run the test files it writes or
  changes and the existing tests in the touched area. The full suite, lint, formatting and typecheck
  run only on the user's explicit command — the user may still be editing, and only they know when
  that is done.
- **Commit nothing.** The change is left uncommitted for the user's own commit and PR flow.
- **Working IDs stay in the session.** AC numbers, decision-log numbers, question numbers, the spec
  version and the spec file's path exist only in this session's working files, so they mean nothing
  to anyone reading the code later. Never write them into code, tests, test titles, comments, test
  IDs (`data-cy`, `data-testid`), fixtures, or text meant for a commit, pull request or issue. Name
  and describe everything by the behaviour it covers. Traceability lives in the spec's test mapping
  (Step 5), where the IDs make sense.

**Input:** the user's request — an issue key or URL, or requirement text, optionally followed by
design URLs or image paths. If none of these is present, ask what to build before doing anything else.

**Placeholders**, named by the adapter:

- `<spec-dir>` — where spec files live, outside every repository.
- `<profile-dir>` — where project profiles live, outside every repository.

**Spec file:** `<spec-dir>/<KEY>.md`. `<KEY>` comes from the tracker variant; with no tracker, propose
a short kebab-case slug and confirm it in Step 3's first group. It lives outside the repo so it never
shows in `git status` or a PR. If the file already exists, this is a resumed session: read it,
summarise its status and changelog, and continue from the first step it has not completed. With no
tracker, the user resumes by passing the slug alone: check for `<spec-dir>/<slug>.md` before
treating the request as requirement text.

**Project profile:** `<profile-dir>/<repo-name>.md` — conventions learned about one repo (Step 2), so
later runs skip rediscovery. Optional; offered in Step 8.

---

## Step 0 — Detect capabilities and choose variants

### Capabilities

Before anything else, establish what you actually have to work with:

- **Ask and wait.** A way to put a question to the user and get the answer before continuing,
  ideally as a structured choice. Without the structured form, ask the same questions as numbered
  plain text and wait for the reply; Step 3's rules still apply.
- **Issue tracker access.** A way to read an issue, its comments and linked issues, which the
  tracker variant needs. Without it, ask the user to paste the issue text and switch to the no-tracker
  variant.
- **Design tool access.** A way to read design frames, screenshots, tokens and comments, which the
  design variant needs. Without it, ask the user to export the frames as images and switch to the
  images variant.
- **Run commands.** A shell to run the targeted tests. Without it, write the tests and the code, give
  the user the exact commands to run, and wait for the results at each point where this procedure
  runs tests.
- **Browser automation.** A way to open the running app, drive it into a state, resize it, take a
  screenshot and read computed styles — needed by Step 7. Without it, give the user the state ×
  viewport list to check by hand, and mark Fidelity as "manual" in the report.
- **A diff or preview.** A way to show a proposed edit against the original. Without it, show the
  before and after text inline.

State in the Step 8 report which of these ran in a degraded mode.

### Variants

Variants live in `variants/<kind>/`. Pick one per kind from the signals below and read only the chosen
files; together they supply every tool- or framework-specific instruction the later steps need. When
two variants of one kind match, ask which applies right away — the answer blocks fetching. When none
matches, follow the "no match" cell.

| Kind | Variant | Use when |
| --- | --- | --- |
| Scope | `variants/scope/react-ts.md` | `package.json` depends on `react` and `typescript`, or the touched code is `.tsx` |
| | no match | Say the framework is not supported yet; ask whether to continue with the core workflow only |
| Tracker | `variants/trackers/jira.md` | A key like `ABC-123` or an `atlassian.net` URL |
| | `variants/trackers/github-issues.md` | A `github.com/<owner>/<repo>/issues/<n>` URL, or `<owner>/<repo>#<n>` |
| | `variants/trackers/none.md` | No issue reference: the requirement is text, a design or screenshots |
| Design | `variants/design/figma.md` | A `figma.com` URL in the request or the issue |
| | `variants/design/images.md` | Image paths in the request, or images attached to the issue |
| | `variants/design/none.md` | Neither in the request nor in the requirement; confirmed in Step 3's first group |
| Unit/component runner | `variants/runners/vitest.md` | `vitest` in `package.json` |
| | `variants/runners/jest.md` | `jest` (or `react-scripts`) in `package.json` |
| E2E | `variants/e2e/cypress.md` | `cypress` in `package.json` |
| | `variants/e2e/playwright.md` | `@playwright/test` in `package.json` |
| | no match | Record for Step 3: the user decides between adding e2e tooling and extra integration tests |

Each row is decided as soon as its signal exists: the tracker row from the request now; the design
rows right after Step 1.1, because design links and images often live in the issue rather than the
request; the scope, runner and e2e rows at the start of Step 2, because they need the repo. Several
design sources may apply at once (Figma frames plus screenshots); read each matching design variant.

**Extending scope.** Every variant of a kind has the same sections, listed in that kind's
`_TEMPLATE.md`. A new framework, tracker, design tool or runner is one new file copied from that
template plus one row in this table — no step below changes.

---

## Change control — applies from Step 4 to the end

Any change to what is being built — requested by the user, or discovered by the skill (a missing
state, an API that behaves differently, a design detail nobody covered) — goes spec-first:

1. Show the spec edit as a diff, write it on a yes, and add a changelog entry: version, what changed,
   why, affected AC IDs.
2. Propagate to everything the spec's test mapping and fidelity matrix link to those AC IDs: behaviour
   tests first (red, then green again), then code, then the affected fidelity checks.
3. Resume the step that was interrupted.

Nothing reaches the code without passing through the spec, and Step 8 reconciles the changelog
against the result — that is what guarantees every change made during the session is addressed.

---

## Step 1 — Gather the requirement

1. Fetch the requirement as the tracker variant describes: the item itself, its comments (decisions
   often live there and contradict the description), and related items one level deep. Deeper chains
   rarely add requirement detail and cost a lot of context.
2. Choose the design variants (Step 0) from the request and the requirement together, then fetch
   every design source as its variant describes: the frames or images for each state and breakpoint,
   tokens where available, and designer notes.
3. If the requirement references a design that was not provided, or no design turned up at all,
   record it for Step 3's first group rather than proceeding without it; with no design, read
   `variants/design/none.md` provisionally until the user confirms.

## Step 2 — Analyse the repo

Work out the repo's conventions from its own files rather than from memory of other repos — each
repo differs, and the nearest existing test is the best template for a new one.

1. Read the project profile if one exists, and verify each entry against the repo still holds rather
   than trusting it blindly. Read the repo's agent instruction files (`AGENTS.md`, `CLAUDE.md`, or
   similar) — company and project rules belong there, and they outrank this skill's defaults.
2. Settle the scope, runner and e2e variants from Step 0 and read them.
3. Find, as the variants describe: test config and setup files, the custom render helper, network
   mock handlers, e2e layout and helpers, and the selector convention.
4. Find the code the task touches: routes, pages, components, hooks, API clients, state. Identify the
   design system's components and tokens to reuse — rebuilding a library component is a fidelity bug
   waiting to happen.
5. Locate i18n files, feature-flag mechanism and analytics calls in the area.
6. List every existing unit, component and e2e test that covers the touched code, and for e2e note
   whether the nearest similar spec hits a real backend or stubs it, and how.

## Step 3 — Gap analysis and questions

Read `FIDELITY-CHECKLIST.md` and `QUESTION-BANK.md` now. They are split out for density, not tokens —
every run reads them here.

1. Walk the checklist and the question bank across three sources at once — requirement, design,
   code — and note every item that is missing, ambiguous or contradictory between them.
2. Separate questions from information. Only items that need the user's decision become questions;
   findings they merely need to know (no visual change, which files are affected) go into the spec in
   Step 4. Mixing the two makes the user hunt for what actually needs an answer.
3. Sort the questions into groups, in this order: requirements and behaviour, design gaps, test
   approach. The first group also carries the setup questions recorded in Steps 0–2 that did not
   block fetching (a missing or absent design, the spec slug). Before asking anything, state the plan
   in one line so the length of the interview is known upfront:
   `7 questions in 3 groups — requirements (4), design (1), tests (2). Starting with requirements.`
4. Ask one group per structured-choice dialog, waiting for the answers before writing the next
   group's questions, so each group can build on the decisions already made and every question is
   visibly a question. A group larger than the dialog's per-call limit (the adapter names it)
   continues in a second dialog on the same topic; a group with no questions is skipped. For each
   question:
   - Start the text with its position and topic, e.g. `[3/7] Scope —`. Keep it self-contained in
     two sentences at most: what was found and where, then the question. The dialog may hide
     earlier text.
   - Give 2–4 concrete options, the recommended one first and labelled "(Recommended)", each with
     a one-line consequence. The user can always answer freely instead.
   Questions with no sensible options (a test user, how to reach a screen locally) follow the
   dialog as plain text under the heading `Need your input`, one numbered line each, keeping their
   `[n/N]` numbers.
5. Close the current group before starting the next, because the next group's questions are written
   from this group's answers. Handle each answer by what it contains:
   - A clear choice, or a free-text answer that clearly answers → resolved.
   - A vague answer → ask a follow-up rather than interpreting it.
   - A question from the user → answer it in plain text first, looking things up if needed, then
     re-ask the original question, re-worded if the answer changed its options.
   - New information → check whether it changes any answer already given, in this group or an
     earlier one, and re-ask each one it does.
   Re-ask only the unresolved questions, together in one dialog, labelled `(follow-up)` and keeping
   their `[n/N]` numbers. Whenever a question is added, update the count out loud:
   `1 follow-up added — 3 questions left.` Move to the next group only when every question in this
   one is resolved; go to Step 4 when the count reaches zero.

## Step 4 — Write the refined requirement spec (gate)

Read `TESTING-STRATEGY.md` now — the spec's test plan is decided here. Like the Step 3 files, it is
split out for density; Steps 5 and 6 apply it.

1. Fill `templates/spec.md` from Steps 1–3: sources, numbered acceptance criteria (AC-1, AC-2, …), the
   state × viewport matrix, the decisions log (every question with its answer), out of scope, files to
   touch, and the test plan.
2. Show the spec in full, then write it to the spec file on a yes. The user may edit the file
   directly; re-read it when told it is ready.
3. Do not continue until the user explicitly approves the spec. From here on, change control applies.

## Step 5 — Red: write the behaviour tests first

Behaviour tests come first because they are derived from the agreed ACs, not from the code — tests
written after the code tend to assert what the code does rather than what the requirement asked for.

1. Re-read the spec file.
2. Run the existing tests that cover the touched area to record a baseline, so later failures can be
   told apart from ones that already existed.
3. Draft component/integration tests and e2e specs for every behavioural AC, following the testing
   strategy, the runner, e2e and scope variants, and the nearest existing test. Name each test for the
   behaviour it checks, in the repo's own naming style (`shows the error message when submission
   fails`) — never with an AC ID.
4. Record each test in the spec's test mapping: AC, file, exact test title, layer. This is what keeps
   coverage traceable without putting session IDs into the repo.
5. Show the test diff and the mapping update, write on a yes, run only those tests with the variants'
   targeted-run commands, and confirm each fails for the expected reason — a test that fails on a
   missing import proves nothing about behaviour.

## Step 6 — Green: implement

1. Re-read the spec file.
   If the design variant's "Fidelity source" needs a "before" capture, take it now — once code
   changes, the original UI is gone.
2. Draft the implementation following the scope variant, reusing the design-system components, tokens
   and translations found in Step 2. Show the diff, write on a yes.
3. Run the Step 5 tests until they pass. Do not edit a test's assertions to make it pass: if a test
   now looks wrong, that is a spec question — go through change control.
4. Add unit tests for pure helpers extracted during implementation, and update existing tests broken
   by an intended behaviour change. Record each one in the spec's test mapping against its AC. Re-run
   the Step 5 baseline set to confirm nothing else regressed.

## Step 7 — Fidelity pass

Pixel and layout detail cannot be asserted in a DOM-only test environment, so it is verified against
the design directly.

1. Re-read the spec file, `FIDELITY-CHECKLIST.md`'s "Verification" section, and the design variant's
   "Fidelity source" section — it defines what the running UI is compared against.
2. Ask the user how to start the app locally if the profile and scripts do not say, and which user,
   locale or flag values reach the screen. Start nothing that talks to production.
3. For every cell of the spec's state × viewport matrix: drive the UI into that state with browser
   automation, resize to the viewport, take a screenshot, and compare it with the fidelity source.
4. List every mismatch (spacing, typography, colour, alignment, copy, missing state). Fix those that
   are implementation errors; route design questions through change control.

## Step 8 — Report

1. Re-read the spec file, then print the report below. Build the coverage table from the spec's test
   mapping, not from test titles. The report is for this session: if the user then asks for a commit
   message or pull request text, describe the change by behaviour and leave the AC IDs out.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━ <KEY> REPORT ━━━━━━━━━━━━━━━━━━━━━━━━━━
Spec: <spec-dir>/<KEY>.md (v<N>)
Variants: <scope> · <tracker> · <design> · <runner> · <e2e>
Degraded capabilities: <list, or "none">

Changelog reconciliation
| Ver | Change | AC IDs | Propagated to |

Acceptance criteria coverage
| AC | Unit | Component | E2E (real/mocked) | Fidelity | Status |

Tests
Added:    <file> — <what>
Modified: <file> — <why>

Fidelity mismatches still open
<list, or "none">

Open items
<list, or "none">

Full checks for you to run when ready
<repo's test, typecheck, lint and format commands>

DONE — every acceptance criterion is covered, nothing is open
  or
NOT DONE — waiting on: <each open item, and who has to act>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. Mark the spec file's status as implemented. Every AC must show at least one passing test and a
   fidelity result, and every changelog entry must show where it was propagated; anything that does
   not goes under Open items rather than being dropped.
3. If no project profile exists, or Step 2 found entries that no longer hold, offer to save one from
   `templates/profile.md` with what this run learned — showing the diff first, like any write.

Stop. No closing remarks.
