# Listing a verification agent in the Agent Gallery

What does the verifier need to publish an agent in the Gemini Enterprise app, and which part of that is done? This page reads the requirements from the pages Google publishes, shows the Agent Card in `a2a/agent-card.json` against them, and lists what is left.

## What Google states

Captured 2026-10-29 with `curl`. [`_raw/web/s13-cloud/MANIFEST.json`](_raw/web/s13-cloud/MANIFEST.json) records the URL, time, size and SHA-256 of each page and of its text extract. The page bytes are not committed, because third-party pages carry names and hosts the repository gates refuse; fetch a URL again and compare its SHA-256 to see whether the page changed.

The designation: "Every featured agent earns the 'Google Cloud Ready - Gemini Enterprise' designation only after passing a strict four-step evaluation for basic functionality, output accuracy, autonomous execution, and enterprise standards." The pages name the four steps and give no further criteria for them. The capture holds no per-step checklist, so a claim that the agent meets a step needs a source this capture does not provide.

The listing requirements, from the page on publishing agents (quoted):

| requirement | text on the page |
|---|---|
| A2A protocol | "Agents must comply with the A2A protocol specifications for interoperability." |
| Agent Card | "Create an Agent Card, a JSON file declaring capabilities (skills), authentication methods, and service endpoints." |
| Authentication | "Agents must support public access or OAuth 2.0 Authorization Code Grant Flow." |
| Marketplace integration | "Mandatory integration with Procurement APIs and Pub/Sub for entitlement lifecycle management." |
| Review | "Google Cloud reviews the agent's functionality, security, and pricing model before it is published to the catalog." |

## The card

[`a2a/agent-card.json`](../../a2a/agent-card.json) declares three skills, one for each check the package already runs, and public access: the agent reads public bytes the caller sends and holds no user data, which is the case the page says public access suits. Check it:

```bash
python3 scripts/check_agent_card.py a2a/agent-card.json
python3 scripts/check_agent_card.py --selftest a2a/agent-card.json
```

The first prints `PASS` when the card has every required field, every skill has an id, name, description and tags, and the authentication is public access or a complete authorization code flow. The second proves the check refuses nine broken variants of the card.

## Left to do

- The `url` is the reserved name `agent.example.org`. An A2A server that answers the three skills has to exist at the real URL before the card is uploaded. The package has the checks; it has no A2A server yet.
- The card goes to Google through a Cloud Storage bucket after a Google Cloud representative nominates the agent. Both need the operator's account.
- Procurement API and Pub/Sub integration are required for every listed agent. A free agent still needs them according to the page; confirm with the representative before building.
- Output accuracy and autonomous execution are evaluated by Google. The digest, coverage and record checks have exit codes and golden vectors, which is the evidence to offer for the first of those.
