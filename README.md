# Agent Evidence

The open specification layer for evidence about AI agents: conformance vectors, a term vocabulary, admission rules, a conformance board, and the `jcs-admit` and `dsse` crates that canonicalize and sign records. It is maintained by Probity AI, under the [governance](GOVERNANCE.md) in this repository.

It is for people who build or check an agent-evidence verifier, and for projects that sign or canonicalize JSON records about what an agent did.

## Install

Pin the parts you use:

```bash
pip install agent-evidence-vectors==0.20.0
cargo add dsse@0.1.4 jcs-admit@0.1.2
```

## Try it

Run every vector of the default corpus through the bundled reference verifier. You need [uv](https://docs.astral.sh/uv/); nothing is cloned or built:

```bash
uvx agent-evidence-vectors==0.20.0
```

The run prints one row per vector and ends with:

```text
totals: 288 vectors, 288 pass, 0 fail; report written to conformance-report.json
```

## Status

This repository is new. Each part moves here from its own repository with its full history, one at a time, and keeps its registry name and its own version line. Until a part arrives, its old repository is where it lives and releases:

| Part | Registry name | Current home |
| --- | --- | --- |
| Conformance vectors | `agent-evidence-vectors` (PyPI) | [probityai/agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) |
| Vocabulary | `agent-evidence-vocabulary` (PyPI) | [probityai/agent-evidence/packages/vocabulary](https://github.com/probityai/agent-evidence/tree/main/packages/vocabulary) |
| Admission rules | `agent-evidence-admission` (PyPI) | [probityai/agent-evidence/packages/admission](https://github.com/probityai/agent-evidence/tree/main/packages/admission) |
| DSSE envelopes | `dsse` (crates.io) | [probityai/agent-evidence/crates/dsse](https://github.com/probityai/agent-evidence/tree/main/crates/dsse) |
| JSON admission and RFC 8785 | `jcs-admit` (crates.io, PyPI) | [probityai/agent-evidence/crates/jcs-admit](https://github.com/probityai/agent-evidence/tree/main/crates/jcs-admit) |

Moved repositories are archived, not deleted: their tags, releases, Actions and pages keep working.

## Documentation

| I want to | Read |
| --- | --- |
| See where each part lives and how it is released | [Layout and releases](docs/LAYOUT.md) |
| Contribute a change | [Contributing](CONTRIBUTING.md) |
| Become a maintainer | [Governance](GOVERNANCE.md) |
| Report a vulnerability | [Security](SECURITY.md) |

## Licence

Each directory carries its own licence file, and it applies to that directory. Files outside every such directory are under the [Apache License 2.0](LICENSE).
