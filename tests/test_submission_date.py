"""Focused wrapper tests; no Nix builds, network access, or wall-clock dependency."""

import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_resume", ROOT / "scripts/build-resume.py")
assert SPEC is not None and SPEC.loader is not None
build_resume = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_resume)


class SubmissionDateTests(unittest.TestCase):
    def test_strict_actual_dates(self):
        for value in ("2024-02-29", "2000-02-29", "0001-01-01", "2026-10-21"):
            with self.subTest(value=value):
                self.assertEqual(build_resume.iso_date(value), value)
        for value in (
            "2026-02-29", "1900-02-29", "0000-01-01", "2026-04-31",
            "2026-00-01", "2026-13-01", "2026-01-00", "2026-1-01",
            "20261021", "2026-W43-3", " 2026-10-21", "2026-10-21\n",
            "2026-10-21T00:00:00", "２０２６-１０-２１", '${abort "bad";}',
        ):
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    build_resume.iso_date(value)

    def test_eastern_today_resolved_once_for_both_outputs(self):
        # UTC is already October 22; Eastern is still October 21.
        instant = datetime(2026, 10, 22, 1, 30, tzinfo=timezone.utc)
        with patch.object(build_resume, "datetime") as clock, patch.object(
            build_resume.subprocess, "run"
        ) as run, patch("builtins.print") as display:
            clock.now.side_effect = lambda zone: instant.astimezone(zone)
            run.return_value.returncode = 0
            self.assertEqual(build_resume.main([]), 0)
            clock.now.assert_called_once()
            self.assertEqual(clock.now.call_args.args[0].key, "America/New_York")
            run.assert_called_once()
            command = run.call_args.args[0]
            expression = command[-1]
            self.assertEqual(expression.count('submissionDate = "2026-10-21";'), 2)
            self.assertIn(".resume.override", expression)
            self.assertIn(".finn-rutis.override", expression)
            display.assert_called_once_with(
                "Submission date: 2026-10-21 (America/New_York calendar)", flush=True
            )

    def test_explicit_date_skips_clock_and_selects_outputs(self):
        for outputs in (("resume",), ("finn-rutis",), ("finn-rutis", "resume")):
            with self.subTest(outputs=outputs), patch.object(
                build_resume, "datetime"
            ) as clock, patch.object(build_resume.subprocess, "run") as run:
                run.return_value.returncode = 7
                self.assertEqual(build_resume.main(["--date", "2024-02-29", *outputs]), 7)
                clock.now.assert_not_called()
                expression = run.call_args.args[0][-1]
                for output in build_resume.OUTPUTS:
                    self.assertEqual(f".{output}.override" in expression, output in outputs)
                self.assertEqual(expression.count('submissionDate = "2024-02-29";'), len(outputs))

    def test_safe_path_and_argv(self):
        repo = Path('/tmp/resume space/"quote"/back\\slash/${abort "bad";}')
        with patch.object(build_resume, "REPO_ROOT", repo), patch.object(
            build_resume.subprocess, "run"
        ) as run:
            run.return_value.returncode = 0
            build_resume.main(["--date", "2026-10-21"])
            command = run.call_args.args[0]
            self.assertEqual(command[:-1], [
                "nix", "build", "--impure", "--no-link", "--print-out-paths", "--expr"
            ])
            self.assertIn(
                'builtins.getFlake "git+file:///tmp/resume%20space/%22quote%22/'
                'back%5Cslash/%24%7Babort%20%22bad%22%3B%7D"',
                command[-1],
            )
            self.assertNotIn("${abort", command[-1])
            self.assertIn("builtins.currentSystem", command[-1])
            self.assertEqual(run.call_args.kwargs, {"cwd": repo, "check": False})

    def test_invalid_cli_never_invokes_nix(self):
        for arguments in (["--date", "2026-02-29"], ["website"], ["resume; touch bad"]):
            with self.subTest(arguments=arguments), patch.object(
                build_resume.subprocess, "run"
            ) as run, patch("sys.stderr"):
                with self.assertRaises(SystemExit) as error:
                    build_resume.main(arguments)
                self.assertEqual(error.exception.code, 2)
                run.assert_not_called()

    def test_archive_default(self):
        contents = (ROOT / "metadata/submission-date.txt").read_text()
        self.assertEqual(contents, "2026-10-21\n")
        self.assertEqual(build_resume.iso_date(contents.removesuffix("\n")), "2026-10-21")


if __name__ == "__main__":
    unittest.main()
