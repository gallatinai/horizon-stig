# Application data protection: Horizon on MPN

Status: Open. Protection requirements per data element: none found as of 2026-11-20 (evidence `mpn-data-protection-requirements-search`).

| Data element | Where stored (Horizon source `b84b9af`) | Protection requirement | Protection in Horizon source `b84b9af` |
|---|---|---|---|
| User identity: email, name, given name, family name, preferred username | Table `users` | | Row-level security enabled and enforced (`row_security`); RESTRICTIVE policy `tenant_isolation` matches `tenant_id` to `app.tenant_id`. Source at the baseline commit, not a deployed state. |
| Contact: name, email, phone, title, note | Table `contact_events` | | Row-level security enabled and enforced (`row_security`); RESTRICTIVE policy `tenant_isolation` matches `tenant_id` to `app.tenant_id`. Source at the baseline commit, not a deployed state. |
| Casualty record: blood type, gender, identity key, injury mechanism, injury pattern, injury timestamp, triage, patient category, ambulatory status, disposition state, note | Table `casualty_events` | | Row-level security enabled and enforced (`row_security`); RESTRICTIVE policy `tenant_isolation` matches `tenant_id` to `app.tenant_id`. Source at the baseline commit, not a deployed state. |
| Content records | Tables `assertions`, `chunks`, `files`, `ingestion_jobs`; each record carries a `classification` label (unclassified, classified, secret, top_secret; default unclassified) | | Row-level security enabled and enforced (`row_security`); RESTRICTIVE policy `tenant_isolation` matches `tenant_id` to `app.tenant_id`. Source at the baseline commit, not a deployed state. |

Tables reviewed as of 2026-11-20: `users`, `contact_events`, `casualty_events`, `assertions`, `chunks`, `files`, `ingestion_jobs`. The schema holds 225 tables; the others are not reviewed (evidence `mpn-data-protection-table`).

Settings in the rendered manifests of release `2026.45.4-uds.1` (not tied to one data element):
- The UDS Package `horizon` sets `network.serviceMesh.mode: ambient`. Application database connections set no TLS (next item); in-cluster traffic is encrypted by the platform's mesh mTLS (STRICT, ambient), a UDS Core 1.14.0 default.
- `POSTGRES_SSLMODE` is `disable` for the API, chat-agent, artifact-ingestion, ops-readiness and simulation workloads and for the five migration containers. OpenFGA connects with `sslmode=disable` in its datastore URI. The tenant-bootstrap script sets `ssl: false`. `DATABASE_URL` sets no `sslmode`, and the PostgreSQL server arguments set no SSL term.
- Database credentials for the API are read from the Kubernetes secret `horizon-postgres-secret` by `secretKeyRef`. The secret itself is not in the rendered manifests.
- The PostgreSQL volume claim requests 50Gi `ReadWriteOnce` with no `storageClassName`. No `encrypt`, `kms`, `storageClass`, `pgcrypto`, `luks` or `tde` term was found in the rendered manifests, the workload summary or the delivered-release files, searched 2026-11-23 (evidence `mpn-data-protection-release-search`). The storage layer of MPN was not searched.
