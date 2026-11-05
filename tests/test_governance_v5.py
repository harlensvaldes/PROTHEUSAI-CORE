import contextlib
import copy
import hashlib
import io
import json
import unittest

from test_governance_v3 import GovernanceV3Tests
from quality_cli import main, mission_errors, read_json
from new_mission import create_mission


class GovernanceV5Tests(GovernanceV3Tests):
    def case(self):
        folder, mission = self.make_case()
        mission['schema_version'] = 5
        mission['scope'] = {'profile':'LOCAL_FICTIONAL_EXPERIMENTAL', 'project_id':'pilot', 'owner_decision_ref':'owner message 1'}
        return folder, mission

    @staticmethod
    def scope_digest(scope):
        return hashlib.sha256(json.dumps(scope, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

    def record_v5(self, folder, m, gate='gate1', decision='PASS'):
        block={'mission':m['id'], 'gate':gate, 'risk':m['risk'], 'decision':decision,
               'reviewer':'quality', 'artifact':{'name':'reviewed','ref':'git:1234567','path':None},
               'effective_authors':['arch' if gate=='gate1' else 'dev'], 'authorship_independent':True,
               'isolation':'I0_CONTEXTO_COMPARTIDO', 'evidence':[], 'date':'2026-11-05',
               'scope_digest':self.scope_digest(m['scope']), 'reviewer_session':None}
        self.write_block(folder,m,gate,block)
        return block

    def test_pending_and_i0_pass_with_distinct_author(self):
        folder,m=self.case()
        self.assertEqual([],mission_errors(folder,m))
        self.record_v5(folder,m)
        self.assertEqual([],mission_errors(folder,m))
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,main(['can-implement','--mission',folder.name,'--root',str(self.root)]))
            self.assertNotEqual(0,main(['can-close','--mission',folder.name,'--root',str(self.root)]))

    def test_self_approval_and_scope_change_are_rejected(self):
        folder,m=self.case(); block=self.record_v5(folder,m)
        block['reviewer']='arch';self.write_block(folder,m,'gate1',block)
        self.assertTrue(mission_errors(folder,m))
        self.record_v5(folder,m);m['scope']['project_id']='another'
        self.assertTrue(mission_errors(folder,m))

    def test_bad_scope_hybrids_and_critical_rejected(self):
        folder,m=self.case()
        for change in (lambda x:x['scope'].update(profile='OTHER'),lambda x:x['scope'].update(project_id=' '),
                       lambda x:x.update(risk='CRITICAL'),lambda x:x.update(gate1_waiver=None),
                       lambda x:x['scope'].update(extra=True)):
            value=copy.deepcopy(m);change(value)
            self.assertTrue(mission_errors(folder,value))

    def test_duplicate_keys_are_rejected_in_v5(self):
        folder,m=self.case(); data=json.dumps(m).replace('"project_id": "pilot"','"project_id": "pilot", "project_id": "other"')
        (folder/'mission.json').write_text(data,encoding='utf-8')
        with self.assertRaises(ValueError): read_json(folder/'mission.json')

    def test_all_gates_require_pass_and_owner_for_close(self):
        folder,m=self.case()
        for gate in ('gate1','gate2','gate3'): self.record_v5(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        self.assertEqual([],mission_errors(folder,m))
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,main(['can-close','--mission',folder.name,'--root',str(self.root)]))

    def test_review_integrity_and_scope_session_validation(self):
        folder,m=self.case()
        for key,value in [('reviewer_session',''),('reviewer_session',5),('scope_digest','0'*64),('authorship_independent',False),('isolation','bad')]:
            block=self.record_v5(folder,m);block[key]=value;self.write_block(folder,m,'gate1',block)
            self.assertTrue(mission_errors(folder,m), key)
        block=self.record_v5(folder,m);block['reviewer_session']='session-1';self.write_block(folder,m,'gate1',block)
        self.assertEqual([],mission_errors(folder,m))
        (folder/'gate1-review.md').write_text('tampered',encoding='utf-8')
        self.assertTrue(mission_errors(folder,m))

    def test_pending_invalid_and_reservations_block_commands(self):
        folder,m=self.case(); (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,main(['status','--mission',folder.name,'--root',str(self.root)]))
            self.assertEqual(1,main(['can-implement','--mission',folder.name,'--root',str(self.root)]))
        self.record_v5(folder,m,decision='PASS_WITH_RESERVATIONS')
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1,main(['can-implement','--mission',folder.name,'--root',str(self.root)]))
        m['scope']['project_id']='changed'
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1,main(['status','--mission',folder.name,'--root',str(self.root)]))
            self.assertEqual(1,main(['can-close','--mission',folder.name,'--root',str(self.root)]))

    def test_v5_duplicate_schema_version_cannot_downgrade_parser(self):
        folder,m=self.case(); raw=json.dumps(m).replace('"schema_version": 5', '"schema_version": 5, "schema_version": 3')
        (folder/'mission.json').write_text(raw,encoding='utf-8')
        with self.assertRaises(ValueError): read_json(folder/'mission.json')

    def test_scope_digest_is_canonical_and_changes_semantics(self):
        _,m=self.case(); reordered=dict(reversed(list(m['scope'].items())))
        self.assertEqual(self.scope_digest(m['scope']),self.scope_digest(reordered))
        for field in ('project_id','owner_decision_ref'):
            changed=dict(m['scope']);changed[field]+='a'
            self.assertNotEqual(self.scope_digest(m['scope']),self.scope_digest(changed))

    def test_explicit_new_v5_mission_starts_pending(self):
        scope={'profile':'LOCAL_FICTIONAL_EXPERIMENTAL','project_id':'p1','owner_decision_ref':'message owner'}
        folder=create_mission(self.root, 'TEST-200','Pilot','HIGH','orch','arch',scope=scope)
        m=read_json(folder/'mission.json')
        self.assertEqual(5,m['schema_version'])
        self.assertEqual([],mission_errors(folder,m))
        self.assertTrue(all(g['decision']=='PENDING' for g in m['gates'].values()))

    def test_invalid_new_scope_must_not_create_directory(self):
        with self.assertRaises(ValueError):
            create_mission(self.root,'TEST-201','Pilot','CRITICAL','orch','arch',scope={'profile':'LOCAL_FICTIONAL_EXPERIMENTAL','project_id':'p','owner_decision_ref':'owner'})
        self.assertFalse((self.root/'docs/MISSIONS/TEST-201').exists())
