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
lines=['# Remaining evidence decisions','','Each remaining item has an investigated evidence boundary. Source can establish mechanisms/defaults; it cannot establish an approval, execution record or an unspecified deployment choice. No live MPN official tests were run.','','| Rule | Evidence needed | Why source does not settle it |','|---|---|---|']
for r in unknown:
 clean=lambda x:x.replace('|','\\|').replace('\n',' ')
 lines.append('| '+' | '.join(clean(x) for x in [r['vuln_id'],r['next_step'],r['justification']])+' |')
(ROOT/'mpn/review/remaining-evidence.md').write_text('\n'.join(lines)+'\n')
lines=['# Horizon STIG tracking','','Suggested statuses and reasons for all **1,048 rules across seven benchmarks**, updated 9 November 2026. The OS benchmark is an eighth family pending MPN distribution/version selection.','','| Benchmark | Rules | Needs work | Likely covered | Unclear | N/A justification | Source-only Compliant |','|---|---:|---:|---:|---:|---:|---:|']
for name in dict.fromkeys(r['benchmark'] for r in rows):
 group=[r for r in rows if r['benchmark']==name];c=Counter(r['status'] for r in group)
 lines.append(f"| [{name.removeprefix('U_')}](mpn/review/{name}.md) | {len(group)} | {c['Needs work']} | {c['Likely covered']} | {c['Unclear']} | {c['Needs N/A justification']} | {c['Compliant']} |")
lines += ['',f"**Totals:** {counts['Needs work']} Needs work; {counts['Likely covered']} Likely covered; {counts['Unclear']} Unclear; {counts['Needs N/A justification']} Needs N/A justification; {counts['Compliant']} source-only Compliant.",'',f"The {counts['Needs work']} needs-work recommendations group into **{len(work)} workstreams**, not {counts['Needs work']} separate implementations. Unclear fell from 662 to {len(unknown)} after source investigation. Every rule has a suggested status, justification, evidence links and next action. These are recommendations, not assessor sign-off or executed runtime checks.",'','- [All rules and reasons (CSV)](mpn/review/suggested-statuses.csv) · [JSON with complete official check/fix](mpn/review/suggested-statuses.json)','- [Suggested workstreams](mpn/review/workstreams.md) · [Remaining evidence decisions](mpn/review/remaining-evidence.md)','- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)','- [Findings, two-pass plan and lift estimate](mpn/FINDINGS.md)','- [Evidence boundaries and exact source versions](mpn/evidence/README.md)','- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)','','UDS Core **1.14.0** was inspected at the candidate’s pinned baseline, including Pepr, Istio, identity, logging, monitoring, backups and hardened offerings. Horizon’s candidate selects **its own bundled Keycloak**; platform identity defaults do not automatically apply to it. Hardened/FIPS platform recommendations depend on the actual supported flavor. The selected MPN release, image/module certificates, host inheritance and operational approval/test records remain external inputs.','','Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. The deeper decision log is preserved in [source-investigation.json](mpn/evidence/source-investigation.json). `scripts/investigate.py` refreshes it against the pinned local source snapshots; `scripts/render_candidate.py <bundle-checkout>` reproduces the 13 candidate chart captures (Helm and PyYAML required). No application remediation or deployment is performed.']
(ROOT/'README.md').write_text('\n'.join(lines)+'\n')
print(dict(counts));print('Needs-work streams:',len(work))
