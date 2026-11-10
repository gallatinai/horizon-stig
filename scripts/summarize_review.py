#!/usr/bin/env python3
"""Build concise review entry points from the authoritative rule list."""
import html,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'mpn/review/suggested-statuses.json').read_text())
counts=Counter(r['status'] for r in rows)
work=defaultdict(list)
for r in rows:
 if r['status']=='Needs work':work[r['task'] or 'unassigned'].append(r)
assert 'unassigned' not in work
lines=['# Suggested workstreams','','Repeated requirements are grouped here; each linked benchmark table has the full justification and evidence. Each action identifies the configuration, implementation or tailoring needed.','','| Workstream | Needs-work rules | First action |','|---|---:|---|']
for task,group in sorted(work.items()):
 lines.append(f"| {task} | {len(group)} | {group[0]['next_step']} |")
(ROOT/'mpn/review/workstreams.md').write_text('\n'.join(lines)+'\n')
(ROOT/'mpn/review/workstreams.json').write_text(json.dumps({t:[{'vuln_id':r['vuln_id'],'benchmark':r['benchmark'],'next_step':r['next_step']} for r in g] for t,g in sorted(work.items())},indent=2)+'\n')
unknown=[r for r in rows if r['status']=='Unclear']
benchmarks={p['package']:p for p in json.loads((ROOT/'mpn/benchmarks/manifest.json').read_text())}
lines=['# Remaining evidence decisions','','Each decision includes the exact STIG/SRG requirement and official check that establish the evidence needed.','','[Implementation plans and operating procedures](../EVIDENCE-ACTIONS.md) cover configuration and record-completion actions.','']
for r in unknown:
 package=benchmarks[r['benchmark']]
 lines += [f"## {r['vuln_id']} — {r['version']}",'',
           f"**Benchmark:** {package['title']} — {r['benchmark'].removeprefix('U_').replace('_',' ')} ([official XCCDF](../benchmarks/{r['benchmark']}/benchmark.xml)).",'',
           f"**Requirement:** {r['title']}",'',
           f"**Decision / action needed:** {r['next_step']}",'',
           f"**Reason:** {r['justification']}",'',
           '<details>',f"<summary>Official check — {r['rule_id']}</summary>",'']
 lines += [('> '+html.escape(line.rstrip(),quote=False)).rstrip() for line in r['check'].splitlines()]
 lines += ['','</details>','']
(ROOT/'mpn/review/remaining-evidence.md').write_text('\n'.join(lines).rstrip()+'\n')
lines=['# Horizon STIG tracking','','Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection. Gallatin manages this UDS Core deployment on MPN, which will process classified data.','','| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |','|---|---:|---:|---:|---:|---:|---:|']
for name in dict.fromkeys(r['benchmark'] for r in rows):
 group=[r for r in rows if r['benchmark']==name];c=Counter(r['status'] for r in group)
 lines.append(f"| [{name.removeprefix('U_')}](mpn/review/{name}.md) | {len(group)} | {c['Needs work']} | {c['Likely covered']} | {c['Unclear']} | {c['Needs N/A justification']} | {c['Compliant']} |")
lines += ['',f"**Totals:** {counts['Needs work']} Needs work; {counts['Likely covered']} Likely covered; {counts['Unclear']} Unclear; {counts['Needs N/A justification']} Needs N/A justification; {counts['Compliant']} source-only Compliant.",'',f"The {counts['Needs work']} needs-work recommendations group into **{len(work)} shared workstreams**. Every rule has a suggested status, justification, evidence links and next action. Final component checklists require acceptance of the stated evidence and applicability.",'','- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)','- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)',
'- [Implementation plans and operating procedures](mpn/EVIDENCE-ACTIONS.md)',
'- [Gallatin UDS configuration actions](mpn/UDS-CONFIGURATION.md)',
'- [NSA-approved cryptography: applying the STIG wording](mpn/NSA-CRYPTOGRAPHY.md) · [Checked components and protection options](mpn/NSA-COMPONENT-CHECK.md)',
'- [Assessment decisions](mpn/evidence/current-assessment.json)','- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)','- [Improvement priorities and effort estimate](mpn/FINDINGS.md)','- [Evidence boundaries and exact source versions](mpn/evidence/README.md)','- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)','','The package baseline is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Image SBOMs, FIPS configuration and release verification support the control mappings. Gallatin manages UDS Core on MPN and owns its platform configuration. Controls may be supplied by the gateway, mesh, IdP, database, host or organizational procedure. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.','','Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, `python3 scripts/generate_cklb.py`, then `python3 scripts/validate.py`. [current-assessment.json](mpn/evidence/current-assessment.json) stores the status decisions and evidence references. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required).']
lines += ['', '''## Updating a STIG in a PR

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
''']
(ROOT/'README.md').write_text('\n'.join(lines).rstrip()+'\n')
print(dict(counts));print('Needs-work streams:',len(work))

plans_path=ROOT/'mpn/evidence/implementation-plans.json'
if plans_path.exists():
 plans=json.loads(plans_path.read_text())
 lookup={r['vuln_id']:r for r in rows}
 solution_dir=ROOT/'mpn/solutions';solution_dir.mkdir(exist_ok=True)
 def cell(value):return str(value).replace('|','\\|').replace('\n',' ')
 index=['# Implementation plans and operating procedures','','Gallatin manages Horizon and UDS Core on MPN. These plans identify the configuration, operating procedure or mission decision needed for each requirement. A proposed action does not establish that it has been implemented or approved.','','| Rule | Requirement | Current status | Plan |','|---|---|---|---|']
 for group in plans['groups']:
  doc=[f"# {group['title']}",'','| STIG/SRG rule | Requirement | Current status |','|---|---|---|']
  for key in group['rules']:
   row=lookup[key];label=key+' / '+row['version']
   index.append('| '+' | '.join([f"[{cell(label)}](review/{row['benchmark']}.md)",cell(row['title']),row['status'],f"[{group['title']}](solutions/{group['id']}.md)"])+' |')
   doc.append('| '+' | '.join([f"[{cell(label)}](../review/{row['benchmark']}.md)",cell(row['title']),row['status']])+' |')
  doc+=['',group['content'],'','## Source references','']
  catalog=json.loads((ROOT/'mpn/evidence/catalog.json').read_text())
  for key in group.get('source_ids',[]):doc.append(f"- [{key}]({catalog[key]['url']})")
  doc.append('')
  (solution_dir/(group['id']+'.md')).write_text('\n'.join(doc).rstrip()+'\n')
 index+=['','## Record templates','','Complete and retain records in the appropriate restricted company/mission system. The files below contain field names only.','','- [Account and repository access certification](templates/access-certification.csv)','- [Audit review record](templates/audit-review-record.csv)','- [PPSM interface and authorization register](templates/ppsm-interface-register.csv)','- [Role-specific secure-development training](templates/secure-development-training.csv)','- [Mission data, PII and protection mapping](templates/mission-data-protection.csv)','']
 (ROOT/'mpn/EVIDENCE-ACTIONS.md').write_text('\n'.join(index).rstrip()+'\n')
