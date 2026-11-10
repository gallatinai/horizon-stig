# Horizon STIG tracking

Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection.

| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |
|---|---:|---:|---:|---:|---:|---:|
| [ASD_V6R5_STIG](mpn/review/U_ASD_V6R5_STIG.md) | 286 | 56 | 184 | 15 | 31 | 0 |
| [Kubernetes_V2R6_STIG](mpn/review/U_Kubernetes_V2R6_STIG.md) | 92 | 2 | 89 | 0 | 0 | 1 |
| [Container_Platform_V2R5_SRG](mpn/review/U_Container_Platform_V2R5_SRG.md) | 188 | 30 | 152 | 4 | 2 | 0 |
| [Web_Server_V4R5_SRG](mpn/review/U_Web_Server_V4R5_SRG.md) | 126 | 15 | 102 | 1 | 6 | 2 |
| [Application_Server_V4R6_SRG](mpn/review/U_Application_Server_V4R6_SRG.md) | 137 | 16 | 107 | 10 | 4 | 0 |
| [Database_V4R6_SRG](mpn/review/U_Database_V4R6_SRG.md) | 142 | 24 | 95 | 4 | 18 | 1 |
| [AAA_Services_V2R3_SRG](mpn/review/U_AAA_Services_V2R3_SRG.md) | 77 | 16 | 50 | 0 | 11 | 0 |

**Totals:** 159 Needs work; 779 Likely covered; 34 Unclear; 72 Needs N/A justification; 4 source-only Compliant.

The 159 needs-work recommendations group into **23 workstreams**, not 159 separate implementations. This re-review checked all **154 previous unknowns and 257 previous needs-work rules** against the full product boundary. Unclear fell from 154 to 34 (662 in the original routing pass). Every rule has a suggested status, justification, evidence links and next action. These are recommendations, not assessor sign-off or executed runtime checks.

- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)
- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)
- [Completed investigation checklist](mpn/review/investigation-checklist.md) · [Detailed source/reviewer log](mpn/evidence/product-boundary-review.json)
- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)
- [Findings, two-pass plan and lift estimate](mpn/FINDINGS.md)
- [Evidence boundaries and exact source versions](mpn/evidence/README.md)
- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)

The reviewed published package is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Actual image SBOMs, FIPS base configuration and cryptographic release verification receive credit. A control may be implemented by the gateway, mesh, IdP, database, host or organizational procedure; the API need not duplicate it. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.

Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. The November 9 investigation is historical context; [product-boundary-review.json](mpn/evidence/product-boundary-review.json) supplies the superseding decisions. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required). No application remediation or deployment is performed.
