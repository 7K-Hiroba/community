# Contributing to community governance

## Contribution gate

**External contributions are currently paused.** Authorized maintainers may prepare focused changes, but external pull requests must not be merged before the separate A6 gate. See the [default contribution policy](https://github.com/7K-Hiroba/.github/blob/main/CONTRIBUTING.md) and [Hiroba CLA status](CLA.md). No DCO substitution, emailed signatures, CLA Assistant check, or signed-agreement attachments are active.

## Maintainer workflow

1. Branch from `main` and open a draft pull request with a Conventional Commit title.
2. Link the relevant approval and identify whether the change affects governance, legal, registry, or security review.
3. Run the offline tests and validators in [AGENTS.md](AGENTS.md), then record actual local and Actions evidence and all not-run checks.
4. Obtain CODEOWNERS review and resolve conversations. Keep the pull request draft while legal, security, or launch approval is pending.

Registry changes must preserve case-insensitive ID uniqueness, exact repository/prefix/folder relationships, and permanent tombstones. Repository rename alone never changes app identity. Use a paired `deprecated` old entry and replacement entry with `replacedBy`/`migratedFrom`, an asset/folder migration plan, owner review, communication, and post-migration validation.

Do not add trust tiers, runtime targets, credentials, signer data, or secrets to `apps.json`. Reserved URLs need not resolve; reserved-to-active transitions require separate administrator/onboarding evidence that the repository and team exist with appropriate access.
