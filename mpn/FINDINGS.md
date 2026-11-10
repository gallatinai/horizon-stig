# Findings and suggested next steps

**1,048 rules: 257 Needs work, 586 Likely covered, 154 Unclear, 47 Needs N/A justification and 4 source-only Compliant recommendations.** The 257 needs-work rows group into [25 workstreams](review/workstreams.md). This is a candidate assessment, not 257 independent bugs or a finding against a running MPN system.

The original review left 662 unclear. The deeper investigation inspected pinned Horizon, bundle, UDS Core 1.14.0 and identity-config 0.32.0 source, upstream PostgreSQL/pgAudit/Keycloak behavior, and all 13 candidate chart renders. There are 949 explicit deeper rule decisions, plus retained exact candidate checks and MPN-owned Kubernetes inheritance recommendations. All 286 ASD rules now have explicit decisions; the scope's broad UDS inheritance assertion is not used to pass application training, governance or vulnerability testing requirements.

| Area | Recommendation and reason |
|---|---|
| Application and database audit | Complete actor-attributed success/denial events, required event/context selection and central forwarding. API trace IDs and selected role-change records provide partial coverage. PostgreSQL preloads pgAudit but does not configure audit classes; its default is none. Bundled Keycloak stores events locally without the UDS JSON listener. |
| Identity, sessions and PKI | Choose the actual MPN provider. Bundled Keycloak defaults differ from platform UDS: five-failure lockout, nonpermanent lockout, hashing-only password policy, no configured CAC/PIV flow. Configure lifecycle, administrator idle/session limits, notice and trust/revocation requirements. Offline API JWT verification leaves a revocation window; explicit logout already exists. |
| Secrets and database privilege | Remove secret environment delivery and SeaweedFS credential ConfigMap placement; S3 authentication already exists. Give bundled Keycloak a restricted database identity instead of the database administrator role. |
| Platform integration | Configure actual security/audit alert routes and recipients, image/component allow-list and approved-signer enforcement. Signed CI attestations and hashes alone do not require signer verification at deployment. Falco detection alone does not revoke access. |
| MPN profile and data recovery | Replace hosted-model egress with approved local inference flows and select the model-serving product. Configure database/data backup and demonstrate secure restore; Core Velero defaults do not snapshot data volumes. |
| Workload/web configuration | Supply missing init-container resources. Resolve explicit nginx binding, HTTP protocol requirements, trusted original-client audit context and other generic web hardening/tailoring. Keycloak's JavaScript-readable session-status cookie requires product-specific HttpOnly tailoring, not a blanket assertion that all cookies comply. |

UDS source supports concrete controls previously left unclear: Pepr privilege restrictions, namespace default-deny policies, STRICT mesh mutual TLS, HTTPS ingress, Vector/Loki collection, protected Grafana access and supported hardened/FIPS offerings. These recommendations remain conditional on the selected release/flavor, policies and exemptions. Platform FIPS support does not prove the Node, bundled Keycloak or signing-runner cryptographic modules are validated.

## First and second pass tonight

1. **First pass — inventory and source disposition:** preserve official packages, full check/fix text and source versions; assign a proposed status and justification to every rule. Completed in this repository; the frozen original review is retained separately from the deeper decisions.
2. **Second pass — exact-check challenge:** test candidate assumptions against rendered charts, current application source and the pinned UDS mechanisms/defaults. Correct false positives and inherited overclaims, group repeated gaps, and leave an explicit evidence request for each remaining unknown. Completed as a source/configuration review; no live official MPN checks are claimed.
3. **Review handoff:** John reviews the [411 Needs work/Unclear rows](review/human-review.csv), with identity choice, audit event/retention policy, local model selection and host inheritance as the first decisions. Confirm the actual release and deployment overrides before converting recommendations into component CKLB results. No application remediation has been performed.

## Lift estimate

Allow **20–40 engineer-days, roughly 3–6 elapsed weeks with two engineers**, with low confidence until identity delegation, audit acceptance and the actual MPN release are selected. Straightforward chart/policy fixes should take days; actor-aware audit coverage, session/revocation behavior, PKI integration and tested data recovery can take weeks. Evidence/checklist assembly and assessor/platform-owner turnaround add elapsed time. The 154 unclear items are specific deployment, organizational approval or targeted test evidence requests; they are not all code work. Losing the assumed platform/host inheritance or introducing a new local model runtime materially increases this estimate.

See [requirements and source links](REQUIREMENTS.md), [all workstreams](review/workstreams.md), and [remaining evidence decisions](review/remaining-evidence.md).
