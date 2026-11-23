# Format — Claude Code

## Where skills live

- **Personal skills** (`<skills-root>`): `~/.claude/skills/<skill-name>/SKILL.md`. A directory counts as
  a skill only if it holds a `SKILL.md`:

  ```bash
  for d in ~/.claude/skills/*/; do [ -f "$d/SKILL.md" ] && basename "$d"; done
  ```

  A skill directory may be a symlink into a repository; PROCEDURE.md Stage 0 then applies that
  repository's contribution rules.
- **Project skills**: `<repo>/.claude/skills/<skill-name>/SKILL.md`, shared through the repository.
- **Plugin skills** (read-only): everything under `~/.claude/plugins/`. That directory is a plugin
  cache; the next marketplace update overwrites any edit made there. Edit a copy, validate it, and ship
  the change through the plugin's own source repository. `~/.claude/plugins/installed_plugins.json`
  lists the plugin versions that actually load.
- **Reload note** for Stage 5: "Claude Code picks this up immediately — no restart needed. If the skill
  does not appear in the skill list, open a new session."

## Entry file

`SKILL.md`, YAML frontmatter followed by a Markdown body:

```
---
name: {skill-name}
description: "{what it does, plus the contexts and phrases that should trigger it}"
argument-hint: "[description of expected arguments, or omit if none]"
allowed-tools: {tools used; see Tool permissions}
---

# {skill-name} — {short title}

{one paragraph — what this skill does and when to use it}

**Constraint:** {hard rules, e.g. "always confirm before writing files", "never emit emojis"}

**Input:** `$ARGUMENTS` — {expected input}

---

## Step 1 — {step title}

{instructions}

---

## Final step — Output

{what to return or display; end with "Stop. No closing remarks." if the skill should terminate cleanly}
```

## Naming

Lowercase letters, digits and single hyphens (kebab-case), 64 characters at most. The `name` field
matches the directory name.

## Description and triggering

- `description` is the entire triggering mechanism: Claude Code shows each skill's name and description
  to the model, which decides from that pair alone whether to load the skill. Put all when-to-use
  information there and nowhere else.
- Claude under-triggers skills more often than it over-triggers them, so name the
  contexts explicitly rather than describing the skill abstractly. Compare "Builds internal dashboards"
  with "Builds internal dashboards. Use whenever the user mentions dashboards, data visualization, or
  internal metrics, even without saying dashboard."
- **Always quote the value.** An unquoted value containing a colon followed by a space parses as a YAML
  mapping and breaks the frontmatter.
- At most 1024 characters, and no angle brackets.
- A skill that must run only when the user types its name says so at the start of its description,
  e.g. "Manual invocation only — never invoke this skill on your own. … Load it only when the user
  explicitly types /skill-name."

## Metadata keys

- Required: `name`, `description`.
- Optional: `argument-hint`, `allowed-tools`, `license`, `metadata`, `compatibility`.
- `argument-hint` is valid in Claude Code but absent from the cross-agent Agent Skills specification;
  the validator accepts it through `--extra-keys`. Do not "fix" a skill by deleting it.
- Keys Claude Code does not read are inert and misleading — `version`, for instance. Remove them. If
  Claude Code documents a key not listed here, pass it to the validator's `--extra-keys` rather than
  deleting it.

## Tool permissions

- `allowed-tools` must list every tool the skill uses and nothing it does not. A tool absent from the
  list cannot be called; a tool listed but unused widens permissions for no reason. With no
  `allowed-tools` key at all, the skill is not restricted to a list.
- Comma-separated, no trailing comma, no brackets around the list; parentheses appear only inside a
  scoped entry such as `Bash(gh:*)`.
- **Scope every static Bash command to a pattern instead of declaring bare `Bash`.** For each distinct
  command whose exact text is fixed at draft time (`git status`, `npm run lint:fix`, `gh pr create`),
  add `Bash(<command prefix>:*)`. This is strictly narrower than bare `Bash` and also removes the
  permission prompt for exactly those commands. Keep bare `Bash` only for a command resolved at
  runtime, or for a compound construct no prefix pattern can match — a `for` loop, a pipeline. A skill
  containing even one of those keeps bare `Bash`, and scoped entries alongside it narrow nothing.
- List the Skill tool if the body invokes another skill, and each MCP tool by its full
  `mcp__<server>__<tool>` name.

