#!/usr/bin/env python3
"""Cross-skill trigger-overlap report.

Two skills whose descriptions claim the same phrases compete, and which one wins is not
predictable from the text. This finds those collisions across every skill source given:

  overlap.py --root <skills-dir> [--root ...] [--plugins-manifest <installed_plugins.json>]

A plugins manifest adds the skills of each installed plugin version it lists; stale cached
versions are ignored, since they never load.
"""

import json
import re
import sys
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

import yaml

STOP = {"the", "a", "an", "to", "for", "when", "use", "this", "skill", "should", "be", "used",
        "or", "and", "of", "in", "on", "with", "from", "that", "it", "is", "as", "asked",
        "user", "asks", "wants", "create", "update", "new", "using", "via", "into", "by",
        "any", "all", "if", "then", "so", "at", "its", "their", "them", "one", "also"}


def read_desc(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        line = next((l for l in m.group(1).split("\n") if l.startswith("description:")), "")
        return {"description": line[len("description:"):].strip(), "name": path.parent.name}
    return fm


def live_sources(argv):
    """(label, dir) for every skill that can actually load."""
    out = []
    roots = [Path(argv[i + 1]).expanduser() for i, a in enumerate(argv) if a == "--root"]
    if not roots:
        print("usage: overlap.py --root <skills-dir> [--root ...] [--plugins-manifest <file>]")
        sys.exit(2)
    for root in roots:
        for d in sorted(root.iterdir()):
            if (d / "SKILL.md").is_file():
                out.append((d.name, d))

    manifest = argv[argv.index("--plugins-manifest") + 1] if "--plugins-manifest" in argv else None
    cfg = Path(manifest).expanduser() if manifest else None
    if cfg and cfg.is_file():
        data = json.loads(cfg.read_text())
        for key, installs in data.get("plugins", {}).items():
            plugin = key.split("@")[0]
            for inst in installs:
                root = Path(inst["installPath"]) / "skills"
                if not root.is_dir():
                    continue
                for d in sorted(root.iterdir()):
                    if (d / "SKILL.md").is_file():
                        out.append((f"{plugin}:{d.name}", d))
    return out


def phrases(desc):
    """Quoted trigger phrases, normalized."""
    found = re.findall(r'"([^"]{3,60})"', desc) + re.findall(r"'([^']{3,60})'", desc)
    return {p.strip().lower().rstrip(".") for p in found}


def keywords(desc):
    words = re.findall(r"[a-z][a-z-]{2,}", desc.lower())
    return {w for w in words if w not in STOP}


def main():
    skills = []
    for label, d in live_sources(sys.argv[1:]):
        fm = read_desc(d / "SKILL.md")
        if not fm or not fm.get("description"):
            continue
        desc = fm["description"]
        skills.append({"label": label, "desc": desc,
                       "phrases": phrases(desc), "kw": keywords(desc)})

    print(f"live skills compared: {len(skills)}\n")

    dupes, phrase_hits, kw_hits = [], [], []
    for a, b in combinations(skills, 2):
        ratio = SequenceMatcher(None, a["desc"], b["desc"]).ratio()
        shared_p = a["phrases"] & b["phrases"]
        shared_k = a["kw"] & b["kw"]
        jaccard = len(shared_k) / len(a["kw"] | b["kw"]) if (a["kw"] | b["kw"]) else 0

        if ratio > 0.90:
            dupes.append((ratio, a["label"], b["label"], shared_p))
        elif shared_p:
            phrase_hits.append((len(shared_p), a["label"], b["label"], shared_p))
        elif jaccard > 0.34:
            kw_hits.append((jaccard, a["label"], b["label"], sorted(shared_k)[:8]))

    print("=" * 72)
    print("TIER 1 — near-identical descriptions (>90% similar)")
    print("=" * 72)
    for ratio, x, y, sp in sorted(dupes, reverse=True):
        print(f"\n  {ratio:.0%}  {x}\n       {y}")
        if sp:
            print(f"       shared phrases: {len(sp)}")
    if not dupes:
        print("  none")

    print("\n" + "=" * 72)
    print("TIER 2 — identical quoted trigger phrases")
    print("=" * 72)
    for n, x, y, sp in sorted(phrase_hits, reverse=True):
        print(f"\n  {n} shared: {x}  vs  {y}")
        for p in sorted(sp):
            print(f"       \"{p}\"")
    if not phrase_hits:
        print("  none")

    print("\n" + "=" * 72)
    print("TIER 3 — high keyword overlap, no shared quoted phrase")
    print("=" * 72)
    for j, x, y, sk in sorted(kw_hits, reverse=True)[:10]:
        print(f"  {j:.0%}  {x}  vs  {y}")
        print(f"        {', '.join(sk)}")
    if not kw_hits:
        print("  none")


if __name__ == "__main__":
    main()
