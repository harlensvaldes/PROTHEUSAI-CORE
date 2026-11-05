#!/usr/bin/env python3
"""Create mission documents with all Quality Gates explicitly PENDING."""
import argparse
import json
import re
from datetime import date
from pathlib import Path

TEMPLATES = {
    'MISSION_PLAN.md': '01-PLAN.md',
    'GATE1_REVIEW.md': '02-GATE1-REVIEW.md',
    'IMPLEMENTATION_REPORT.md': '03-IMPLEMENTATION.md',
    'GATE2_REVIEW.md': '04-GATE2-REVIEW.md',
    'GATE3_EVIDENCE.md': '05-GATE3-EVIDENCE.md',
    'DECISION.md': '06-DECISION.md',
}

def create_mission(root: Path, mission_id: str, title: str, risk: str, author: str) -> Path:
    if not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+', mission_id):
        raise ValueError('ID inválido; por ejemplo APP-001 o APP-MOD-001')
    if risk not in {'LOW','MEDIUM','HIGH','CRITICAL'}:
        raise ValueError('riesgo inválido')
    if not title.strip() or not author.strip():
        raise ValueError('título y autor son obligatorios')
    contents = {}
    for template, output in TEMPLATES.items():
        contents[output] = (root / 'docs/templates' / template).read_text(encoding='utf-8').replace('[MISSION-ID]', mission_id)
    target = root / 'docs/MISSIONS' / mission_id
    target.mkdir(parents=True, exist_ok=False)
    manifest = {
        'schema_version':1, 'id':mission_id, 'title':title, 'risk':risk,
        'author':author, 'implementation_author':author,
        'created_at':date.today().isoformat(),
        'gates': {g:{'decision':'PENDING','reviewer_id':None,'reviewed_artifact':None,
                     'evidence_file':None,'date':None} for g in ('gate1','gate2','gate3')},
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
    parser.add_argument('--author',required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    try:
        target=create_mission(args.root.resolve(),args.id,args.title,args.risk,args.author)
    except (ValueError,OSError) as exc:
        parser.error(str(exc))
    print(f'{target} — Gates 1, 2 y 3 PENDING; ninguna aprobación inventada')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
