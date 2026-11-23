#!/usr/bin/env python3
"""Body-level audit for SKILL.md skills — the checks validate.py cannot make.

Usage: audit_bodies.py --root <skills-dir> [--root <skills-dir> ...]

Reports only mechanically verifiable findings, to keep false positives low:
  - tools used in the body but absent from allowed-tools
  - tools declared but never referenced in the body
  - step/stage cross-references that point at nothing
  - mixed argument-placeholder styles
  - description fragility (unquoted scalar containing ": ")
"""

import re
import sys
from pathlib import Path

import yaml

# Bash commands that are shell builtins or so generic that Bash alone covers them.
GENERIC = {"cd", "echo", "for", "if", "then", "fi", "done", "do", "export", "printf",
           "cat", "set", "while", "case", "esac", "return", "exit", "local", "read"}


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else (None, text)


def declared_tools(fm):
    raw = fm.get("allowed-tools") or ""
    if isinstance(raw, list):
        return [str(t).strip() for t in raw if str(t).strip()]
    return [t.strip() for t in raw.split(",") if t.strip()]


def bash_commands(body):
    """First token of each line inside ```bash fences."""
    cmds = set()
    for block in re.findall(r"```bash\n(.*?)```", body, re.DOTALL):
        for line in block.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tok = re.match(r"([A-Za-z0-9_./-]+)", line)
            if tok:
                name = tok.group(1).split("/")[-1]
                if name not in GENERIC:
                    cmds.add(name)
    return cmds


def covers_bash(declared, cmd):
    """Does any declared entry authorize this bash command?"""
    for d in declared:
        if d == "Bash":
            return True
        m = re.match(r"Bash\(([^:)]+)", d)
        if m and m.group(1).split("/")[-1] == cmd:
            return True
    return False


def audit(path):
    text = path.read_text()
    fm_text, body = split_frontmatter(text)
    findings = []
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        return [f"frontmatter does not parse: {str(e).splitlines()[0]}"]

    declared = declared_tools(fm)
    declared_set = set(declared)

    # Description fragility
    raw_desc_line = next((l for l in fm_text.split("\n") if l.startswith("description:")), "")
    val = raw_desc_line[len("description:"):].strip()
    unquoted = val[:1] not in ("'", '"')
    if unquoted and ": " in fm.get("description", ""):
        findings.append("description is an unquoted scalar containing ': ' — invalid YAML per spec")
    elif unquoted:
        findings.append("advisory: description unquoted (parses today, fragile if a colon is added)")

    # MCP tools named in body but not declared
    for tool in sorted(set(re.findall(r"mcp__[A-Za-z0-9_-]+__[A-Za-z0-9_]+", body))):
        if tool not in declared_set:
            findings.append(f"body references {tool} but it is not in allowed-tools")

    # Bash commands not covered
    if declared:
        for cmd in sorted(bash_commands(body)):
            if not covers_bash(declared, cmd):
                findings.append(f"body runs `{cmd}` but allowed-tools does not authorize it")

    # Named non-Bash tools used in body but undeclared.
    # Skipped entirely when allowed-tools is absent: no key means no restriction.
    if declared:
        for tool in ("Read", "Write", "Edit", "AskUserQuestion", "ToolSearch", "Skill", "Agent", "Task"):
            if tool in declared_set:
                continue
            for m in re.finditer(rf"\b{tool}\b tool|via the `{tool}`|`{tool}` tool", body):
                # A skill documenting how *others* invoke it names the Skill tool without
                # needing it declared. Look at the surrounding sentence to tell direction.
                ctx = body[max(0, m.start() - 200):m.end() + 200]
                if tool == "Skill" and re.search(
                        r"for other skills|other skills.{0,40}invoke|invoke .{0,30}this skill|"
                        r"calling contract", ctx, re.IGNORECASE):
                    continue
                findings.append(f"body names the {tool} tool but it is not in allowed-tools")
                break

    # Declared but unused
    for d in declared:
        base = re.match(r"([A-Za-z0-9_]+)", d)
        if not base:
            continue
        name = base.group(1)
        if name == "Bash":
            inner = re.match(r"Bash\(([^:)]+)", d)
            if inner and inner.group(1).split("/")[-1] not in bash_commands(body) \
                    and inner.group(1).split("/")[-1] not in body:
                findings.append(f"allowed-tools declares {d} but the body never uses it")
        elif d.startswith("mcp__"):
            # Bodies conventionally use the bare operation name (createJiraIssue), not the
            # full mcp__server__operation id, so match the last segment too.
            short = d.split("__")[-1]
            if d not in body and not re.search(rf"\b{re.escape(short)}\b", body):
                findings.append(f"allowed-tools declares {d} but the body never references it")
        elif not re.search(rf"\b{name}\b", body):
            # Read/Write/Edit are ambient — a body can say "read the file" or "overwrite it"
            # and use the tool without ever naming it, so absence is weak evidence. Specialty
            # tools (Grep, Agent, Skill, …) are named when used, so absence is real.
            level = "advisory: " if name in ("Read", "Write", "Edit") else ""
            findings.append(
                f"{level}allowed-tools declares {name} but the body never references it")

    # Step/stage cross-references
    headings = set()
    for m in re.finditer(r"^#+\s*(?:Step|Stage)\s+([0-9]+[A-Za-z]*)", body, re.MULTILINE):
        headings.add(m.group(1))
    if headings:
        for m in re.finditer(r"(?:Step|Stage)\s+([0-9]+[A-Za-z]*)", body):
            ref = m.group(1)
            if ref not in headings and ref.rstrip(".") not in headings:
                base = re.match(r"([0-9]+)", ref)
                if not (base and base.group(1) in headings):
                    findings.append(f"references Step/Stage {ref} which has no heading")
                    break

    # Placeholder style. `$1` is deliberately excluded — it collides with shell positional
    # parameters and JS regex backreferences far more often than it means "the argument".
    styles = [s for s in ("$ARGUMENTS", "<input>", "{{args}}") if s in body]
    if len(styles) > 1:
        findings.append(f"mixed argument placeholders: {', '.join(styles)}")

    return findings


def roots(argv):
    """Every --root DIR given on the command line."""
    out = [Path(argv[i + 1]).expanduser() for i, a in enumerate(argv) if a == "--root"]
    if not out:
        print("usage: audit_bodies.py --root <skills-dir> [--root <skills-dir> ...]")
        sys.exit(2)
    return out


def main():
    total = 0
    dirs = [d for root in roots(sys.argv[1:]) for d in sorted(root.iterdir())]
    for d in dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            continue
        findings = audit(skill_md)
        real = [f for f in findings if not f.startswith("advisory:")]
        lines = len(skill_md.read_text().split("\n"))
        status = "clean" if not real else f"{len(real)} finding(s)"
        if findings and not real:
            status += " (advisories only)"
        print(f"\n{d.name}  ({lines} lines) — {status}")
        for f in findings:
            print(f"    - {f}")
        total += len(real)
    print(f"\n{'=' * 60}\nactionable findings: {total}")


if __name__ == "__main__":
    sys.exit(main())
