# Remaining evidence decisions

Each decision includes the exact STIG/SRG requirement and official check that establish the evidence needed.

## V-222412 — APSC-DV-000330

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** Unnecessary application accounts must be disabled, or deleted.

**Decision / action needed:** Attach current MPN human-account certification or approved roster comparison; exclude necessary service identities.

**Reason:** Official check expressly excludes required service accounts and requires validation of the actual human account list. Code defines provisioning and permissions, but cannot identify which real mission personnel still require access. No current MPN user roster/certification was found; this is a specific external identity-ownership record, not a request to run an unexplained runtime test.

<details>
<summary>Official check — SV-222412r960774_rule</summary>

> Review the system documentation and identify any valid application accounts that are required in order for the application to operate. Accounts the application itself uses in order to function are not in scope for this requirement.
>
> Have the application administrator generate a list of all application users. This should include relevant user metadata such as phone numbers or department identifiers.
>
> Have the application administrator identify and validate all user accounts.
>
> If any accounts cannot be validated and are deemed to be unnecessary, this is a finding.

</details>

## V-222433 — APSC-DV-000540

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application administrator must follow an approved process to unlock locked user accounts.

**Decision / action needed:** Record ISSO/ISSM acceptance of the actual UDS/MPN account-unlock procedure; no separate Horizon unlock implementation is implied.

**Reason:** Identity-verified recovery administration is documented, and UDS provides administrator account controls. The official check specifically requires the unlock process to carry ISSO/ISSM approval. Corporate policy is still Draft / Effective TBD and no MPN-specific signed or otherwise recorded acceptance was found; source cannot confer that authority.

<details>
<summary>Official check — SV-222433r961368_rule</summary>

> Interview the application administrator and identify the approved process for unlocking user accounts.
>
> The process may involve a manual or automated reset after the locked out user has identified themselves using standard user identification processes outlined in the vulnerability discussion.
>
> If the admin does not unlock the account following the approved process, and if the process does not have documented ISSO and ISSM approvals, this is a finding.

</details>

## V-222587 — APSC-DV-002330

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must protect the confidentiality and integrity of stored information when required by DoW policy or the information owner.

**Decision / action needed:** Identify the MPN storage/backend/KMS configuration or accepted physical protection so source/configuration encryption can be assessed; no arbitrary app encryption implementation is proposed.

**Reason:** Reviewed actual release images/values define PostgreSQL/PVC and S3 data paths, but choose no MPN storage class/backend encryption/key policy. Mesh protection and FIPS-capable images do not encrypt an unspecified external volume/object-store automatically. This remaining boundary is an actual environment/service selection, not a request to observe code-defined behavior at runtime.

<details>
<summary>Official check — SV-222587r1263591_rule</summary>

> Review the application documentation and interview the application administrator.
>
> Identify the data processed by the application and the accompanying data protection requirements.
>
> Determine if the data owner has specified stored data protection requirements.
>
> Determine if the application is processing publicly releasable, CUI, or classified stored data.
>
> Determine if the application configuration information contains sensitive information.
>
> Access the data repository and have the application administrator, application developer, or designer identify the data integrity and confidentiality protections used to protect stored data.
>
> If the application processes classified data or the data owner has specified data protection requirements and the application administrator is unable to demonstrate how the data is protected, this is a finding.

</details>

## V-222588 — APSC-DV-002340

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must implement approved cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest on organization-defined information system components.

**Decision / action needed:** Identify the MPN storage/backend/KMS configuration or accepted physical protection so source/configuration encryption can be assessed; no arbitrary app encryption implementation is proposed.

**Reason:** Reviewed actual release images/values define PostgreSQL/PVC and S3 data paths, but choose no MPN storage class/backend encryption/key policy. Mesh protection and FIPS-capable images do not encrypt an unspecified external volume/object-store automatically. This remaining boundary is an actual environment/service selection, not a request to observe code-defined behavior at runtime.

<details>
<summary>Official check — SV-222588r1263593_rule</summary>

