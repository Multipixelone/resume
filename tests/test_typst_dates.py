"""Evaluate the real Typst date helpers without packages, fonts, or Nix builds."""

from datetime import date
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALID_DATES = ("0001-01-01", "2000-02-29", "2024-02-29", "2026-10-21", "9999-12-31")
INVALID_DATES = (
    "0000-01-01", "0000-02-29", "2026-02-29", "1900-02-29", "2026-04-31",
    "2026-00-01", "2026-13-01", "2026-01-00", "2026-1-01", "2026-10", "",
    "20261021", "2026-W43-3",
    "2026-10-21T00:00:00", "２０２６-１０-２１", "10000-01-01",
)
WHITESPACE_DATES = (" 2026-10-21", "2026-10-21\n")


class TypstDateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.typst = shutil.which("typst")
        if cls.typst is None:
            raise RuntimeError("Typst executable required for actual date-helper evaluation")

    def compile_fixture(self, **inputs):
        typst = self.typst
        assert typst is not None
        with tempfile.TemporaryDirectory(prefix="portfolio-typst-dates-") as temporary:
            command = [
                typst, "compile", "--root", str(ROOT),
                str(ROOT / "tests/date-input.typ"), str(Path(temporary) / "fixture.pdf"),
            ]
            for key, value in inputs.items():
                command.extend(("--input", f"{key}={value}"))
            return subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True, timeout=30,
                check=False,
            )

    def assert_compiles(self, **inputs):
        result = self.compile_fixture(**inputs)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_valid_submission_dates_override_conflicting_version(self):
        for value in VALID_DATES:
            with self.subTest(value=value):
                self.assert_compiles(**{
                    "mode": "build", "submission-date": value,
                    "version": "1999-01-01", "expected": value,
                })
        # CLI normalization happens before buildDate can inspect sys.inputs.
        for value in WHITESPACE_DATES:
            with self.subTest(cli_normalization=value):
                self.assert_compiles(**{
                    "mode": "build", "submission-date": value,
                    "version": "1999-01-01", "expected": "2026-10-21",
                })

    def test_invalid_dates_rejected_by_both_helper_paths(self):
        for mode, field in (("build", "submission-date"), ("upcoming", "date")):
            for value in INVALID_DATES:
                with self.subTest(mode=mode, value=value):
                    result = self.compile_fixture(**{
                        "mode": mode, field: value, "expected": value,
                    })
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    # Do not let an import/syntax/fixture assertion error count as rejection.
                    self.assertRegex(
                        result.stderr,
                        r"must be a real ISO calendar date|(?:date|month) is invalid",
                    )
        # Encode whitespace inside JSON so the fixture constructs the exact
        # original string, bypassing CLI trimming without weakening the parser.
        for mode in ("parse", "upcoming"):
            for value in WHITESPACE_DATES:
                with self.subTest(mode=mode, literal_whitespace=value):
                    result = self.compile_fixture(**{
                        "mode": mode, "date-json": json.dumps(value),
                        "expected": "false",
                    })
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("must be a real ISO calendar date", result.stderr)

    def test_valid_performance_dates_and_start_boundary(self):
        for value in (*VALID_DATES, "2026-10-20", "2026-10-22"):
            with self.subTest(value=value):
                upcoming = date(2026, 10, 21) < date.fromisoformat(value)
                self.assert_compiles(
                    mode="upcoming", date=value, expected=str(upcoming).lower(),
                )
        for value in WHITESPACE_DATES:
            with self.subTest(cli_normalization=value):
                self.assert_compiles(mode="upcoming", date=value, expected="false")

    def test_exported_parser_valid_boundaries_and_leaps(self):
        for value in VALID_DATES:
            with self.subTest(value=value):
                self.assert_compiles(mode="parse", date=value, expected=value)

    def test_absent_submission_date_preserves_manual_fallback(self):
        self.assert_compiles(mode="build")
        self.assert_compiles(mode="build", version="1999-01-01")

    def test_absent_performance_start_has_no_marker(self):
        self.assert_compiles(mode="upcoming", expected="false")


if __name__ == "__main__":
    unittest.main()
