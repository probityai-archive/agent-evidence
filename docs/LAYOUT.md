# Layout and releases

## Directories

| Directory | Holds | Built with |
| --- | --- | --- |
| `crates/<name>/` | one Rust crate each: `dsse`, `jcs-admit` (with its Python binding in `crates/jcs-admit/python/`) | Cargo, from inside the crate directory |
| `packages/<name>/` | one Python distribution each | uv, as members of the root uv workspace |
| `vectors/` | the conformance corpora and their harness | uv |
| `site/` | the conformance board and the pages that serve the published identifiers | the site's own build |

A directory appears when its part is imported. An import brings the source repository's full history under the new directory, so `git log --follow` and `git blame` keep working, and renames its tags with the part's prefix (below). The source repository is then archived, and its tags, releases, Actions and pages keep working.

The root `Cargo.toml` is a workspace that excludes `crates/`: each crate keeps its own `Cargo.lock` and `supply-chain/` audits, and `cargo publish` from the crate directory packages what it packaged before the import. The root `pyproject.toml` is a uv workspace over `packages/*`.

## Continuous integration

`.github/workflows/ci.yml` runs on every pull request and every push to `main`. Its `changes` job asks `scripts/workspace.py` which directories a change touches, and only their checks run. A change outside every directory, other than documentation, runs everything. The `ci-ok` job passes when every job that ran passed; it is the one required check.

## Releases

Each part has its own version line. A published GitHub release whose tag is `<prefix>-v<version>` runs `.github/workflows/release.yml`, which publishes that part only. A pushed tag alone publishes nothing.

| Tag prefix | Registry | Part |
| --- | --- | --- |
| `dsse-v` | crates.io | `crates/dsse` |
| `jcs-admit-v` | crates.io | `crates/jcs-admit` |
| `jcs-admit-py-v` | PyPI | `crates/jcs-admit/python`: seven abi3 wheels and the sdist |
| `agent-evidence-vectors-v` | PyPI | the vectors distribution |
| `agent-evidence-vocabulary-v` | PyPI | the vocabulary distribution |
| `agent-evidence-admission-v` | PyPI | the admission distribution |

`release.toml` lists the parts that have arrived. The workflow refuses a tag whose part is not listed, whose version differs from the part's manifest, or whose commit is not on `main`. Publishing uses registry trusted publishing from the GitHub environments `crates-io` and `pypi`; no registry token is stored.