> Review the documentation and interview the application administrator.
>
> Identify the data processed by the application and the accompanying data protection requirements.
>
> Determine if the data owner has specified data protection encryption requirements regarding modification of data.
>
> Determine if the application is processing publicly releasable, CUI, or classified data.
>
> Determine if the application configuration information contains sensitive information.
>
> If the data is strictly publicly releasable information and system documentation specifies no data encryption is required for any hosted application data, this is not applicable.
>
> Access the data repository and have the application administrator identify the encryption protections that are utilized.
>
> If the application processes classified data or if the data owner has specified encryption requirements and the application administrator is unable to demonstrate how the data is encrypted, this is a finding.

</details>

## V-222589 — APSC-DV-002350

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must use appropriate cryptography in order to protect stored DoW information when required by the information owner or DoW policy.

**Decision / action needed:** Identify the MPN storage/backend/KMS configuration or accepted physical protection so source/configuration encryption can be assessed; no arbitrary app encryption implementation is proposed.

**Reason:** Reviewed actual release images/values define PostgreSQL/PVC and S3 data paths, but choose no MPN storage class/backend encryption/key policy. Mesh protection and FIPS-capable images do not encrypt an unspecified external volume/object-store automatically. This remaining boundary is an actual environment/service selection, not a request to observe code-defined behavior at runtime.

<details>
<summary>Official check — SV-222589r1263595_rule</summary>

> Review the application documentation and interview the application administrator.
>
> Identify the data processed by the application and the accompanying data protection requirements.
>
> Determine if the application is processing publicly releasable, SBU, CUI, or classified data.
>
> If the data is strictly publicly releasable information with no SBU, CUI, or classified and system documentation specifies no data encryption is required for any hosted application data, this requirement is not applicable.
>
> Have the application administrator identify the encryption protections that are utilized.
>
> Validate the application is using encryption protections that are commensurate with the data being protected.
>
> If the application is processing classified data, type 1, suite B cryptography, or hardware-based encryption solutions; meeting NSA encryption requirements for classified data processing and storage is required.
>
> If the application processes classified data or if the data owner has specified encryption requirements and the application administrator is unable to demonstrate the type of encryption used or if the application processes classified and does not use type 1, suite B, or NSA-approved hardware-based encryption, this is a finding.

</details>

## V-222595 — APSC-DV-002410

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The web service design must include redundancy mechanisms when used with high-availability systems.

**Decision / action needed:** Obtain the explicit mission classification/availability/network designation; assess the applicable product/platform control or submit supported N/A only after that condition is established.

**Reason:** The exact check depends on the actual mission high-availability designation, DMZ topology or classified-data boundary. Product code supports classification labels and connected documents discuss partner/IL6-equivalent delivery, so unclassified-only/private-only applicability cannot be inferred. The relevant mission/environment designation has not been selected in the delivered app package; this is a policy input, not an uninvestigated runtime behavior.

<details>
<summary>Official check — SV-222595r961155_rule</summary>

> Interview the application administrator and review the system documentation to determine if the application has been designated as a high availability system and if the application is designed to operate in a high availability environment.
>
> If the application has not been designated as a high availability system, this requirement is not applicable.
>
> Review the application architecture documentation and identify solutions that provide application DoS protections.
>
> Verify the application has been built to work in a clustered or otherwise high availability environment in accordance with documented availability requirements.
>
> This includes:
>
> - load balancers
> - redundant systems such as multiple web, application servers or DB servers
> - high bandwidth or redundant data circuits
> - multiple data centers (geographic dispersal)
> - server clusters
>
> If the application has been designated as high availability but the architecture is not built to high availability standards, this is a finding.

</details>

## V-222620 — APSC-DV-002890

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** Application web servers must be on a separate network segment from the application and database servers if it is a tiered application operating in the DoW DMZ.

**Decision / action needed:** Obtain the explicit mission classification/availability/network designation; assess the applicable product/platform control or submit supported N/A only after that condition is established.

**Reason:** The exact check depends on the actual mission high-availability designation, DMZ topology or classified-data boundary. Product code supports classification labels and connected documents discuss partner/IL6-equivalent delivery, so unclassified-only/private-only applicability cannot be inferred. The relevant mission/environment designation has not been selected in the delivered app package; this is a policy input, not an uninvestigated runtime behavior.

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

