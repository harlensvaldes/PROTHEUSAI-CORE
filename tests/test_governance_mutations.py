"""Focused mutation controls: each mutant disables a single named defense in memory.

The production source is never changed. A control survives only if both the
valid fixture remains accepted and the corresponding invalid fixture becomes
accepted by the mutant or raises unexpectedly while the original rejects it.
"""
import copy
import json
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from quality_cli import canon
import quality_v3
import test_governance_v3 as fixtures


class MutationControls(unittest.TestCase):
    setUp = fixtures.GovernanceV3Tests.setUp
    make_case = fixtures.GovernanceV3Tests.make_case
    record = fixtures.GovernanceV3Tests.record
    write_block = fixtures.GovernanceV3Tests.write_block

    def mutant(self, *replacements):
        source = (ROOT / 'scripts/quality_v3.py').read_text(encoding='utf-8')
        for old, new in replacements:
            self.assertEqual(1, source.count(old), old)
            source = source.replace(old, new, 1)
        module = types.ModuleType('isolated_governance_mutant')
        exec(compile(source, '<isolated governance mutant>', 'exec'), module.__dict__)
        return module

    def policy(self):
        return json.loads((self.root / 'quality/controls.json').read_text(encoding='utf-8'))

    def check_gate(self, changes, replacements, diagnostic, policy_change=None):
        folder, manifest = self.make_case()
        block = self.record(folder, manifest, 'gate1')
        policy = self.policy()
        if policy_change:
            policy_change(policy)
        mutant = self.mutant(*replacements)
        def errors(module):
            a, b = module.gate_errors(folder, manifest, 'gate1', policy, canon)
            return a + b
        self.assertEqual([], errors(quality_v3))
        self.assertEqual([], errors(mutant))
        changes(block, manifest, folder)
        self.write_block(folder, manifest, 'gate1', block)
        self.assertTrue(any(diagnostic in item for item in errors(quality_v3)), errors(quality_v3))
        self.assertEqual([], errors(mutant))

    def test_authorship_mutants(self):
        variants = [
            ('reviewer author', lambda b, m, f: b.update(reviewer=' ARCH ')),
            ('declaration false', lambda b, m, f: b.update(authorship_independent=False)),
        ]
        for name, change in variants:
            with self.subTest(name=name):
                self.check_gate(change, [("if reviewer in all_authors or block['authorship_independent'] is not True:",
                                          'if False:')], 'self approval')
                self.tearDown_case()

    def tearDown_case(self):
        # Reuse the fixture's fixed mission ID without disturbing other test files.
        import shutil
        shutil.rmtree(self.root / 'docs/MISSIONS/TEST-100')

    def test_effective_author_mutant(self):
        self.check_gate(lambda b,m,f:b.update(effective_authors=['intruder']),
                        [("not {canon(a) for a in effective} <= allowed):", 'False):')],
                        'effective authors invalid')

    def test_i0_allowed_without_absolute_prohibition(self):
        folder, m = self.make_case()
        block = self.record(folder, m, 'gate1')
        policy = self.policy()
        policy['independence_minimums']['HIGH']['gate1']['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        block['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        self.write_block(folder, m, 'gate1', block)
        self.assertEqual(([], []), quality_v3.gate_errors(folder, m, 'gate1', policy, canon))


    def test_review_equalities_mutants(self):
        for key, value in [('mission','OTHER'),('gate','gate2'),('risk','LOW'),('decision','FAIL')]:
            with self.subTest(key=key):
                def change(block, manifest, folder):
                    block[key] = value
                # write_block follows the block decision: restore manifest PASS afterward.
                folder, manifest = self.make_case()
                block = self.record(folder,manifest,'gate1')
                policy = self.policy()
                mutant = self.mutant(("if block.get(key) != expected:",
                                      f"if key != '{key}' and block.get(key) != expected:"))
                self.assertEqual(([],[]),quality_v3.gate_errors(folder,manifest,'gate1',policy,canon))
                self.assertEqual(([],[]),mutant.gate_errors(folder,manifest,'gate1',policy,canon))
                change(block,manifest,folder)
                self.write_block(folder,manifest,'gate1',block)
                manifest['gates']['gate1']['decision']='PASS'
                errors, minima=quality_v3.gate_errors(folder,manifest,'gate1',policy,canon)
                self.assertIn('review mismatch: '+key,errors)
                self.assertEqual(([],[]),mutant.gate_errors(folder,manifest,'gate1',policy,canon))
                self.tearDown_case()

    def test_artifact_grammar_mutant(self):
        self.check_gate(lambda b,m,f:b['artifact'].update(ref='git:bad'),
                        [("not REF.fullmatch(artifact['ref'])", 'False')], 'artifact invalid')

    def test_review_hash_mutant(self):
        folder,manifest=self.make_case()
        self.record(folder,manifest,'gate1')
        policy=self.policy()
        mutant=self.mutant(("if digest(data).lower() != review['sha256_lf'].lower():",'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,manifest,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,manifest,'gate1',policy,canon))
        manifest['gates']['gate1']['review']['sha256_lf']='a'*64
        errors,_=quality_v3.gate_errors(folder,manifest,'gate1',policy,canon)
        self.assertIn('review hash mismatch',errors)
        self.assertEqual(([],[]),mutant.gate_errors(folder,manifest,'gate1',policy,canon))

    def test_excluded_evidence_mutant(self):
        def change(b,m,f):
            b['evidence'][0]['path']='01-PLAN.md'
            b['evidence'][0]['sha256_lf']=quality_v3.digest((f/'01-PLAN.md').read_bytes())
        self.check_gate(change, [('name in FILES or name ==', 'False or name ==')],
                        'evidence excluded')

    def test_missing_required_evidence_mutant(self):
        # Mutate both checks that enforce the same evidence requirement; otherwise
        # the calculated guarantee independently rejects the missing evidence.
        self.check_gate(lambda b,m,f:b.update(evidence=[]),
                        [("if not set(rule['evidence']) <= present:", 'if False:'),
                         ("if GUARANTEE.index(level) < GUARANTEE.index(rule['guarantee']):", 'if False:')],
                        'required evidence missing')

    def test_evidence_hash_mutant(self):
        def change(b,m,f):
            b['evidence'][0]['sha256_lf']='f'*64
        # Mark the evidence as present when the integrity comparison is bypassed.
        self.check_gate(change,
                        [("if digest(path.read_bytes()).lower() != item['sha256_lf'].lower():", 'if False:')],
                        'evidence hash mismatch')

    def test_noncanonical_path_mutant(self):
        folder,m=self.make_case()
        policy=self.policy()
        self.record(folder,m,'gate1')
        mutant=self.mutant(("if not isinstance(name, str) or not PATH.fullmatch(name):", 'if not isinstance(name, str):'))
        target=folder/'file with space.txt'
        target.write_text('evidence',encoding='utf-8')
        self.assertIsNotNone(quality_v3.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNone(quality_v3.canonical_file(folder,target.name))
        self.assertEqual(target,mutant.canonical_file(folder,target.name))

    def test_invalid_fence_mutant(self):
        mutant=self.mutant(("if len(starts) != 1:", 'if not starts:'))
        block={'a':1}
        data=b'```protheusai-review\n'+json.dumps(block).encode()+b'\n```\n'
        # Use a complete valid block so that only the duplicate fence is in question.
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        data=(folder/'gate1-review.md').read_bytes()
        self.assertIsNotNone(quality_v3.parse_block(data))
        self.assertIsNotNone(mutant.parse_block(data))
        doubled=data+data
        self.assertIsNone(quality_v3.parse_block(doubled))
        self.assertIsNotNone(mutant.parse_block(doubled))

    def test_matrix_monotonicity_mutant(self):
        mutant=self.mutant(("if (ISOLATION.index(a['isolation']) > ISOLATION.index(b['isolation']) or",
                            "if (False or"))
        policy=self.policy()
        self.assertEqual([],quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))
        policy['independence_minimums']['CRITICAL']['gate1']['isolation']='I0_CONTEXTO_COMPARTIDO'
        self.assertTrue(quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_g2_reviewer_verifier_mutant(self):
        mutant=self.mutant(("by not in forbidden and by != target", 'True'))
        valid={'id':'quality','by':'third','method':'log','ref':'log:1','date':'2026-11-05'}
        invalid=dict(valid,by='arch')
        args=('quality', {'quality','arch'}, canon)
        self.assertTrue(quality_v3.valid_verification(valid,*args,reviewer=True))
        self.assertTrue(mutant.valid_verification(valid,*args,reviewer=True))
        self.assertFalse(quality_v3.valid_verification(invalid,*args,reviewer=True))
        self.assertTrue(mutant.valid_verification(invalid,*args,reviewer=True))

    def test_pinned_artifact_mutant(self):
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        block=self.record(folder,m,'gate2')
        policy=self.policy()
        mutant=self.mutant(("if not pinned:", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate2',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
        block['artifact']['ref']='sha256:'+'a'*64
        self.write_block(folder,m,'gate2',block)
        _,minima=quality_v3.gate_errors(folder,m,'gate2',policy,canon)
        self.assertIn('pinned artifact required',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))

    def test_pinned_input_hash_mutant(self):
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        block=self.record(folder,m,'gate2')
        path=folder/'GATE2-INPUT-05.sha256'
        path.write_bytes(b'input\n')
        block['artifact']={'name':'input','ref':'sha256_lf:'+quality_v3.digest(path.read_bytes()),'path':path.name}
        self.write_block(folder,m,'gate2',block)
        policy=self.policy()
        mutant=self.mutant(("if digest(artifact_path.read_bytes()).lower() != artifact['ref'][10:].lower():", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate2',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
        path.write_bytes(b'altered\n')
        errors,_=quality_v3.gate_errors(folder,m,'gate2',policy,canon)
        self.assertIn('artifact hash mismatch',errors)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))

    def test_g2_reviewer_id_mutant(self):
        mutant=self.mutant(("if reviewer and canon(value['id']) != target:", 'if False:'))
        valid={'id':'quality','by':'third','method':'log','ref':'log:1','date':'2026-11-05'}
        args=('quality', {'quality','arch'}, canon)
        self.assertTrue(quality_v3.valid_verification(valid,*args,reviewer=True))
        self.assertTrue(mutant.valid_verification(valid,*args,reviewer=True))
        invalid=dict(valid,id='other')
        self.assertFalse(quality_v3.valid_verification(invalid,*args,reviewer=True))
        self.assertTrue(mutant.valid_verification(invalid,*args,reviewer=True))

    def test_gate_order_mutant(self):
        folder,m=self.make_case()
        self.record(folder,m,'gate1')
        self.record(folder,m,'gate2')
        policy=self.policy()
        mutant=self.mutant(("if decision in ('PASS', 'PASS_WITH_RESERVATIONS') and not prior:", 'if False:'))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        self.record(folder,m,'gate1',decision='PASS_WITH_RESERVATIONS')
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertTrue(any('previous gate lacks PASS' in x for x in errors))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def test_owner_author_mutant(self):
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'):
            self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        policy=self.policy()
        line="elif canon(owner['approved_by']) in {canon(i['id']) for role in ('architect','developer') for i in mission['roles'][role]}:"
        mutant=self.mutant((line,'elif False:'))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        m['owner_acceptance']['approved_by']='ARCH'
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertIn('owner approval by author',errors)
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def test_matrix_nonmonotonic_guarantee_mutant(self):
        # Negative: MEDIUM G1 falls to HIGH G0 at gate1, with equal evidence.
        policy=self.policy()
        policy['independence_minimums']['MEDIUM']['gate1'].update(guarantee='G1_EVIDENCIA_REGISTRADA',evidence=['identity'])
        policy['independence_minimums']['HIGH']['gate1']['guarantee']='G0_DECLARADA'
        mutant=self.mutant(("GUARANTEE.index(a['guarantee']) > GUARANTEE.index(b['guarantee']) or", 'False or'))
        original=self.policy()
        self.assertEqual([],quality_v3.policy_errors(original))
        self.assertEqual([],mutant.policy_errors(original))
        self.assertTrue(quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_matrix_nonmonotonic_types_mutant(self):
        # Negative: HIGH gate3 drops MEDIUM's execution evidence requirement.
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate3']['evidence']=['identity']
        mutant=self.mutant(("not set(a['evidence']) <= set(b['evidence']) or", 'False or'))
        self.assertEqual([],quality_v3.policy_errors(self.policy()))
        self.assertEqual([],mutant.policy_errors(self.policy()))
        self.assertTrue(quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_matrix_nonmonotonic_pin_mutant(self):
        # Negative: HIGH gate2 drops MEDIUM's pinned-artifact requirement.
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate2']['pinned_artifact']=False
        mutant=self.mutant(("(a['pinned_artifact'] and not b['pinned_artifact'])", 'False'))
        self.assertEqual([],quality_v3.policy_errors(self.policy()))
        self.assertEqual([],mutant.policy_errors(self.policy()))
        self.assertTrue(quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_matrix_g1_empty_types_mutant(self):
        # Negative: HIGH gate1 requires G1 but has no evidence kinds.
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate1']['evidence']=[]
        mutant=self.mutant(("elif guarantee != GUARANTEE[0] and not evidence:", 'elif False:'))
        self.assertEqual([],quality_v3.policy_errors(self.policy()))
        self.assertEqual([],mutant.policy_errors(self.policy()))
        self.assertTrue(any('empty evidence types' in x for x in quality_v3.policy_errors(policy)))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_matrix_invalid_isolation_enum_mutant(self):
        # Negative: an unknown isolation level at HIGH gate1.
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate1']['isolation']='bogus'
        # Adding an invalid enum to the accepted list models the enum check being weakened.
        mutant=self.mutant(("'I1_CONTEXTO_SEPARADO', 'I2_PERMISOS_SEPARADOS'", "'I1_CONTEXTO_SEPARADO', 'bogus', 'I2_PERMISOS_SEPARADOS'"))
        self.assertEqual([],quality_v3.policy_errors(self.policy()))
        self.assertEqual([],mutant.policy_errors(self.policy()))
        self.assertTrue(quality_v3.policy_errors(policy))
        self.assertEqual([],mutant.policy_errors(policy))

    def test_isolation_below_matrix_mutant(self):
        # Negative: I1 declared where HIGH gate1 policy requires I2.
        folder,m=self.make_case()
        block=self.record(folder,m,'gate1')
        block['isolation']='I2_PERMISOS_SEPARADOS'
        self.write_block(folder,m,'gate1',block)
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate1']['isolation']='I2_PERMISOS_SEPARADOS'
        mutant=self.mutant(("if isolation in ISOLATION and ISOLATION.index(isolation) < ISOLATION.index(rule['isolation']):", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        block['isolation']='I1_CONTEXTO_SEPARADO'
        self.write_block(folder,m,'gate1',block)
        _,minima=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('isolation below minimum',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_reviewer_verification_missing_g2_mutant(self):
        # Negative: CRITICAL gate1 has no reviewer verification; author is verified.
        folder,m=self.make_case('CRITICAL')
        b=self.record(folder,m,'gate1')
        evidence=folder/'isolation.txt'; evidence.write_bytes(b'permissions')
        b['isolation']='I2_PERMISOS_SEPARADOS'
        b['evidence'].append({'kind':'isolation','path':evidence.name,'sha256_lf':quality_v3.digest(evidence.read_bytes())})
        self.write_block(folder,m,'gate1',b)
        m['roles']['architect'][0]['evidence']={'method':'log','ref':'x'}
        m['roles']['architect'][0]['verification']={'by':'third','method':'log','ref':'x','date':'2026-11-05'}
        v={'id':'quality','by':'third','method':'log','ref':'x','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']=v
        policy=self.policy()
        # The G2 calculated level and explicit G2 check both require this function.
        original="reviewer_verified = valid_verification(verification, reviewer, forbidden, canon, True)"
        explicit="if not valid_verification(verification, reviewer, forbidden, canon, True):"
        mutant=self.mutant((original,'reviewer_verified = True'),(explicit,'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        m['gates']['gate1']['review']['reviewer_verification']=None
        _,minima=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('reviewer verification required',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_parser_nested_fence_mutant(self):
        # Negative: an extra fence occurs inside a review block.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        data=(folder/'gate1-review.md').read_bytes()
        mutant=self.mutant(("or any(line.startswith('```') for line in lines[start+1:end])", 'or False'))
        self.assertIsNotNone(quality_v3.parse_block(data)); self.assertIsNotNone(mutant.parse_block(data))
        nested=data.replace(b'```protheusai-review\n',b'```protheusai-review\n```python\n')
        # Remove the injected line only in the mutant's JSON decoder, preserving a
        # valid payload while disabling nested-fence rejection.
        self.assertIsNone(quality_v3.parse_block(nested))
        # A parser mutant ignoring nested fences must ignore the injected fence as syntax.
        mutant=self.mutant(("or any(line.startswith('```') for line in lines[start+1:end])", 'or False'),
                           ("json.loads('\\n'.join(lines[start+1:end]), object_pairs_hook=_unique)",
                            "json.loads('\\n'.join(x for x in lines[start+1:end] if not x.startswith('```')), object_pairs_hook=_unique)"))
        self.assertIsNotNone(mutant.parse_block(nested))

    def test_hash_lf_normalization_mutant(self):
        # Negative mutation: the hash function ceases to normalize CRLF.
        mutant=self.mutant(("hashlib.sha256(data.replace(b'\\r\\n', b'\\n')).hexdigest()", 'hashlib.sha256(data).hexdigest()'))
        self.assertEqual(quality_v3.digest(b'a\n'),mutant.digest(b'a\n'))
        self.assertEqual(quality_v3.digest(b'a\r\n'),quality_v3.digest(b'a\n'))
        self.assertNotEqual(mutant.digest(b'a\r\n'),quality_v3.digest(b'a\n'))

    def test_parser_extra_key_mutant(self):
        # Negative: JSON block has an additional key.
        folder,m=self.make_case(); block=self.record(folder,m,'gate1')
        path=folder/'gate1-review.md'
        valid=path.read_bytes()
        mutant=self.mutant(("and set(value) == KEYS else None", 'else None'))
        self.assertIsNotNone(quality_v3.parse_block(valid)); self.assertIsNotNone(mutant.parse_block(valid))
        block['extra']='x'; self.write_block(folder,m,'gate1',block)
        invalid=path.read_bytes()
        self.assertIsNone(quality_v3.parse_block(invalid)); self.assertIsNotNone(mutant.parse_block(invalid))

    def test_parser_nul_mutant(self):
        # Negative: report narrative contains a NUL, with JSON unchanged.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        data=(folder/'gate1-review.md').read_bytes()
        mutant=self.mutant(("if '\\x00' in text:", 'if False:'))
        self.assertIsNotNone(quality_v3.parse_block(data)); self.assertIsNotNone(mutant.parse_block(data))
        data=b'narrative\x00\n'+data
        self.assertIsNone(quality_v3.parse_block(data)); self.assertIsNotNone(mutant.parse_block(data))

    def test_parser_utf8_mutant(self):
        # Negative: report narrative contains malformed UTF-8.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        data=(folder/'gate1-review.md').read_bytes()
        mutant=self.mutant((".decode('utf-8')", ".decode('utf-8', errors='replace')"))
        self.assertIsNotNone(quality_v3.parse_block(data)); self.assertIsNotNone(mutant.parse_block(data))
        data=b'narrative\xff\n'+data
        self.assertIsNone(quality_v3.parse_block(data)); self.assertIsNotNone(mutant.parse_block(data))

    def test_excluded_manifest_mutant(self):
        # Negative: mission.json masquerades as identity evidence.
        def change(b,m,f):
            b['evidence'][0]['path']='mission.json'
            b['evidence'][0]['sha256_lf']=quality_v3.digest((f/'mission.json').read_bytes())
        self.check_gate(change, [("name == 'mission.json'", 'False')], 'evidence excluded')

    def test_g2_author_verification_missing_mutant(self):
        # Negative: CRITICAL gate1 architect lacks third-party verification.
        folder,m=self.make_case('CRITICAL'); b=self.record(folder,m,'gate1')
        path=folder/'isolation.txt'; path.write_bytes(b'permissions')
        b['isolation']='I2_PERMISOS_SEPARADOS'
        b['evidence'].append({'kind':'isolation','path':path.name,'sha256_lf':quality_v3.digest(path.read_bytes())})
        self.write_block(folder,m,'gate1',b)
        author=m['roles']['architect'][0]
        author['evidence']={'method':'log','ref':'x'}
        author['verification']={'by':'third','method':'log','ref':'x','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']={'id':'quality','by':'third','method':'log','ref':'x','date':'2026-11-05'}
        policy=self.policy()
        # Both the calculated G2 and explicit G2 checks independently protect it.
        mutant=self.mutant(("authors_verified = all(valid_verification(i.get('verification'), canon(i['id']), forbidden, canon)\n                           for i in pertinent)", 'authors_verified = True'),
                           ("if not valid_verification(ident.get('verification'), canon(ident['id']), forbidden, canon):", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        author['verification']=None
        _,minima=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('author verification required',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_cli_pwr_cannot_implement_mutant(self):
        # Negative: Gate1 PWR must not enable can-implement.
        import contextlib, io, quality_cli
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="if not errs and m['gates']['gate1']['decision']=='PASS':"
        self.assertEqual(1,source.count(old))
        source=source.replace(old,"if not errs and m['gates']['gate1']['decision'] in ('PASS','PASS_WITH_RESERVATIONS'):")
        mutant=types.ModuleType('isolated_cli_mutant')
        mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source,'<isolated cli mutant>','exec'),mutant.__dict__)
        args=['can-implement','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()): return module.main(args)
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        self.record(folder,m,'gate1',decision='PASS_WITH_RESERVATIONS')
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_matrix_missing_mutant(self):
        # Negative: controls have no independence_minimums matrix.
        mutant=self.mutant(("return ['controls: missing or incomplete independence_minimums']", 'return []'))
        valid=self.policy(); invalid=copy.deepcopy(valid); del invalid['independence_minimums']
        self.assertEqual([],quality_v3.policy_errors(valid)); self.assertEqual([],mutant.policy_errors(valid))
        self.assertTrue(quality_v3.policy_errors(invalid)); self.assertEqual([],mutant.policy_errors(invalid))

    def test_matrix_missing_gate_mutant(self):
        # Negative: HIGH has no gate2 rule.
        mutant=self.mutant(("errs.append('controls: incomplete ' + risk)", 'pass'))
        valid=self.policy(); invalid=copy.deepcopy(valid); del invalid['independence_minimums']['HIGH']['gate2']
        self.assertEqual([],quality_v3.policy_errors(valid)); self.assertEqual([],mutant.policy_errors(valid))
        self.assertTrue(quality_v3.policy_errors(invalid))
        with self.assertRaises(KeyError):
            mutant.policy_errors(invalid)

    def test_parser_missing_key_mutant(self):
        # Negative: JSON review lacks the authorship_independent key.
        folder,m=self.make_case(); b=self.record(folder,m,'gate1'); path=folder/'gate1-review.md'
        valid=path.read_bytes()
        mutant=self.mutant(("and set(value) == KEYS else None", 'else None'))
        self.assertIsNotNone(quality_v3.parse_block(valid)); self.assertIsNotNone(mutant.parse_block(valid))
        del b['authorship_independent']; self.write_block(folder,m,'gate1',b)
        self.assertIsNone(quality_v3.parse_block(path.read_bytes()))
        self.assertIsNotNone(mutant.parse_block(path.read_bytes()))

    def test_junction_path_mutant(self):
        # Negative: a path traverses a directory reported as a junction.
        # This mocks the filesystem junction signal, not a real Windows junction.
        from unittest.mock import patch
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        directory=folder/'junction'; directory.mkdir(); target=directory/'record.txt'; target.write_bytes(b'evidence')
        mutant=self.mutant(("if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):", 'if False:'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,'junction/record.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'junction/record.txt'))
        with patch.object(Path,'is_junction',lambda p:p.name=='junction',create=True):
            self.assertIsNone(quality_v3.canonical_file(folder,'junction/record.txt'))
            self.assertIsNotNone(mutant.canonical_file(folder,'junction/record.txt'))

    def test_excluded_review_mutant(self):
        # Negative: the review report itself is used as identity evidence.
        # Hashing it into its own block is circular, so exercise exclusion at
        # gate level while neutralizing only the independent digest check.
        folder,m=self.make_case(); block=self.record(folder,m,'gate1'); policy=self.policy()
        mutant=self.mutant(("name == review['file']", 'False'),
                           ("if digest(path.read_bytes()).lower() != item['sha256_lf'].lower():", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        block['evidence'][0]['path']='gate1-review.md'; self.write_block(folder,m,'gate1',block)
        errors,_=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('evidence excluded, duplicated or invalid',errors)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_cli_historical_v2_cannot_implement_mutant(self):
        # Negative: structurally valid schema v2 with PASS cannot authorize implementation.
        import contextlib, io, quality_cli
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="if legacy:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')"
        self.assertEqual(2,source.count(old))
        source=source.replace(old,"if False:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')",1)
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source,'<isolated cli mutant>','exec'),mutant.__dict__)
        args=['can-implement','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()): return module.main(args)
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        m['schema_version']=2
        m['gates']={g:{'decision':m['gates'][g]['decision'],'reviewer':None,
                       'reviewed_artifact':None,'evidence_file':None,'date':None} for g in ('gate1','gate2','gate3')}
        self.assertEqual([],quality_cli.structure_errors(m))
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_cli_approved_matrix_can_close_mutant(self):
        # Negative: accepted HIGH mission falls below newly tightened matrix.
        import contextlib, io, quality_cli
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="else: errs+=v3_errors(folder,m,policy,canon,True)[1]"
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,'else: pass'),'<isolated cli mutant>','exec'),mutant.__dict__)
        args=['can-close','--mission',folder.name,'--root',str(self.root)]
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        def invoke(module):
            with contextlib.redirect_stdout(io.StringIO()): return module.main(args)
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        policy=self.policy()
        policy['independence_minimums']['HIGH']['gate1']['isolation']='I2_PERMISOS_SEPARADOS'
        (self.root/'quality/controls.json').write_text(json.dumps(policy),encoding='utf-8')
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_gate3_missing_execution_mutant(self):
        # Negative: HIGH gate3 has identity evidence but no execution evidence.
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): block=self.record(folder,m,gate)
        policy=self.policy()
        mutant=self.mutant(("if not set(rule['evidence']) <= present:", 'if False:'),
                           ("if GUARANTEE.index(level) < GUARANTEE.index(rule['guarantee']):", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate3',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate3',policy,canon))
        block['evidence']=[e for e in block['evidence'] if e['kind']!='execution']
        self.write_block(folder,m,'gate3',block)
        _,minima=quality_v3.gate_errors(folder,m,'gate3',policy,canon)
        self.assertIn('required evidence missing',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate3',policy,canon))

    def test_evidence_unknown_kind_mutant(self):
        # Negative: additional evidence has a non-enumerated kind.
        def change(b,m,f):
            path=f/'other.txt'; path.write_bytes(b'other')
            b['evidence'].append({'kind':'unapproved','path':path.name,'sha256_lf':quality_v3.digest(path.read_bytes())})
        self.check_gate(change, [("KINDS = {'identity', 'isolation', 'execution'}", "KINDS = {'identity', 'isolation', 'execution', 'unapproved'}")], 'evidence entry invalid')

    def test_excluded_reviewed_artifact_mutant(self):
        # Negative: reviewed artifact is reused as the required identity evidence.
        def change(b,m,f):
            path=f/'identity-gate1.txt'
            b['artifact']={'name':'artifact','ref':'sha256_lf:'+quality_v3.digest(path.read_bytes()),'path':path.name}
        self.check_gate(change, [("(artifact_path is not None and path is not None and path.resolve() == artifact_path.resolve())", 'False')], 'evidence excluded')

    def test_parser_absent_block_mutant(self):
        # Negative: report has no fenced block. The mutant fabricates a block
        # when the fence check fails; this models fail-open recovery.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        valid=(folder/'gate1-review.md').read_bytes()
        old="if len(starts) != 1:\n        return None"
        mutant=self.mutant((old,"if len(starts) != 1:\n        return {k: None for k in KEYS}"))
        self.assertIsNotNone(quality_v3.parse_block(valid)); self.assertIsNotNone(mutant.parse_block(valid))
        self.assertIsNone(quality_v3.parse_block(b'no structured block'))
        self.assertIsNotNone(mutant.parse_block(b'no structured block'))

    def test_parser_invalid_json_mutant(self):
        # Negative: fenced review contains malformed JSON. Fail-open recovery
        # returns a placeholder dict instead of rejecting the parse error.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        valid=(folder/'gate1-review.md').read_bytes()
        old="except (ValueError, TypeError):\n        return None"
        mutant=self.mutant((old,"except (ValueError, TypeError):\n        return {k: None for k in KEYS}"))
        self.assertIsNotNone(quality_v3.parse_block(valid)); self.assertIsNotNone(mutant.parse_block(valid))
        bad=b'```protheusai-review\n{invalid\n```\n'
        self.assertIsNone(quality_v3.parse_block(bad)); self.assertIsNotNone(mutant.parse_block(bad))

    def test_pending_template_decision_mutant(self):
        # Negative: review block still says PENDING while manifest says PASS.
        folder,m=self.make_case(); block=self.record(folder,m,'gate1'); policy=self.policy()
        mutant=self.mutant(("if block.get(key) != expected:", "if key != 'decision' and block.get(key) != expected:"))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        block['decision']='PENDING'; self.write_block(folder,m,'gate1',block)
        m['gates']['gate1']['decision']='PASS'
        errors,_=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('review mismatch: decision',errors)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_orchestrator_developer_reviewer_mutant(self):
        # Negative: the orchestrator is also developer and reviews their own diff.
        folder,m=self.make_case(); m['roles']['developer']=[m['roles']['orchestrator'][0]]
        self.record(folder,m,'gate1'); block=self.record(folder,m,'gate2')
        block['effective_authors']=['orch']; self.write_block(folder,m,'gate2',block)
        policy=self.policy()
        mutant=self.mutant(("if reviewer in all_authors or block['authorship_independent'] is not True:", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate2',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
        block['reviewer']=' ORCH '; self.write_block(folder,m,'gate2',block)
        errors,_=quality_v3.gate_errors(folder,m,'gate2',policy,canon)
        self.assertTrue(any('self approval' in x for x in errors))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))

    def test_authorship_nonboolean_mutant(self):
        # Negative: declaration is string 'true', not a boolean. Two independent
        # checks are disabled: type check and PASS's exact-True check.
        self.check_gate(lambda b,m,f:b.update(authorship_independent='true'),
                        [("if type(block['authorship_independent']) is not bool:", 'if False:'),
                         ("if reviewer in all_authors or block['authorship_independent'] is not True:", 'if reviewer in all_authors:')],
                        'authorship declaration invalid')

    def test_g2_verifier_for_each_role_mutants(self):
        # Negative: third party is orchestrator, architect, developer or reviewer.
        mutant=self.mutant(("by not in forbidden and by != target", 'True'))
        valid={'id':'quality','by':'third','method':'log','ref':'log:1','date':'2026-11-05'}
        forbidden={'orch','arch','dev','quality'}
        self.assertTrue(quality_v3.valid_verification(valid,'quality',forbidden,canon,True))
        self.assertTrue(mutant.valid_verification(valid,'quality',forbidden,canon,True))
        for person in sorted(forbidden):
            with self.subTest(verifier=person):
                invalid=dict(valid,by=person)
                self.assertFalse(quality_v3.valid_verification(invalid,'quality',forbidden,canon,True))
                self.assertTrue(mutant.valid_verification(invalid,'quality',forbidden,canon,True))

    def test_matrix_invalid_guarantee_enum_mutant(self):
        # Negative: HIGH gate1 has a non-enumerated guarantee.
        valid=self.policy(); bad=copy.deepcopy(valid)
        bad['independence_minimums']['HIGH']['gate1']['guarantee']='bogus'
        mutant=self.mutant(("'G1_EVIDENCIA_REGISTRADA', 'G2_VERIFICACION_REGISTRADA'", "'G1_EVIDENCIA_REGISTRADA', 'bogus', 'G2_VERIFICACION_REGISTRADA'"))
        self.assertEqual([],quality_v3.policy_errors(valid)); self.assertEqual([],mutant.policy_errors(valid))
        self.assertTrue(quality_v3.policy_errors(bad)); self.assertEqual([],mutant.policy_errors(bad))

    def test_matrix_invalid_evidence_enum_mutant(self):
        # Negative: HIGH gate1 requires unknown evidence kind.
        valid=self.policy(); bad=copy.deepcopy(valid)
        bad['independence_minimums']['HIGH']['gate1']['evidence']=['identity','bogus']
        bad['independence_minimums']['CRITICAL']['gate1']['evidence'].append('bogus')
        mutant=self.mutant(("KINDS = {'identity', 'isolation', 'execution'}", "KINDS = {'identity', 'isolation', 'execution', 'bogus'}"))
        self.assertEqual([],quality_v3.policy_errors(valid)); self.assertEqual([],mutant.policy_errors(valid))
        self.assertTrue(quality_v3.policy_errors(bad)); self.assertEqual([],mutant.policy_errors(bad))

    @unittest.skipUnless(sys.platform=='win32', 'Windows junction requires Windows')
    def test_real_junction_path_mutant(self):
        # Negative: an actual NTFS junction within the temporary mission folder.
        import os, subprocess
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        target=folder/'real-directory'; target.mkdir(); (target/'evidence.txt').write_bytes(b'evidence')
        junction=folder/'real-junction'
        result=subprocess.run(['cmd','/c','mklink','/J',str(junction),str(target)],capture_output=True,text=True)
        if result.returncode:
            self.skipTest('mklink /J unavailable: '+result.stderr.strip())
        self.addCleanup(lambda: os.rmdir(junction) if junction.exists() else None)
        if not hasattr(junction,'is_junction') or not junction.is_junction():
            self.skipTest('runtime cannot identify the actual junction')
        mutant=self.mutant(("if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):", 'if False:'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,'real-directory/evidence.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'real-directory/evidence.txt'))
        self.assertIsNone(quality_v3.canonical_file(folder,'real-junction/evidence.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'real-junction/evidence.txt'))

    def test_cli_validate_accepted_matrix_warning_mutant(self):
        # Negative: accepted mission below current matrix must produce warning.
        import quality_cli
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="if low:\n                    warnings.append(f'{child.name}: no cumple la matriz vigente')"
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,'if False:\n                    pass'),'<isolated cli mutant>','exec'),mutant.__dict__)
        self.assertEqual(([],[]),quality_cli.project_report(self.root)); self.assertEqual(([],[]),mutant.project_report(self.root))
        policy=self.policy(); policy['independence_minimums']['HIGH']['gate1']['isolation']='I2_PERMISOS_SEPARADOS'
        (self.root/'quality/controls.json').write_text(json.dumps(policy),encoding='utf-8')
        errors,warnings=quality_cli.project_report(self.root)
        self.assertEqual([],errors); self.assertTrue(any('no cumple la matriz vigente' in x for x in warnings))
        self.assertEqual(([],[]),mutant.project_report(self.root))

    def test_cli_validate_open_matrix_mutant(self):
        # Negative: open HIGH mission below current matrix must fail validate.
        import quality_cli
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="found,_=v3_errors(folder,m,policy,canon,m['owner_acceptance']['status']!='APPROVED')"
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,'found,_=v3_errors(folder,m,policy,canon,False)'),'<isolated cli mutant>','exec'),mutant.__dict__)
        self.assertEqual(([],[]),quality_cli.project_report(self.root)); self.assertEqual(([],[]),mutant.project_report(self.root))
        policy=self.policy(); policy['independence_minimums']['HIGH']['gate1']['isolation']='I2_PERMISOS_SEPARADOS'
        (self.root/'quality/controls.json').write_text(json.dumps(policy),encoding='utf-8')
        errors,_=quality_cli.project_report(self.root)
        self.assertTrue(any('isolation below minimum' in e for e in errors))
        self.assertEqual(([],[]),mutant.project_report(self.root))

    def test_cli_historical_v2_cannot_close_mutant(self):
        # Negative: all-PASS structurally valid historical v2 cannot close.
        import contextlib, io, quality_cli
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="if legacy:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')"
        self.assertEqual(2,source.count(old))
        first=source.index(old); second=source.index(old,first+len(old))
        source=source[:second]+source[second:].replace(old,"if False:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')",1)
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source,'<isolated cli mutant>','exec'),mutant.__dict__)
        args=['can-close','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()): return module.main(args)
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        m['schema_version']=2
        m['gates']={g:{'decision':'PASS','reviewer':None,'reviewed_artifact':None,'evidence_file':None,'date':None} for g in ('gate1','gate2','gate3')}
        self.assertEqual([],quality_cli.structure_errors(m))
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_cli_pwr_cannot_close_mutant(self):
        # Negative: gate3 PWR must prevent owner-approved closure. The mutant
        # must disable both R7 validation and the CLI's independent all-PASS check.
        import contextlib, io, quality_cli
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        v3_mutant=self.mutant(("if any(mission['gates'][g]['decision'] != 'PASS' for g in GATES):", 'if False:'))
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="all(m['gates'][g]['decision']=='PASS' for g in GATES)"
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,"all(m['gates'][g]['decision'] in ('PASS','PASS_WITH_RESERVATIONS') for g in GATES)"),'<isolated cli mutant>','exec'),mutant.__dict__)
        mutant.v3_errors=v3_mutant.v3_errors
        args=['can-close','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()): return module.main(args)
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        self.record(folder,m,'gate3',decision='PASS_WITH_RESERVATIONS')
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_owner_canonical_empty_mutant(self):
        # Negative: approval identity contains only a zero-width format character.
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        policy=self.policy()
        mutant=self.mutant(("if not canon(owner.get('approved_by'))", "if not str(owner.get('approved_by') or '').strip()"))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        m['owner_acceptance']['approved_by']='\u200b'
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertIn('owner approval missing identity/date',errors)
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def test_missing_authorship_declaration_mutant(self):
        # Negative: absent authorship_independent. Bypassing exact block keys
        # makes the remaining code raise KeyError, which this control detects.
        folder,m=self.make_case(); block=self.record(folder,m,'gate1'); policy=self.policy()
        mutant=self.mutant(("and set(value) == KEYS else None", 'else None'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        del block['authorship_independent']; self.write_block(folder,m,'gate1',block)
        errors,_=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('invalid structured review block',errors)
        with self.assertRaises(KeyError): mutant.gate_errors(folder,m,'gate1',policy,canon)

    def test_i0_pwr_does_not_become_pass(self):
        folder, m = self.make_case()
        block = self.record(folder, m, 'gate1', decision='PASS_WITH_RESERVATIONS')
        policy = self.policy()
        policy['independence_minimums']['HIGH']['gate1']['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        block['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        self.write_block(folder, m, 'gate1', block)
        self.assertEqual(([], []), quality_v3.gate_errors(folder, m, 'gate1', policy, canon))
        self.assertEqual('PASS_WITH_RESERVATIONS', m['gates']['gate1']['decision'])


    def test_g2_author_verifier_for_each_role_mutants(self):
        # Negative: architect verification is written by one of the three roles
        # or by the reviewer; this exercises author verification, not reviewer verification.
        mutant=self.mutant(("by not in forbidden and by != target", 'True'))
        valid={'by':'third','method':'log','ref':'log:1','date':'2026-11-05'}
        forbidden={'orch','arch','dev','quality'}
        self.assertTrue(quality_v3.valid_verification(valid,'arch',forbidden,canon))
        self.assertTrue(mutant.valid_verification(valid,'arch',forbidden,canon))
        for person in sorted(forbidden):
            with self.subTest(verifier=person):
                invalid=dict(valid,by=person)
                self.assertFalse(quality_v3.valid_verification(invalid,'arch',forbidden,canon))
                self.assertTrue(mutant.valid_verification(invalid,'arch',forbidden,canon))

    def test_review_extra_key_mutant(self):
        # Negative: review manifest reference has an extra unexpected key.
        folder,m=self.make_case(); self.record(folder,m,'gate1'); policy=self.policy()
        mutant=self.mutant(("set(review) != {'file', 'sha256_lf', 'reviewer_verification'}", 'False'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        m['gates']['gate1']['review']['extra']='x'
        errors,_=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('invalid review reference',errors)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_developer_reviewer_mutant(self):
        # Negative: developer reviews their own Gate2 diff (without orchestrator overlap).
        folder,m=self.make_case(); self.record(folder,m,'gate1'); block=self.record(folder,m,'gate2')
        policy=self.policy()
        mutant=self.mutant(("if reviewer in all_authors or block['authorship_independent'] is not True:", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate2',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
        block['reviewer']=' DEV '; self.write_block(folder,m,'gate2',block)
        errors,_=quality_v3.gate_errors(folder,m,'gate2',policy,canon)
        self.assertTrue(any('self approval' in e for e in errors))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))

    def test_critical_missing_isolation_evidence_mutant(self):
        # Negative: CRITICAL gate1 omits the isolation evidence kind.
        # Both required-kinds and calculated-guarantee defenses must be disabled.
        folder,m=self.make_case('CRITICAL'); block=self.record(folder,m,'gate1')
        block['isolation']='I2_PERMISOS_SEPARADOS'
        path=folder/'isolation.txt'; path.write_bytes(b'isolation')
        block['evidence'].append({'kind':'isolation','path':path.name,'sha256_lf':quality_v3.digest(path.read_bytes())})
        self.write_block(folder,m,'gate1',block)
        author=m['roles']['architect'][0]; author['evidence']={'method':'log','ref':'x'}
        author['verification']={'by':'third','method':'log','ref':'x','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']={'id':'quality','by':'third','method':'log','ref':'x','date':'2026-11-05'}
        policy=self.policy()
        mutant=self.mutant(("if not set(rule['evidence']) <= present:", 'if False:'),
                           ("if GUARANTEE.index(level) < GUARANTEE.index(rule['guarantee']):", 'if False:'))
        self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate1',policy,canon))
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))
        block['evidence']=[e for e in block['evidence'] if e['kind']!='isolation']; self.write_block(folder,m,'gate1',block)
        m['gates']['gate1']['review']['reviewer_verification']={'id':'quality','by':'third','method':'log','ref':'x','date':'2026-11-05'}
        _,minima=quality_v3.gate_errors(folder,m,'gate1',policy,canon)
        self.assertIn('required evidence missing',minima)
        self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate1',policy,canon))

    def test_empty_developer_gate2_pass_fail_mutants(self):
        # Negative: Gate2 PASS and FAIL with no developer. Both nonempty-role
        # and author-subset checks independently detect the missing role.
        for decision in ('PASS','FAIL'):
            with self.subTest(decision=decision):
                folder,m=self.make_case(); self.record(folder,m,'gate1'); self.record(folder,m,'gate2',decision)
                policy=self.policy()
                mutant=self.mutant(("if (not allowed or not isinstance(effective, list) or not effective or", "if (not isinstance(effective, list) or not effective or"),
                                   ("not {canon(a) for a in effective} <= allowed):", 'False):'))
                self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,'gate2',policy,canon))
                self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
                m['roles']['developer']=[]
                errors,_=quality_v3.gate_errors(folder,m,'gate2',policy,canon)
                self.assertIn('effective authors invalid',errors)
                self.assertEqual(([],[]),mutant.gate_errors(folder,m,'gate2',policy,canon))
                self.tearDown_case()

    def test_empty_effective_authors_mutant(self):
        # Negative: gate1 review has an empty effective_authors array.
        self.check_gate(lambda b,m,f:b.update(effective_authors=[]),
                        [("not isinstance(effective, list) or not effective or", "not isinstance(effective, list) or False or")],
                        'effective authors invalid')

    def test_empty_artifact_name_mutant(self):
        # Negative: artifact.name is whitespace only.
        self.check_gate(lambda b,m,f:b['artifact'].update(name=' '),
                        [("or not isinstance(artifact.get('name'), str) or not canon(artifact['name'])", "or not isinstance(artifact.get('name'), str)")],
                        'artifact invalid')

    def test_path_traversal_mutant(self):
        # Negative: traversal through .. to an existing file outside the mission.
        # Grammar, component rejection, enumeration and containment are all
        # independent checks, so the mutant disables all four.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        outside=folder.parent/'outside-evidence.txt'; outside.write_bytes(b'evidence')
        mutant=self.mutant(("if not isinstance(name, str) or not PATH.fullmatch(name):", 'if not isinstance(name, str):'),
                           ("if any(part in ('.', '..') for part in parts):", 'if False:'),
                           ("if part not in os.listdir(current):", "if part not in ('.', '..') and part not in os.listdir(current):"),
                           ("if not current.resolve().is_relative_to(folder.resolve()) or not current.is_file():", 'if not current.is_file():'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNone(quality_v3.canonical_file(folder,'../outside-evidence.txt'))
        self.assertEqual(outside.resolve(),mutant.canonical_file(folder,'../outside-evidence.txt').resolve())

    def test_path_dot_segment_mutant(self):
        # Negative: ./ segment is not canonical, even for an existing file.
        mutant=self.mutant(("if any(part in ('.', '..') for part in parts):", 'if False:'),
                           ("if part not in os.listdir(current):", "if part not in ('.', '..') and part not in os.listdir(current):"))
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        self.assertIsNotNone(quality_v3.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNone(quality_v3.canonical_file(folder,'./identity-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'./identity-gate1.txt'))

    @unittest.skipUnless(sys.platform=='win32', 'case-insensitive filesystem test requires Windows')
    def test_path_case_mutant(self):
        # Negative: an existing Windows file is referenced with different case.
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        mutant=self.mutant(("if part not in os.listdir(current):", 'if False:'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'identity-gate1.txt'))
        self.assertIsNone(quality_v3.canonical_file(folder,'IDENTITY-gate1.txt'))
        self.assertIsNotNone(mutant.canonical_file(folder,'IDENTITY-gate1.txt'))

    @unittest.skipUnless(sys.platform=='win32', 'Windows symbolic link test requires Windows')
    def test_real_symlink_path_mutant(self):
        # Negative: a real symbolic link, as distinct from a directory junction.
        import os
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        target=folder/'identity-gate1.txt'; link=folder/'link.txt'
        try: os.symlink(target,link)
        except OSError as exc: self.skipTest('symbolic-link privilege unavailable: '+str(exc))
        mutant=self.mutant(("if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):", 'if False:'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,target.name))
        self.assertIsNotNone(mutant.canonical_file(folder,target.name))
        self.assertIsNone(quality_v3.canonical_file(folder,link.name))
        self.assertIsNotNone(mutant.canonical_file(folder,link.name))

    def test_i0_pwr_after_pass_is_not_pass(self):
        folder, m = self.make_case()
        self.record(folder, m, 'gate1')
        block = self.record(folder, m, 'gate2', decision='PASS_WITH_RESERVATIONS')
        policy = self.policy()
        policy['independence_minimums']['HIGH']['gate2']['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        block['isolation'] = 'I0_CONTEXTO_COMPARTIDO'
        self.write_block(folder, m, 'gate2', block)
        self.assertEqual(([], []), quality_v3.v3_errors(folder, m, policy, canon))
        self.assertEqual('PASS_WITH_RESERVATIONS', m['gates']['gate2']['decision'])


    def test_g2_pertinent_author_verification_gate_mutants(self):
        # Negative: each pertinent author (architect gate1, developer gate2)
        # has a third-party verifier who is actually one of the roles/reviewer.
        for gate,role in [('gate1','architect'),('gate2','developer')]:
            for by in ('orch','arch','dev','quality'):
                with self.subTest(gate=gate,by=by):
                    folder,m=self.make_case('CRITICAL'); block=self.record(folder,m,gate)
                    block['isolation']='I2_PERMISOS_SEPARADOS'
                    path=folder/'isolation.txt'; path.write_bytes(b'permissions')
                    block['evidence'].append({'kind':'isolation','path':path.name,'sha256_lf':quality_v3.digest(path.read_bytes())})
                    self.write_block(folder,m,gate,block)
                    author=m['roles'][role][0]
                    author['evidence']={'method':'log','ref':'x'}
                    author['verification']={'by':'third','method':'log','ref':'x','date':'2026-11-05'}
                    m['gates'][gate]['review']['reviewer_verification']={'id':'quality','by':'third','method':'log','ref':'x','date':'2026-11-05'}
                    policy=self.policy(); mutant=self.mutant(("by not in forbidden and by != target", 'True'))
                    self.assertEqual(([],[]),quality_v3.gate_errors(folder,m,gate,policy,canon))
                    self.assertEqual(([],[]),mutant.gate_errors(folder,m,gate,policy,canon))
                    author['verification']['by']=by
                    _,minima=quality_v3.gate_errors(folder,m,gate,policy,canon)
                    self.assertIn('author verification required',minima)
                    self.assertEqual(([],[]),mutant.gate_errors(folder,m,gate,policy,canon))
                    self.tearDown_case()

    def test_historical_v1_cannot_transition_mutants(self):
        # Negative: all-PASS structurally valid v1 is blocked by both can-*.
        import contextlib, io, quality_cli
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="if legacy:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')"
        self.assertEqual(2,source.count(old))
        mutants=[]
        for idx in range(2):
            positions=[]; offset=0
            for unused in range(2):
                offset=source.index(old,offset); positions.append(offset); offset+=len(old)
            at=positions[idx]
            altered=source[:at]+source[at:].replace(old,"if False:\n            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')",1)
            module=types.ModuleType('isolated_cli_mutant'); module.__file__=str(ROOT/'scripts/quality_cli.py')
            exec(compile(altered,'<isolated cli mutant>','exec'),module.__dict__); mutants.append(module)
        def invoke(module,command):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()): return module.main([command,'--mission',folder.name,'--root',str(self.root)])
        for command,mutant in zip(('can-implement','can-close'),mutants):
            self.assertEqual(0,invoke(quality_cli,command)); self.assertEqual(0,invoke(mutant,command))
        m['schema_version']=1; del m['roles']; m['author']='arch'; m['implementation_author']='dev'
        m['gates']={g:{'decision':'PASS','reviewer_id':'quality','reviewed_artifact':None,'evidence_file':None,'date':None} for g in ('gate1','gate2','gate3')}
        self.assertEqual([],quality_cli.structure_errors(m))
        for command,mutant in zip(('can-implement','can-close'),mutants):
            with self.subTest(command=command):
                self.assertEqual(1,invoke(quality_cli,command)); self.assertEqual(0,invoke(mutant,command))

    def test_cli_unqualified_verification_claim_mutant(self):
        # Negative: successful can-implement output claims an identity is
        # verified without qualifying it as recorded or not checked by the CLI.
        import contextlib, io, re, quality_cli
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="print('Gate 1 record consistent; reviewer identity and isolation are not checked by the CLI.')"
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,"print('revisor verificado')"),'<isolated cli mutant>','exec'),mutant.__dict__)
        args=['can-implement','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            output=io.StringIO()
            with contextlib.redirect_stdout(output): code=module.main(args)
            return code,output.getvalue()
        def unqualified(text):
            return any(re.search(r'verificad[oa]',line,re.I) and not re.search(r'registrad[oa]|no comprobada por la CLI',line,re.I)
                       for line in text.splitlines())
        code,output=invoke(quality_cli); self.assertEqual(0,code); self.assertFalse(unqualified(output))
        code,output=invoke(mutant); self.assertEqual(0,code); self.assertTrue(unqualified(output))

    def test_symlink_signal_mutant(self):
        # Negative: mocked symlink signal on a file; real symlink creation is
        # separately attempted and may be skipped if Windows denies privilege.
        from unittest.mock import patch
        folder,m=self.make_case(); self.record(folder,m,'gate1')
        name='identity-gate1.txt'
        mutant=self.mutant(("if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):", 'if False:'))
        self.assertIsNotNone(quality_v3.canonical_file(folder,name))
        self.assertIsNotNone(mutant.canonical_file(folder,name))
        with patch.object(Path,'is_symlink',lambda path:path.name==name):
            self.assertIsNone(quality_v3.canonical_file(folder,name))
            self.assertIsNotNone(mutant.canonical_file(folder,name))

    def test_medium_gate2_pinned_artifact_mutant(self):
        # Negative: MEDIUM gate2 uses a declared sha256 without a pinned file.
        folder,m=self.make_case('MEDIUM')
        self.record(folder,m,'gate1'); block=self.record(folder,m,'gate2')
        self.assertEqual('MEDIUM',m['risk'])
        policy=self.policy()
        self.assertTrue(policy['independence_minimums']['MEDIUM']['gate2']['pinned_artifact'])
        mutant=self.mutant(("if not pinned:", 'if False:'))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        block['artifact']['ref']='sha256:'+'a'*64
        self.write_block(folder,m,'gate2',block)
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertIn('gate2: pinned artifact required',errors)
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def test_medium_gate3_missing_execution_mutant(self):
        # Negative: MEDIUM gate3 has no execution record. Both the minimum
        # kind and calculated G1 defenses must be disabled to allow it.
        folder,m=self.make_case('MEDIUM')
        for gate in ('gate1','gate2','gate3'): block=self.record(folder,m,gate)
        self.assertEqual('MEDIUM',m['risk'])
        policy=self.policy()
        self.assertIn('execution',policy['independence_minimums']['MEDIUM']['gate3']['evidence'])
        mutant=self.mutant(("if not set(rule['evidence']) <= present:", 'if False:'),
                           ("if GUARANTEE.index(level) < GUARANTEE.index(rule['guarantee']):", 'if False:'))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        block['evidence']=[e for e in block['evidence'] if e['kind']!='execution']
        self.write_block(folder,m,'gate3',block)
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertIn('gate3: required evidence missing',errors)
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def test_validate_v2_historical_warning_mutant(self):
        # Negative: validate fails to warn that a valid v2 record is historical.
        import contextlib, io, quality_cli
        folder,m=self.make_case('MEDIUM')
        self.record(folder,m,'gate1')
        m['schema_version']=2
        m['gates']={g:{'decision':m['gates'][g]['decision'],'reviewer':None,
                       'reviewed_artifact':None,'evidence_file':None,'date':None}
                    for g in ('gate1','gate2','gate3')}
        self.assertEqual([],quality_cli.structure_errors(m))
        (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
        source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        old="""warnings.append(f'{child.name} v{m["schema_version"]} historico; no habilita autorizaciones')"""
        self.assertEqual(1,source.count(old))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(source.replace(old,'pass'),'<isolated cli mutant>','exec'),mutant.__dict__)
        def invoke(module):
            out=io.StringIO()
            with contextlib.redirect_stdout(out): code=module.main(['validate','--root',str(self.root)])
            return code,out.getvalue()
        code,output=invoke(quality_cli)
        self.assertEqual(0,code,output)
        self.assertIn('AVISO: TEST-100 v2 historico; no habilita autorizaciones',output)
        code,output=invoke(mutant)
        self.assertEqual(0,code,output)
        self.assertNotIn('AVISO: TEST-100 v2 historico; no habilita autorizaciones',output)

    def test_owner_canonical_empty_date_mutant(self):
        # Negative: approval date contains only a zero-width format character.
        folder,m=self.make_case()
        for gate in ('gate1','gate2','gate3'): self.record(folder,m,gate)
        m['owner_acceptance']={'status':'APPROVED','approved_by':'owner','date':'2026-11-05'}
        policy=self.policy()
        mutant=self.mutant(("not canon(owner.get('date'))", "not str(owner.get('date') or '').strip()"))
        self.assertEqual(([],[]),quality_v3.v3_errors(folder,m,policy,canon))
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))
        m['owner_acceptance']['date']='\u200b'
        errors,_=quality_v3.v3_errors(folder,m,policy,canon)
        self.assertIn('owner approval missing identity/date',errors)
        self.assertEqual(([],[]),mutant.v3_errors(folder,m,policy,canon))

    def critical_canonical_fixture(self):
        folder,m=self.make_case('CRITICAL')
        block=self.record(folder,m,'gate1')
        path=folder/'isolation.txt'; path.write_bytes(b'permissions')
        block['isolation']='I2_PERMISOS_SEPARADOS'
        block['evidence'].append({'kind':'isolation','path':path.name,'sha256_lf':quality_v3.digest(path.read_bytes())})
        self.write_block(folder,m,'gate1',block)
        architect=m['roles']['architect'][0]
        architect['evidence']={'method':'source','ref':'record'}
        architect['verification']={'by':'third','method':'source','ref':'record','date':'2026-11-05'}
        m['gates']['gate1']['review']['reviewer_verification']={'id':'quality','by':'third','method':'source','ref':'record','date':'2026-11-05'}
        return folder,m,block

    def canonical_field_mutation(self, group, field):
        # One test per named field. For author verification, CLI structure and
        # G2 each reject the same input, so both must be disabled for the mutant
        # to demonstrate the original bypass of can-implement.
        import contextlib, io, quality_cli
        folder,m,block=self.critical_canonical_fixture()
        cli_source=(ROOT/'scripts/quality_cli.py').read_text(encoding='utf-8')
        v3=quality_v3
        if group in ('author_verification','reviewer_verification'):
            is_reviewer = group=='reviewer_verification'
            original="if not all(isinstance(x, str) and canon(x) for x in value.values()):"
            weakened=("if not all(isinstance(x, str) and (x.strip() if reviewer == "
                      +repr(is_reviewer)+" and k == "+repr(field)+" else canon(x)) for k,x in value.items()):")
            v3=self.mutant((original,weakened))
        if group in ('author_verification','author_evidence'):
            field_group='verification' if group=='author_verification' else 'evidence'
            original="if record is not None and not all(canon(value) for value in record.values()):"
            weakened=("if record is not None and not all((value.strip() if field == "+repr(field_group)
                      +" and key == "+repr(field)+" else canon(value)) for key,value in record.items()):")
            self.assertEqual(1,cli_source.count(original))
            cli_source=cli_source.replace(original,weakened,1)
        if group=='artifact_name':
            v3=self.mutant(("or not isinstance(artifact.get('name'), str) or not canon(artifact['name'])",
                            "or not isinstance(artifact.get('name'), str) or not artifact['name'].strip()"))
        mutant=types.ModuleType('isolated_cli_mutant'); mutant.__file__=str(ROOT/'scripts/quality_cli.py')
        exec(compile(cli_source,'<isolated cli mutant>','exec'),mutant.__dict__)
        mutant.v3_errors=v3.v3_errors
        args=['can-implement','--mission',folder.name,'--root',str(self.root)]
        def invoke(module):
            (folder/'mission.json').write_text(json.dumps(m),encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                return module.main(args)
        self.assertEqual([],quality_cli.mission_errors(folder,m))
        self.assertEqual([],mutant.mission_errors(folder,m))
        self.assertEqual(0,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))
        if group=='reviewer_verification':
            m['gates']['gate1']['review']['reviewer_verification'][field]='\u200b'
        elif group=='author_verification':
            m['roles']['architect'][0]['verification'][field]='\u200b'
        elif group=='author_evidence':
            m['roles']['architect'][0]['evidence'][field]='\u200b'
        else:
            block['artifact']['name']='\u200b'
            verification=m['gates']['gate1']['review']['reviewer_verification']
            self.write_block(folder,m,'gate1',block)
            m['gates']['gate1']['review']['reviewer_verification']=verification
        self.assertNotEqual([],quality_cli.mission_errors(folder,m))
        self.assertEqual([],mutant.mission_errors(folder,m))
        self.assertEqual(1,invoke(quality_cli)); self.assertEqual(0,invoke(mutant))

    def test_reviewer_verification_method_canonical_mutant(self):
        self.canonical_field_mutation('reviewer_verification','method')

    def test_reviewer_verification_ref_canonical_mutant(self):
        self.canonical_field_mutation('reviewer_verification','ref')

    def test_reviewer_verification_date_canonical_mutant(self):
        self.canonical_field_mutation('reviewer_verification','date')

    def test_author_verification_method_canonical_mutant(self):
        self.canonical_field_mutation('author_verification','method')

    def test_author_verification_ref_canonical_mutant(self):
        self.canonical_field_mutation('author_verification','ref')

    def test_author_verification_date_canonical_mutant(self):
        self.canonical_field_mutation('author_verification','date')

    def test_author_evidence_method_canonical_mutant(self):
        self.canonical_field_mutation('author_evidence','method')

    def test_author_evidence_ref_canonical_mutant(self):
        self.canonical_field_mutation('author_evidence','ref')

    def test_artifact_name_canonical_mutant(self):
        self.canonical_field_mutation('artifact_name','name')


if __name__ == '__main__':
    unittest.main()
