# Application data protection: Horizon on MPN

Status: Open. Protection requirements per data element: none found as of 2026-11-20 (evidence `mpn-data-protection-requirements-search`).

| Data element | Where stored (Horizon source `b84b9af`) | Protection requirement | Protection in release `2026.45.4-uds.1` |
|---|---|---|---|
| User identity: email, name, given name, family name, preferred username | Table `users` | | |
| Contact: name, email, phone, title, note | Table `contact_events` | | |
| Casualty record: blood type, gender, identity key, injury mechanism, injury pattern, injury timestamp, triage, patient category, ambulatory status, disposition state, note | Table `casualty_events` | | |
| Content records | Tables `assertions`, `chunks`, `files`, `ingestion_jobs`; each record carries a `classification` label (unclassified, classified, secret, top_secret; default unclassified) | | |

Tables reviewed as of 2026-11-20: `users`, `contact_events`, `casualty_events`, `assertions`, `chunks`, `files`, `ingestion_jobs`. The schema holds 222 tables; the others are not reviewed (evidence `mpn-data-protection-table`).
