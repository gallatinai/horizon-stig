#!/usr/bin/env python3
"""Build current status lists from official rules and saved assessment decisions."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / 'mpn/benchmarks'
OUT = ROOT / 'mpn/review'


def write_rows(path, rows):
    path.write_text(json.dumps(rows, indent=2) + '\n')
    fields = ['benchmark', 'vuln_id', 'rule_id', 'version', 'severity', 'title',
              'components', 'status', 'justification', 'evidence', 'next_step',
              'owner', 'category', 'human_review', 'task', 'evidence_state']
    with path.with_suffix('.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    assessment = json.loads((ROOT / 'mpn/evidence/current-assessment.json').read_text())
    catalog = json.loads((ROOT / 'mpn/evidence/catalog.json').read_text())
    manifest = json.loads((BENCH / 'manifest.json').read_text())
    rows = []
    for package in manifest:
        name = package['package']
        rules = json.loads((BENCH / name / 'rules.json').read_text())
        current = []
        for rule in rules:
            row = {**rule, **assessment['decisions'][rule['vuln_id']]}
            row['evidence'] = '; '.join(catalog[key]['url'] for key in row['evidence_ids'])
            row['human_review'] = row['status'] in {'Needs work', 'Unclear'}
            current.append(row)
        rows.extend(current)
        lines = [f"# {package['title']}: current status", '',
                 'Recommended status, supporting evidence and action for each requirement. '
                 'Apply the stated component boundaries and obtain final checklist acceptance.', '',
                 '| Rule | Requirement | Status | Justification | Evidence / next action |',
                 '|---|---|---|---|---|']
        def clean(value):
            return str(value).replace('|', '\\|').replace('\n', ' ')
        for row in current:
            evidence = ' '.join(f"[{key}]({catalog[key]['url']})" for key in row['evidence_ids'])
            cells = [row['vuln_id'] + ' / ' + row['version'], row['title'], row['status'],
                     row['justification'], evidence + ' ' + row['next_step']]
            lines.append('| ' + ' | '.join(clean(cell) for cell in cells) + ' |')
        (OUT / (name + '.md')).write_text('\n'.join(lines) + '\n')
    assert len(rows) == len(assessment['decisions'])
    write_rows(OUT / 'suggested-statuses.json', rows)
    write_rows(OUT / 'human-review.json', [row for row in rows if row['human_review']])
    counts = {'total': len(rows), 'by_status': dict(Counter(row['status'] for row in rows)),
              'by_benchmark': {p['package']: dict(Counter(row['status'] for row in rows
                                if row['benchmark'] == p['package'])) for p in manifest}}
    (OUT / 'counts.json').write_text(json.dumps(counts, indent=2) + '\n')
    print(json.dumps(counts['by_status']))


if __name__ == '__main__':
    main()
