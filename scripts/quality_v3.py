"""Validation of structured v3 governance records; declarations are not certifications."""
import hashlib
import json
import os
import re
from datetime import date
from pathlib import Path

GATES = ('gate1', 'gate2', 'gate3')
RISKS = ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')
ISOLATION = ('I0_CONTEXTO_COMPARTIDO', 'I1_CONTEXTO_SEPARADO', 'I2_PERMISOS_SEPARADOS', 'I3_ENTORNO_SEPARADO')
GUARANTEE = ('G0_DECLARADA', 'G1_EVIDENCIA_REGISTRADA', 'G2_VERIFICACION_REGISTRADA')
KINDS = {'identity', 'isolation', 'execution'}
REF = re.compile(r'(?:git:[0-9a-fA-F]{7,40}(?:\.\.[0-9a-fA-F]{7,40})?|sha256(?:_lf)?:[0-9a-fA-F]{64})')
PATH = re.compile(r'[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*')
HEX = re.compile(r'[0-9a-fA-F]{64}')
KEYS = {'mission', 'gate', 'risk', 'decision', 'reviewer', 'artifact', 'effective_authors',
        'authorship_independent', 'isolation', 'evidence', 'date'}
FILES = {'01-PLAN.md', '02-GATE1-REVIEW.md', '03-IMPLEMENTATION.md',
         '04-GATE2-REVIEW.md', '05-GATE3-EVIDENCE.md', '06-DECISION.md'}


def digest(data):
    return hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()


def canonical_file(folder, name):
    if not isinstance(name, str) or not PATH.fullmatch(name):
        return None
    parts = name.split('/')
    if any(part in ('.', '..') for part in parts):
        return None
    try:
        current = folder
        for part in parts:
            if part not in os.listdir(current):
                return None
            current = current / part
            if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
                return None
        if not current.resolve().is_relative_to(folder.resolve()) or not current.is_file():
            return None
        return current
    except (OSError, ValueError):
        return None


def policy_errors(policy):
    if not isinstance(policy, dict) or policy.get('schema_version') != 2:
        return ['controls: schema_version 2 required']
    matrix = policy.get('independence_minimums')
    if not isinstance(matrix, dict) or set(matrix) != set(RISKS):
        return ['controls: missing or incomplete independence_minimums']
    errs = []
    for risk in RISKS:
        row = matrix[risk]
        if not isinstance(row, dict) or set(row) != set(GATES):
            errs.append('controls: incomplete ' + risk)
            continue
        for gate in GATES:
            rule = row[gate]
            if not isinstance(rule, dict) or set(rule) != {'isolation', 'guarantee', 'evidence', 'pinned_artifact'}:
                errs.append('controls: invalid rule ' + risk + '/' + gate)
                continue
            iso, guarantee, evidence, pinned = (rule[k] for k in ('isolation', 'guarantee', 'evidence', 'pinned_artifact'))
            if (iso not in ISOLATION or guarantee not in GUARANTEE or
                    not isinstance(evidence, list) or any(not isinstance(x, str) or x not in KINDS for x in evidence)
                    or len(evidence) != len(set(evidence)) or type(pinned) is not bool):
                errs.append('controls: invalid values ' + risk + '/' + gate)
            elif guarantee != GUARANTEE[0] and not evidence:
                errs.append('controls: empty evidence types ' + risk + '/' + gate)
    if errs:
        return errs
    for gate in GATES:
        for lower, higher in zip(RISKS, RISKS[1:]):
            a, b = matrix[lower][gate], matrix[higher][gate]
            if (ISOLATION.index(a['isolation']) > ISOLATION.index(b['isolation']) or
                GUARANTEE.index(a['guarantee']) > GUARANTEE.index(b['guarantee']) or
                not set(a['evidence']) <= set(b['evidence']) or
                (a['pinned_artifact'] and not b['pinned_artifact'])):
                errs.append('controls: non-monotonic ' + gate + '/' + higher)
    return errs


def parse_block(data, v5=False):
    try:
        text = data.replace(b'\r\n', b'\n').decode('utf-8')
    except UnicodeError:
        return None
    if '\x00' in text:
        return None
    lines = text.split('\n')
    starts = [i for i, line in enumerate(lines) if line == '```protheusai-review']
    if len(starts) != 1:
        return None
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines)) if lines[i] == '```'), None)
    if end is None or any(line.startswith('```') for line in lines[start+1:end]):
        return None
    try:
        value = json.loads('\n'.join(lines[start+1:end]), object_pairs_hook=_unique)
    except (ValueError, TypeError):
        return None
    if v5:
        return value if isinstance(value, dict) and set(value) == KEYS | {'scope_digest', 'reviewer_session'} else None
    return value if isinstance(value, dict) and set(value) == KEYS else None


