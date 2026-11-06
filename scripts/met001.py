"""MET-001: aggregate Codex response-usage records; never export message bodies."""
import argparse
import collections
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import re

FIELDS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens')


def time_of(value):
    result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamp needs timezone')
    return result.astimezone(dt.timezone.utc)


def extract(directory, session_id, cutoff, phases=None, prices=None):
    end = time_of(cutoff)
    starts = sorted((time_of(p['start']), p['name']) for p in (phases or []))
    counters = collections.Counter()
    totals = collections.Counter()
    groups = {key: collections.defaultdict(collections.Counter) for key in ('thread', 'model', 'phase')}
    seen = {}
    provenance = []
    cumulative = 0
    files = 0
    priced = Decimal(0)
    priced_count = 0
    identities = {}
    for file in sorted(Path(directory).rglob('*.jsonl')):
        try:
            with file.open(encoding='utf-8') as stream:
                first = json.loads(next(stream))
                if not isinstance(first, dict):
                    counters['file_read_errors'] += 1
                    continue
                meta = first.get('payload', {}) if first.get('type') == 'session_meta' else {}
                if not isinstance(meta, dict):
                    counters['file_read_errors'] += 1
                    continue
                source = meta.get('source')
                subagent = source.get('subagent', {}) if isinstance(source, dict) else {}
                spawn = subagent.get('thread_spawn', {}) if isinstance(subagent, dict) else {}
                if not isinstance(spawn, dict):
                    spawn = {}
                def safe_id(value):
                    return value if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_./-]{1,160}', value) else None
                identity = {'agent_path': safe_id(spawn.get('agent_path')), 'parent_thread_id': safe_id(spawn.get('parent_thread_id')), 'evidence': 'session_meta.payload.source.subagent.thread_spawn' if spawn else 'unknown'}
                contexts = {}
                files += 1
                for lineno, line in enumerate(stream, 2):
                    try:
                        event = json.loads(line)
                        if not isinstance(event, dict):
                            counters['invalid_event'] += 1
                            continue
                        if event.get('timestamp') and time_of(event['timestamp']) >= end:
                            continue
                        payload = event.get('payload') or {}
                        if not isinstance(payload, dict):
                            counters['invalid_event'] += 1
                            continue
                        if event.get('type') == 'turn_context':
                            contexts[payload.get('turn_id')] = payload.get('model')
                        if event.get('type') == 'event_msg' and payload.get('type') == 'token_count' and meta.get('id') == session_id:
                            try:
                                if time_of(event['timestamp']) < end:
                                    cumulative += 1
                            except (KeyError, ValueError, TypeError):
                                counters['invalid_event'] += 1
                        if event.get('type') != 'token_usage_record':
                            continue
                        stamp = time_of(event['timestamp'])
                        if stamp >= end:
                            continue
                        if payload.get('session_id') != session_id:
                            if not payload.get('session_id') and (meta.get('id') == session_id or payload.get('thread_id') == session_id):
                                counters['unattributable'] += 1
                            continue
                        usage = payload.get('usage')
                        rid, thread = payload.get('response_id'), payload.get('thread_id')
                        if not rid or not thread or not isinstance(usage, dict) or any(type(usage.get(k)) is not int for k in FIELDS):
                            counters['incomplete'] += 1
                            continue
                        values = {k: usage[k] for k in FIELDS}
                        if (any(v < 0 for v in values.values()) or values['input_tokens'] + values['output_tokens'] != values['total_tokens'] or values['cached_input_tokens'] + values['cache_write_input_tokens'] > values['input_tokens'] or values['reasoning_output_tokens'] > values['output_tokens']):
                            counters['invalid_usage'] += 1
                            continue
                        if rid in seen:
                            counters['duplicate_response_id'] += 1
                            if seen[rid] != (thread, values):
                                counters['duplicate_conflicts'] += 1
                            continue
                        seen[rid] = (thread, values)
                        if meta.get('id') != thread:
                            counters['thread_meta_mismatch'] += 1
                        else:
                            identities[thread] = identity
                        model = contexts.get(payload.get('turn_id')) or 'unknown'
                        phase = next((name for start, name in reversed(starts) if stamp >= start), 'unknown')
                        totals.update(values)
                        totals['responses'] += 1
                        for dimension, name in [('thread', thread), ('model', model), ('phase', phase)]:
                            groups[dimension][name].update(values)
                            groups[dimension][name]['responses'] += 1
                        provenance.append({'file': str(file.relative_to(directory)).replace('\\', '/'), 'line': lineno, 'timestamp': event['timestamp'], 'field': 'payload.usage', 'thread_id': thread, 'response_id': rid})
                        rate = (prices or {}).get('models', {}).get(model)
                        if rate and all(k in rate for k in ('input', 'cached_input', 'cache_write_input', 'output')):
                            # Prices are explicitly configured per million, never inferred billing.
                            units = (Decimal(values['input_tokens'] - values['cached_input_tokens'] - values['cache_write_input_tokens']) * Decimal(str(rate['input'])) + Decimal(values['cached_input_tokens']) * Decimal(str(rate['cached_input'])) + Decimal(values['cache_write_input_tokens']) * Decimal(str(rate['cache_write_input'])) + Decimal(values['output_tokens']) * Decimal(str(rate['output'])))
                            priced += units / 1000000
                            priced_count += 1
                    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                        counters['invalid_event'] += 1
        except (OSError, StopIteration, json.JSONDecodeError):
            counters['file_read_errors'] += 1
    partial = not seen or any(counters[k] for k in ('incomplete', 'duplicate_conflicts', 'invalid_usage', 'thread_meta_mismatch', 'unattributable', 'invalid_event', 'file_read_errors'))
    result = {'schema': 'met-001/v1', 'root_session_id': session_id, 'cutoff_exclusive_utc': end.isoformat(), 'measurement_status': 'partial' if partial else 'observed_records_only', 'limitations': ['Only observed response records; completeness of source logs is not established.', 'Cumulative token_count events are excluded because they may include inherited counters.', 'Reasoning tokens are included in output; cached tokens are included in input.', 'Model is declared by turn_context, not verified billing identity.', 'Phase attribution uses supplied time windows; agent role is not inferred.'], 'files_scanned': files, 'ignored_cumulative_events': cumulative, 'anomalies': dict(sorted(counters.items())), 'totals': dict(sorted(totals.items())), 'provenance': provenance, 'actual_cost': None, 'hypothetical_cost': None}
    for dimension, entries in groups.items():
        result['by_' + dimension] = {key: dict(sorted(value.items())) for key, value in sorted(entries.items())}
    result['thread_identities'] = dict(sorted(identities.items()))
    result['phase_windows'] = [{'name': name, 'start_utc': start.isoformat(), 'end_utc': min(starts[i+1][0], end).isoformat() if i+1 < len(starts) else end.isoformat(), 'duration_seconds': max(0, (min(starts[i+1][0], end) - start).total_seconds()) if i+1 < len(starts) else max(0, (end - start).total_seconds()), 'basis': 'configured time boundaries; elapsed, not active work time'} for i, (start, name) in enumerate(starts) if start < end]
    result['review_cycles'] = {'value': None, 'status': 'unknown', 'reason': 'No standardized review-cycle events are available.'}
    if prices:
        result['hypothetical_cost'] = {'amount': str(priced), 'currency': prices['currency'], 'effective_date': prices['effective_date'], 'source': prices['source'], 'priced_responses': priced_count, 'total_responses': len(seen), 'status': 'complete_for_configured_flat_rates' if priced_count == len(seen) else 'partial', 'note': 'Hypothetical configured flat API rates; not an invoice.'}
    return result


