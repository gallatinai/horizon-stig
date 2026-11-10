# Mission classification and PII processing

| STIG/SRG rule | Requirement | Current status |
|---|---|---|
| [V-222664 / APSC-DV-003290](../review/U_ASD_V6R5_STIG.md) | If the application contains classified data, a Security Classification Guide must exist containing data elements and their classification. | Needs work |
| [V-265634 / APSC-DV-002010](../review/U_ASD_V6R5_STIG.md) | The application must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Needs work |
| [V-233211 / SRG-APP-000416-CTR-001015](../review/U_Container_Platform_V2R5_SRG.md) | The container platform must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Needs work |
| [V-240925 / SRG-APP-000416-AS-000140](../review/U_Application_Server_V4R6_SRG.md) | The application server must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. | Needs work |
| [V-233495 / SRG-APP-000416-DB-000380](../review/U_Database_V4R6_SRG.md) | The DBMS must use NSA-approved cryptography to protect classified information in accordance with the data owner's requirements. | Unclear |
| [V-239371 / SRG-APP-000416-WSR-000118](../review/U_Web_Server_V4R5_SRG.md) | The web server must implement required cryptographic protections using cryptographic modules complying with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance when encrypting data that must be compartmentalized. | Needs work |
| [V-278962 / SRG-APP-001045-AS-000325](../review/U_Application_Server_V4R6_SRG.md) | The application server must attach data tags containing organization-defined authorized processing to organization-defined elements of personally identifiable information. | Needs work |
| [V-278963 / SRG-APP-001050-AS-000326](../review/U_Application_Server_V4R6_SRG.md) | The application server must attach data tags containing organization-defined processing purposes to organization-defined elements of personally identifiable information. | Needs work |

## Classified encryption

MPN will process classified data. The classified-encryption rules apply.

For each relevant component, identify the encryption implementation protecting its data, check whether it meets the rule's NSA-approved requirement, and configure missing protection. Record the product/module, approval reference and required settings. Reuse approved encryption already supplied by the host, storage or network; no duplicate application crypto is required.

For PostgreSQL V-233495, read the discussion as well as the title: it addresses DBMS compatibility with NSA-approved encryption devices. Identify the MPN encryption protecting PostgreSQL and confirm the database paths use it. Credit that protection rather than requiring a separate NSA certificate for the PostgreSQL container. CMVP5132 establishes its software module validation; it does not by itself answer the infrastructure-coverage check. See [the requirement interpretation](../NSA-CRYPTOGRAPHY.md).

The ASD V-265634 check has a specific non-SAMI/SAMI distinction: it permits NIST-certified cryptography for stored non-SAMI data as required by the owner and requires NSA-validated Type1 for stored SAMI. Use that wording when checking the implementation; do not impose Type1 on every component merely because the environment is classified.

## Classification guide

Use the existing program/mission classification guide if it covers Horizon's data elements, as V-222664 permits. Record its identifier and applicable sections. Extend the guide only for uncovered data; the guide requirement is separate from checking whether a cryptographic implementation is approved.

## PII processing metadata

Approve the permitted processing and purposes for the actual PII fields. Reuse document `files.tags` and propagated metadata for `privacy.profile`, `privacy.authorized_processing`, `privacy.processing_purpose` and `privacy.policy_ref`. Add only the missing schema/API associations for account identity fields. Validate presence, allowed values, propagation and protection against unauthorized tag removal.

Use the mission-data protection record template for the field/purpose associations and the governing guide references. A proposed tag profile is not an implemented control or an approved guide.


## Checked products and viable protection layers

[The component comparison](../NSA-COMPONENT-CHECK.md) identifies exact checked products, listed storage/network candidates and their evaluated-configuration restrictions. The available MPN sources do not select a qualifying layer. Retain the database and map or select the approved protection rather than inferring approval from a FIPS image label.


## Source references

- [re-mission-classification-model](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/packages/database/typescript/src/schema/schema.ts)
- [solution-asd-scg-check](https://github.com/gallatinai/horizon-stig/blob/main/mpn/benchmarks/U_ASD_V6R5_STIG/benchmark.xml)
- [re-mission-nsa-system-solutions](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/faq/)
- [re-mission-nsa-registration](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/solution-registration/)
- [re-mission-nsa-cp](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Capability-Packages/)
- [classified-crypto-definition](https://csrc.nist.gov/glossary/term/NSA_approved_cryptography)
- [db-nsa-rule-discussion](https://github.com/gallatinai/horizon-stig/blob/main/mpn/benchmarks/U_Database_V4R6_SRG/benchmark.xml)
- [postgres-delivered-crypto](https://github.com/gallatinai/horizon-stig/blob/main/mpn/evidence/database-image-provenance.json)
- [nsa-storage-current-list](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Components-List/)
- [nsa-network-msc-boundary](https://www.nsa.gov/Portals/75/documents/CSfC%20CP%20Updates%202026/(U)%20Multi-Site%20Connectivity%20Capability%20Package%20v1.3.0.pdf?ver=mJWYHsX8a0wSY6bOPdCrZA%3D%3D)
- [nsa-mpn-notional-abd](https://drive.google.com/file/d/1rOyMxUBWdnwfrpnv-gvCWyne0drA5iZ5/view)
- [nsa-mpn-release-contract-boundary](https://github.com/gallatinai/horizon-uds-bundle/actions/runs/42114745685)
- [re-mission-user-fields](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/apps/api/src/api/users/users.schema.ts)
- [re-mission-upload-tags](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/apps/api/src/api/files/files.schema.ts)
- [re-mission-ingestion-tags](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/workers/artifact-ingestion/artifact_ingestion/processor.py)
- [re-docs-classification-policy](https://github.com/gallatinai/gallatin-company-policies/blob/e5b6ec5a2862cc3880c2ccc011d57698f14611e9/POL-CUI-data-classification.md)
