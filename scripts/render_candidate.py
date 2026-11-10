#!/usr/bin/env python3
"""Capture candidate Helm manifests without deployment or live credentials.
Requires Helm and PyYAML. Argument: bundle checkout at recorded commit.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('checkout',type=Path)
parser.add_argument('--source-path',action='store_true')
parser.add_argument('--output',required=True)
args=parser.parse_args()
src=args.checkout.resolve() if args.source_path else args.checkout.resolve()/'source'
out=ROOT/args.output;out.mkdir(exist_ok=True)
entries=[];summary=[]
for component in yaml.safe_load((src/'zarf.yaml').read_text())['components']:
 for chart in component.get('charts',[]):
  command=['helm','template',chart['releaseName'],chart['localPath'],'-n',chart['namespace']]
  for value in chart.get('valuesFiles',[]):command+=['-f',value]
  # Zarf substitutes this default before Helm; it is not a credential or call.
  if component['name'] in {'horizon-chat-agent','horizon-artifact-ingestion'}:command+=['--set-string','llm.provider=openai']
  data=subprocess.check_output(command,cwd=src)
  path=out/(component['name']+'.yaml');path.write_bytes(data)
  entries.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'command':command,'cwd':'<pinned bundle>/source'})
  for doc in yaml.safe_load_all(data):
   if not isinstance(doc,dict):continue
   spec=doc.get('spec',{});template=spec.get('template',{})
   pod=template.get('spec',{})
   for kind in ['containers','initContainers']:
    for container in pod.get(kind,[]):
     summary.append({'component':component['name'],'workload':doc['metadata']['name'],'container':container['name'],'kind':kind,'namespace':doc['metadata'].get('namespace',chart['namespace']),'image':container.get('image'),'securityContext':container.get('securityContext',{}),'resources':container.get('resources',{}),'secret_env':[e['name'] for e in container.get('env',[]) if 'secretKeyRef' in e.get('valueFrom',{})]})
(out/'workload-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
m=ROOT/'mpn/evidence/rendered-manifest.json';manifest=json.loads(m.read_text());manifest['files']=[x for x in manifest['files'] if not x['path'].startswith(args.output+'/')]+entries;m.write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Captured {len(entries)} charts, {len(summary)} workload containers; placeholders only.')
