# Hiroba launch checklists

Check items only with recorded evidence. Unchecked items are incomplete, not implied failures or approvals. Evidence containing secrets, private member data, or signer data stays outside git.

## 1. Private foundation → public organization/profile (A1–A5)

### A1 private administration

- [x] Existing private `.github` and `community` repositories preserved on their recorded initial `main` SHAs; no repository was created.
- [x] Original teams preserved; only missing `community-maintainers` and `legal-reviewers` were created after verification and mapped as approved.
- [x] Issues enabled, wikis/Projects disabled, Actions read-only token and no PR-approval permission verified.
- [x] Pages 404/unset verified; no GHCR, release, tag, app, or public setting changed.
- [ ] Branch/tag rules and required checks are technically enforced, or the approved private-plan fallback remains recorded in [the organization record](governance/github-organization.md).

### A2/A3 content, brand, and policy review

- [ ] Profile/default health files and approved dark-green assets/provenance are committed and reviewed in the `.github` draft PR.
- [ ] Governance, registry, legal/commercial/trademark, resource-access, and paused-contribution content is reviewed in the `community` draft PR.
- [ ] `legal-reviewers` and `platform-security` complete their respective reviews; owner/counsel CLA coverage remains separately unresolved.
- [ ] LICENSE, Contributor Covenant, security fallback, issue/PR templates, and contribution status are accurate.
- [ ] Registry schema/semantic/migration tests and actual CI evidence pass; local links and immutable workflow references pass.

### A4 merge gate

- [ ] Both PRs have actual green CI, CODEOWNERS review, resolved conversations, no secrets/PII, and complete not-run disclosures.
- [ ] Coordinator explicitly confirms each squash merge. Until then both remain draft.

### A5 public launch — not authorized

- [ ] Legacy `/hiroba` website content is replaced by its owning M3 task and verified live; no stale link is published.
- [ ] Future user/org-owner approval is recorded for visibility, avatar, website/social/featured settings, and repository social previews.
- [ ] Approved full-history secret scanner passes both repositories; manual review alone is not accepted as equivalent.
- [ ] Public metadata, canonical docs/contact/social links, asset notices, and existing-only featured repositories are applied.
- [ ] Logged-out desktop/mobile light/dark profile, repository, link, image, issue-form, and content-type checks pass with evidence.

## 2. External contributions / G1 (A6)

- [ ] Owner/counsel approves final ICLA/CCLA and explicit `7K-Hiroba` coverage, legal identity, version, jurisdiction, privacy/retention/export, and all G1 items.
- [ ] CLA Assistant installation/dashboard/Gist owner, target repositories, allowlists, positive/negative tests, required-check rollout, and rollback are approved and evidenced.
- [ ] No signatures or signer PII enter git; accurate activation status replaces paused text only after the verified check is live.
- [ ] External-contribution reopening is separately announced; external merges remain prohibited before then.

## 3. Future static listing (A7 / task #14)

- [ ] ArgoCD dogfood, all six SDK gaps, launch hygiene, and user/admin Pages approval are complete.
- [ ] The separately owned listing generator validates signed repository indexes and untrusted metadata without duplicating the app registry.
- [ ] Documentation, preview, responsive/logged-out checks, and rollback evidence pass before any public listing.

No Artifact Hub, npm scope, embedded dashboards, GHCR publication, production change, or public launch is approved by this checklist.
