# Account, audit, access and training procedures

| STIG/SRG rule | Requirement | Current status |
|---|---|---|
| [V-222412 / APSC-DV-000330](../review/U_ASD_V6R5_STIG.md) | Unnecessary application accounts must be disabled, or deleted. | Likely covered |
| [V-222433 / APSC-DV-000540](../review/U_ASD_V6R5_STIG.md) | The application administrator must follow an approved process to unlock locked user accounts. | Needs work |
| [V-222622 / APSC-DV-002910](../review/U_ASD_V6R5_STIG.md) | The ISSO must review audit trails periodically based on system documentation recommendations or immediately upon system security events. | Needs work |
| [V-222628 / APSC-DV-002980](../review/U_ASD_V6R5_STIG.md) | New IP addresses, data services, and associated ports used by the application must be submitted to the appropriate approving authority for the organization, which in turn will be submitted through the DoW Ports, Protocols, and Services Management (DoW PPSM) | Needs work |
| [V-222629 / APSC-DV-002990](../review/U_ASD_V6R5_STIG.md) | The application must be registered with the DoW Ports and Protocols Database. | Needs work |
| [V-222630 / APSC-DV-002995](../review/U_ASD_V6R5_STIG.md) | The Configuration Management (CM) repository must be properly patched and STIG compliant. | Likely covered |
| [V-222631 / APSC-DV-003000](../review/U_ASD_V6R5_STIG.md) | Access privileges to the Configuration Management (CM) repository must be reviewed every three months. | Needs work |
| [V-222673 / APSC-DV-003400](../review/U_ASD_V6R5_STIG.md) | The Program Manager must verify all levels of program management, designers, developers, and testers receive annual security training pertaining to their job function. | Needs work |

## Governance actions

Gallatin operates the Horizon/UDS deployment on MPN. These actions use the existing identity, logging, release and company-policy mechanisms. Prepared checklists are not claims that a review, training course or authorization has been completed.

| Rule | Suggested status | Action | Owner |
|---|---|---|---|
| V-222412 | Needs work | Gallatin SRE exports the scoped UDS/Horizon human-account list to a controlled record; the mission account owner marks each retained/removed with a business justification and date, and the authorized operator carries out approved removals. | Gallatin SRE operator and MPN mission account owner |
| V-222433 | Needs work | Adopt the prepared identity-verification, authorized-unlock and audit-record procedure for Gallatin-operated UDS; obtain named MPN ISSO/ISSM acceptance and retain its version. | Gallatin UDS identity administrator; MPN ISSO and ISSM |
| V-222622 | Needs work | Gallatin SRE and the designated security reviewer perform the prepared Loki/Grafana event review, disposition exceptions, record its date and set the next review due under the quarterly policy. | Gallatin SRE; designated MPN ISSO/security reviewer |
| V-222628 | Needs work | Ian/Gallatin SRE derives the external-enclave flow rows from the selected MPN overlay and existing System Impact Assessment; the security lead routes them to the MPN network/PPSM authority for CAL compliance review and approval. | Gallatin SRE/Ian; security lead; MPN network/PPSM approving authority |
| V-222629 | Needs work | The Gallatin security lead and MPN sponsor submit the approved Horizon MPN flow set through the applicable PPSM/eMASS process and record the resulting identifier or written registration exemption in the controlled authorization packet. | Gallatin security lead and MPN Government sponsor/PPSM authority |
| V-222630 | Likely covered | Record the managed-service responsibility boundary and current GitHub assurance-report references; review the actual repository controls and obtain acceptance of any applicable provider-side STIG tailoring in the development authorization packet. | Gallatin GitHub organization owner and security/compliance lead |
| V-222631 | Needs work | The GitHub organization owner and Horizon engineering owner certify the protected Nov10 entitlement snapshot, justify each privileged role, record approved changes and review again within three months. | GitHub organization owner; Horizon engineering owner; security reviewer |
| V-222673 | Needs work | Program management and security training owners add the prepared role-specific secure-SDLC module to ThreatSwitch, assign all application roles, record completion/assessment and refresh annually. | Program manager; security training owner/FSO; engineering managers |

The read-only GitHub entitlement snapshot is prepared; no account changes were made. Human rosters, report bodies and sensitive event details belong in controlled evidence storage. Only record identifiers, dates, summary disposition and links belong in the public tracker.

### V-222412

