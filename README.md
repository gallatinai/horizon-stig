# Horizon STIG tracking

Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection. Gallatin manages this UDS Core deployment on MPN.

| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |
|---|---:|---:|---:|---:|---:|---:|
| [ASD_V6R5_STIG](mpn/review/U_ASD_V6R5_STIG.md) | 286 | 56 | 184 | 15 | 31 | 0 |
| [Kubernetes_V2R6_STIG](mpn/review/U_Kubernetes_V2R6_STIG.md) | 92 | 2 | 89 | 0 | 0 | 1 |
| [Container_Platform_V2R5_SRG](mpn/review/U_Container_Platform_V2R5_SRG.md) | 188 | 32 | 152 | 2 | 2 | 0 |
| [Web_Server_V4R5_SRG](mpn/review/U_Web_Server_V4R5_SRG.md) | 126 | 15 | 102 | 1 | 6 | 2 |
| [Application_Server_V4R6_SRG](mpn/review/U_Application_Server_V4R6_SRG.md) | 137 | 16 | 107 | 10 | 4 | 0 |
| [Database_V4R6_SRG](mpn/review/U_Database_V4R6_SRG.md) | 142 | 24 | 95 | 4 | 18 | 1 |
| [AAA_Services_V2R3_SRG](mpn/review/U_AAA_Services_V2R3_SRG.md) | 77 | 16 | 50 | 0 | 11 | 0 |

**Totals:** 161 Needs work; 779 Likely covered; 32 Unclear; 72 Needs N/A justification; 4 source-only Compliant.

The 161 needs-work recommendations group into **25 shared workstreams**. Every rule has a suggested status, justification, evidence links and next action. Final component checklists require acceptance of the stated evidence and applicability.

- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)
- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)
- [Gallatin UDS configuration actions](mpn/UDS-CONFIGURATION.md)
- [Assessment decisions](mpn/evidence/current-assessment.json)
- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)
- [Improvement priorities and effort estimate](mpn/FINDINGS.md)
- [Evidence boundaries and exact source versions](mpn/evidence/README.md)
- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)

The package baseline is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Image SBOMs, FIPS configuration and release verification support the control mappings. Gallatin manages UDS Core on MPN and owns its platform configuration. Controls may be supplied by the gateway, mesh, IdP, database, host or organizational procedure. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.

Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. [current-assessment.json](mpn/evidence/current-assessment.json) stores the status decisions and evidence references. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required).
