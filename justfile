set shell := ["bash", "-euo", "pipefail", "-c"]

default:
  @just --list

bump bump_type:
  @if [[ ! "{{bump_type}}" =~ ^(patch|minor|major)$ ]]; then \
    echo "Usage: just bump <patch|minor|major>" >&2; \
    exit 1; \
  fi
  gh workflow run release.yml -f bump={{bump_type}}
