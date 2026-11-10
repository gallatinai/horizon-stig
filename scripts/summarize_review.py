#!/usr/bin/env python3
"""Build concise review entry points from the authoritative rule list."""
import json
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
lines=['# Remaining evidence decisions','','Resolve the listed infrastructure selections, policy decisions and approval records to determine these requirements.','','| Rule | Evidence needed | Why source does not settle it |','|---|---|---|']
for r in unknown:
 clean=lambda x:x.replace('|','\\|').replace('\n',' ')
 lines.append('| '+' | '.join(clean(x) for x in [r['vuln_id'],r['next_step'],r['justification']])+' |')
(ROOT/'mpn/review/remaining-evidence.md').write_text('\n'.join(lines)+'\n')
lines=['# Horizon STIG tracking','','Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection. Gallatin manages this UDS Core deployment on MPN.','','| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |','|---|---:|---:|---:|---:|---:|---:|']
for name in dict.fromkeys(r['benchmark'] for r in rows):
 group=[r for r in rows if r['benchmark']==name];c=Counter(r['status'] for r in group)
 lines.append(f"| [{name.removeprefix('U_')}](mpn/review/{name}.md) | {len(group)} | {c['Needs work']} | {c['Likely covered']} | {c['Unclear']} | {c['Needs N/A justification']} | {c['Compliant']} |")
lines += ['',f"**Totals:** {counts['Needs work']} Needs work; {counts['Likely covered']} Likely covered; {counts['Unclear']} Unclear; {counts['Needs N/A justification']} Needs N/A justification; {counts['Compliant']} source-only Compliant.",'',f"The {counts['Needs work']} needs-work recommendations group into **{len(work)} shared workstreams**. Every rule has a suggested status, justification, evidence links and next action. Final component checklists require acceptance of the stated evidence and applicability.",'','- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)','- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)',
'- [Gallatin UDS configuration actions](mpn/UDS-CONFIGURATION.md)',
'- [Assessment decisions](mpn/evidence/current-assessment.json)','- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)','- [Improvement priorities and effort estimate](mpn/FINDINGS.md)','- [Evidence boundaries and exact source versions](mpn/evidence/README.md)','- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)','','The package baseline is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Image SBOMs, FIPS configuration and release verification support the control mappings. Gallatin manages UDS Core on MPN and owns its platform configuration. Controls may be supplied by the gateway, mesh, IdP, database, host or organizational procedure. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.','','Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. [current-assessment.json](mpn/evidence/current-assessment.json) stores the status decisions and evidence references. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required).']
(ROOT/'README.md').write_text('\n'.join(lines)+'\n')
print(dict(counts));print('Needs-work streams:',len(work))