## V-222622 — APSC-DV-002910

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The ISSO must review audit trails periodically based on system documentation recommendations or immediately upon system security events.

**Decision / action needed:** Attach the latest MPN/UDS audit review result/date and confirm it satisfies the documented cadence.

**Reason:** A concrete quarterly audit-review policy and responsible security role were found, resolving the missing-procedure question. The exact check also asks when logs were last reviewed; no dated MPN review was found in source or connected evidence. Retain the required completed audit-review record.

<details>
<summary>Official check — SV-222622r961863_rule</summary>

> Interview the application representative and ask for the system documentation that states how often audit logs are reviewed. Also, determine when the audit logs were last reviewed.
>
> If the application representative cannot provide system documentation identifying how often the auditing logs are reviewed, or has not audited within the last time period stated in the system documentation, this is a finding.

</details>

## V-222628 — APSC-DV-002980

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** New IP addresses, data services, and associated ports used by the application must be submitted to the appropriate approving authority for the organization, which in turn will be submitted through the DoW Ports, Protocols, and Services Management (DoW PPSM)

**Decision / action needed:** Attach the approved external-enclave ports/protocols mapping; internal pod ports need not all be treated as external PPSM registrations.

**Reason:** Source identifies the actual service/gateway/mesh ports, so port discovery is not unfinished. The remaining official condition is external-enclave PPSM/CAL approval; the reviewed sources do not identify the MPN approving authority decision/current allowable-use record for those flows. Local product config cannot grant that approval.

<details>
<summary>Official check — SV-222628r1263608_rule</summary>

> All application ports, protocols, and services needed for application operation need to be in compliance with the DoW Ports and Protocols guidance.
>
> Check:
>
> http://iase.disa.mil/ppsm/Pages/index.aspx
>
> to verify the ports, protocols, and services are in compliance with the PPS CAL.
>
> Check all necessary ports and protocols needed for application operation (only those accessed from outside the local enclave) are checked against the DoW Ports and Protocols guidance to ensure compliance.
>
> Identify the ports needed for the application:
>
> - Look at System Security Plan/Accreditation documentation
> - Ask System Administrator
> - Go to Network Administrator
> - Go to Network Reviewer
> - If a network scan is available, use it
> - Use netstat/task manager
> - Check /etc./services
>
> If the application is not in compliance with DoW Ports and Protocols guidance, this is a finding.

</details>

## V-222629 — APSC-DV-002990

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must be registered with the DoW Ports and Protocols Database.

**Decision / action needed:** Attach the actual production PPSM record or registration exemption.

**Reason:** The rule tests actual production registration when required, not whether source can enumerate ports. No MPN PPSM registration identifier or authority-issued exemption was found. This is an external administrative record and can be resolved without a runtime check.

<details>
<summary>Official check — SV-222629r1263609_rule</summary>

> Verify registration of the application and ports in the Ports and Protocols Database for a production site.
>
> If the application requires registration, and is not registered or all ports used have not been identified in the database, this is a finding.

</details>

## V-222630 — APSC-DV-002995

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The Configuration Management (CM) repository must be properly patched and STIG compliant.

**Decision / action needed:** Attach accepted GitHub managed-service security/CM inheritance for the development boundary, or obtain scoped N/A for the site assessment.

**Reason:** GitHub is the managed source service and live ruleset proves repository controls; there is no customer-operated Git server in this source to patch. However the check also asks for repository-service platform authorization/STIG inheritance, and no applicable GitHub service compliance/accepted inheritance record was found. Do not remediate a nonexistent local CM server.

<details>
<summary>Official check — SV-222630r961863_rule</summary>

> Review the application system documentation and interview the application administrator.
>
> Identify if the STIG is being applied to application developers or organizations responsible for code management or who have and operate an application CM repository. If this is not the case, the requirement is not applicable.
>
> Review CM patch management processes and procedures.  Have the system and CM admins demonstrate their patch management processes and verify the system has the latest security patches applied.
>
> Review the ATO documentation and verify the system that operates the CM repository software has had all relevant STIGs applied.
>
> If CM repository is not at the latest security patch level and is not operating on a STIG compliant system, this is a finding.