def _unique(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result


def valid_verification(value, target, forbidden, canon, reviewer=False):
    fields = {'id', 'by', 'method', 'ref', 'date'} if reviewer else {'by', 'method', 'ref', 'date'}
    if not isinstance(value, dict) or set(value) != fields:
        return False
    if not all(isinstance(x, str) and canon(x) for x in value.values()):
        return False
    if reviewer and canon(value['id']) != target:
        return False
    by = canon(value['by'])
    return bool(by) and by not in forbidden and by != target


def calculated_guarantee(required, present, reviewer_verified, authors_verified):
    # The level records presence and shape, not the truth of the records.
    if not required or not set(required) <= present:
        return GUARANTEE[0]
    if reviewer_verified and authors_verified:
        return GUARANTEE[2]
    return GUARANTEE[1]


def gate_errors(folder, mission, gate, policy, canon, exception_gate1=False, v5_scope_digest=None):
    errors, minima = [], []
    if exception_gate1 and (gate != 'gate1' or mission.get('risk') != 'HIGH'):
        return ['invalid exception scope'], []
    g = mission['gates'][gate]
    decision = g['decision']
    review = g.get('review')
    if decision == 'PENDING':
        return (['review must be null for PENDING'] if review is not None else []), []
    if (not isinstance(review, dict) or set(review) != {'file', 'sha256_lf', 'reviewer_verification'}
            or not isinstance(review.get('sha256_lf'), str) or not HEX.fullmatch(review['sha256_lf'])):
        return ['invalid review reference'], []
    report = canonical_file(folder, review['file'])
    if report is None:
        return ['review path invalid or missing'], []
    try:
        data = report.read_bytes()
    except OSError:
        return ['review unreadable'], []
    if digest(data).lower() != review['sha256_lf'].lower():
        errors.append('review hash mismatch')
    block = parse_block(data, v5=v5_scope_digest is not None)
    if block is None:
        return errors + ['invalid structured review block'], []
    if v5_scope_digest is not None:
        if block['scope_digest'] != v5_scope_digest:
            errors.append('scope digest mismatch')
        if block['reviewer_session'] is not None and not canon(block['reviewer_session']):
            errors.append('reviewer session invalid')
    for key, expected in (('mission', mission['id']), ('gate', gate), ('risk', mission['risk']), ('decision', decision)):
        if block.get(key) != expected:
            errors.append('review mismatch: ' + key)
    reviewer = canon(block.get('reviewer'))
    if not reviewer:
        errors.append('missing reviewer')
    roles = mission['roles']
    all_authors = {canon(i['id']) for role in roles.values() for i in role}
    pertinent = roles['architect' if gate == 'gate1' else 'developer']
    allowed = {canon(i['id']) for i in pertinent}
    effective = block['effective_authors']
    if (not allowed or not isinstance(effective, list) or not effective or
            any(not canon(a) for a in effective) or
            not {canon(a) for a in effective} <= allowed):
        errors.append('effective authors invalid')
    artifact = block['artifact']
    artifact_path = None
    if (not isinstance(artifact, dict) or set(artifact) != {'name', 'ref', 'path'}
            or not isinstance(artifact.get('name'), str) or not canon(artifact['name'])
            or not isinstance(artifact.get('ref'), str) or not REF.fullmatch(artifact['ref'])
            or (artifact.get('path') is not None and not isinstance(artifact['path'], str))):
        errors.append('artifact invalid')
    else:
        if artifact['path'] is not None:
            artifact_path = canonical_file(folder, artifact['path'])
            if artifact_path is None:
                errors.append('artifact path invalid')
            elif artifact['ref'].startswith('sha256_lf:'):
                try:
                    if digest(artifact_path.read_bytes()).lower() != artifact['ref'][10:].lower():
                        errors.append('artifact hash mismatch')
                except OSError:
                    errors.append('artifact unreadable')
    try:
        date_text = block['date']
        if not isinstance(date_text, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', date_text):
            raise ValueError('invalid date format')
        date.fromisoformat(date_text)
    except ValueError:
        errors.append('date invalid')
    if type(block['authorship_independent']) is not bool:
        errors.append('authorship declaration invalid')
    isolation = block['isolation']
    if not isinstance(isolation, str) or isolation not in ISOLATION:
        errors.append('isolation invalid')
    evidence = block['evidence']
    present, paths = set(), set()
    if not isinstance(evidence, list):
        errors.append('evidence invalid')
    else:
        for item in evidence:
            if (not isinstance(item, dict) or set(item) != {'kind', 'path', 'sha256_lf'}
                    or not isinstance(item.get('kind'), str) or item['kind'] not in KINDS
                    or not isinstance(item.get('path'), str) or not isinstance(item.get('sha256_lf'), str)
                    or not HEX.fullmatch(item['sha256_lf'])):
                errors.append('evidence entry invalid')
                continue
            name = item['path']
            path = canonical_file(folder, name)
            if (name in paths or name in FILES or name == 'mission.json' or name == review['file']
                    or (artifact_path is not None and path is not None and path.resolve() == artifact_path.resolve())
                    or path is None):
                errors.append('evidence excluded, duplicated or invalid')
                continue
            paths.add(name)
            try:
                if digest(path.read_bytes()).lower() != item['sha256_lf'].lower():
                    errors.append('evidence hash mismatch')
                else:
                    present.add(item['kind'])
            except OSError:
                errors.append('evidence unreadable')
    verification = review['reviewer_verification']
    if verification is not None and not valid_verification(verification, reviewer, all_authors | {reviewer}, canon, True):
        errors.append('reviewer verification invalid')
    if decision not in ('PASS', 'PASS_WITH_RESERVATIONS'):
        return errors, minima
    if reviewer in all_authors or block['authorship_independent'] is not True:
        errors.append('self approval or authorship declaration invalid')
    if not exception_gate1 and v5_scope_digest is None:
        if isolation == ISOLATION[0]:
            errors.append('I0 cannot enable decision')
    rule = policy['independence_minimums'][mission['risk']][gate]
    if v5_scope_digest is not None:
        rule = {'isolation': ISOLATION[0], 'guarantee': GUARANTEE[0], 'evidence': [],
                'pinned_artifact': mission['risk'] in ('MEDIUM', 'HIGH') and gate == 'gate2'}
    if not exception_gate1 and v5_scope_digest is None:
        if isolation in ISOLATION and ISOLATION.index(isolation) < ISOLATION.index(rule['isolation']):
            minima.append('isolation below minimum')
        if not set(rule['evidence']) <= present:
            minima.append('required evidence missing')
    if rule['pinned_artifact']:
        pinned = isinstance(artifact, dict) and isinstance(artifact.get('ref'), str) and (
            artifact['ref'].startswith('git:') or
            (artifact['ref'].startswith('sha256_lf:') and artifact_path is not None and
             bool(re.fullmatch(r'GATE2-INPUT-[0-9]{2}\.sha256', artifact.get('path') or ''))))
        if not pinned:
            minima.append('pinned artifact required')
    forbidden = all_authors | {reviewer}
    reviewer_verified = valid_verification(verification, reviewer, forbidden, canon, True)
    authors_verified = all(valid_verification(i.get('verification'), canon(i['id']), forbidden, canon)
                           for i in pertinent)
    level = calculated_guarantee(rule['evidence'], present, reviewer_verified, authors_verified)
    if not exception_gate1 and v5_scope_digest is None:
        if GUARANTEE.index(level) < GUARANTEE.index(rule['guarantee']):
            minima.append('guarantee below minimum')
    if exception_gate1 and 'execution' not in present:
        errors.append('execution evidence required')
    if rule['guarantee'] == GUARANTEE[2]:
        if not valid_verification(verification, reviewer, forbidden, canon, True):
            minima.append('reviewer verification required')
        for ident in pertinent:
            if not valid_verification(ident.get('verification'), canon(ident['id']), forbidden, canon):
                minima.append('author verification required')
    return errors, minima


def v3_errors(folder, mission, policy, canon, enforce_minima=True, waiver_actions=frozenset()):
    errors, minima = [], []
    prior = True
    for gate in GATES:
        decision = mission['gates'][gate]['decision']
        e, low = gate_errors(folder, mission, gate, policy, canon)
        errors.extend(gate + ': ' + x for x in e)
        minima.extend(gate + ': ' + x for x in low)
        waived_prior = (mission['gates']['gate1']['decision'] == 'PENDING'
                        and ((gate == 'gate2' and 'gate2' in waiver_actions)
                             or (gate == 'gate3' and 'gate3' in waiver_actions
                                 and mission['gates']['gate2']['decision'] == 'PASS')))
        if decision in ('PASS', 'PASS_WITH_RESERVATIONS') and not prior:
            if not waived_prior:
                errors.append(gate + ': previous gate lacks PASS')
        if decision != 'PASS':
            prior = False
    owner = mission['owner_acceptance']
    if owner['status'] == 'APPROVED':
        waived_close = (mission['gates']['gate1']['decision'] == 'PENDING'
                        and 'close' in waiver_actions
                        and all(mission['gates'][g]['decision'] == 'PASS' for g in ('gate2', 'gate3')))
        if any(mission['gates'][g]['decision'] != 'PASS' for g in GATES):
            if not waived_close:
                errors.append('owner APPROVED requires three PASS')
        if not canon(owner.get('approved_by')) or not canon(owner.get('date')):
            errors.append('owner approval missing identity/date')
        elif canon(owner['approved_by']) in {canon(i['id']) for role in ('architect','developer') for i in mission['roles'][role]}:
            errors.append('owner approval by author')
    return errors + (minima if enforce_minima else []), minima
