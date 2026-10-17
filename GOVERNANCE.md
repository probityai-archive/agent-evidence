# Governance

This repository holds a shared specification layer: vectors, vocabulary, admission rules, a conformance board and two crates. It is run so that anyone who builds against it can help decide it.

## Roles

- **Contributors** open issues and pull requests. Anyone can.
- **Maintainers** review and merge pull requests, cut releases and decide open questions. The current maintainers are listed in [MAINTAINERS.md](MAINTAINERS.md), with the parts of the repository each one looks after.

## Becoming a maintainer

The path is open to anyone, from any organisation.

1. Contribute: reviewed pull requests, careful reviews of other people's pull requests, issues that find real defects, or an independent implementation that runs against the vectors.
2. Any maintainer can nominate a contributor in a public issue, naming the work that supports the nomination.
3. The nomination passes when no maintainer objects within ten working days. An objection must give its reason in the issue.

The goal is maintainers from at least two organisations, and no single organisation holding a majority, as soon as enough people qualify.

## Decisions

- Most changes merge when one maintainer who did not write them approves, and CI passes.
- A change to a wire identifier, a predicate type, a vocabulary term's meaning, or an admission rule's outcome needs two maintainer approvals and a public issue open for at least five working days before merge. Published identifiers are never reused for a different meaning.
- When maintainers disagree, they try to reach consensus in the issue. If that fails, a simple majority of maintainers decides, and the reasons are recorded in the issue.

## Releases

Each part has its own version line and tag prefix ([layout and releases](docs/LAYOUT.md)). Any maintainer can cut a release once CI is green on `main`. Releases publish through registry trusted publishing; no maintainer holds a registry token for this repository.

## Changes to this document

A change to this file follows the rule for wire identifiers above.

## A future home

If a neutral foundation accepts the project, the maintainers decide by the rule above whether to move it there. Published identifiers and package names stay as they are.