</details>

## V-222631 — APSC-DV-003000

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** Access privileges to the Configuration Management (CM) repository must be reviewed every three months.

**Decision / action needed:** Attach a dated GitHub repository/organization entitlement review covering the assessed development team.

**Reason:** Corporate policy now supplies a quarterly access-review process, and source service has controlled membership/review gates. The exact check requires evidence the last repository access certification occurred within 3 months; no dated GitHub certification was found. Other-environment access reviews are not substituted.

<details>
<summary>Official check — SV-222631r961863_rule</summary>

> Review the application system documentation.
>
> Interview the application administrator.
>
> Identify if development of the application is done in house and if application configuration management repository exists.
>
> If application development is not done in house and if a code configuration management repository does not exist, the requirement is not applicable.
>
> Review CM management processes and procedures.
>
> Verify the CM repository access permissions are reviewed at least every three months.
>
> Ask the application administrator or the CM administrator when the last time the CM access privileges were reviewed.
>
> If CM access privileges have not been reviewed within the last three months, this is a finding.

</details>

## V-222664 — APSC-DV-003290

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** If the application contains classified data, a Security Classification Guide must exist containing data elements and their classification.

**Decision / action needed:** Obtain the explicit mission classification/availability/network designation; assess the applicable product/platform control or submit supported N/A only after that condition is established.

**Reason:** The exact check depends on the actual mission high-availability designation, DMZ topology or classified-data boundary. Product code supports classification labels and connected documents discuss partner/IL6-equivalent delivery, so unclassified-only/private-only applicability cannot be inferred. The relevant mission/environment designation has not been selected in the delivered app package; this is a policy input, not an uninvestigated runtime behavior.

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

## V-222673 — APSC-DV-003400

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The Program Manager must verify all levels of program management, designers, developers, and testers receive annual security training pertaining to their job function.

**Decision / action needed:** Attach annual secure-development training completion by role from the training record system; no runtime check is required.

**Reason:** Annual awareness/role-based training program and assigned 2026 courses are documented; this is stronger than missing policy. The official rule requires annual secure SDLC training for all management/design/development/test roles in addition to general awareness. Neither the source policy nor the connected findings provide that complete course completion record; do not substitute generic awareness assignments.

<details>
<summary>Official check — SV-222673r961863_rule</summary>

> This requirement is meant to be applied to developers and development teams only, otherwise, this requirement is not applicable.
>
> Interview the application representative.
>
> Ask for evidence of annual security training for application managers, designers, developers, and testers.
>
> Examples of evidence include course completion certificates and a class roster. At a minimum, security training should include security awareness training pertaining to overall principles of secure application development.
>
> Training must be in addition to DoD 8570 training requirements as DoD 8570 annual security training does not presently cover application SDLC security concerns.
>
> If there is no evidence of security training, this is a finding.

</details>

## V-265634 — APSC-DV-002010

**Benchmark:** Application Security and Development Security Technical Implementation Guide — ASD V6R5 STIG ([official XCCDF](../benchmarks/U_ASD_V6R5_STIG/benchmark.xml)).

**Requirement:** The application must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Decision / action needed:** Obtain the explicit mission classification/availability/network designation; assess the applicable product/platform control or submit supported N/A only after that condition is established.

**Reason:** The exact check depends on the actual mission high-availability designation, DMZ topology or classified-data boundary. Product code supports classification labels and connected documents discuss partner/IL6-equivalent delivery, so unclassified-only/private-only applicability cannot be inferred. The relevant mission/environment designation has not been selected in the delivered app package; this is a policy input, not an uninvestigated runtime behavior.

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

**Decision / action needed:** Identify the MPN mission classification and approved NSA/CSfC/platform cryptographic boundary. Assess that inherited boundary or record a supported unclassified N/A; do not infer classification from product naming.

**Reason:** The actual UDS release supplies FIPS-oriented controls, but FIPS validation alone is not evidence of the NSA-approved classified-data cryptographic boundary required by this check. Platform/host external protection may supply it; classification and approved boundary must be identified before source can determine applicability.

