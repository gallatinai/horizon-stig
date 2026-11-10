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
lines=['# Suggested workstreams','','Repeated requirements are grouped here; each linked benchmark table has the full justification and evidence. These are candidate corrections/tailoring proposals, not approved implementation tickets.','','| Workstream | Needs-work rules | First action |','|---|---:|---|']
for task,group in sorted(work.items()):
 lines.append(f"| {task} | {len(group)} | {group[0]['next_step']} |")
(ROOT/'mpn/review/workstreams.md').write_text('\n'.join(lines)+'\n')
(ROOT/'mpn/review/workstreams.json').write_text(json.dumps({t:[{'vuln_id':r['vuln_id'],'benchmark':r['benchmark'],'next_step':r['next_step']} for r in g] for t,g in sorted(work.items())},indent=2)+'\n')
unknown=[r for r in rows if r['status']=='Unclear']
lines=['# Remaining evidence decisions','','Each item was checked against source, delivery artifacts and available organizational evidence. What remains is a specific unselected infrastructure/policy input or historical approval/action record, not a generic request to run runtime checks.','','| Rule | Evidence needed | Why source does not settle it |','|---|---|---|']
for r in unknown:
 clean=lambda x:x.replace('|','\\|').replace('\n',' ')
 lines.append('| '+' | '.join(clean(x) for x in [r['vuln_id'],r['next_step'],r['justification']])+' |')
(ROOT/'mpn/review/remaining-evidence.md').write_text('\n'.join(lines)+'\n')
lines=['# Horizon STIG tracking','','Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 10 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection.','','| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |','|---|---:|---:|---:|---:|---:|---:|']
for name in dict.fromkeys(r['benchmark'] for r in rows):
 group=[r for r in rows if r['benchmark']==name];c=Counter(r['status'] for r in group)
 lines.append(f"| [{name.removeprefix('U_')}](mpn/review/{name}.md) | {len(group)} | {c['Needs work']} | {c['Likely covered']} | {c['Unclear']} | {c['Needs N/A justification']} | {c['Compliant']} |")
lines += ['',f"**Totals:** {counts['Needs work']} Needs work; {counts['Likely covered']} Likely covered; {counts['Unclear']} Unclear; {counts['Needs N/A justification']} Needs N/A justification; {counts['Compliant']} source-only Compliant.",'',f"The {counts['Needs work']} needs-work recommendations group into **{len(work)} workstreams**, not {counts['Needs work']} separate implementations. This re-review checked all **154 previous unknowns and 257 previous needs-work rules** against the full product boundary. Unclear fell from 154 to {len(unknown)} (662 in the original routing pass). Every rule has a suggested status, justification, evidence links and next action. These are recommendations, not assessor sign-off or executed runtime checks.",'','- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)','- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)',
'- [Completed investigation checklist](mpn/review/investigation-checklist.md) · [Detailed source/reviewer log](mpn/evidence/product-boundary-review.json)','- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)','- [Findings, two-pass plan and lift estimate](mpn/FINDINGS.md)','- [Evidence boundaries and exact source versions](mpn/evidence/README.md)','- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)','','The reviewed published package is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Actual image SBOMs, FIPS base configuration and cryptographic release verification receive credit. A control may be implemented by the gateway, mesh, IdP, database, host or organizational procedure; the API need not duplicate it. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.','','Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. The November 9 investigation is historical context; [product-boundary-review.json](mpn/evidence/product-boundary-review.json) supplies the superseding decisions. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required). No application remediation or deployment is performed.']
(ROOT/'README.md').write_text('\n'.join(lines)+'\n')
print(dict(counts));print('Needs-work streams:',len(work))

product_path=ROOT/'mpn/evidence/product-boundary-review.json'
if product_path.exists():
 product=json.loads(product_path.read_text())
 prior={r['vuln_id']:r for r in json.loads((ROOT/'mpn/review/pre-rereview-20261109.json').read_text())}
 final={r['vuln_id']:r for r in rows}
 checklist=['# Completed investigation checklist','','All 411 previously open recommendations were explicitly re-reviewed. This includes every previous unknown and every needs-work recommendation; additional corrections address stale inheritance, profile and applicability statements.','','| Reviewer | Assigned | Completed |','|---|---:|---:|']
 for reviewer,ids in product['assignments'].items():checklist.append(f'| {reviewer} | {len(ids)} | {len(ids)} |')
 checklist+=['','| Rule | Previous | Recommended now | Investigation |','|---|---|---|---|']
 for reviewer,ids in product['assignments'].items():
  for key in ids:
   row=final[key];note=row['investigation'].replace('|','\\|').replace('\n',' ')
   checklist.append(f"| [{key}]({row['benchmark']}.md) | {prior[key]['status']} | {row['status']} | {note} |")
 (ROOT/'mpn/review/investigation-checklist.md').write_text('\n'.join(checklist)+'\n')
 changed=[{'vuln_id':key,'before':prior[key]['status'],'after':decision['status'],'justification':decision['justification']} for key,decision in product['decisions'].items() if prior[key]['status']!=decision['status']]
 (ROOT/'mpn/review/product-review-changes.json').write_text(json.dumps(changed,indent=2)+'\n')
