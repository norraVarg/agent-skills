#!/usr/bin/env bash
# Entry point: ./install.sh <skill-name> <provider>
# Runs the installer of the chosen skill's adapter for that provider, e.g.
# ./install.sh audit-content claude-code
set -eu

root="$(cd "$(dirname "$0")" && pwd)"
skill="${1:-}"
provider="${2:-}"

if [ -z "$skill" ] || [ -z "$provider" ] || [ ! -f "$root/skills/$skill/adapters/$provider/install.sh" ]; then
  echo "Usage: $0 <skill-name> <provider>" >&2
  echo "Available skills:" >&2
  for dir in "$root"/skills/*/; do
    echo "  $(basename "$dir")" >&2
  done
  if [ -n "$skill" ] && [ -d "$root/skills/$skill/adapters" ]; then
    echo "Available providers for $skill:" >&2
    for dir in "$root/skills/$skill"/adapters/*/; do
      echo "  $(basename "$dir")" >&2
    done
  fi
  exit 1
fi

exec bash "$root/skills/$skill/adapters/$provider/install.sh"
