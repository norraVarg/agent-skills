#!/usr/bin/env bash
# Installs the Claude Code entry point for git.
# A manually-invoked skill needs nothing beyond a symlink: no CLAUDE.md edit, no
# hooks, no settings.json changes.
# Idempotent — safe to re-run after every git pull.
# Set CLAUDE_HOME to install somewhere other than ~/.claude (used for testing).
set -eu

adapter_dir="$(cd "$(dirname "$0")" && pwd)"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"

skill_link="$claude_home/skills/git"
if [ -d "$skill_link" ] && [ ! -L "$skill_link" ]; then
  echo "git: $skill_link is a real directory; remove it and re-run." >&2
  exit 1
fi
mkdir -p "$claude_home/skills"
ln -sfn "$adapter_dir" "$skill_link"

echo "git installed for Claude Code"
echo "  skill    $skill_link -> $adapter_dir"
echo "Invoke with the Skill tool (skill \"git\") in any session."
