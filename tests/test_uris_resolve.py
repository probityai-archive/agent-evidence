"""Tests for scripts/check_uris_resolve.py and scripts/build_vocabulary_pages.py."""

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uris = _load("check_uris_resolve")
vocab_pages = _load("build_vocabulary_pages")
INDEX = json.loads((_ROOT / "packages" / "vocabulary" / "registry.json").read_text(encoding="utf-8"))
TABLE = uris.rules((_ROOT / "w3id" / "agent-evidence.htaccess").read_text(encoding="utf-8"))


@pytest.fixture
def pages(tmp_path: Path) -> Path:
    shutil.copytree(_ROOT / "pages", tmp_path / "pages")
    return tmp_path / "pages"


def test_every_identifier_resolves_against_the_built_site() -> None:
    assert uris.check(_ROOT / "pages", INDEX, TABLE) == []


def test_the_vocabulary_pages_are_current() -> None:
    assert vocab_pages.main(["--check"]) == 0


def test_every_term_and_value_is_an_identifier() -> None:
    found = set(uris.identifiers(_ROOT / "pages", INDEX))
    assert "https://w3id.org/agent-evidence/vocab/v1/observation_vantage#substrate" in found
    assert "https://w3id.org/agent-evidence/predicate/v1/done-receipt" in found
    assert len([u for u in found if "/vocab/v1/" in u and "#" not in u]) == len(INDEX["terms"]) + 1


def test_a_missing_term_page_fails(pages: Path) -> None:
    shutil.rmtree(pages / "vocab" / "v1" / "observation_vantage")
    failures = uris.check(pages, INDEX, TABLE)
    assert any(f.startswith("https://w3id.org/agent-evidence/vocab/v1/observation_vantage") for f in failures)


def test_a_missing_value_anchor_fails(pages: Path) -> None:
    page = pages / "vocab" / "v1" / "observation_vantage" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace('id="substrate"', 'id="x"'), encoding="utf-8")
    assert uris.check(pages, INDEX, TABLE) == [
        ("https://w3id.org/agent-evidence/vocab/v1/observation_vantage#substrate: "
         "pages/vocab/v1/observation_vantage/index.html has no anchor for the fragment")]


def test_an_identifier_with_no_rule_fails() -> None:
    table = [rule for rule in TABLE if "vocab" not in rule[0].pattern]
    failures = uris.check(_ROOT / "pages", INDEX, table)
    vocab = [u for u in uris.identifiers(_ROOT / "pages", INDEX) if "/vocab/v1/" in u]
    assert [f.split(": ", 1)[0] for f in failures] == vocab


def test_the_rules_rewrite_like_w3id() -> None:
    assert uris.rewrite("https://w3id.org/agent-evidence/predicate/v1/done-receipt", TABLE) == \
        "https://probityai.github.io/agent-evidence/predicate/v1/done-receipt/"
    assert uris.rewrite("https://w3id.org/agent-evidence/vocab/v1/result#fail", TABLE) == \
        "https://probityai.github.io/agent-evidence/vocab/v1/result/"
    assert uris.rewrite("https://w3id.org/agent-evidence/other", TABLE) is None
