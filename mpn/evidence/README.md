# Evidence scope

Product-boundary re-review, 10 November 2026. Recommendations describe expected behavior from the selected source, image contents, delivery contract and available organizational evidence; they are not formal assessor acceptance.

| Input | Exact version/source |
|---|---|
| Published UDS candidate | `2026.45.4-uds.1`, [successful push 42114745685](https://github.com/gallatinai/horizon-uds-bundle/actions/runs/42114745685) |
| Delivered Horizon source | `b84b9afcd6983d553b6b8406317b6592ec90cb7c`, [successful build 42109769948](https://github.com/gallatinai/horizon/actions/runs/42109769948) |
| Package source | `d528b7febf1ce8bb5ccf99661dade6ae09a84381` |
| Platform contract | UDS Core `1.14.0`, shared UDS identity, 12 digest-pinned images, no bundled Keycloak |
| Inspected Core source | `c15677633cffa17e99656a7d7ccd1f98d7cb6e4d` |
| Identity config | `0.32.0`, `74480722e1cc8405b5e9b65ac7d7086ab7f4056d`; shared Keycloak source `26.7.4` |

[Delivered release metadata](delivered-release/provenance.json) preserves the actual public build-info, platform contract, validation/vouch and registry digest records with hashes. [Image evidence](delivered-image-evidence.json) preserves exact image identities and selected SBOM crypto components. [Database image provenance](database-image-provenance.json) records statically inspected file hashes/packages. Image layers, registry credentials, real secrets, personnel rosters and controlled policy bodies are excluded.

[product-boundary-review.json](product-boundary-review.json) is the superseding decision log: all 411 previously open rows plus additional profile/applicability corrections, totaling 613 explicit re-review decisions and 258 sourced facts. [catalog.json](catalog.json) supplies clickable exact source references. Each original official check/fix is preserved in the rule exports.

## Reproduction and verification

`python3 scripts/build_review.py` applies the saved November 10 decisions after the historical source review. Then run `python3 scripts/summarize_review.py` and `python3 scripts/validate.py`. Validation checks all 1,048 official rules, original package/XML hashes and text, export agreement, complete 411-rule assignments, evidence links, render hashes and delivered image/profile closure.

`python3 scripts/render_delivered.py <bundle-checkout-at-d528b7f>` applies the same `apply_identity` and immutable `runtime_source.stage` transformations using saved release metadata, then Helm-renders `rendered-delivered/`: 12 charts and 16 main/init containers. No registry pull, secret generation, provider request or deployment occurs. Helm and PyYAML are required. Source placeholders remain placeholders; all rendered workload images match the delivered digest inventory.

[Independent verification](independent-verification.json) checked 15 release-artifact consistency assertions and ran 50 existing targeted crypto/profile/release-binding regression tests successfully. These test the verification mechanisms and negative cases. The small published metadata artifact does not include original phase DSSE envelopes, so actual release signature execution is inferred from the successful trusted pipeline and inspected gates, rather than falsely claimed as a replay of those envelopes.

## Historical inputs and limits

`rendered/` and `rendered-all/` retain earlier generic/default candidate captures; they are not the selected UDS profile. [source-investigation.json](source-investigation.json) retains the November 9 analysis of Horizon `3f3b51d...` and generic bundle defaults; [pre-rereview-20261109.json](../review/pre-rereview-20261109.json) freezes its published recommendations. The October ASD notes remain historical as originally dated. None silently replaces the delivered `b84b9af` source.

The published UDS candidate is still distinct from MPN-specific infrastructure and mission selection. No source selects the final MPN storage/KMS, leaf gateway certificate, registry lifecycle or mission classification/availability policy. Platform-provided controls are credited where source implements the objective; exact external selections/approval records remain explicit in [remaining evidence decisions](../review/remaining-evidence.md). Core flavor is not established by the Horizon identity contract alone; relevant auth/image crypto evidence is cited at the actual component boundary.
