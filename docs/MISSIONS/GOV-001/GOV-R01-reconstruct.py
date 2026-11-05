"""GOV-R01 investigation: rebuild GATE2-INPUT.sha256 (cycle 1) from known state, verify by original SHA-256.

Reads Git blobs and uses a temporary clone; writes output only with --out.
"""
import argparse
import hashlib
import os
import shutil
import stat
import tempfile
import subprocess
import sys
from pathlib import Path

TARGET = 'f0f7392a971467ad7816da81ae7bef57323249e36f0ac10c0838dbc1768c4a9b'
KNOWN = {  # printed in the session at generation time (first 9 lines) and at mission creation
    'AGENTS.md': 'acabd847055c7abae27e0468584f356334839b8b4a4d7b3e423a7bff99957408',
    'FILE_INDEX.md': 'd321fa905feb9619737876a106f42fffc72998b557068fe10b0864b441a515bb',
    'README.md': '2244a5f4c1fd6b5b5f52b3005d17d8919edbd1b0d98ef32dbdf32c323a04b39e',
    'docs/MISSIONS/EXAMPLE-001/mission.json': '3e07b1aff46eba1deacf2db5d3c0e251bd025eb915110173f789ca8de0f7122b',
    'docs/MISSIONS/README.md': 'f75de97581804900f1d986df0bfc369e341de1c8cdd86e7ec0c676ecd7f8030e',
    'docs/QUALITY_EVIDENCE_PROTOCOL.md': '5da87a7722d0e15e36f6063da54f0dd3755856a17bb20b2ca0610e93c52e3a98',
    'docs/QUALITY_POLICY.md': '13c570c49e88b734e2a29d95a60454817e3439f7fb5403b02b2d7a465d99e922',
    'docs/ROLE_MATRIX.md': '3541a8298b7c8ae6bc6649afde7cc99e0291527d2973f9cb80023847a8f37a70',
    'docs/templates/GATE1_REVIEW.md': '134ce83abac28e07ebe7ac3709c8ae726c8c71592a8ebcfc6ae7ed64943cde5d',
    'docs/MISSIONS/GOV-001/04-GATE2-REVIEW.md': '03977e1a1926e00822d3e1d4b0cc90a23aa8c1b2e86544dec16180ee54eb1e61',
    'docs/MISSIONS/GOV-001/05-GATE3-EVIDENCE.md': 'cc76c6773db8fccb35d07995c9a4246a8c68332fb811e6bc960fe872c47c96dc',
    'docs/MISSIONS/GOV-001/06-DECISION.md': '9084d71aef48b7861b4205ce98d8dbf2a5949b90c5e4437b3a0b6a7bf7ac0374',
}
PORCELAIN = [' M ' + p for p in (
    'AGENTS.md', 'FILE_INDEX.md', 'README.md', 'docs/MISSIONS/EXAMPLE-001/mission.json',
    'docs/MISSIONS/README.md', 'docs/QUALITY_EVIDENCE_PROTOCOL.md', 'docs/QUALITY_POLICY.md',
    'docs/ROLE_MATRIX.md', 'docs/templates/GATE1_REVIEW.md', 'docs/templates/GATE2_REVIEW.md',
    'docs/templates/GATE3_EVIDENCE.md', 'docs/templates/IMPLEMENTATION_REPORT.md',
    'docs/templates/MISSION_PLAN.md', 'quality/controls.json', 'scripts/new_mission.py',
    'scripts/quality_cli.py', 'tests/test_governance.py')] + ['?? docs/MISSIONS/GOV-001/' + p for p in (
    '01-PLAN.md', '02-GATE1-REVIEW.md', '03-IMPLEMENTATION.md', '04-GATE2-REVIEW.md',
    '05-GATE3-EVIDENCE.md', '06-DECISION.md', 'GATE1-REVIEW-05.md', 'GATE1-REVIEW-06.md',
    'GATE1-REVIEW-07.md', 'GATE1-REVIEW-08.md', 'OWNER-DECISION-01.md',
    *[f'PROPOSAL-v{i}.md' for i in range(1, 9)], 'QUALITY-CYCLES-01-04-NOTE.md', 'mission.json')]

