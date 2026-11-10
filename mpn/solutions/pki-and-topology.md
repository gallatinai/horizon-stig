# Certificate trust and deployment topology

| STIG/SRG rule | Requirement | Current status |
|---|---|---|
| [V-204811 / SRG-APP-000427-AS-000264](../review/U_Application_Server_V4R6_SRG.md) | The application server must only allow the use of DoW PKI-established certificate authorities for verification of the establishment of protected sessions. | Needs work |
| [V-204832 / SRG-APP-000514-AS-000137](../review/U_Application_Server_V4R6_SRG.md) | The application server must use DoW or CNSS-approved PKI Class 3 or Class 4 certificates. | Needs work |
| [V-222595 / APSC-DV-002410](../review/U_ASD_V6R5_STIG.md) | The web service design must include redundancy mechanisms when used with high-availability systems. | Likely covered |
| [V-204814 / SRG-APP-000435-AS-000069](../review/U_Application_Server_V4R6_SRG.md) | The application server, when a MAC I system, must be in a high-availability (HA) cluster. | Unclear |
| [V-222620 / APSC-DV-002890](../review/U_ASD_V6R5_STIG.md) | Application web servers must be on a separate network segment from the application and database servers if it is a tiered application operating in the DoW DMZ. | Unclear |

## Gateway PKI and conditional topology solutions

These are proposed target settings and operating procedures. They are not deployed changes or new claims about the running MPN environment. Gallatin operates Core; the mission authority supplies only mission designation and approved issuance/CA decisions.

### Approved gateway certificates and restrictive verification

1. Gallatin SRE owns the gateway certificate lifecycle. Prepare a CSR using the actual MPN tenant/admin host SANs; prefer explicit SANs where mission issuance policy disallows wildcards. Route it through the mission-authorized DoW/CNSS NPE/server certificate issuance process or an explicitly approved external-PKI equivalent. A FIPS image does not select certificate assurance/class. A generic public certificate is not automatically approved or disapproved: record its issuer/policy approval.
2. Deliver full-chain `tls.crt`, private `tls.key`, and the approved client CA roots (`cacert`, when client-certificate verification is selected) through the protected secret process. Create separate Secrets in `istio-tenant-gateway` and `istio-admin-gateway`; do not commit keys to this tracker. Existing Core supports these references:

```yaml
## Core package bundle overrides; example names, not actual production secrets.
overrides:
  istio-tenant-gateway:
    uds-istio-config:
      values:
        - path: tls.credentialName
          value: mpn-tenant-gateway-tls
  istio-admin-gateway:
    uds-istio-config:
      values:
        - path: tls.credentialName
          value: mpn-admin-gateway-tls
```

Retain Core's HTTPS/TLS1.3 gateway. `OPTIONAL_MUTUAL` on the SSO host permits password+OTP alongside CAC; select `MUTUAL` only for a mission certificate-only path. Configure the client CA in the referenced secret for the selected mode. API containers remain protected by mesh plus the gateway; there is no need to reimplement public TLS per application container.

3. Publish an explicit approved-root bundle through Core. Start from `CA_BUNDLE_INCLUDE_DOD_CERTS: "true"`, `CA_BUNDLE_INCLUDE_PUBLIC_CERTS: "false"`; use `CA_BUNDLE_CERTS` only for named, approved additional chains. Do not turn on the whole public bundle to work around a missing service CA. Every exception is tied to a needed service and documented approved issuer. Confirm that the DoD external-PKI root set actually selected is appropriate for the mission's assurance policy.
4. Mount `uds-trust-bundle` at a read-only path in the API; for its Node HTTPS/JWKS verification use an explicit per-client `ca` configuration, or `--use-openssl-ca` with `SSL_CERT_FILE` pointing to the curated PEM and `SSL_CERT_DIR` pointing to a controlled empty/curated directory. Preserve existing FIPS/startup options when adding Node options. Remove conflicting additive/system-root choices. `NODE_EXTRA_CA_CERTS` alone only adds roots and does **not** enforce the rule's restrictive trust set. Scope CA restrictions to the actual protected-session verifier; local mesh workload certificates and externally approved server certificates have separate trust mappings. Apply equivalent per-client CA settings for other service runtimes that initiate relevant TLS.
5. Keep the certificate evidence record in the compliance package: host/SAN, issuer and approved assurance/class/certificate-policy OID, public-chain fingerprint, validity, renewal owner, approved CA set, and secret reference. Validate the public chain and exact hostname offline against approved roots; keep fixtures showing that an unrelated CA is rejected. Secret manager/certificate automation should rotate material before expiration and retain old/new public fingerprints, without exposing keys. This closes a specified provisioning/control task; evidence is not a request for a DU-managed-cluster attestation.

### HA design versus MAC I deployment

V-222595 asks about redundancy design, which the templates already support. V-204814 additionally requires an actual HA cluster **if** the mission declares MAC I. Mission authority records MAC I true/false; this policy choice cannot be invented from source.

For a required HA target, deploy Core/ingress and the application on at least three schedulable nodes across the available fault domains. Configure each stateless web/API service with at least two replicas (or HPA `minReplicas: 2`), readiness/liveness, PDB `minAvailable: 1`, and node/zone spreading. Example existing common-chart settings:

```yaml
replicaCount: 2
pdb:
  enabled: true
  minAvailable: 1
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app.kubernetes.io/instance: horizon-api
```

