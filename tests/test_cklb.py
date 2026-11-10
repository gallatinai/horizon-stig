"""Check exports against the independent official XCCDF inventory and decisions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from uuid import UUID
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generate_cklb', ROOT / 'scripts/generate_cklb.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
N = {'x': 'http://checklists.nist.gov/xccdf/1.1'}


class Checklists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = generator.outputs()
        cls.manifest = json.loads((ROOT / 'mpn/benchmarks/manifest.json').read_text())
        cls.assessment = json.loads((ROOT / 'mpn/evidence/current-assessment.json').read_text())

    def test_all_rules_and_official_metadata_preserved(self):
        self.assertEqual(set(self.outputs), {p['package'] + '.cklb' for p in self.manifest})
        uuids = set()
        total = 0
        for package in self.manifest:
            name = package['package']
            document = json.loads(self.outputs[name + '.cklb'])
            self.assertEqual(document['cklb_version'], '1.0')
            self.assertIs(type(document['active']), bool)
            self.assertIs(type(document['mode']), int)
            self.assertIs(type(document['has_path']), bool)
            self.assertEqual(document['target_data']['host_name'], 'Horizon-MPN')
            for key in ('ip_address', 'mac_address', 'fqdn'):
                self.assertEqual(document['target_data'][key], '')
            self.assertEqual(len(document['stigs']), 1)
            stig = document['stigs'][0]
            xml = ET.parse(ROOT / 'mpn/benchmarks' / name / 'benchmark.xml').getroot()
            self.assertEqual(stig['stig_id'], xml.attrib['id'])
            self.assertEqual(stig['version'], xml.findtext('x:version', namespaces=N))
            self.assertEqual(stig['release_info'], xml.findtext('x:plain-text[@id="release-info"]', namespaces=N))
            self.assertEqual(stig['size'], package['rule_count'])
            self.assertEqual(len(stig['rules']), package['rule_count'])
            official = {rule.attrib['id']: (group, rule)
                        for group in xml.findall('x:Group', N)
                        for rule in group.findall('x:Rule', N)}
            self.assertEqual({r['rule_id_src'] for r in stig['rules']}, set(official))
            for value in [document['id'], stig['uuid']] + [r['uuid'] for r in stig['rules']]:
                self.assertEqual(UUID(value).version, 5)
                self.assertNotIn(value, uuids)
                uuids.add(value)
            for row in stig['rules']:
                group, rule = official[row['rule_id_src']]
                self.assertEqual(row['group_id'], group.attrib['id'])
                self.assertEqual(row['stig_uuid'], stig['uuid'])
                for field, path in [('check_content', 'x:check/x:check-content'),
                                    ('fix_text', 'x:fixtext'), ('rule_title', 'x:title'),
                                    ('rule_version', 'x:version')]:
                    self.assertEqual(row[field], rule.findtext(path, namespaces=N))
                self.assertEqual(row['severity'], rule.attrib['severity'])
                ccis = [i.text for i in rule.findall('x:ident', N) if i.text.startswith('CCI-')]
                self.assertEqual(row['ccis'], ccis)
                self.assertIsInstance(row['overrides'], dict)
                self.assertIsInstance(row['group_tree'], list)
                self.assertEqual(row['group_tree'][0]['id'], row['group_id'])
                self.assertIn(row['status'], {'open', 'not_reviewed', 'not_a_finding', 'not_applicable'})
                decision = self.assessment['decisions'][row['group_id']]
                self.assertIn(decision['justification'], row['comments'])
                self.assertIn(decision['next_step'], row['comments'])
                self.assertTrue(row['discussion'])
                self.assertTrue(row['finding_details'])
            total += len(stig['rules'])
        self.assertEqual(total, len(self.assessment['decisions']))

    def test_default_dispositions_do_not_close_provisional_findings(self):
        expected = {'Compliant': 'not_a_finding', 'Needs work': 'open',
                    'Likely covered': 'not_reviewed', 'Unclear': 'not_reviewed',
                    'Needs N/A justification': 'not_reviewed'}
        for recommendation, status in expected.items():
            self.assertEqual(generator.disposition({'status': recommendation}), status)
        with self.assertRaises(KeyError):
            generator.disposition({'status': 'Typo'})
        with self.assertRaises(ValueError):
            generator.disposition({'status': 'Compliant', 'cklb_status': 'pass'})

    def test_explicit_na_disposition_requires_reason_and_is_exported(self):
        decision = {'status': 'Needs N/A justification', 'cklb_status': 'not_applicable'}
        with self.assertRaises(ValueError):
            generator.disposition(decision)
        decision['cklb_justification'] = '   '
        with self.assertRaises(ValueError):
            generator.disposition(decision)
        assessment = copy.deepcopy(self.assessment)
        package = self.manifest[0]
        xml = ET.parse(ROOT / 'mpn/benchmarks' / package['package'] / 'benchmark.xml').getroot()
        key = xml.find('x:Group', N).attrib['id']
        assessment['decisions'][key].update(decision, cklb_justification='This component does not expose this capability.')
        catalog = json.loads((ROOT / 'mpn/evidence/catalog.json').read_text())
        row = generator.build_checklist(package, xml, assessment, catalog)['stigs'][0]['rules'][0]
        self.assertEqual(row['status'], 'not_applicable')
        self.assertEqual(row['finding_details'], 'This component does not expose this capability.')
        self.assertIn(row['finding_details'], row['comments'])

    def test_description_preserves_literal_prose(self):
        fields = generator.description_fields('<VulnDiscussion>x < 5 & y</VulnDiscussion><Documentable>false</Documentable>')
        self.assertEqual(fields['discussion'], 'x < 5 & y')
        self.assertEqual(fields['documentable'], 'false')
        self.assertEqual(generator.description_fields('Plain description')['discussion'], 'Plain description')

    def test_repeatable_output_and_ids_stable_when_disposition_changes(self):
        self.assertEqual(self.outputs, generator.outputs())
        assessment = copy.deepcopy(self.assessment)
        package = self.manifest[0]
        xml = ET.parse(ROOT / 'mpn/benchmarks' / package['package'] / 'benchmark.xml').getroot()
        catalog = json.loads((ROOT / 'mpn/evidence/catalog.json').read_text())
        before = generator.build_checklist(package, xml, assessment, catalog)
        key = xml.find('x:Group', N).attrib['id']
        assessment['decisions'][key]['status'] = ('Compliant' if assessment['decisions'][key]['status'] == 'Needs work' else 'Needs work')
        assessment['decisions'][key].pop('cklb_status', None)
        after = generator.build_checklist(package, xml, assessment, catalog)
        self.assertNotEqual(before['stigs'][0]['rules'][0]['status'], after['stigs'][0]['rules'][0]['status'])
        self.assertEqual(before['stigs'][0]['rules'][1:], after['stigs'][0]['rules'][1:])
        self.assertEqual(before['id'], after['id'])
        self.assertEqual(before['stigs'][0]['uuid'], after['stigs'][0]['uuid'])
        self.assertEqual([r['uuid'] for r in before['stigs'][0]['rules']],
                         [r['uuid'] for r in after['stigs'][0]['rules']])

    def test_check_detects_missing_modified_and_obsolete_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'mpn').mkdir()
            (root / 'mpn/benchmarks').symlink_to(ROOT / 'mpn/benchmarks', target_is_directory=True)
            (root / 'mpn/evidence').symlink_to(ROOT / 'mpn/evidence', target_is_directory=True)
            with self.assertRaises(ValueError):
                generator.generate(root, check=True)
            generator.generate(root)
            generator.generate(root, check=True)
            path = root / 'mpn/cklb' / next(iter(self.outputs))
            path.write_text('{}')
            with self.assertRaises(ValueError):
                generator.generate(root, check=True)
            obsolete = root / 'mpn/cklb/old.cklb'
            obsolete.write_text('{}')
            with self.assertRaises(ValueError):
                generator.generate(root, check=True)
            generator.generate(root)
            self.assertFalse(obsolete.exists())
            generator.generate(root, check=True)


if __name__ == '__main__':
    unittest.main()
