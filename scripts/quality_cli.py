#!/usr/bin/env python3
"""Validates documentation records; never grants a Quality Gate PASS nor checks identities."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

GATES=('gate1','gate2','gate3')
DECISIONS={'PENDING','PASS','PASS_WITH_RESERVATIONS','FAIL'}
ENABLING={'PASS','PASS_WITH_RESERVATIONS'}
OWNER_STATUS={'PENDING','APPROVED','REJECTED'}
RISK={'LOW','MEDIUM','HIGH','CRITICAL'}
ROLES=('orchestrator','architect','developer')
FILES=('AGENTS.md','docs/PROJECT_CHARTER.md','docs/ARCHITECTURE.md',
       'docs/QUALITY_POLICY.md','docs/TEST_STRATEGY.md','quality/controls.json',
       'docs/templates/MISSION_PLAN.md','docs/templates/GATE1_REVIEW.md',
       'docs/templates/GATE2_REVIEW.md','docs/templates/GATE3_EVIDENCE.md')
MISSION_FILES=('01-PLAN.md','02-GATE1-REVIEW.md','03-IMPLEMENTATION.md',
               '04-GATE2-REVIEW.md','05-GATE3-EVIDENCE.md','06-DECISION.md')
VERSION_ID=re.compile(r'(?<![0-9A-Za-z])(?:sha256:[0-9a-fA-F]{64}|git:[0-9a-fA-F]{7,40}(?:\.\.[0-9a-fA-F]{7,40})?)(?![0-9A-Za-z])')
INDEPENDENCE=re.compile(r'^s[ií]\s*[—–:;,\-]\s*(\S.*)$')
NOT_CHECKED='no comprobada por la CLI'


def read_json(path: Path):
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
    except (ValueError,OSError,UnicodeError) as exc:
        raise ValueError(f'{path}: {exc}') from exc
    if not isinstance(data,dict):
        raise ValueError(f'{path}: JSON debe contener objeto')
    return data


def canon(value):
    """Canonical form used to compare declared identifiers (not an identity check)."""
    if not isinstance(value,str):
        return ''
    # Format characters (e.g. zero-width space) must not make two identifiers look different.
    text=''.join(ch for ch in unicodedata.normalize('NFKC',value) if unicodedata.category(ch)!='Cf')
    return text.strip().casefold()


def report_text(folder: Path, file: object):
    """Text of a real report inside the mission folder, or None (never raises)."""
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
    return report_text(folder,file) is not None


def labels(text: str, label: str):
    return re.findall(rf'^[ \t]*\*\*{re.escape(label)}:\*\*[ \t]*(.*?)[ \t]*$',text,flags=re.MULTILINE)


def _text(value, nonempty=False):
    return isinstance(value,str) and (not nonempty or bool(value.strip()))


def ident_errors(ident, where):
    if not isinstance(ident,dict) or set(ident)!={'id','evidence','verification'}:
        return [f'{where}: identidad debe tener exactamente id, evidence y verification']
    errs=[]
    if not canon(ident['id']):
        errs.append(f'{where}.id vacío o no es texto')
    evidence=ident['evidence']
    if evidence is not None and (not isinstance(evidence,dict) or set(evidence)!={'method','ref'}
                                 or not all(_text(v,True) for v in evidence.values())):
        errs.append(f'{where}.evidence debe ser null o {{method, ref}} no vacíos')
    record=ident['verification']
    if record is not None:
        if (not isinstance(record,dict) or set(record)!={'by','method','ref','date'}
                or not all(_text(v,True) for v in record.values())):
            errs.append(f'{where}.verification debe ser null o {{by, method, ref, date}} no vacíos')
        elif evidence is None:
            errs.append(f'{where}: verificación registrada sin evidence')
        elif canon(record['by'])==canon(ident['id']):
            errs.append(f'{where}: autoverificación no permitida')
    return errs


def identity_level(ident):
    if ident.get('verification'):
        return f"verificación registrada por {ident['verification']['by']}; {NOT_CHECKED}"
    if ident.get('evidence'):
        return 'con evidencia; sin verificación registrada'
    return 'solo declarada'


def structure_errors(m: dict):
    version=m.get('schema_version')
    if type(version) is not int or version not in (1,2):
        return ['schema_version inválido (admitidos: 1, 2)']
    errs=[f'{k}: debe ser texto' for k in ('id','title','risk','created_at') if not _text(m.get(k))]
    gates=m.get('gates')
    if not isinstance(gates,dict) or set(gates)!=set(GATES):
        errs.append('gates: objeto con gate1, gate2 y gate3 exactamente')
    else:
        for name in GATES:
            g=gates[name]
            if not isinstance(g,dict):
                errs.append(f'{name}: debe ser objeto')
                continue
            if not isinstance(g.get('decision'),str) or g['decision'] not in DECISIONS:
                errs.append(f'{name}: decisión inválida')
            errs+=[f'{name}.{k}: texto o null' for k in ('reviewed_artifact','evidence_file','date')
                   if g.get(k) is not None and not _text(g.get(k))]
            if version==1:
                if g.get('reviewer_id') is not None and not _text(g.get('reviewer_id')):
                    errs.append(f'{name}.reviewer_id: texto o null')
            else:
                if 'reviewer_id' in g:
                    errs.append(f'{name}: reviewer_id no admitido en v2')
                if g.get('reviewer') is not None:
                    errs+=ident_errors(g['reviewer'],f'{name}.reviewer')
    owner=m.get('owner_acceptance')
    if (not isinstance(owner,dict) or not isinstance(owner.get('status'),str)
            or owner['status'] not in OWNER_STATUS):
        errs.append('aceptación del propietario inválida')
    else:
        errs+=[f'owner_acceptance.{k}: texto o null' for k in ('approved_by','date')
               if owner.get(k) is not None and not _text(owner.get(k))]
    if version==1:
        errs+=[f'{k} vacío' for k in ('author','implementation_author') if not _text(m.get(k),True)]
        return errs
    errs+=[f'{k} no admitido en v2' for k in ('author','implementation_author') if k in m]
    roles=m.get('roles')
    if not isinstance(roles,dict) or set(roles)!=set(ROLES):
        return errs+['roles: objeto con orchestrator, architect y developer exactamente']
    for role in ROLES:
        idents=roles[role]
        if not isinstance(idents,list):
            errs.append(f'roles.{role}: debe ser lista')
            continue
        seen=set()
        for i,ident in enumerate(idents):
            found=ident_errors(ident,f'roles.{role}[{i}]')
            errs+=found
            if not found:
                if canon(ident['id']) in seen:
                    errs.append(f'roles.{role}: identidad duplicada {ident["id"]}')
                seen.add(canon(ident['id']))
    if isinstance(roles['orchestrator'],list) and not roles['orchestrator']:
        errs.append('roles.orchestrator vacío')
    return errs


def legacy_errors(folder: Path, m: dict):
    """Schema v1 rules, unchanged; v1 records are historical and never enable transitions."""
    errs=[]
    gates=m['gates']
    preceding=True
    for name in GATES:
        g=gates[name]
        decision=g['decision']
        if decision=='PASS':
            reviewer=str(g.get('reviewer_id') or '').strip()
            who=str(m.get('author') if name=='gate1' else m.get('implementation_author') or '').strip()
            if not reviewer: errs.append(f'{name}: falta revisor identificado')
            if reviewer and reviewer.casefold()==who.casefold():
                errs.append(f'{name}: autoaprobación no permitida')
            if not has_evidence(folder,g.get('evidence_file')):
                errs.append(f'{name}: falta informe independiente real, no plantilla')
            if not str(g.get('reviewed_artifact') or '').strip():
                errs.append(f'{name}: falta hash/revisión evaluada')
            if not str(g.get('date') or '').strip():
                errs.append(f'{name}: falta fecha de revisión')
            if not preceding:
                errs.append(f'{name}: Gate anterior no tiene PASS')
        else:
            preceding=False
    acceptance=m['owner_acceptance']
    if acceptance['status']=='APPROVED':
        if any(gates[g]['decision']!='PASS' for g in GATES):
            errs.append('owner APPROVED sin tres Gates PASS')
        if not acceptance.get('approved_by') or not acceptance.get('date'):
            errs.append('aprobación del owner sin identidad/fecha')
    return errs


def report_errors(name: str, text: str, g: dict, pertinent: set, pertinent_role: str):
    errs=[]
    decision=g['decision']
    reviewer=labels(text,'Revisor')
    if len(reviewer)!=1 or (g.get('reviewer') and canon(reviewer[0])!=canon(g['reviewer']['id'])):
        errs.append(f'{name}: inconsistencia informe/manifiesto en Revisor')
    verdict=labels(text,'Dictamen')
    if len(verdict)!=1 or verdict[0]!=decision:
        errs.append(f'{name}: inconsistencia informe/manifiesto en Dictamen')
    artifact=labels(text,'Artefacto revisado')
    if len(artifact)!=1 or ' '.join(artifact[0].split())!=' '.join(str(g.get('reviewed_artifact') or '').split()):
        errs.append(f'{name}: trazabilidad incompleta: Artefacto revisado no coincide')
    authors=labels(text,'Autor efectivo')
    names={canon(a) for a in authors[0].split(',') if canon(a)} if len(authors)==1 else set()
    if not names or not names<=pertinent:
        errs.append(f'{name}: trazabilidad incompleta: Autor efectivo debe ser subconjunto no vacío de {pertinent_role}')
    if decision in ENABLING:
        independence=labels(text,'Independencia verificada')
        match=INDEPENDENCE.match(canon(independence[0])) if len(independence)==1 else None
        evidence=re.sub(r'^\W+','',match.group(1)) if match else ''
        if not match or match.group(1).startswith('[') or not evidence or re.match(r'no\b',evidence):
            errs.append(f'{name}: independencia no acreditada en el informe')
    return errs


def v2_errors(folder: Path, m: dict):
    errs=[]
    roles=m['roles']
    ids={role:{canon(i['id']) for i in roles[role]} for role in ROLES}
    authors=ids['orchestrator']|ids['architect']|ids['developer']
    gates=m['gates']
    preceding=True
    for name in GATES:
        g=gates[name]
        decision=g['decision']
        if decision=='PENDING':
            preceding=False
            continue
        pertinent_role='architect' if name=='gate1' else 'developer'
        pertinent=ids[pertinent_role]
        reviewer=g.get('reviewer')
        if reviewer is None:
            errs.append(f'{name}: falta revisor identificado')
        if not pertinent:
            errs.append(f'{name}: autor efectivo desconocido ({pertinent_role} vacío): independencia no evaluable')
        artifact=str(g.get('reviewed_artifact') or '')
        if not VERSION_ID.search(artifact) or not VERSION_ID.sub('',artifact).strip():
            errs.append(f'{name}: trazabilidad incompleta: reviewed_artifact requiere nombre y sha256:/git:')
        if not str(g.get('date') or '').strip():
            errs.append(f'{name}: falta fecha de revisión')
        text=report_text(folder,g.get('evidence_file'))
        if text is None:
            errs.append(f'{name}: falta informe independiente real, no plantilla')
        else:
            errs+=report_errors(name,text,g,pertinent,pertinent_role)
        if decision in ENABLING:
            if reviewer is not None:
                if canon(reviewer['id']) in authors:
                    errs.append(f'{name}: autoaprobación/independencia: el revisor figura como orchestrator, architect o developer')
                if reviewer['verification'] is None:
                    errs.append(f'{name}: revisor sin verificación registrada')
                elif canon(reviewer['verification']['by']) in pertinent:
                    errs.append(f'{name}: revisor registrado como verificado por el autor revisado')
            needed=('orchestrator','architect') if name=='gate1' else ROLES
            for role in needed:
                for ident in roles[role]:
                    if ident['verification'] is None:
                        errs.append(f'{name}: {role} {ident["id"]} sin verificación registrada')
            if not preceding:
                errs.append(f'{name}: Gate anterior no tiene PASS')
        if decision!='PASS':
            preceding=False
    acceptance=m['owner_acceptance']
    if acceptance['status']=='APPROVED':
        if any(gates[g]['decision']!='PASS' for g in GATES):
            errs.append('owner APPROVED sin tres Gates PASS')
        if not str(acceptance.get('approved_by') or '').strip() or not str(acceptance.get('date') or '').strip():
            errs.append('aprobación del owner sin identidad/fecha')
        elif canon(acceptance['approved_by']) in ids['developer']|ids['architect']:
            errs.append('aprobación por autor del trabajo')
    return errs


def mission_errors(folder: Path, m: dict):
    errs=structure_errors(m)
    if errs:
        return errs
    if m['id']!=folder.name: errs.append('id no coincide con carpeta')
    if not m['title'].strip(): errs.append('título vacío')
    if m['risk'] not in RISK: errs.append('risk inválido')
    for file in MISSION_FILES:
        if not (folder/file).is_file(): errs.append(f'falta {file}')
    return errs+(legacy_errors(folder,m) if m['schema_version']==1 else v2_errors(folder,m))


def project_report(root: Path):
    errors=[f'falta {file}' for file in FILES if not (root/file).is_file()]
    warnings=[]
    if (root/'quality/controls.json').exists():
        try:
            policy=read_json(root/'quality/controls.json')
            if policy.get('gate_order')!=list(GATES) or not policy.get('independent_review_required'):
                errors.append('controls.json sin Gates ordenados o independencia')
        except ValueError as exc:
            errors.append(str(exc))
    folder=root/'docs/MISSIONS'
    if not folder.is_dir():
        errors.append('falta docs/MISSIONS')
    else:
        for child in sorted(p for p in folder.iterdir() if p.is_dir()):
            try:
                m=read_json(child/'mission.json')
            except ValueError as exc:
                errors.append(str(exc))
                continue
            found=mission_errors(child,m)
            errors+=[f'{child.name}: {e}' for e in found]
            if not found and m['schema_version']==1:
                warnings.append(f'{child.name} v1 histórico; no habilita autorizaciones')
    return errors,warnings


def project_errors(root: Path):
    return project_report(root)[0]


def print_status(m: dict, errs: list):
    if structure_errors(m):
        print('INVALID')
        return
    print(f"{m['id']} · {m['title']} · {m['risk']} · schema v{m['schema_version']}")
    if m['schema_version']==1:
        print('v1 histórico; no habilita autorizaciones')
        for name in GATES:
            g=m['gates'][name]
            print(name.upper(),g['decision'],'revisor:',g.get('reviewer_id') or '—')
    else:
        for role in ROLES:
            people=', '.join(f"{i['id']} ({identity_level(i)})" for i in m['roles'][role])
            print(f'{role}: {people or "—"}')
        for name in GATES:
            g=m['gates'][name]
            r=g.get('reviewer')
            print(name.upper(),g['decision'],'revisor:',f"{r['id']} ({identity_level(r)})" if r else '—')
    print('OWNER',m['owner_acceptance']['status'])


def main(argv=None):
    parser=argparse.ArgumentParser(description='Validación FORMAL; no emite PASS ni comprueba identidades')
    parser.add_argument('command',choices=['validate','status','can-implement','can-close'])
    parser.add_argument('--mission')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    root=args.root.resolve()
    if args.command=='validate':
        errors,warnings=project_report(root)
        for warning in warnings: print('AVISO:',warning)
        if errors:
            print('FAIL (estructura/metadatos)')
            for error in errors: print(' -',error)
            return 1
        print('OK — estructura consistente. NO es certificación de Quality ni comprobación de identidades.')
        return 0
    if not args.mission:
        parser.error('--mission es obligatorio')
    if not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+', args.mission):
        print('ERROR: ID de misión inválido')
        return 2
    folder=root/'docs/MISSIONS'/args.mission
    try:
        m=read_json(folder/'mission.json')
    except ValueError as exc:
        print(f'ERROR: {exc}')
        return 2
    errs=mission_errors(folder,m)
    legacy=not structure_errors(m) and m['schema_version']==1
    if args.command=='status':
        print_status(m,errs)
    elif args.command=='can-implement':
        if legacy:
            print('BLOCKED: manifiesto v1 histórico; migrar o revalidar en v2.')
            return 1
        if not errs and m['gates']['gate1']['decision']=='PASS':
            print(f'Registro Gate 1 consistente. Identidades: verificación registrada, {NOT_CHECKED}. Verificar revisión REAL y autorización.')
            return 0
        print('BLOCKED: Gate 1 sin PASS independiente documentado.')
        for error in errs: print(' -',error)
        return 1
    elif args.command=='can-close':
        if legacy:
            print('BLOCKED: manifiesto v1 histórico; migrar o revalidar en v2.')
            return 1
        if (not errs and all(m['gates'][g]['decision']=='PASS' for g in GATES)
                and m['owner_acceptance']['status']=='APPROVED'):
            print('Registro formal cerrado; no equivale a autorización de despliegue.')
            return 0
        print('BLOCKED: Gates 1/2/3 y owner no aprobados.')
        for error in errs: print(' -',error)
        return 1
    if errs:
        for error in errs: print(' -',error)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
