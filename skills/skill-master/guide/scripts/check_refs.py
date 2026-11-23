#!/usr/bin/env python3
"""Whole-skill reference check — the links audit_bodies.py cannot see because it reads SKILL.md only.

Usage:
  check_refs.py <skill-dir> [--baseline <snapshot-dir>]

Checks every .md file in the skill directory, not just SKILL.md, following symlinked directories:
  - bundled-file references (`references/x.md`, `scope/z.md`, "Read `CHECKLIST.md`") that do not exist
  - Step/Stage references that match no `## Step N` / `## Stage X` heading in any file
  - quoted section names ('section "X"', '"X" section') that match no heading in any file
  - tools named anywhere (MCP tools, core tools in backticks) missing from allowed-tools

With --baseline, the same checks run on the snapshot and each finding is tagged NEW or pre-existing,
so an update is judged only on what it introduced. Exit code 1 when any NEW finding exists (or, without
a baseline, any finding at all). Standard library only.
"""

import os
import re
import sys
from pathlib import Path

CORE_TOOLS = {"Read", "Write", "Edit", "Bash", "Grep", "Glob", "AskUserQuestion", "Skill", "Agent",
              "WebFetch", "WebSearch", "ReadMcpResourceTool", "NotebookEdit", "TodoWrite"}
FILE_REF = re.compile(r"`((?:references|assets|scripts|[a-z0-9-]+)/[A-Za-z0-9_./-]+\.(?:md|py|sh|json|txt))`")
BARE_REF = re.compile(r"\b[Rr]ead `([A-Za-z0-9_-]+\.md)`")
STEP_REF = re.compile(r"\b(Step|Stage) ([0-9]+[A-Z]?|[A-Z])(?:\.[0-9]+)?\b")
HEADING = re.compile(r"^#{2,3} (Step|Stage) ([0-9]+[A-Z]?|[A-Z])\b", re.M)
SECTION_REF = re.compile(r'section "([^"]{3,60})"|"([^"]{3,60})" section')
ANY_HEADING = re.compile(r"^#{1,4} (.+?)\s*$", re.M)
MCP_TOOL = re.compile(r"\bmcp__[A-Za-z0-9_-]+__[A-Za-z0-9_]+\b")
CORE_REF = re.compile(r"`(" + "|".join(sorted(CORE_TOOLS)) + r")`")


def allowed_tools(skill_md):
    m = re.search(r"^allowed-tools:\s*(.+)$", skill_md, re.M)
    if not m:
        return set()
    return {t.strip().split("(")[0] for t in m.group(1).split(",") if t.strip()}


def md_files(root):
    """Every .md file under root, following symlinked directories (an adapter's guide/ link)."""
    out = []
    for dirpath, _, names in os.walk(root, followlinks=True):
        out += [Path(dirpath) / n for n in names if n.endswith(".md")]
    return sorted(out)


def resolves(ref, root, here, names):
    if "/" not in ref:
        return ref in names
    return any((base / ref).exists() for base in (root, root / "references", root / "guide", here))


def findings(root):
    root = Path(root)
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    declared = allowed_tools(skill)
    restricted = re.search(r"^allowed-tools:", skill, re.M) is not None
    files = md_files(root)
    names = {p.name for p in files} | {
        n for dirpath, _, ns in os.walk(root, followlinks=True) for n in ns}
    headings, all_headings = set(), set()
    for p in files:
        text = p.read_text(encoding="utf-8")
        headings |= {(k, n) for k, n in HEADING.findall(text)}
        all_headings |= {h.strip().lower() for h in ANY_HEADING.findall(text)}

    out = set()
    for p in files:
        rel = os.path.relpath(p, root)
        text = p.read_text(encoding="utf-8")
        body = text.split("\n---\n", 2)[-1] if rel == "SKILL.md" else text
        for ref in set(FILE_REF.findall(body)) | set(BARE_REF.findall(body)):
            if not resolves(ref, root, p.parent, names):
                out.add(f"{rel}: missing file `{ref}` (fine if it is only an example name)")
        if headings:
            for kind, num in STEP_REF.findall(body):
                if (kind, num) not in headings and any(k == kind for k, _ in headings):
                    out.add(f"{rel}: '{kind} {num}' matches no heading")
        for a, b in SECTION_REF.findall(body):
            name = " ".join((a or b).split())
            if not any(h == name.lower() or h.startswith(name.lower()) for h in all_headings):
                out.add(f'{rel}: section "{name}" matches no heading')
        for tool in set(MCP_TOOL.findall(body)) | set(CORE_REF.findall(body)):
            if restricted and tool not in declared:
                out.add(f"{rel}: tool `{tool}` is named but not in allowed-tools")
    return out


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    current = findings(argv[0])
    baseline = None
    if "--baseline" in argv:
        baseline = findings(argv[argv.index("--baseline") + 1])
    if not current:
        print("check_refs: no findings")
        return 0
    new = current - baseline if baseline is not None else current
    for f in sorted(current):
        tag = "NEW " if baseline is not None and f in new else ("" if baseline is None else "old ")
        print(f"{tag}{f}")
    if baseline is not None:
        print(f"\n{len(new)} new, {len(current) - len(new)} pre-existing")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
