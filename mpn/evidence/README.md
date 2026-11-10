# Evidence and assessed configuration

Gallatin manages the UDS Core deployment on MPN. Recommendations use UDS Core source, Horizon source, image contents and the package's selected configuration. DU-managed IL5/IL6 deployment evidence is outside this assessment.

| Input | Version/source |
|---|---|
| Horizon UDS package | `2026.45.4-uds.1`, [publication pipeline](https://github.com/gallatinai/horizon-uds-bundle/actions/runs/42114745685) |
| Horizon source | `b84b9afcd6983d553b6b8406317b6592ec90cb7c`, [build](https://github.com/gallatinai/horizon/actions/runs/42109769948) |
| Package source | `d528b7febf1ce8bb5ccf99661dade6ae09a84381` |
| Package configuration | UDS Core `1.14.0`, shared UDS identity, 12 digest-pinned images |
| UDS Core source | `c15677633cffa17e99656a7d7ccd1f98d7cb6e4d` |
| Identity configuration | `0.32.0`, `74480722e1cc8405b5e9b65ac7d7086ab7f4056d`; Keycloak `26.7.4` |

[current-assessment.json](current-assessment.json) contains every current status decision and next action. [catalog.json](catalog.json) links the supporting source files and observations. Official check/fix text and package hashes are retained in the [benchmark manifest](../benchmarks/manifest.json).

[Release metadata](delivered-release/provenance.json) identifies build, profile, validation and publication digests. [Image evidence](delivered-image-evidence.json) records image identities and relevant SBOM crypto components; [database image provenance](database-image-provenance.json) records inspected package/file identities. [Verification results](independent-verification.json) cover release consistency and the pipeline's crypto/profile validation mechanisms.

Rebuild with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. Validation checks rule completeness, official text, source package hashes, evidence references, export consistency and delivered image/profile closure.

`python3 scripts/render_delivered.py <bundle-checkout-at-d528b7f>` applies the package's identity and immutable image transformations, then renders 12 charts and 16 containers to `rendered-delivered/`. It requires Helm and PyYAML and uses placeholders without registry pulls, secret generation or deployment.

UDS source defaults supply the platform behavior used for recommendations. MPN-specific storage/KMS, network/registry, certificate and mission choices must be selected in Gallatin's deployment configuration. Final CKLB acceptance also requires the stated organizational decisions and records.