<details>
<summary>Official check — SV-233211r961863_rule</summary>

> Review documentation to verify that the container platform is using NSA-approved cryptography to protect classified data and applications.
>
> If the container platform is not using NSA-approved cryptography for classified data and applications, this is a finding.

</details>

## V-233220 — SRG-APP-000429-CTR-001060

**Benchmark:** Container Platform Security Requirements Guide — Container Platform V2R5 SRG ([official XCCDF](../benchmarks/U_Container_Platform_V2R5_SRG/benchmark.xml)).

**Requirement:** The container platform keystore must implement encryption to prevent unauthorized disclosure of information at rest within the container platform.

**Decision / action needed:** Gallatin selects the MPN Kubernetes distribution and encrypted storage/key-management design. Configure API Secret encryption through that distribution’s supported mechanism (upstream API server: --encryption-provider-config with nonidentity provider first), protect control-plane/datastore disks, and select encrypted storage for identity database/PVC data. Then map this rule to those committed infrastructure settings. Core has no universal storage-encryption flag that can substitute for this host choice.

**Reason:** Core source fully describes its own behavior but intentionally does not provision or choose MPN’s Kubernetes control-plane datastore and encrypted storage implementation. Keycloak PVCs can select a storage class; Core does not enable host Secret encryption or encrypted disks by itself. The remaining unknown is Gallatin’s as-yet-unselected MPN host/storage design, not an unknown UDS setting or a request for vendor proof.

<details>
<summary>Official check — SV-233220r1050650_rule</summary>

> Review container platform keystore documentation and configuration to verify encryption levels meet the information sensitivity level.
>
> If the container platform keystore encryption configuration does not meet system requirements, this is a finding.

</details>

## V-239371 — SRG-APP-000416-WSR-000118

**Benchmark:** Web Server Security Requirements Guide — Web Server V4R5 SRG ([official XCCDF](../benchmarks/U_Web_Server_V4R5_SRG/benchmark.xml)).

**Requirement:** The web server must implement required cryptographic protections using cryptographic modules complying with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance when encrypting data that must be compartmentalized.

**Decision / action needed:** Record the authoritative compartmentation/classification protection profile, then map the identified modules and boundary to that profile.

**Reason:** The original unclassified-MPN exclusion was unsupported: this rule includes sensitive/need-to-know compartmentalized data, not only formally classified data. Delivered FIPS images/Core mechanisms are now identified, but source does not specify the mission compartmentation policy and required protection profile for NATO/partner/IL6-equivalent use. Do not invent either an NSA-Type1 obligation or an unclassified exclusion.

<details>
<summary>Official check — SV-239371r1117186_rule</summary>

> Review policy documents to identify data that is compartmentalized (i.e. classified, sensitive, need-to-know, etc.) and requires cryptographic protection.
>
> Review the web server documentation and deployed configuration to identify the encryption modules utilized to protect the compartmentalized data.
>
> If the encryption modules used to protect the compartmentalized data are not compliant with the data, this is a finding.

</details>

## V-204770 — SRG-APP-000231-AS-000133

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must protect the confidentiality and integrity of all information at rest.

**Decision / action needed:** Attach or select the MPNstorage class/host/objectstore and backupencryption contract/configuration; assess that provider mechanism, not APIcrypto code.

**Reason:** The deliveredprofile selects UDS identity/Core but no MPN CSI/storage class, host disk encryption or offline backup target. Applicationpostgresvalues use default/empty storageClass and object storage is platform-provided. At-restcrypto can and should be supplied by that lowerlayer; source cannot identify an encryption backend that the deliveredcontract does not select. No new application-level crypto requirement is inferred.

<details>
<summary>Official check — SV-204770r1265177_rule</summary>

> Review the application server documentation and configuration to ensure the application server is protecting the confidentiality and integrity of all information at rest.
>
> If the confidentiality and integrity of all information at rest is not protected, this is a finding.

</details>

## V-204771 — SRG-APP-000231-AS-000156

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must employ cryptographic mechanisms to ensure confidentiality and integrity of all information at rest when stored off-line.

**Decision / action needed:** Attach or select the MPNstorage class/host/objectstore and backupencryption contract/configuration; assess that provider mechanism, not APIcrypto code.

