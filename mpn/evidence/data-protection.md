# Application data protection: Horizon on MPN

| Data element group | Where stored | Classification and sensitivity | Protection in release `2026.45.4-uds.1` |
|---|---|---|---|
| User identity: email, name, given name, family name, preferred username | Table `users` (Horizon source `b84b9af`) | The SIA form of 2026-11-02 (signature fields empty) states "Processes PII? No". | |
| Contact event name and email | Table `contact_events` (Horizon source `b84b9af`) | | |
| Content records: assertions, chunks, files, ingestion jobs | Tables `assertions`, `chunks`, `files`, `ingestion_jobs`, column `classification` (Horizon source `b84b9af`) | Column values: unclassified, classified, secret, top_secret. Default: unclassified. | |

Protection requirements per element: none found as of 2026-11-20 (evidence `mpn-data-protection-requirements-search`).

Table source: evidence `mpn-data-protection-table`, 2026-11-20.
