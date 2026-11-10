# Remaining evidence decisions

Each decision includes the exact STIG/SRG requirement and official check that establish the evidence needed.

[Implementation plans and operating procedures](../EVIDENCE-ACTIONS.md) cover configuration and record-completion actions.

## V-222620 — APSC-DV-002890

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** Application web servers must be on a separate network segment from the application and database servers if it is a tiered application operating in the DoW DMZ.

**Decision / action needed:** Record the DoW DMZ applicability decision. If true, implement the documented three-tier policy and approved diagram; if false, record accepted N/A. Gallatin owns Core network policy configuration.

**Reason:** Applicability depends on whether the mission hosts this tiered application in the DoW DMZ. Existing gateway routing and broad intra-namespace allowances do not establish separation between web, application and database tiers. The conditional solution removes broad allowances and places the tiers in separate default-deny namespaces/Packages with explicit peer/port rules and no web-to-database path. If the system is outside the DoW DMZ, the exact check permits N/A.

<details>
<summary>Official check — SV-222620r1263602_rule</summary>

> Review the application documentation.
>
> Review the application data protection requirements and identify if all data types hosted on server are identical.
>
> Review the network diagram and identify web servers/web services, web application servers, and database servers.
>
> If the application is not hosted in the DoW DMZ, this requirement is not applicable.
>
> Verify the application web servers are separated from the application and database servers if the application is a tiered design as per DoW DMZ STIG requirements.
>
> If the application is tiered and the network infrastructure hosting the application is not configured to provide separation and security access controls between the tiered layers in accordance with DoW DMZ requirements, this is a finding.

</details>

## V-222664 — APSC-DV-003290

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** If the application contains classified data, a Security Classification Guide must exist containing data elements and their classification.

**Decision / action needed:** Draft the data-element-to-existing-SCG matrix below; have the Government mission/security owner supply the controlling guide identifier/version/paragraphs and OCA approval reference. Mark nonclassified branch N/A only when that mission restriction is confirmed. Do not put a classified guide or its contents in the public tracker.

**Reason:** The product has classification metadata, but no identified governing program SCG/data-element mapping establishes the mission classification. The exact check permits an existing higher-level guide; a new Gallatin-authored classification authority or an unclassified assumption would be unsupported. This is one documentation/mission-owner decision, not an uninvestigated runtime check.

<details>
<summary>Official check — SV-222664r1051277_rule</summary>

> If the application does not process classified information, this check is not applicable.
>
> The application may already be covered by a higher level program or other classification guide. If the classification guide is not written specifically to the application, the sensitive application data should be reviewed to determine whether it is contained in the classification guide.
>
> DOD 5200.01 Volume 1 identifies requirements for security classification and declassification guides.
>
> https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodm/520001m_vol1.pdf
>
> Security classification guides must provide the following information:
>
> Identify specific items, elements, or categories of information to be protected.
>
> State the specific classification to be assigned to each item or element of information and, when useful, specify items of information that are unclassified.
>
> Provide declassification instructions for each item or element of information, including the applicable exemption category for information exempted from automatic declassification.
>
> State a concise reason for classification for each item, element, or category of information that, at a minimum, cites the applicable classification categories in Section 1.5 of E.O. 12958.
>
> Identify any special handling caveats that apply to items, elements, or categories of information.
>
> Identify, by name or personal identifier and position title, the original classification authority approving the guide and the date of that approval.
>
> Provide a point of contact for questions about the guide and suggestions for improvement.
>
> For information exempted from automatic declassification because its disclosure would reveal foreign government information or violate a statute, treaty, or international agreement, the security classification guide will identify the government or specify the applicable statute, treaty, or international agreement, as appropriate.
>
> If the security classification guide does not exist, or does not contain application data elements and their classification, this is a finding.

</details>

## V-265634 — APSC-DV-002010

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Decision / action needed:** Prepare one mission data/protection matrix covering identities, mission records, source files/chunks, derived assertions/embeddings, generated artifacts and backups/logs. Map each to the controlling program SCG or handling authority, permitted recipients/REL TO rules, SAMI applicability, at-rest and in-transit protection and the responsible implemented boundary. Have the mission owner select the actual classification/handling branch. For classified data, attach the existing approved MPN boundary protection evidence and map every data path; only engineer a missing boundary after that mapping. For unclassified scope, record the supported classified-rule N/A. Do not impose independent app-level CNSA/Type1 TLS merely because the benchmark names the application.

