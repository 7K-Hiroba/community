# Trust tiers

Trust is assigned to a **server-configured source** and displayed through its source label. It is never self-declared in `registry/apps.json` or inferred from a repository name. Older “first-party” and “third-party-reviewed” terms map to `official` and `reviewed` only after equivalent evidence is verified; no WASM or assumed-safe untrusted runtime tier is created.

## Official

For 7K-owned sources under direct platform governance. Require:

- Reviewed ownership, immutable workflows, signed releases, and protected publishing paths.
- Verified artifact signature, digest, expected OIDC publisher, SLSA provenance, and current release-linked signed test evidence.
- All applicable runtime, browser/slot, compatibility, and operational checks, with honest freshness and not-run records.
- Platform approval before visibility, installation, and upgrades.

## Reviewed

For community sources that pass an explicit platform/security review and continuous evidence requirements. Apply the same signature, digest, publisher, provenance, and signed-test requirements as official. Reviewed runtime applications need a meaningful Argo runtime-smoke journey; static packages are exempt. UI plugins need browser mount and every declared-slot compatibility check within the last seven days.

Reviewers verify packaging boundaries: inherited authentication, no ambient credentials, declared UI slots and backend endpoints, pinned contracts, structured errors, minimal B6 attack surface, and platform approval before visibility/install/upgrades.

## Experimental

For early evaluation with visibly limited support and no production trust claim. Signature and publisher verification remain the default. Unsigned use requires an explicit **development-only** exception in server configuration, is visibly marked, and cannot target production. Experimental status is not a bypass for legal, security, or contribution policy.

## Ongoing review and demotion

Evidence ages, contract changes, failed compatibility, revoked ownership, missing provenance, or security findings can suspend or demote a source. Re-review requires fresh evidence; a green historical badge is not permanent. Admission verifies both index and selected artifact again at deploy/render, retains last-good state on sync failure, and never silently promotes a channel.

The registry records app identity only. It does not encode these tiers or override server admission.
