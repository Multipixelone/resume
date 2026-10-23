set shell := ["bash", "-euo", "pipefail", "-c"]

default:
  @just --list

bump bump_type:
  @if [[ ! "{{bump_type}}" =~ ^(patch|minor|major)$ ]]; then \
    echo "Usage: just bump <patch|minor|major>" >&2; \
    exit 1; \
  fi
  gh workflow run release.yml -f bump={{bump_type}}

# Render three shared cards with an explicit, locally licensed Sabon font.
business-cards sabon output="/tmp/business-cards":
  nix run "path:$PWD#business-cards" -- --root "$PWD" --output {{quote(output)}} --sabon {{quote(sabon)}}