The product uses UDS identity and individual accounts; no additional account-discovery implementation is needed. Complete the mission human-account certification against the current approved personnel list. Required service accounts are excluded by the official check. This is a defined account-owner review action rather than an unresolved runtime behavior.

Cadence: Before mission account enablement, on joiner/mover/leaver events, and quarterly under the existing access-review policy.

1. Export only identities entitled to the Horizon MPN tenant, including inherited groups and privileged roles.
2. Separate human identities from necessary service identities.
3. Match each human to the approved mission roster and role; record retain/modify/remove, owner reason, review date and ticket.
4. Have the mission account owner certify decisions; an authorized operator executes approved changes and records completion.

Complete when: All in-scope human accounts have an accountable owner and certification; approved unnecessary-account removals are recorded.

### V-222433

UDS Keycloak already provides account lockout and administrator recovery, and corporate policy requires identity verification. Complete the short operational unlock procedure and its explicit ISSO/ISSM approval; do not build a second unlock API.

Cadence: For every account-unlock event; reapprove on a material identity/recovery change.

1. Open an incident/help-desk request recording realm and account identifier without passwords or recovery secrets.
2. Verify requester identity using the approved independent channel or sponsor/CAC/PIV process; never rely solely on the locked account session.
3. Confirm employment/mission entitlement and investigate suspicious lockouts before recovery.
4. An authorized UDS identity administrator resets the brute-force lock using native Keycloak administration; require credential reset or session revocation when compromise is suspected.
5. Retain request, verification method, administrator, timestamp, reason and native administration-event reference; close the request.

Complete when: ISSO and ISSM accept the versioned procedure and the operator can produce a complete recovery record when an unlock occurs.

### V-222622

The review tooling and quarterly procedure exist. Establish and record the first scoped MPN audit review, then follow the same cadence and event-driven reviews. A Grafana dashboard is an enabling mechanism, not a dated security review.

Cadence: Quarterly under the existing policy and immediately upon identified security events, as the official check requires.

1. Define review window, deployed release and included audit sources; verify the required sources delivered records throughout the window.
2. Review denied authentication and authorization, account/role/realm changes, privileged actions, deployment/configuration changes, suspicious data access and audit interruption/tampering alerts.
3. For each exception, record query/time range, event references, triage, disposition and linked incident or remediation ticket.
4. Reviewer records date, conclusions, source omissions and next due date; retain a restricted review record with traceable evidence.

Complete when: A dated review is retained and no review interval exceeds the approved policy; security-event-triggered reviews have tickets.

### V-222628

Delivered configuration and existing System Impact Assessment identify the network flows. Complete the MPN-specific external-enclave ports/protocols classification and authority submission; reuse the flow inventory and default-deny policy rather than redesign networking or register every pod port as external.

Cadence: Before production authorization and before adding/changing an external-enclave service or port.

1. Use the current MPN architecture boundary and deployment configuration, not the separate DU or III Corps IATT inventory.
2. Separate browser/gateway, identity, permitted mission-data interfaces and required platform service flows from purely internal pod/service flows.
3. For each external flow, record direction, protocol/port, endpoints, service function, release/profile, encryption/authentication and the PPS CAL disposition.
4. Have the MPN network authority confirm the applicable boundary and accepted CAL entries; record approval or exact conditions.
5. Keep approved rows synchronized with the generated UDS Package/network policies on each affected release.

Complete when: External-enclave flows have an accepted MPN CAL mapping and approval record; configuration matches that mapping.

### V-222629

A source-controlled flow table cannot itself create the production registration required by this check. Complete a concrete MPN registration action using the same approved flow set; retain an authority-issued registration identifier or explicit exemption, without treating a draft from another program as completion.

Cadence: Before production authorization and when a registered service/port/release boundary materially changes.

1. Identify the MPN system/authorization record and responsible PPSM registration authority with the Government sponsor.
2. Submit the approved external-flow inventory from V-222628 using the required authority template.
3. Resolve required endpoint/system identifier fields and retain submission receipt and authority decision.
4. Record registration ID, date, scope/release and approved flows, or the authority-issued exemption and rationale.

Complete when: The production MPN authorization packet contains a valid registration or written authority determination that registration is not required.

### V-222630

