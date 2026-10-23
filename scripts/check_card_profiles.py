"""Validate explicit resume associations without producing per-resume cards."""

import argparse
import json
from pathlib import Path
import sys
import tomllib
from typing import Any


PROFILE_NAMES = frozenset({"performance", "technology", "work"})


def validate_registry(
    variants: dict[str, Any], profiles: dict[str, Any]
) -> dict[str, list[str]]:
    """Return three deduplicated output groups; excluded documents never join one."""
    if set(profiles) != PROFILE_NAMES:
        raise ValueError(
            "profiles must contain exactly performance, technology, work; "
            f"got {sorted(profiles)}"
        )
    associations: dict[str, list[str]] = {name: [] for name in sorted(profiles)}
    errors = []
    for name, variant in variants.items():
        if not isinstance(variant, dict):
            errors.append(f"{name}: expected a variant table")
            continue
        profile = variant.get("card_profile")
        if not isinstance(profile, str) or profile not in PROFILE_NAMES | {"none"}:
            errors.append(f"{name}: card_profile must be performance, technology, work, or none")
            continue
        # The registry already identifies supporting artifacts by disabling
        # resume metadata checks. Do not duplicate their names in another list.
        if variant.get("check_metadata") is False and profile != "none":
            errors.append(f"{name}: supporting documents must use card_profile = 'none'")
        elif variant.get("check_metadata") is True and profile == "none":
            errors.append(f"{name}: resumes must associate a card profile")
        elif profile != "none":
            associations[profile].append(name)
    if errors:
        raise ValueError("\n".join(errors))
    return associations


def check_root(root: Path) -> dict[str, list[str]]:
    with (root / "variants.toml").open("rb") as stream:
        variants = tomllib.load(stream)
    with (root / "cards/profiles.toml").open("rb") as stream:
        data = tomllib.load(stream)
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("cards/profiles.toml must define a [profiles] table")
    return validate_registry(variants, profiles)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        associations = check_root(args.root)
    except (OSError, ValueError) as error:
        print(f"Card profile validation failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(associations, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
