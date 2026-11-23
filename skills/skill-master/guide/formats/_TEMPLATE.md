# Format — <agent name>

Copy this file to `formats/<agent>.md` and fill every section. PROCEDURE.md and the other guide files
reach into a format by these section names, so keep them exactly; write "Not supported" in a section
the agent has no equivalent for, and say what the procedure should do instead.

## Where skills live

The user's own skills directory (`<skills-root>`), any project-level location, and any read-only
location (plugin or package caches) with how a change to one ships instead. How to list installed
skills, which file marks a directory as a skill, and whether a new or edited skill needs a reload — the
one-line note Stage 5's size report ends with.

## Entry file

The entry file's name and a complete template: metadata block plus body, with every placeholder the
house style expects (title, one-paragraph purpose, constraints, input, numbered steps, final output).

## Naming

The rules a skill name must satisfy (characters, length, relation to the directory name).

## Description and triggering

How the agent decides to load a skill, the description's length and character limits, quoting rules,
and how to write a skill that must only run when invoked explicitly.

## Metadata keys

Every key the agent reads, required or optional, and keys commonly seen that the agent ignores.

## Tool permissions

How a skill declares the tools it may use, the declaration's syntax, how narrowly to scope it, and what
an absent declaration means.

## Arguments

The placeholder for the user's input, and how a skill refers to its own bundled files.

## Asking the user

The structured-choice mechanism a skill uses to ask questions, and its limits (questions per call,
options per question, label lengths).

## Review checks

Format-specific items for Stage 3R that `REVIEW-CHECKLIST.md` cannot state without naming this format.

## Validation

Exact commands for: the validator on one skill, the body audit across all skills, the overlap report,
the description-quoting pass (dry run and apply), the reference check (with and without
`--baseline`), and the privacy scan. Use `<py>` and `<guide>` from PROCEDURE.md, and name every argument the scripts need for
this format. If a script does not fit this format, say what replaces it.

## Evaluation harness

What Stages 6–8 run on for this agent: where the harness lives, how to install it, and the file or
command behind each name `EVALS.md` and `DESCRIPTION-TUNING.md` use — `<schemas>`, `<grader>`,
`<aggregate>`, `<analyzer>`, `<viewer>`, `<comparator>`, `<review-page>`, `<tuning-loop>` — plus the
packaging command for Stage 8. "Not supported" makes those stages unavailable for this format.

## Pitfalls

Format behaviours that have caused real breakage.
