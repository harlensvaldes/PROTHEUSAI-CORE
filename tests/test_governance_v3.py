import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from new_mission import create_mission
from quality_cli import FILES, mission_errors


class GovernanceV3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in FILES:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        for source in (ROOT / 'docs/templates').glob('*.md'):
            shutil.copyfile(source, self.root / 'docs/templates' / source.name)

    def test_new_mission_uses_v3_pending_review(self):
        folder = create_mission(self.root, 'TEST-001', 'T', 'HIGH', 'orch', 'arch')
        m = json.loads((folder / 'mission.json').read_text(encoding='utf-8'))
        self.assertEqual(3, m['schema_version'])
        self.assertEqual({'decision': 'PENDING', 'review': None}, m['gates']['gate1'])
        self.assertEqual([], mission_errors(folder, m))


    def make_case(self, risk='HIGH'):
        folder = create_mission(self.root, 'TEST-100', 'Test', risk, 'orch', 'arch')
        manifest = json.loads((folder / 'mission.json').read_text(encoding='utf-8'))
        manifest['roles']['developer'] = [{'id': 'dev', 'evidence': None, 'verification': None}]
        return folder, manifest

    def record(self, folder, manifest, gate, decision='PASS'):
        import hashlib
        path = folder / ('identity-' + gate + '.txt')
        path.write_text('identity record', encoding='utf-8')
        ev = [{'kind':'identity', 'path':path.name,
               'sha256_lf':hashlib.sha256(path.read_bytes()).hexdigest()}]
        if gate == 'gate3':
            path = folder / 'execution.txt'
            path.write_text('execution record', encoding='utf-8')
            ev.append({'kind':'execution','path':path.name,
                       'sha256_lf':hashlib.sha256(path.read_bytes()).hexdigest()})
        block = {'mission':manifest['id'], 'gate':gate, 'risk':manifest['risk'], 'decision':decision,
                 'reviewer':'quality', 'artifact':{'name':'reviewed', 'ref':'git:1234567', 'path':None},
                 'effective_authors':['arch' if gate == 'gate1' else 'dev'],
                 'authorship_independent':True, 'isolation':'I1_CONTEXTO_SEPARADO',
                 'evidence':ev, 'date':'2026-11-05'}
        self.write_block(folder, manifest, gate, block)
        return block

    def write_block(self, folder, manifest, gate, block):
        import hashlib
        fence = chr(96)*3
        text = fence+'protheusai-review\n'+json.dumps(block)+'\n'+fence+'\n'
        path = folder / (gate + '-review.md')
        path.write_text(text, encoding='utf-8', newline='\n')
        manifest['gates'][gate] = {'decision':block['decision'],
           'review':{'file':path.name,'sha256_lf':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'reviewer_verification':None}}

    def test_high_full_chain_and_mutated_authorship(self):
        folder, m = self.make_case()
        for gate in ('gate1','gate2','gate3'):
            self.record(folder,m,gate)
        self.assertEqual([], mission_errors(folder,m))
        cases = [('reviewer',' ORCH '), ('authorship_independent',False),
                 ('isolation','I0_CONTEXTO_COMPARTIDO'), ('mission','OTHER'),
                 ('gate','gate2'), ('risk','LOW'), ('effective_authors',[])]
        for key,value in cases:
            with self.subTest(key=key):
                block=self.record(folder,m,'gate1')
                block[key]=value
                self.write_block(folder,m,'gate1',block)
                self.assertTrue(mission_errors(folder,m), key)
        self.record(folder,m,'gate1')
        self.assertEqual([],mission_errors(folder,m))

    def test_report_integrity_missing_evidence_and_excluded_evidence(self):
        folder,m=self.make_case()
        block=self.record(folder,m,'gate1')
        self.assertEqual([],mission_errors(folder,m))
        (folder/'identity-gate1.txt').write_text('altered',encoding='utf-8')
        self.assertTrue(mission_errors(folder,m))
        block=self.record(folder,m,'gate1')
        block['evidence']=[]
        self.write_block(folder,m,'gate1',block)
        self.assertTrue(mission_errors(folder,m))
        block=self.record(folder,m,'gate1')
        block['evidence'][0]['path']='01-PLAN.md'
        self.write_block(folder,m,'gate1',block)
        self.assertTrue(mission_errors(folder,m))
        self.record(folder,m,'gate1')
        (folder/'gate1-review.md').write_text('bad',encoding='utf-8')
        self.assertTrue(mission_errors(folder,m))

    def test_block_structure_invalid_and_path_traversal(self):
        folder,m=self.make_case()
        block=self.record(folder,m,'gate1')
        self.assertEqual([],mission_errors(folder,m))
        for mutation in ('extra','missing','path'):
            with self.subTest(mutation=mutation):
                block=self.record(folder,m,'gate1')
                if mutation=='extra': block['unexpected']=True
                elif mutation=='missing': del block['reviewer']
                else: block['evidence'][0]['path']='../identity'
                self.write_block(folder,m,'gate1',block)
                self.assertTrue(mission_errors(folder,m))
        self.record(folder,m,'gate1')
        path=folder/'gate1-review.md'
        path.write_bytes(b'\xff\x00')
        self.assertTrue(mission_errors(folder,m))

    def test_fail_traceable_never_enables(self):
        folder,m=self.make_case()
        block=self.record(folder,m,'gate1',decision='FAIL')
        block['reviewer']='arch'
        block['authorship_independent']=False
        block['isolation']='I0_CONTEXTO_COMPARTIDO'
        block['evidence']=[]
        self.write_block(folder,m,'gate1',block)
        self.assertEqual([],mission_errors(folder,m))
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        from quality_cli import main
        self.assertEqual(1,main(['can-implement','--mission',folder.name,'--root',str(self.root)]))

    def test_invalid_matrix_fails_closed_and_hash_normalizes(self):
        from quality_v3 import policy_errors,digest
        policy=json.loads((self.root/'quality/controls.json').read_text(encoding='utf-8'))
        self.assertEqual([],policy_errors(policy))
        policy['independence_minimums']['HIGH']['gate1']['evidence']=[]
        self.assertTrue(policy_errors(policy))
        self.assertEqual(digest(b'a\r\nb'),digest(b'a\nb'))
        self.assertNotEqual(digest(b'a\rb'),digest(b'a\nb'))

    def test_critical_requires_third_party_verification(self):
        folder,m=self.make_case('CRITICAL')
        block=self.record(folder,m,'gate1')
        isolation=folder/'isolation.txt'
        isolation.write_text('permission record',encoding='utf-8')
        import hashlib
        block['isolation']='I2_PERMISOS_SEPARADOS'
        block['evidence'].append({'kind':'isolation','path':isolation.name,
                                  'sha256_lf':hashlib.sha256(isolation.read_bytes()).hexdigest()})
        self.write_block(folder,m,'gate1',block)
        self.assertTrue(mission_errors(folder,m))
        m['roles']['architect'][0]['evidence']={'method':'source','ref':'record'}
        m['roles']['architect'][0]['verification']={'by':'third','method':'source','ref':'record','date':'2026-11-05'}
        verification={'id':'quality','by':'third','method':'source','ref':'record','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']=verification
        self.assertEqual([],mission_errors(folder,m))
        for key,value in [('by','orch'),('by','quality'),('id','wrong')]:
            with self.subTest(key=key,value=value):
                m['gates']['gate1']['review']['reviewer_verification']=dict(verification,**{key:value})
                self.assertTrue(mission_errors(folder,m))
        m['gates']['gate1']['review']['reviewer_verification']=verification
        m['roles']['architect'][0]['verification']['by']='quality'
        self.assertTrue(mission_errors(folder,m))

    def test_matrix_monotonicity_and_missing_policy(self):
        from quality_v3 import policy_errors
        import copy
        original=json.loads((self.root/'quality/controls.json').read_text(encoding='utf-8'))
        cases=[]
        p=copy.deepcopy(original);del p['independence_minimums'];cases.append(p)
        p=copy.deepcopy(original);del p['independence_minimums']['HIGH']['gate2'];cases.append(p)
        p=copy.deepcopy(original);p['independence_minimums']['HIGH']['gate1']['isolation']='bad';cases.append(p)
        p=copy.deepcopy(original);p['independence_minimums']['CRITICAL']['gate1']['isolation']='I0_CONTEXTO_COMPARTIDO';cases.append(p)
        p=copy.deepcopy(original);p['independence_minimums']['MEDIUM']['gate1']['guarantee']='G1_EVIDENCIA_REGISTRADA';p['independence_minimums']['MEDIUM']['gate1']['evidence']=['identity'];p['independence_minimums']['HIGH']['gate1']['guarantee']='G0_DECLARADA';cases.append(p)
        p=copy.deepcopy(original);p['independence_minimums']['HIGH']['gate3']['evidence']=['identity'];cases.append(p)
        p=copy.deepcopy(original);p['independence_minimums']['HIGH']['gate2']['pinned_artifact']=False;cases.append(p)
        for i,p in enumerate(cases):
            with self.subTest(i=i): self.assertTrue(policy_errors(p))
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        (self.root/'quality/controls.json').unlink()
        self.assertTrue(mission_errors(folder,m))

    def test_pinned_artifact_execution_and_review_hash(self):
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        block=self.record(folder,m,'gate2')
        block['artifact']['ref']='sha256:'+'a'*64
        self.write_block(folder,m,'gate2',block)
        self.assertTrue(mission_errors(folder,m))
        block=self.record(folder,m,'gate2')
        self.assertEqual([],mission_errors(folder,m))
        block=self.record(folder,m,'gate3')
        block['evidence']=[x for x in block['evidence'] if x['kind']!='execution']
        self.write_block(folder,m,'gate3',block)
        self.assertTrue(mission_errors(folder,m))
        self.record(folder,m,'gate3')
        m['gates']['gate2']['review']['sha256_lf']='a'*64
        self.assertTrue(mission_errors(folder,m))

    def test_approved_warns_but_current_minima_block_close(self):
        from quality_cli import main
        from contextlib import redirect_stdout
        import io
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        self.assertEqual([],mission_errors(folder,m))
        path=self.root/'quality/controls.json'
        policy=json.loads(path.read_text(encoding='utf-8'))
        policy['independence_minimums']['HIGH']['gate1']['isolation']='I2_PERMISOS_SEPARADOS'
        path.write_text(json.dumps(policy),encoding='utf-8')
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        out=io.StringIO()
        with redirect_stdout(out):
            result=main(['validate','--root',str(self.root)])
        self.assertEqual(0,result,out.getvalue())
        self.assertIn('no cumple la matriz vigente',out.getvalue())
        self.assertEqual(1,main(['can-close','--mission',folder.name,'--root',str(self.root)]))
        m['owner_acceptance']={'status':'PENDING','approved_by':None,'date':None}
        self.assertTrue(mission_errors(folder,m))

    def test_i0_never_enables_even_if_policy_attempts_to_allow_it(self):
        folder,m=self.make_case('LOW')
        path=self.root/'quality/controls.json'
        policy=json.loads(path.read_text(encoding='utf-8'))
        policy['independence_minimums']['LOW']['gate1']['isolation']='I0_CONTEXTO_COMPARTIDO'
        path.write_text(json.dumps(policy),encoding='utf-8')
        block=self.record(folder,m,'gate1')
        block['isolation']='I0_CONTEXTO_COMPARTIDO'
        self.write_block(folder,m,'gate1',block)
        self.assertTrue(any('I0' in x for x in mission_errors(folder,m)))

    def test_owner_whitespace_identity_and_date_do_not_close(self):
        from quality_cli import main
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'):
            self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        self.assertEqual([],mission_errors(folder,m))
        m['owner_acceptance']['approved_by']='\u200b'
        self.assertTrue(mission_errors(folder,m))
        m['owner_acceptance']['approved_by']='owner'
        m['owner_acceptance']['date']='\u200b'
        self.assertTrue(mission_errors(folder,m))
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        self.assertEqual(1,main(['can-close','--mission',folder.name,'--root',str(self.root)]))
        m['owner_acceptance']['date']='2026-11-05'
        for key in ('approved_by','date'):
            with self.subTest(key=key):
                m['owner_acceptance'][key]='   '
                self.assertTrue(mission_errors(folder,m))
                (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
                self.assertEqual(1,main(['can-close','--mission',folder.name,'--root',str(self.root)]))
                m['owner_acceptance'][key]='owner' if key=='approved_by' else '2026-11-05'

    def test_report_crosschecks_and_block_shapes(self):
        import hashlib
        folder,m=self.make_case()
        fence=chr(96)*3
        cases=[
          ('mission',lambda b:b.update(mission='OTHER')),
          ('gate',lambda b:b.update(gate='gate2')),
          ('risk',lambda b:b.update(risk='LOW')),
          ('decision',lambda b:b.update(decision='FAIL')),
          ('missing_independence',lambda b:b.pop('authorship_independent')),
          ('wrong_independence_type',lambda b:b.update(authorship_independent='true')),
          ('extra_key',lambda b:b.update(extra='x')),
          ('empty_name',lambda b:b['artifact'].update(name=' ')),
          ('bad_ref',lambda b:b['artifact'].update(ref='git:short')),
          ('wrong_authors',lambda b:b.update(effective_authors=['other'])),
          ('no_authors',lambda b:b.update(effective_authors=[])),
        ]
        for label,mutate in cases:
            with self.subTest(label=label):
                b=self.record(folder,m,'gate1')
                self.assertEqual([],mission_errors(folder,m))
                mutate(b);self.write_block(folder,m,'gate1',b)
                if label=='decision': m['gates']['gate1']['decision']='PASS'
                self.assertTrue(mission_errors(folder,m))
        for label,text in [
            ('missing','no block'),
            ('duplicate',fence+'protheusai-review\n{}\n'+fence+'\n'+fence+'protheusai-review\n{}\n'+fence),
            ('nested',fence+'protheusai-review\n'+fence+'python\n{}\n'+fence+'\n'+fence),
            ('invalid_json',fence+'protheusai-review\n{\n'+fence),
            ('nul',fence+'protheusai-review\n{}\x00\n'+fence),
        ]:
            with self.subTest(label=label):
                self.record(folder,m,'gate1')
                path=folder/'gate1-review.md';path.write_text(text,encoding='utf-8')
                m['gates']['gate1']['review']['sha256_lf']=hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertTrue(mission_errors(folder,m))

    def test_canonical_paths_and_integrity_rejections(self):
        import hashlib
        folder,m=self.make_case()
        for name in ('../outside','./identity-gate1.txt','Identity-gate1.txt',
                     'identity-gate1.txt\n','sub\\file','not there.txt','missing','.', '..'):
            with self.subTest(name=name):
                b=self.record(folder,m,'gate1')
                self.assertEqual([],mission_errors(folder,m))
                b['evidence'][0]['path']=name
                self.write_block(folder,m,'gate1',b)
                self.assertTrue(mission_errors(folder,m))
        for name in ('01-PLAN.md','02-GATE1-REVIEW.md','mission.json','gate1-review.md'):
            with self.subTest(excluded=name):
                b=self.record(folder,m,'gate1')
                b['evidence'][0]['path']=name
                self.write_block(folder,m,'gate1',b)
                self.assertTrue(mission_errors(folder,m))
        b=self.record(folder,m,'gate1')
        b['evidence'].append(dict(b['evidence'][0]))
        self.write_block(folder,m,'gate1',b)
        self.assertTrue(mission_errors(folder,m))
        b=self.record(folder,m,'gate1')
        b['evidence'][0]['sha256_lf']='f'*64
        self.write_block(folder,m,'gate1',b)
        self.assertTrue(mission_errors(folder,m))

    def test_low_medium_high_same_environment_and_free_narrative(self):
        import hashlib
        for risk in ('LOW','MEDIUM','HIGH'):
            with self.subTest(risk=risk):
                folder,m=self.make_case(risk)
                for gate in ('gate1','gate2','gate3'):
                    self.record(folder,m,gate)
                self.assertEqual([],mission_errors(folder,m))
                path=folder/'gate1-review.md'
                path.write_text('Narrative: no shared isolation claim.\n'+path.read_text(encoding='utf-8'),encoding='utf-8')
                m['gates']['gate1']['review']['sha256_lf']=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
                self.assertEqual([],mission_errors(folder,m))
                shutil.rmtree(folder)

    def test_path_backed_artifact_is_recalculated(self):
        import hashlib
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        b=self.record(folder,m,'gate2')
        path=folder/'GATE2-INPUT-09.sha256'
        path.write_bytes(b'review input\n')
        b['artifact']={'name':'input','ref':'sha256_lf:'+hashlib.sha256(path.read_bytes()).hexdigest(),'path':path.name}
        self.write_block(folder,m,'gate2',b)
        self.assertEqual([],mission_errors(folder,m))
        path.write_bytes(b'changed\n')
        self.assertTrue(mission_errors(folder,m))

    def test_review_date_must_be_a_valid_iso_date(self):
        folder,m=self.make_case()
        b=self.record(folder,m,'gate1')
        self.assertEqual([],mission_errors(folder,m))
        for value in ('yesterday','2026-02-31','20261105',' '):
            with self.subTest(value=value):
                b=self.record(folder,m,'gate1')
                b['date']=value
                self.write_block(folder,m,'gate1',b)
                self.assertTrue(mission_errors(folder,m))

    def test_invisible_fields_do_not_satisfy_g2_or_artifact_traceability(self):
        import hashlib
        folder,m=self.make_case('CRITICAL')
        b=self.record(folder,m,'gate1')
        p=folder/'isolation.txt';p.write_text('permission',encoding='utf-8')
        b['isolation']='I2_PERMISOS_SEPARADOS'
        b['evidence'].append({'kind':'isolation','path':p.name,'sha256_lf':hashlib.sha256(p.read_bytes()).hexdigest()})
        self.write_block(folder,m,'gate1',b)
        m['roles']['architect'][0]['evidence']={'method':'source','ref':'record'}
        m['roles']['architect'][0]['verification']={'by':'third','method':'source','ref':'record','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']={'id':'quality','by':'third','method':'source','ref':'record','date':'2026-11-05'}
        self.assertEqual([],mission_errors(folder,m))
        for target,fields in [
            (m['roles']['architect'][0]['evidence'],('method','ref')),
            (m['roles']['architect'][0]['verification'],('method','ref','date')),
            (m['gates']['gate1']['review']['reviewer_verification'],('method','ref','date'))]:
            for field in fields:
                with self.subTest(field=field,target=id(target)):
                    prior=target[field];target[field]='\u200b'
                    self.assertTrue(mission_errors(folder,m))
                    target[field]=prior
        b['artifact']['name']='\u200b'
        self.write_block(folder,m,'gate1',b)
        self.assertTrue(mission_errors(folder,m))
