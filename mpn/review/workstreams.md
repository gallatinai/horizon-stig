# Suggested workstreams

Repeated requirements are grouped here; each linked benchmark table has the full justification and evidence. These are candidate corrections/tailoring proposals, not approved implementation tickets.

| Workstream | Needs-work rules | First action |
|---|---:|---|
| account-lifecycle | 18 | Configure or document the accepted delegated lifecycle policy and account-type exceptions. |
| application-auditing | 43 | Complete the shared audit event catalog, actor attribution and forwarding; verify each required event rather than enabling indiscriminate payload logging. |
| approved-image-policy | 2 | Implement or evidence an accepted approved-image/component allow-list. |
| audit-alert-routing | 35 | Configure the shared identity/security alert routing and named recipients. |
| audit-retention | 1 | Complete identity audit forwarding and define/implement the required active/archive retention and capacity policy. |
| compliance-package | 6 | Complete the shared compliance package with chosen product guidance and component evidence. |
| continuous-vulnerability-management | 1 | Attach the actual DU/CAT/MPN continuous scanning service and cadence, or configure one and document its scope. |
| data-backup-restore | 3 | Configure database/data backup and secure restore verification. |
| database-account-policy | 11 | Set approved per-role concurrent-connection limits (including service-account/pool allowances) and verify the selected database configuration. |
| database-auditing | 23 | Define the approved event set, enable targeted pgaudit/native connection/context settings, forward to Loki and validate records plus performance/secret redaction. One audit configuration workstream covers these rules. |
| database-service-privilege | 2 | Provision a restricted Keycloak database role. |
| identity-audit-forwarding | 1 | Enable a suitable event listener/forwarder for bundled Keycloak or consume the UDS identity service. |
| identity-policy | 37 | Configure/test the three-failure policy at the actual login provider. |
| mpn-network-profile | 5 | Approve and implement the MPN-specific flow allow-list. |
| notice-banner | 6 | Configure the notice and explicit acknowledgement on the actual application entry point. |
| pki-authentication | 19 | Adopt the approved UDS/MPN identity profile or configure equivalent controls in bundled mode; record account/path applicability. |
| pki-trust | 17 | Select and configure the accepted MPN identity/trust path, including required federal issuers and offline revocation policy. |
| release-signature-enforcement | 4 | Enforce approved-signer verification or accepted signed-package equivalent. |
| runtime-response | 1 | Define the approved automated response/integration or obtain assessor tailoring; do not treat a dashboard alert as an access-control action. |
| secret-delivery | 2 | Move credentials to protected mounted files/vault-supported delivery and adapt consumers; rerender and verify admitted pods. Review with John before implementation. |
| session-policy | 13 | Configure approved per-user/admin session limits. |
| web-audit-context | 1 | Configure a trusted forwarding chain and original-client-IP audit field; do not trust arbitrary user-supplied X-Forwarded-For. |
| web-hardening | 3 | Bind the approved interface or document/obtain accepted container-network tailoring; this corrects the earlier overbroad source-pass designation. |
| web-http-protocol | 2 | Configure the required protocol path or seek the explicit permitted downgrade disposition using the official check, including ambiguity/smuggling controls. |
| workload-resource-policy | 1 | Set the required resource requests/limits on all application/init containers or record approved exceptions. |
