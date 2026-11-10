# Candidate changes and second-pass corrections

The source assessment uses Horizon `3f3b51d454197c077b33896caf93de72b94eafda` and horizon-uds-bundle `d528b7febf1ce8bb5ccf99661dade6ae09a84381`. The bundle is a general/demo candidate with bundled identity selected by default, not a verified MPN release. A change recommendation means this candidate needs correction or an evidenced replacement/delegation before use under the corresponding check. It is not a claim about deployed MPN behavior.

| Candidate change | Rules | Recommendation and justification |
|---|---|---|
| Secret delivery | Kubernetes V-242415; V-274883 | Rendered PostgreSQL sets a secret password environment variable, which V-242415 expressly prohibits. Rendered SeaweedFS stores S3 credentials in a ConfigMap, which V-274883 prohibits. Use protected file/Secret or approved vault delivery and update consumers. The SeaweedFS S3 API already has authentication; do not report that it has none. |
| Bundled identity policy | AAA V-204644; V-204689; V-204664; V-204666–V-204669; V-204673–V-204674 | The selected candidate uses local Keycloak users, five-failure threshold, nonpermanent lockout, and a password policy specifying only hashing. The respective rules require three-failure lockout, administrator release, and explicit password constraints. Review the official check for account-type and directory-delegation exceptions before changing the selected MPN identity path. Lifetime rules exclude service accounts and the account of last resort. |

Eleven rule recommendations group into these two change areas. They are not eleven independent implementations. The missing runtime/organizational evidence can reveal additional work; it must not be silently counted as passing or as a confirmed defect.

## Important unresolved requirements

- **Identity:** The active chart supports both bundled and UDS identity; the default is bundled. Choose and record the actual MPN mode and test CAC/PIV, revocation, privileged MFA, account lifecycle and session termination along that path. The platform's identity and application's identity are distinct.
- **Audit logging:** Current Horizon logging includes request/trace IDs, event names, remote address, response status and secret redaction. Common bindings do not supply actor identity, but additional records may supply correlation. Capture end-to-end user-attributed security events before declaring the entire audit path deficient. Agree the event set, retention, access, alerting and capacity/performance requirements with John/security.
- **Database:** Preloading/installing pgaudit does not establish event coverage. Capture effective settings and sample allowed/denied event records, connection records and collection/retention evidence. Extension creation catches failures, so observe whether it is installed. Do not solve this by indiscriminately logging every statement without performance and secret-exposure review.
- **Local inference:** The October MPN decision requires local inference, but the general candidate still allows external hosted-LLM egress. Produce an MPN profile with the selected model runtime and permitted destinations. This is a deployment-requirement mismatch, not proof of an MPN production violation.
- **Model serving:** No selected self-hosted serving implementation is established by this source snapshot. Keep its Application Server mapping open instead of assessing hosted OpenAI/Anthropic as if it were the intended local service.
- **Host inheritance:** Obtain MPN's actual Kubernetes/OS checklist and UDS ASD coverage record, tied to versions and boundaries. The scope page marks scope confirmation complete but still leaves the OS unspecified; that remains unresolved here.

## False-positive controls applied in the second pass

- Plain HTTP/Postgres URLs and `sslmode=disable` do not prove unprotected wire traffic under ambient mesh. Require effective hop-by-hop protection evidence.
- Chart-local `networkPolicy.enabled=false` does not prove no network control: UDS Package resources declare generated policy. Inspect admitted policies/exemptions.
- Empty digest fields in sample values do not prove release images lack provenance: the builder verifies source digests. Assess the actual generated release.
- Browser localStorage does not by itself prove logout fails. Current code wipes auth state and invokes IdP signout; test termination and token replay.
- A FIPS image name does not prove approved validated operation. Conversely, a disabled, unused stunnel sidecar is not proof that the active mesh lacks protection.
- A single replica is not automatically an HA violation. Application Server V-204814 explicitly depends on MAC I designation.
- The older ASD worksheet is retained as historical evidence and is not attributed to today's Horizon commit.

See [second-pass changes](review/second-pass-changes.json) for recorded designation changes. The remaining broad evidence-routing recommendations were not individually validated against live runtime behavior.

## Lift

The two candidate change areas look bounded. Overall completion is still dominated by mapping, evidence and possible application/audit changes. Retain **20–40 engineer-days / approximately 3–6 weeks with two engineers** only as a low-confidence planning allowance, not a measured estimate or commitment. The present results do not validate a total remediation backlog. Re-estimate after the Unclear queue is dispositioned with component owners and John. Host/assessor turnaround is additional elapsed time; losing the assumed platform inheritance would materially expand scope.
