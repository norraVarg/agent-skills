#!/usr/bin/env python3
"""Quote unquoted `description:` scalars in SKILL.md frontmatter.

Usage: quote_descriptions.py --root <skills-dir> [--root ...] [--apply]

Picks the quote style that needs no escaping, and refuses to write unless the
re-parsed value is byte-identical to the original. Pass --apply to write.
"""

import re
import sys
from pathlib import Path

import yaml


def parse_desc(fm_text):
    try:
        return yaml.safe_load(fm_text).get("description")
    except yaml.YAMLError:
        return None


def process(path, apply):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return f"{path.parent.name}: no frontmatter"
    fm_text = m.group(1)

    lines = fm_text.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.startswith("description:")), None)
    if idx is None:
        return f"{path.parent.name}: no description key"

    # Multi-line scalars continue on indented lines; handle single-line only.
    if idx + 1 < len(lines) and lines[idx + 1].startswith(("  ", "\t")):
        return f"{path.parent.name}: SKIP (multi-line scalar, needs manual handling)"

    val = lines[idx][len("description:"):].strip()
    if val[:1] in ("'", '"'):
        return f"{path.parent.name}: already quoted"

    original = parse_desc(fm_text)
    if original is None:
        return f"{path.parent.name}: SKIP (frontmatter does not parse)"

    has_single = "'" in val
    has_double = '"' in val
    if not has_single:
        quoted, style = f"'{val}'", "single"
    elif not has_double:
        quoted, style = f'"{val}"', "double"
    else:
        quoted, style = "'" + val.replace("'", "''") + "'", "single (escaped)"

    new_lines = list(lines)
    new_lines[idx] = f"description: {quoted}"
    new_fm = "\n".join(new_lines)

    reparsed = parse_desc(new_fm)
    if reparsed != original:
        return f"{path.parent.name}: REFUSED (value would change)"

    if apply:
        path.write_text(text.replace(fm_text, new_fm, 1))
        return f"{path.parent.name}: quoted with {style}, {len(original)} chars verified identical"
    return f"{path.parent.name}: would quote with {style}, {len(original)} chars verified identical"


def main():
    argv = sys.argv[1:]
    apply = "--apply" in argv
    roots = [Path(argv[i + 1]).expanduser() for i, a in enumerate(argv) if a == "--root"]
    if not roots:
        print("usage: quote_descriptions.py --root <skills-dir> [--root ...] [--apply]")
        return 2
    for d in [d for root in roots for d in sorted(root.iterdir())]:
        f = d / "SKILL.md"
        if f.is_file():
            result = process(f, apply)
            if "already quoted" not in result:
                print("  " + result)
    print("\n" + ("APPLIED" if apply else "DRY RUN — pass --apply to write"))


if __name__ == "__main__":
    sys.exit(main())
