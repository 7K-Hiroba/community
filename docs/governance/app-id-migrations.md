# Application ID migrations

IDs are permanent, case-insensitive reservations. Normally the ID equals the repository name. Dashboard UID prefix is exactly `<id>-`; Grafana folder segment is exactly `<id>`, rendered beneath an approved `<org>/` folder.

A repository rename alone never changes app identity. Do not silently edit an ID, canonical repository, dashboard prefix, or folder segment, and never resolve a collision by overwriting another entry.

## Required migration shape

1. Keep the old entry as `status: deprecated` and set `replacedBy` to the current replacement ID.
2. Add the replacement with its own canonical repository, maintainers, prefix, folder, and `migratedFrom` pointing to the old ID.
3. Obtain owner and CODEOWNERS review for the reason, compatibility, communication, and rollback/transition plan.
4. Migrate dashboard UIDs, Grafana folders, source-qualified catalog references, and access policy without deleting historical evidence.
5. Run offline semantic/base-revision validation and post-migration deployment/link checks, recording actual evidence.

Cycles, unpaired changes, many-to-one implicit takeovers, deleted deprecated tombstones, reopened identities, and old-ID reuse are invalid. A deprecated entry without a replacement may remain as a permanent tombstone.

The initial registry is introduced from a base without `apps.json`; that specific absence is treated as an empty registry. All later changes compare against `origin/main` in CI.
