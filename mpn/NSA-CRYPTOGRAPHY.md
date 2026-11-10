# NSA-approved cryptography in STIGs

Use the exact requirement, discussion and check to identify which component supplies the protection.

NIST defines NSA-approved cryptography through an approved algorithm, an implementation approved for the relevant environment, and supporting key management. A FIPS certificate establishes a module's validation; it does not automatically approve every use of that module. Approved protection can be supplied by infrastructure around an application. [NIST definition](https://csrc.nist.gov/glossary/term/NSA_approved_cryptography).

## Database SRG: V-233495

The deployment is classified, so the rule applies. Its discussion states:

> This requirement addresses the compatibility of a DBMS with the encryption devices.

The check is whether the DBMS is protected by the required NSA-approved cryptography. It does not specify a separate NSA certificate for the PostgreSQL container. Determine which approved encryption protects PostgreSQL, confirm the database paths use it, and credit that control. Add or change database encryption only if a required path lacks protection. [Official SRG content](benchmarks/U_Database_V4R6_SRG/benchmark.xml).

The PostgreSQL 16 implementation of the same SRG provides an example: it checks PostgreSQL SSL configuration and protection by NSA-approved encrypting devices. Its PostgreSQL-specific SSL check is not automatically a new requirement for this repository's PostgreSQL 18 SRG mapping. [Implementation example, page 86](https://www.crunchydata.com/files/stig/PGSQL_16_STIG_V1R1.pdf#page=86).

## Apply each check's scope

Some checks address software modules, some encryption devices, and some the approved system solution. NSA's CSfC program permits appropriately configured commercial solutions as an alternative to Type1 protection; a product supporting a CNSA algorithm is not the entire solution. Do not require every component to obtain separate NSA product approval, and do not assume a FIPS image alone establishes classified-system protection. [NSA guidance](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/faq/).

[Component comparison and protection options](NSA-COMPONENT-CHECK.md) records the actual UDS/Horizon products checked against the public list and the exact candidate versions and limitations.
