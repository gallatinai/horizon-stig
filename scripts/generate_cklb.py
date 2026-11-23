#!/usr/bin/env python3
"""Generate deterministic STIG Viewer 3 checklists from XCCDF and saved decisions."""
import argparse
import json
import re
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
N = {'x': 'http://checklists.nist.gov/xccdf/1.1',
     'dc': 'http://purl.org/dc/elements/1.1/'}
STATUS = {
    'Compliant': 'not_a_finding',
    'Needs work': 'open',
    'Likely covered': 'not_reviewed',
    'Unclear': 'not_reviewed',
    'Needs N/A justification': 'not_reviewed',
}
DISPOSITIONS = {'open', 'not_a_finding', 'not_applicable', 'not_reviewed'}
DESCRIPTION_FIELDS = {
    'discussion': 'VulnDiscussion', 'false_positives': 'FalsePositives',
    'false_negatives': 'FalseNegatives', 'documentable': 'Documentable',
    'security_override_guidance': 'SeverityOverrideGuidance',
    'potential_impacts': 'PotentialImpacts', 'third_party_tools': 'ThirdPartyTools',
    'ia_controls': 'IAControls', 'responsibility': 'Responsibility',
    'mitigations': 'Mitigations', 'mitigation_control': 'MitigationControl',
}

# CKLB files go to external assessors; justifications must not carry in-house references.
INTERNAL_PATTERNS = [
    re.compile(r'slack\.com|docs\.google\.com|drive\.google\.com|atlassian\.net', re.I),
    re.compile(r'github\.com/gallatinai/', re.I),
    re.compile(r'\bGAL-\d+\b', re.I),
    # Fail closed on any case: an external justification must state a disposition, not a triage label.
    re.compile(r'\b(needs work|likely covered|needs n/a justification|unclear|evidence state|next action|owner:)', re.I),
]


def stable_id(key):
    return str(uuid5(NAMESPACE_URL, 'https://github.com/gallatinai/horizon-stig/' + key))


def text(element, path):
    return element.findtext(path, default='', namespaces=N)


def disposition(decision):
    default = STATUS[decision['status']]
    result = decision.get('cklb_status', default)
    if result not in DISPOSITIONS:
        raise ValueError(f'Invalid CKLB status: {result!r}')
    if result != default and not decision.get('cklb_justification', '').strip():
        raise ValueError('A CKLB status override requires cklb_justification')
    return result


def reject_internal_content(vuln_id, justification):
    for pattern in INTERNAL_PATTERNS:
        match = pattern.search(justification)
        if match:
            raise ValueError(f'{vuln_id}: cklb_justification contains internal-only content: {match.group(0)!r}')


def cited_evidence(justification, catalog):
    # Only parenthesised items count: prose words such as "images" and "host" are also catalog keys.
    cited = []
    for group in re.findall(r'\(([^()]*)\)', justification):
        for token in re.split(r'[,;]', group):
            token = token.strip()
            if token in catalog and token not in cited:
                cited.append(token)
    return cited


def evidence_block(vuln_id, justification, evidence_ids, catalog):
    lines = []
    for evidence_id in cited_evidence(justification, catalog):
        if evidence_id not in evidence_ids:
            raise ValueError(f'{vuln_id}: cklb_justification cites {evidence_id!r} but it is not in evidence_ids')
        title = catalog[evidence_id]['title']
        for pattern in INTERNAL_PATTERNS:
            match = pattern.search(title)
            if match:
                raise ValueError(f'{vuln_id}: evidence {evidence_id} title contains internal-only content: {match.group(0)!r}')
        lines.append(f'- {evidence_id}: {title}')
    return '\n'.join(['Evidence:'] + lines) if lines else ''


def description_fields(description):
    # XCCDF descriptions contain escaped markup. Extract the known wrappers
    # without parsing the embedded prose as XML (it may contain literal < or &).
    fields = {}
    for field, tag in DESCRIPTION_FIELDS.items():
        match = re.search(r'<' + tag + r'>(.*?)</' + tag + '>', description, re.S)
        fields[field] = match.group(1).strip() if match else ''
    if not fields['discussion']:
        fields['discussion'] = description
    if not fields['documentable']:
        fields['documentable'] = 'false'
    return fields


