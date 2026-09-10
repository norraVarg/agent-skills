# Adding a skill

This is what an agent asked to add a new skill to this repository needs to know.
Follow this exactly; do not invent a different structure.

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

## Structure

    skills/<skill-name>/
      README.md                    what this skill does, how to use it, how to extend it
      guide/                       the provider-neutral procedure and rules
      adapters/<provider>/         one directory per supported provider
        <provider's entry file>    e.g. SKILL.md for Claude Code
        install.sh                 idempotent; wires the entry point into that provider
        guide -> ../../guide       relative symlink back into this skill's own guide/

Every skill directory is fully independent. Nothing is shared between skills, and
nothing skill-specific belongs at the repository root beyond the install dispatcher
and each skill's one-line entry in the root `README.md`'s Skills list.

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

## Steps to add a new skill

1. Write `skills/<name>/guide/` — the procedure and rules, naming no specific tool.
2. Write `skills/<name>/adapters/claude-code/` — the entry point, the symlink, and an
   `install.sh` following the contract above. Add other providers' adapters if asked.
3. Write `skills/<name>/README.md` — what it does, how to invoke it, how to extend it.
   Do not restate this file's content in it; link back here for the general structure.
4. Add one line to the root `README.md`'s "Skills" list: the skill's name, linked to
   its own `README.md`. No description there, the skill's own README carries that.
5. Install it (`~/agent-skills/install.sh <name> claude-code`) and invoke it once to
   confirm it actually resolves and runs before considering it done.

## Privacy

Nothing in this repository may identify a person, an employer, or a specific
machine, in any skill, in any layer: no names, emails, employers, or machine paths.
This applies to every skill added here, not only the ones already present. Before
committing, search the whole repository for anything that would identify you.
