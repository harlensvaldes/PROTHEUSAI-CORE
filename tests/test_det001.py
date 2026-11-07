"""Deterministic checks for sha256 manifests and mission record anchors (DET-001)."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from quality_cli import classify, main
from new_mission import create_mission


def sha_lf(data):
    return hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()


def run(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            code = main(argv)
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue()


class DetBase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
        return path

    def manifest(self, name, lines):
        return self.write(name, '\n'.join(lines) + '\n')


class ManifestCommandTests(DetBase):
    def test_manifest_valid_crlf_status_and_classification(self):
        product = self.write('scripts/tool.py', b'print(1)\r\n')
        governance = self.write('docs/PROJECT_CHARTER.md', b'# charter\n')
        self.manifest('MANIFEST-01.sha256', [
            '# comment',
            f' M {sha_lf(product.read_bytes())}  scripts/tool.py',
            f'{sha_lf(governance.read_bytes())}  docs/PROJECT_CHARTER.md',
        ])
        code, out = run(['manifest', str(self.root / 'MANIFEST-01.sha256'), '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('gobernanza 1', out)
        self.assertIn('producto/implementación 1', out)
        self.assertIn('2/2', out)
        self.assertIn('no altera qué artefactos forman parte de un Gate', out)

    def test_manifest_reports_mismatch_missing_duplicate_and_unsafe_paths(self):
        self.write('ok.py', 'content\n')
        self.manifest('MANIFEST-02.sha256', [
            f"{'0' * 64}  ok.py",
            f"{'a' * 64}  missing.py",
            f"{'b' * 64}  ../outside.py",
            f"{'c' * 64}  /absolute.py",
            f"{'d' * 64}  ok.py",
        ])
        code, out = run(['manifest', str(self.root / 'MANIFEST-02.sha256'), '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('sha256_lf no coincide', out)
        self.assertIn('archivo ausente', out)
        self.assertIn('ruta no canónica', out)
        self.assertIn('ruta duplicada', out)

    def test_manifest_unreadable_returns_two(self):
        code, out = run(['manifest', str(self.root / 'absent.sha256'), '--root', str(self.root)])
        self.assertEqual(2, code, out)
        code, out = run(['manifest', str(self.root), '--root', str(self.root)])
        self.assertEqual(2, code, out)
        self.write('BROKEN.sha256', b'\xff\xfe\x00')
        code, out = run(['manifest', str(self.root / 'BROKEN.sha256'), '--root', str(self.root)])
        self.assertEqual(2, code, out)
        code, out = run(['manifest', '--root', str(self.root)])
        self.assertEqual(2, code, out)

    def test_manifest_ambiguous_and_empty(self):
        self.write('EMPTY.sha256', '# only comments\n\n')
        code, out = run(['manifest', str(self.root / 'EMPTY.sha256'), '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('manifiesto sin entradas', out)
        self.write('ok.py', 'x\n')
        self.manifest('AMBIGUOUS.sha256', [f"{'a' * 65}  ok.py"])
        code, out = run(['manifest', str(self.root / 'AMBIGUOUS.sha256'), '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('entrada ambigua', out)

    def test_manifest_truncated_hash_is_ambiguous(self):
        target = self.write('ok.py', 'x\n')
        self.manifest('TRUNCATED.sha256', [
            f'{sha_lf(target.read_bytes())}  ok.py',
            f"{'a' * 63}  ghost.py",
        ])
        code, out = run(['manifest', str(self.root / 'TRUNCATED.sha256'), '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('entrada ambigua', out)

    def test_manifest_prose_and_single_space(self):
        target = self.write('a.md', 'value\n')
        self.manifest('PROSE.sha256', [
            f"# sha256 raw reconstructed {'f' * 64}",
            f"HEAD {'1' * 40}",
            'Git status --porcelain; SHA256 LF',
            '```',
            f'{sha_lf(target.read_bytes())} a.md',
            '```',
        ])
        code, out = run(['manifest', str(self.root / 'PROSE.sha256'), '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('1/1', out)

    def test_manifest_porcelain_tokens(self):
        for name in ('a.py', 'b.py', 'c.py'):
            self.write(name, name + '\n')
        lines = [f"{token} {sha_lf((self.root / name).read_bytes())}  {name}"
                 for token, name in ((' M', 'a.py'), ('??', 'b.py'), ('!!', 'c.py'))]
        self.manifest('PORCELAIN.sha256', lines)
        code, out = run(['manifest', str(self.root / 'PORCELAIN.sha256'), '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('3/3', out)

    def test_manifest_hash_is_case_insensitive(self):
        target = self.write('upper.txt', b'line\r\n')
        self.manifest('UPPER.sha256', [f'{sha_lf(target.read_bytes()).upper()}  upper.txt'])
        code, out = run(['manifest', str(self.root / 'UPPER.sha256'), '--root', str(self.root)])
        self.assertEqual(0, code, out)

    def test_manifest_root_missing_or_outside(self):
        self.write('present.txt', 'x\n')
        self.manifest('ROOT.sha256', [f"{'0' * 64}  present.txt"])
        code, out = run(['manifest', str(self.root / 'ROOT.sha256'), '--root', str(self.root / 'absent')])
        self.assertEqual(1, code, out)
        self.assertIn('archivo ausente', out)

    def test_manifest_path_resolved_from_cwd(self):
        base = self.root / 'base'
        target = self.write('base/inside.txt', 'inside\n')
        self.manifest('OUTSIDE.sha256', [f'{sha_lf(target.read_bytes())}  inside.txt'])
        code, out = run(['manifest', str(self.root / 'OUTSIDE.sha256'), '--root', str(base)])
        self.assertEqual(0, code, out)

    def test_manifest_rejects_symlink(self):
        target = self.write('real.txt', 'real\n')
        try:
            os.symlink(target, self.root / 'link.txt')
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlink privilege unavailable: {exc}')
        self.manifest('LINK.sha256', [f'{sha_lf(target.read_bytes())}  link.txt'])
        code, out = run(['manifest', str(self.root / 'LINK.sha256'), '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('archivo ausente', out)

    def test_classify_is_presentation_only(self):
        self.assertEqual('gobernanza', classify('docs/MISSIONS/X/01-PLAN.md'))
        self.assertEqual('gobernanza', classify('quality/controls.json'))
        self.assertEqual('gobernanza', classify('AGENTS.md'))
        self.assertEqual('gobernanza', classify('PLAN-REFORMA-QUALITY-01.md'))
        self.assertEqual('producto/implementación', classify('scripts/quality_cli.py'))
        self.assertEqual('producto/implementación', classify('src/app.py'))


class AuditBase(DetBase):
    def setUp(self):
        super().setUp()
        (self.root / 'quality').mkdir(parents=True)
        shutil.copyfile(ROOT / 'quality/controls.json', self.root / 'quality/controls.json')
        for source in (ROOT / 'docs/templates').glob('*.md'):
            target = self.root / 'docs/templates' / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def mission(self, mid='TEST-100', risk='LOW'):
        folder = create_mission(self.root, mid, 'Test', risk, 'orch', 'arch')
        mission = json.loads((folder / 'mission.json').read_text(encoding='utf-8'))
        mission['roles']['developer'] = [{'id': 'dev', 'evidence': None, 'verification': None}]
        return folder, mission

    def write_block(self, folder, mission, gate, block):
        text = '# review\n```protheusai-review\n' + json.dumps(block) + '\n```\n'
        path = folder / f'{gate}-review.md'
        path.write_text(text, encoding='utf-8', newline='\n')
        mission['gates'][gate] = {'decision': block['decision'],
                                  'review': {'file': path.name,
                                             'sha256_lf': sha_lf(path.read_bytes()),
                                             'reviewer_verification': None}}

    def record(self, folder, mission, gate):
        evidence = folder / f'{gate}-evidence.txt'
        evidence.write_text(gate + ' record\n', encoding='utf-8')
        block = {'mission': mission['id'], 'gate': gate, 'risk': mission['risk'],
                 'decision': 'PASS', 'reviewer': 'quality',
                 'artifact': {'name': 'reviewed', 'ref': 'git:1234567', 'path': None},
                 'effective_authors': ['arch' if gate == 'gate1' else 'dev'],
                 'authorship_independent': True, 'isolation': 'I0_CONTEXTO_COMPARTIDO',
                 'evidence': [{'kind': 'execution' if gate == 'gate3' else 'identity',
                               'path': evidence.name,
                               'sha256_lf': sha_lf(evidence.read_bytes())}],
                 'date': '2026-11-07'}
        self.write_block(folder, mission, gate, block)
        return block

    def full_record(self, folder, mission):
        for gate in ('gate1', 'gate2', 'gate3'):
            self.record(folder, mission, gate)

    def save(self, folder, mission):
        (folder / 'mission.json').write_text(json.dumps(mission, ensure_ascii=False, indent=2),
                                             encoding='utf-8')

    def anchor(self, folder, name, entries):
        """entries: (repo-relative path, sha256_lf) exactly as manifests store them."""
        (folder / name).write_text(
            '\n'.join(f'{digest}  {path}' for path, digest in entries) + '\n', encoding='utf-8')

    def path_of(self, folder, mission_relative):
        return f'docs/MISSIONS/{folder.name}/{mission_relative}'

    def anchors_for_record(self, folder, mission):
        entries = []
        for gate in ('gate1', 'gate2', 'gate3'):
            review = mission['gates'][gate].get('review')
            if not review:
                continue
            entries.append((self.path_of(folder, review['file']), review['sha256_lf']))
            evidence = folder / f'{gate}-evidence.txt'
            entries.append((self.path_of(folder, evidence.name), sha_lf(evidence.read_bytes())))
        return entries


class AuditCommandTests(AuditBase):
    def test_audit_anchored_consistency_passes(self):
        folder, mission = self.mission()
        self.full_record(folder, mission)
        self.save(folder, mission)
        self.write('scripts/tool.py', 'product\n')
        entries = self.anchors_for_record(folder, mission)
        entries.append(('scripts/tool.py', sha_lf((self.root / 'scripts/tool.py').read_bytes())))
        self.anchor(folder, 'GATE2-INPUT-01.sha256', entries)
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('manifiesto GATE2-INPUT-01.sha256: 7 entradas', out)
        self.assertIn('OK — registro y anclas coherentes', out)
        self.assertNotIn('AVISO', out)

    def test_audit_maps_mission_relative_to_repo_relative(self):
        folder, mission = self.mission('TEST-101')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        self.anchor(folder, 'GATE2-INPUT-01.sha256', self.anchors_for_record(folder, mission))
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertNotIn('no figura en ningún manifiesto', out)

    def test_audit_detects_record_divergence(self):
        folder, mission = self.mission('TEST-102')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        review = mission['gates']['gate1']['review']
        self.anchor(folder, 'GATE2-INPUT-01.sha256', [(self.path_of(folder, review['file']), review['sha256_lf'])])
        (folder / review['file']).write_text('tampered\n', encoding='utf-8')
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('review hash mismatch', out)

    def test_audit_reuses_mission_record_checks(self):
        folder, mission = self.mission('TEST-103')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        (folder / 'gate1-evidence.txt').unlink()
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('evidence', out)


    def test_audit_record_not_anchored(self):
        folder, mission = self.mission('TEST-104')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        review = mission['gates']['gate1']['review']
        self.anchor(folder, 'GATE2-INPUT-01.sha256', [(self.path_of(folder, review['file']), '0' * 64)])
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('versión registrada no anclada', out)

    def test_audit_missing_anchor_is_warning_only(self):
        folder, mission = self.mission('TEST-105')
        self.full_record(folder, mission)
        self.save(folder, mission)
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('AVISO:', out)
        self.assertIn('no figura en ningún manifiesto', out)

    def test_audit_multi_cycle_precedence(self):
        folder, mission = self.mission('TEST-106')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        review = mission['gates']['gate1']['review']
        self.write('scripts/tool.py', 'v1\n')
        tool = self.write('scripts/tool2.py', 'actual\n')
        first = sha_lf(tool.read_bytes())
        review_path = self.path_of(folder, review['file'])
        self.anchor(folder, 'GATE2-INPUT-01.RECONSTRUCTED.sha256', [(review_path, review['sha256_lf'])])
        self.anchor(folder, 'GATE2-INPUT-02.sha256', [(review_path, '0' * 64)])
        self.anchor(folder, 'GATE2-INPUT-03.RECONSTRUCTED.sha256', [('scripts/tool2.py', '1' * 64)])
        self.anchor(folder, 'GATE2-INPUT-03.sha256', [('scripts/tool2.py', first)])
        self.anchor(folder, 'GATE2-INPUT-09.sha256', [('scripts/tool.py', '2' * 64)])
        self.anchor(folder, 'GATE2-INPUT-10.sha256', [
            ('scripts/tool.py', sha_lf((self.root / 'scripts/tool.py').read_bytes()))])
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('coincide con un ciclo anterior', out)
        self.assertNotIn('deriva del árbol respecto al ancla efectiva: scripts/tool2.py', out)
        self.assertNotIn('deriva del árbol respecto al ancla efectiva: scripts/tool.py', out)

    def test_audit_tree_drift_is_warning(self):
        folder, mission = self.mission('TEST-107')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        review = mission['gates']['gate1']['review']
        tool = self.write('scripts/tool.py', 'v1\n')
        self.anchor(folder, 'GATE2-INPUT-01.sha256', [
            (self.path_of(folder, review['file']), review['sha256_lf']),
            ('scripts/tool.py', sha_lf(tool.read_bytes())),
        ])
        tool.write_text('v2\n', encoding='utf-8')
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('deriva del árbol respecto al ancla efectiva: scripts/tool.py', out)

    def test_audit_invalid_vs_unreadable_manifest(self):
        folder, mission = self.mission('TEST-108')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        (folder / 'BAD-01.sha256').write_text(f"{'a' * 65}  x.py\n", encoding='utf-8')
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('entrada ambigua', out)
        other, other_mission = self.mission('TEST-109')
        self.record(other, other_mission, 'gate1')
        self.save(other, other_mission)
        (other / 'BAD-01.sha256').write_bytes(b'\xff\xfe\x00')
        code, out = run(['audit', '--mission', other.name, '--root', str(self.root)])
        self.assertEqual(2, code, out)
        self.assertIn('no se puede leer', out)

    def test_audit_unreadable_takes_precedence(self):
        folder, mission = self.mission('TEST-110')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        review = mission['gates']['gate1']['review']
        (folder / review['file']).write_text('tampered\n', encoding='utf-8')
        (folder / 'A-BAD.sha256').write_bytes(b'\xff\xfe\x00')
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(2, code, out)

    def test_audit_mission_without_manifests(self):
        folder, mission = self.mission('TEST-111')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)
        self.assertIn('manifiestos: 0', out)

    def test_audit_foreign_mission_anchor_is_not_error(self):
        folder, mission = self.mission('TEST-112')
        self.record(folder, mission, 'gate1')
        self.save(folder, mission)
        foreign = self.write('docs/MISSIONS/OTHER-001/01-PLAN.md', 'plan\n')
        self.anchor(folder, 'GATE2-INPUT-01.sha256', [
            ('docs/MISSIONS/OTHER-001/01-PLAN.md', sha_lf(foreign.read_bytes()))])
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(0, code, out)

    def test_audit_invalid_mission_returns_two(self):
        code, out = run(['audit', '--mission', 'bad', '--root', str(self.root)])
        self.assertEqual(2, code, out)
        code, out = run(['audit', '--mission', 'MISSING-001', '--root', str(self.root)])
        self.assertEqual(2, code, out)

    def test_audit_structural_record_failure_returns_one(self):
        folder = create_mission(self.root, 'TEST-113', 'Test', 'LOW', 'orch', 'arch')
        (folder / 'mission.json').write_text('{}', encoding='utf-8')
        code, out = run(['audit', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code, out)
        self.assertIn('FAIL (discrepancias documentales)', out)
        self.assertNotIn('Traceback', out)