## Arguments

- `$ARGUMENTS` is the user's input, used consistently, with no competing placeholder style.
- `${CLAUDE_SKILL_DIR}` is the skill's own directory, for paths to its bundled files.

## Asking the user

The structured-choice mechanism is the `AskUserQuestion` tool: up to 4 questions per call, 2–4 options
per question, a header chip of at most 12 characters, and an automatic "Other" option for free text.

## Review checks

- `allowed-tools` follows every rule in "Tool permissions" above, including Bash scoping.
- The description is quoted and within limits; `argument-hint` is present when the skill takes input.
- The body uses `$ARGUMENTS`, not another placeholder.

## Validation

`<py>` and `<guide>` come from PROCEDURE.md Stage 0.

```bash
# validator, one skill
<py> <guide>/scripts/validate.py <skill-dir> --extra-keys argument-hint

# body audit, every skill
<py> <guide>/scripts/audit_bodies.py --root ~/.claude/skills

# overlap report, personal skills plus installed plugins
<py> <guide>/scripts/overlap.py --root ~/.claude/skills --plugins-manifest ~/.claude/plugins/installed_plugins.json

# description quoting, dry run then apply
<py> <guide>/scripts/quote_descriptions.py --root ~/.claude/skills
<py> <guide>/scripts/quote_descriptions.py --root ~/.claude/skills --apply

# reference check (standard library only, plain python3)
python3 <guide>/scripts/check_refs.py <skill-dir>
python3 <guide>/scripts/check_refs.py <skill-dir> --baseline <workspace>/skill-snapshot

# privacy scan, shareable skills (standard library only, plain python3)
python3 <guide>/scripts/scan_private.py <skill-dir> --terms <private-terms>
```

## Evaluation harness

Stages 6–8 run on Anthropic's skill-creator, cloned to disk with the `claude-plugins-official`
marketplace:

```bash
SC=~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
```

If `$SC` is absent, tell the user:

```
Anthropic's skill-creator files are not on disk. To get them:
  /plugin marketplace add anthropics/claude-plugins-official
(or, if already added)
  /plugin marketplace update claude-plugins-official
Do not install the plugin — this skill only reads its files.
```

Its scripts use `X | None` annotations, so they need Python 3.10 or later. Run them with `python3`,
except packaging, which parses frontmatter and so runs with `<py>`.

| Name | File or command |
| --- | --- |
| `<schemas>` | `$SC/references/schemas.md` |
| `<grader>` | `$SC/agents/grader.md` — `grading.json`'s `expectations` entries use the fields `text`, `passed` and `evidence`, which the viewer reads |
| `<aggregate>` | `cd "$SC" && python3 -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` — writes `benchmark.json` and `benchmark.md` |
| `<analyzer>` | `$SC/agents/analyzer.md` |
| `<viewer>` | `nohup python3 "$SC/eval-viewer/generate_review.py" <workspace>/iteration-N --skill-name "<name>" --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &` — add `--previous-workspace <workspace>/iteration-<N-1>` from iteration 2. Two tabs: Outputs for each case and its feedback box, Benchmark for the numbers. The user clicks "Submit All Reviews"; read `feedback.json`, then stop the process |
| `<comparator>` | `$SC/agents/comparator.md` |
| `<review-page>` | `$SC/assets/eval_review.html` — replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array (unquoted; it is a JavaScript assignment), `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__`; write it to a temporary file and open it. "Export Eval Set" saves `eval_set.json` to the user's downloads folder |
| `<tuning-loop>` | `cd "$SC" && python3 -m scripts.run_loop --eval-set <path> --skill-path <path> --model <model-id> --max-iterations 5 --verbose` — needs the `claude` CLI; prints `best_description` and opens an HTML report |
| Packaging (Stage 8) | `cd "$SC" && <py> -m scripts.package_skill <path-to-skill-folder>` |

Each fresh-context run's completion notice carries `total_tokens` and `duration_ms`; that is the only
place they appear, so record them in `timing.json` at once (EVALS.md Step 4).

## Pitfalls

- An unquoted `description` containing ": " is invalid YAML. Claude Code tolerates it today; stricter
  tools reject it.
- A tool used only from a bundled file looks unused to the body audit, which reads `SKILL.md` alone.
  The reference check reads every file.
