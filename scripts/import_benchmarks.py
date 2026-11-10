#!/usr/bin/env python3
"""Preserve the requested DISA packages and normalize their complete rule text."""
import hashlib, io, json, urllib.request, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
N = {'x':'http://checklists.nist.gov/xccdf/1.1'}
PACKAGES = ['U_ASD_V6R5_STIG','U_Kubernetes_V2R6_STIG','U_Container_Platform_V2R5_SRG','U_Web_Server_V4R5_SRG','U_Application_Server_V4R6_SRG','U_Database_V4R6_SRG','U_AAA_Services_V2R3_SRG']
def txt(el, name):
 e=el.find('x:'+name,N)
 return ''.join(e.itertext()).strip() if e is not None else ''
def main():
 manifest=[]
 for name in PACKAGES:
  p=ROOT/'mpn/benchmarks'/name;p.mkdir(parents=True,exist_ok=True)
  url='https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/'+name+'.zip'
  archive=p/(name+'.zip')
  if not archive.exists():archive.write_bytes(urllib.request.urlopen(url,timeout=60).read())
  data=archive.read_bytes()
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   paths=[s for s in z.namelist() if s.endswith('xccdf.xml')]; assert len(paths)==1,paths
   xml=z.read(paths[0]); (p/'benchmark.xml').write_bytes(xml)
  b=ET.fromstring(xml);rows=[]
  for g in b.findall('x:Group',N):
   for r in g.findall('x:Rule',N):
    refs=[ ''.join(e.itertext()).strip() for e in r.findall('x:ident',N)]
    rows.append(dict(benchmark=name,vuln_id=g.attrib['id'],rule_id=r.attrib['id'],version=txt(r,'version'),title=txt(r,'title'),severity=r.attrib.get('severity'),description=txt(r,'description'),check='\n'.join(''.join(e.itertext()).strip() for e in r.findall('x:check/x:check-content',N)),fix=txt(r,'fixtext'),references=refs))
  assert rows and len({r['rule_id'] for r in rows})==len(rows)
  (p/'rules.json').write_text(json.dumps(rows,indent=2)+'\n')
  item=dict(package=name,title=txt(b,'title'),version=txt(b,'version'),rule_count=len(rows),source_url=url,sha256=hashlib.sha256(data).hexdigest(),xml_sha256=hashlib.sha256(xml).hexdigest(),retrieved_date='2026-11-09')
  manifest.append(item);print(name,len(rows),flush=True)
 (ROOT/'mpn/benchmarks/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
