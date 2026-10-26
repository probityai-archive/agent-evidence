"""Build the vocabulary term pages under pages/vocab/v1/ from the registry index.

    python3 scripts/build_vocabulary_pages.py          # write the pages
    python3 scripts/build_vocabulary_pages.py --check  # fail when they are stale

Every term URI https://w3id.org/agent-evidence/vocab/v1/<term> redirects to
https://probityai.github.io/agent-evidence/vocab/v1/<term>/, and every registered
value is an anchor (#<value>) on its term's page. The input is
packages/vocabulary/registry.json, which gen_registry_index.py generates from
vocabulary.yaml. The build also publishes the exact vocabulary.yaml bytes at
vocab/v1/registry/sha256-<hex>.yaml, the address a record's registryDigest
names. A published registry copy is never removed, because older records name
it. Never edit pages/vocab/ by hand.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages" / "vocabulary"
OUT = ROOT / "pages" / "vocab" / "v1"
_SPEC = importlib.util.spec_from_file_location("build_predicate_pages", ROOT / "scripts" / "build_predicate_pages.py")
_predicate = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_predicate)
SOURCE_URL = "https://github.com/probityai/agent-evidence/blob/main/packages/vocabulary/vocabulary.yaml"


def _term_page(name: str, term: dict, children: dict) -> str:
    e = html.escape
    parts = [f"<h1><code>{e(name)}</code></h1>",
             f'<p>Term URI: <a href="{term["uri"]}">{term["uri"]}</a></p>',
             f"<p>Section: <code>{e(term['section'])}</code>. Criticality: <code>{e(term['criticality'])}</code>.</p>",
             f"<p>{e(term['definition'])}</p>"]
    if term["values"]:
        parts.append("<h2>Registered values</h2>\n<ul>")
        for value in term["values"]:
            meaning = term["value_definitions"].get(value)
            tail = f": {e(meaning)}" if meaning else ""
            parts.append(f'<li id="{e(value)}"><code>{term["uri"]}#{e(value)}</code>{tail}</li>')
        parts.append("</ul>")
    if children:
        parts.append("<h2>Registered verdict classes</h2>\n<ul>")
        for code, child in sorted(children.items()):
            parts.append(f'<li id="{e(code)}"><code>{e(child["uri"])}</code>, parent <code>{e(child["parent"])}</code></li>')
        parts.append("</ul>")
    footer = (f'Generated from <a href="{SOURCE_URL}">vocabulary.yaml</a>. The term URI does not change once a '
              "signed record carries it.")
    return _predicate._page(f"{name}: Agent Evidence vocabulary", term["uri"],
                            f"The {name} term of the Agent Evidence vocabulary.", "\n".join(parts), footer)


def render(index: dict) -> dict[str, str]:
    """Every generated page, by path relative to pages/vocab/v1/."""
    base = index["term_uri_base"]
    children = index["verdict_classes"]["children"]
    parent_term = index["verdict_classes"]["parent_term"]
    pages = {}
    rows = []
    for name in sorted(index["terms"]):
        term = index["terms"][name]
        pages[f"{name}/index.html"] = _term_page(name, term, children if name == parent_term else {})
        rows.append(f'<li><a href="{name}/"><code>{term["uri"]}</code></a> ({html.escape(term["criticality"])})</li>')
    digest = index["source_sha256"]
    listing = (f"<h1>Vocabulary terms, version 1</h1>\n<p>Registry version {html.escape(index['version'])}, "
               f'registryDigest <a href="registry/sha256-{digest}.yaml"><code>{digest}</code></a>.</p>\n'
               "<ul>\n" + "\n".join(rows) + "\n</ul>")
    pages["index.html"] = _predicate._page("Agent Evidence vocabulary terms", base,
                                           "The terms of the Agent Evidence vocabulary.", listing,
                                           "Agent Evidence vocabulary terms.")
    return pages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail when the pages are stale")
    args = parser.parse_args(argv)
    index = json.loads((PACKAGE / "registry.json").read_text(encoding="utf-8"))
    source = (PACKAGE / "vocabulary.yaml").read_bytes()
    if hashlib.sha256(source).hexdigest() != index["source_sha256"]:
        print("registry.json is stale: run packages/vocabulary/scripts/gen_registry_index.py", file=sys.stderr)
        return 1
    pages = render(index)
    copy = f"registry/sha256-{index['source_sha256']}.yaml"
    stale = [p for p, text in pages.items() if not (OUT / p).is_file() or (OUT / p).read_text(encoding="utf-8") != text]
    expected = set(pages) | {copy}
    extra = [str(p.relative_to(OUT)) for p in OUT.rglob("index.html")] if OUT.is_dir() else []
    extra = sorted(set(extra) - expected)
    if args.check:
        if not (OUT / copy).is_file() or (OUT / copy).read_bytes() != source:
            stale.append(copy)
        for failure in stale + [f"{p}: no longer generated" for p in extra]:
            print(f"pages/vocab/v1/{failure} is stale: run scripts/build_vocabulary_pages.py", file=sys.stderr)
        if stale or extra:
            return 1
        print(f"vocabulary pages ok ({len(pages)} pages)")
        return 0
    for path in extra:
        (OUT / path).unlink()
    for path, text in pages.items():
        (OUT / path).parent.mkdir(parents=True, exist_ok=True)
        (OUT / path).write_text(text, encoding="utf-8")
    (OUT / copy).parent.mkdir(parents=True, exist_ok=True)
    (OUT / copy).write_bytes(source)
    print(f"wrote {len(pages)} pages and {copy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
