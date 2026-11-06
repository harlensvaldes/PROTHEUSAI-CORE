import contextlib
import copy
import hashlib
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from quality_cli import FILES, GATES, MISSION_FILES, mission_errors, project_errors, main as quality_main
from new_mission import AUTHOR_DEPRECATED, create_mission, main as new_mission_main

HASH='a'*64
REPORTS={'gate1':'02-GATE1-REVIEW.md','gate2':'04-GATE2-REVIEW.md','gate3':'05-GATE3-EVIDENCE.md'}
TEMPLATES={'gate1':'GATE1_REVIEW.md','gate2':'GATE2_REVIEW.md','gate3':'GATE3_EVIDENCE.md'}
UNQUALIFIED_CLAIM=re.compile(r'verificad[oa]',re.IGNORECASE)


def ident(identifier, by='owner-0', evidence=True):
    record={'id':identifier,'evidence':None,'verification':None}
    if evidence:
        record['evidence']={'method':'spawn-handle','ref':f'log:{identifier}'}
    if by:
        record['verification']={'by':by,'method':'spawn-handle','ref':f'log:{identifier}','date':'2026-11-05'}
    return record


def run(func, argv):
    out=io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            code=func(argv)
        except SystemExit as exc:
            code=exc.code
    return code,out.getvalue()


