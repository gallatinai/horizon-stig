# Open STIG work by category

The 252 open rules (176 Needs work, 73 Needs N/A justification, 3 Unclear) fall into three categories. Each list is ordered from least to most effort. Effort is a rough engineering estimate for the whole item, not per rule.

## 1. Horizon code changes

Changes to the Horizon application, its charts or its release pipeline.

| Item | Rules | Effort | Next steps |
|---|---:|---|---|
| Hide nginx version and internal paths in error responses | 1 | Hours | Check the headers and error pages the gateway actually returns. Turn off server tokens and use generic error pages where anything leaks. |
| HTTP/2 downgrade handling at the gateway | 1 | Hours | Confirm whether HTTP/2 requests are downgraded to HTTP/1.1. If they are and that is needed, test that malformed requests are rejected and record the result as a CAT III disposition. |
| PostgreSQL per-role connection limits | 1 | Hours | Agree a connection limit for admin, service and user roles. Set it on the roles and keep the approved numbers with the config. |
| Show last successful login date and time | 1 | 1 day | Add the previous login timestamp to the Horizon UI (or the UDS login flow) using existing login events. Test that it shows the prior login, not the current one. |
| NATS authentication crypto module | 1 | 1–2 days | Trace which library signs NATS auth tokens. Either move signing onto Node's validated crypto provider or write up an accepted tailoring with the evidence. |
| FIPS-validated signing and hashing in the release pipeline | 2 | 1–2 days | Confirm which crypto module Witness and the Python/OpenSSL hashing steps actually run in. Pin an approved-mode module or an approved remote signer and keep the build provenance. |
| PII processing tags on data | 2 | 2–3 days | Confirm with the data owner which fields are PII and what processing is authorized. Reuse existing schema metadata or tags to carry that, and test it survives ingestion and query paths. |
| Secrets delivered as files, not environment variables | 2 | 2–4 days | Move credential-bearing env vars and the SeaweedFS s3.json ConfigMap to mounted Secrets or files. Check other customers' delivery requirements first so the shared defaults do not break them. |
| Session termination and re-authentication | 6 | 3–5 days | Define when users must re-authenticate (role change, privilege escalation). Make account deletion and logout revoke live sessions, API tokens and NATS connections, and clear browser credentials on close. Test each path end to end. |
| Application audit events with actor, target and outcome | 33 | 1–2 weeks | Agree the list of auditable operations (privileged actions, data access and change, permission grants, denied attempts). Map each to records that already exist, add the missing ones, and forward them through the existing log pipeline. |

## 2. Platform and deployment configuration

Settings Gallatin owns in UDS Core, Keycloak, Postgres, monitoring and the deployment profile. No Horizon code.

