# Hiroba governance

## Roles

- **Organization owners** approve significant organizational, legal, public-launch, and production decisions and privately control team membership.
- **`hiroba-maintainers`** administer the organization profile and community repositories and steward cross-community decisions.
- **`community-maintainers`** maintain governance, onboarding, and the application registry through reviewed pull requests.
- **Application maintainer teams** own their application repositories, releases, compatibility evidence, and operational documentation. Every active application requires at least one maintainer team.
- **`platform-security`** provides combined platform and security review for trust, registry, resource-access, CI, and security-sensitive changes.
- **`legal-reviewers`** reviews contribution status, CLA links, trademark, and commercial-boundary content. Legal review does not replace owner/counsel approval.
- **Contributors** follow the current contribution gate. While external contributions are paused, only authorized maintainer-authored changes are eligible for merge.

## Decisions and review

Routine changes use pull requests, CODEOWNERS review, resolved conversations, green required checks, and accurate not-run disclosures. Significant decisions—including new trust policy, app-ID migrations, public launch, legal terms, or production access—also require the named owner approval in the applicable gate. There is no invented voting foundation or external governance authority.

Platform-governed installation and admission remain mandatory: community metadata never grants itself visibility, installation, upgrade, or production permission. A source's server-configured trust tier is distinct from registry identity.

## Escalation and lifecycle

Resolve disagreements through the relevant owning teams, then `platform-security` or `legal-reviewers` for their domains, and finally the organization owners. Security and legal escalation stays private; do not publish vulnerability or signer information.

Maintainer changes, ownership handoffs, and orphaned applications must be documented in `MAINTAINERS.md` and reviewed. Decommissioning uses the registry's permanent `deprecated` tombstone, migration pairing, communication, and validation process; it never silently deletes or reuses an identity.

Current status and deferred gates are recorded openly in [the launch checklist](docs/launch-checklist.md) and [GitHub organization record](docs/governance/github-organization.md).
