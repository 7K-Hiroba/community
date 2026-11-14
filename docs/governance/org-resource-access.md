# Organization resource access

This is a documentation convention for the platform's generic organization resource-target resolver, not a second resource catalog or a monitoring-only ACL system.

## Target descriptor and providers

Platform teams register or adopt resources in organization inventory with:

- `resourceRef` and `orgId`
- capabilities and non-secret type-specific configuration
- renderer/baseline-repository binding
- `view` and `use/provision` grants

Capability providers own validation, UI schema, defaults, policy hooks, and readiness checks. Secrets stay in approved secret stores, never in this registry or documentation.

`view` controls discovery. `use/provision` controls selection and provisioning. The server independently enforces entitlement when listing targets and when validating submitted DeploymentPlans, including stale or revoked grants. Teams cannot submit arbitrary URL, cluster, repository, folder, or datasource bindings.

## Monitoring and generality

Monitoring/Grafana is the first new consumer. Platform policy owns central/local evaluation, folder, datasource, approval, and readiness rules. The same inventory/RBAC path must also expose at least one existing target type—such as a deployment cluster or Git repository—to prove the model is generic.

Onboarding validates target ACLs and team self-service policies against platform guardrails. Central changes follow renderer → reviewed baseline pull request → required approval → ArgoCD; no direct Grafana writes, hub-originated Grafana API calls, embedded dashboards, or observability-only ACL catalog is introduced.

Actual multi-target companion rendering and deployed verification remain gated on the platform renderer/multi-repo milestone. This document does not authorize pre-gate adapters or production changes.
