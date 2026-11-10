# Improvement priorities

Gallatin operates Horizon and UDS Core on MPN. Use the pinned UDS Core source and deployment configuration to establish platform controls; Gallatin owns the configuration changes below.

1. **Audit coverage and alerting:** add missing actor/target/outcome records for domain access, denied operations and direct database activity. Configure targeted pgAudit/native logging, central log integrity, retention and named security alert routes. Reuse UDS identity events, existing role-change audit and Vector/Loki collection.
2. **Identity and sessions:** configure UDS account inactivity, session limits/lifetimes, notice/consent, password policy, required-card policy, CRL caching and notifications. Address outstanding-token termination, browser-close credential state and fresh authentication on privilege changes through the existing provider/API integration.
3. **Secrets:** replace secret environment variables and SeaweedFS credential ConfigMap placement with protected file/Secret delivery.
4. **Data and network profile:** configure database/data backup and restore, choose the MPN local model service and restrict network destinations to the required flows.
5. **Crypto:** replace or obtain accepted tailoring for NATS authentication's pure-JavaScript signatures outside Node's validated provider. Select approved crypto providers for release signing/hashing. Keep the existing validated OIDC/mesh mechanisms.
6. **Assessment and documentation:** complete contract-specific data markings, contingency and retirement procedures, targeted security-assessment coverage, nginx version hiding and HTTP protocol tailoring.

[UDS configuration actions](UDS-CONFIGURATION.md) identify the Core settings Gallatin owns. [Workstreams](review/workstreams.md) list affected rules and next actions. [Open decisions](review/remaining-evidence.md) identify infrastructure selections, mission policy and approval records that still need resolution. Each [rule list](../README.md) includes the current status, justification and source evidence.

Allow **15–30 engineer-days, approximately 2–4 elapsed weeks with two engineers**. The estimate depends on mission decisions and accepted control tailoring. Rough allocation: 4–10 days for Horizon audit/session/secret work, 3–8 for UDS/database/release configuration and crypto integration, and 5–10 for documentation and targeted assessment. These ranges overlap. MPN coordination and assessor turnaround add elapsed time.

John should review the needs-work and unknown recommendations, plus proposed N/A justifications, before final component CKLB acceptance.
