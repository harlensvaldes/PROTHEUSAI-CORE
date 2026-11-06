import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from quality_cli import FILES, main, project_report


class ReconstructedMissionTests(unittest.TestCase):
    def test_real_reconstructed_records_preserve_history_without_enabling_transitions(self):
        expected = {
            'CONTEXT-001': (('PASS', 'PASS', 'PASS_WITH_RESERVATIONS'), 'PENDING'),
            'CONTEXT-OPT-001': (('PENDING', 'PENDING', 'PASS_WITH_RESERVATIONS'), 'APPROVED'),
            'DESIGN-001': (('PASS', 'PASS', 'PASS_WITH_RESERVATIONS'), 'APPROVED'),
        }
        errors, warnings = project_report(ROOT)
        self.assertEqual([], errors)
        for mission, (gates, owner) in expected.items():
            folder = ROOT / 'docs' / 'MISSIONS' / mission
            record = json.loads((folder / 'mission.json').read_text(encoding='utf-8'))
            self.assertEqual(1, record['schema_version'])
            self.assertEqual('indice_retrospectivo', record['reconstruction']['type'])
            self.assertIn('no se afirma que existiera originalmente', record['reconstruction']['notice'])
            self.assertTrue(all((folder / p).is_file() for p in record['reconstruction']['sources']))
            self.assertEqual(gates, tuple(record['gates'][g]['decision'] for g in ('gate1', 'gate2', 'gate3')))
            self.assertEqual(owner, record['owner_acceptance']['status'])
            self.assertTrue(any(mission in w for w in warnings))
            for command in ('can-implement', 'can-close'):
                self.assertEqual(1, main([command, '--mission', mission, '--root', str(ROOT)]))

    def test_new_unregistered_directory_fails_global_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in FILES:
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dest)
            (root / 'docs/MISSIONS/NEW-001').mkdir(parents=True)
            errors, _ = project_report(root)
            self.assertTrue(any('NEW-001' in e and 'mission.json' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
