"""Registry-only checks, independent of rendering and proprietary fonts."""

import importlib.util
from pathlib import Path
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_card_profiles", ROOT / "scripts/check_card_profiles.py"
)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def profiles():
    return {name: {} for name in ("performance", "technology", "work")}


@pytest.mark.parametrize("value", [None, "", "tech", "fourth", [], False])
def test_missing_or_unknown_association(value):
    variant = {} if value is None else {"card_profile": value}
    with pytest.raises(ValueError, match="card_profile"):
        checker.validate_registry({"example": variant}, profiles())


@pytest.mark.parametrize(
    "names",
    [[], ["performance", "work"], ["performance", "technology", "work", "extra"]],
)
def test_exactly_three_named_profiles(names):
    with pytest.raises(ValueError, match="exactly"):
        checker.validate_registry({}, dict.fromkeys(names, {}))


def test_associations_are_deduplicated_and_supporting_documents_omitted():
    result = checker.validate_registry(
        {
            "general": {"card_profile": "technology", "check_metadata": True},
            "tailored": {"card_profile": "technology", "check_metadata": True},
            "letter": {"card_profile": "none", "check_metadata": False},
            "song-list": {"card_profile": "none", "check_metadata": False},
        },
        profiles(),
    )
    assert set(result) == set(profiles())
    assert result["technology"] == ["general", "tailored"]
    assert result["performance"] == result["work"] == []
    assert len(result) == 3  # outputs are profiles, not registry rows


def test_supporting_document_cannot_generate_card():
    with pytest.raises(ValueError, match="supporting documents"):
        checker.validate_registry(
            {"letter": {"card_profile": "performance", "check_metadata": False}},
            profiles(),
        )


def test_resume_cannot_silently_opt_out():
    with pytest.raises(ValueError, match="resumes must associate"):
        checker.validate_registry(
            {"resume": {"card_profile": "none", "check_metadata": True}}, profiles()
        )


def test_real_registry_is_complete_and_excludes_all_supporting_documents():
    with (ROOT / "variants.toml").open("rb") as stream:
        variants = tomllib.load(stream)
    result = checker.validate_registry(variants, profiles())
    associated = {name for names in result.values() for name in names}
    assert associated == {
        name for name, variant in variants.items() if variant["check_metadata"]
    }


def test_profile_file_requires_named_table(tmp_path):
    (tmp_path / "variants.toml").write_text("")
    (tmp_path / "cards").mkdir()
    (tmp_path / "cards/profiles.toml").write_text("performance = true")
    with pytest.raises(ValueError, match=r"\[profiles\]"):
        checker.check_root(tmp_path)
