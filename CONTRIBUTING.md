# Contributing

Issues and pull requests are welcome. A record that a verifier gets wrong, a vector whose expected outcome you dispute, or a term whose meaning is unclear are the most useful reports. Include the bytes.

## Before you open a pull request

Each directory documents its own checks in its README. From the repository root, these must pass:

```bash
uv run --frozen --only-group dev ruff check .
uv run --frozen --only-group dev python -m pytest
python3 scripts/readme-lint.py README.md
```

CI runs the checks of every directory your change touches. The one required check is `ci-ok`.

## Licence

Contributions are accepted under the licence of the directory they change, per that licence. There is no contributor licence agreement to sign.

## Signing off your commits

Every commit in a pull request carries a sign-off: a line at the end of the commit message, in the name and email of the commit's author.

    Signed-off-by: Your Name <you@example.org>

The line certifies the [Developer Certificate of Origin](DCO): that you wrote the change or otherwise have the right to submit it under this repository's licence, and that the record of your contribution is public. The text in [`DCO`](DCO) is the Linux Foundation's Developer Certificate of Origin, version 1.1, unmodified.

`git commit --signoff` (or `-s`) adds the line. To add it to commits already on your branch, run `git rebase --signoff main` and force-push the branch.

The `dco/sign-off` check verifies the line on every pull request and names each commit that lacks one. It does not ask for a sign-off on a merge commit, on a commit by a bot account, or on a maintainer's own commits.
