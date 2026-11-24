# implement-frontend

Takes a frontend task from requirement to a tested, design-faithful change, asking instead of
assuming at every gap between the requirement, the design and the code.

- Reads the requirement from an issue tracker, or from text, a design or screenshots given directly,
  and analyses the design and the repo before writing anything.
- Asks grouped clarifying questions until nothing is open, then writes a **refined requirement spec**
  for approval. The spec stays outside the repository and is the single source of truth from then on.
- Works **test-first**: behaviour tests from the agreed acceptance criteria fail first, then the
  implementation makes them pass. Tests are named for the behaviour they check; the spec maps them
  to its acceptance criteria.
- Checks **visual fidelity** against the design in the running app, state by state and viewport by
  viewport.
- Routes every change after approval through the spec, and reports coverage per acceptance
  criterion at the end. Commits nothing.
- **Variants** (`guide/variants/`) hold everything specific to one issue tracker, design tool, test
  runner or framework, chosen by detection. Scope today is React + TypeScript.

See the repository root's [CONTRIBUTING.md](../../CONTRIBUTING.md#the-core-split) for how `guide/`
and `adapters/` relate to each other; this file only covers what `implement-frontend` itself does.

## How to install

From the repository root:

```bash
./install.sh implement-frontend claude-code
```

## How to use it

Invoke the skill with an issue key or URL, or with requirement text, optionally followed by design
URLs or image paths. It:

1. Detects what the platform can do and chooses the variants for the tracker, design source,
   framework, test runner and e2e framework.
2. Gathers the requirement and the design, then analyses the repo's conventions and existing tests.
3. Asks its questions in grouped rounds, announcing how many there are, until every one is resolved.
4. Writes the refined spec and waits for your approval.
5. Writes failing behaviour tests, then the implementation, showing each diff before writing.
6. Compares the running app with the design and lists every mismatch.
7. Reports coverage per acceptance criterion and the full check commands for you to run.

The spec is resumable: invoking the skill again with the same issue key, or with the spec's slug
when there is no tracker, continues where the last run stopped.

## How to extend

**Add a variant** — a framework, issue tracker, design source, test runner or e2e framework. Copy the
kind's `guide/variants/<kind>/_TEMPLATE.md` to a new file in the same folder, fill it in, and add one
row to the variants table in `guide/PROCEDURE.md`, Step 0. No step changes.

**Add a provider adapter.** Follow the general steps in the repository root's
[CONTRIBUTING.md](../../CONTRIBUTING.md#steps-to-add-or-adopt-a-skill); map `guide/PROCEDURE.md`'s
placeholders and capabilities onto whatever that provider actually has.
