import contextlib
import copy
import hashlib
import io
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from test_governance_v3 import GovernanceV3Tests
from quality_cli import main, mission_errors, project_report, read_json, structure_errors
from quality_v4 import waiver_current
from quality_v3 import parse_block
from new_mission import create_mission


class GovernanceWaiverTests(GovernanceV3Tests):
    def test_existing_waivers_with_current_matrix(self):
        root = Path(__file__).resolve().parents[1]
        shutil.copyfile(root / 'quality/controls.json', self.root / 'quality/controls.json')
        for kind in ('valid', 'expired', 'revoked', 'malformed', 'accepted'):
            with self.subTest(kind=kind):
                folder, mission = self.case()
                if kind == 'expired':
                    mission['gate1_waiver']['expires_at'] = '2021-01-01T00:00:00Z'
                if kind == 'revoked':
                    mission['gate1_waiver']['revocations'] = [{'at':'2026-11-06T00:00:00Z','reason':'revoked','owner_ref':'owner'}]
                if kind == 'malformed':
                    mission['gate1_waiver']['exceptions'] = []
                if kind == 'accepted':
                    self.record(folder, mission, 'gate2')
                    self.record(folder, mission, 'gate3')
                    mission['owner_acceptance'] = {'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
                (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = main(['can-implement', '--mission', folder.name, '--root', str(self.root)])
                self.assertEqual(1, code)
                self.assertEqual('MANUAL_OWNER_VERIFICATION_REQUIRED' in out.getvalue(), kind in ('valid', 'accepted'))
                if kind == 'accepted':
                    self.assertEqual('APPROVED', mission['owner_acceptance']['status'])
                    self.assertEqual([], mission_errors(folder, mission))
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(1, main(['can-close', '--mission', folder.name, '--root', str(self.root)]))
                    mission['gate1_waiver']['revocations'].append({'at':'2026-11-06T00:00:00Z','reason':'revoked','owner_ref':'owner'})
                    self.assertEqual([], mission_errors(folder, mission))
                    (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(1, main(['can-close', '--mission', folder.name, '--root', str(self.root)]))

    def case(self):
        self.case_number = getattr(self, 'case_number', 0) + 1
        folder = create_mission(self.root, f'CASE-{self.case_number}', 'Test', 'HIGH', 'orch', 'arch')
        mission = json.loads((folder / 'mission.json').read_text(encoding='utf-8'))
        mission['roles']['developer'] = [{'id': 'dev', 'evidence': None, 'verification': None}]
        plan = folder / '01-PLAN.md'
        execution = folder / 'execution-record.txt'
        execution.write_text('session evidence', encoding='utf-8')
        block = {
            'mission': mission['id'], 'gate': 'gate1', 'risk': 'HIGH', 'decision': 'PASS',
            'reviewer': 'quality', 'artifact': {'name': plan.name,
                'ref': 'sha256_lf:' + hashlib.sha256(plan.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                'path': plan.name},
            'effective_authors': ['arch'], 'authorship_independent': True,
            'isolation': 'I0_CONTEXTO_COMPARTIDO',
            'evidence': [{'kind': 'execution', 'path': execution.name,
                          'sha256_lf': hashlib.sha256(execution.read_bytes()).hexdigest()}],
            'date': '2026-11-05',
        }
        self.write_block(folder, mission, 'gate1', block)
        review = mission['gates']['gate1']['review']
        mission['gates']['gate1'] = {'decision': 'PENDING', 'review': None}
        mission['schema_version'] = 4
        mission['pilot_project'] = {'id': 'pilot', 'local_fictional': True}
        mission['gate1_waiver'] = {
            'id': 'WAIVER-01', 'mission': mission['id'], 'project_id': 'pilot',
            'owner_id': 'owner', 'authorization_ref': 'owner-controlled-channel',
            'issued_at': '2020-01-01T00:00:00Z', 'not_before': '2020-01-01T00:00:00Z',
            'expires_at': '2099-01-01T00:00:00Z',
            'actions': ['implement', 'gate2', 'gate3', 'close'],
            'exceptions': ['I1_CONTEXTO_SEPARADO', 'G1_EVIDENCIA_REGISTRADA'],
            'technical_review': review, 'artifact': block['artifact'],
            'revocations': [], 'prior_failures': [],
        }
        return folder, mission

    def test_valid_waiver_is_structural_not_automatic_authorization(self):
        folder, mission = self.case()
        self.assertEqual([], mission_errors(folder, mission))
        (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(['can-implement', '--mission', folder.name, '--root', str(self.root)])
        self.assertEqual(1, code)
        self.assertIn('MANUAL_OWNER_VERIFICATION_REQUIRED', out.getvalue())
        self.assertEqual('PENDING', mission['gates']['gate1']['decision'])

    def test_scope_authority_and_exception_mutations_fail(self):
        cases = [
            lambda m: m.update(risk='CRITICAL'),
            lambda m: m['pilot_project'].update(local_fictional=False),
            lambda m: m['gate1_waiver'].update(mission='OTHER-001'),
            lambda m: m['gate1_waiver'].update(project_id='other'),
            lambda m: m['gate1_waiver'].update(owner_id='arch'),
            lambda m: m['gate1_waiver'].update(owner_id='orch'),
            lambda m: m['gate1_waiver'].update(owner_id='quality'),
            lambda m: m['gate1_waiver'].update(authorization_ref=' '),
            lambda m: m['gate1_waiver'].update(actions=['implement', 'implement']),
            lambda m: m['gate1_waiver'].update(actions=['gate4']),
            lambda m: m['gate1_waiver'].update(exceptions=['I1_CONTEXTO_SEPARADO']),
            lambda m: m['gate1_waiver'].update(expires_at='not-a-date'),
            lambda m: m['gate1_waiver'].update(unexpected=True),
            lambda m: m.update(unexpected=True),
            lambda m: m['gates']['gate1'].update(decision='FAIL'),
        ]
        for mutate in cases:
            with self.subTest(mutate=mutate):
                folder, mission = self.case()
                mutate(mission)
                self.assertTrue(mission_errors(folder, mission))

    def test_review_integrity_and_execution_are_required(self):
        folder, mission = self.case()
        review = folder / mission['gate1_waiver']['technical_review']['file']
        review.write_text('tampered', encoding='utf-8')
        self.assertTrue(mission_errors(folder, mission))
        folder, mission = self.case()
        (folder / 'execution-record.txt').unlink()
        self.assertTrue(mission_errors(folder, mission))
        folder, mission = self.case()
        (folder / '01-PLAN.md').write_text('changed', encoding='utf-8')
        self.assertTrue(mission_errors(folder, mission))

    def test_revocation_expiry_and_action_never_authorize(self):
        folder, mission = self.case()
        now = datetime(2026, 11, 5, tzinfo=timezone.utc)
        self.assertTrue(waiver_current(mission, 'implement', now))
        self.assertFalse(waiver_current(mission, 'unknown', now))
        mission['gate1_waiver']['revocations'].append(
            {'at': '2098-01-01T00:00:00Z', 'reason': 'revoked', 'owner_ref': 'channel'})
        self.assertEqual([], mission_errors(folder, mission))
        self.assertFalse(waiver_current(mission, 'implement', now))
        mission['gate1_waiver']['revocations'] = []
        self.assertFalse(waiver_current(mission, 'implement', datetime(2099, 1, 1, tzinfo=timezone.utc)))

    def test_v3_downgrade_with_extra_fields_stays_blocked(self):
        folder, mission = self.case()
        mission['schema_version'] = 3
        self.assertTrue(mission_errors(folder, mission))
        (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, main(['can-implement', '--mission', folder.name, '--root', str(self.root)]))

    def test_waiver_fields_are_rejected_by_all_legacy_versions(self):
        folder, mission = self.case()
        for version in (1, 2, 3):
            with self.subTest(version=version):
                mission['schema_version'] = version
                self.assertTrue(any('v4 waiver fields' in e for e in structure_errors(mission)))

    def test_chain_is_structural_and_revocation_does_not_rewrite_history(self):
        folder, mission = self.case()
        self.record(folder, mission, 'gate2')
        self.record(folder, mission, 'gate3')
        mission['owner_acceptance'] = {'status': 'APPROVED', 'approved_by': 'owner', 'date': '2026-11-05'}
        self.assertEqual([], mission_errors(folder, mission))
        mission['gate1_waiver']['revocations'].append(
            {'at': '2026-11-06T00:00:00Z', 'reason': 'revoked', 'owner_ref': 'channel'})
        self.assertEqual([], mission_errors(folder, mission))
        (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, main(['can-close', '--mission', folder.name, '--root', str(self.root)]))
        mission['gate1_waiver'] = None
        self.assertTrue(mission_errors(folder, mission))

    def test_prior_failure_integrity(self):
        folder, mission = self.case()
        original = folder / 'original-fail.md'
        block = parse_block((folder / 'gate1-review.md').read_bytes())
        block['decision'] = 'FAIL'
        original.write_text('```protheusai-review\n' + json.dumps(block) + '\n```\n', encoding='utf-8')
        mission['gate1_waiver']['prior_failures'].append(
            {'path': original.name, 'sha256_bytes': hashlib.sha256(original.read_bytes()).hexdigest()})
        self.assertEqual([], mission_errors(folder, mission))
        original.write_text('altered', encoding='utf-8')
        self.assertTrue(mission_errors(folder, mission))

    def test_waiver_never_bypasses_stronger_matrix_minima(self):
        folder, mission = self.case()
        policy_path = self.root / 'quality/controls.json'
        policy = json.loads(policy_path.read_text(encoding='utf-8'))
        policy['independence_minimums']['HIGH']['gate1']['isolation'] = 'I2_PERMISOS_SEPARADOS'
        policy_path.write_text(json.dumps(policy), encoding='utf-8')
        self.assertTrue(mission_errors(folder, mission))

    def test_waiver_rejects_changed_guarantee_or_extra_evidence(self):
        folder, mission = self.case()
        policy_path = self.root / 'quality/controls.json'
        baseline = json.loads(policy_path.read_text(encoding='utf-8'))
        for kind in ('guarantee', 'evidence'):
            with self.subTest(kind=kind):
                policy = copy.deepcopy(baseline)
                if kind == 'guarantee':
                    policy['independence_minimums']['HIGH']['gate1']['guarantee'] = 'G2_VERIFICACION_REGISTRADA'
                else:
                    policy['independence_minimums']['HIGH']['gate1']['evidence'].append('execution')
                    policy['independence_minimums']['CRITICAL']['gate1']['evidence'].append('execution')
                policy_path.write_text(json.dumps(policy), encoding='utf-8')
                self.assertTrue(any('policy exceeds' in e for e in mission_errors(folder, mission)))

    def test_v4_duplicate_json_keys_are_rejected(self):
        folder, mission = self.case()
        raw = json.dumps(mission).replace('"owner_id": "owner"',
                                          '"owner_id": "attacker", "owner_id": "owner"')
        path = folder / 'mission.json'
        path.write_text(raw, encoding='utf-8')
        with self.assertRaises(ValueError):
            read_json(path)

    def test_accepted_v4_history_warns_when_matrix_is_strengthened(self):
        for waived in (False, True):
            with self.subTest(waived=waived):
                folder, mission = self.case()
                if not waived:
                    mission['gate1_waiver'] = None
                    self.record(folder, mission, 'gate1')
                self.record(folder, mission, 'gate2')
                self.record(folder, mission, 'gate3')
                mission['owner_acceptance'] = {'status': 'APPROVED', 'approved_by': 'owner', 'date': '2026-11-05'}
                (folder / 'mission.json').write_text(json.dumps(mission), encoding='utf-8')
                policy_path = self.root / 'quality/controls.json'
                policy = json.loads(policy_path.read_text(encoding='utf-8'))
                policy['independence_minimums']['HIGH']['gate1']['isolation'] = 'I2_PERMISOS_SEPARADOS'
                policy_path.write_text(json.dumps(policy), encoding='utf-8')
                self.assertEqual([], mission_errors(folder, mission))
                errors, warnings = project_report(self.root)
                self.assertEqual([], errors)
                self.assertTrue(any('no cumple la matriz vigente' in w for w in warnings))
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(1, main(['can-close', '--mission', folder.name, '--root', str(self.root)]))
                policy['independence_minimums']['HIGH']['gate1']['isolation'] = 'I1_CONTEXTO_SEPARADO'
                policy_path.write_text(json.dumps(policy), encoding='utf-8')

    def test_technical_review_mutations_are_rejected(self):
        cases = [('reviewer', 'arch'), ('authorship_independent', False),
                 ('mission', 'OTHER-001'), ('gate', 'gate2'), ('risk', 'LOW'),
                 ('decision', 'FAIL'), ('decision', 'PASS_WITH_RESERVATIONS'),
                 ('effective_authors', []), ('isolation', 'unknown'), ('evidence', [])]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                folder, mission = self.case()
                block = parse_block((folder / 'gate1-review.md').read_bytes())
                block[key] = value
                self.write_block(folder, mission, 'gate1', block)
                mission['gate1_waiver']['technical_review'] = mission['gates']['gate1']['review']
                mission['gates']['gate1'] = {'decision': 'PENDING', 'review': None}
                self.assertTrue(mission_errors(folder, mission))

    def test_invalid_references_and_revocations_fail_closed(self):
        mutations = [
            lambda w: w['technical_review'].update(file='../escape'),
            lambda w: w['artifact'].update(path='../escape'),
            lambda w: w.update(prior_failures=[{'path': '../escape', 'sha256_bytes': '0' * 64}]),
            lambda w: w.update(revocations=[{'at': 'wrong', 'reason': 'revoked', 'owner_ref': 'x'}]),
            lambda w: w.update(revocations=[{'at': '2026-01-01T00:00:00Z', 'reason': '', 'owner_ref': 'x'}]),
            lambda w: w.update(exceptions=['I1_CONTEXTO_SEPARADO', 'G1_EVIDENCIA_REGISTRADA', 'extra']),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                folder, mission = self.case()
                mutate(mission['gate1_waiver'])
                self.assertTrue(mission_errors(folder, mission))

    def test_utc_window_boundaries(self):
        folder, mission = self.case()
        self.assertFalse(waiver_current(mission, 'implement', datetime(2019, 12, 31, 23, 59, 59, tzinfo=timezone.utc)))
        self.assertTrue(waiver_current(mission, 'implement', datetime(2020, 1, 1, tzinfo=timezone.utc)))
        self.assertFalse(waiver_current(mission, 'implement', datetime(2099, 1, 1, tzinfo=timezone.utc)))

    def test_owner_acceptance_cannot_be_attributed_to_orchestrator(self):
        folder, mission = self.case()
        self.record(folder, mission, 'gate2')
        self.record(folder, mission, 'gate3')
        mission['owner_acceptance'] = {'status': 'APPROVED', 'approved_by': 'orch', 'date': '2026-11-05'}
        self.assertTrue(mission_errors(folder, mission))

    def test_each_chain_action_is_required(self):
        folder, mission = self.case()
        self.record(folder, mission, 'gate2')
        self.record(folder, mission, 'gate3')
        mission['owner_acceptance'] = {'status': 'APPROVED', 'approved_by': 'owner', 'date': '2026-11-05'}
        self.assertEqual([], mission_errors(folder, mission))
        for action in ('gate2', 'gate3', 'close'):
            with self.subTest(action=action):
                altered = copy.deepcopy(mission)
                altered['gate1_waiver']['actions'].remove(action)
                self.assertTrue(mission_errors(folder, altered))

    def test_gate2_reservations_do_not_satisfy_gate3(self):
        folder, mission = self.case()
        self.record(folder, mission, 'gate2', decision='PASS_WITH_RESERVATIONS')
        self.record(folder, mission, 'gate3')
        self.assertTrue(mission_errors(folder, mission))

    def test_symlink_to_evidence_is_rejected_when_supported(self):
        folder, mission = self.case()
        target = folder / 'execution-record.txt'
        link = folder / 'evidence-link.txt'
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f'symlink unavailable: {exc}')
        self.assertIsNone(__import__('quality_v3').canonical_file(folder, link.name))


if __name__ == '__main__':
    unittest.main()
