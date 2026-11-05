#!/usr/bin/env python3
"""Create mission documents with all Quality Gates explicitly PENDING."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from quality_cli import canon

TEMPLATES = {
    'MISSION_PLAN.md': '01-PLAN.md',
    'GATE1_REVIEW.md': '02-GATE1-REVIEW.md',
    'IMPLEMENTATION_REPORT.md': '03-IMPLEMENTATION.md',
    'GATE2_REVIEW.md': '04-GATE2-REVIEW.md',
    'GATE3_EVIDENCE.md': '05-GATE3-EVIDENCE.md',
    'DECISION.md': '06-DECISION.md',
}
AUTHOR_DEPRECATED = 'DEPRECATED: --author registrado como orchestrator; developer/architect no asignados'

def declared(identifier: str) -> dict:
    """Identity only declared: evidence and verification must be added from real records."""
    return {'id': identifier, 'evidence': None, 'verification': None}

def create_mission(root: Path, mission_id: str, title: str, risk: str, orchestrator: str,
                   architect: str | None = None) -> Path:
    if not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+', mission_id):
        raise ValueError('ID inválido; por ejemplo APP-001 o APP-MOD-001')
    if risk not in {'LOW','MEDIUM','HIGH','CRITICAL'}:
        raise ValueError('riesgo inválido')
    if not title.strip() or not canon(orchestrator):
        raise ValueError('título y orchestrator son obligatorios')
    if architect is not None and not canon(architect):
        raise ValueError('architect vacío')
    contents = {}
    for template, output in TEMPLATES.items():
        contents[output] = (root / 'docs/templates' / template).read_text(encoding='utf-8').replace('[MISSION-ID]', mission_id)
    target = root / 'docs/MISSIONS' / mission_id
    target.mkdir(parents=True, exist_ok=False)
    manifest = {
        'schema_version':3, 'id':mission_id, 'title':title, 'risk':risk,
        'created_at':date.today().isoformat(),
        'roles': {'orchestrator':[declared(orchestrator)],
                  'architect':[declared(architect)] if architect else [],
                  'developer':[]},
        'gates': {g:{'decision':'PENDING','review':None} for g in ('gate1','gate2','gate3')},
        'owner_acceptance':{'status':'PENDING','approved_by':None,'date':None},
    }
    (target/'mission.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name, content in contents.items():
        (target/name).write_text(content,encoding='utf-8')
    return target

def main(argv=None):
    parser=argparse.ArgumentParser(description='Crear misión; todos los Gates comienzan en PENDING')
    parser.add_argument('--id',required=True)
    parser.add_argument('--title',required=True)
    parser.add_argument('--risk',required=True,choices=['LOW','MEDIUM','HIGH','CRITICAL'])
    parser.add_argument('--orchestrator',help='identidad declarada de quien crea y coordina la misión')
    parser.add_argument('--architect',help='identidad declarada del autor del plan (opcional)')
    parser.add_argument('--author',help='OBSOLETO: alias de --orchestrator')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    if args.author is not None and args.orchestrator is not None:
        parser.error('--author (obsoleto) y --orchestrator son incompatibles')
    if args.author is not None:
        print(AUTHOR_DEPRECATED,file=sys.stderr)
    orchestrator=args.orchestrator if args.orchestrator is not None else args.author
    if orchestrator is None:
        parser.error('--orchestrator es obligatorio')
    try:
        target=create_mission(args.root.resolve(),args.id,args.title,args.risk,orchestrator,args.architect)
    except (ValueError,OSError) as exc:
        parser.error(str(exc))
    print(f'{target} — Gates 1, 2 y 3 PENDING; identidades solo declaradas; developer sin asignar')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
