"""Structural checks for a narrowly scoped owner waiver; never authenticates it."""
import copy
import hashlib
import re
from datetime import datetime, timezone

from quality_v3 import canonical_file, gate_errors, parse_block

ROOT_KEYS = {'schema_version', 'id', 'title', 'risk', 'created_at', 'roles',
             'gates', 'owner_acceptance', 'pilot_project', 'gate1_waiver'}
WAIVER_KEYS = {'id', 'mission', 'project_id', 'owner_id', 'authorization_ref',
               'issued_at', 'not_before', 'expires_at', 'actions', 'exceptions',
               'technical_review', 'artifact', 'revocations', 'prior_failures'}
ACTIONS = {'implement', 'gate2', 'gate3', 'close'}
EXCEPTIONS = {'I1_CONTEXTO_SEPARADO', 'G1_EVIDENCIA_REGISTRADA'}
HEX = re.compile(r'[0-9a-fA-F]{64}')
UTC = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')


def parse_utc(value):
    if not isinstance(value, str) or not UTC.fullmatch(value):
        raise ValueError('invalid UTC timestamp')
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def waiver_errors(folder, mission, policy, canon, historical=False):
    errors = []
    w = mission.get('gate1_waiver')
    if w is None:
        return []
    if not isinstance(w, dict) or set(w) != WAIVER_KEYS:
        return ['waiver: invalid fields']
    pilot = mission.get('pilot_project')
    if (not isinstance(pilot, dict) or set(pilot) != {'id', 'local_fictional'}
            or not canon(pilot.get('id')) or pilot.get('local_fictional') is not True
            or mission.get('risk') != 'HIGH' or w.get('mission') != mission.get('id')
            or w.get('project_id') != pilot.get('id')):
        errors.append('waiver: scope invalid')
    rule = policy['independence_minimums']['HIGH']['gate1']
    if not historical and (rule['isolation'] != 'I1_CONTEXTO_SEPARADO'
            or rule['guarantee'] != 'G1_EVIDENCIA_REGISTRADA'
            or set(rule['evidence']) != {'identity'}):
        errors.append('waiver: policy exceeds explicitly excepted minima')
    roles = mission.get('roles', {})
    role_ids = {canon(item.get('id')) for group in roles.values() for item in group}
    if (not all(canon(w.get(k)) for k in ('id', 'owner_id', 'authorization_ref'))
            or canon(w.get('owner_id')) in role_ids):
        errors.append('waiver: owner or reference invalid')
    acceptance = mission.get('owner_acceptance', {})
    if (acceptance.get('status') == 'APPROVED'
            and canon(acceptance.get('approved_by')) != canon(w.get('owner_id'))):
        errors.append('waiver: acceptance must be attributed to declared owner')
    for field, expected, exact in (('actions', ACTIONS, False), ('exceptions', EXCEPTIONS, True)):
        value = w.get(field)
        if (not isinstance(value, list) or not value or any(not isinstance(x, str) for x in value)
                or len(value) != len(set(value)) or not set(value) <= expected
                or (exact and set(value) != expected)):
            errors.append('waiver: invalid ' + field)
    try:
        issued, start, end = (parse_utc(w[k]) for k in ('issued_at', 'not_before', 'expires_at'))
        if not issued <= start < end:
            raise ValueError('invalid time order')
    except (ValueError, KeyError, TypeError):
        errors.append('waiver: invalid time')
    revocations = w.get('revocations')
    if not isinstance(revocations, list):
        errors.append('waiver: invalid revocations')
    else:
        for item in revocations:
            if (not isinstance(item, dict) or set(item) != {'at', 'reason', 'owner_ref'}
                    or not canon(item.get('reason')) or not canon(item.get('owner_ref'))):
                errors.append('waiver: invalid revocation')
                continue
            try:
                parse_utc(item['at'])
            except (ValueError, KeyError, TypeError):
                errors.append('waiver: invalid revocation time')
    failures = w.get('prior_failures')
    if not isinstance(failures, list):
        errors.append('waiver: invalid prior failures')
    else:
        seen = set()
        for item in failures:
            if (not isinstance(item, dict) or set(item) != {'path', 'sha256_bytes'}
                    or not isinstance(item.get('sha256_bytes'), str)
                    or not HEX.fullmatch(item['sha256_bytes'])):
                errors.append('waiver: invalid prior failure')
                continue
            path = canonical_file(folder, item.get('path'))
            if path is None or item['path'] in seen:
                errors.append('waiver: prior failure path invalid')
                continue
            seen.add(item['path'])
            try:
                data = path.read_bytes()
                block = parse_block(data)
                if (hashlib.sha256(data).hexdigest() != item['sha256_bytes'].lower()
                        or not block or block.get('decision') != 'FAIL'
                        or block.get('gate') != 'gate1' or block.get('mission') != mission['id']):
                    errors.append('waiver: prior failure mismatch')
            except OSError:
                errors.append('waiver: prior failure unreadable')
    if mission['gates']['gate1'] != {'decision': 'PENDING', 'review': None}:
        errors.append('waiver: gate1 must remain pending')
    artifact = w.get('artifact')
    if (not isinstance(artifact, dict) or set(artifact) != {'name', 'ref', 'path'}
            or not isinstance(artifact.get('ref'), str)
            or not re.fullmatch(r'sha256_lf:[0-9a-fA-F]{64}', artifact['ref'])
            or not isinstance(artifact.get('path'), str)):
        errors.append('waiver: artifact invalid')
    fake = copy.deepcopy(mission)
    fake['gates']['gate1'] = {'decision': 'PASS', 'review': w.get('technical_review')}
    review_policy = copy.deepcopy(policy)
    if historical:
        review_policy['independence_minimums']['HIGH']['gate1'] = {
            'isolation': 'I1_CONTEXTO_SEPARADO', 'guarantee': 'G1_EVIDENCIA_REGISTRADA',
            'evidence': ['identity'], 'pinned_artifact': False}
    found, minima = gate_errors(folder, fake, 'gate1', review_policy, canon, exception_gate1=True)
    errors.extend('technical review: ' + x for x in found + minima)
    review = w.get('technical_review')
    if isinstance(review, dict):
        path = canonical_file(folder, review.get('file'))
        if path:
            try:
                block = parse_block(path.read_bytes())
                if not block or block.get('artifact') != artifact:
                    errors.append('waiver: artifact does not match review')
                if block and canon(block.get('reviewer')) == canon(w.get('owner_id')):
                    errors.append('waiver: reviewer cannot authorize own exception')
            except OSError:
                errors.append('waiver: review unreadable')
    return errors


def waiver_current(mission, action, now=None):
    w = mission['gate1_waiver']
    if not w or action not in w['actions'] or w['revocations']:
        return False
    try:
        now = now if now is not None else datetime.now(timezone.utc)
        return parse_utc(w['issued_at']) <= now and parse_utc(w['not_before']) <= now < parse_utc(w['expires_at'])
    except (ValueError, TypeError, KeyError, OverflowError, OSError):
        return False
