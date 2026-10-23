"""Assemble a complete static portfolio from already-built artifacts (Python 3.11+)."""

import argparse
from pathlib import Path
import re
import shutil
import tomllib


def required_file(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"required file is missing or empty: {path}")


def assemble(website: Path, resume: Path, composite: Path, registry: Path, output: Path) -> None:
    """Preflight all inputs and collisions before creating the output directory."""
    if output.exists() or output.is_symlink():
        raise ValueError(f"output already exists: {output}")
    required_file(website / "index.html")
    # GitHub Pages serves this for every unknown path; without it, misses get GitHub's own page.
    required_file(website / "404.html")
    required_file(website / "resumes/index.html")
    required_file(registry)
    with registry.open("rb") as stream:
        variants = tomllib.load(stream)
    if not variants:
        raise ValueError("registry must contain at least one variant")

    copies = []
    destinations = set()
    for key, variant in variants.items():
        dest = variant.get("dest") if isinstance(variant, dict) else None
        if not isinstance(dest, str) or re.fullmatch(r"[A-Za-z0-9_-]+", dest) is None:
            raise ValueError(f"unsafe destination for variant {key}: {dest!r}")
        if dest in destinations:
            raise ValueError(f"duplicate destination: {dest}")
        destinations.add(dest)
        # Hidden variants remain downloadable artifacts; only the UI filters them.
        for extension in ("pdf", "png"):
            filename = f"{dest}.{extension}"
            copies.append((resume / filename, Path("resumes") / filename))
    copies.append((composite, Path("resumes/FINN RUTIS.pdf")))
    for source, target in copies:
        required_file(source)
        existing = website / target
        if existing.exists() or existing.is_symlink():
            raise ValueError(f"artifact collides with website: {target}")
    if (website / ".nojekyll").is_dir():
        raise ValueError("website .nojekyll must not be a directory")
    # Reject dangling/out-of-tree symlinks rather than copying an incomplete site
    # or accidentally exposing files outside its build directory.
    site_root = website.resolve()
    for path in website.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"website must not contain symlinks: {path}")
    resolved_output = output.resolve()
    if resolved_output == site_root or site_root in resolved_output.parents:
        raise ValueError("output must not be inside website")

    shutil.copytree(website, output)
    for source, target in copies:
        shutil.copyfile(source, output / target)
    (output / ".nojekyll").touch()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("website", "resume", "composite", "registry", "output"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    try:
        assemble(**vars(args))
    except (ValueError, OSError) as error:
        parser.exit(1, f"portfolio assembly failed: {error}\n")


if __name__ == "__main__":
    main()