def sha(path: Path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()


class GovernanceBase(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        for file in FILES:
            (self.root/file).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/file,self.root/file)
        shutil.copyfile(ROOT/'tests/fixtures/legacy-controls.json',self.root/'quality/controls.json')
        for source in (ROOT/'docs/templates').glob('*.md'):
            shutil.copyfile(source,self.root/'docs/templates'/source.name)

    def mission(self, mid=None, developer=('dev-1',)):
        self.counter=getattr(self,'counter',0)+1
        mid=mid or f'TEST-{100+self.counter}'
        out=create_mission(self.root,mid,'Test','HIGH','orch-1','arch-1')
        m=json.loads((out/'mission.json').read_text(encoding='utf-8'))
        m['roles']={'orchestrator':[ident('orch-1')],'architect':[ident('arch-1')],
                    'developer':[ident(d) for d in developer]}
        return out,m

    def record(self, out, m, name, decision='PASS', reviewer='quality-1', verified_by='owner-0', authors=None):
        authors=authors or ('arch-1' if name=='gate1' else 'dev-1')
        evidence=[]
        for kind in ('identity','isolation','execution'):
            path=out/f'{name}-{kind}.log'
            path.write_text(f'{name} {kind} fixture\n',encoding='utf-8')
            evidence.append({'kind':kind,'path':path.name,'sha256_lf':sha(path)})
        block={'mission':m['id'],'gate':name,'risk':m['risk'],'decision':decision,
               'reviewer':reviewer,'artifact':{'name':'reviewed artifact','ref':'git:29d741e','path':None},
               'effective_authors':[authors], 'authorship_independent':True,
               'isolation':'I2_PERMISOS_SEPARADOS' if m['risk']=='CRITICAL' else 'I1_CONTEXTO_SEPARADO',
               'evidence':evidence,'date':'2026-11-05'}
        verification=({'id':reviewer,'by':verified_by,'method':'spawn-handle',
                       'ref':f'log:{reviewer}','date':'2026-11-05'} if verified_by else None)
        m['gates'][name]={'decision':decision,'review':{'file':REPORTS[name],
            'sha256_lf':'','reviewer_verification':verification}}
        self.write_block(out,m,name,block)

    def write_block(self,out,m,name,block):
        path=out/REPORTS[name]
        path.write_text('# Review\n```protheusai-review\n'+json.dumps(block,ensure_ascii=False)+
                        '\n```\n',encoding='utf-8',newline='\n')
        m['gates'][name]['review']['sha256_lf']=sha(path)

    def block(self,out,name):
        text=(out/REPORTS[name]).read_text(encoding='utf-8')
        return json.loads(text.split('```protheusai-review\n',1)[1].split('\n```',1)[0])

    def mutate_block(self,out,m,name,mutate):
        block=self.block(out,name)
        mutate(block)
        self.write_block(out,m,name,block)

    def full(self, out, m, **kw):
        for name in GATES:
            self.record(out,m,name,**kw)

    def save(self, out, m):
        (out/'mission.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

    def assertMissionError(self, out, m, fragment):
        errs=mission_errors(out,m)
        self.assertTrue(any(fragment in e for e in errs),errs)
        return errs

    def edit_report(self, out, name, old, new):
        path=out/REPORTS[name]
        text=path.read_text(encoding='utf-8')
        self.assertIn(old,text)
        path.write_text(text.replace(old,new),encoding='utf-8')


class TemplateQualityTests(GovernanceBase):
    def test_package_has_all_required_files_and_example_pending(self):
        self.assertEqual([], project_errors(ROOT))
        self.assertEqual(1,run(quality_main,['can-implement','--mission','EXAMPLE-001','--root',str(ROOT)])[0])
        example=json.loads((ROOT/'docs/MISSIONS/EXAMPLE-001/mission.json').read_text(encoding='utf-8'))
        self.assertEqual(3,example['schema_version'])
        self.assertEqual('PENDING',example['gates']['gate1']['decision'])
        self.assertEqual([],example['roles']['developer'])

    def test_new_mission_starts_pending_and_preserves_existing(self):
        out=create_mission(self.root,'TEST-001','Test','MEDIUM','orch-a')
        m=json.loads((out/'mission.json').read_text(encoding='utf-8'))
        self.assertEqual([],mission_errors(out,m))
        self.assertEqual('PENDING',m['gates']['gate1']['decision'])
        # Root cause regression: the creator is never recorded as the implementer.
        self.assertEqual([],m['roles']['developer'])
        self.assertNotIn('implementation_author',m)
        self.assertEqual({'id':'orch-a','evidence':None,'verification':None},m['roles']['orchestrator'][0])
        with self.assertRaises(FileExistsError):
            create_mission(self.root,'TEST-001','No sobrescribir','MEDIUM','orch-a')
        for invisible in ('\u200b',' \u200b '):
            with self.assertRaises(ValueError):
                create_mission(self.root,'TEST-005','T','LOW',invisible)
            with self.assertRaises(ValueError):
                create_mission(self.root,'TEST-005','T','LOW','orch-a',invisible)

    def test_author_alias_is_deprecated_and_only_sets_orchestrator(self):
        code,output=run(new_mission_main,['--id','TEST-002','--title','T','--risk','LOW','--author','dev-01','--root',str(self.root)])
        self.assertEqual(0,code)
        self.assertIn(AUTHOR_DEPRECATED,output)
        m=json.loads((self.root/'docs/MISSIONS/TEST-002/mission.json').read_text(encoding='utf-8'))
        self.assertEqual(['dev-01'],[i['id'] for i in m['roles']['orchestrator']])
        self.assertEqual([],m['roles']['developer'])
        self.assertEqual([],m['roles']['architect'])
        self.assertNotIn('implementation_author',m)
        both=['--id','TEST-003','--title','T','--risk','LOW','--author','a','--orchestrator','b','--root',str(self.root)]
        self.assertNotEqual(0,run(new_mission_main,both)[0])
        self.assertNotEqual(0,run(new_mission_main,['--id','TEST-004','--title','T','--risk','LOW','--root',str(self.root)])[0])
        self.assertFalse((self.root/'docs/MISSIONS/TEST-003').exists())

    def test_full_chain_with_registered_verifications(self):
        out,m=self.mission()
        self.full(out,m)
        m['owner_acceptance'].update(status='APPROVED',approved_by='owner-9',date='2026-11-05')
        self.assertEqual([],mission_errors(out,m))
        self.save(out,m)
        args=['--mission',out.name,'--root',str(self.root)]
        self.assertEqual(0,run(quality_main,['can-implement']+args)[0])
        self.assertEqual(0,run(quality_main,['can-close']+args)[0])
        code,status=run(quality_main,['status']+args)
        self.assertEqual(0,code)
        self.assertIn('no comprobada por la CLI',status)

    def test_no_self_approval_or_missing_evidence(self):
        cases=[('gate1','arch-1',('dev-1',)),('gate1','orch-1',('dev-1',)),('gate2','dev-1',('dev-1',)),
               ('gate2','DEV-2 ',('dev-1','dev-2')),('gate3','ｄｅｖ－１',('dev-1',)),('gate2','dev\u200b-1',('dev-1',))]
        for gate,reviewer,developers in cases:
            with self.subTest(gate=gate,reviewer=reviewer):
                out,m=self.mission(developer=developers)
                for name in GATES[:GATES.index(gate)]:
                    self.record(out,m,name)
                self.record(out,m,gate,reviewer=reviewer,verified_by='owner-0')
                self.assertMissionError(out,m,'self approval')
        out,m=self.mission()
        self.record(out,m,'gate1')
        shutil.copyfile(self.root/'docs/templates/GATE1_REVIEW.md',out/'02-GATE1-REVIEW.md')
        self.assertNotEqual([],mission_errors(out,m))
        for invalid in ('../../secrets.txt','02-GATE1\x00-REVIEW.md'):
            self.record(out,m,'gate1')
            self.assertEqual([],mission_errors(out,m))
            m['gates']['gate1']['review']['file']=invalid
            self.assertNotEqual([],mission_errors(out,m))
        m['gates']['gate1']['review']['file']='02-GATE1-REVIEW.md'
        (out/'02-GATE1-REVIEW.md').write_bytes(b'\xff\xfe no es UTF-8\n')
        self.assertNotEqual([],mission_errors(out,m))
        self.save(out,m)
        self.assertEqual(1,run(quality_main,['validate','--root',str(self.root)])[0])

    def test_must_pass_gate1_before_gate2(self):
        out,m=self.mission()
        self.record(out,m,'gate2')
        self.assertMissionError(out,m,'previous gate lacks PASS')

    def test_gate2_requires_known_developer(self):
        out,m=self.mission(developer=())
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='dev-1')
        self.assertMissionError(out,m,'effective authors invalid')

    def test_identities_need_registered_verification(self):
        cases=[('reviewer',lambda m:m['gates']['gate1']['review'].update(reviewer_verification=None)),
               ('architect',lambda m:m['roles']['architect'][0].update(verification=None)),
               ('reviewer by author',lambda m:m['gates']['gate1']['review']['reviewer_verification'].update(by='arch-1'))]
        for label,mutate in cases:
            with self.subTest(label=label):
                out,m=self.mission()
                m['risk']='CRITICAL'
                self.record(out,m,'gate1')
                self.assertEqual([],mission_errors(out,m))
                mutate(m)
                self.assertNotEqual([],mission_errors(out,m))
        out,m=self.mission()
        self.record(out,m,'gate1',verified_by=None)
        m['roles']['architect'][0]=ident('arch-1',None)
        self.assertEqual([],mission_errors(out,m))

    def test_orchestrator_acting_as_developer(self):
        out,m=self.mission()
        m['roles']['developer']=[ident('orch-1')]
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='orch-1',verified_by='owner-0')
        self.assertEqual([],mission_errors(out,m))
        self.record(out,m,'gate2',reviewer='orch-1',authors='orch-1',verified_by=None)
        self.assertMissionError(out,m,'self approval')

    def test_report_must_match_manifest(self):
        cases=[('mission',lambda b:b.update(mission='OTHER-001')),
               ('gate',lambda b:b.update(gate='gate1')),
               ('risk',lambda b:b.update(risk='LOW')),
               ('decision FAIL',lambda b:b.update(decision='FAIL')),
               ('decision PWR',lambda b:b.update(decision='PASS_WITH_RESERVATIONS')),
               ('reviewer missing',lambda b:b.update(reviewer='')),
               ('reviewer author',lambda b:b.update(reviewer='dev-1')),
               ('independence false',lambda b:b.update(authorship_independent=False)),
               ('independence absent',lambda b:b.pop('authorship_independent')),
               ('independence type',lambda b:b.update(authorship_independent='true')),
               ('author absent',lambda b:b.pop('effective_authors')),
               ('author foreign',lambda b:b.update(effective_authors=['dev-1','intruso'])),
               ('author empty',lambda b:b.update(effective_authors=[])),
               ('extra key',lambda b:b.update(extra='x'))]
        for label,mutate in cases:
            with self.subTest(label=label):
                out,m=self.mission()
                self.record(out,m,'gate1')
                self.record(out,m,'gate2',verified_by=None)
                self.assertEqual([],mission_errors(out,m))
                self.mutate_block(out,m,'gate2',mutate)
                self.assertNotEqual([],mission_errors(out,m))

    def test_effective_author_may_be_subset_of_developers(self):
        out,m=self.mission(developer=('dev-1','dev-2'))
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='DEV-2')
        self.assertEqual([],mission_errors(out,m))

    def test_reviewed_artifact_requires_name_and_version(self):
        for name,ref in [('',f'sha256:{HASH}'),('plan',f'sha256:{"a"*63}'),
                         ('plan',f'sha256:{"a"*65}'),('plan',''),('diff','git:12345')]:
            with self.subTest(name=name,ref=ref):
                out,m=self.mission()
                self.record(out,m,'gate1')
                self.assertEqual([],mission_errors(out,m))
                self.mutate_block(out,m,'gate1',lambda b:b.update(artifact={'name':name,'ref':ref,'path':None}))
                self.assertMissionError(out,m,'artifact invalid')

    def test_fail_must_be_traceable_but_never_enables(self):
        out,m=self.mission()
        m['gates']['gate1']['decision']='FAIL'
        self.assertNotEqual([],mission_errors(out,m))
        self.record(out,m,'gate1',decision='FAIL',verified_by=None)
        self.assertEqual([],mission_errors(out,m))
        self.save(out,m)
        self.assertEqual(1,run(quality_main,['can-implement','--mission',out.name,'--root',str(self.root)])[0])
        for field in ('reviewer','date'):
            self.record(out,m,'gate1',decision='FAIL',verified_by=None)
            self.assertEqual([],mission_errors(out,m))
            self.mutate_block(out,m,'gate1',lambda b:b.update({field:''}))
            self.assertNotEqual([],mission_errors(out,m))
        self.record(out,m,'gate1',decision='FAIL',verified_by=None)
        self.mutate_block(out,m,'gate1',lambda b:b.update(decision='PASS'))
        self.assertMissionError(out,m,'review mismatch: decision')
        out2,m2=self.mission('TEST-002',developer=())
        self.record(out2,m2,'gate1')
        self.record(out2,m2,'gate2',decision='FAIL')
        self.assertMissionError(out2,m2,'effective authors invalid')
        out3,m3=self.mission()
        self.record(out3,m3,'gate1',decision='FAIL',verified_by=None)
        self.mutate_block(out3,m3,'gate1',lambda b:b.update(effective_authors=[]))
        self.assertMissionError(out3,m3,'effective authors invalid')
        self.record(out3,m3,'gate1',decision='FAIL',verified_by=None)
        self.mutate_block(out3,m3,'gate1',lambda b:b['artifact'].update(ref='01-PLAN.md'))
        self.assertMissionError(out3,m3,'artifact invalid')

    def test_pass_with_reservations_never_enables(self):
        out,m=self.mission()
        self.record(out,m,'gate1',decision='PASS_WITH_RESERVATIONS')
        self.assertEqual([],mission_errors(out,m))
        self.save(out,m)
        args=['--mission',out.name,'--root',str(self.root)]
        self.assertEqual(1,run(quality_main,['can-implement']+args)[0])
        self.record(out,m,'gate2')
        self.assertMissionError(out,m,'gate2: previous gate lacks PASS')
        self.record(out,m,'gate2',decision='PASS_WITH_RESERVATIONS')
        self.assertMissionError(out,m,'gate2: previous gate lacks PASS')
        out2,m2=self.mission('TEST-002')
        self.full(out2,m2,decision='PASS_WITH_RESERVATIONS')
        m2['owner_acceptance'].update(status='APPROVED',approved_by='owner-9',date='2026-11-05')
        self.assertMissionError(out2,m2,'owner APPROVED requires three PASS')
        self.save(out2,m2)
        self.assertEqual(1,run(quality_main,['can-close','--mission','TEST-002','--root',str(self.root)])[0])
        out3,m3=self.mission('TEST-003')
        self.record(out3,m3,'gate1')
        self.record(out3,m3,'gate2',decision='PASS_WITH_RESERVATIONS',reviewer='dev-1',verified_by='owner-0')
        self.assertMissionError(out3,m3,'self approval')

    def test_owner_approval_cannot_come_from_authors(self):
        for approver,developer in (('dev-1','dev-1'),('ARCH-1','dev-1'),('Ｏｒｃｈ-1','orch-1')):
            with self.subTest(approver):
                out,m=self.mission(developer=(developer,))
                self.record(out,m,'gate1')
                for name in ('gate2','gate3'):
                    self.record(out,m,name,authors=developer,verified_by='owner-0')
                m['owner_acceptance'].update(status='APPROVED',approved_by='owner-9',date='2026-11-05')
                self.assertEqual([],mission_errors(out,m))
                m['owner_acceptance']['approved_by']=approver
                self.assertEqual(['owner approval by author'],mission_errors(out,m))
                self.save(out,m)
                self.assertEqual(1,run(quality_main,['can-close','--mission',out.name,'--root',str(self.root)])[0])

    def test_malformed_records_fail_without_exceptions(self):
        def dup_dev(m): m['roles']['developer']=[ident('dev-1'),ident('DEV-1')]
        def drop_gate3(m): del m['gates']['gate3']
        mutations={
            'schema bool':lambda m:m.update(schema_version=True),
            'schema str':lambda m:m.update(schema_version='2'),
            'schema 4':lambda m:m.update(schema_version=4),
            'schema ausente':lambda m:m.pop('schema_version'),
            'gates lista':lambda m:m.update(gates=[]),
            'gate no objeto':lambda m:m['gates'].update(gate1=[]),
            'gate ausente':drop_gate3,
            'gate extra':lambda m:m['gates'].update(gate4={}),
            'decision lista':lambda m:m['gates']['gate1'].update(decision=[]),
            'decision null':lambda m:m['gates']['gate1'].update(decision=None),
            'decision desconocida':lambda m:m['gates']['gate1'].update(decision='OK'),
            'review no objeto':lambda m:m['gates']['gate1'].update(review=5),
            'owner no objeto':lambda m:m.update(owner_acceptance=[]),
            'owner status no texto':lambda m:m['owner_acceptance'].update(status=1),
            'roles ausente':lambda m:m.pop('roles'),
            'rol desconocido':lambda m:m['roles'].update(reviewer=[]),
            'rol no lista':lambda m:m['roles'].update(developer={}),
            'orchestrator vacío':lambda m:m['roles'].update(orchestrator=[]),
            'id vacío':lambda m:m['roles']['architect'].append({'id':'','evidence':None,'verification':None}),
            'id espacios':lambda m:m['roles']['architect'].append({'id':'   ','evidence':None,'verification':None}),
            'identidad incompleta':lambda m:m['roles']['architect'].append({'id':'x'}),
            'verification texto':lambda m:m['roles']['architect'][0].update(verification='VERIFIED'),
            'verification sin evidence':lambda m:m['roles']['architect'][0].update(evidence=None),
            'evidence ref vacía':lambda m:m['roles']['architect'][0]['evidence'].update(ref=' '),
            'verification sin campo':lambda m:m['roles']['architect'][0]['verification'].pop('date'),
            'autoverificación':lambda m:m['roles']['architect'][0]['verification'].update(by=' ARCH-1'),
            'identidad duplicada':dup_dev,
            'reviewer vacío':lambda m:m['gates']['gate1'].update(reviewer={}),
            'mixto implementation_author':lambda m:m.update(implementation_author='dev-1'),
            'mixto reviewer_id':lambda m:m['gates']['gate1'].update(reviewer_id='q'),
        }
        base_out,base=self.mission('TEST-001')
        for label,mutate in mutations.items():
            with self.subTest(label):
                m=copy.deepcopy(base)
                mutate(m)
                self.assertNotEqual([],mission_errors(base_out,m))
                self.save(base_out,m)
                for command in ('status','can-implement','can-close'):
                    self.assertNotEqual(0,run(quality_main,[command,'--mission','TEST-001','--root',str(self.root)])[0])
                self.assertNotEqual(0,run(quality_main,['validate','--root',str(self.root)])[0])

    def test_v1_manifests_are_historical(self):
        folder=self.root/'docs/MISSIONS/HIST-001'
        folder.mkdir(parents=True)
        for file in MISSION_FILES:
            (folder/file).write_text(f'# {file}\nRevisor quality-x\nDictamen: PASS\nInforme histórico real.\n',encoding='utf-8')
        manifest={'schema_version':1,'id':'HIST-001','title':'Histórico','risk':'HIGH','author':'orch-x',
                  'implementation_author':'orch-x','created_at':'2026-11-04',
                  'gates':{n:{'decision':'PASS','reviewer_id':'quality-x','reviewed_artifact':f'{REPORTS[n]} sha256:{HASH}',
                              'evidence_file':REPORTS[n],'date':'2026-11-04'} for n in GATES},
                  'owner_acceptance':{'status':'PENDING','approved_by':None,'date':None}}
        path=folder/'mission.json'
        path.write_text(json.dumps(manifest,indent=4),encoding='utf-8')
        before=path.read_bytes()
        code,output=run(quality_main,['validate','--root',str(self.root)])
        self.assertEqual(0,code,output)
        self.assertIn('AVISO: HIST-001 v1',output)
        args=['--mission','HIST-001','--root',str(self.root)]
        self.assertEqual(1,run(quality_main,['can-implement']+args)[0])
        self.assertEqual(1,run(quality_main,['can-close']+args)[0])
        code,output=run(quality_main,['status']+args)
        self.assertEqual(0,code)
        self.assertIn('v1 hist',output)
        self.assertEqual(before,path.read_bytes())
        manifest['gates']['gate1']['reviewer_id']='ORCH-X'
        self.assertEqual([],mission_errors(folder,manifest))
        for gate in manifest['gates'].values():
            gate.update(decision='PENDING')
        manifest['gates']['gate1']['reviewer_id']=None
        self.assertEqual([],mission_errors(folder,manifest))

    def test_cli_never_claims_identity_checks(self):
        messages=[]
        out,m=self.mission()
        self.full(out,m)
        self.save(out,m)
        for command in ('status','can-implement','can-close'):
            messages.append(run(quality_main,[command,'--mission',out.name,'--root',str(self.root)])[1])
        messages.append(run(quality_main,['validate','--root',str(self.root)])[1])
        m['roles']['developer'][0]=ident('dev-1',None)
        messages+=mission_errors(out,m)
        self.save(out,m)
        messages.append(run(quality_main,['status','--mission',out.name,'--root',str(self.root)])[1])
        self.assertTrue(any('no comprobada por la CLI' in text for text in messages))
        for text in messages:
            for line in text.splitlines():
                if UNQUALIFIED_CLAIM.search(line):
                    self.assertRegex(line,r'registrad[oa]|no comprobada por la CLI')

    def test_filled_templates_satisfy_report_rules(self):
        out,m=self.mission()
        for name in GATES:
            self.record(out,m,name)
            template=(self.root/'docs/templates'/TEMPLATES[name]).read_text(encoding='utf-8')
            self.assertEqual(1,template.count('```protheusai-review'))
            start=template.index('```protheusai-review\n')+len('```protheusai-review\n')
            end=template.index('\n```',start)
            text=template[:start]+json.dumps(self.block(out,name),ensure_ascii=False)+template[end:]
            path=out/REPORTS[name]
            path.write_text(text,encoding='utf-8',newline='\n')
            m['gates'][name]['review']['sha256_lf']=sha(path)
        self.assertEqual([],mission_errors(out,m))

if __name__=='__main__':
    unittest.main()
