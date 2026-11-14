# CLA readiness addendum

This is a readiness record, **not authorization to activate CLA Assistant or collect signatures**. Follow the canonical [Inari CLA overview](https://github.com/7K-Inari/inari-docs/blob/main/docs/legal/cla/README.md) and [activation runbook](https://github.com/7K-Inari/inari-docs/blob/main/docs/legal/cla/cla-assistant-setup.md) only after every prerequisite and the separate A6 gate are approved.

## Prerequisites

- Owner/counsel approves final ICLA/CCLA and explicit `7K-Hiroba` organization coverage, legal identity, agreement version, and jurisdiction.
- The approved canonical source SHA and change history are recorded; local documents do not diverge from it.
- Terms, privacy, signer-data retention/export, trademark filing, and all remaining G1 items have named approvals.
- An organization owner is designated for the CLA Assistant dashboard and Gist administration, with access and continuity controls.
- Target repositories are explicitly selected: `.github`, `community`, and later approved Hiroba repositories.
- Automation-only allowlists, individual/corporate signing, re-signing, and negative tests are designed and reviewed without real signer data in git.
- Required-check rollout, audit, and rollback preserve existing records and never fabricate signatures or bypass failing checks.

Hosted CLA Assistant uses its dashboard plus Gist. Do **not** add a local `.github/cla-assistant.yml` placeholder, Gist, app installation, status-check requirement, or activation claim from this task.

Until A6, external contributions remain paused, external pull requests must not be merged, and no DCO substitution or emailed/attached agreement is accepted. See the current [Hiroba CLA status](../../CLA.md).
