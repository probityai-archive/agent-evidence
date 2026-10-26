# Predicate pages and their persistent identifiers

A predicate type URI of this project is a persistent identifier under `https://w3id.org/agent-evidence/predicate/v1/`. The w3id.org service redirects it, with HTTP 302, to `https://probityai.github.io/agent-evidence/predicate/v1/<name>/`, the Pages site of this repository, and the page there is the predicate's specification rendered to HTML. The redirect rules live in `ids/agent-evidence/.htaccess` of [perma-id/w3id.org](https://github.com/perma-id/w3id.org).

| Type URI | Page | Specification |
| --- | --- | --- |
| `https://w3id.org/agent-evidence/predicate/v1/done-contract` | `pages/predicate/v1/done-contract/` | `spec/predicates/done-contract.md` of agent-evidence-vectors |
| `https://w3id.org/agent-evidence/predicate/v1/done-receipt` | `pages/predicate/v1/done-receipt/` | `spec/predicates/done-receipt.md` of agent-evidence-vectors |

## Why the identifier and the page are separate

A producer writes the type URI inside the bytes it signs, so the URI can never change. The w3id identifier carries no host: if the pages move, one pull request to w3id.org repoints every identifier, and no signed statement changes. The page address is therefore not part of any record, and nothing should cite it in place of the type URI.

## Changing a page

`pages/` is generated. Rebuild it from the specification at a pinned commit, with pandoc 3.3:

```sh
python3 scripts/build_predicate_pages.py --spec-dir <agent-evidence-vectors>/spec/predicates --commit <sha>
python3 scripts/check_predicate_pages.py
```

The build writes each page's SHA-256 to `pages/predicate/v1/PAGES.sha256`, and the check (run by the `repository` job and before every deploy) refuses a page whose bytes differ from its pin, a page whose canonical link is not its type URI, and a link to a host outside its list. A page changes only when its specification changes, and the pin moves in the same commit.

Whatever later serves the Pages site of this repository must keep serving `pages/` at the same paths, because the w3id rules point there.

## Vocabulary term URIs

Every term of `packages/vocabulary/vocabulary.yaml` has the URI `https://w3id.org/agent-evidence/vocab/v1/<term>`, and each registered value is that URI with the value as its fragment, for example `https://w3id.org/agent-evidence/vocab/v1/observation_vantage#substrate`. The page behind each one is generated, never edited:

```sh
cd packages/vocabulary && python3 scripts/gen_registry_index.py && cd ../..
python3 scripts/build_vocabulary_pages.py
```

The first command writes `packages/vocabulary/registry.json`, which carries the SHA-256 of the exact `vocabulary.yaml` bytes (the `registryDigest` a record carries); the second writes `pages/vocab/v1/` and publishes those bytes at `pages/vocab/v1/registry/sha256-<hex>.yaml`.

`w3id/agent-evidence.htaccess` is the copy, kept here, of `ids/agent-evidence/.htaccess` in perma-id/w3id.org. `scripts/check_uris_resolve.py` applies it to every predicate type URI, term URI and value URI, and fails when one does not land on a page and anchor under `pages/`; the repository job runs it on every pull request. `--network` (the `uris-network` workflow) also compares the copy with the live rules and requests every identifier, so a rule added to the copy and not yet merged upstream shows there.
