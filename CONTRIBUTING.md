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
smuggled in through a worked example, a file path, a feature name, or a skill's own
accumulated state. This applies to every skill added here, not only the ones already present, and to
any edit, not only adding a new one. It matters most right here, though, at the
moment new content enters the repo. Before committing, search the whole repository
for anything that would identify you or your organization.

## The core split

Every skill has two parts, and they are never mixed:

- **`guide/`** is the actual content: the procedure the skill follows and the rules
  it checks or applies, plus any state the procedure itself reads and writes as it
  runs (a learned-command table, a candidate-rules file). It is plain Markdown and
  names no specific tool, so the same content works with any AI agent. This is the
  only part that carries real substance.
- **`adapters/<provider>/`** is a thin entry point, nothing more. Its only jobs are:
  (1) sit wherever that provider looks for an invocable skill, in whatever format that
  provider expects, and (2) map the guide's abstract capabilities (an independent
  check, a structured report, asking and waiting, and so on, whatever the specific
  guide calls for) onto that provider's real, concrete tools. An adapter reads
  `guide/`; it never adds a rule, changes one, or duplicates guide content into
  itself. If a provider lacks a capability the guide asks for, the guide's own
  procedure must already say what to do instead, that is the guide's job to handle,
  not the adapter's to work around.

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
nothing skill-specific belongs at the repository root beyond the install dispatcher
and each skill's one-line entry in the root `README.md`'s Skills list.

`guide/PROCEDURE.md` is always the name of the entry point: the file an adapter tells
the agent to read and follow step by step, named for what it does (the whole
procedure), not for the skill's domain. `guide/` may hold other files — checklists,
rule sets, reference tables the procedure loads — but only `PROCEDURE.md` runs on its
own; give every other file a name that describes what it actually holds.

`PROCEDURE.md`'s step 0 must list every capability a later step relies on that can
genuinely degrade — something the procedure can still do a lesser version of
without — each with a stated fallback for when it's unavailable. A later step that
assumes such a capability without step 0 naming it (or naming it with no fallback)
is a bug, not a stylistic choice. A hard requirement with no meaningful degraded
mode (a git skill without shell access, for instance) does not belong in step 0;
there is nothing to detect, because there is no fallback to describe.

Never restate how many capabilities there are anywhere outside step 0 itself — not
the intro line, not an adapter's `SKILL.md`, not a skill's `README.md`. That count
is guide content; duplicating it outside its one source of truth is exactly the
kind of drift this file already warns adapters against, and it has already broken
twice.

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

If the skill already exists somewhere else — a different repo, a different agent's
format, an existing skill with no repo of its own, a rough draft the user hands over —
port its actual substance into `guide/` and rebuild `adapters/claude-code/` from
scratch to this repo's contract. Do not carry over the source's file layout, naming,
or adapter mechanics just because that is how it arrived.

The next three points apply only to that porting case — skip ahead to the numbered
steps below if you're writing a skill fresh, with no existing source to work from.

A source written for one person or one platform usually has platform mechanics (tool
names, invocation syntax, permission lists) woven directly into its actual decision
logic. Pull them apart: the decision logic is provider-neutral guide content; the
platform mechanics belong in the adapter. This is a real rewrite, not a copy — expect
to reword sentences, not just move files.

Scrub the source for anything the Privacy rule forbids before it lands in `guide/` —
not only names and pronouns, but worked examples, file paths, and any state the
source already accumulated (a learned-command table, cached values) that might
carry real project detail — see the Privacy section above for the full rule. A
mechanical port is the likeliest place to miss this, because the temptation
is to copy content wholesale rather than write it fresh.

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
3. Write `skills/<name>/adapters/claude-code/` — the entry point, the symlink, and an
   `install.sh` following the contract above. Add other providers' adapters if asked.
4. Write `skills/<name>/README.md` — what it does, how to invoke it, how to extend it.
   Do not restate this file's content in it; link back here for the general structure.
5. Add one line to the root `README.md`'s "Skills" list: the skill's name, linked to
   its own `README.md`. No description there, the skill's own README carries that.
6. Install it (`~/agent-skills/install.sh <name> claude-code`) and invoke it once to
   confirm it actually resolves and runs before considering it done.
7. Compare the result against the other skills in `skills/` — file layout,
   `PROCEDURE.md`'s capability-detection-with-fallback pattern, `rules/user-rules.md`'s
   format and header wording, `README.md`'s section order — and propose reconciling,
   with the developer's confirmation, any place it drifts without good reason.
   Matching an existing skill's shape is not optional polish; it is what lets a
   developer use any skill in this repo without relearning conventions per skill.
