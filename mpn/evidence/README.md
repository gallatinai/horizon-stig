# Evidence scope

Assessment date: 9 November 2026. This is provisional source/configuration triage, not certification or a live MPN assessment.

| Input | Exact snapshot |
|---|---|
| Horizon `origin/main` fetched for this review | `3f3b51d454197c077b33896caf93de72b94eafda` |
| horizon-uds-bundle `origin/main` fetched for this review | `d528b7febf1ce8bb5ccf99661dade6ae09a84381` |
| Historical ASD review | Horizon `3361610361b80eabd08527b2cd640b696edda4d5`; UDS candidate `204caa2657434dcb9d3217ae7ea4dc5c894a2d38`, updated Oct 27 |
| Official content | Original DISA packages, XCCDF and SHA-256 recorded in [manifest](../benchmarks/manifest.json) |

The current source heads and image tags embedded in the candidate are different baselines. No claim is made that current Horizon source has been built into those candidate images or deployed on MPN. No MPN release digest was supplied.

[catalog.json](catalog.json) links observations to exact GitHub commits or dated scope. [asd-october-review.json](asd-october-review.json) preserves earlier per-rule observations with their original commit references; it does not silently refresh those conclusions to current source.

## Rendered candidate evidence

The files in `rendered/` were produced using Helm with chart defaults plus the corresponding `source/values/*.yaml` from the pinned UDS candidate. Namespace: `horizon-uds`. Deploy-time Zarf substitutions remain placeholders; no real credential values were read or captured.

Example (substitute a checkout at the pinned commit):

```sh
helm template seaweedfs source/charts/seaweedfs -n horizon-uds -f source/values/seaweedfs.yaml
helm template postgres source/charts/horizon-postgres -n horizon-uds -f source/values/postgres.yaml
helm template keycloak source/charts/keycloak -n horizon-uds -f source/values/keycloak.yaml
helm template package source/charts/horizon-uds-package -n horizon-uds -f source/values/uds-package.yaml
```

These renders verify candidate template behavior. They do not include a final MPN override set, Zarf deployment, UDS admission mutations, the host's effective policies or observed workload behavior.

## Method and limits

1. Parse every official rule with ID, severity, title, description, complete check and fix. Retain original packages.
2. Route all requirements to provisional ownership/evidence categories. Keep this generated initial pass.
3. Inspect current source and four rendered charts for high-risk candidate concerns; compare exact Kubernetes/AAA checks, inspect conditional applicability, and record supported corrections.
4. Leave unsupported outcomes Unclear or conditional Likely covered. No Compliant designation is generated. Flag Needs work/Unclear for John.

The second pass is bounded source validation, not 1,048 completed manual/runtime tests. Generic rows describe what evidence is missing. Final results require the official checks applied separately to each component, actual release configuration, host/inheritance records and assessor decisions. Human approval fields are deliberately not fabricated.