Use the matching release label for each service; add zone spread only when multiple zones actually exist. HPA CPU scaling also requires meaningful CPU requests. PDBs limit voluntary disruptions; they do not prevent hardware failure or make a singleton stateful service redundant.

Complete stateful dependencies explicitly: replace the selected single-node PostgreSQL topology with a supported HA PostgreSQL primary/standby setup and stable failover endpoint (or approved external HA PostgreSQL); do not merely set StatefulSet replicas greater than one on independent unreplicated PGDATA. Use a properly configured clustered NATS/JetStream deployment with replicated streams and separate durable volumes, redundant object storage/storage backend, and HA Core identity/database/gateway dependencies. Select storage/cluster products supported in the MPN environment, with an owned failover/restore procedure and approved recovery objectives. Multiple stateless replicas alone do not satisfy this whole-service requirement. If MAC I is false, retain the source-capability mapping and submit the exact rule's N/A.

### Conditional DoW DMZ tier isolation

The mission authority records whether the approved MPN network boundary is a DoW DMZ. Do not equate private DNS, `uds.dev`, classification discussion, or a namespace with that designation.

If the tiered app is in the DoW DMZ, Gallatin replaces broad `IntraNamespace` permissions with three default-deny tier namespaces/Packages: `horizon-web`, `horizon-app`, `horizon-data`. A diagram and policy matrix state the following target flows:

| Source | Destination | Allowed target |
|---|---|---|
| Tenant ingress gateway | Web | Static HTTP port3000 |
| Tenant ingress gateway | API | API port3001, declared API routes |
| Tenant ingress gateway | NATS websocket endpoint | Only selected websocket8443 route |
| API/authorized workers | PostgreSQL | TCP5432 with explicit destination namespace/pod selector |
| API/authorized workers | NATS | Declared service ports only |
| API/authorized workers | Object storage/model runtime | Approved local endpoints/ports only |
| Web pod | API/database | No direct pod-to-pod access; browser calls the public API route |
| Each selected tier | DNS, approved telemetry, identity | Explicit infrastructure/service peers and required ports only |

Each application pod remains mesh enrolled. Peer rules combine namespace and pod selectors in a **single** peer when both are needed, rather than accidentally OR-ing all namespaces/all pods. Remove the old broad permissions: Kubernetes policies are additive, so a narrow policy does not cancel an existing allow-all. Namespace separation requires updating chart namespaces, service FQDN references and Package exposures; the static browser's public API/SSO origin need not change merely because backend namespaces change. Keep administrative access on the separately controlled Core admin path. Have the mission accept this logical network segmentation against the actual DMZ boundary requirements; NSA/CISA guidance supports pod/namespace policy isolation as a Kubernetes segmentation mechanism. If not in the DoW DMZ, record the exact conditional N/A instead of implementing a fictitious DMZ deployment.

## Source references

- [solution-topology-trust-doc](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/docs/how-to-guides/networking/manage-trust-bundles.mdx)
- [solution-topology-trust-source](https://github.com/defenseunicorns/uds-identity-config/blob/74480722e1cc8405b5e9b65ac7d7086ab7f4056d/src/truststore/ca-to-jks.sh)
- [solution-topology-app-jwks](https://github.com/gallatinai/horizon/blob/b84b9afcd6983d553b6b8406317b6592ec90cb7c/apps/api/src/api/auth/auth.oidc-jwt.service.ts)
- [solution-topology-node-ca](https://nodejs.org/api/cli.html#--use-bundled-ca---use-openssl-ca)
- [solution-topology-istio-secret](https://istio.io/latest/docs/reference/config/networking/gateway/)
- [solution-topology-dod-ca](https://dl.dod.cyber.mil/wp-content/uploads/pki-pke/pdf/unclass-dod_approved_external_pkis_master_document.pdf)
- [solution-topology-tls-doc](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/docs/how-to-guides/networking/configure-tls-certificates.mdx)
- [solution-topology-tls-template](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/istio/charts/uds-istio-config/templates/gateway.yaml)
- [solution-topology-dod-commercial](https://dl.dod.cyber.mil/wp-content/uploads/pki-pke/pdf/unclass-ss_using_commercial_pki_certificates.pdf)
- [solution-topology-dod-npe](https://www.cyber.mil/pki-pke)
- [solution-topology-deploy](https://github.com/gallatinai/horizon-uds-bundle/blob/d528b7febf1ce8bb5ccf99661dade6ae09a84381/source/charts/horizon-service/templates/deployment.yaml)
- [solution-topology-ha-values](https://github.com/gallatinai/horizon-uds-bundle/blob/d528b7febf1ce8bb5ccf99661dade6ae09a84381/source/charts/horizon-service/values.yaml)
- [solution-topology-pdb](https://github.com/gallatinai/horizon-uds-bundle/blob/d528b7febf1ce8bb5ccf99661dade6ae09a84381/source/charts/horizon-service/templates/pdb.yaml)
- [solution-topology-postgres](https://github.com/gallatinai/horizon-uds-bundle/blob/d528b7febf1ce8bb5ccf99661dade6ae09a84381/source/values/postgres.yaml)
- [solution-topology-tiers](https://github.com/gallatinai/horizon-uds-bundle/blob/d528b7febf1ce8bb5ccf99661dade6ae09a84381/source/charts/horizon-uds-package/templates/package.yaml)
- [solution-topology-default-deny](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/pepr/operator/controllers/network/defaults/default-deny-all.ts)
- [solution-topology-k8-seg](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [solution-topology-nsa-seg](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