| Item | Rules | Effort | Next steps |
|---|---:|---|---|
| DoD notice and consent banner | 6 | Hours | Enable the Keycloak terms-and-conditions flag in the Core override and apply it to the existing realm. Verify the banner shows before every interactive login. |
| 35-day inactive account disable | 6 | Hours | Set the 35-day inactivity value in the Core override and enable the disable-inactive-users workflow on the existing realm. Document any exempt service or emergency accounts. |
| Concurrent session limit and 8-hour absolute session cap | 4 | Hours | Get security to approve one concurrent session per user. Set max sessions per user and an 8-hour max lifespan in the realm, and confirm the realm enforces them. |
| Registry image cleanup after upgrades | 1 | Hours | Add the existing Zarf registry prune step to the post-upgrade runbook. Keep approved rollback images. |
| CAC/PIV required login path | 2 | 1 day | Confirm which users must use card login. Keep X509 enabled, disable password and social flows for that scope, and keep an approved emergency path. Test that card is actually required. |
| Password policy: denylist, minimum age, character change | 17 | 1–2 days | Confirm whether any humans still log in with passwords. If so, mount a maintained password denylist and add it to the realm policy. Minimum age and 8-character-change have no Core flag, so pick an extension or write the tailoring. |
| Registry transport over TLS 1.2+ | 1 | 1–2 days | Decide between Zarf proxy mode and an external TLS registry for MPN. The default HTTP NodePort path does not pass. Plan the migration if the cluster is already initialized. |
| Central log integrity (hashing or signing) | 1 | 1–2 days | Identify who owns the central log store on MPN. Turn on hashing or signing of retained logs there, or document an accepted equivalent. |
| Automated response to intrusion detection events | 1 | 1–2 days | Route Falco alerts to Alertmanager with named receivers. Agree which detections trigger which responses before enabling any automatic lockout. |
| Recurring vulnerability scans of deployed images | 1 | 1–2 days | Set up scheduled scans of the running image inventory, not just build-time scans. Keep dated results and link them to the existing defect process. |
| PKI trust: local CRL cache, approved CAs, certificate class | 7 | 2–3 days | Enable CRL checking in Keycloak with mounted CRL files and a refresh schedule. Confirm the approved CA list and certificate class for MPN and test revoked and stale-CRL behavior while disconnected. |
| Encrypted backup and restore of application data | 4 | 2–4 days | Find out what backup service MPN provides and who runs it. Cover Horizon's Postgres and object storage with encrypted backups, run a restore test, and keep the record. |
| MPN network flow policy and local model service | 2 | 3–5 days | Define which destinations and ports are allowed and which local inference service will be used. Encode that in UDS Package network policies and test allowed versus blocked flows. |
| Security alert routing (account events, audit capacity, audit failures, tampering) | 33 | 3–5 days | Name the SA and ISSO recipients. Configure Alertmanager routes and rules for account create/modify/disable/remove/enable, 75 percent audit storage, audit pipeline failures and audit tampering. Fire a test for each and keep the evidence. |
| PostgreSQL audit configuration (pgAudit) | 19 | 1 week | Turn on connection, disconnection, privileged, DDL, role and direct-access logging with session and user context. Review the volume and sensitive-data exposure, then test a representative success and failure for each event type. |

## 3. Documentation, procedures and applicability decisions

Written justifications, approvals and mission decisions. No engineering change unless a decision turns one on.

| Item | Rules | Effort | Next steps |
|---|---:|---|---|
| Accept the drafted N/A justifications | 73 | 1–2 days | Review the drafted justifications (SOAP/SAML, 802.1x, temporary accounts, remote maintenance, local console login, DB password rules for service accounts, and similar). Accept, edit or reject each and record the decision. |
| Quarterly access review of the Horizon repositories | 1 | Hours | Find the most recent access review. If none is recent, have the owner review repo access, record decisions, and set the next date. |
| ISSO audit review cadence | 1 | Hours | Confirm who reviews audit trails on MPN and how often. Record the first review and the next due date. |
| Approved account unlock procedure | 1 | Hours | Finalize the identity-verification and unlock procedure and get ISSO/ISSM sign-off. |
| Annual secure-development training records | 1 | Hours | Map existing training to each engineering role and confirm dated completions. Note any gaps. |
| Security classification guide | 1 | Hours of ours, external wait | Ask the mission classification authority for the guide covering Horizon data elements. Record the reference once received. |
| PPSM submission and registration | 2 | 1 day, external wait | Reconcile the existing interface table against the deployed profile and submit it to the PPSM authority. Keep the acceptance record. |
| Data marking and labeling policy | 1 | 1 day | Once the classification guide exists, check that screens, reports and exports carry the required markings and document any manual procedure. |
| Vulnerability and fuzz testing coverage | 2 | 1–2 days | Document the active scanning and fuzz testing already performed, confirm it covers the web/API surface, and track findings older than 21 business days. |
| Compliance package documents | 7 | 2–4 days | Write the data protection requirements, contingency plan, decommissioning notice procedure, and the per-component hardening baseline rollups. Get mission owner confirmation where needed. |
| NSA-approved cryptography for classified data | 4 | 2–3 days to decide | Confirm the data classification and where the MPN/Gallatin crypto boundary sits. Map existing validated modules and inherited protection to each rule and record what, if anything, is left. |
| Three mission applicability decisions: DoW DMZ, MAC I, DB encryption | 3 | Hours to decide, large if yes | Get a written answer from the mission owner on each. DMZ yes means tiered network separation. MAC I yes means an HA profile. Classified DB yes means selecting an NSA-approved storage or network protection. A no on each is an accepted N/A. |
