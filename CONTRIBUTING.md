# Adding or adopting a skill

This is what an agent asked to add a new skill to this repository — or to adopt one
that already exists elsewhere, in whatever shape it currently has — a different repo,
a different agent's format, an existing skill with no repo of its own — needs to know.
Read this file in full before starting; do not act from memory of an earlier read,
and do not invent a different structure.

## Privacy

Nothing in this repository may identify a person, an employer, or a specific
machine, in any skill, in any layer: no names, gendered pronouns describing a
specific person, emails, employers, or machine paths — and no real project detail
smuggled in through a worked example, a file path, or a feature name. The rule covers
every skill and every edit, and it matters most when new content enters the repo.

The repository checks this mechanically. Enable its hooks once per clone:

    git config core.hooksPath .githooks

Before every commit they scan the staged files and the commit message with
`skills/skill-master/guide/scripts/scan_private.py`, and block the commit on a hit. The
scan matches built-in patterns — email addresses, home-directory paths with a username,
IP addresses, secret-shaped tokens — and your own list of private terms: your names and
usernames, employer, clients, teams, ticket-project prefixes, internal domains and
repository names. The list lives at `~/.config/skill-master/private-terms.txt`, or
wherever `AGENT_SKILLS_PRIVATE_TERMS` points, and never inside this repository, because
the list is private itself. `skills/skill-master/guide/PRIVACY.md` describes its format.

A hit is fixed, not bypassed: replace it with a neutral stand-in (`user@example.com`,
`ABC-123`, `example-org/example-repo`, "a team", "the user") everywhere it occurs, and do
not commit with `--no-verify`. A scan cannot recognise real project detail inside an
example — a feature name, a file path, an error message — so read the change once more
for that before committing.

## Writing for the reader

Any skill that produces prose a human reads — a findings report, a commit message, a
proposed edit, any text a step hands back to the user — writes it to ASD-STE100
(Simplified Technical English) first: front-load the point, one idea per sentence,
active voice with a stated actor, short sentences (roughly 20-25 words), one
consistent term per concept, and jargon glossed on first use. Avoid idioms, phrasal
verbs, slang, and culturally-specific references ("hit the ground running," "give it
a shot") — say the same thing in plain, literal words instead. The goal is text a
competent reader can follow regardless of whether English is their first language,
not text that only reads well to a native speaker. This is the baseline, not one
rule among several. Whatever else that skill's own guide asks of the same output — a
severity tag, a category label, a length ceiling, a field a future edit adds —
composes on top of ASD-STE100-compliant wording; it never licenses relaxing it back
to passive, jargon-heavy, idiomatic, or multi-idea-per-sentence prose. Like the Privacy
rule, it covers every skill and every edit.

## The core split

Every skill has two parts, and they are never mixed:

- **`guide/`** is the actual content: the procedure the skill follows and the rules
  it checks or applies. It is plain Markdown and names no specific tool, so the same
  content works with any AI agent. This is the only part that carries real substance.
- **`adapters/<provider>/`** is a thin entry point, nothing more. Its only jobs are:
  (1) sit wherever that provider looks for an invocable skill, in whatever format that
  provider expects, and (2) map the guide's abstract capabilities (an independent
  check, a structured report, asking and waiting, and so on, whatever the specific
  guide calls for) onto that provider's real, concrete tools. An adapter reads
  `guide/`; it never adds a rule, changes one, or duplicates guide content into
  itself. If a provider lacks a capability the guide asks for, the guide's own
  procedure must already say what to do instead, that is the guide's job to handle,
  not the adapter's to work around.

## Delegating to a fresh context

A step that spawns a subagent, a separate session, or any other fresh context pays a
fixed cost before it does any useful work: that context has to load whatever content
it needs — a diff, a document, the guide layers — even when the delegating context
already has that same content loaded. Only pay that cost where it buys something the
current context cannot provide on its own:

- **Independence.** A check that has to genuinely try to disprove a candidate, not
  reread its own reasoning and agree with itself, must run somewhere separate — the
  one legitimate reason to delegate regardless of content size.
- **Capacity.** Content too large for one context to reason about carefully. This is
  a real limit, not a routine parallelization technique; delegate by size only once
  content actually crosses it, and reason in the current context otherwise.

