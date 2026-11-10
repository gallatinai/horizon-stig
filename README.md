# Horizon STIG tracking

Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection. Gallatin manages this UDS Core deployment on MPN, which will process classified data.

| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |
|---|---:|---:|---:|---:|---:|---:|
| [ASD_V6R5_STIG](mpn/review/U_ASD_V6R5_STIG.md) | 286 | 63 | 190 | 1 | 32 | 0 |
| [Kubernetes_V2R6_STIG](mpn/review/U_Kubernetes_V2R6_STIG.md) | 92 | 2 | 89 | 0 | 0 | 1 |
| [Container_Platform_V2R5_SRG](mpn/review/U_Container_Platform_V2R5_SRG.md) | 188 | 33 | 153 | 0 | 2 | 0 |
| [Web_Server_V4R5_SRG](mpn/review/U_Web_Server_V4R5_SRG.md) | 126 | 16 | 102 | 0 | 6 | 2 |
| [Application_Server_V4R6_SRG](mpn/review/U_Application_Server_V4R6_SRG.md) | 137 | 22 | 110 | 1 | 4 | 0 |
| [Database_V4R6_SRG](mpn/review/U_Database_V4R6_SRG.md) | 142 | 24 | 98 | 1 | 18 | 1 |
| [AAA_Services_V2R3_SRG](mpn/review/U_AAA_Services_V2R3_SRG.md) | 77 | 16 | 50 | 0 | 11 | 0 |

**Totals:** 176 Needs work; 792 Likely covered; 3 Unclear; 73 Needs N/A justification; 4 source-only Compliant.

The 176 needs-work recommendations group into **33 shared workstreams**. Every rule has a suggested status, justification, evidence links and next action. Final component checklists require acceptance of the stated evidence and applicability.

- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)
- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)
- [Implementation plans and operating procedures](mpn/EVIDENCE-ACTIONS.md)
- [Gallatin UDS configuration actions](mpn/UDS-CONFIGURATION.md)
- [NSA-approved cryptography: applying the STIG wording](mpn/NSA-CRYPTOGRAPHY.md) · [Checked components and protection options](mpn/NSA-COMPONENT-CHECK.md)
- [Assessment decisions](mpn/evidence/current-assessment.json)
- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)
- [Improvement priorities and effort estimate](mpn/FINDINGS.md)
- [Evidence boundaries and exact source versions](mpn/evidence/README.md)
- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)

The package baseline is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Image SBOMs, FIPS configuration and release verification support the control mappings. Gallatin manages UDS Core on MPN and owns its platform configuration. Controls may be supplied by the gateway, mesh, IdP, database, host or organizational procedure. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.

Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, `python3 scripts/generate_cklb.py`, then `python3 scripts/validate.py`. [current-assessment.json](mpn/evidence/current-assessment.json) stores the status decisions and evidence references. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required).

## Updating a STIG in a PR

Use Python 3.9 or later and run commands from the repository root. The assessment JSON files are the editable source; the rule tables, CSVs, counts, solution pages and CKLB files are generated.

[Download the seven CKLB checklists](mpn/cklb/). The [Update CKLB checklists workflow](.github/workflows/update-cklb.yml) regenerates and commits them after every push to `main`. Each file contains one benchmark and its current findings, evidence and next actions. See [CKLB status mapping and explicit dispositions](mpn/cklb/README.md) for how recommendations become checklist statuses. Edit the assessment sources; do not edit CKLB files directly.

### 1. Create a branch

```sh
git switch main
git pull --ff-only
git switch -c stig/v206414-session-lifetime
```

### 2. Add evidence for the fix

Add an entry to [mpn/evidence/catalog.json](mpn/evidence/catalog.json). Give it a stable ID, describe what the implementation/configuration establishes, and link to the exact commit or retained evidence. Replace the placeholders in this example:

```json
"uds-session-eight-hours": {
  "title": "UDS eight-hour session limit",
  "observation": "The Core override sets SSO_SESSION_MAX_LIFESPAN to 28800 seconds; the existing realm is updated to match.",
  "url": "https://github.com/gallatinai/<deployment-repo>/blob/<full-commit>/<core-overrides-file>"
}
```

Only record settings, test results and approvals that the evidence actually supports. Link configuration and public fingerprints; keep secrets and restricted records in their appropriate controlled systems.

### 3. Update the rule's decision

Find the V-ID under `decisions` in [mpn/evidence/current-assessment.json](mpn/evidence/current-assessment.json). Update its status, justification, evidence IDs and next action; preserve the other fields.

For example, after implementing the eight-hour limit required by `V-206414`, the relevant fields could be:

```json
"status": "Likely covered",
"justification": "The UDS realm maximum session lifetime is configured to 28800 seconds (eight hours).",
"evidence_ids": ["uds-session-eight-hours"],
"next_step": "Confirm the assessed release applies these realm settings."
```

These snippets illustrate edits, not completed fixes. Use `Likely covered` for supported source/configuration coverage that still needs confirmation; use `Compliant` only when the complete requirement is supported for the assessed component. This repository's Compliant recommendations use `evidence_state: "source-inferred"`; final CKLB acceptance is separate. Keep `Needs work`, `Unclear` or `Needs N/A justification` where the corresponding work, decision or applicability justification remains.

Check related rules sharing the same `task`, and update each only where the fix covers it. A merged source fix does not prove it is included in the assessed deployment. Cite its release/configuration scope accurately; update the top-level baseline and corresponding release artifacts only when assessing a new release.

### 4. Update the implementation plan if needed

Edit [mpn/evidence/implementation-plans.json](mpn/evidence/implementation-plans.json) when the solution instructions change. It generates `mpn/solutions/` and the implementation-plan index. Edit prose guides such as `mpn/UDS-CONFIGURATION.md` directly when their instructions change.

### 5. Rebuild and validate

```sh
python3 scripts/build_review.py
python3 scripts/summarize_review.py
python3 scripts/generate_cklb.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
git diff --stat
```

Review the regenerated tables, counts, evidence decisions, workstreams and CKLB findings. Do not edit `mpn/review/`, `mpn/solutions/`, `mpn/EVIDENCE-ACTIONS.md` or `mpn/cklb/*.cklb` directly: rebuild them from their sources. Preserve the official benchmark ZIPs, XCCDF and normalized rules in `mpn/benchmarks/`. After merge, the workflow refreshes the CKLB files even if the PR did not regenerate them locally.

The README is also generated. To change this tutorial or its surrounding text, edit `scripts/summarize_review.py` and regenerate it.

### 6. Commit the sources and generated outputs

```sh
git add mpn README.md
git commit -m "Update V-206414 session-limit assessment"
git push -u origin stig/v206414-session-lifetime
```

Include `scripts/` in the commit if you changed a generator. Open a PR stating the affected V-IDs, the implementation/configuration commit or PR, the assessed release scope, the recommended statuses and the validation result.
