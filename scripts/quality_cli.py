#!/usr/bin/env python3
"""Validates documentation records; never grants a Quality Gate PASS."""
import argparse
import json
import re
from pathlib import Path

GATES=('gate1','gate2','gate3')
DECISIONS={'PENDING','PASS','PASS_WITH_RESERVATIONS','FAIL'}
RISK={'LOW','MEDIUM','HIGH','CRITICAL'}
FILES=('AGENTS.md','docs/PROJECT_CHARTER.md','docs/ARCHITECTURE.md',
       'docs/QUALITY_POLICY.md','docs/TEST_STRATEGY.md','quality/controls.json',
       'docs/templates/MISSION_PLAN.md','docs/templates/GATE1_REVIEW.md',
       'docs/templates/GATE2_REVIEW.md','docs/templates/GATE3_EVIDENCE.md')
MISSION_FILES=('01-PLAN.md','02-GATE1-REVIEW.md','03-IMPLEMENTATION.md',
               '04-GATE2-REVIEW.md','05-GATE3-EVIDENCE.md','06-DECISION.md')


def read_json(path: Path):
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
    except (ValueError,OSError,UnicodeError) as exc:
        raise ValueError(f'{path}: {exc}') from exc
    if not isinstance(data,dict):
        raise ValueError(f'{path}: JSON debe contener objeto')
    return data


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
    return not ('**Dictamen:** PENDING' in text or '**Revisor:** [IDENTIDAD REAL]' in text)


def mission_errors(folder: Path, m: dict):
    errs=[]
    if m.get('id')!=folder.name: errs.append('id no coincide con carpeta')
    if not str(m.get('title') or '').strip(): errs.append('título vacío')
    if m.get('risk') not in RISK: errs.append('risk inválido')
    if not str(m.get('author') or '').strip(): errs.append('author vacío')
    if not str(m.get('implementation_author') or '').strip(): errs.append('implementation_author vacío')
    for file in MISSION_FILES:
        if not (folder/file).is_file(): errs.append(f'falta {file}')
    gates=m.get('gates')
    if not isinstance(gates,dict): return errs+['gates inválido']
    preceding=True
    for name in GATES:
        g=gates.get(name)
        if not isinstance(g,dict):
            errs.append(f'{name}: objeto ausente')
            preceding=False
            continue
        decision=g.get('decision')
        if decision not in DECISIONS:
            errs.append(f'{name}: decisión inválida')
            preceding=False
            continue
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
    acceptance=m.get('owner_acceptance',{})
    if not isinstance(acceptance,dict) or acceptance.get('status') not in {'PENDING','APPROVED','REJECTED'}:
        errs.append('aceptación del propietario inválida')
    elif acceptance.get('status')=='APPROVED':
        if any(gates.get(g,{}).get('decision')!='PASS' for g in GATES):
            errs.append('owner APPROVED sin tres Gates PASS')
        if not acceptance.get('approved_by') or not acceptance.get('date'):
            errs.append('aprobación del owner sin identidad/fecha')
    return errs


def project_errors(root: Path):
    errors=[f'falta {file}' for file in FILES if not (root/file).is_file()]
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
                errors += [f'{child.name}: {e}' for e in mission_errors(child,read_json(child/'mission.json'))]
            except ValueError as exc:
                errors.append(str(exc))
    return errors


def main(argv=None):
    parser=argparse.ArgumentParser(description='Validación FORMAL; no emite PASS')
    parser.add_argument('command',choices=['validate','status','can-implement','can-close'])
    parser.add_argument('--mission')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    root=args.root.resolve()
    if args.command=='validate':
        errors=project_errors(root)
        if errors:
            print('FAIL (estructura/metadatos)')
            for error in errors: print(' -',error)
            return 1
        print('OK — estructura consistente. NO es certificación de Quality.')
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
    if args.command=='status':
        print(f"{m.get('id')} · {m.get('title')} · {m.get('risk')}")
        for name in GATES:
            g=m.get('gates',{}).get(name,{})
            print(name.upper(),g.get('decision','INVALID'),'revisor:',g.get('reviewer_id') or '—')
        print('OWNER',m.get('owner_acceptance',{}).get('status','INVALID'))
    elif args.command=='can-implement':
        if not errs and m['gates']['gate1']['decision']=='PASS':
            print('Registro Gate 1 consistente. Verificar revisión REAL y autorización.')
            return 0
        print('BLOCKED: Gate 1 sin PASS independiente documentado.')
        return 1
    elif args.command=='can-close':
        if (not errs and all(m['gates'][g]['decision']=='PASS' for g in GATES)
                and m['owner_acceptance']['status']=='APPROVED'):
            print('Registro formal cerrado; no equivale a autorización de despliegue.')
            return 0
        print('BLOCKED: Gates 1/2/3 y owner no aprobados.')
        return 1
    if errs:
        for error in errs: print(' -',error)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
