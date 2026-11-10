# Suggested workstreams

Repeated requirements are grouped here; each linked benchmark table has the full justification and evidence. These are candidate corrections/tailoring proposals, not approved implementation tickets.

| Workstream | Needs-work rules | First action |
|---|---:|---|
| account-lifecycle | 6 | Enable35-day inactivity enforcement for applicable nonexempt UDS accounts or supply the actual authoritative-directory setting. |
| application-auditing | 34 | Define required domain events and add only missing actor/target/outcome records and correlation to central collection. Reuse role/transaction/UDS events for operations they already cover. |
| audit-alert-routing | 33 | Enable the relevant centralized account-change alerts and map named SA/ISSO routes, or retain existing accepted operator routing evidence. |
| central-log-integrity | 1 | Map an accepted immutable/authenticated centralized storage or log hash/sign control to the record lifecycle, or enable it centrally; do not implement per-API duplicate log signing. |
| compliance-package | 7 | Complete the MPN data-element/protection requirements by applying the contract-specific categories to existing architecture/security design. |
| continuous-vulnerability-management | 1 | Map an existing accepted DU/MPN recurring scanning service to the fixed delivered image inventory, or configure a scheduled rescan/cadence with retained results; do not duplicate the existing build scans. |
| data-backup-restore | 3 | Attach an accepted platform data-backup/restore service or configure PostgreSQL/PVC data protection and secure restore verification. |
| data-label-policy | 1 | Set the MPN data classification and provide the required application/report markings or exact permitted manual procedure/tailoring. |
| database-account-policy | 1 | Set approved service/admin per-role connection limits, with service-pool allowances; do not force2 if approved service-account limits differ. |
| database-auditing | 19 | Enable the required native connection/disconnection/privileged/direct-access event selection and contextual fields, with data/performance/redaction review; one shared audit workstream covers these rows. |
| identity-policy | 18 | Enable a supported previous-logon display/theme extension at the provider, or document accepted tailoring. |
| mpn-network-profile | 2 | Select the local model service and approved destination/port profile, then encode it in the existing UDS Package policies or document accepted changed scope. |
| nats-auth-crypto-module | 1 | Route the NATS client/callout authentication signature operations through a validated approved-mode implementation, or obtain explicit accepted cryptographic-boundary tailoring for the existing protected mesh path. Credit current UDS/OIDC FIPS controls. |
| notice-banner | 6 | Enable and supply the approved notice text/acknowledgement in UDS identity; document any accepted inherited entry-point banner. |
| pki-authentication | 2 | Select/enforce required PIV/CAC identity flows and privileged-card policy at sharedUDS, or record accepted externalprovider enforcement. |
| pki-trust | 5 | Enable and refresh approved local CRL/cache at UDS identity or record the official SIPR/CA-access applicability exception. |
| release-crypto-provider | 2 | Use a verified validated/approved-mode signing implementation or record approved signing-scope/risk tailoring; retain tool module provenance. |
| runtime-response | 1 | Configure an accepted Falco/security event-to-access-control response or record approvedtailoring for the exactautomated integration. |
| secret-delivery | 2 | Move affected secret consumers to protected file/vault delivery, or retain a formally accepted environment-delivery exception with the corresponding protection rationale. Reuse the shared secret-delivery workstream. |
| security-assessment-coverage | 2 | Add or attach a scoped active/fuzz security assessment for web/API and relevant parsers, reusing the existing CI artifacts and defect process. |
| session-policy | 10 | Set the approved per-user maximum in UDS identity, or document an accepted unlimited policy/tailoring. No Horizon session-limiter code is needed. |
| web-hardening | 1 | Disable nginx version disclosure in error bodies or use a generic error response while retaining existing gateway header stripping. |
| web-http-protocol | 1 | Document operationally necessary translation, HTTP1 request validation/smuggling controls and CATIII/accepted tailoring, or configure end-to-endH2 if required. |
