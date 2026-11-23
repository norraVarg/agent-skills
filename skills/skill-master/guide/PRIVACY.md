# Privacy pass for shareable skills

Read this when the target skill is shareable (PROCEDURE.md Stage 0 "Sharing"): in Stage 3R before
showing a draft, in Stage 2A and Stage A when auditing, and whenever a personal skill is being made
shareable. A personal skill never needs it.

A shareable skill may reach people who do not know the author, their employer or their machine. The
skill's behaviour can come from real work; its wording must not identify where that work happened.

## What counts as private

- **People** — names, usernames, handles, email addresses, and pronouns that describe a real person.
- **Organizations** — employers, clients, teams, products, internal project or service names.
- **Systems** — internal hostnames and URLs, repository and organization names, ticket keys and
  ticket-project prefixes, channel names, dashboards, account IDs.
- **Machines** — home-directory paths with a username in them, hostnames, IP addresses.
- **Secrets** — tokens, keys, passwords, private-key blocks. A secret in a skill is also a security
  incident, not only a privacy one: tell the user to rotate it.
- **Real detail in examples** — a worked example, file path, feature name or error message copied from a
  real project. This is the category a scan cannot catch, so it gets its own manual step below.

Public tool and product names (an issue tracker, a design tool, a cloud provider, an AI model) are not
private. They make a skill specific to a tool, which `HOUSE-STYLE.md` handles with variant files, not a
privacy problem.

## The private-terms list

The scan matches built-in patterns (email addresses, home paths, IP addresses, secret-shaped tokens) and
the user's own list of private terms at `<private-terms>`. The list stays outside every repository,
because the list itself is private: never copy its contents into a skill, a report, a commit message or
any other file.

One term per line, matched case-insensitively. Lines starting with `#` are comments. A line starting
with `!` allows that exact text even if a pattern matches it — a public no-reply address, for instance.
A term ending in `-` is a ticket prefix: it matches only when a digit follows, so `ABC-` catches
`ABC-123` but not a hyphenated word.

If `<private-terms>` does not exist, offer to create it before scanning. Ask the user for: their name and
usernames, email addresses, employer and team names, client names, ticket-project prefixes, internal
domain names, and repository or organization names. Offer candidates the user can accept or reject —
the name and email from the local version-control configuration, the organization in the current
repository's remote — but write only what the user confirms. Without the list, only the built-in
patterns run; say so in the report.

## Step 1 — Scan

Run `<format>`'s privacy scan on the draft (Stage 3R) or the skill (Stage 2A, Stage A, Stage 5V). Do
not pass `--baseline` for a shareable skill: a hit inherited from an older version is still a leak. The
scan reads every text file in the skill, following symlinked directories.

## Step 2 — Review every hit

For each hit, decide:

- **Real leak** → replace it with a neutral stand-in that keeps the meaning: `user@example.com`,
  `ABC-123`, `example-org/example-repo`, `https://tracker.example.com`, "a team", "the user". Replace
  every occurrence, not only the one reported, and check the examples around it still make sense.
- **Secret** → remove it, and tell the user to rotate it at its source before anything else.
- **False positive** → a public address or a term that is also an ordinary word. Leave it, and suggest
  an `!` allow line or a narrower term so the next scan stays quiet.

## Step 3 — Manual review

Read the whole skill once more for what no pattern catches:

- Examples, sample data, file paths and feature names that came from a real project. Rewrite them as
  invented but realistic ones.
- Descriptions of the author's own setup — "this machine has", "our team uses", "my company's" — that
  should become conditions the skill detects or asks about.
- Pronouns describing a specific person. Use "the user", "they".

## Step 4 — Report

Add one line to the draft box (Stage 4), the audit row (Stage 2A, Stage A) or the regression report
(Stage 5V):

```
Privacy: <n> files scanned, <n> hits fixed, <n> allowed, manual review done — private-terms list <used | missing>
```

A shareable skill does not reach Stage 4 with an unresolved hit.
