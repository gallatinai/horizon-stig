#!/usr/bin/env python3
"""Reproduce release profile/image transforms, then Helm-render without deployment.
Requires the recorded bundle checkout, saved public release metadata, Helm/PyYAML.
No registry pull, resolver credential, real secret or cluster access is used.
"""
import argparse,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('bundle_checkout',type=Path);args=p.parse_args()
bundle=args.bundle_checkout.resolve()
sys.path.insert(0,str(bundle/'scripts/ci'))
from platform_identity import apply_identity
from runtime_source import stage
metadata=ROOT/'mpn/evidence/delivered-release'
info=json.loads((metadata/'build-info.json').read_text())
contract=json.loads((metadata/'platform-contract.json').read_text())
assert info['platformContract']==contract
assert contract['identity']['mode']=='uds'
assert info['runtimeSource']['sourceSha']==info['horizonCommit']
with tempfile.TemporaryDirectory(prefix='horizon-stig-delivered-') as temp:
 source=Path(temp)/'source';shutil.copytree(bundle/'source',source)
 for relative in ['zarf.yaml','charts/horizon-uds-package/Chart.yaml']:
  target=source/relative;content=target.read_text()
  assert '0.0.0-dev' in content
  target.write_text(content.replace('0.0.0-dev',info['version']))
 apply_identity(source,contract);stage(source,info['runtimeSource'])
 subprocess.run([sys.executable,str(ROOT/'scripts/render_candidate.py'),str(source),'--source-path','--output','mpn/evidence/rendered-delivered'],check=True)
print('Rendered exact saved UDS identity/image selection; no live credentials or deployment.')