**Reason:** Delivered FIPS mechanisms can protect normal application hops, but the source/package does not select a mission-approved classified-data cryptographic boundary. The required outcome may be supplied by MPN network/storage protection around Gallatin-managed UDS; it need not be reimplemented independently by every named service. Approval/classification and the actual protected storage/path map remain one shared mission input, not proof of a missing crypto feature. The exact ASD check distinguishes non-SAMI stored data and SAMI Type1 requirements; do not replace that decision with a blanket FIPS-or-CNSA assertion.

<details>
<summary>Official check — SV-265634r1117183_rule</summary>

> Review the application documentation, system security plan and interview the application administrator to determine if the application processes classified data.
>
> If the application does not process classified data, this requirement is not applicable.
>
> Identify the data classifications and the cryptographic protections established to protect the application data.
>
> Verify the application is configured to utilize the appropriate encryption based upon data classification, cryptographic tasks that need to be performed (information protection, hashing, signing) and information protection requirements.
>
> NIST-certified cryptography must be used to store classified non-Sources and Methods Intelligence (SAMI) information if required by the information owner.
>
> NSA-validated type-1 encryption must be used for all SAMI data stored in the enclave.
>
> If the application is not configured to utilize the NSA-approved cryptographic modules in accordance with data protection requirements specified in the security plan, this is a finding.

</details>

## V-233211 — SRG-APP-000416-CTR-001015

**Benchmark:** Container Platform Security Requirements Guide — Container Platform V2R5 SRG ([official XCCDF](../benchmarks/U_Container_Platform_V2R5_SRG/benchmark.xml)).

**Requirement:** The container platform must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Decision / action needed:** Prepare one mission data/protection matrix covering identities, mission records, source files/chunks, derived assertions/embeddings, generated artifacts and backups/logs. Map each to the controlling program SCG or handling authority, permitted recipients/REL TO rules, SAMI applicability, at-rest and in-transit protection and the responsible implemented boundary. Have the mission owner select the actual classification/handling branch. For classified data, attach the existing approved MPN boundary protection evidence and map every data path; only engineer a missing boundary after that mapping. For unclassified scope, record the supported classified-rule N/A. Do not impose independent app-level CNSA/Type1 TLS merely because the benchmark names the application.

**Reason:** Delivered FIPS mechanisms can protect normal application hops, but the source/package does not select a mission-approved classified-data cryptographic boundary. The required outcome may be supplied by MPN network/storage protection around Gallatin-managed UDS; it need not be reimplemented independently by every named service. Approval/classification and the actual protected storage/path map remain one shared mission input, not proof of a missing crypto feature.

<details>
<summary>Official check — SV-233211r961863_rule</summary>

> Review documentation to verify that the container platform is using NSA-approved cryptography to protect classified data and applications.
>
> If the container platform is not using NSA-approved cryptography for classified data and applications, this is a finding.

</details>

## V-239371 — SRG-APP-000416-WSR-000118

**Benchmark:** Web Server Security Requirements Guide — Web Server V4R5 SRG ([official XCCDF](../benchmarks/U_Web_Server_V4R5_SRG/benchmark.xml)).

**Requirement:** The web server must implement required cryptographic protections using cryptographic modules complying with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance when encrypting data that must be compartmentalized.

**Decision / action needed:** Add web requests/responses, generated artifacts and relevant compartment/releasability labels to the same mission protection matrix. Reuse the existing gateway/mesh module evidence when it meets the selected policy; add storage/enclave protection only for an actual uncovered requirement. Record the accepted existing-boundary justification.

**Reason:** This rule includes sensitive/need-to-know compartments, so a classified-only N/A is too narrow. Delivered FIPS gateway/mesh protection can supply the cryptographic mechanism for ordinary sensitive web data; the missing item is the compartment/data-owner protection profile and mapping to that existing boundary. A new nginx encryption layer is not justified by this evidence.

