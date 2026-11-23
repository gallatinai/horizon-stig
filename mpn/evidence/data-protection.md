# Application data protection: Horizon on MPN

Status: Open. Protection requirements per data element: none found as of 2026-11-20 (evidence `mpn-data-protection-requirements-search`).

| Data element | Where stored (Horizon source `b84b9af`) | Protection requirement | Protection in release `2026.45.4-uds.1` |
|---|---|---|---|
| User identity: email, name, given name, family name, preferred username | Table `users` | | Row-level security enabled and enforced; tenant isolation policy limits rows to the session tenant. |
| Contact: name, email, phone, title, note | Table `contact_events` | | Row-level security enabled and enforced; tenant isolation policy limits rows to the session tenant. |
| Casualty record: blood type, gender, identity key, injury mechanism, injury pattern, injury timestamp, triage, patient category, ambulatory status, disposition state, note | Table `casualty_events` | | Row-level security enabled and enforced; tenant isolation policy limits rows to the session tenant. |
| Content records | Tables `assertions`, `chunks`, `files`, `ingestion_jobs`; each record carries a `classification` label (unclassified, classified, secret, top_secret; default unclassified) | | Row-level security enabled and enforced; tenant isolation policy limits rows to the session tenant. |

Tables reviewed as of 2026-11-20: `users`, `contact_events`, `casualty_events`, `assertions`, `chunks`, `files`, `ingestion_jobs`. The schema holds 225 tables; the others are not reviewed (evidence `mpn-data-protection-table`).

Release `2026.45.4-uds.1` settings that apply to every row: service mesh mode ambient; application-to-database `sslmode` disable; database credentials read from a Kubernetes secret. No encryption-at-rest setting found in the rendered manifests, searched 2026-11-23 (evidence `mpn-data-protection-release-search`).