Neither reason justifies delegating the same content twice for two different lenses
(a safety-focused pass and a style-focused pass, say): content already loaded in one
context can be reasoned about a second time for the cost of extra output tokens, not
another read. A guide's own `PROCEDURE.md` states this distinction explicitly
wherever it asks a later step to delegate, rather than leaving "when to spawn a fresh
context" to be rediscovered per skill.

## Structure

    skills/<skill-name>/
      README.md                    what this skill does, how to use it, how to extend it
      guide/                       the provider-neutral procedure and rules
        PROCEDURE.md                the entry point: the whole procedure, step by step
      adapters/<provider>/         one directory per supported provider
        <provider's entry file>    e.g. SKILL.md for Claude Code
        install.sh                 idempotent; wires the entry point into that provider
        guide -> ../../guide       relative symlink back into this skill's own guide/

Every skill directory is fully independent. Nothing is shared between skills, and
nothing skill-specific belongs at the repository root beyond the install dispatcher,
the repository-wide privacy hooks in `.githooks/`, and each skill's one-line entry in
the root `README.md`'s Skills list. The hooks are the one place the repository uses a
skill's internals: they run `skills/skill-master/guide/scripts/scan_private.py`, so a
change that moves or renames that script updates `.githooks/` in the same commit.

`guide/PROCEDURE.md` is always the name of the entry point: the file an adapter tells
the agent to read and follow step by step, named for what it does (the whole
procedure), not for the skill's domain. `guide/` may hold other files — checklists,
rule sets, reference tables the procedure loads — but only `PROCEDURE.md` runs on its
own; give every other file a name that describes what it actually holds.

A capability can genuinely degrade when the procedure can still do a lesser
version of the step without it. `PROCEDURE.md`'s step 0 must list every such
capability a later step relies on, each with a stated fallback for when it's
unavailable. A later step that assumes such a capability without step 0 naming it
(or naming it with no fallback) is a bug, not a stylistic choice. A hard
requirement with no meaningful degraded mode (a git skill without shell access,
for instance) does not belong in step 0; there is nothing to detect, because
there is no fallback to describe.

Never restate how many capabilities there are anywhere outside step 0 itself — not
the intro line, not an adapter's `SKILL.md`, not a skill's `README.md`. That count
is guide content; duplicating it outside its one source of truth is exactly the
kind of drift this file already warns adapters against.

## The install contract

Every skill must be installable the same way, through the repository's own
`install.sh <skill-name> <provider>`, exactly as its root `README.md` documents. For
the Claude Code provider specifically, that means the adapter's own `install.sh`:

- symlinks the whole `adapters/<provider>/` directory to `~/.claude/skills/<skill-name>`
  (never copies files, so a `git pull` updates the installed skill automatically),
- is idempotent, safe to run again after every pull,
- makes no other change: no `CLAUDE.md` edit, no hooks, no `settings.json` changes,
  since a manually-invoked skill needs none of that,
- accepts a `CLAUDE_HOME` environment variable override, for testing against a
  scratch directory instead of the real `~/.claude`.

A new provider's adapter follows the same shape, adapted to wherever and however that
provider actually finds an invocable skill.

## Steps to add or adopt a skill

Every skill here is generic, not only private, whether it is written fresh or ported.
A skill written for one team usually assumes that team's tools and setup. Move every
tool- or company-specific part into a variant file the guide chooses by detection — one
file per issue tracker, design tool, test runner or framework — so supporting another
one is one new file. Replace real examples with invented but realistic ones, and
descriptions of the author's own setup ("this machine has", "our team uses") with a
condition the skill detects or a question it asks. Drop any personal or team prefix
from the skill's name.

If the skill already exists somewhere else — a different repo, a different agent's
format, an existing skill with no repo of its own, a rough draft the user hands over —
port its actual substance into `guide/` and rebuild `adapters/claude-code/` from
scratch to this repo's contract. Do not carry over the source's file layout, naming,
or adapter mechanics just because that is how it arrived.

The next three paragraphs apply only to that porting case — skip ahead to the numbered
steps below if you're writing a skill fresh, with no existing source to work from.

A source written for one person or one platform usually has platform mechanics (tool
names, invocation syntax, permission lists) woven directly into its actual decision
logic. Pull them apart: the decision logic is provider-neutral guide content; the
platform mechanics belong in the adapter. This is a real rewrite, not a copy — expect
to reword sentences, not just move files.

