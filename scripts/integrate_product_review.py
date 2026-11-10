#!/usr/bin/env python3
"""Preserve and integrate completed, explicit product-boundary review decisions.
Input directory contains reviewer result files and the frozen assignment manifest.
"""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('results',type=Path);args=p.parse_args()
source=args.results
assigned=json.loads((source/'manifest.json').read_text())
prior=json.loads((ROOT/'mpn/review/pre-rereview-20261109.json').read_text())
assert {x['vuln_id'] for x in prior if x['status'] in {'Unclear','Needs work'}}=={v for batch in assigned.values() for v in batch}
facts={};decisions={};logs={};summaries={};reviewed={}
for reviewer,ids in assigned.items():
 result=json.loads((source/(reviewer+'-result.json')).read_text())
 got=[d['vuln_id'] for d in result['decisions']]
 assert len(got)==len(set(got)) and set(got)==set(ids),(reviewer,'incomplete assignment')
 reviewed[reviewer]=got
 for f in result['facts']:
  if f['id'] in facts:assert facts[f['id']]==f
  facts[f['id']]=f
 for d in result['decisions']+result.get('extra_decisions',[]):
  assert d['vuln_id'] not in decisions,('overlapping review',d['vuln_id'],reviewer)
  assert d['status'] in {'Compliant','Likely covered','Needs work','Needs N/A justification','Unclear'}
  assert all(d.get(k) for k in ['justification','evidence_ids','next_step','investigation'])
  if d['status']=='Needs work':assert d.get('task'),d['vuln_id']
  decisions[d['vuln_id']]={**d,'reviewer':reviewer,'evidence_state':'source-inferred'}
 logs[reviewer]=result.get('investigation_log',[]);summaries[reviewer]=result.get('summary','')
research=json.loads((source/'internaldocs-result.json').read_text())
for f in research['facts']:facts[f['id']]=f
logs['internaldocs']=research['investigation_log'];summaries['internaldocs']=research['summary']
known=set(json.loads((ROOT/'mpn/evidence/catalog.json').read_text()))|set(facts)
for v,d in decisions.items():assert set(d['evidence_ids'])<=known,(v,set(d['evidence_ids'])-known)
verification=json.loads((source/'independent-verification.json').read_text())
release=json.loads((ROOT/'mpn/evidence/delivered-release/build-info.json').read_text())
output={'date':'2026-11-10','method':'Exact official checks reviewed against the delivered package/profile, application source, upstream products and connected organizational sources. Recommended product-boundary disposition; no new deployment or formal assessor acceptance claimed.','baseline':{'version':release['version'],'horizon_commit':release['horizonCommit'],'package_commit':release['packageCommit'],'identity':release['platformContract']['identity'],'image_count':len(release['images']),'release_run':'https://github.com/gallatinai/horizon-uds-bundle/actions/runs/42114745685'},'assignments':reviewed,'facts':facts,'decisions':decisions,'investigation_logs':logs,'reviewer_summaries':summaries,'independent_verification':verification}
(ROOT/'mpn/evidence/product-boundary-review.json').write_text(json.dumps(output,indent=2)+'\n')
print(f'Integrated all {sum(len(x) for x in reviewed.values())} originally open rules, {len(decisions)} total explicit re-review decisions and {len(facts)} facts.')
