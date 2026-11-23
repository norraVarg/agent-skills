# Skill authoring procedure

This is the whole procedure for creating a skill, updating one, auditing the skills a user already
has, and — on request — measuring a skill empirically. It is written for any agent to follow, on any
platform: it names no specific tool, because no specific tool exists on every platform. Each
provider's entry point (`adapters/<provider>/`) tells you what concretely fulfils the capabilities
named in Stage 0, on that platform. What a finished skill must look like for a given agent — its entry
file, metadata keys, permission model, where it is installed — lives in a format file under
`formats/`, chosen in Stage 0. Everything else below is identical everywhere.

Stages 1–5 are the everyday path and should stay fast. Stages 6–8 measure a skill empirically — they
use fresh contexts and take real wall-clock time, so they run only when the user asks for them. Offer
them; do not impose them. Eight stages routing three modes justify the length of this file.

**Constraints:**

- Never write or overwrite a skill file until the user has confirmed the draft. This is a hard gate.
- Do not emit emojis, with two exceptions: audit reports (Stage 2A and Stage A) and the Stage 5V
  regression report use the status markers defined in Stage 2A, and Stage 5's size report uses the
  trend markers in `SIZE-REPORT.md`. Nothing else.
- Use fresh contexts only in Stages 6–8, and only after the user has agreed to that stage — they are
  the one place an independent run buys something this context cannot provide.
- Write only inside the target skill's directory and `<workspace>`, plus `<private-terms>` when the
  user has confirmed its contents. Other directories belong to other skills or to the user — never move
  or delete files there, even to tidy up.

**Input:** the user's request may contain a skill name, a description, a change request, or the word
`audit`. Use what is given and ask only for what is missing.

**Placeholders used below**, all settled in Stage 0:

- `<guide>` — this guide's directory, as the adapter names it.
- `<format>` — the chosen format file, `formats/<agent>.md`.
- `<skills-root>` — where the format says the user's own skills live.
- `<workspace>` — scratch space for one skill, outside `<skills-root>` so it never looks like a skill.
  It holds the pre-edit snapshot (Stage 2U), the draft under validation (Stage 3R) and the eval runs
  (Stage 6). The adapter names its location.
- `<py>` — how to run this guide's scripts: see Stage 0's "Run scripts".
- `<private-terms>` — the user's list of private terms for the privacy pass, kept outside every
  repository. The adapter names its location.

---

## Stage 0 — Detect capabilities, format, intent and sharing

### Capabilities

Before anything else, establish what you actually have to work with:

- **Ask and wait.** A way to put a question to the user and get the answer before continuing,
  ideally with a structured-choice form. Without the structured form, ask in a plain message with
  numbered questions and wait for the reply.
- **Run scripts.** A shell with `python3`. The scripts in `<guide>/scripts/` need PyYAML except
  `check_refs.py` and `scan_private.py`. Test `python3 -c 'import yaml'`: if it works, `<py>` is
  `python3`; if not and `uv` is available, `<py>` is `uv run --no-project --with pyyaml python3`, which
  supplies PyYAML for that run only. Do not install packages into a system or externally managed
  interpreter. With no shell, or neither option, apply the same checks by hand from
  `REVIEW-CHECKLIST.md` and say in every report that the mechanical passes did not run.
- **A diff or preview.** A way to show a proposed edit against the original. Without it, show the
  before and after text inline.
- **Fresh contexts.** A way to run a task in a separate context that starts without this
  conversation — needed only by Stage 6. Without it, Stage 6 is unavailable; say so and recommend the
  dry run that Stage 5 describes instead.
- **An evaluation harness.** The tooling `<format>`'s "Evaluation harness" section names — needed only
  by Stages 6–8. Check for it when entering one of those stages; if it is absent, give the user the
  format's setup instructions and stop that stage. Do not reimplement the harness.

State in the final report of any stage which of these ran in a degraded mode.

### Format

Pick the format file for the agent the target skill is written for. Today `formats/claude-code.md` is
the only one; read it now. If the user is writing for an agent with no format file, say that format is
not supported yet and offer to add one from `formats/_TEMPLATE.md` — that file defines every section a
format must fill. Each format answers where skills live, how a skill is named and described, how it
declares tool permissions, how it takes arguments, how to validate it, and how to evaluate it.

### Intent

List the skills in `<skills-root>` the way `<format>`'s "Where skills live" section describes, counting
only directories that hold the format's entry file — leftover workspaces and packaged archives land
there too and would otherwise look like skills to the routing below.

Strip a leading `/` or other invocation prefix from any name that arrives as text, then match it
against the listing. The adapter describes how a skill name typed as an invocation reaches this
procedure on its platform; follow that note when one exists.

Route on what the request contains:

- **`audit` with no skill name, or a request to review or check skills generally** → Stage A, across
  every skill.
- **A skill name alone, or `audit` plus a skill name** → audit that one skill. Read its entry file,
  then Stage 2A.
