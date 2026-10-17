# Agent instructions

- Run `uv run --frozen --only-group dev ruff check .` and `uv run --frozen --only-group dev python -m pytest` from the root before every commit.
- Run `actionlint` after editing anything under `.github/workflows/`.
- Run `python3 scripts/readme-lint.py <README>` after editing any README. Keep each under 600 prose words; detail goes in `docs/`.
- Never edit `scripts/readme-lint.py` or `scripts/readme-lint-test.py`; they are shared byte-for-byte with sibling repositories.
- Sign off every commit (`git commit -s`).
- Rules for one part live in that part's directory. Read its `AGENTS.md` before changing it.
- An imported part adds its CI job to `.github/workflows/ci.yml` and to the `needs` of `ci-ok`, and its row to `release.toml`.
- Never push a tag to publish. A release is a published GitHub release, and `release.yml` checks it.
