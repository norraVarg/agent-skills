# Tracker variant — GitHub Issues

## Detect

A `github.com/<owner>/<repo>/issues/<n>` URL, or `<owner>/<repo>#<n>`. A bare `#<n>` refers to the
current repo's remote — confirm the repo before fetching.

## Fetch

- `gh issue view <n> --repo <owner>/<repo> --json title,body,labels,milestone,assignees,url`
- `gh issue view <n> --repo <owner>/<repo> --comments` for the discussion. Comments frequently
  override the body; when they conflict, the conflict is a question.
- If `gh` is not authenticated for that repo, ask the user to run `gh auth login` or paste the issue.

## Related items

One level deep: issues and PRs referenced in the body or comments (`#<n>`, URLs), sub-issues, and
the milestone description. Read linked PRs only for their description, not their diff.

## Spec key

`<repo>-<n>` (e.g. `my-app-42`), so keys from different repos never collide.

## Pitfalls

- Images in the body are `user-attachments` URLs — download them to a temporary folder for the
  images design variant only after asking the user.
- Task lists (`- [ ]`) in the body are usually the acceptance criteria; treat unchecked ones as in scope
  unless the user says otherwise.
