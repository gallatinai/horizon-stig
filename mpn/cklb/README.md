# Generated CKLB checklists

The [Update CKLB checklists workflow](../../.github/workflows/update-cklb.yml) runs
after every push to `main`. It regenerates one STIG Viewer 3 `.cklb` per benchmark
in [the manifest](../benchmarks/manifest.json), validates the assessment and
checklists, and commits changed CKLB files back to `main`. It can also be run with
**Run workflow** in GitHub Actions. Unchanged output produces no commit. Commits
use `GITHUB_TOKEN`, whose pushes do not start another workflow run.

Edit [current-assessment.json](../evidence/current-assessment.json) and
[catalog.json](../evidence/catalog.json), not these generated files. Each rule
includes its recommendation, justification, evidence links, owner and next action.
The complete check/fix text, discussion, identifiers and benchmark version come
from the saved DISA XCCDF. UUIDs are deterministic so status changes produce
small diffs.

| Assessment recommendation | CKLB status |
|---|---|
| Compliant | Not a Finding |
| Needs work | Open |
| Likely covered | Not Reviewed |
| Unclear | Not Reviewed |
| Needs N/A justification | Not Reviewed |

To record a specific checklist disposition, add `cklb_status` to that rule's
assessment decision. Allowed values are `open`, `not_a_finding`, `not_applicable`
and `not_reviewed`. When this differs from the default above, also provide a
nonempty `cklb_justification` explaining the disposition and cite its supporting
evidence in `evidence_ids`. For example, an established N/A determination can use:

```json
"cklb_status": "not_applicable",
"cklb_justification": "Explain why this requirement does not apply to the assessed component."
```

These files use the logical target `Horizon-MPN`, with addresses and asset fields
blank. They represent the repository's product assessment. Add actual submission
asset metadata to a copy in the appropriate deployment system. The rule
`classification` field describes the public DISA benchmark content; it does not
designate the classification of the MPN environment. Changes made directly in
STIG Viewer are overwritten on regeneration unless incorporated into the source
decisions.

Generate or verify locally with Python 3.9 or later; no packages are required:

```sh
python3 scripts/generate_cklb.py
python3 scripts/generate_cklb.py --check
python3 -m unittest discover -s tests -v
```

The field layout is cross-checked against the primary
[UDS CKLB writer](https://github.com/defenseunicorns/uds-pk/blob/cea02930525991c7cc132aa29aa78ab765548ab6/src/stig/xccdf.go)
and [MITRE CKLB reader/writer](https://github.com/mitre/hdf-libs/blob/9c1d2d0a9a495e7346576826994d4c88c381217b/hdf-converters/shared/go/checklist/cklb.go).
Tests check inventory, field types, dispositions, identifiers and official text
preservation. These are format and content checks, not a claim of validation
against DISA's JSON schema or an import test in STIG Viewer.
