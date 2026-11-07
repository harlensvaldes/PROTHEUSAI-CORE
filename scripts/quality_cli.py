#!/usr/bin/env python3
"""Validates documentation records; never grants a Quality Gate PASS nor checks identities."""
import argparse
import json
import re
import unicodedata
import hashlib
from quality_v3 import policy_errors, v3_errors, digest, _unique, canonical_file, parse_block, HEX
from quality_v3 import PATH as RELATIVE_PATH
from quality_v4 import ROOT_KEYS, waiver_errors, waiver_current
from quality_v5 import scope_errors, v5_errors
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
NOT_CHECKED='no comprobada por la CLI'
MANIFEST_LINE=re.compile(r'^[ \t]*(?:[ MADRCU?!]{1,2}[ \t]+)?([0-9a-fA-F]{64})[ \t]+([^ \t].*?)[ \t]*$')
HEX_TOKEN=HEX
TRUNCATED_HEX=re.compile(r'[0-9a-fA-F]{63}(?![0-9a-fA-F])')
CYCLE=re.compile(r'-([0-9]+)(?:\.RECONSTRUCTED)?\.sha256$')
GOVERNANCE_DIRS=('docs/','quality/','agents/')
GOVERNANCE_FILES={'AGENTS.md','START_HERE.md','CONTRIBUTING.md','FILE_INDEX.md','README.md'}
GOVERNANCE_RECORD=re.compile(r'(?:PLAN|REVIEW|OWNER|CORE)-[^/]*\.(?:md|sha256)')


def classify(name):
    """Presentation heuristic only: never changes which artifacts belong to a Gate."""
    if name.startswith(GOVERNANCE_DIRS) or name in GOVERNANCE_FILES:
        return 'gobernanza'
    if '/' not in name and GOVERNANCE_RECORD.fullmatch(name):
        return 'gobernanza'
    return 'producto/implementación'