# Files written with LF before cycle 1 and converted to CRLF in cycle 2.
LF_AT_T1 = {'docs/MISSIONS/EXAMPLE-001/mission.json', 'scripts/new_mission.py', 'scripts/quality_cli.py',
            'tests/test_governance.py', 'docs/MISSIONS/GOV-001/01-PLAN.md',
            'docs/MISSIONS/GOV-001/02-GATE1-REVIEW.md', 'docs/MISSIONS/GOV-001/03-IMPLEMENTATION.md',
            'docs/MISSIONS/GOV-001/QUALITY-CYCLES-01-04-NOTE.md', 'docs/MISSIONS/GOV-001/mission.json'}

# Content edits made after cycle 1, as (current_text, text_at_T1), applied in this order.
REVERSE = {
 'scripts/quality_cli.py': [
  ("""        match=INDEPENDENCE.match(canon(independence[0])) if len(independence)==1 else None
        evidence=re.sub(r'^\\W+','',match.group(1)) if match else ''
        if not match or match.group(1).startswith('[') or not evidence or re.match(r'no\\b',evidence):
            errs.append(f'{name}: independencia no acreditada en el informe')""",
   """        match=INDEPENDENCE.match(canon(independence[0])) if len(independence)==1 else None
        if not match or match.group(1).startswith('['):
            errs.append(f'{name}: independencia no acreditada en el informe')"""),
  ("""            print(f'Registro Gate 1 consistente. Identidades: verificación registrada, {NOT_CHECKED}. Verificar revisión REAL y autorización.')""",
   """            print(f'Registro Gate 1 consistente; identidades {NOT_CHECKED}. Verificar revisión REAL y autorización.')"""),
  ("""        text=report_text(folder,g.get('evidence_file'))
        if text is None:
            errs.append(f'{name}: falta informe independiente real, no plantilla')
        else:
            errs+=report_errors(name,text,g,pertinent,pertinent_role)""",
   """        if not has_evidence(folder,g.get('evidence_file')):
            errs.append(f'{name}: falta informe independiente real, no plantilla')
        else:
            text=(folder/g['evidence_file']).read_text(encoding='utf-8')
            errs+=report_errors(name,text,g,pertinent,pertinent_role)"""),
  ("""def canon(value):
    \"\"\"Canonical form used to compare declared identifiers (not an identity check).\"\"\"
    if not isinstance(value,str):
        return ''
    # Format characters (e.g. zero-width space) must not make two identifiers look different.
    text=''.join(ch for ch in unicodedata.normalize('NFKC',value) if unicodedata.category(ch)!='Cf')
    return text.strip().casefold()


def report_text(folder: Path, file: object):
    \"\"\"Text of a real report inside the mission folder, or None (never raises).\"\"\"
    if not isinstance(file,str) or not file.strip():
        return None
    try:
        path=(folder/file).resolve()
        if not path.is_relative_to(folder.resolve()):
            return None
        if not path.is_file() or path.stat().st_size < 10:
            return None
        text=path.read_text(encoding='utf-8')
    except (OSError,ValueError,UnicodeError):
        return None
    # An unchanged template is not a review report.
    if '**Dictamen:** PENDING' in text or '**Revisor:** [IDENTIDAD REAL]' in text:
        return None
    return text


def has_evidence(folder: Path, file: object):
    return report_text(folder,file) is not None""",
   """def canon(value):
    \"\"\"Canonical form used to compare declared identifiers (not an identity check).\"\"\"
    return unicodedata.normalize('NFKC',value).strip().casefold() if isinstance(value,str) else ''


def has_evidence(folder: Path, file: object):
    if not isinstance(file,str) or not file.strip():
        return False
    path=(folder/file).resolve()
    if not path.is_relative_to(folder.resolve()):
        return False
    if not path.is_file() or path.stat().st_size < 10:
        return False
    text=path.read_text(encoding='utf-8')
    # An unchanged template is not a review report.
    return not ('**Dictamen:** PENDING' in text or '**Revisor:** [IDENTIDAD REAL]' in text)"""),
 ],
 'scripts/new_mission.py': [
  ("""import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from quality_cli import canon""",
   """import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path"""),
  ("""    if not title.strip() or not canon(orchestrator):
        raise ValueError('título y orchestrator son obligatorios')
    if architect is not None and not canon(architect):
        raise ValueError('architect vacío')""",
   """    if not title.strip() or not unicodedata.normalize('NFKC', orchestrator or '').strip():
        raise ValueError('título y orchestrator son obligatorios')
    if architect is not None and not unicodedata.normalize('NFKC', architect).strip():
        raise ValueError('architect vacío')"""),
 ],
 'tests/test_governance.py': [
  ("""            ('independencia afirmación vacía de contenido','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** si — no','independencia no acreditada'),
            ('independencia «no» tras doble guion','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí -- no','independencia no acreditada'),
            ('independencia «no» entre comillas','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** sí — «no»','independencia no acreditada'),""",
   """            ('independencia afirmación vacía de contenido','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** si — no','independencia no acreditada'),"""),
  ("""        with self.assertRaises(FileExistsError):
            create_mission(self.root,'TEST-001','No sobrescribir','MEDIUM','orch-a')
        for invisible in ('\\u200b',' \\u200b '):
            with self.assertRaises(ValueError):
                create_mission(self.root,'TEST-005','T','LOW',invisible)
            with self.assertRaises(ValueError):
                create_mission(self.root,'TEST-005','T','LOW','orch-a',invisible)""",
   """        with self.assertRaises(FileExistsError):
            create_mission(self.root,'TEST-001','No sobrescribir','MEDIUM','orch-a')"""),
  ("""            ('autor efectivo vacío','**Autor efectivo:** dev-1','**Autor efectivo:** ','Autor efectivo'),
            ('autor efectivo duplicado','**Autor efectivo:** dev-1','**Autor efectivo:** dev-1\\n**Autor efectivo:** dev-1','Autor efectivo'),
            ('independencia afirmación vacía de contenido','**Independencia verificada:** sí — subagente distinto del autor, log:quality-1','**Independencia verificada:** si — no','independencia no acreditada'),
        ]""",
   """            ('autor efectivo vacío','**Autor efectivo:** dev-1','**Autor efectivo:** ','Autor efectivo'),
        ]"""),
  ("""        cases=[('gate1','arch-1',('dev-1',)),('gate1','orch-1',('dev-1',)),('gate2','dev-1',('dev-1',)),
               ('gate2','DEV-2 ',('dev-1','dev-2')),('gate3','ｄｅｖ－１',('dev-1',)),('gate2','dev\\u200b-1',('dev-1',))]""",
   """        cases=[('gate1','arch-1',('dev-1',)),('gate1','orch-1',('dev-1',)),('gate2','dev-1',('dev-1',)),
               ('gate2','DEV-2 ',('dev-1','dev-2')),('gate3','ｄｅｖ－１',('dev-1',))]"""),
  ("""        m['gates']['gate1']['evidence_file']='../../secrets.txt'
        self.assertMissionError(out,m,'falta informe independiente')
        m['gates']['gate1']['evidence_file']='02-GATE1\\x00-REVIEW.md'
        self.assertMissionError(out,m,'falta informe independiente')
        m['gates']['gate1']['evidence_file']='02-GATE1-REVIEW.md'
        (out/'02-GATE1-REVIEW.md').write_bytes(b'**Dictamen:** PASS\\n\\xff\\xfe no es UTF-8\\n')
        self.assertMissionError(out,m,'falta informe independiente')
        self.save(out,m)
        self.assertEqual(1,run(quality_main,['validate','--root',str(self.root)])[0])""",
   """        m['gates']['gate1']['evidence_file']='../../secrets.txt'
        self.assertMissionError(out,m,'falta informe independiente')"""),
  ("""        self.assertMissionError(out2,m2,'developer vacío')
        out3,m3=self.mission()
        self.record(out3,m3,'gate1',decision='FAIL',verified_by=None)
        self.edit_report(out3,'gate1','**Autor efectivo:** arch-1','')
        self.assertMissionError(out3,m3,'Autor efectivo')
        m3['gates']['gate1']['reviewed_artifact']='01-PLAN.md'
        self.edit_report(out3,'gate1',f'01-PLAN.md sha256:{HASH}','01-PLAN.md')
        self.assertMissionError(out3,m3,'reviewed_artifact requiere')""",
   """        self.assertMissionError(out2,m2,'developer vacío')"""),
  ("""            'evidence ref vacía':lambda m:m['roles']['architect'][0]['evidence'].update(ref=' '),
            'verification sin campo':lambda m:m['roles']['architect'][0]['verification'].pop('date'),""",
   """            'evidence ref vacía':lambda m:m['roles']['architect'][0]['evidence'].update(ref=' '),"""),
 ],
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def t1_bytes(path: str) -> bytes:
    if path in ('docs/MISSIONS/GOV-001/04-GATE2-REVIEW.md', 'docs/MISSIONS/GOV-001/05-GATE3-EVIDENCE.md'):
        template = {'04': 'GATE2_REVIEW.md', '05': 'GATE3_EVIDENCE.md'}[Path(path).name[:2]]
        text = blob('docs/templates/' + template).decode('utf-8').replace('\r\n', '\n').replace('[MISSION-ID]', 'GOV-001')
        return text.replace('\n', '\r\n').encode('utf-8')  # Path.write_text on Windows
    current = blob(path)
    if path not in LF_AT_T1:
        return current.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    text = current.decode('utf-8').replace('\r\n', '\n')
    for now, before in REVERSE.get(path, []):
        if text.count(now) != 1:
            sys.exit(f'reverse edit not found exactly once in {path}: {now[:60]!r}')
        text = text.replace(now, before)
    if path.endswith('03-IMPLEMENTATION.md'):
        marker = '\n\n## Reapertura de Gate 2 — ciclo 2'
        text = text[:text.index(marker) + 1]
    return text.encode('utf-8')


def diff_stat(files: dict) -> list:
    """git diff --stat 29d741e over the reconstructed tracked files, in a throwaway clone."""
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix='gov-r01-'))
    try:
        subprocess.run(['git', 'clone', '-q', '--no-hardlinks', '--no-checkout', str(REPO), str(tmp)], check=True)
        subprocess.run(['git', '-C', str(tmp), '-c', 'core.autocrlf=true', 'checkout', '-q', '29d741e'], check=True)
        for path, data in files.items():
            if not path.startswith('docs/MISSIONS/GOV-001/'):
                (tmp / path).write_bytes(data)
        out = subprocess.run(['git', '-C', str(tmp), '-c', 'core.autocrlf=true', 'diff', '--stat', '29d741e'],
                             capture_output=True, check=True).stdout.decode('utf-8')
        return out.splitlines()
    finally:
        def remove_readonly(func, path, exc):
            os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
            func(path)
        shutil.rmtree(tmp, onexc=remove_readonly)


parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=Path.cwd())
parser.add_argument('--commit', default='6e5e929')
parser.add_argument('--out', type=Path)
args = parser.parse_args()
REPO = args.repo.resolve()
def blob(path):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{args.commit}:{path}'], check=True, capture_output=True).stdout

print('Git:', subprocess.run(['git', '--version'], check=True, capture_output=True, text=True).stdout.strip())
files = {line[3:]: t1_bytes(line[3:]) for line in PORCELAIN}
known_ok = True
for path, expected in KNOWN.items():
    got = sha(files[path])
    print(('OK  ' if got == expected else 'DIFF') + f' {path}')
    known_ok &= got == expected
lines = ['# GOV-001 Gate 2/3 input. Base 29d741e641c77f8569ee74d2262bb70bc8b38be7. SHA-256 of working-tree bytes. This file excludes itself.',
         '# git status --porcelain --untracked-files=all']
lines += [f'# {p}' for p in PORCELAIN]
lines += ['# sha256  path'] + [f'{sha(files[p[3:]])}  {p[3:]}' for p in PORCELAIN]
lines += ['# git diff --stat 29d741e (tracked files)'] + [f'# {s}' for s in diff_stat(files)]
data = ('\n'.join(lines) + '\n').encode('utf-8')
if args.out:
    args.out.write_bytes(data)
tracked = subprocess.run(['git', '-C', str(REPO), 'cat-file', 'blob', 'HEAD:docs/MISSIONS/GOV-001/GATE2-INPUT-01.RECONSTRUCTED.sha256'], capture_output=True)
blob_ok = tracked.returncode != 0 or tracked.stdout == data
print('Blob HEAD:', 'no committed reconstruction' if tracked.returncode else ('MATCH' if blob_ok else 'NO MATCH'))
ok = sha(data) == TARGET and known_ok and blob_ok
print('entries', len(PORCELAIN), 'sha256', sha(data), 'MATCH' if ok else 'NO MATCH')
sys.exit(0 if ok else 1)
