#!/usr/bin/env python3
"""Build provisional rule lists. Routing is explicit and never grants compliance."""
import csv, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BENCH=ROOT/'mpn/benchmarks'
OUT=ROOT/'mpn/review'
H='3f3b51d454197c077b33896caf93de72b94eafda'
U='d528b7febf1ce8bb5ccf99661dade6ae09a84381'
SCOPE='https://gallatin.atlassian.net/wiki/spaces/GG/pages/733085804/WIP+STIG+SRG+Compliance+Scope+MPN'
COMPONENTS={
'U_ASD_V6R5_STIG':'Navigator application; UDS Core inheritance boundary must be established',
'U_Kubernetes_V2R6_STIG':'MPN cluster and nodes; Gallatin horizon-uds workloads',
'U_Container_Platform_V2R5_SRG':'UDS platform: registry, runtime, Pepr, Istio, logging; delivered workloads',
'U_Web_Server_V4R5_SRG':'Istio tenant gateway and frontend nginx (evaluate separately)',
'U_Application_Server_V4R6_SRG':'Navigator API, workers, chat, ingestion; SeaweedFS; model-serving runtime (evaluate separately)',
'U_Database_V4R6_SRG':'In-cluster PostgreSQL, including application and identity databases',
'U_AAA_Services_V2R3_SRG':'Selected Keycloak/Authservice path; bundled Keycloak is current candidate default',
}
E={
'host':('MPN ownership','Current scope assigns control plane/node OS to MPN; no host assessment or live configuration was supplied.',SCOPE),
'uds':('UDS architecture','Current scope names Pepr, Istio, Falco, Velero and centralized logging; architecture supplies a mechanism, not observed enforcement.',SCOPE),
'identity':('Identity selection',"The active package chart supports bundled or UDS identity; source/values/uds-package.yaml selects bundled by default. UDS SSO cannot be assumed for this path.",f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/values/uds-package.yaml'),
'realm':('Bundled realm','Realm defaults: failureFactor=5, permanentLockout=false, idle=900s, max=28800s, password policy includes hashing only, events/admin events enabled with 90-day local event retention.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/charts/keycloak/realms/horizon-realm.json'),
'mesh':('Mesh and policy','Package chart declares ambient mesh and generated network policy. Disabled chart-local NetworkPolicy and plaintext application URLs do not establish missing mesh enforcement.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/charts/horizon-uds-package/templates/package.yaml'),
'logging':('API logging','Current HTTP logger includes service, request/trace IDs, event, remote address and response status, with secret redaction. Its common bindings do not add authenticated actor identity; other records/correlation must be checked.',f'https://github.com/gallatinai/horizon/blob/{H}/apps/api/src/core/observability/logging.ts'),
'db':('Database audit','Candidate PostgreSQL preloads pgaudit; migration creates extension but catches failures. This does not establish effective event classes, connection logging, retention, or collection.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/values/postgres.yaml'),
'secrets':('Secret environment variables','Rendered PostgreSQL StatefulSet injects POSTGRES_PASSWORD via secretKeyRef; secret-as-environment is expressly disallowed by Kubernetes V-242415.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/charts/horizon-postgres/templates/statefulset.yaml'),
's3':('SeaweedFS credential ConfigMap','Rendered SeaweedFS chart places S3 accessKey/secretKey in s3.json in a ConfigMap and mounts that ConfigMap. Zarf supplies secrets at deployment; stored candidate placeholders are not actual leaked credentials.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/charts/seaweedfs/templates/configmap.yaml'),
'web':('Frontend nginx','Frontend config serves a SPA with try_files; ingress security, complete image config, effective HTTP versions, headers and enabled modules remain unobserved.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/values/web.yaml'),
'logout':('Browser logout','Current auth store wipes local auth state then invokes OIDC signout. Local storage use alone is not proof that logout fails; replay/expiry/server-side invalidation need tests.',f'https://github.com/gallatinai/horizon/blob/{H}/apps/web/src/auth/auth-store.ts'),
'authz':('Application access control','API guard validates identity and sets tenant/user context; permission guard invokes a permission enforcer when route metadata is present. This is source support, not complete route/tenant coverage.',f'https://github.com/gallatinai/horizon/blob/{H}/apps/api/src/api/auth/auth.guard.ts'),
'images':('Image release process','Builder verifies source digests and produces archive hashes; sample values with empty digests do not establish that a built release is unpinned. Assessed release/SBOM/scans still needed.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/scripts/build-bundle.py'),
'local':('MPN inference mismatch','The MPN notes require local inference. Candidate package still permits Anywhere:443 egress for hosted LLM consumers; it is a demo/general candidate, not proof of deployed MPN behavior.',f'https://github.com/gallatinai/horizon-uds-bundle/blob/{U}/source/charts/horizon-uds-package/templates/package.yaml'),
}

def base(r):
 b=r['benchmark']; t=r['title'].lower();v=r['vuln_id']; component=COMPONENTS[b]
 status='Unclear';owner='Gallatin SRE / component owner';evidence='uds'
 why='No component-specific assessment evidence establishes this requirement in the selected MPN release.'
 next_step='Apply the complete official check below to each listed component; retain effective settings and observed results.'
 category='component verification'
 if b=='U_ASD_V6R5_STIG':
  status='Likely covered';evidence='uds';category='inheritance'
  why='Nov 6 scope asserts ASD coverage through UDS Core. Accept only the exact documented inherited scope; Horizon-specific residual requirements remain to be tested.'
  next_step='Obtain UDS ASD attestation and boundary/version mapping; review residual Horizon applicability using the preserved October worksheet.'
 elif b=='U_Kubernetes_V2R6_STIG':
  status='Likely covered';owner='MPN/GDIT platform owner; Gallatin for workload residuals';evidence='host';category='inheritance'
  why='MPN owns the cluster/control plane/nodes in the current scope; this rule needs inherited host evidence rather than an application-code fix.'
  next_step='Obtain the matching MPN cluster checklist and effective setting for this exact rule; retain Gallatin workload residuals.'
  if v in {'V-242381','V-242383','V-242414','V-242415','V-242417','V-242437','V-245544','V-254800','V-254801','V-274883','V-274884'}:
   status='Unclear';owner='Gallatin SRE with MPN platform owner';evidence='mesh';category='workload verification'
   why='This rule has workload or shared responsibility; MPN cluster ownership does not establish compliance for Horizon manifests and admitted pods.'
   next_step='Review rendered workloads and actual admitted pods/RBAC against the official check; include UDS admission mutations/exemptions.'
 else:
  # These categories route evidence requests; they never certify a result.
  if re.search(r'audit|log record|log information|log tools|logging|logged|loggable|logable',t):
   category='audit evidence';evidence='db' if 'Database' in b else ('realm' if 'AAA_' in b else 'logging')
   why='A logging mechanism exists, but the required event/content, collection, protection or operational evidence for this particular rule is not established.'
   next_step='Execute this rule\'s check with representative successful and denied actions; inspect the final protected audit destination and approved event/retention policy.'
  elif re.search(r'password|authenticator|authentication|authenticate|certificate|pki|piv|cac|account|identifier',t):
   category='identity evidence';evidence='identity'
   why='Coverage depends on the effective identity path and account type. The candidate defaults to bundled Keycloak, so platform SSO coverage is not sufficient evidence.'
   if 'Database' in b:
    evidence='db';why='Database native/service accounts and administrator access need their own effective authentication and role evidence; web SSO does not establish this DBMS requirement.'
   if 'Container' in b:
    evidence='uds';why='Platform registry/runtime identity and Horizon application identity are separate scopes; obtain the operator\'s effective platform identity controls for this rule.'
   next_step='Identify each relevant user/admin/service-account path and apply the official conditional check; retain inherited provider evidence where applicable.'
  elif re.search(r'session|logout|logoff|cookie',t):
   category='session evidence';evidence='logout'
   why='Source provides OIDC session/logout mechanisms, but required limits and end-to-end termination behavior have not been demonstrated for this component.'
   next_step='Test the official timeout/logout/session condition on the effective user and administrator paths, including old-token reuse.'
  elif re.search(r'cryptograph|encrypt|cipher|transmi|tls|ssl|confidentiality|integrity',t):
   category='crypto evidence';evidence='mesh'
   why='Ambient mesh and hardened-image intent provide possible coverage; declarations and FIPS-labelled images do not establish validated operation on this specific path or storage layer.'
   next_step='Identify termination points and storage/key owner; capture effective protection, module/version/approved mode, trust and relevant official-check results.'
  elif re.search(r'backup|recover|revert|failure|known safe|secure state|clustering|availability',t):
   category='recovery evidence';evidence='uds'
   why='UDS/Velero and persistent storage are named in the design, but this component\'s recovery policy and a successful relevant failure/restore test are absent.'
   next_step='Obtain component-specific backup/failover configuration and an observed restore/failure test; determine any official applicability condition.'
  elif re.search(r'privilege|access control|authoriz|rbac|role-based|attribute-based',t):
   category='access evidence';evidence='authz' if 'Application' in b else 'uds'
   why='Source/design supplies access-control mechanisms; role assignments, policy coverage and denied-operation tests for this exact requirement are missing.'
   next_step='Inspect effective roles and policy scope and demonstrate allowed/denied operations, including admin and cross-tenant paths where applicable.'
  elif re.search(r'image|patch|update|software|vendor|version supported|signature|signed',t):
   category='release evidence';evidence='images'
   why='Release tooling supplies provenance mechanisms; the selected MPN artifact, scan results, approval records and update process must be linked to this requirement.'
   next_step='Bind this check to the delivered image digests/SBOM/scans and release approval evidence; do not infer a missing control from example tags.'
  elif re.search(r'time stamp|clock|ntp|time source',t):
   category='host time evidence';evidence='host';owner='MPN time-service owner with Gallatin SRE'
   why='Containers depend on host time; no inherited time synchronization/precision evidence was captured for this requirement.'
   next_step='Obtain MPN time-service settings and observed component timestamps matching the official check.'
  elif 'Web_Server' in b:
   evidence='web';category='web configuration evidence'
   why='The frontend SPA config is available, but gateway and nginx image/runtime settings do not establish this requirement for both components.'
   next_step='Apply the official check separately to tenant gateway and frontend nginx; record delegation/applicability and effective configuration.'
 if b=='U_AAA_Services_V2R3_SRG' and (('802.1x' in t) or v in {'V-204701','V-204703'}):
  status='Needs N/A justification';category='applicability';evidence='identity'
  why='The selected Navigator identity design is OIDC/Keycloak, not an 802.1x/RADIUS/TACACS+ network-access deployment. This is a candidate scope exclusion, not an accepted N/A.'
  next_step='Confirm no delivered AAA component performs the function in the official check; retain architecture evidence and assessor-approved rationale, or reassess it.'
 if b=='U_Application_Server_V4R6_SRG' and v=='V-204749':
  status='Needs N/A justification';category='applicability';evidence='authz'
  why='The identified API uses HTTP/OIDC rather than a demonstrated SOAP security endpoint. SOAP/WS-Security applicability must be confirmed for every delivered service.'
  next_step='Inventory actual exposed protocols/connectors for all services and obtain acceptance of a supported non-SOAP rationale.'
 if b=='U_Application_Server_V4R6_SRG' and v=='V-204814':
  status='Needs N/A justification';category='applicability';evidence='uds'
  why='The official title conditions HA clustering on MAC I; the MPN designation and required HA topology are not established. Single replica alone is not a confirmed failure.'
  next_step='Obtain the designated mission category/HA requirement; justify exclusion only if supported, otherwise assess failover and topology.'
 return dict(status=status,justification=why,evidence_ids=[evidence],next_step=next_step,owner=owner,category=category,components=component)

# Exact, source-supported recommendations. These apply to the reviewed candidate,
# not a claim about a running MPN deployment. One task can cover multiple rules.
OVERRIDES={
'V-242415':dict(status='Needs work',justification='Rendered PostgreSQL injects POSTGRES_PASSWORD through secretKeyRef into an environment variable. The official check explicitly treats this pattern as a finding. This is a candidate-manifest gap, not a live-cluster finding.',evidence_ids=['secrets'],next_step='Move credentials to protected mounted files/vault-supported delivery and adapt consumers; rerender and verify admitted pods. Review with John before implementation.',category='code/config',task='secret-delivery'),
'V-274883':dict(status='Needs work',justification='SeaweedFS renders accessKey and secretKey inside s3.json in a ConfigMap. The official rule requires sensitive values in Secrets or an approved external store. S3 authentication already exists; credential placement is the gap.',evidence_ids=['s3'],next_step='Render S3 credential configuration as a Secret or approved external-store mount, restrict access, and verify deployment with substituted test credentials. Review with John.',category='code/config',task='secret-delivery'),
'V-204644':dict(status='Needs work',justification='Bundled Keycloak realm sets failureFactor=5; the official AAA check requires locking after three consecutive failures within 15 minutes. Bundled mode/local users are the candidate default. UDS SSO inheritance does not fix this realm.',evidence_ids=['identity','realm'],next_step='Choose the MPN identity path. For bundled local accounts, configure and demonstrate the required threshold/window; if delegated, obtain directory evidence and supported rule-specific applicability.',category='code/config',task='identity-policy'),
'V-204689':dict(status='Needs work',justification='Bundled Keycloak realm has permanentLockout=false, while the official AAA check requires locks maintained until administrator release when accounts are managed locally.',evidence_ids=['identity','realm'],next_step='Set and test administrator-release lockout for applicable local accounts, or document the selected directory delegation with its corresponding evidence.',category='code/config',task='identity-policy'),
}
# Local-password policy checks have an explicit exception for directory management.
for v in ['V-204664','V-204666','V-204667','V-204668','V-204669','V-204673','V-204674']:
 OVERRIDES[v]=dict(status='Needs work',justification='Candidate bundled Keycloak uses local users and its explicit passwordPolicy specifies only hash algorithm/iterations; it lacks the length, character-class or lifetime constraint required by this exact rule. An inherited directory exception has not been established.',evidence_ids=['identity','realm'],next_step='Agree the MPN identity model; encode and demonstrate this rule\'s exact constraint for applicable local accounts, or retain accepted directory delegation evidence.',category='code/config',task='identity-policy')

def write_rows(path, rows):
 path.write_text(json.dumps(rows,indent=2)+'\n')
 with path.with_suffix('.csv').open('w',newline='') as f:
  fields=['benchmark','vuln_id','rule_id','version','severity','title','components','status','justification','evidence','next_step','owner','category','human_review','task','evidence_state','investigation']
  writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(rows)

def main():
 investigation=ROOT/'mpn/evidence/source-investigation.json'
 if investigation.exists():
  saved=json.loads(investigation.read_text())
  for k,f in saved['facts'].items():E[k]=(k,f['observation'],f['url'])
  # Explicit caller decisions win when refreshing the investigation.
  for k,v in saved['explicit_rule_decisions'].items():OVERRIDES.setdefault(k,v)
 history=json.loads((ROOT/'mpn/evidence/asd-october-review.json').read_text())
 first=[];second=[]
 for package in json.loads((BENCH/'manifest.json').read_text()):
  name=package['package'];rules=json.loads((BENCH/name/'rules.json').read_text());final=[]
  for r in rules:
   initial={**r,**base(r)}
   initial['review_method']='Automated evidence routing followed by exact-rule source review where recorded; no runtime assessment.'
   if name=='U_ASD_V6R5_STIG':
    initial['historical_review_reference']='../evidence/asd-october-review.json#'+r['vuln_id']
    initial['historical_review_warning']='October source snapshots only; not current-release validation and not a formal compliance result.'
   row=dict(initial)
   if r['vuln_id'] in OVERRIDES:row.update(OVERRIDES[r['vuln_id']])
   # Second pass corrections prevent blanket inherited/authentication passes.
   if name=='U_Kubernetes_V2R6_STIG' and r['vuln_id']=='V-242383' and r['vuln_id'] not in OVERRIDES:
    row.update(status='Likely covered',justification='Zarf chart declarations target horizon-uds and an explicit namespace manifest exists. Likely source coverage; inventory actual admitted resources to exclude default-namespace exceptions.',evidence_ids=['mesh'],next_step='Capture actual workload namespaces and check all user-managed resources per the official check.',category='workload verification')
   if name=='U_ASD_V6R5_STIG':
    row['justification']+=' The existing October per-rule evidence/test notes are preserved as historical context only.'
   for entry in [initial,row]:
    entry['evidence']='; '.join(E[k][2] for k in entry['evidence_ids'])
    entry['human_review']=entry['status'] in ['Needs work','Unclear']
    entry.setdefault('task','')
   row['second_pass_note']='Official rule compared with the cited pinned source/configuration or explicit applicability evidence; no live test claimed.' if r['vuln_id'] in OVERRIDES else 'Conservative evidence/applicability review; unresolved operational checks remain explicit.'
   first.append(initial);second.append(row);final.append(row)
  title=package['title']
  lines=[f'# {title}: suggested statuses','', 'Provisional recommendations for the identified candidate/source snapshots. No live MPN assessment or formal sign-off. Evaluate each component listed separately before final checklists.','', '| Rule | Requirement | Suggested status | Justification | Evidence / next step |','|---|---|---|---|---|']
  def clean(s):return str(s).replace('|','\\|').replace('\n',' ')
  for r in final:
   evidence=' '.join(f'[{k}]({E[k][2]})' for k in r['evidence_ids'])
   lines.append('| '+' | '.join(clean(s) for s in [r['vuln_id']+' / '+r['version'],r['title'],r['status'],r['justification'],evidence+' '+r['next_step']])+' |')
  (OUT/(name+'.md')).write_text('\n'.join(lines)+'\n')
 write_rows(OUT/'pass-1.json',first);write_rows(OUT/'suggested-statuses.json',second)
 write_rows(OUT/'human-review.json',[r for r in second if r['human_review']])
 changes=[dict(benchmark=a['benchmark'],vuln_id=a['vuln_id'],before=a['status'],after=b['status'],reason=b['justification']) for a,b in zip(first,second) if a['status']!=b['status']]
 (OUT/'second-pass-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 counts={p['package']:dict(Counter(r['status'] for r in second if r['benchmark']==p['package'])) for p in json.loads((BENCH/'manifest.json').read_text())}
 (OUT/'counts.json').write_text(json.dumps(dict(total=len(second),by_status=dict(Counter(r['status'] for r in second)),by_benchmark=counts),indent=2)+'\n')
 (ROOT/'mpn/evidence/catalog.json').write_text(json.dumps({k:dict(title=v[0],observation=v[1],url=v[2]) for k,v in E.items()},indent=2)+'\n')
 print(json.dumps(dict(total=len(second),statuses=dict(Counter(r['status'] for r in second)),candidate_tasks=sorted({r['task'] for r in second if r['task']})),indent=2))
if __name__=='__main__':main()