def parse_manifest(path: Path):
    """Reads declared sha256_lf entries; unknown prose is ignored, ambiguity is not guessed."""
    text=path.read_bytes().decode('utf-8')
    entries, errors = [], []
    for number,line in enumerate(text.splitlines(),1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match=MANIFEST_LINE.match(line)
        if match:
            entries.append((number, match.group(2).strip(), match.group(1).lower()))
        elif HEX.search(line) or TRUNCATED_HEX.search(line):
            errors.append(f'línea {number}: entrada ambigua (hash sha256 no interpretable)')
    return entries, errors


def manifest_report(root: Path, path: Path):
    entries, errors = parse_manifest(path)
    if not entries and not errors:
        errors.append('manifiesto sin entradas')
    seen=set()
    verified=0
    counts={'gobernanza':0,'producto/implementación':0}
    for number,name,declared in entries:
        counts[classify(name)]+=1
        if name in seen:
            errors.append(f'{name}: ruta duplicada en el manifiesto')
            continue
        seen.add(name)
        if not RELATIVE_PATH.fullmatch(name) or any(part in ('.','..') for part in name.split('/')):
            errors.append(f'{name}: ruta no canónica')
            continue
        target=canonical_file(root,name)
        if target is None:
            errors.append(f'{name}: archivo ausente, no regular o fuera de la raíz')
            continue
        try:
            actual=digest(target.read_bytes())
        except OSError as exc:
            errors.append(f'{name}: ilegible ({exc.__class__.__name__})')
            continue
        if actual.lower()!=declared:
            errors.append(f'{name}: sha256_lf no coincide (declarado {declared}, calculado {actual})')
        else:
            verified+=1
    return {'entries':entries,'verified':verified,'errors':errors,'counts':counts}


def read_json(path: Path):
    try:
        text=path.read_text(encoding='utf-8')
        class PairObject(dict):
            def __init__(self, pairs):
                super().__init__(pairs)
                self.versions = [v for k,v in pairs if k == 'schema_version']
        data=json.loads(text, object_pairs_hook=PairObject)
        if isinstance(data,dict) and (data.get('schema_version')==4 or 5 in data.versions):
            data=json.loads(text,object_pairs_hook=_unique)
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
    if type(version) is not int or version not in (1,2,3,4,5):
        return ['schema_version inválido (admitidos: 1, 2)']
    errs=[f'{k}: debe ser texto' for k in ('id','title','risk','created_at') if not _text(m.get(k))]
    if version==4 and set(m)!=ROOT_KEYS:
        errs.append('invalid v4 root keys')
    if version in (1,2,3) and ({'pilot_project','gate1_waiver'} & set(m)):
        errs.append('v4 waiver fields not allowed in legacy schema')
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
            if version in (3,4,5):
                if set(g)!={'decision','review'}:
                    errs.append(f'{name}: invalid v3 keys')
                continue
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


def mission_errors(folder: Path, m: dict):
    errs=structure_errors(m)
    if errs:
        return errs
    if m['schema_version']==5:
        errs.extend(scope_errors(m,canon))
        if errs:
            return errs
    if m['schema_version'] in (1,2):
        return errs
    for role, identities in m['roles'].items():
        for ident in identities:
            for field in ('evidence','verification'):
                record=ident.get(field)
                if record is not None and not all(canon(value) for value in record.values()):
                    errs.append(f'roles.{role}.{field}: empty canonical field')
    if m['id']!=folder.name: errs.append('id no coincide con carpeta')
    if not m['title'].strip(): errs.append('título vacío')
    if m['risk'] not in RISK: errs.append('risk inválido')
    for file in MISSION_FILES:
        if not (folder/file).is_file(): errs.append(f'falta {file}')
    if m['schema_version'] in (1,2):
        return errs
    if errs:
        return errs
    try:
        policy=read_json(folder.parents[2]/'quality/controls.json')
    except ValueError as exc:
        return errs+[str(exc)]
    policy_errs=policy_errors(policy)
    if policy_errs:
        return errs+policy_errs
    actions=frozenset()
    if m['schema_version']==5:
        return errs+v5_errors(folder,m,policy,canon)
    if m['schema_version']==4:
        pilot=m.get('pilot_project')
        if (not isinstance(pilot,dict) or set(pilot)!={'id','local_fictional'}
                or not canon(pilot.get('id')) or type(pilot.get('local_fictional')) is not bool):
            return errs+['invalid pilot project']
        invalid=waiver_errors(folder,m,policy,canon,m['owner_acceptance']['status']=='APPROVED')
        if invalid:
            return errs+invalid
        if m['gate1_waiver']:
            actions=frozenset(m['gate1_waiver']['actions'])
    if m['schema_version']==4:
        found,_=v3_errors(folder,m,policy,canon,m['owner_acceptance']['status']!='APPROVED',actions)
    else:
        found,_=v3_errors(folder,m,policy,canon,m['owner_acceptance']['status']!='APPROVED')
    return errs+found


def project_report(root: Path):
    errors=[f'falta {file}' for file in FILES if not (root/file).is_file()]
    warnings=[]
    if (root/'quality/controls.json').exists():
        try:
            policy=read_json(root/'quality/controls.json')
            if policy.get('gate_order')!=list(GATES) or not policy.get('independent_review_required'):
                errors.append('controls.json sin Gates ordenados o independencia')
            errors.extend(policy_errors(policy))
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
            if not found and m['schema_version'] in (1,2):
                warnings.append(f'{child.name} v{m["schema_version"]} historico; no habilita autorizaciones')
            if not found and m['schema_version']==4 and m.get('gate1_waiver'):
                warnings.append(f'{child.name}: OWNER_AUTHORIZATION_AND_HISTORICAL_VALIDITY_NOT_VERIFIED')
            if not found and m['schema_version']==5:
                warnings.append(f'{child.name}: alcance e identidades declarados, no comprobados por la CLI')
            if not found and m['schema_version']==4 and m['owner_acceptance']['status']=='APPROVED':
                actions=frozenset(m['gate1_waiver']['actions']) if m.get('gate1_waiver') else frozenset()
                _,low=v3_errors(child,m,policy,canon,False,actions)
                if low or (m.get('gate1_waiver') and waiver_errors(child,m,policy,canon)):
                    warnings.append(f'{child.name}: no cumple la matriz vigente')
            if not found and m['schema_version']==3 and m['owner_acceptance']['status']=='APPROVED':
                _, low=v3_errors(child,m,policy,canon,False)
                if low:
                    warnings.append(f'{child.name}: no cumple la matriz vigente')
    return errors,warnings


def project_errors(root: Path):
    return project_report(root)[0]


def _anchor_key(item):
    cycle, reconstructed, name, declared = item
    return (cycle, -reconstructed, name)


def _check_anchor(label, relative, declared, anchors, mission, errors, warnings):
    anchored=anchors.get(f'docs/MISSIONS/{mission}/{relative}')
    if not anchored:
        warnings.append(f'{label}: {relative} no figura en ningún manifiesto de la misión (no es requisito de Gate)')
        return
    hashes={item[3] for item in anchored}
    if declared not in hashes:
        errors.append(f'{label}: {relative} versión registrada no anclada '
                      f'(registrado {declared}, anclas {", ".join(sorted(hashes))})')
        return
    effective=max(anchored,key=_anchor_key)
    if declared!=effective[3]:
        warnings.append(f'{label}: {relative} coincide con un ciclo anterior ({declared}); '
                        f'ancla efectiva {effective[3]} en {effective[2]}')


def audit_report(root: Path, mission: str):
    """Cross-checks record hashes against manifest anchors; tree drift is advisory only."""
    folder=root/'docs/MISSIONS'/mission
    m=read_json(folder/'mission.json')
    errors=mission_errors(folder,m)
    warnings=[]
    anchors={}
    summaries=[]
    for path in sorted(p for p in folder.glob('*.sha256') if p.is_file()):
        try:
            entries, format_errors=parse_manifest(path)
        except (OSError,UnicodeError) as exc:
            return m, None, [], [f'{path.name}: no se puede leer ({exc.__class__.__name__})']
        if not entries and not format_errors:
            format_errors=['manifiesto sin entradas']
        match=CYCLE.search(path.name)
        cycle=int(match.group(1)) if match else 0
        reconstructed=1 if '.RECONSTRUCTED' in path.name else 0
        counts={'gobernanza':0,'producto/implementación':0}
        seen=set()
        for number,name,declared in entries:
            counts[classify(name)]+=1
            if name in seen:
                format_errors.append(f'{name}: ruta duplicada en el manifiesto')
                continue
            seen.add(name)
            if (not RELATIVE_PATH.fullmatch(name)
                    or any(part in ('.','..') for part in name.split('/'))):
                format_errors.append(f'{name}: ruta no canónica')
                continue
            anchors.setdefault(name,[]).append((cycle,reconstructed,path.name,declared))
        if format_errors:
            errors.extend(f'{path.name}: {error}' for error in format_errors)
        if entries:
            summaries.append((path.name,len(entries),counts))
    for name in sorted(anchors):
        effective=max(anchors[name],key=_anchor_key)
        target=canonical_file(root,name)
        if target is None:
            continue
        try:
            actual=digest(target.read_bytes())
        except OSError:
            continue
        if actual.lower()!=effective[3]:
            warnings.append(f'deriva del árbol respecto al ancla efectiva: {name} '
                            f'(actual {actual.lower()}, ancla {effective[3]} en {effective[2]})')
    v5=m.get('schema_version')==5
    gates=m.get('gates')
    for gate in GATES:
        record=gates.get(gate) if isinstance(gates,dict) else None
        if not isinstance(record,dict):
            continue
        review=record.get('review')
        if record.get('decision')=='PENDING' or not isinstance(review,dict):
            continue
        file=review.get('file')
        raw=review.get('sha256_lf')
        declared=raw.lower() if isinstance(raw,str) else ''
        if not isinstance(file,str) or not declared:
            continue
        _check_anchor(f'{gate}.review',file,declared,anchors,mission,errors,warnings)
        report=canonical_file(folder,file)
        if report is None:
            continue
        try:
            block=parse_block(report.read_bytes(),v5=v5)
        except OSError:
            continue
        if block is None:
            warnings.append(f'{gate}: bloque protheusai-review no interpretable; cruce de evidencias omitido')
            continue
        evidence=block.get('evidence')
        if not isinstance(evidence,list):
            continue
        for index,item in enumerate(evidence):
            if (not isinstance(item,dict) or not isinstance(item.get('path'),str)
                    or not isinstance(item.get('sha256_lf'),str)
                    or not HEX_TOKEN.fullmatch(item['sha256_lf'])):
                continue
            _check_anchor(f'{gate}.evidence[{index}]',item['path'],item['sha256_lf'].lower(),
                          anchors,mission,errors,warnings)
    return m, errors, warnings, summaries


def print_manifest(path: Path, root: Path):
    try:
        report=manifest_report(root,path)
    except (OSError,UnicodeError) as exc:
        print(f'ERROR: no se puede leer {path}: {exc.__class__.__name__}')
        return 2
    counts=report['counts']
    print(f'manifiesto: {path}')
    print(f"entradas: {len(report['entries'])} (gobernanza {counts['gobernanza']}, "
          f"producto/implementación {counts['producto/implementación']})")
    if report['errors']:
        print('FAIL (integridad de manifiesto)')
        for error in report['errors']: print(' -',error)
        return 1
    print(f"OK — {report['verified']}/{len(report['entries'])} hashes sha256_lf coinciden. "
          'Clasificación informativa: no altera qué artefactos forman parte de un Gate.')
    return 0


def print_audit(root: Path, mission: str):
    try:
        m, errors, warnings, summaries = audit_report(root,mission)
    except (ValueError,KeyError,TypeError,AttributeError) as exc:
        print(f'ERROR: {exc}')
        return 2
    risk=m.get('risk')
    version=m.get('schema_version')
    print(f"AUDITORÍA {mission} | {risk if isinstance(risk,str) else 'DESCONOCIDO'} | "
          f"schema v{version if type(version) is int else '?'}")
    if errors is None:
        print('ERROR: no se puede completar la verificación')
        for failure in summaries: print(' -',failure)
        return 2
    if not summaries:
        print('manifiestos: 0 — la misión no declara manifiestos que cruzar')
    for name,total,counts in summaries:
        print(f"manifiesto {name}: {total} entradas (gobernanza {counts['gobernanza']}, "
              f"producto/implementación {counts['producto/implementación']})")
    for warning in warnings: print('AVISO:',warning)
    if errors:
        print('FAIL (discrepancias documentales)')
        for error in errors: print(' -',error)
        return 1
    print('OK — registro y anclas coherentes. No es dictamen de Quality ni comprueba identidades.')
    return 0



def print_status(m: dict, errs: list):
    if structure_errors(m):
        print('INVALID')
        return
    print(f"{m['id']} | {m['title']} | {m['risk']} | schema v{m['schema_version']}")
    if m['schema_version'] in (1,2):
        print(f"v{m['schema_version']} historico; no habilita autorizaciones")
    for name in GATES:
        gate=m['gates'][name]
        print(name.upper(),gate['decision'], 'review:',gate.get('review') if m['schema_version'] in (3,4,5) else 'historical')
    if m['schema_version']==5:
        print('Perfil local ficticio experimental; elegibilidad e identidades no verificadas por la CLI.')
    if m['schema_version']==4 and m.get('gate1_waiver'):
        print('OWNER_WAIVER declarado; autorización e identidad no verificadas por la CLI.')
    print('OWNER',m['owner_acceptance']['status'])
    print('Identidad y aislamiento: declarados, no comprobada por la CLI.')


def main(argv=None):
    parser=argparse.ArgumentParser(description='Validación FORMAL; no emite PASS ni comprueba identidades')
    parser.add_argument('command',choices=['validate','status','can-implement','can-close','hash','manifest','audit'])
    parser.add_argument('path',nargs='?')
    parser.add_argument('--mission')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    root=args.root.resolve()
    if args.command=='hash':
        if not args.path: parser.error('hash requires a path')
        try: data=Path(args.path).read_bytes()
        except OSError as exc:
            print(f'ERROR: {exc}')
            return 2
        print('sha256_lf:',digest(data))
        print('sha256:',hashlib.sha256(data).hexdigest())
        return 0
    if args.command=='manifest':
        if not args.path: parser.error('manifest requires a path')
        return print_manifest(Path(args.path),root)
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
    if args.command=='audit':
        return print_audit(root,args.mission)
    folder=root/'docs/MISSIONS'/args.mission
    try:
        m=read_json(folder/'mission.json')
    except ValueError as exc:
        print(f'ERROR: {exc}')
        return 2
    errs=mission_errors(folder,m)
    legacy=not structure_errors(m) and m['schema_version'] in (1,2)
    if not legacy and not structure_errors(m) and m['schema_version']==3 and args.command in ('can-implement','can-close'):
        try:
            policy=read_json(root/'quality/controls.json')
            perrs=policy_errors(policy)
            if perrs: errs+=perrs
            else: errs+=v3_errors(folder,m,policy,canon,True)[1]
        except (ValueError,KeyError,TypeError) as exc:
            errs.append(str(exc))
    if not legacy and not structure_errors(m) and m['schema_version']==4 and args.command in ('can-implement','can-close'):
        try:
            policy=read_json(root/'quality/controls.json')
            perrs=policy_errors(policy)
            if perrs: errs+=perrs
            elif not errs:
                errs+=waiver_errors(folder,m,policy,canon)
                actions=frozenset(m['gate1_waiver']['actions']) if m.get('gate1_waiver') else frozenset()
                errs+=v3_errors(folder,m,policy,canon,True,actions)[1]
        except (ValueError,KeyError,TypeError) as exc:
            errs.append(str(exc))
    if args.command=='status':
        print_status(m,errs)
    elif args.command=='can-implement':
        if legacy:
            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')
            return 1
        if m.get('schema_version')==4 and m.get('gate1_waiver'):
            if not errs and waiver_current(m,'implement'):
                print('MANUAL_OWNER_VERIFICATION_REQUIRED: Gate 1 PENDING; waiver',m['gate1_waiver']['id'],
                      'implement expires',m['gate1_waiver']['expires_at'])
            else:
                print('BLOCKED: waiver inválido, revocado, caducado o sin acción implement.')
                for error in errs: print(' -',error)
            return 1
        if not errs and m['gates']['gate1']['decision']=='PASS':
            if m['schema_version']==5:
                print('Gate 1 record consistent; this does not authorize implementation; reviewer identity and isolation are not checked by the CLI.')
            else:
                print('Gate 1 record consistent; reviewer identity and isolation are not checked by the CLI.')
            return 0
        print('REVIEW_NOT_PASS: Gate 1 sin PASS; resultado de revisión, no decisión de permisos del entorno ni del Owner.')
        for error in errs: print(' -',error)
        return 1
    elif args.command=='can-close':
        if legacy:
            print('BLOCKED: historical v1/v2 manifest; migrate or revalidate in v3.')
            return 1
        if m.get('schema_version')==4 and m.get('gate1_waiver'):
            if (not errs and waiver_current(m,'close')
                    and all(m['gates'][g]['decision']=='PASS' for g in ('gate2','gate3'))
                    and m['owner_acceptance']['status']=='APPROVED'):
                print('MANUAL_OWNER_VERIFICATION_REQUIRED: cierre con waiver',m['gate1_waiver']['id'],
                      'expires',m['gate1_waiver']['expires_at'])
            else:
                print('BLOCKED: cierre con waiver no habilitado.')
                for error in errs: print(' -',error)
            return 1
        if (not errs and all(m['gates'][g]['decision']=='PASS' for g in GATES)
                and m['owner_acceptance']['status']=='APPROVED'):
            print('Registro formal consistente; no autoriza cierre ni despliegue.' if m['schema_version']==5 else 'Registro formal cerrado; no equivale a autorización de despliegue.')
            return 0
        print('REVIEW_INCOMPLETE: no constan tres PASS y aceptación del Owner; diagnóstico documental, no control de permisos.')
        for error in errs: print(' -',error)
        return 1
    if errs:
        for error in errs: print(' -',error)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