Horizon uses provider-operated GitHub Enterprise Cloud, with enforced repository reviews, CodeQL and change controls. GitHub manages the hosting software; applying a customer Git-server/OS patch checklist to this SaaS instance would create a fictitious server obligation. Record scoped provider inheritance using GitHub assurance reports and retain Gallatin responsibility for organization/repository settings. SOC/ISO reports support that mapping but are not called a DISA STIG certificate.

Cadence: On adoption, material GitHub hosting/enterprise-policy change, and annual provider-assurance refresh as a proposed operating cadence.

1. Document provider-operated GitHub.com Enterprise Cloud as the CM service; distinguish it from self-hosted Enterprise Server.
2. Organization owner obtains current SOC2/ISO/CSA and relevant continuity/security reports through organization Settings → Security → Compliance.
3. Map provider hosting/patching duties to GitHub; map repository access, rulesets, review gates, security scanning, integrations and audit retention to Gallatin.
4. Retain report dates, boundary, repository settings snapshot and security acceptance of the tailored provider-side evidence; do not publish licensed reports.

Complete when: Provider inheritance and customer controls are recorded and accepted for the development boundary; no unsupported claim of a GitHub STIG certificate is made.

### V-222631

Use a read-only effective-entitlement snapshot of the Horizon repository for the quarterly access-certification workflow. Record accountable owner decisions against the full effective grant list.

Cadence: At least every three months; also on departures and material role changes.

1. Compare effective memberships, team/default grants, outside collaborators, invitations and installed automation permissions with active engineering responsibilities.
2. Each human role receives retain/change/remove with owner rationale; individually justify admin or bypass authority.
3. Review relevant GitHub membership/permission-change audit history since the preceding review.
4. Owner certifies the decisions and an authorized administrator executes approved changes separately; retain the completed record and next due date.

Complete when: Every current grant is certified and approved changes are complete, with a dated retained record no more than three months old.

### V-222673

The corporate annual training platform and general awareness courses exist. Assign and record role-appropriate secure-development instruction for every application manager, designer, developer and tester; general awareness or CAC/SIPR training alone does not meet this explicit SDLC requirement.

Cadence: At least annually for all relevant application roles; include new staff before independent security-sensitive duties and keep the existing hire-training deadline.

1. Map current personnel to one or more application roles without publishing the roster.
2. Assign the approved secure-SDLC course plus applicable role modules in ThreatSwitch.
3. Use attendance plus completion assessment or equivalent recorded demonstration; capture date and course/version.
4. Managers resolve missing completion and the program manager verifies full role coverage, then schedules annual refresh.

Complete when: All application roles have annual role-relevant secure-development completion records, distinct from generic security-awareness assignments.

## Source references

- [solution-governance-account-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-AC-access-control.md)
- [re-governance-delivered-contract](https://github.com/gallatinai/horizon-uds-bundle/actions/runs/42114745685)
- [solution-governance-recovery-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-IA-identification-and-authentication.md)
- [core-keycloak](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/keycloak/chart/values.yaml)
- [core-id-realm](https://github.com/defenseunicorns/uds-identity-config/blob/74480722e1cc8405b5e9b65ac7d7086ab7f4056d/src/realm.json5)
- [solution-governance-audit-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-AU-audit-and-accountability.md)
- [core-vector](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/vector/values/values.yaml)
- [core-loki](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/loki/chart/templates/uds-package.yaml)
- [core-grafana](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/grafana/values/values.yaml)
- [solution-governance-mpn-scope](https://docs.google.com/document/d/1RzBd9YPzJSYk8LDI126LbvRBiaF3uJjfN4T5V8-0Pbw/edit)
- [solution-governance-ppsm-routing](https://grid-gallatin-ai.enterprise.slack.com/archives/C0AL2QNMGG3/p1793127354624349)
- [core-network](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/pepr/operator/controllers/network/defaults/default-deny-all.ts)
- [core-gateway](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/istio/charts/uds-istio-config/templates/gateway.yaml)
- [solution-governance-managed-service](https://docs.github.com/en/enterprise-cloud@latest/admin/overview/about-github-enterprise-cloud)
- [solution-governance-provider-assurance](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/accessing-compliance-reports-for-your-organization)
- [re-governance-rules](https://github.com/gallatinai/horizon/rules/11323811)
- [re-governance-scm](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/docs/rfcs/RFC-057-release-management-and-change-tracking.md)
- [solution-governance-access-snapshot](https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#list-repository-collaborators)
- [solution-governance-github-audit-log](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
- [solution-governance-training-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-AT-awareness-and-training.md)