Scrub the source for anything the Privacy rule forbids before it lands in `guide/` —
not only names and pronouns, but worked examples, file paths, and any cached values
the source already accumulated that might carry real project detail — see the Privacy
section above for the full rule. A mechanical port is the likeliest place to miss this,
because the temptation is to copy content wholesale rather than write it fresh.

Porting is also the moment to fix a genuine gap in the source's own logic if one turns
up — not just to restructure files around unchanged content. If the source hard-codes
an assumption that does not hold everywhere it will now be used, replace the
assumption with a check (inferred from evidence where possible) or an explicit
question, rather than porting the assumption as-is.

1. Pick `<name>` — where it fits, name it as the instruction a developer would
   actually say to invoke it, verb first then what it acts on: `code-better` reads
   as "code it better," `audit-content` as "audit the content." Verb-first names the
   action the skill performs, not just its subject, so the name alone tells you
   what invoking it does. Not mandatory: a skill that wraps an entire existing tool
   or domain rather than one synthesized action can just use that domain's own name
   instead (`git`).
2. Write `skills/<name>/guide/` — the procedure and rules, naming no specific tool.
   Copy the shape from an existing skill and change only what the new domain
   requires.
3. Write `skills/<name>/adapters/claude-code/` — the entry point, the symlink, and an
   `install.sh` following the contract above. Add other providers' adapters if asked.
4. Write `skills/<name>/README.md` — what it does, how to invoke it, how to extend it.
   Do not restate this file's content in it; link back here for the general structure.
5. Add one line to the root `README.md`'s "Skills" list: the skill's name, linked to
   its own `README.md`. No description there, the skill's own README carries that.
6. Install it (`./install.sh <name> claude-code` from the repository root), so the
   review below can find it by name.
7. Review it before the first commit, in this order — each pass catches what the
   previous one cannot. Run each pass yourself by reading and following that skill's
   guide; the request to add or adopt a skill is the request to review it, so do not
   wait for the user to invoke the review skills.

   1. **Structure and privacy** — `skills/skill-master/guide/PROCEDURE.md`, Stage 2A, on
      the new skill. It checks the metadata, tool permissions, cross-references and size,
      and runs the privacy pass. Without a shell, run the checklist by hand and say so.
   2. **Content** — `skills/audit-content/guide/PROCEDURE.md` on the skill's whole
      directory as one set. It finds rules that conflict across files, stale or redundant
      passages, and unclear wording — problems a structural check does not examine.
   3. **Real project detail** — reread the skill once more for examples, file paths and
      feature names that came from real work. No scan recognises them.

   Collect the findings of all three passes, then ask the user once which to fix. The
   commit hooks still run the privacy scan on every later change.
8. Invoke it once to confirm it actually loads and routes. A skill that needs a real task
   or the user's answers is started on a real request and stopped at its first approval
   gate; that proves it runs without doing the task.
9. Compare the result against the other skills in `skills/`:

   - file layout
   - `PROCEDURE.md`'s capability-detection-with-fallback pattern
   - any step that delegates to a fresh context — only for independence or genuine
     capacity limits, never as routine parallelization
   - the adapter entry file's frontmatter keys
   - `README.md`'s section order

   Propose reconciling, with the developer's confirmation, any place it drifts without
   good reason. Matching an existing skill's shape is not optional polish; it is what
   lets a developer use any skill in this repo without relearning conventions per skill.
10. Report where the adoption stands, one line per step, and end with a verdict — so
    the user never has to work out from the conversation whether the job is finished:

    ```
    ━━━━━━━━━━━━━━━━━━━━━━━━━ ADOPTION: <name> ━━━━━━━━━━━━━━━━━━━━━━━━━
    ✅ 1–5  Written (guide, adapter, README, root README line)
    ✅ 6    Installed
    ✅ 7    Reviewed — structure and privacy · content · real project detail
    ⏳ 8    Test invocation — waiting for a real request
    ✅ 9    Compared with the other skills
    ⏳      Committed

    NOT DONE — waiting on: <what is pending, and on whom>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```

    Use ✅ for a step that is finished, ❌ for one that failed or has open findings, and
    ⏳ for one waiting on something. The last line is either `DONE — ready to commit`
    (or `DONE — committed`) or `NOT DONE — waiting on:` followed by exactly what is
    pending and who has to act.
