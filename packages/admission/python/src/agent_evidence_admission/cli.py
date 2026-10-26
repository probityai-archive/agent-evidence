"""Command line.

``agent-evidence-admission digest-check <document> <artifact>``: exit 0 when the artifact has a
digest the document names, 1 when it does not (or the document names none), 2 when the document
or the artifact could not be read.

``agent-evidence-admission coverage-check <document> --required <list>``: exit 0 when every
required class is accounted for, 1 when any is missing, doubly selected, or not assessed with no
reason and no covering reference, 2 when the document or the list could not be read.
"""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .coverage_check import (
    check,
    detect_format,
    format_report,
    parse_required,
)
from .digest_check import check as digest_check
from .digest_check import parse_document, read_source


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-evidence-admission")
    parser.add_argument("--version", action="version", version=f"agent-evidence-admission {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    digest = commands.add_parser(
        "digest-check",
        help="check that an artifact has a digest its document (TEA, CycloneDX, in-toto) names",
    )
    digest.add_argument("document", help="path or https URL of the document that names the digest")
    digest.add_argument("artifact", help="path or https URL of the artifact the document covers")
    coverage = commands.add_parser(
        "coverage-check",
        help="check that a CycloneDX BOM or SPDX 3 document accounts for every class a buyer requires",
    )
    coverage.add_argument("document", help="path or https URL of the CycloneDX JSON BOM or SPDX 3 JSON-LD document")
    listing = coverage.add_mutually_exclusive_group(required=True)
    listing.add_argument("--required", help="path or https URL of the required-class list: a JSON array, a JSON object, or names")
    listing.add_argument("--require", help="the required classes inline, separated by commas")
    coverage.add_argument("--require-complete", action="store_true", help="fail a class stated incomplete as well")
    coverage.add_argument("--json", action="store_true", help="print the report as JSON")
    return parser


def _run_digest(args: argparse.Namespace) -> int:
    try:
        document = parse_document(read_source(args.document))
        artifact = read_source(args.artifact)
    except (OSError, ValueError) as error:
        print(f"ERROR could not read: {error}", file=sys.stderr)
        return 2
    result = digest_check(document, artifact)
    if result.ok and result.matched:
        algorithm, value = result.matched
        print(f"PASS {args.artifact} has {algorithm}:{value}, named in {args.document}")
        return 0
    named = ", ".join(f"{a}:{v}" for a, v in result.declared) or "nothing"
    print(f"FAIL {result.reason}: {args.document} names {named}")
    return 1


def _run_coverage(args: argparse.Namespace) -> int:
    try:
        document = json.loads(read_source(args.document))
        text = args.require if args.require is not None else read_source(args.required).decode("utf-8")
        required = parse_required(text, detect_format(document))
        report = check(document, required, require_complete=args.require_complete)
    except (OSError, ValueError) as error:
        print(f"ERROR could not read: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report.as_dict(), indent=2) if args.json else format_report(report))
    return 0 if report.ok else 1


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    return _run_digest(args) if args.command == "digest-check" else _run_coverage(args)


if __name__ == "__main__":
    sys.exit(main())
