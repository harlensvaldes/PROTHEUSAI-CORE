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
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GovernanceBase(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        for file in FILES:
            (self.root/file).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/file,self.root/file)
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

    def record(self, out, m, name, decision='PASS', reviewer='quality-1', verified_by='orch-1',
               authors=None, independence='sí — subagente distinto del autor, log:quality-1'):
        artifact=f'01-PLAN.md sha256:{HASH}' if name=='gate1' else f'diff git:29d741e..{"b"*40}'
        authors=authors or ('arch-1' if name=='gate1' else 'dev-1')
        (out/REPORTS[name]).write_text('\n'.join([
            f'# {name}', f'**Dictamen:** {decision}', f'**Revisor:** {reviewer}',
            f'**Verificación de identidad:** spawn-handle log:{reviewer}',
            f'**Independencia verificada:** {independence}',
            f'**Artefacto revisado:** {artifact}', f'**Autor efectivo:** {authors}',
            '', 'Hallazgos: ninguno bloqueante.', '']),encoding='utf-8')
        m['gates'][name].update(decision=decision,reviewer=ident(reviewer,verified_by),
                                reviewed_artifact=artifact,evidence_file=REPORTS[name],date='2026-11-05')

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
        self.assertEqual(2,example['schema_version'])
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
                self.assertMissionError(out,m,'autoaprobación')
        out,m=self.mission()
        self.record(out,m,'gate1')
        shutil.copyfile(self.root/'docs/templates/GATE1_REVIEW.md',out/'02-GATE1-REVIEW.md')
        self.assertMissionError(out,m,'falta informe independiente')
        m['gates']['gate1']['evidence_file']='../../secrets.txt'
        self.assertMissionError(out,m,'falta informe independiente')
        m['gates']['gate1']['evidence_file']='02-GATE1\x00-REVIEW.md'
        self.assertMissionError(out,m,'falta informe independiente')
        m['gates']['gate1']['evidence_file']='02-GATE1-REVIEW.md'
        (out/'02-GATE1-REVIEW.md').write_bytes(b'**Dictamen:** PASS\n\xff\xfe no es UTF-8\n')
        self.assertMissionError(out,m,'falta informe independiente')
        self.save(out,m)
        self.assertEqual(1,run(quality_main,['validate','--root',str(self.root)])[0])

    def test_must_pass_gate1_before_gate2(self):
        out,m=self.mission()
        self.record(out,m,'gate2')
        self.assertMissionError(out,m,'Gate anterior no tiene PASS')

    def test_gate2_requires_known_developer(self):
        out,m=self.mission(developer=())
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='dev-1')
        self.assertMissionError(out,m,'developer vacío')

    def test_identities_need_registered_verification(self):
        cases=[
            ('revisor solo con evidencia',lambda m:m['gates']['gate1'].update(reviewer=ident('quality-1',None)),'gate1: revisor sin verificación registrada'),
            ('revisor solo declarado',lambda m:m['gates']['gate1'].update(reviewer=ident('quality-1',None,False)),'gate1: revisor sin verificación registrada'),
            ('architect solo declarado',lambda m:m['roles']['architect'].__setitem__(0,ident('arch-1',None,False)),'gate1: architect arch-1 sin verificación registrada'),
            ('developer solo con evidencia',lambda m:m['roles']['developer'].__setitem__(0,ident('dev-1',None)),'gate2: developer dev-1 sin verificación registrada'),
            ('orchestrator solo declarado',lambda m:m['roles']['orchestrator'].__setitem__(0,ident('orch-1',None,False)),'gate1: orchestrator orch-1 sin verificación registrada'),
            ('revisor verificado por el autor revisado',lambda m:m['gates']['gate2']['reviewer']['verification'].update(by='dev-1'),'gate2: revisor registrado como verificado por el autor revisado'),
        ]
        for label,mutate,fragment in cases:
            with self.subTest(label):
                out,m=self.mission()
                self.full(out,m)
                mutate(m)
                self.assertMissionError(out,m,fragment)

    def test_orchestrator_acting_as_developer(self):
        out,m=self.mission()
        m['roles']['developer']=[ident('orch-1')]
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='orch-1',verified_by='owner-0')
        self.assertEqual([],mission_errors(out,m))
        m['gates']['gate2']['reviewer']['verification']['by']='ORCH-1'
        self.assertMissionError(out,m,'verificado por el autor revisado')
        self.record(out,m,'gate2',reviewer='orch-1',authors='orch-1',verified_by='owner-0')
        self.assertMissionError(out,m,'autoaprobación')

    def test_report_must_match_manifest(self):
        cases=[
            ('suplantación de revisor','**Revisor:** quality-1','**Revisor:** dev-1','Revisor'),
            ('revisor ausente','**Revisor:** quality-1','','Revisor'),
            ('revisor duplicado','**Revisor:** quality-1','**Revisor:** quality-1\n**Revisor:** quality-1','Revisor'),
            ('dictamen FAIL en informe','**Dictamen:** PASS','**Dictamen:** FAIL','Dictamen'),
            ('dictamen con reservas en informe','**Dictamen:** PASS','**Dictamen:** PASS_WITH_RESERVATIONS','Dictamen'),
            ('dictamen duplicado','**Dictamen:** PASS','**Dictamen:** PASS\n**Dictamen:** FAIL','Dictamen'),
            ('independencia negada','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** no; no se pudo acreditar separación','independencia no acreditada'),
            ('independencia sin evidencia','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí','independencia no acreditada'),
            ('independencia marcador','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí — [evidencia]','independencia no acreditada'),
            ('independencia duplicada','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí — a\n**Independencia verificada:** sí — b','independencia no acreditada'),
            ('artefacto distinto',f'git:29d741e..{"b"*40}',f'git:29d741e..{"c"*40}','Artefacto revisado'),
            ('autor efectivo ausente','**Autor efectivo:** dev-1','','Autor efectivo'),
            ('autor efectivo ajeno','**Autor efectivo:** dev-1','**Autor efectivo:** dev-1, intruso','Autor efectivo'),
            ('autor efectivo vacío','**Autor efectivo:** dev-1','**Autor efectivo:** ','Autor efectivo'),
            ('autor efectivo duplicado','**Autor efectivo:** dev-1','**Autor efectivo:** dev-1\n**Autor efectivo:** dev-1','Autor efectivo'),
            ('independencia afirmación vacía de contenido','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** si — no','independencia no acreditada'),
            ('independencia «no» tras doble guion','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí -- no','independencia no acreditada'),
            ('independencia «no» entre comillas','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí — «no»','independencia no acreditada'),
        ]
        for label,old,new,fragment in cases:
            with self.subTest(label):
                out,m=self.mission()
                self.record(out,m,'gate1')
                self.record(out,m,'gate2')
                self.assertEqual([],mission_errors(out,m))
                self.edit_report(out,'gate2',old,new)
                self.assertMissionError(out,m,fragment)

    def test_effective_author_may_be_subset_of_developers(self):
        out,m=self.mission(developer=('dev-1','dev-2'))
        self.record(out,m,'gate1')
        self.record(out,m,'gate2',authors='DEV-2')
        self.assertEqual([],mission_errors(out,m))

    def test_reviewed_artifact_requires_name_and_version(self):
        bad=[f'sha256:{HASH}', f'01-PLAN.md sha256:{"a"*63}', f'01-PLAN.md sha256:{"a"*65}', '01-PLAN.md', 'diff git:12345']
        for artifact in bad:
            with self.subTest(artifact):
                out,m=self.mission()
                self.record(out,m,'gate1')
                self.edit_report(out,'gate1',f'01-PLAN.md sha256:{HASH}',artifact)
                m['gates']['gate1']['reviewed_artifact']=artifact
                self.assertMissionError(out,m,'reviewed_artifact requiere')

    def test_fail_must_be_traceable_but_never_enables(self):
        out,m=self.mission()
        m['gates']['gate1']['decision']='FAIL'
        errs=mission_errors(out,m)
        for fragment in ('falta revisor','falta informe','reviewed_artifact requiere','falta fecha'):
            self.assertTrue(any(fragment in e for e in errs),(fragment,errs))
        self.record(out,m,'gate1',decision='FAIL',verified_by=None)
        m['gates']['gate1']['reviewer']=ident('quality-1',None,False)
        self.assertEqual([],mission_errors(out,m))
        self.save(out,m)
        self.assertEqual(1,run(quality_main,['can-implement','--mission',out.name,'--root',str(self.root)])[0])
        self.edit_report(out,'gate1','**Dictamen:** FAIL','**Dictamen:** PASS')
        self.assertMissionError(out,m,'Dictamen')
        out2,m2=self.mission('TEST-002',developer=())
        self.record(out2,m2,'gate1')
        self.record(out2,m2,'gate2',decision='FAIL',authors='dev-1')
        self.assertMissionError(out2,m2,'developer vacío')
        out3,m3=self.mission()
        self.record(out3,m3,'gate1',decision='FAIL',verified_by=None)
        self.edit_report(out3,'gate1','**Autor efectivo:** arch-1','')
        self.assertMissionError(out3,m3,'Autor efectivo')
        m3['gates']['gate1']['reviewed_artifact']='01-PLAN.md'
        self.edit_report(out3,'gate1',f'01-PLAN.md sha256:{HASH}','01-PLAN.md')
        self.assertMissionError(out3,m3,'reviewed_artifact requiere')

    def test_pass_with_reservations_never_enables(self):
        out,m=self.mission()
        self.record(out,m,'gate1',decision='PASS_WITH_RESERVATIONS')
        self.assertEqual([],mission_errors(out,m))
        self.save(out,m)
        args=['--mission',out.name,'--root',str(self.root)]
        self.assertEqual(1,run(quality_main,['can-implement']+args)[0])
        self.record(out,m,'gate2')
        self.assertMissionError(out,m,'gate2: Gate anterior no tiene PASS')
        self.record(out,m,'gate2',decision='PASS_WITH_RESERVATIONS')
        self.assertMissionError(out,m,'gate2: Gate anterior no tiene PASS')
        out2,m2=self.mission('TEST-002')
        self.full(out2,m2,decision='PASS_WITH_RESERVATIONS')
        m2['owner_acceptance'].update(status='APPROVED',approved_by='owner-9',date='2026-11-05')
        self.assertMissionError(out2,m2,'owner APPROVED sin tres Gates PASS')
        self.save(out2,m2)
        self.assertEqual(1,run(quality_main,['can-close','--mission','TEST-002','--root',str(self.root)])[0])
        out3,m3=self.mission('TEST-003')
        self.record(out3,m3,'gate1')
        self.record(out3,m3,'gate2',decision='PASS_WITH_RESERVATIONS',reviewer='dev-1',verified_by='owner-0')
        self.assertMissionError(out3,m3,'autoaprobación')

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
                self.assertEqual(['aprobación por autor del trabajo'],mission_errors(out,m))
                self.save(out,m)
                self.assertEqual(1,run(quality_main,['can-close','--mission',out.name,'--root',str(self.root)])[0])

    def test_malformed_records_fail_without_exceptions(self):
        def dup_dev(m): m['roles']['developer']=[ident('dev-1'),ident('DEV-1')]
        def drop_gate3(m): del m['gates']['gate3']
        mutations={
            'schema bool':lambda m:m.update(schema_version=True),
            'schema str':lambda m:m.update(schema_version='2'),
            'schema 3':lambda m:m.update(schema_version=3),
            'schema ausente':lambda m:m.pop('schema_version'),
            'gates lista':lambda m:m.update(gates=[]),
            'gate no objeto':lambda m:m['gates'].update(gate1=[]),
            'gate ausente':drop_gate3,
            'gate extra':lambda m:m['gates'].update(gate4={}),
            'decision lista':lambda m:m['gates']['gate1'].update(decision=[]),
            'decision null':lambda m:m['gates']['gate1'].update(decision=None),
            'decision desconocida':lambda m:m['gates']['gate1'].update(decision='OK'),
            'artefacto no texto':lambda m:m['gates']['gate1'].update(reviewed_artifact=5),
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
        before=sha(path)
        code,output=run(quality_main,['validate','--root',str(self.root)])
        self.assertEqual(0,code,output)
        self.assertIn('AVISO: HIST-001 v1 histórico; no habilita autorizaciones',output)
        args=['--mission','HIST-001','--root',str(self.root)]
        self.assertEqual(1,run(quality_main,['can-implement']+args)[0])
        self.assertEqual(1,run(quality_main,['can-close']+args)[0])
        code,output=run(quality_main,['status']+args)
        self.assertEqual(0,code)
        self.assertIn('v1 histórico',output)
        self.assertEqual(before,sha(path))
        manifest['gates']['gate1']['reviewer_id']='ORCH-X'
        self.assertTrue(any('autoaprobación' in e for e in mission_errors(folder,manifest)))
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
        m['gates']['gate2']['reviewer']['verification']['by']='dev-1'
        m['gates']['gate1']['reviewer']=ident('quality-1',None)
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
            artifact=f'01-PLAN.md sha256:{HASH}' if name=='gate1' else f'diff git:29d741e..{"b"*40}'
            values={'Dictamen':'PASS','Revisor':'quality-1','Verificación de identidad':'spawn-handle log:quality-1',
                    'Independencia verificada':'sí — subagente distinto del autor','Artefacto revisado':artifact,
                    'Autor efectivo':'arch-1' if name=='gate1' else 'dev-1'}
            text=(self.root/'docs/templates'/TEMPLATES[name]).read_text(encoding='utf-8')
            for label,value in values.items():
                text,count=re.subn(rf'^\*\*{re.escape(label)}:\*\*.*$',lambda _:f'**{label}:** {value}',text,flags=re.MULTILINE)
                self.assertEqual(1,count,(name,label))
            (out/REPORTS[name]).write_text(text,encoding='utf-8')
            m['gates'][name].update(decision='PASS',reviewer=ident('quality-1','orch-1'),reviewed_artifact=artifact,
                                    evidence_file=REPORTS[name],date='2026-11-05')
        self.assertEqual([],mission_errors(out,m))


if __name__=='__main__':
    unittest.main()
