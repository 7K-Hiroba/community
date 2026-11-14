# Agent guidance

## Ownership boundaries

This repository owns Hiroba governance, onboarding, application identity, legal/commercial/trademark boundaries, and organization resource-access conventions. `7K-Hiroba/.github` owns the organization profile and default health files; `7K-Hiroba/workflows` owns reusable workflows. All source/reference repositories are read-only.

Do not create a public listing, enable Pages, activate CLA, collect signatures, change reference repositories, publish GHCR artifacts, or change production. External contributions and external-PR merges remain paused before A6.

## Registry invariants

Preserve case-insensitive unique IDs/repositories, canonical `https://github.com/7K-Hiroba/<id>` URLs, unique maintainer handles per entry, `<id>-` dashboard prefixes, and `<id>` folder segments. Do not encode trust, secrets, targets, releases, or signer data.

Never delete a deprecated tombstone or silently rename identity fields. Migrations require paired `replacedBy`/`migratedFrom` entries, owner review, an asset/folder plan, and validation. A genuinely absent initial `registry/apps.json` in the base revision is an empty registry; other Git errors are fatal.

## Required local checks

```bash
python3 -m pip install --require-hashes -r requirements-dev.txt
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_registry.py --registry registry/apps.json --schema registry/apps.schema.json
git fetch origin main
python3 scripts/validate_registry.py --registry registry/apps.json --schema registry/apps.schema.json --base-revision origin/main
python3 scripts/check_markdown_links.py --root .
python3 scripts/validate_workflow_pins.py .github/workflows
python3 -m json.tool registry/apps.json >/dev/null
python3 -m json.tool registry/apps.schema.json >/dev/null
git diff --check
git status --short
```

CI is deterministic and offline apart from dependency installation and the initial `git fetch`; reserved repository URLs are not fetched. Use full 40-character SHAs plus human-readable comments for every non-local `uses:` reference. Keep permissions read-only and add no publish jobs or secrets.

Link canonical legal documents instead of duplicating them. Record actual settings and evidence in `docs/governance/github-organization.md` and incomplete gates in `docs/launch-checklist.md`.
