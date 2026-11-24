# Tracker variant — Jira

## Detect

A key matching `[A-Z][A-Z0-9]+-[0-9]+` (e.g. `ABC-123`), or an `*.atlassian.net/browse/<KEY>` URL.

## Fetch

- The issue, for each key: summary, description, acceptance criteria (often a custom field that a
  compact view leaves out — request the full field set), attachments, links.
- Its comments, for each key. Comments frequently override the description; when they conflict, the
  conflict is a question, not a choice to make silently.
- Without issue tracker access, use Step 0's fallback.

## Related items

One level deep, with a search for the parent epic and the issues linked as blocks, is blocked by,
relates to, or duplicates. Read the epic for context and constraints, linked
issues for overlapping or conflicting requirements.

## Spec key

The first Jira key, as is (`ABC-123`).

## Pitfalls

- Images attached to the issue are design sources too — hand them to the images design variant.
- Figma links often sit in comments or attachments rather than the description.