**Reason:** The deliveredprofile selects UDS identity/Core but no MPN CSI/storage class, host disk encryption or offline backup target. Applicationpostgresvalues use default/empty storageClass and object storage is platform-provided. At-restcrypto can and should be supplied by that lowerlayer; source cannot identify an encryption backend that the deliveredcontract does not select. No new application-level crypto requirement is inferred.

<details>
<summary>Official check — SV-204771r961128_rule</summary>

> Review the application server configuration to ensure the system is protecting the confidentiality and integrity of all application server data at rest when stored off-line.
>
> If the application server is not configured to protect all application server data at rest when stored off-line, this is a finding.

</details>

## V-204811 — SRG-APP-000427-AS-000264

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must only allow the use of DoW PKI-established certificate authorities for verification of the establishment of protected sessions.

**Decision / action needed:** Attach/select the gateway TLSissuance configuration/certificate policy and map its CA and class to the exact protected session requirement.

**Reason:** UDS supplies DoD-approvedidentitytrust chains and meshworkloadcertificates, but this rule concerns the CA/class of the presented protected sessioncertificate. Gateway references an operator-suppliedTLS Secret; the deliveredHorizonprofile names host/issuer but contains no suppliedleaf certificate chain/class. Reusing identitytruststore evidence would conflate two differentcertificates.

<details>
<summary>Official check — SV-204811r1265185_rule</summary>

> Review the application server documentation and configuration to determine if the application server only allows the use of DoW PKI-established certificate authorities.
>
> If the application server allows other certificate authorities for verification, this is a finding.

</details>

## V-204812 — SRG-APP-000428-AS-000265

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must implement cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest on organization-defined information system components.

**Decision / action needed:** Attach or select the MPNstorage class/host/objectstore and backupencryption contract/configuration; assess that provider mechanism, not APIcrypto code.

**Reason:** The deliveredprofile selects UDS identity/Core but no MPN CSI/storage class, host disk encryption or offline backup target. Applicationpostgresvalues use default/empty storageClass and object storage is platform-provided. At-restcrypto can and should be supplied by that lowerlayer; source cannot identify an encryption backend that the deliveredcontract does not select. No new application-level crypto requirement is inferred.

<details>
<summary>Official check — SV-204812r1067567_rule</summary>

> Review application server documentation and configuration to determine if the application server implements cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest on organization-defined information system components.
>
> If the application server does not implement cryptographic mechanisms to prevent unauthorized modification, this is a finding.

</details>

## V-204813 — SRG-APP-000429-AS-000157

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application must implement cryptographic mechanisms to prevent unauthorized disclosure of organization-defined information at rest on organization-defined information system components.

**Decision / action needed:** Attach or select the MPNstorage class/host/objectstore and backupencryption contract/configuration; assess that provider mechanism, not APIcrypto code.

**Reason:** The deliveredprofile selects UDS identity/Core but no MPN CSI/storage class, host disk encryption or offline backup target. Applicationpostgresvalues use default/empty storageClass and object storage is platform-provided. At-restcrypto can and should be supplied by that lowerlayer; source cannot identify an encryption backend that the deliveredcontract does not select. No new application-level crypto requirement is inferred.

<details>
<summary>Official check — SV-204813r1067568_rule</summary>

> Review application server documentation and configuration to determine if the application server implements cryptographic mechanisms to prevent unauthorized disclosure of organization-defined information at rest on organization-defined information system components.
>
> If the application server does not implement cryptographic mechanisms to prevent unauthorized disclosure, this is a finding.

</details>

## V-204814 — SRG-APP-000435-AS-000069

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server, when a MAC I system, must be in a high-availability (HA) cluster.

**Decision / action needed:** Record MPN mission/MAC availability designation and its selected redundancy topology; assess that declared requirement.

**Reason:** The official check expressly depends on MAC I designation. The actual release contract identifies the identity/Core integration but does not declare mission criticality or required failover topology. Neither a universal HA finding nor N/A is justified by a source default replica count.

<details>
<summary>Official check — SV-204814r961620_rule</summary>

