# Approved SQL example

This reader compares an approval, an application record, a database audit projection, and a later state observation.
It is for people who want to test whether those records agree before connecting a native export.

Use the locked development tools. The reader itself has no external dependencies.

```sh
uv sync --frozen --group dev
.venv/bin/python -m sql_illustration.check fixtures/matching-commit-later-change.json
```

The output includes `"result": "recorded_commit_matches"` and `"later_state": "supplied_state_differs"`.
That is the useful distinction: a later change does not erase an earlier matching execution record.

Version 0.1.0. The 16 fixtures are author-created examples. This source does not invoke Tadpole or a database.
The reader compares supplied records. It does not authenticate them or prove that an audit export is complete.

| Read next | Content |
|---|---|
| [Input contract](docs/INPUT-CONTRACT.md) | Fields, exact comparisons, outputs, and native input needed |
| [Source map](SOURCE-MAP.md) | Cho's case, pinned Tadpole source, and the actual native boundaries |
| [Design decisions](docs/architecture/DESIGN_DECISIONS.md) | Why SQL bytes, outcome, and later state stay separate |
| [Join the case](https://github.com/probityai/agent-evidence-atlas/issues/49) | Bring a native pair, another reader, or a check to keep |

## Other readers

`ogasurfproject-jpg` wrote a second reader from the input contract and the 16 fixture inputs alone, without
this reader, its tests or the manifest:
[`horizon-shield@5037ecf8`, `workers/hs-ledger/nenrin/approved-sql-reader-v0/`](https://github.com/ogasurfproject-jpg/horizon-shield/tree/5037ecf8a2195f2f17f1b47ca3d2b5f49ea0a0e0/workers/hs-ledger/nenrin/approved-sql-reader-v0)
(`reader.py` sha256 `fc87a6ec...0fa0b86`, Python standard library only).
We ran it over the fixtures on 2026-10-23 with CPython 3.13.15. Against the manifest:

| Measure | Agreement |
| --- | --- |
| Exit code | 16 of 16 |
| `result` string, exactly | 4 of 16; the contract named only two results then, so the rest are the reader's own |
| Partition | Consistent: no two fixtures this reader separates fall in one manifest result |
| `later_state` | 15 of 16; it says `changed` where this reader says `supplied_state_differs` |

Its two contract gaps, a literal reading that accepts `approval.granted: false` and a missing application
record, are now closed in the [input contract](docs/INPUT-CONTRACT.md), which lists every result.
Run it from this directory:

```sh
for f in fixtures/*.json; do [ "$(basename $f)" = manifest.json ] || { python3 <path>/reader.py "$f" > /dev/null; echo "$(basename $f) $?"; }; done
```

Cho HyunJong (`hangum`) supplied the case in [the Lab thread](https://github.com/probityai/agent-evidence-atlas/issues/49#issuecomment-6072475161).
We own this illustration's fields and code. The producer owns its export semantics.
