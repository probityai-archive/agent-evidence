#!/usr/bin/env python3
"""Check an A2A Agent Card against the Google Cloud Marketplace requirements captured in
docs/google-cloud-ready/_raw/web/s13-cloud (the "publish agents" page, MANIFEST.json).

    scripts/check_agent_card.py a2a/agent-card.json
    scripts/check_agent_card.py --selftest

Exit codes: 0 the card meets every requirement the page states, 1 it does not (each finding
printed), 2 the card could not be read, or a selftest control did not fire.

It checks what the page states and nothing else: the card is a JSON object with the required
fields; the agent declares public access (no security) or exactly the OAuth 2.0 authorization
code flow with its three URLs; a card that declares a Dynamic Client Registration extension
carries its target_url; every skill has id, name, description and tags. Whether Google accepts
the card is Google's review, not this check.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

DCR_URI = "https://cloud.google.com/marketplace/docs/partners/ai-agents/setup-dcr"
REQUIRED = ("name", "protocolVersion", "description", "url", "preferredTransport", "provider", "version", "capabilities", "skills")
SKILL_FIELDS = ("id", "name", "description", "tags")


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _auth_findings(card: dict) -> list[str]:
    security = card.get("security")
    schemes = card.get("securitySchemes")
    if not isinstance(security, list) or not isinstance(schemes, dict):
        return ["security and securitySchemes must be a list and an object"]
    if not security:
        return [] if not schemes else ["public access declares no security but securitySchemes is not empty"]
    oauth = schemes.get("oauth2")
    flow = oauth.get("flows", {}).get("authorizationCode") if isinstance(oauth, dict) and isinstance(oauth.get("flows"), dict) else None
    if not isinstance(flow, dict):
        return ["authentication must be public access or the OAuth 2.0 authorization code flow"]
    return [f"authorizationCode.{key} is missing" for key in ("authorizationUrl", "tokenUrl", "scopes") if not flow.get(key)]


def _extension_findings(card: dict) -> list[str]:
    extensions = card.get("capabilities", {}).get("extensions", []) if isinstance(card.get("capabilities"), dict) else []
    return [
        "the DCR extension carries no target_url"
        for ext in extensions
        if isinstance(ext, dict) and ext.get("uri") == DCR_URI and not _text(ext.get("params", {}).get("target_url"))
    ]


def findings(card: object) -> list[str]:
    if not isinstance(card, dict):
        return ["the card is not a JSON object"]
    out = [f"missing or empty field: {key}" for key in REQUIRED if card.get(key) in (None, "", [], {}) and key != "capabilities"]
    if not isinstance(card.get("capabilities"), dict):
        out.append("capabilities must be an object")
    provider = card.get("provider")
    if not isinstance(provider, dict) or not _text(provider.get("organization")) or not _text(provider.get("url")):
        out.append("provider needs organization and url")
    skills = card.get("skills")
    if isinstance(skills, list):
        for index, skill in enumerate(skills):
            if not isinstance(skill, dict) or not all(skill.get(f) for f in SKILL_FIELDS):
                out.append(f"skills[{index}] needs id, name, description and tags")
    out += _auth_findings(card) + _extension_findings(card)
    return out


def _selftest(card: dict) -> int:
    broken = {
        "missing description": lambda c: c.pop("description"),
        "no skills": lambda c: c.update(skills=[]),
        "skill without tags": lambda c: c["skills"][0].pop("tags"),
        "provider without url": lambda c: c["provider"].pop("url"),
        "api-key scheme": lambda c: c.update(security=[{"k": []}], securitySchemes={"k": {"type": "apiKey"}}),
        "oauth without token url": lambda c: c.update(
            security=[{"oauth2": ["s"]}],
            securitySchemes={"oauth2": {"type": "oauth2", "flows": {"authorizationCode": {"authorizationUrl": "https://a.example.org", "scopes": {"s": "d"}}}}},
        ),
        "DCR without target": lambda c: c["capabilities"].update(extensions=[{"uri": DCR_URI, "params": {}}]),
        "schemes without security": lambda c: c.update(securitySchemes={"x": {}}),
    }
    if findings(card):
        print("selftest: the committed card does not pass", file=sys.stderr)
        return 2
    for name, edit in broken.items():
        trial = copy.deepcopy(card)
        edit(trial)
        if not findings(trial):
            print(f"selftest: the control '{name}' did not fire", file=sys.stderr)
            return 2
    if not findings([]):
        print("selftest: a non-object passed", file=sys.stderr)
        return 2
    print(f"selftest: the card passes and {len(broken) + 1} broken variants are refused")
    return 0


def main(argv: list[str]) -> int:
    selftest = argv[:1] == ["--selftest"]
    rest = argv[1:] if selftest else argv
    if len(rest) > 1 or (not selftest and not rest):
        print("usage: check_agent_card.py CARD | --selftest [CARD]", file=sys.stderr)
        return 2
    path = Path(rest[0] if rest else "a2a/agent-card.json")
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"ERROR could not read {path}: {error}", file=sys.stderr)
        return 2
    if selftest:
        return _selftest(card)
    problems = findings(card)
    for problem in problems:
        print(f"FAIL {problem}")
    if not problems:
        print(f"PASS {path} meets every requirement the captured page states")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
