# Evidence scope

Provisional source/configuration assessment, 9 November 2026. No live MPN tests or assessor sign-off are claimed.

| Source | Exact version/commit |
|---|---|
| Horizon | `3f3b51d454197c077b33896caf93de72b94eafda` |
| horizon-uds-bundle | `d528b7febf1ce8bb5ccf99661dade6ae09a84381` |
| UDS Core | `1.14.0`, `c15677633cffa17e99656a7d7ccd1f98d7cb6e4d` |
| UDS identity-config | `0.32.0`, `74480722e1cc8405b5e9b65ac7d7086ab7f4056d` |
| Keycloak cookie implementation | `26.7.2`, linked exact tagged upstream source |
| Historical ASD review | Horizon `3361610361b80eabd08527b2cd640b696edda4d5`; bundle `204caa2657434dcb9d3217ae7ea4dc5c894a2d38`, October review |

[catalog.json](catalog.json) links evidence to exact source files. [source-investigation.json](source-investigation.json) preserves 949 explicit deeper decisions and observations. [asd-october-review.json](asd-october-review.json) retains the older rule-level notes as historical context, not refreshed test results. The original 1,048-row published review is frozen in [initial-source-pass.json](../review/initial-source-pass.json).

The selected candidate is a general/demo profile with bundled Keycloak and hosted LLM assumptions; it is not an established MPN release. Current Horizon source and embedded candidate image tags are different baselines. Recommendations based on current source do not establish that it was built into those images. The deployed release digest, overrides, host OS baseline, exceptions, CA/storage settings and operational approval/test records remain external inputs.

## Render captures

`rendered/` retains the original four chart captures. `rendered-all/` captures all 13 candidate charts and summarizes 21 main/init containers. [rendered-manifest.json](rendered-manifest.json) records hashes, source commit and reproduction commands. Helm uses pinned source values with Zarf placeholders retained; the chat/ingestion provider placeholder is resolved to the package's `openai` default for rendering only. No deployment or provider request occurs and no live credential was captured.

Reproduce with `python3 scripts/render_candidate.py <pinned-bundle-checkout>` from the repository root (Helm and PyYAML required). These are pre-admission candidate manifests, without actual MPN overrides or observed behavior. Kubernetes inheritance recommendations identify MPN ownership; they do not prove an unseen host setting. Source-only Compliant recommendations are limited to four narrow layout/configuration checks and require confirmation against the selected release.

The official ZIP/XCCDF and full normalized checks/fixes are preserved with [hashes](../benchmarks/manifest.json). Rebuild the saved disposition with `python3 scripts/build_review.py`; run `python3 scripts/summarize_review.py` and `python3 scripts/validate.py` for summaries and inventory/export/provenance checks. Refreshing the deeper investigation additionally requires the pinned checkouts at the paths described in `scripts/investigate.py`.
