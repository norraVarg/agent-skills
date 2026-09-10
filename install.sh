#!/usr/bin/env bash
# Entry point: ./install.sh <skill-name> <adapter>
# Runs the installer of the chosen skill's agent adapter, e.g.
# ./install.sh audit-content claude-code
set -eu

root="$(cd "$(dirname "$0")" && pwd)"
skill="${1:-}"
adapter="${2:-}"

if [ -z "$skill" ] || [ -z "$adapter" ] || [ ! -f "$root/skills/$skill/adapters/$adapter/install.sh" ]; then
  echo "Usage: $0 <skill-name> <adapter>" >&2
  echo "Available skills:" >&2
  for dir in "$root"/skills/*/; do
    echo "  $(basename "$dir")" >&2
  done
  if [ -n "$skill" ] && [ -d "$root/skills/$skill/adapters" ]; then
    echo "Available adapters for $skill:" >&2
    for dir in "$root/skills/$skill"/adapters/*/; do
      echo "  $(basename "$dir")" >&2
    done
  fi
  exit 1
fi

exec bash "$root/skills/$skill/adapters/$adapter/install.sh"
