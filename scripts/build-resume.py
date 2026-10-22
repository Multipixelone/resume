#!/usr/bin/env python3
"""Build PDF packages with one explicit Eastern submission date."""

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ("resume", "finn-rutis")


def iso_date(value):
    """Validate spelling as well as the actual Gregorian calendar date."""
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must be a real calendar date") from error


def nix_string(value):
    # JSON quoting covers quotes/backslashes; additionally disable Nix interpolation.
    return json.dumps(str(value), ensure_ascii=False).replace("${", r"\${")


def build_command(repo, submission_date, outputs):
    submission_date = iso_date(submission_date)
    if not outputs or any(output not in OUTPUTS for output in outputs):
        raise ValueError("select resume and/or finn-rutis")
    packages = "\n".join(
        f"(f.packages.${{builtins.currentSystem}}.{output}.override "
        f"{{ submissionDate = {nix_string(submission_date)}; }})"
        for output in dict.fromkeys(outputs)
    )
    # A git+file URI keeps self.rev; a bare path stamps the footer "commit dirty".
    flake_ref = "git+" + Path(repo).as_uri()
    expression = (
        f"let f = builtins.getFlake {nix_string(flake_ref)};\nin [\n{packages}\n]"
    )
    return ["nix", "build", "--impure", "--no-link", "--print-out-paths", "--expr", expression]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=iso_date, help="YYYY-MM-DD (default: today in America/New_York)")
    parser.add_argument("outputs", nargs="*", metavar="{resume,finn-rutis}")
    args = parser.parse_args(argv)
    outputs = args.outputs or OUTPUTS
    if any(output not in OUTPUTS for output in outputs):
        parser.error("outputs must be resume and/or finn-rutis")
    submission_date = args.date
    if submission_date is None:
        submission_date = datetime.now(ZoneInfo("America/New_York")).date().isoformat()
    print(f"Submission date: {submission_date} (America/New_York calendar)", flush=True)
    command = build_command(REPO_ROOT, submission_date, outputs)
    return subprocess.run(command, cwd=REPO_ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
