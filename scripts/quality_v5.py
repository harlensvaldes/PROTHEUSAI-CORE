"""Declarative checks for the local fictional experimental v5 profile."""
import hashlib
import json
from quality_v3 import gate_errors

ROOT_KEYS = {'schema_version', 'id', 'title', 'risk', 'created_at', 'roles', 'gates', 'owner_acceptance', 'scope'}
SCOPE_KEYS = {'profile', 'project_id', 'owner_decision_ref'}
PROFILE = 'LOCAL_FICTIONAL_EXPERIMENTAL'
GATES = ('gate1', 'gate2', 'gate3')


def scope_errors(mission, canon):
    errors = []
    if set(mission) != ROOT_KEYS:
        errors.append('v5: invalid root keys')
    if mission.get('risk') not in ('LOW', 'MEDIUM', 'HIGH'):
        errors.append('v5: invalid risk for profile')
    scope = mission.get('scope')
    if not isinstance(scope, dict) or set(scope) != SCOPE_KEYS:
        return errors + ['v5: invalid scope fields']
    if scope['profile'] != PROFILE:
        errors.append('v5: invalid profile')
    for key in ('project_id', 'owner_decision_ref'):
        value = scope[key]
        if not isinstance(value, str) or not canon(value) or canon(value) in ('[decidir]', '[pendiente]', 'tbd'):
            errors.append('v5: invalid ' + key)
    return errors


def scope_digest(scope):
    raw = json.dumps(scope, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def v5_errors(folder, mission, policy, canon):
    errors = scope_errors(mission, canon)
    if errors:
        return errors
    digest = scope_digest(mission['scope'])
    prior = True
    for gate in GATES:
        decision = mission['gates'][gate]['decision']
        found, minima = gate_errors(folder, mission, gate, policy, canon, v5_scope_digest=digest)
        errors.extend(gate + ': ' + value for value in found + minima)
        if decision in ('PASS', 'PASS_WITH_RESERVATIONS') and not prior:
            errors.append(gate + ': previous gate lacks PASS')
        if decision != 'PASS':
            prior = False
    owner = mission['owner_acceptance']
    if owner['status'] == 'APPROVED':
        if any(mission['gates'][gate]['decision'] != 'PASS' for gate in GATES):
            errors.append('owner APPROVED requires three PASS')
        if not canon(owner.get('approved_by')) or not canon(owner.get('date')):
            errors.append('owner approval missing identity/date')
        elif canon(owner['approved_by']) in {canon(i['id']) for role in ('architect', 'developer') for i in mission['roles'][role]}:
            errors.append('owner approval by author')
    return errors