- **A skill name plus a change request** → update. Read its entry file, then Stage 2U.
- **A skill name that does not exist** → create. Stage 1.
- **Nothing usable** → ask, in one message, as a structured choice: "Creating a new skill, updating an
  existing one, or auditing what you already have? If updating, which skill?" Later questions follow
  the same split: a structured choice for a fixed set of options, numbered plain text for open-ended
  ones.

**Read-only locations.** If `<format>` marks the target's location as read-only — a plugin or package
cache, for instance — edit and validate a copy in `<workspace>`, then tell the user the change has to
ship through that plugin's or package's own source. Editing a cache in place is silently reverted by
the next update.

**Skills that live in a repository.** If the target resolves — directly or through a symlink — into a
repository with its own contribution rules (a `CONTRIBUTING.md` or similar), read them before drafting.
They outrank `HOUSE-STYLE.md` for that skill: its layout, naming and writing rules come from the
repository, and this procedure's gates and checks still apply on top.

### Sharing

Decide whether the target skill is **personal** — private details allowed, because it never leaves the
user — or **shareable**, which must not identify the user, their employer or their machine:

- It lives in, or will be written into, a repository whose contribution rules forbid identifying
  information → shareable. Do not ask.
- Creating any other skill → ask in Stage 1.
- Updating or auditing any other skill → personal, unless the user asks to make it shareable; that
  request then becomes part of the change.
- Stage A decides each skill by the same rules.

A shareable skill gets the privacy pass in `PRIVACY.md` wherever Stages 2A, 3R, 5V and A say so. A
reviewer's judgement alone misses identifiers; the pass adds a scan, so known ones cannot slip through.

---

## Stage 1 — (Create) Gather basics

Extract from the request:

- **skill-name** — in the form `<format>`'s naming rules require.
- **purpose** — one sentence on what the skill does.
- **sharing** — personal or shareable, unless Stage 0's "Sharing" already settled it. Ask it as a
  structured choice: "Personal — only you use it; private details are allowed" or "Shareable — must be
  generic; a privacy pass runs before you see the draft".

Ask for whatever is missing in one message, then continue to Stage 2.

---

## Stage 2 — (Create) Understand the behaviour

Read `HOUSE-STYLE.md` and ask the questions in its "Gather the behaviour" section the way that section
says. Stage 3 needs the rest of the file, so keep it in context instead of reading it again. Wait for
the answers, then continue to Stage 3.

---

## Stage 2A — (Audit one skill) Report before changing anything

A name on its own means audit, not edit. No skill file is written in this stage.

Run the mechanical passes first — they execute without loading into context, so they are nearly free.
`<format>`'s "Validation" section gives each command for this format: the validator on the target, and
the body audit and overlap report across every skill.

The body audit and overlap report cover every skill: read only the rows for this one, plus any overlap
pair it appears in. Overlap is the failure mode a large collection of skills in one domain actually
hits, and it cannot be seen from inside a single file. Findings prefixed `advisory:` are robustness
notes rather than defects, and a tool called only from a bundled file will look unused — check that file
before believing the finding.

Then read `REVIEW-CHECKLIST.md` and apply it to the current content. For a shareable skill, also read
`PRIVACY.md` and run its pass; every unresolved hit is a ❌ finding. Report:

- Issues found → list them, each prefixed with its status marker, then ask "Apply all fixes?"
- Nothing found → say "✅ No issues found." and ask "Anything you'd like to change manually?"

**Status markers.** Audit reports — this stage and Stage A — and the Stage 5V regression report are
the only places in this procedure that use emoji. Use exactly these, one per finding, as a status
marker and never as decoration:

| Marker | Meaning |
| ------ | ------- |
| ✅ | Passes — no action needed |
| ❌ | Defect — the skill is broken or invalid as written |
| ⚠️ | Advisory — robustness note, safe to leave as is |
| 💰 | Size or token cost worth a decision |
| ⚔️ | Trigger overlap — two skills competing for the same phrase |

On confirmation, carry the agreed fixes into Stage 2U as the change request. If the user wants
something else changed instead, that becomes the change request. Either way Stage 4's confirm gate
still applies.

---

## Stage 2U — (Update) Understand the change

Apply the change request — the user's, or the fixes agreed in Stage 2A — to the existing content to
produce a draft, then go to Stage 3R.

**Before editing, snapshot the current version** to `<workspace>/skill-snapshot/`. It costs one copy
and it is what lets Stage 5 report a size delta instead of an absolute count, what lets Stage 5V blame
only what the update introduced, and what lets Stage 6 measure the new version against the old one
rather than against nothing.

---

## Stage 3 — Draft the skill

Compose the full entry file to `HOUSE-STYLE.md` and `<format>`'s "Entry file" template. Stage 2 already
loaded the house style — read it here only if control reached this stage without passing Stage 2. Its
opening section decides the skill's shape: the directory layout, the loading levels that make bundling
worth it, and the rule for what stays in the entry file versus what moves to a bundled file. Settle the
shape before writing prose, not after. Then continue to Stage 3R.

**Do not create a skill that would surprise the user if described plainly.** No malware, no exploit
code, no data exfiltration, nothing designed for unauthorized access. Roleplay and persona skills are
fine.

