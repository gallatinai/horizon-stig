# Findings and suggested next steps

**1,048 rules:** 159 Needs work, 779 Likely covered, 34 Unclear, 72 Needs N/A justification and 4 source-only Compliant recommendations. Needs-work rows group into **23 shared workstreams**, not 159 separate implementations.

The November 10 re-review explicitly checked all **154 previous unknowns and 257 previous needs-work recommendations**, with 613 total rule decisions including additional corrections. The [completed checklist](review/investigation-checklist.md) and [source/investigation log](evidence/product-boundary-review.json) record what was checked. The earlier review assessed generic defaults and missed available delivery artifacts; its broad bundled-Keycloak and unknown-image assumptions are superseded.

| Correction | Result and justification |
|---|---|
| Actual delivered profile | The successful UDS push published `2026.45.4-uds.1`: UDS shared identity, Core 1.14.0, 12 digest-pinned images and no bundled Keycloak. Provider account, audit, password, PKI and MFA capabilities receive credit at that boundary. |
| Actual image crypto | API/web/PostgreSQL SBOMs identify the FIPS provider and CMVP identifiers; base configuration selects approved mode. API OIDC verification uses WebCrypto. This resolves image unknowns without requiring a live cluster check. |
| Signature verification | Release code validates certificate trust, signer identity, cryptographic signatures and authenticated timestamps, bound to exact artifacts/digests before publication. Signed-package equivalence and the official manual-hash exception replace several proposed signature/allow-list fixes; universal individual-image admission is not claimed. |
| Controls elsewhere in the product | Gateway/mesh transport, static nginx configuration, centralized UDS identity/logging, native PostgreSQL recovery and application permission/label mechanisms receive credit. The API need not duplicate those controls. |
| Security mechanisms and procedures | Targeted source review, actual CI SARIF/coverage artifacts and written company policies resolve previously unfinished checks. Reviewed scanner false positives are distinguished from real scan findings; zero vulnerabilities is not claimed. |

## Remaining work

- **Application/database audit:** complete the missing actor/target/outcome and successful/denied domain/direct-database event coverage. Existing UDS events, role-change audit and proxy logs remain credited. Configure targeted pgAudit/native logging and central integrity/retention/alert routes once, rather than building an audit system for every benchmark.
- **Shared identity/session policy:** configure applicable inactivity, session limits/lifetimes, notice, exact password rules, required-card policy, CRL caching and notifications in UDS. Resolve browser-close state, account-deletion/outstanding-token termination and sensitive-action reauthentication or accepted tailoring. These are shared control changes, not separate implementations per rule.
- **Delivery and data:** fix secret environment delivery and SeaweedFS credential ConfigMap placement; define data backup/restore and the MPN local-inference profile. The actual UDS profile already removes the old bundled-Keycloak database-privilege and missing-init-resource findings.
- **Narrow crypto residuals:** actual NATS authentication uses pure-JavaScript TweetNaCl signatures outside Node's validated provider. Separately, the release signing/hash tool's crypto mode is not established by the application's FIPS image. Assess an approved implementation or accepted scoped tailoring; do not duplicate already working OIDC/mesh crypto.
- **Documentation, testing and small hardening:** complete contract-specific data/retirement/contingency details, missing security-assessment coverage, nginx version disclosure and permitted HTTP/2-to-HTTP/1 translation disposition.

The 34 remaining unknowns have precise boundaries: selected MPN storage/KMS, gateway certificate and registry settings; mission classification/availability/topology; PII-purpose policy; and named organizational approvals or historical review/training records. They are not an unfinished-code-investigation bucket. Some former N/A candidates are now unknown because the prior unclassified-only MPN assumption was unsupported.

## Lift and handoff

Allow **15–30 engineer-days, approximately 2–4 elapsed weeks with two engineers**, with low confidence until platform owners accept the control mappings and remaining mission choices. Rough allocation: 4–10 days for Horizon audit/session/secret work, 3–8 for shared provider/database/release configuration and crypto integration, and 5–10 for documentation, targeted assessment and accepted tailoring. These ranges overlap and are not independent commitments; approved platform services/tailoring can reduce engineering work. Operator/assessor waiting time is additional.

The source/configuration passes and review handoff are complete. John can review the [193 needs-work/unknown recommendations](review/human-review.csv), alongside the N/A justifications, before remediation decisions. Final per-component CKLBs and assessor acceptance remain outside this research pass. No deployment or application remediation was performed.
