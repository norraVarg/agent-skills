# <Domain name>

<!--
How to add a domain:
1. Copy this file to `domains/<domain-name>.md` (lowercase, hyphenated).
2. Replace the heading and fill the sections below. Delete sections that do not
   apply; add sections only for concerns unique to this domain.
3. Add one row to the Domain table in `RULE-LAYERS.md`'s Classify section with the
   signals that identify a project of this kind (dependencies, files, folders).
4. Remove this comment block.
Rules here must not contradict `universal/`. If a universal rule needs a domain
exception, propose the change to the universal rule instead.
-->

Loaded when <the condition under which this domain applies>.

## Boundaries and contracts
- <How this kind of program receives input and returns output; what must be
  validated where.>

## State and data
- <What holds state, for how long, and who owns it.>

## Failure and reliability
- <What can fail, what the user or caller sees, what is retried.>

## Observability
- <What is logged or measured, and what must never be.>

## Security
- <Threats specific to this domain and the default defences.>

## Performance
- <What is measured, and what is optimised only when measured.>