> If the application server is not a MAC I system, this requirement is NA.
>
> Review the application server documentation and configuration to determine if the application server is part of an HA cluster.
>
> If the application server is not part of an HA cluster, this is a finding.

</details>

## V-204832 — SRG-APP-000514-AS-000137

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must use DoW or CNSS-approved PKI Class 3 or Class 4 certificates.

**Decision / action needed:** Attach/select the gateway TLSissuance configuration/certificate policy and map its CA and class to the exact protected session requirement.

**Reason:** UDS supplies DoD-approvedidentitytrust chains and meshworkloadcertificates, but this rule concerns the CA/class of the presented protected sessioncertificate. Gateway references an operator-suppliedTLS Secret; the deliveredHorizonprofile names host/issuer but contains no suppliedleaf certificate chain/class. Reusing identitytruststore evidence would conflate two differentcertificates.

<details>
<summary>Official check — SV-204832r1265188_rule</summary>

> Review the application server configuration to determine if the application server utilizes approved PKI Class 3 or Class 4 certificates.
>
> If the application server is not configured to use approved DoW or CNS certificates, this is a finding.

</details>

## V-240925 — SRG-APP-000416-AS-000140

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Decision / action needed:** Obtain the MPN data classification and cryptographic protection boundary decision; assess required NSA-approved protection or record accepted N/A.

**Reason:** The actual artifact does not establish that MPN is unclassified. NSA-approved classified protection depends on the mission data classification and processing boundary, which are absent from the release contract. UDS FIPS cryptography alone does not establish NSA approval for a classified use case.

<details>
<summary>Official check — SV-240925r1117186_rule</summary>

> Review application server documentation to verify that the application server is using NSA-approved cryptography to protect classified data and applications resident on the device.
>
> If the application server is not using NSA-approved cryptography for classified data and applications, this is a finding.

</details>

## V-278962 — SRG-APP-001045-AS-000325

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must attach data tags containing organization-defined authorized processing to organization-defined elements of personally identifiable information.

**Decision / action needed:** Define in-scopePII elements and approvedprocessing/purposes, then record supportedN/A/delegation or map/add the requiredtags.

**Reason:** Users/profiledata are tenant-bound and protected, but these exact rules ask for tags identifying organization-defined authorizedPIIprocessing and processing purposes. Neither the release contract nor users schema defines those legal/policy tags or the in-scopePII elements. Tenant_id is an accesssecurityattribute, not automatically an authorized-processing-purpose tag. This remaining item is a policy/applicabilitydefinition, not uninvestigated runtimebehavior.

<details>
<summary>Official check — SV-278962r1227258_rule</summary>

> Verify the application server is configured to attach data tags containing organization-defined authorized processing to organization-defined elements of personally identifiable information.
>
> If the application server does not attach data tags containing organization-defined authorized processing to organization-defined elements of personally identifiable information, this is a finding.

</details>

## V-278963 — SRG-APP-001050-AS-000326

**Benchmark:** Application Server Security Requirements Guide — Application Server V4R6 SRG ([official XCCDF](../benchmarks/U_Application_Server_V4R6_SRG/benchmark.xml)).

**Requirement:** The application server must attach data tags containing organization-defined processing purposes to organization-defined elements of personally identifiable information.

**Decision / action needed:** Define in-scopePII elements and approvedprocessing/purposes, then record supportedN/A/delegation or map/add the requiredtags.

**Reason:** Users/profiledata are tenant-bound and protected, but these exact rules ask for tags identifying organization-defined authorizedPIIprocessing and processing purposes. Neither the release contract nor users schema defines those legal/policy tags or the in-scopePII elements. Tenant_id is an accesssecurityattribute, not automatically an authorized-processing-purpose tag. This remaining item is a policy/applicabilitydefinition, not uninvestigated runtimebehavior.

<details>
<summary>Official check — SV-278963r1227259_rule</summary>

> Verify the application server is configured to attach data tags containing organization-defined processing purposes to organization-defined elements of personally identifiable information.
>
> If the application server does not attach data tags containing organization-defined processing purposes to organization-defined elements of personally identifiable information, this is a finding.

</details>