def markdown(result):
    t = result['totals']
    lines = ['# MET-001', '', f"Estado: {result['measurement_status']}", f"Corte exclusivo UTC: {result['cutoff_exclusive_utc']}", f"Respuestas: {t.get('responses', 0)}", f"Entrada: {t.get('input_tokens', 0)}; caché incluida: {t.get('cached_input_tokens', 0)}; salida: {t.get('output_tokens', 0)}; total: {t.get('total_tokens', 0)}.", '', 'Coste real: no disponible sin evidencia de facturación.', '', 'Limitaciones:']
    lines += ['- ' + item for item in result['limitations']]
    if result['hypothetical_cost']:
        lines += ['', 'Coste hipotético: ' + json.dumps(result['hypothetical_cost'], ensure_ascii=False, sort_keys=True)]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sessions', type=Path, required=True)
    parser.add_argument('--session-id', required=True)
    parser.add_argument('--cutoff', required=True, help='exclusive ISO-8601 with timezone')
    parser.add_argument('--output', type=Path, required=True, help='output filename prefix')
    parser.add_argument('--phases', type=Path, help='JSON array of {name,start}; explicitly supplied timestamps')
    parser.add_argument('--prices', type=Path, help='JSON dated flat rates by model')
    args = parser.parse_args()
    phases = json.loads(args.phases.read_text(encoding='utf-8')) if args.phases else None
    prices = json.loads(args.prices.read_text(encoding='utf-8')) if args.prices else None
    result = extract(args.sessions, args.session_id, args.cutoff, phases, prices)
    args.output.with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    args.output.with_suffix('.md').write_text(markdown(result), encoding='utf-8')


if __name__ == '__main__':
    main()
