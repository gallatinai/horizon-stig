# NSA component comparison for the MPN deployment

**The supplied Horizon/UDS package does not establish an NSA-approved protection layer.** Its FIPS modules and TLS mechanisms are identified, but no exact product match was found in the reviewed public CSfC categories. This does not establish that the surrounding MPN infrastructure lacks approved protection; the available architecture and release metadata do not name it.

| Component/function | Checked configuration | Result |
|---|---|---|
| PostgreSQL crypto | Delivered PostgreSQL 18 image; Chainguard OpenSSL provider, CMVP5132 | FIPS validation established; no exact CSfC product match found. PostgreSQL may remain behind approved platform encryption. |
| Object storage | SeaweedFS FIPS 4.52; optional native AES-GCM | No exact listed product match found. Its AES-GCM option is not itself evidence of a qualified CSfC composition. |
| UDS network encryption | Core 1.14.0; Istio/ztunnel 1.30.3; STRICT mTLS and TLS1.3 ingress | No exact mesh-product listing found. Source defaults do not establish a CNSA-only profile; matching ztunnel source also permits AES128 and uses P256 certificate keys. This is not a blanket finding against internal trusted-enclave traffic. |
| MPN host/storage/network protection | Operator-selected infrastructure outside the application package | Product/model, version and evaluated configuration are unspecified in the available MPN sources. This is the remaining protection-selection input. |

Sources: [NSA Components List](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Components-List/), [exact release metadata](evidence/delivered-release/build-info.json), and [source-level findings](evidence/nsa-component-check.json).

## Concrete listed candidates

These are conditional candidates, not an approved pair, purchase recommendation or claim about installed MPN equipment.

| Role | Listed product/version | Relevant restriction |
|---|---|---|
| Storage encryption | NetApp Volume Encryption, ONTAP 9.16.1 — VID11574 | Evaluated physical FAS/AFF/ASA configurations. The security target excludes cloud environments and VMware; Azure NetApp Files and Cloud Volumes ONTAP cannot inherit this listing by name. |
| Host block encryption | CACI Archon LUKS 3.0.0.2 — VID11568 | Evaluated Archon/RHEL8.10-derived build on specified Dell hardware. This is not generic approval for Linux LUKS, server hardware or Azure VMs. |
| IPsec boundary gateway | Juniper SRX1600, Junos23.4R1 | Match the exact evaluated model, software and security configuration. |
| IPsec boundary gateway | Cisco Secure Firewall3105/3110/3120/3130/3140, ASA9.20 | This listing is for the specified ASA configuration, not interchangeable FTD or arbitrary releases. |

Sources: [current product list](https://www.nsa.gov/Resources/Commercial-Solutions-for-Classified-Program/Components-List/), [NetApp evaluated scope](https://www.niap-ccevs.org/api/file/get_public_file/?file_id=37652), [Archon evaluated scope](https://www.niap-ccevs.org/api/file/get_public_file/?file_id=34448), [Juniper evaluation](https://www.niap-ccevs.org/products/international-product/2025.1096), [Cisco evaluation](https://www.niap-ccevs.org/products/11459).

## Correct placement

- **Storage:** DAR CP5.1 has power-state, architecture, independent-layer and unattended-use requirements. NAS/SAN drive protection in its stated powered-off scope does not establish protection of an authenticated, mounted database or its traffic. Do not assume two arbitrary encryption layers satisfy the package. [DAR package](https://www.nsa.gov/Portals/75/documents/CSfC%20CP%20Updates%202026/%28U%29%20Approved%20DAR%20CP%20v5.1.0%20-%20March%202026.pdf).
- **Network:** MSC CP1.3 protects relevant site-to-site crossings over untrusted networks using its prescribed independent IPsec/MACsec layers. It does not require treating each pod inside a trusted enclave as a separate site. Keep UDS mesh protection; map the actual external boundary separately. [MSC package](https://www.nsa.gov/Portals/75/documents/CSfC%20CP%20Updates%202026/%28U%29%20Multi-Site%20Connectivity%20Capability%20Package%20v1.3.0.pdf).

## Recommendation for V-233495

Keep PostgreSQL and UDS. Identify the MPN-approved encryption protecting the database volume, recovery media and relevant network boundaries. Record its **product/model, version, approved configuration and protected path**. Credit existing protection where it covers the requirement. If none is supplied, select an appropriately scoped Type1 or complete CSfC design with supported infrastructure.

The current status remains **Unclear** because that underlying protection is not selected in the supplied configuration. No application-only flag or PostgreSQL certificate lookup resolves the missing infrastructure selection.