---

## Stage 3R — Review before showing

Mandatory in create and update mode, even for a one-line change. Read `REVIEW-CHECKLIST.md` and apply
it end to end. It stays a separate file even though nearly every run reads it: keeping it here would
load the review rules onto audit runs too, which review no skill at all. Density in this file, not
token count, is what justifies that split.

The validator reads metadata from disk, so it needs a file to point at — and in create mode the real
directory does not exist until Stage 5. Write the draft to `<workspace>/draft/` and run `<format>`'s
validator there. It is a validation copy only; Stage 5 still writes the real files.

For a shareable skill, read `PRIVACY.md` and run its pass on `<workspace>/draft/`. A shareable draft
does not reach Stage 4 with an unresolved hit.

Fold every fix into the draft before showing it to the user.

---

## Stage 4 — Show the draft and confirm

Display the full draft in a box:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━ DRAFT SKILL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: <skills-root>/<skill-name>/<entry file>

<full entry file content>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For an update, show what changed rather than the whole file, unless the rewrite is substantial. For a
shareable skill, put the privacy pass's report line directly under the box.

Ask: "Does this look right? Any changes before I write the file?" Apply edits and re-show until the
user confirms.

---

## Stage 5 — Write

Once confirmed:

- **Create** — make the skill's directory under `<skills-root>`, then write the entry file and any
  bundled files.
- **Update** — make targeted edits so the rest of each file provably stays byte-identical, and rewrite
  a whole file only when the change is substantial enough that a diff would be noise.

Then measure and report what this cost: **read `SIZE-REPORT.md` and follow it.** It holds the
measurement, the trend markers, the thresholds worth warning about, and the output block to print.

**In update mode, run Stage 5V next**, before the offers below: a skill broken by its own update is not
worth measuring, and the check needs the snapshot that the workspace question may delete.

If the skill's output is objectively checkable, it runs to the end without the user, and the user has
not already declined, offer once: "Want me to test it against a few real prompts and measure it?
That's stage 6 — it takes a few minutes." Then stop.

If the skill instead depends on the user mid-run — question rounds, approval gates, live systems — do
not offer Stage 6: fresh contexts cannot answer its questions, so a run stalls at the first gate and
measures nothing. Recommend a dry run on one real, already-finished case instead, stopping at the
skill's first major output and comparing it with what was actually done. Then stop.

If they decline, ask once whether to delete `<workspace>` — the snapshot has no further use at that
point. If they accept, ask the same question when Stage 6 finishes, since the baseline is needed until
then.

---

## Stage 5V — (Update) Regression check

Every update, whether it came from an audit or from the user, ends here once Stage 5 has written it.
Edits are reviewed line by line in Stage 3R, but breakage usually lands in the lines they did not touch
— a step that now runs before its input exists, a pointer to a renamed section. **Read
`REGRESSION-CHECK.md` and follow it.** It holds the mechanical passes against the snapshot, the
change-impact sweep, the scenario trace, and the report block. Nothing is written in this stage; fixes
go back through Stages 2U → 5.

---

## Stage A — Audit existing skills

A health check across everything the user has. One named skill goes to Stage 2A instead; this stage is
for the whole collection, and its value is the cross-skill checks that a single-skill audit cannot
make.

**Read `AUDIT.md` and follow it.** It holds the per-skill metadata pass, the body-level audit and how
to read its advisory findings, a size pass that ranks every entry file for judgement against its
complexity, the bulk description-quoting pass, the privacy pass for shareable skills, and the
cross-skill checks that only make sense in aggregate — trigger overlap, metadata fragility, dead
metadata keys.

Two things hold regardless: **removing a tool permission needs evidence from the skill's own files**,
because a missing permission breaks the skill while a spare one only widens it. And **fix findings
through Stages 2U → 5, one skill at a time**, so every change still passes the confirm gate — an audit
is not a licence to batch-edit.

---

## Stage 6 — Test and measure (opt-in)

Only when the user asks, or accepts the offer in Stage 5. Needs fresh contexts and the evaluation
harness (Stage 0).

Read `EVALS.md` and follow it. In outline: write test prompts, run each one twice in fresh contexts —
once with the skill and once against the baseline — grade assertions, aggregate the benchmark, and put
the results in front of the user in the harness's viewer before forming your own opinion. The baseline
is no skill at all for a new skill, and the Stage 2U snapshot for an update.

---

## Stage 7 — Tune the description (opt-in)

Only when the user asks, or when a skill demonstrably fails to fire. Needs the evaluation harness.

Read `DESCRIPTION-TUNING.md`. This is the highest-value optional stage for anyone running many skills
in one domain, because near-miss collisions between descriptions are the real failure mode there, not
vague wording.

---

## Stage 8 — Package (opt-in)

Only if the user wants a shareable package. `<format>`'s "Evaluation harness" section gives the
packaging command, if the format has one. Preserve the original skill name — never emit a `-v2`
variant. Move the resulting file out of `<skills-root>` once built, so that directory stays skills-only
and Stage 0's listing has nothing to filter.

Stop. No closing remarks.