def build_checklist(package, benchmark, assessment, catalog):
    name = package['package']
    stig_uuid = stable_id(name + '/stig')
    rules = []
    for group in benchmark.findall('x:Group', N):
        for rule in group.findall('x:Rule', N):
            vuln_id = group.attrib['id']
            decision = assessment['decisions'][vuln_id]
            status = disposition(decision)
            justification = decision.get('cklb_justification', '').strip()
            reject_internal_content(vuln_id, justification)
            baseline = assessment['baseline']
            comments = (f"Assessed release: {baseline['version']} "
                        f"(Horizon commit {baseline['horizon_commit']})")
            if justification:
                block = evidence_block(vuln_id, justification, decision.get('evidence_ids', []), catalog)
                if block:
                    comments += '\n' + block
            check_ref = rule.find('x:check/x:check-content-ref', N)
            identifiers = [ident.text for ident in rule.findall('x:ident', N) if ident.text]
            reference = text(rule, 'x:reference/dc:identifier') or None
            rule_id = rule.attrib['id']
            rules.append({
                'group_id_src': vuln_id,
                'group_tree': [{'id': vuln_id, 'title': text(group, 'x:title'),
                                'description': text(group, 'x:description')}],
                'group_id': vuln_id, 'severity': rule.attrib['severity'],
                'group_title': text(group, 'x:title'), 'rule_id_src': rule_id,
                'rule_id': rule_id.removesuffix('_rule'),
                'rule_version': text(rule, 'x:version'), 'rule_title': text(rule, 'x:title'),
                'fix_text': text(rule, 'x:fixtext'), 'weight': rule.attrib.get('weight', '10.0'),
                'check_content': text(rule, 'x:check/x:check-content'),
                'check_content_ref': dict(check_ref.attrib) if check_ref is not None else None,
                'classification': 'Unclassified',
                **description_fields(text(rule, 'x:description')),
                'legacy_ids': [item for item in identifiers if not item.startswith('CCI-')],
                'ccis': [item for item in identifiers if item.startswith('CCI-')],
                'reference_identifier': reference,
                'uuid': stable_id(name + '/' + rule_id), 'stig_uuid': stig_uuid,
                'status': status, 'overrides': {}, 'comments': comments,
                'finding_details': justification,
            })
    if len(rules) != package['rule_count']:
        raise ValueError(f"{name}: expected {package['rule_count']} rules, got {len(rules)}")
    return {
        'title': 'Horizon MPN - ' + name,
        'id': stable_id(name + '/checklist'), 'cklb_version': '1.0',
        'active': False, 'mode': 1, 'has_path': True,
        'target_data': {
            'target_type': 'Computing', 'host_name': 'Horizon-MPN',
            'ip_address': '', 'mac_address': '', 'fqdn': '',
            'comments': ('Product-level assessment for Gallatin-managed UDS Core on MPN. '
                         'Logical target; deployment asset identifiers are not recorded here. '
                         'Rule classification describes the public benchmark content.'),
            'role': 'None', 'is_web_database': False, 'technology_area': '',
            'web_db_site': '', 'web_db_instance': '',
        },
        'stigs': [{
            'stig_name': text(benchmark, 'x:title'),
            'display_name': text(benchmark, 'x:title'), 'stig_id': benchmark.attrib['id'],
            'version': text(benchmark, 'x:version'),
            'release_info': text(benchmark, 'x:plain-text[@id="release-info"]'),
            'uuid': stig_uuid,
            'reference_identifier': next((r['reference_identifier'] for r in rules
                                          if r['reference_identifier']), None),
            'size': len(rules), 'rules': rules,
        }],
    }


def outputs(root=ROOT):
    assessment = json.loads((root / 'mpn/evidence/current-assessment.json').read_text())
    catalog = json.loads((root / 'mpn/evidence/catalog.json').read_text())
    manifest = json.loads((root / 'mpn/benchmarks/manifest.json').read_text())
    result = {}
    seen = set()
    for package in manifest:
        name = package['package']
        benchmark = ET.parse(root / 'mpn/benchmarks' / name / 'benchmark.xml').getroot()
        checklist = build_checklist(package, benchmark, assessment, catalog)
        for rule in checklist['stigs'][0]['rules']:
            if rule['group_id'] in seen:
                raise ValueError('Duplicate assessment rule: ' + rule['group_id'])
            seen.add(rule['group_id'])
        result[name + '.cklb'] = json.dumps(checklist, indent=2, ensure_ascii=False) + '\n'
    if seen != set(assessment['decisions']):
        raise ValueError('Benchmark inventory and assessment decisions differ')
    return result


def generate(root=ROOT, check=False):
    expected = outputs(root)
    directory = root / 'mpn/cklb'
    stale = []
    for name, content in expected.items():
        path = directory / name
        if not path.exists() or path.read_text() != content:
            stale.append(name)
            if not check:
                directory.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    extras = sorted(p.name for p in directory.glob('*.cklb') if p.name not in expected)
    if not check:
        for name in extras:
            (directory / name).unlink()
    if check and (stale or extras):
        raise ValueError('CKLB files need regeneration: ' + ', '.join(stale + extras))
    return len(expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed files are stale')
    args = parser.parse_args()
    print(f"PASS: {generate(check=args.check)} CKLB checklists {'verified' if args.check else 'generated'}.")
