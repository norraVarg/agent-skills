#!/usr/bin/env python3
"""Scan a skill for private information before it is shared.

Usage:
  scan_private.py <skill-dir | file> [--terms <private-terms-file>] [--baseline <snapshot-dir>]
  scan_private.py <repo-dir> --staged [--terms <private-terms-file>]

Reads every text file in the skill, following symlinked directories — or one file, such as a commit
message — and reports each line that contains:
  - a term from the private-terms file (case-insensitive; '#' comments, '!' lines allow exact text;
    a term ending in '-' is a ticket prefix and matches only when a digit follows, e.g. 'ABC-123')
  - an email address (example.com, example.org and example.net addresses are ignored)
  - a home-directory path with a username (/Users/<name>, /home/<name>, C:\\Users\\<name>)
  - an IPv4 address other than 127.0.0.1 and 0.0.0.0
  - a secret-shaped token: AWS access key, GitHub token, Slack token, private-key block, JWT, or an
    'sk-' style API key

With --staged, it reads the content staged for the next commit in that repository straight from git,
so a pre-commit hook can block a leak before it reaches history; every staged file that decodes as
UTF-8 text is scanned, whatever its extension.

Matched terms are shown in full; secrets are shown masked. With --baseline, each hit is tagged NEW or
old, and only NEW hits fail. Exit code 1 when a failing hit exists, 0 otherwise. Standard library only.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

TEXT = {".md", ".py", ".sh", ".json", ".txt", ".yml", ".yaml", ".html", ".js", ".ts", ".toml", ".csv"}
PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("home path", re.compile(r"(?:/Users/|/home/|[Cc]:\\Users\\)([A-Za-z0-9._-]+)")),
    ("ip address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]
SECRETS = [
    ("aws key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("api key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
]
SAFE_EMAIL = re.compile(r"@(?:example\.(?:com|org|net))$", re.I)
SAFE_IP = {"127.0.0.1", "0.0.0.0"}
PLACEHOLDER_USER = {"<name>", "name", "username", "user", "you", "me", "runner", "example"}


def load_terms(path):
    terms, allow = [], set()
    if not path:
        return terms, allow
    for line in Path(path).expanduser().read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            allow.add(line[1:].strip().lower())
        else:
            terms.append(line)
    return terms, allow


def text_files(root):
    for dirpath, _, names in os.walk(root, followlinks=True):
        if "/.git" in dirpath or "__pycache__" in dirpath:
            continue
        for n in names:
            p = Path(dirpath) / n
            if p.suffix.lower() in TEXT:
                yield p


def sources(root, staged):
    """(relative path, text) for every file to scan."""
    root = Path(root)
    if staged:
        git = ["git", "-C", str(root)]
        names = subprocess.run(git + ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                               check=True, capture_output=True).stdout.decode().split("\0")
        for name in filter(None, names):
            blob = subprocess.run(git + ["show", f":{name}"], check=True, capture_output=True).stdout
            try:
                yield name, blob.decode("utf-8")
            except UnicodeDecodeError:
                continue
        return
    files = [root] if root.is_file() else text_files(root)
    for p in files:
        try:
            yield (p.name if root.is_file() else os.path.relpath(p, root)), p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def mask(s):
    return s[:4] + "…" + s[-2:] if len(s) > 8 else "…"


def hits(root, terms, allow, staged=False):
    out, count = set(), 0
    # Word boundaries apply only on a side where the term itself ends in a letter or digit. A term
    # ending in "-" is a ticket prefix: it must be followed by a digit, so "ABC-" matches "ABC-123"
    # but not a hyphenated word such as "abc-style".
    def term_re(t):
        start = r"(?<![A-Za-z0-9])" if t[0].isalnum() else ""
        end = r"(?=\d)" if t.endswith("-") else (r"(?![A-Za-z0-9])" if t[-1].isalnum() else "")
        return re.compile(start + re.escape(t) + end, re.I)

    term_res = [(t, term_re(t)) for t in terms]
    for rel, text in sources(root, staged):
        count += 1
        for no, line in enumerate(text.splitlines(), 1):
            found = []
            for term, rx in term_res:
                for m in rx.finditer(line):
                    found.append(("private term", m.group(0)))
            for kind, rx in PATTERNS:
                for m in rx.finditer(line):
                    val = m.group(0)
                    if kind == "email" and SAFE_EMAIL.search(val):
                        continue
                    if kind == "ip address" and (val in SAFE_IP or
                                                 any(int(o) > 255 for o in val.split("."))):
                        continue
                    if kind == "home path" and m.group(1).lower() in PLACEHOLDER_USER:
                        continue
                    found.append((kind, val))
            for kind, rx in SECRETS:
                for m in rx.finditer(line):
                    found.append((kind, mask(m.group(0))))
            for kind, val in found:
                if val.lower() in allow:
                    continue
                out.add((rel, kind, val, no))
    return out, count


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    terms_file = argv[argv.index("--terms") + 1] if "--terms" in argv else None
    if terms_file and not Path(terms_file).expanduser().is_file():
        print(f"private-terms list not found: {terms_file} — only built-in patterns ran")
        terms_file = None
    terms, allow = load_terms(terms_file)
    current, count = hits(argv[0], terms, allow, staged="--staged" in argv)
    baseline = None
    if "--baseline" in argv:
        # Compare hits without line numbers, so an edit above a hit does not make an old hit look new.
        baseline = {h[:3] for h in hits(argv[argv.index("--baseline") + 1], terms, allow)[0]}

    print(f"{count} files scanned; private-terms list {'used' if terms_file else 'missing'}")
    if not current:
        print("no hits")
        return 0
    new = 0
    for rel, kind, val, no in sorted(current):
        is_new = baseline is None or (rel, kind, val) not in baseline
        new += is_new
        tag = "" if baseline is None else ("NEW " if is_new else "old ")
        print(f"{tag}{rel}:{no}: {kind}: {val}")
    if baseline is not None:
        print(f"\n{new} new, {len(current) - new} pre-existing")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
