# Horizon STIG tracking

Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 9 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection.

| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |
|---|---:|---:|---:|---:|---:|---:|
| [ASD_V6R5_STIG](mpn/review/U_ASD_V6R5_STIG.md) | 286 | 90 | 105 | 70 | 21 | 0 |
| [Kubernetes_V2R6_STIG](mpn/review/U_Kubernetes_V2R6_STIG.md) | 92 | 2 | 87 | 2 | 0 | 1 |
| [Container_Platform_V2R5_SRG](mpn/review/U_Container_Platform_V2R5_SRG.md) | 188 | 28 | 139 | 20 | 1 | 0 |
| [Web_Server_V4R5_SRG](mpn/review/U_Web_Server_V4R5_SRG.md) | 126 | 28 | 80 | 10 | 6 | 2 |
| [Application_Server_V4R6_SRG](mpn/review/U_Application_Server_V4R6_SRG.md) | 137 | 34 | 74 | 23 | 6 | 0 |
| [Database_V4R6_SRG](mpn/review/U_Database_V4R6_SRG.md) | 142 | 41 | 71 | 25 | 4 | 1 |
| [AAA_Services_V2R3_SRG](mpn/review/U_AAA_Services_V2R3_SRG.md) | 77 | 34 | 30 | 4 | 9 | 0 |

**Totals:** 257 Needs work; 586 Likely covered; 154 Unclear; 47 Needs N/A justification; 4 source-only Compliant.

The 257 needs-work recommendations group into **25 workstreams**, not 257 separate implementations. Unclear fell from 662 to 154 after source investigation. Every rule has a suggested status, justification, evidence links and next action. These are recommendations, not assessor sign-off or executed runtime checks.

- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)
- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)
- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)
- [Findings, two-pass plan and lift estimate](mpn/FINDINGS.md)
- [Evidence boundaries and exact source versions](mpn/evidence/README.md)
- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)

UDS Core **1.14.0** was inspected at the candidate’s pinned baseline, including Pepr, Istio, identity, logging, monitoring, backups and hardened offerings. Horizon’s candidate selects **its own bundled Keycloak**; platform identity defaults do not automatically apply to it. Hardened/FIPS platform recommendations depend on the actual supported flavor. The selected MPN release, image/module certificates, host inheritance and operational approval/test records remain external inputs.

Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. The deeper decision log is preserved in [source-investigation.json](mpn/evidence/source-investigation.json). `scripts/investigate.py` refreshes it against the pinned local source snapshots; `scripts/render_candidate.py <bundle-checkout>` reproduces the 13 candidate chart captures (Helm and PyYAML required). No application remediation or deployment is performed.
