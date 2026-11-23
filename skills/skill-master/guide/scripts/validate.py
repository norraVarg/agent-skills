#!/usr/bin/env python3
"""Validate one skill's entry file metadata (SKILL.md with YAML frontmatter).

Usage:
  validate.py <skill-dir> [--entry SKILL.md] [--extra-keys key1,key2]

Checks: the entry file exists; it opens with a `---` frontmatter block that parses as a YAML mapping;
every key is known; `name` is kebab-case and at most 64 characters; `description` is a non-empty string of at most 1024 characters with no angle brackets.

Known keys are the cross-agent Agent Skills set (name, description, license, allowed-tools, metadata,
compatibility) plus any passed with --extra-keys. Prints "valid" and exits 0, or prints each problem and
exits 1. Needs PyYAML.
"""

import re
import sys
from pathlib import Path

import yaml

BASE_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def arg(argv, flag, default):
    return argv[argv.index(flag) + 1] if flag in argv else default


def problems(skill_dir, entry, extra_keys):
    path = Path(skill_dir) / entry
    if not path.is_file():
        return [f"{entry} not found in {skill_dir}"]
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---(\n|$)", text, re.DOTALL)
    if not m:
        return ["no frontmatter block: the file must start with '---' and close it with '---'"]
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return [f"frontmatter is not valid YAML: {str(e).splitlines()[0]}"]
    if not isinstance(fm, dict):
        return ["frontmatter must be a YAML mapping"]

    out = []
    unknown = sorted(set(fm) - BASE_KEYS - extra_keys)
    if unknown:
        out.append(f"unknown key(s): {', '.join(unknown)}")

    name = fm.get("name")
    if not isinstance(name, str) or not name.strip():
        out.append("missing 'name'")
    else:
        if not NAME.match(name):
            out.append(f"name '{name}' must be kebab-case: lowercase letters, digits, single hyphens")
        if len(name) > 64:
            out.append(f"name is {len(name)} characters; the limit is 64")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        out.append("missing 'description'")
    else:
        if len(desc) > 1024:
            out.append(f"description is {len(desc)} characters; the limit is 1024")
        if "<" in desc or ">" in desc:
            out.append("description contains angle brackets")
    return out


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    extra = {k.strip() for k in arg(argv, "--extra-keys", "").split(",") if k.strip()}
    found = problems(argv[0], arg(argv, "--entry", "SKILL.md"), extra)
    if not found:
        print("valid")
        return 0
    for p in found:
        print(p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
