"""Focused stdlib tests for the production portfolio assembly boundary."""

import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("assembly", ROOT / "scripts/assemble-portfolio.py")
assert SPEC is not None and SPEC.loader is not None
ASSEMBLY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSEMBLY)


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.website = root / "website"
        (self.website / "resumes").mkdir(parents=True)
        (self.website / "index.html").write_text("real homepage")
        (self.website / "resumes/index.html").write_text("real downloads")
        self.resume = root / "resume"
        self.resume.mkdir()
        self.composite = root / "FINN RUTIS.pdf"
        self.composite.write_bytes(b"composite")
        self.registry = root / "variants.toml"
        self.output = root / "output"
        self.set_registry('[visible]\ndest = "resume"\n[hidden]\ndest = "private"\nsite_hidden = true\n')

    def set_registry(self, text):
        self.registry.write_text(text)
        for variant in tomllib.loads(text).values():
            dest = variant.get("dest") if isinstance(variant, dict) else None
            if isinstance(dest, str) and "/" not in dest and "\\" not in dest:
                for extension in ("pdf", "png"):
                    (self.resume / f"{dest}.{extension}").write_bytes(b"artifact")

    def assemble(self):
        ASSEMBLY.assemble(self.website, self.resume, self.composite, self.registry, self.output)

    def assert_preflight_failure(self, message):
        with self.assertRaisesRegex(ValueError, message):
            self.assemble()
        self.assertFalse(self.output.exists())

    def test_complete_site_including_hidden_and_real_indexes(self):
        self.assemble()
        self.assertEqual((self.output / "index.html").read_text(), "real homepage")
        self.assertEqual((self.output / "resumes/index.html").read_text(), "real downloads")
        self.assertEqual((self.output / "resumes/FINN RUTIS.pdf").read_bytes(), b"composite")
        self.assertTrue((self.output / ".nojekyll").is_file())
        self.assertEqual(len(list((self.output / "resumes").iterdir())), 6)
        self.assertTrue((self.output / "resumes/private.png").is_file())

    def test_actual_registry_all_artifacts_not_just_visible(self):
        self.set_registry((ROOT / "variants.toml").read_text())
        variants = tomllib.loads(self.registry.read_text())
        self.assemble()
        files = list((self.output / "resumes").iterdir())
        self.assertEqual(len(files), 2 * len(variants) + 2)  # composite and index
        for variant in variants.values():
            for extension in ("pdf", "png"):
                self.assertEqual((self.output / f'resumes/{variant["dest"]}.{extension}').read_bytes(), b"artifact")

    def test_unsafe_destinations(self):
        for dest in ("../escape", "/absolute", "a/b", "a\\b", ".", "", "a b", "a%20b"):
            with self.subTest(dest=dest):
                self.registry.write_text(f'[bad]\ndest = {json.dumps(dest)}\n')
                self.assert_preflight_failure("unsafe destination")

    def test_duplicate_destinations(self):
        self.set_registry('[one]\ndest = "resume"\n[two]\ndest = "resume"\n')
        self.assert_preflight_failure("duplicate destination")

    def test_invalid_registry_shapes_and_types(self):
        for text in ("", 'bad = 1', '[bad]\ndest = 42', '[bad]\nsource = "only"'):
            with self.subTest(text=text):
                self.registry.write_text(text)
                self.assert_preflight_failure("registry|unsafe destination|required file")

    def test_real_toml_duplicate_keys_rejected(self):
        self.registry.write_text('[bad]\ndest = "one"\ndest = "two"\n')
        self.assert_preflight_failure("overwrite")

    def test_missing_and_empty_required_sources(self):
        paths = [self.resume / "private.png", self.composite,
                 self.website / "index.html", self.website / "resumes/index.html"]
        for path in paths:
            original = path.read_bytes()
            for missing in (True, False):
                with self.subTest(path=path, missing=missing):
                    if missing:
                        path.unlink()
                    else:
                        path.write_bytes(b"")
                    self.assert_preflight_failure("missing or empty")
                    path.write_bytes(original)

    def test_existing_website_artifact_collision(self):
        for name in ("resume.pdf", "FINN RUTIS.pdf"):
            path = self.website / "resumes" / name
            path.write_bytes(b"do not overwrite")
            self.assert_preflight_failure("collides")
            path.unlink()

    def test_existing_output_is_not_modified(self):
        self.output.mkdir()
        marker = self.output / "marker"
        marker.write_text("keep")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.assemble()
        self.assertEqual(marker.read_text(), "keep")

    def test_symlink_in_site_rejected_before_copy(self):
        (self.website / "outside").symlink_to(self.composite)
        self.assert_preflight_failure("symlinks")

    def test_output_inside_site_rejected(self):
        self.output = self.website / "nested"
        self.assert_preflight_failure("inside website")


if __name__ == "__main__":
    unittest.main()
