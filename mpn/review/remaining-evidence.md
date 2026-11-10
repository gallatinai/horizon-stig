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

## V-233495 — SRG-APP-000416-DB-000380

**Benchmark:** Database Security Requirements Guide — Database V4R6 SRG ([official XCCDF](../benchmarks/U_Database_V4R6_SRG/benchmark.xml)).

**Requirement:** The DBMS must use NSA-approved cryptography to protect classified information in accordance with the data owner's requirements.

**Decision / action needed:** Identify or select the actual NSA-approved protection for PostgreSQL storage and relevant network boundaries. Record the product/model, version and approved configuration covering the DB. Reuse existing MPN protection where present; add a new layer only where needed.

**Reason:** The classified-deployment rule concerns DBMS compatibility with NSA-approved encryption devices. PostgreSQL can use transparent platform protection, but the checked UDS/PostgreSQL/SeaweedFS products have no exact match in the reviewed public CSfC component categories. The release and available MPN architecture do not name the selected approved storage/network protection. That missing selection prevents a supported pass; it does not prove PostgreSQL requires replacement or its own NSA certificate.

<details>
<summary>Official check — SV-233495r1117186_rule</summary>

> If the DBMS is deployed in an unclassified environment, this is not applicable (NA).
>
> If the DBMS is not configured to use NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards, this is a finding.

</details>
