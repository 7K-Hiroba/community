# Application onboarding

This checklist distinguishes the target contract from tools already available. Reservation does not make an app trusted, and planned capabilities must not be documented as available.

## 1. Reserve identity and ownership

- Reserve a permanent lowercase app ID in `registry/apps.json`, normally matching the repository name.
- Record the canonical repository URL, planned `<app>-maintainers` handle, `<id>-` dashboard prefix, and `<id>` folder segment.
- Create or onboard the repository and team only through separately approved administration. Verify maintainer rights and CODEOWNERS before activation.

## 2. Scaffold and document

- When available, generate the application skeleton with `inari hiroba init <name>` and the approved options. Until that command exists, follow the reviewed repository contract without claiming CLI verification.
- Include Apache-2.0, an accurate README with a deployment example when deployable, security contacts, ownership, and pre-v1/status disclosures.
- Use app config v2 with explicit `archetype: stack|non-stack`; classification is never inferred from charts/KRO or silently defaulted. Use full-SHA reusable-workflow callers with version comments and read-only tokens. Never use mutable release/production references.

## 3. Validate artifacts and evidence

- Require all applicable package, chart, plugin, UI, registry, link, and contract lanes to pass.
- Require signed releases, verified digest/OIDC publisher, SLSA provenance, and release-linked signed test evidence for official/reviewed sources.
- Reviewed runtime applications need at least one meaningful Argo runtime-smoke journey; static packages are exempt.
- UI plugins need current browser mount and declared-slot compatibility evidence, no older than seven days for reviewed status.
- Verify generated chart/observability-pack output is synchronized and packaged artifacts match reviewed sources.
- For `archetype: stack`, require complete `tests/stack` install+same-cluster-upgrade declarations and the immutable lifecycle caller under the [shared stack-testing contract](https://github.com/7K-Hiroba/workflows/blob/main/docs/stack-testing.md). Require a passing result whose `headSha` exactly matches the reviewed source, and require the stable result check where repository enforcement supports it. Missing declarations or exact-head evidence fail onboarding. Non-stack sources explicitly declare `non-stack` and acquire no stack lane. Lifecycle evidence is not deployed production readiness.
- Validate dashboard UID and folder prefixes against the registry. Do not publish `latest` as an implicit deployment identity.

## 4. Review access and activate

- Complete trust-tier, legal, security, trademark, commercial-boundary, and artifact-admission review.
- Validate organization resource-target ACLs, team self-service policy, folder/datasource/evaluation rules, and renderer/baseline bindings where applicable. Teams may not supply arbitrary URLs, clusters, or repositories.
- Record actual CI runs and not-run checks. A repository/team existence check is required for reserved → active but is not a substitute for the other gates.
- Update the registry only after the evidence is complete. Offline validators never require reserved URLs to resolve.

## 5. Maintain and deprecate

Keep dependencies, contracts, provenance, runtime/browser evidence, and ownership current. Demote or suspend trust when evidence becomes stale. For decommissioning, use a permanent deprecated tombstone and the paired migration process; never silently delete or reuse an ID.
