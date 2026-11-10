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
'- [Assessment decisions](mpn/evidence/current-assessment.json)','- [Requirements found in Slack and Gemini meeting notes](mpn/REQUIREMENTS.md)','- [Improvement priorities and effort estimate](mpn/FINDINGS.md)','- [Evidence boundaries and exact source versions](mpn/evidence/README.md)','- [John’s human-review queue](mpn/review/human-review.csv) · [Official packages and hashes](mpn/benchmarks/manifest.json)','','The package baseline is **2026.45.4-uds.1**, from the successful UDS push pipeline: **UDS shared identity, Core 1.14.0, 12 digest-pinned images, no bundled Keycloak**. Image SBOMs, FIPS configuration and release verification support the control mappings. Gallatin manages UDS Core on MPN and owns its platform configuration. Controls may be supplied by the gateway, mesh, IdP, database, host or organizational procedure. MPN-specific local inference, selected host/storage and mission applicability remain distinct from the generic UDS release.','','Rebuild saved decisions with `python3 scripts/build_review.py`, `python3 scripts/summarize_review.py`, then `python3 scripts/validate.py`. [current-assessment.json](mpn/evidence/current-assessment.json) stores the status decisions and evidence references. `python3 scripts/render_delivered.py <pinned-bundle-checkout>` reproduces the 12 delivered-profile chart captures from saved release metadata (Helm and PyYAML required).']
(ROOT/'README.md').write_text('\n'.join(lines)+'\n')
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
