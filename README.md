# Horizon STIG tracking

Provisional MPN recommendations, 9 November 2026. Start with the list below; each link opens the complete rule list with a suggested status, justification, source evidence, and next check.

| Benchmark | Rules | Suggested designation | Why |
|---|---:|---|---|
| [ASD V6R5](mpn/review/U_ASD_V6R5_STIG.md) | 286 | Likely covered, subject to inheritance evidence | Austin's current scope asserts UDS Core coverage. Obtain the attestation and identify Horizon-specific residuals; UDS presence is not a blanket application pass. |
| [Kubernetes V2R6](mpn/review/U_Kubernetes_V2R6_STIG.md) | 92 | Likely covered for host controls; mixed for workloads | MPN owns cluster/nodes. Candidate manifests show secret-delivery gaps that remain Gallatin's responsibility. |
| [Container Platform SRG V2R5](mpn/review/U_Container_Platform_V2R5_SRG.md) | 188 | Unclear | UDS supplies mechanisms, but effective configuration, exemptions, operational evidence and inheritance are still needed. |
| OS STIG, distribution/version TBD | — | Likely covered; baseline selection outstanding | MPN owns the node OS. Do not substitute an old Amazon Linux or other baseline without confirming the actual host. |
| [Web Server SRG V4R5](mpn/review/U_Web_Server_V4R5_SRG.md) | 126 | Unclear | Evaluate the tenant gateway and nginx separately; image/runtime settings and accepted delegation remain unverified. |
| [Application Server SRG V4R6](mpn/review/U_Application_Server_V4R6_SRG.md) | 137 | Unclear | Navigator services, storage and model serving need individual mappings and runtime checks. Largest expected workstream. |
| [Database SRG V4R6](mpn/review/U_Database_V4R6_SRG.md) | 142 | Unclear | pgaudit is preloaded, but effective audit settings, roles, protection, retention and recovery are unverified. |
| [AAA Services SRG V2R3](mpn/review/U_AAA_Services_V2R3_SRG.md) | 77 | Needs work in bundled candidate; other rules unresolved | The source default uses Horizon's own Keycloak. Its lockout/password settings do not match several explicit checks. UDS SSO cannot be assumed. |

**1,048 rules inventoried:** 368 Likely covered, 662 Unclear, 11 Needs work, 7 Needs N/A justification, 0 Compliant. These are recommended triage designations, not formal STIG results. Likely covered still needs evidence; Unclear is not a defect count. The missing OS baseline is tracked separately and is not part of 1,048.

- [All recommendations (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix text](mpn/review/suggested-statuses.json)
- [Candidate changes and second-pass corrections](mpn/FINDINGS.md)
- [Requirements found in Slack, Drive and the linked task](mpn/REQUIREMENTS.md)
- [Evidence scope and limitations](mpn/evidence/README.md)
- [Human-review queue](mpn/review/human-review.csv)
- [Official benchmark sources, hashes and counts](mpn/benchmarks/manifest.json)

This run completed an initial evidence-routing pass and a bounded second source/configuration pass. It did not run every official check or access a live MPN cluster. Many recommendations are explicitly unresolved; final component checklists, accepted N/A/inheritance, remediation and sign-off remain separate work. The two passes generated here are not the earlier first-pass output mentioned in Slack, which was not available as a separate artifact.

Rebuild locally with Python 3: `python3 scripts/import_benchmarks.py`, `python3 scripts/build_review.py`, then `python3 scripts/validate.py`. The importer retains cached source packages and does not silently update the selected versions. No application code or runtime configuration is modified.