<details>
<summary>Official check — SV-239371r1117186_rule</summary>

> Review policy documents to identify data that is compartmentalized (i.e. classified, sensitive, need-to-know, etc.) and requires cryptographic protection.
>
> Review the web server documentation and deployed configuration to identify the encryption modules utilized to protect the compartmentalized data.
>
> If the encryption modules used to protect the compartmentalized data are not compliant with the data, this is a finding.

</details>

## V-204814 — SRG-APP-000435-AS-000069

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server, when a MAC I system, must be in a high-availability (HA) cluster.

**Decision / action needed:** Record the single MAC I applicability decision. If true, implement the concrete HA profile; if false, record accepted N/A. Gallatin operates Core and owns the configuration.

**Reason:** Applicability still depends on the mission declaring MAC I; code cannot select that designation. The implementation is now defined: a MAC I profile needs multiple failure domains, at least two web/API replicas with disruption/placement controls, and HA stateful, storage and identity dependencies. Current source describes single-node PostgreSQL and does not declare a completed MAC I HA cluster. If MAC I applies, the specified profile needs implementation; otherwise the exact check permits N/A.

<details>
<summary>Official check — SV-204814r961620_rule</summary>

> If the application server is not a MAC I system, this requirement is NA.
>
> Review the application server documentation and configuration to determine if the application server is part of an HA cluster.
>
> If the application server is not part of an HA cluster, this is a finding.

</details>

## V-240925 — SRG-APP-000416-AS-000140

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Decision / action needed:** Prepare one mission data/protection matrix covering identities, mission records, source files/chunks, derived assertions/embeddings, generated artifacts and backups/logs. Map each to the controlling program SCG or handling authority, permitted recipients/REL TO rules, SAMI applicability, at-rest and in-transit protection and the responsible implemented boundary. Have the mission owner select the actual classification/handling branch. For classified data, attach the existing approved MPN boundary protection evidence and map every data path; only engineer a missing boundary after that mapping. For unclassified scope, record the supported classified-rule N/A. Do not impose independent app-level CNSA/Type1 TLS merely because the benchmark names the application.

**Reason:** Delivered FIPS mechanisms can protect normal application hops, but the source/package does not select a mission-approved classified-data cryptographic boundary. The required outcome may be supplied by MPN network/storage protection around Gallatin-managed UDS; it need not be reimplemented independently by every named service. Approval/classification and the actual protected storage/path map remain one shared mission input, not proof of a missing crypto feature.

<details>
<summary>Official check — SV-240925r1117186_rule</summary>

> Review application server documentation to verify that the application server is using NSA-approved cryptography to protect classified data and applications resident on the device.
>
> If the application server is not using NSA-approved cryptography for classified data and applications, this is a finding.

</details>

## V-233495 — SRG-APP-000416-DB-000380

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must use NSA-approved cryptography to protect classified information in accordance with the data owner's requirements.

**Decision / action needed:** Prepare one mission data/protection matrix covering identities, mission records, source files/chunks, derived assertions/embeddings, generated artifacts and backups/logs. Map each to the controlling program SCG or handling authority, permitted recipients/REL TO rules, SAMI applicability, at-rest and in-transit protection and the responsible implemented boundary. Have the mission owner select the actual classification/handling branch. For classified data, attach the existing approved MPN boundary protection evidence and map every data path; only engineer a missing boundary after that mapping. For unclassified scope, record the supported classified-rule N/A. Do not impose independent app-level CNSA/Type1 TLS merely because the benchmark names the application.

**Reason:** Delivered FIPS mechanisms can protect normal application hops, but the source/package does not select a mission-approved classified-data cryptographic boundary. The required outcome may be supplied by MPN network/storage protection around Gallatin-managed UDS; it need not be reimplemented independently by every named service. Approval/classification and the actual protected storage/path map remain one shared mission input, not proof of a missing crypto feature.

<details>
<summary>Official check — SV-233495r1117186_rule</summary>

> If the DBMS is deployed in an unclassified environment, this is not applicable (NA).
>
> If the DBMS is not configured to use NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards, this is a finding.

</details>
