# Application identity registry

`apps.json` reserves stable application identities; `apps.schema.json` is the offline JSON Schema draft 2020-12 contract. The registry contains identity and ownership metadata only—never trust tiers, releases, packages, runtime targets, credentials, or signer data.

## Status meanings

- `reserved`: identity allocation only. The repository and planned maintainer team need not exist or resolve yet.
- `active`: onboarding is complete and administrator evidence confirms the repository, maintainer team, access, and required checks.
- `deprecated`: a permanent tombstone. It cannot be deleted, reopened, or reused.

Trust is assigned to a server-configured source, not self-declared in this registry. Offline CI validates structure and semantics; activation requires separate live administrator/onboarding evidence without making CI depend on the network.

## Entry contract

Each entry requires `id`, canonical `repository`, non-empty unique `maintainers`, `status`, `dashboardUidPrefix` (`<id>-`), and `grafanaFolderSegment` (`<id>`). IDs use lowercase DNS-label form, are unique under case folding, and normally equal the repository name. Runtime Grafana folders are `<org>/<id>/...` under platform policy.

The initial five reservations are `argocd`, `monitoring`, `aws`, `identity`, and `platform-essentials`. `workflows-maintainers` belongs to the sibling workflows repository and is not a sixth app identity.

## Updates and migrations

Open a focused pull request and run:

```bash
python3 -m pip install --require-hashes -r requirements-dev.txt
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_registry.py --registry registry/apps.json --schema registry/apps.schema.json
git fetch origin main
python3 scripts/validate_registry.py --registry registry/apps.json --schema registry/apps.schema.json --base-revision origin/main
```

Do not silently edit an ID, repository, dashboard prefix, or folder segment. A migration requires a deprecated old entry plus a current replacement with paired `replacedBy` and `migratedFrom`, owner review, an asset/folder migration plan, communication, and post-migration validation. Cycles, many-to-one takeovers, tombstone deletion, and old-ID reuse are invalid.

For the registry's first introduction, a base revision that genuinely has no `registry/apps.json` is treated as an empty registry. Other Git errors remain fatal.
