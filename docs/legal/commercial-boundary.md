# Commercial and open-source boundary

Hiroba community content follows the current Inari ADR 0005 community/services model: the community repositories and their authored content are Apache-2.0, while paid services may be offered without changing those repositories into proprietary products.

The following remain in separately owned private systems and are not community features: proprietary billing, entitlements, signup, metering, and hosted-only hub functions. Do not add license checks, feature-gating designs, usage metering, or claims that community artifacts require a hosted subscription.

## Review examples

- A signed community plugin, catalog package, chart, or observability asset with documented deployment and support boundaries belongs here.
- A hosted billing API, entitlement decision, customer meter, signup service, or proprietary control-plane extension does not.
- Documentation may explain a paid service factually when approved, but must not disguise proprietary hosted functionality as Apache-licensed community code or promise future license changes.
- Contribution rights use the [canonical CLA status](../../CLA.md); this boundary is not a substitute for owner/counsel terms or a promise of a different future license.

When classification is uncertain, stop and request `legal-reviewers` plus organization-owner review before publishing or merging. Do not infer approval from an existing private repository or an unrelated Inari component.
