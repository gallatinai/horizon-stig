#!/usr/bin/env python3
"""Check inventory completeness, evidence links, exports and candidate assertions."""
import csv
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from generate_cklb import generate

ROOT = Path(__file__).resolve().parents[1]
N = {'x': 'http://checklists.nist.gov/xccdf/1.1'}
ALLOWED = {'Compliant', 'Likely covered', 'Needs work', 'Needs N/A justification', 'Unclear'}


def main():
    generate(check=True)
    manifest = json.loads((ROOT / 'mpn/benchmarks/manifest.json').read_text())
    rows = json.loads((ROOT / 'mpn/review/suggested-statuses.json').read_text())
    evidence = json.loads((ROOT / 'mpn/evidence/catalog.json').read_text())
    expected = set()
    for package in manifest:
        name = package['package']
        path = ROOT / 'mpn/benchmarks' / name
        original = (path / (name + '.zip')).read_bytes()
        assert hashlib.sha256(original).hexdigest() == package['sha256'], name
        xml = (path / 'benchmark.xml').read_bytes()
        assert hashlib.sha256(xml).hexdigest() == package['xml_sha256'], name
        with zipfile.ZipFile(path / (name + '.zip')) as archive:
            members = [p for p in archive.namelist() if p.endswith('xccdf.xml')]
            assert len(members) == 1 and archive.read(members[0]) == xml, name
        official = ET.fromstring(xml).findall('x:Group/x:Rule', N)
        normalized = json.loads((path / 'rules.json').read_text())
        assert len(official) == len(normalized) == package['rule_count'], name
        assert {r.attrib['id'] for r in official} == {r['rule_id'] for r in normalized}, name
        subset = [r for r in rows if r['benchmark'] == name]
        assert len(subset) == len(official), name
        assert all(r['check'] and r['fix'] for r in subset), name
        md = (ROOT / 'mpn/review' / (name + '.md')).read_text()
        assert sum(line.startswith('| V-') for line in md.splitlines()) == len(official), name
        for r in normalized:
            expected.add((name, r['rule_id']))
        for original_rule in normalized:
            reviewed = next(r for r in subset if r['rule_id'] == original_rule['rule_id'])
            for field in original_rule:
                assert reviewed[field] == original_rule[field], (name, original_rule['rule_id'], field)
    for batch in [rows]:
        keys = [(r['benchmark'], r['rule_id']) for r in batch]
        assert len(keys) == len(set(keys)) == len(expected) and set(keys) == expected
        for r in batch:
            assert r['status'] in ALLOWED
            assert all(r.get(k) for k in ['justification', 'components', 'owner', 'next_step', 'evidence'])
            assert all(k in evidence for k in r['evidence_ids'])
            assert r['human_review'] == (r['status'] in {'Needs work', 'Unclear'})
    assert all(r.get('evidence_state') == 'source-inferred' for r in rows if r['status'] == 'Compliant'), 'Source-only compliant recommendations must be explicitly labelled'
    assessment = json.loads((ROOT / 'mpn/evidence/current-assessment.json').read_text())
    indexed = {r['vuln_id']: r for r in rows}
    assert set(indexed) == set(assessment['decisions'])
    for key, decision in assessment['decisions'].items():
        for field, value in decision.items():
            assert indexed[key][field] == value, (key, field)
    release_dir = ROOT / 'mpn/evidence/delivered-release'
    release = json.loads((release_dir / 'build-info.json').read_text())
    assert release['horizonCommit'] == assessment['baseline']['horizon_commit']
    assert release['platformContract']['identity']['mode'] == 'uds'
    assert len(release['images']) == 12
    workloads = json.loads((ROOT / 'mpn/evidence/rendered-delivered/workload-summary.json').read_text())
    assert {w['image'] for w in workloads} == set(release['images'])
    assert not (ROOT / 'mpn/evidence/rendered-delivered/keycloak.yaml').exists()
    assert all(w['resources'] for w in workloads)
    for item in json.loads((release_dir / 'provenance.json').read_text())['files']:
        assert hashlib.sha256((release_dir / item['path']).read_bytes()).hexdigest() == item['sha256']
    for item in json.loads((ROOT / 'mpn/evidence/rendered-manifest.json').read_text())['files']:
        assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
    for name, batch in [('suggested-statuses', rows)]:
        with (ROOT / 'mpn/review' / (name + '.csv')).open() as f:
            exported = list(csv.DictReader(f))
        assert [(r['benchmark'], r['rule_id'], r['status']) for r in exported] == [
            (r['benchmark'], r['rule_id'], r['status']) for r in batch
        ]
    queue = json.loads((ROOT / 'mpn/review/human-review.json').read_text())
    assert queue == [r for r in rows if r['human_review']]
    counts = json.loads((ROOT / 'mpn/review/counts.json').read_text())
    assert counts['total'] == len(rows) and counts['by_status'] == dict(Counter(r['status'] for r in rows))
    rendered = ROOT / 'mpn/evidence/rendered-delivered'
    assert 'POSTGRES_PASSWORD' in (rendered / 'postgres.yaml').read_text()
    assert 'secretKeyRef:' in (rendered / 'postgres.yaml').read_text()
    s3 = (rendered / 'seaweedfs.yaml').read_text()
    assert 'kind: ConfigMap' in s3 and '"secretKey"' in s3 and 'ZARF_VAR_S3_SECRET_ACCESS_KEY' in s3
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        import re
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in target and not target.startswith('#'):
                assert (path.parent / target.split('#')[0]).exists(), (path, target)
    print(f'PASS: {len(manifest)} official packages; {len(rows)} unique rules; full check/fix preserved; CSV/JSON/Markdown agree.')
    print(f'PASS: human-review queue contains all {len(queue)} Needs work/Unclear recommendations; candidate assertions match Helm renders.')


if __name__ == '__main__':
    main()
