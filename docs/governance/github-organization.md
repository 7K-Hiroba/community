# GitHub organization settings record

This non-secret record distinguishes desired settings from actual evidence. It contains no tokens, app keys, signer data, private membership, screenshots, or local evidence files.

## Approval and actor

- **A1 actor:** GitHub CLI account `joaodss2`, verified active `7K-Hiroba` organization admin on 2026-11-14 with `admin:org`, `repo`, and `workflow` scopes.
- **Approval:** recovered M1W1 spec `e53a67c5-a3c0-414c-9380-52d16584fa4e` and the coordinator's Work transition.
- **Scope:** only two existing private repositories and the three original plus two conditionally created approved teams. No repository was created and no other team was created, renamed, deleted, or duplicated.

## Repositories and attachments

| Repository | Actual A1 state on 2026-11-14 |
| --- | --- |
| `7K-Hiroba/.github` | Private, default `main`, initial SHA `98c5b35e90d571b6878e48ac38482850ab4fd924`; fresh-task feature attachment used; issues enabled, wiki/Projects disabled; description set to organization-profile purpose |
| `7K-Hiroba/community` | Private, default `main`, initial SHA `4e224592fdecce2a1ad9be48b00ce86fe8af1afd`, repository UUID `58ee1a81-1c8c-481b-b55f-9e322843138c`; self-attached from `main` before edits; issues enabled, wiki/Projects disabled; description set to community purpose |

The organization contains exactly `workflows`, `.github`, and `community`. Public sibling `workflows` was not modified. Legacy website and social/featured settings were not applied; repository homepages remain unset pending accurate public content and A5.

## Team reconciliation

- Preserved `hiroba-maintainers` as administrator of both repositories.
- Preserved `platform-security` with triage review access to both repositories.
- Preserved `workflows-maintainers` only on sibling `workflows`, with no mapping to these repositories.
- Verified `community-maintainers` absent, created it with closed privacy, and mapped maintain on `community`.
- Verified `legal-reviewers` absent, created it with closed privacy, and mapped triage review access to both repositories.
- No individual members were added, removed, or published.

## Actions and repository controls

Actions is enabled on both repositories. The default `GITHUB_TOKEN` is read-only, and `can_approve_pull_request_reviews` was set to `false`. `allowed_actions: all` and `sha_pinning_required: false` were observed and left unchanged; repository workflows independently enforce full-SHA references. No `pull_request_target`, publish job, publish credential, org-wide Actions change, GHCR package, release, or tag was added.

GitHub returned **403 Upgrade to GitHub Pro or make this repository public** for repository rulesets and classic `main` branch protection on both private repositories. Therefore no branch/tag protection or required-check enforcement is claimed. Until suitable plan features are available, the named admin control is the organization owner plus `hiroba-maintainers`: direct pushes, force pushes, deletions, unreviewed merges, and non-admin tag changes are prohibited by task policy, with owner-only break-glass handling recorded separately. This is an administrative fallback, not technical enforcement. Required checks remain pending actual CI observation and an available enforcement mechanism.

Both Pages endpoints returned 404, confirming Pages is unset. Secret scanning/push-protection settings were not changed. A pre-public full-history approved secret scan remains an A5 blocker.

## Drift and pending gates

- A2/A3 asset and policy reviews, A4 coordinator-confirmed merges, and actual CI evidence are tracked in the two draft PRs.
- A5 public visibility, avatar, website/social/featured settings, social previews, logged-out checks, and public metadata remain unauthorized.
- A6 CLA activation/signatures/external contributions and A7 Pages/listing remain separate gates. GHCR and production are out of scope.

Remediate drift only through the corresponding approval gate, then update this record with actor, date, evidence URL, and any unavailable/not-run check.
