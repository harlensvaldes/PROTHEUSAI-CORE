"""Analiza referencias MET-001 existentes sin exportar mensajes del runner."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SESSIONS = Path.home() / '.codex' / 'sessions'


def events(name):
    data = json.loads((ROOT / 'docs/MISSIONS/CONTEXT-001' / name).read_text(encoding='utf-8'))
    files = {}
    rows = []
    for ref in data['provenance']:
        path = SESSIONS / ref['file']
        if path not in files:
            files[path] = path.read_text(encoding='utf-8').splitlines()
        event = json.loads(files[path][ref['line'] - 1])
        payload = event['payload']
        if (event['timestamp'] != ref['timestamp'] or payload['response_id'] != ref['response_id']
                or payload['thread_id'] != ref['thread_id']):
            raise ValueError('La procedencia no coincide con el evento')
        rows.append({**ref, **payload['usage']})
    rows.sort(key=lambda x: (x['timestamp'], x['file'], x['line']))
    return data, rows, files


def main():
    data, rows, files = events('05-MET-CORTE-2.json')
    main_rows = [r for r in rows if r['thread_id'] == data['root_session_id']]
    if len(main_rows) != 24:
        raise ValueError(f"Esperadas 24 respuestas raíz, hay {len(main_rows)}")
    columns = ['index', 'timestamp', 'response_id', 'file', 'line', 'input_tokens',
               'cached_input_tokens', 'uncached_input_tokens', 'output_tokens', 'input_delta']
    series = []
    for i, r in enumerate(main_rows):
        series.append({'index': i + 1, **{k: r[k] for k in columns if k in r},
                       'uncached_input_tokens': r['input_tokens'] - r['cached_input_tokens'],
                       'input_delta': r['input_tokens'] - main_rows[i-1]['input_tokens'] if i else None})
    with (OUT / '05-CONTEXT-SERIE.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(series)
    n = len(series)
    xm = (n + 1) / 2
    ym = sum(r['input_tokens'] for r in series) / n
    slope = sum((r['index'] - xm) * (r['input_tokens'] - ym) for r in series) / sum((r['index'] - xm)**2 for r in series)
    intercept = ym - slope * xm
    residuals = [r['input_tokens'] - (intercept + slope * r['index']) for r in series]
    total_ss = sum((r['input_tokens'] - ym)**2 for r in series)
    delta = [r for r in series if r['input_delta'] is not None]
    observed = Counter()
    root_files = {r['file'] for r in main_rows}
    for file in root_files:
        last_line = max(r['line'] for r in main_rows if r['file'] == file)
        for text in files[SESSIONS / file][:last_line]:
            event = json.loads(text)
            payload = event.get('payload') or {}
            typ = str(event.get('type', ''))
            subtype = str(payload.get('type', '')) if isinstance(payload, dict) else ''
            if 'compact' in typ.lower() or 'compact' in subtype.lower():
                observed[f'{typ}/{subtype}'] += 1
    result = {'responses': n, 'first_input': series[0]['input_tokens'], 'last_input': series[-1]['input_tokens'],
              'input_sum': sum(r['input_tokens'] for r in series), 'cache_sum': sum(r['cached_input_tokens'] for r in series),
              'input_min': min(r['input_tokens'] for r in series), 'input_max': max(r['input_tokens'] for r in series),
              'ols_slope_per_response': slope, 'ols_intercept_index_zero': intercept,
              'ols_r2': 1 - sum(x*x for x in residuals)/total_ss if total_ss else None,
              'positive_increments': sum(r['input_delta'] > 0 for r in delta),
              'negative_increments': sum(r['input_delta'] < 0 for r in delta),
              'zero_increments': sum(r['input_delta'] == 0 for r in delta),
              'largest_increase': max(delta, key=lambda r:r['input_delta']),
              'smallest_increment': min(delta, key=lambda r:r['input_delta']),
              'compact_named_events_to_last_usage': dict(observed),
              'limitations': 'Only observed MET references; named-event scan cannot establish absence of compaction.'}
    ab, all_rows, _ = events('05-MET-AB.json')
    starts = {}
    for r in all_rows:
        thread = r['thread_id']
        if thread not in starts:
            starts[thread] = {'thread_id': thread, 'identity': ab.get('thread_identities', {}).get(thread),
                              'timestamp': r['timestamp'], 'file': r['file'], 'line': r['line'],
                              'input_tokens': r['input_tokens'], 'cached_input_tokens': r['cached_input_tokens'],
                              'output_tokens': r['output_tokens']}
    result['first_observed_by_thread'] = list(starts.values())
    (OUT / '05-CONTEXT-RESULTADOS.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    # SVG is drawn in-process to avoid extra dependencies and includes only measured values.
    width, height, left, top, plot_w, plot_h = 850, 390, 75, 35, 735, 295
    scale = 100000
    def point(i, value):
        return f'{left+(i-1)*plot_w/(n-1):.1f},{top+plot_h*(1-value/scale):.1f}'
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<text x="75" y="23" font-family="sans-serif" font-size="16">CONTEXT-001 · Entrada por respuesta del hilo raíz</text>']
    for y in range(0, scale+1, 20000):
        yy=top+plot_h*(1-y/scale)
        svg += [f'<line x1="{left}" x2="{left+plot_w}" y1="{yy}" y2="{yy}" stroke="#dddddd"/>',
                f'<text x="8" y="{yy+4}" font-size="11" font-family="sans-serif">{y:,}</text>']
    for field, color in [('input_tokens','#145db2'), ('cached_input_tokens','#d1661e')]:
        pts=' '.join(point(r['index'],r[field]) for r in series)
        svg.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>')
    svg += ['<text x="75" y="370" font-family="sans-serif" font-size="12">Azul: entrada total · Naranja: caché incluida · Eje X: índice de respuesta (1–24)</text>', '</svg>']
    (OUT/'05-CONTEXT-GRAFICA.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
