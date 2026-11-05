import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from quality_cli import mission_errors, project_errors, main as quality_main
from new_mission import create_mission


class TemplateQualityTests(unittest.TestCase):
    def test_package_has_all_required_files_and_example_pending(self):
        self.assertEqual([], project_errors(ROOT))
        self.assertEqual(1,quality_main(['can-implement','--mission','EXAMPLE-001','--root',str(ROOT)]))
        example=json.loads((ROOT/'docs/MISSIONS/EXAMPLE-001/mission.json').read_text())
        self.assertEqual('PENDING',example['gates']['gate1']['decision'])

    def test_new_mission_starts_pending_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'docs/templates').mkdir(parents=True)
            for source in (ROOT/'docs/templates').glob('*.md'):
                (root/'docs/templates'/source.name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
            out=create_mission(root,'TEST-001','Test','MEDIUM','dev-a')
            m=json.loads((out/'mission.json').read_text(encoding='utf-8'))
            self.assertEqual([],mission_errors(out,m))
            self.assertEqual('PENDING',m['gates']['gate1']['decision'])
            with self.assertRaises(FileExistsError):
                create_mission(root,'TEST-001','No sobrescribir','MEDIUM','dev-a')

    def test_no_self_approval_or_missing_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'docs/templates').mkdir(parents=True)
            for source in (ROOT/'docs/templates').glob('*.md'):
                (root/'docs/templates'/source.name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
            out=create_mission(root,'TEST-002','Test','HIGH','developer-1')
            m=json.loads((out/'mission.json').read_text())
            gate=m['gates']['gate1']
            gate.update(decision='PASS',reviewer_id='developer-1',reviewed_artifact='sha256:abc',evidence_file='02-GATE1-REVIEW.md',date='2026-01-01')
            self.assertTrue(any('autoaprobación' in e for e in mission_errors(out,m)))
            gate['reviewer_id']='quality-2'
            self.assertTrue(any('falta informe independiente' in e for e in mission_errors(out,m)))
            (out/'02-GATE1-REVIEW.md').write_text('Revisor quality-2\n\nDictamen: PASS\nEvidencia: revisión estática del caso de test.',encoding='utf-8')
            self.assertEqual([],mission_errors(out,m))
            gate['evidence_file']='../../secrets.txt'
            self.assertTrue(any('falta informe independiente' in e for e in mission_errors(out,m)))

    def test_must_pass_gate1_before_gate2(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'docs/templates').mkdir(parents=True)
            for source in (ROOT/'docs/templates').glob('*.md'):
                (root/'docs/templates'/source.name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
            out=create_mission(root,'TEST-003','Test','HIGH','developer-1')
            m=json.loads((out/'mission.json').read_text())
            m['gates']['gate2'].update(decision='PASS',reviewer_id='quality-2',reviewed_artifact='sha256:xyz',evidence_file='04-GATE2-REVIEW.md',date='2026-01-01')
            self.assertTrue(any('Gate anterior no tiene PASS' in e for e in mission_errors(out,m)))


if __name__=='__main__':
    unittest.main()