## V-206570 — SRG-APP-000231-DB-000154

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must protect the confidentiality and integrity of all information at rest.

**Decision / action needed:** Attach the selected MPN storage/IaC encryption and key-management record, or accepted data-owner exemption/physical protection. Do not substitute unrelated Gallatin AWS storage.

**Reason:** DB-local encryption is not required when the MPN host/storage layer supplies the required at-rest protection. PostgreSQL uses a default-class PVC, but neither the release contract nor UDS chart selects the actual MPN storage encryption/key settings; MPN documentation still leaves host/storage decisions pending. This is a precise operator storage input, not an application encryption-code defect or a demand to observe runtime.

<details>
<summary>Official check — SV-206570r961128_rule</summary>

> If the application owner and Authorizing Official have determined that encryption of data at rest is NOT required, this is not a finding.
>
> Review DBMS settings to determine whether controls exist to protect the confidentiality and integrity of data at rest in the database.
>
> If controls do not exist or are not enabled, this is a finding.

</details>

## V-206604 — SRG-APP-000428-DB-000386

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must implement cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest (to include, at a minimum, PII and classified information) on organization-defined information system components.

**Decision / action needed:** Attach the selected MPN storage/IaC encryption and key-management record, or accepted data-owner exemption/physical protection. Do not substitute unrelated Gallatin AWS storage.

**Reason:** DB-local encryption is not required when the MPN host/storage layer supplies the required at-rest protection. PostgreSQL uses a default-class PVC, but neither the release contract nor UDS chart selects the actual MPN storage encryption/key settings; MPN documentation still leaves host/storage decisions pending. This is a precise operator storage input, not an application encryption-code defect or a demand to observe runtime.

<details>
<summary>Official check — SV-206604r1018552_rule</summary>

> Review the system documentation to determine whether the organization has defined the information at rest that is to be protected from modification, which must include, at a minimum, PII and classified information.
>
> If no information is identified as requiring such protection, this is not a finding.
>
> Review the configuration of the DBMS, operating system/file system, and additional software as relevant.
>
> If any of the information defined as requiring cryptographic protection from modification is not encrypted in a manner that provides the required level of protection, this is a finding.

</details>

## V-206605 — SRG-APP-000429-DB-000387

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must implement cryptographic mechanisms preventing the unauthorized disclosure of organization-defined information at rest on organization-defined information system components.

**Decision / action needed:** Attach the selected MPN storage/IaC encryption and key-management record, or accepted data-owner exemption/physical protection. Do not substitute unrelated Gallatin AWS storage.

**Reason:** DB-local encryption is not required when the MPN host/storage layer supplies the required at-rest protection. PostgreSQL uses a default-class PVC, but neither the release contract nor UDS chart selects the actual MPN storage encryption/key settings; MPN documentation still leaves host/storage decisions pending. This is a precise operator storage input, not an application encryption-code defect or a demand to observe runtime.

<details>
<summary>Official check — SV-206605r1018553_rule</summary>

> Review the system documentation to determine whether the organization has defined the information at rest that is to be protected from disclosure, which must include, at a minimum, PII and classified information.
>
> If the documentation indicates no information requires such protections, this is not a finding.
>
> Review the configuration of the DBMS, operating system/file system, and additional software as relevant.
>
> If any of the information defined as requiring protection is not encrypted in a manner that provides the required level of protection and is not physically secured to the required level, this is a finding.

</details>

## V-233495 — SRG-APP-000416-DB-000380

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must use NSA-approved cryptography to protect classified information in accordance with the data owner's requirements.

**Decision / action needed:** Record actual MPN data classification and required NSA cryptographic protection boundary; apply N/A only to a documented unclassified deployment.

**Reason:** Source supports classification metadata but does not determine whether the delivered MPN data requires NSA-approved classified cryptography. This is a mission-owner cryptographic applicability input; ordinary FIPS evidence alone cannot close a classified-data requirement.

<details>
<summary>Official check — SV-233495r1117186_rule</summary>

> If the DBMS is deployed in an unclassified environment, this is not applicable (NA).
>
> If the DBMS is not configured to use NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards, this is a finding.

</details>
