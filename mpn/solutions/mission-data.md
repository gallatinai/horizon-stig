# Mission classification and PII processing

| STIG/SRG rule | Requirement | Current status |
|---|---|---|
| [V-222664 / APSC-DV-003290](../review/U_ASD_V6R5_STIG.md) | If the application contains classified data, a Security Classification Guide must exist containing data elements and their classification. | Unclear |
| [V-265634 / APSC-DV-002010](../review/U_ASD_V6R5_STIG.md) | The application must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Unclear |
| [V-233211 / SRG-APP-000416-CTR-001015](../review/U_Container_Platform_V2R5_SRG.md) | The container platform must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Unclear |
| [V-240925 / SRG-APP-000416-AS-000140](../review/U_Application_Server_V4R6_SRG.md) | The application server must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Unclear |
| [V-233495 / SRG-APP-000416-DB-000380](../review/U_Database_V4R6_SRG.md) | The DBMS must use NSA-approved cryptography to protect classified information in accordance with the data owner's requirements. | Unclear |
| [V-239371 / SRG-APP-000416-WSR-000118](../review/U_Web_Server_V4R5_SRG.md) | The web server must implement required cryptographic protections using cryptographic modules complying with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance when encrypting data that must be compartmentalized. | Unclear |
| [V-278962 / SRG-APP-001045-AS-000325](../review/U_Application_Server_V4R6_SRG.md) | The application server must attach data tags containing organization-defined authorized processing to organization-defined elements of personally identifiable information. | Needs work |
| [V-278963 / SRG-APP-001050-AS-000326](../review/U_Application_Server_V4R6_SRG.md) | The application server must attach data tags containing organization-defined processing purposes to organization-defined elements of personally identifiable information. | Needs work |

### Mission data and protection mapping

Prepare one matrix rather than separate classified-crypto changes for each server benchmark. Gallatin owns its UDS configuration on MPN; do not inherit the separate DU-managed IL5/IL6 service package by name.

| Data element family | Existing source association | Mission-owner fields to complete |
|---|---|---|
| Account identity: email, names, username, subject | Users schema; tenant and role context | PII determination, authorized processing, purpose, recipients, retention, controlling policy |
| Mission planning records | Tenant/domain authorization | Governing program SCG/paragraph, classification, caveats/REL TO, aggregation rules |
| Uploaded files, chunks and ingestion jobs | Classification field and tags | Source marking, allowed processing, purpose, derivative marking, permitted inference boundary |
| Assertions, embeddings and retrieved context | Classification/tenant metadata | Derivative/aggregation rule, retrieval/export permission and recipients |
| Generated artifacts and exports | Application content and delivery boundary | Required markings, recipients, export policy and allowed navigation/delivery |
| Audit logs, database/object backups and temporary files | Producing service/storage association | Inherited sensitivity, minimum necessary content, retention and protection boundary |

Record the governing guide identifier/version, original authority reference, element/paragraph mapping, reasons/declassification/handling reference, scope/caveats, owner and decision date. Use the existing higher-level program SCG where it covers these elements. This is a draft mapping for the mission owner's completion, not an approved classification guide; do not put sensitive guide contents or decisions in a public repo.

For unclassified scope, record the mission restriction and conditional N/A for classified-only checks. For classified scope, identify whether each data/path is already within an approved MPN cryptographic protection boundary and attach its authority/module/configuration evidence. Map at-rest, backup and network crossings separately. Use the exact ASD SAMI/non-SAMI distinction where applicable. NSA's CSfC guidance treats approved protection as a configured system solution; FIPS container names, modern TLS or a CNSA cipher list alone do not establish that solution. Partner/national-authority constraints must be part of the same map. Do not start a new CSfC registration or add Type1/app-local encryption unless the actual mission protection gap calls for it. [NSA solution guidance](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/faq/), [registration requirements](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/solution-registration/), [capability packages](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Capability-Packages/).

### PII processing metadata

Use a versioned profile such as `mission-account-identity/v1`, with the data owner approving scope and values. Suggested draft field associations are email/subject/name → account administration and authorized identity display; the authorized processing and purpose wording must be approved, not inferred as a legal basis. Document uploads require a separate mission-document profile if they contain PII. Avoid tagging all mission records as PII by default.

Reuse existing `files.tags` and downstream metadata for document-level attributes. Proposed keys are `privacy.profile`, `privacy.authorized_processing`, `privacy.processing_purpose` and `privacy.policy_ref`; they are proposed labels, not a current configured behavior. Keep field-level account associations in versioned API/schema metadata tied to the actual identity fields. If the required interpretation demands field-attached machine-readable tags, add that narrow mapping at the schema/API boundary. Validate required presence, allowed values, propagation to chunks/exports and preservation across updates; prevent ordinary callers from stripping required policy labels. General-purpose tags already exist, so a new database-wide tagging subsystem is not the first step.

Acceptance artifacts are the approved PII element/purpose profile and an example source-derived metadata/export record showing the approved associations. Security classification and tenant labels remain separate from processing purpose.

## Source references

- [re-mission-classification-model](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/packages/database/typescript/src/schema/schema.ts)
- [solution-asd-scg-check](https://github.com/gallatinai/horizon-stig/blob/main/mpn/benchmarks/U_ASD_V6R5_STIG/benchmark.xml)
- [re-docs-mpn-decision-boundary](https://drive.google.com/file/d/1p5zQe7lko71bWNfBd2B6clzJK52Rl0U5/view)
- [re-docs-mpn-scope-not-unclassified](https://grid-gallatin-ai.enterprise.slack.com/archives/C0AL2QNMGG3/p1793201707357709)
- [re-mission-nsa-system-solutions](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/faq/)
- [re-mission-nsa-registration](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/solution-registration/)
- [re-mission-nsa-cp](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Capability-Packages/)
- [re-mission-user-fields](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/apps/api/src/api/users/users.schema.ts)
- [re-mission-upload-tags](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/apps/api/src/api/files/files.schema.ts)
- [re-mission-ingestion-tags](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/workers/artifact-ingestion/artifact_ingestion/processor.py)
- [re-docs-classification-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-CUI-data-classification.md)
