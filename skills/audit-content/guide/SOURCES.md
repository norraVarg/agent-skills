# Sources

How to resolve a target into raw text, once identified (`PROCEDURE.md`, step 1). Named
here in the abstract; each provider's adapter documents which concrete mechanism
fulfils each one on that platform.

- **Something already in the session** — a draft, a message, a file just written, a
  ticket being discussed. Use what is already visible; no fetch needed.
- **The system clipboard** — the user says "what's on my clipboard," or pastes nothing
  but refers to "this" or "what I just copied." Read the clipboard.
- **A link** — a URL to a web page, document, or other resource named or pasted by the
  user. Fetch it.
- **A local file** — a path named by the user, or a file the agent just wrote or edited.
  Read it.
- **A set of related documents** — a directory, a skill, a guide, a docs tree: several
  files read as one body of work. Read all of them, not a sample. The set is the target,
  so both the documents and the relationships between them are in scope.
  Two documents belong to the same set when they serve the same purpose or are read by
  the same consumer: files one procedure loads together, a summary or index and the
  documents it covers, a template and the files copied from it, a README and the guide
  it describes. Sharing a folder is a weak signal on its own; a shared reader or a
  shared job is the test.
- **A GitHub pull request or issue, and its comments** — a PR/issue number or URL. Fetch
  the description and, if the user's ask concerns them, the comment thread.
- **A Jira ticket** — a ticket key or link. Fetch its description and comments.
- **A Confluence page** — a page name or link. Fetch its content.
- **An artifact already published in this session** — something the agent generated and
  shared earlier in the conversation. Re-read its published content, not a summary of
  it.
- **The agent's own not-yet-sent draft** — a reply, a proposal, a ticket update the
  agent is about to send but has not sent yet. Audit it before sending, using the draft
  text directly.

If the source needed is not actually reachable (no access to the ticket system, a broken
link, a file that does not exist), say so and stop rather than fabricating content to
audit.

## Disambiguation

If, after checking the user's own words, more than one of the above is a plausible
target — or none is — ask the user which one before doing anything else. Never guess
silently (`PROCEDURE.md`, step 1).
