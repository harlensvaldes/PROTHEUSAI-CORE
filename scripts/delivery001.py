"""Prepare and verify explicitly selected, reviewable delivery directories."""
import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath

RESERVED = {'MANIFEST.json', 'INSTALL.md', 'DELIVERY_REPORT.md'}
FORBIDDEN = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'backup', 'backups', 'log', 'logs'}
SECRET = re.compile(rb'(?i)(?:api[_-]?key|password|secret|token)\s*[=:]\s*["\']?[a-z0-9_\-]{20,}')
FIELDS = ('prerequisites', 'install_steps', 'start_steps', 'configuration', 'verification_steps', 'evidence', 'limitations')


def relative_path(value):
    if not isinstance(value, str) or not value or '\\' in value or PureWindowsPath(value).drive:
        raise ValueError('invalid relative path')
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('invalid relative path')
    parts = [p.lower() for p in path.parts]
    if any(p in FORBIDDEN or p == '.env' or p.startswith('.env.') or p in {'credentials.json', 'credentials', 'secrets.json', 'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519'} or p.endswith(('.log', '.pem', '.key', '.pyc', '.sqlite', '.sqlite3', '.db', '.db3', '.tmp', '.bak')) for p in parts):
        raise ValueError('excluded path')
    return path


def regular_under(root, relative):
    current = root
    for part in relative.parts:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('link or reparse point')
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError('not a regular file')
    return current


def checked_root(value):
    path = Path(os.path.abspath(value))
    for part in reversed((path, *path.parents)):
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('linked root')
    if not path.is_dir():
        raise ValueError('root is not a directory')
    return path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_review(entry, data):
    keys = {'source', 'destination', 'sha256', 'provenance', 'justification', 'reviewer', 'review', 'review_date', 'findings'}
    if not isinstance(entry, dict) or set(entry) != keys:
        raise ValueError('missing per-file review')
    if any(not isinstance(entry[k], str) or not entry[k].strip() for k in ('provenance', 'justification', 'reviewer', 'review_date')):
        raise ValueError('incomplete per-file review')
    if any(entry[k].strip().lower() in {'unknown', 'unknown source', 'desconocido', 'desconocida', 'n/a'} for k in ('provenance', 'justification', 'reviewer')):
        raise ValueError('unknown provenance or review')
    try:
        datetime.date.fromisoformat(entry['review_date'])
    except ValueError:
        raise ValueError('invalid review date') from None
    if entry['review'] != 'approved' or entry['findings'] != [] or entry['sha256'] != digest(data):
        raise ValueError('unresolved finding or changed file')


def scan_content(data, known_roots):
    if SECRET.search(data) or b'-----BEGIN ' in data and b'PRIVATE KEY-----' in data or data.startswith(b'SQLite format 3\x00'):
        raise ValueError('sensitive content detected')
    for root in known_roots:
        for encoding in ('utf-8', 'utf-16-le'):
            if root.encode(encoding).lower() in data.lower():
                raise ValueError('workshop path detected')
    try:
        decoded = json.loads(data)
    except (ValueError, UnicodeError):
        return
    scan_json_strings(decoded, known_roots)


def scan_json_strings(value, known_roots):
    if isinstance(value, str):
        raw = value.encode('utf-8')
        if SECRET.search(raw) or any(root.casefold() in value.casefold() for root in known_roots):
            raise ValueError('sensitive metadata')
    elif isinstance(value, dict):
        for key, item in value.items():
            scan_json_strings(key, known_roots)
            scan_json_strings(item, known_roots)
    elif isinstance(value, list):
        for item in value:
            scan_json_strings(item, known_roots)


def validate_descriptor(d):
    expected = {'schema', 'product', 'version', 'mission', 'approval', 'files', 'known_roots', *FIELDS}
    if not isinstance(d, dict) or set(d) != expected or d['schema'] != 'delivery-001/v1':
        raise ValueError('invalid descriptor fields')
    for field in ('product', 'version', 'mission', 'approval'):
        if not isinstance(d[field], str) or not d[field].strip() or '\n' in d[field]:
            raise ValueError('invalid identity')
    for field in FIELDS:
        if not isinstance(d[field], list) or not d[field] or any(not isinstance(x, str) or not x.strip() for x in d[field]):
            raise ValueError('invalid instructions')
    if not isinstance(d['files'], list) or not d['files']:
        raise ValueError('empty file selection')
    if not isinstance(d['known_roots'], list) or not d['known_roots'] or any(not isinstance(x, str) or len(x.strip()) < 4 for x in d['known_roots']):
        raise ValueError('known roots required')


def prepare(descriptor, source, output):
    d = json.loads(Path(descriptor).read_text(encoding='utf-8'))
    validate_descriptor(d)
    source = checked_root(source)
    output = Path(output).absolute()
    checked_root(output.parent)
    if not source.is_dir() or output.exists() or output.is_symlink() or output.resolve().is_relative_to(source):
        raise ValueError('invalid source or output')
    seen = {name.casefold() for name in RESERVED}
    selected = []
    for item in d['files']:
        if not isinstance(item, dict) or not {'source', 'destination'} <= set(item):
            raise ValueError('invalid selection')
        src, dst = relative_path(item['source']), relative_path(item['destination'])
        key = str(dst).casefold()
        if key in seen or any(key.startswith(x + '/') or x.startswith(key + '/') for x in seen):
            raise ValueError('destination collision')
        seen.add(key)
        selected.append((src, dst, item))
    public_descriptor = {k: v for k, v in d.items() if k != 'known_roots'}
    scan_json_strings(public_descriptor, d['known_roots'] + [str(source)])
    stage = Path(tempfile.mkdtemp(prefix='.delivery001-', dir=output.parent))
    reviews = {}
    for src, dst, item in selected:
        path = regular_under(source, src)
        before = path.stat()
        data = path.read_bytes()
        after = path.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError('source changed')
        check_review(item, data)
        scan_content(data, d['known_roots'] + [str(source)])
        target = stage.joinpath(*dst.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        reviews[str(dst)] = {k: item[k] for k in ('provenance', 'justification', 'reviewer', 'review', 'review_date')}
    titles = {'prerequisites': 'Prerequisites', 'install_steps': 'Installation', 'start_steps': 'Start', 'configuration': 'Configuration', 'verification_steps': 'Verification'}
    instructions = [f"# {d['product']} — {d['version']}", '']
    for field, title in titles.items():
        instructions += [f'## {title}', ''] + [f'- {line}' for line in d[field]] + ['']
    (stage / 'INSTALL.md').write_text('\n'.join(instructions), encoding='utf-8')
    report = [f"# Delivery report: {d['product']}", '', f"Version: {d['version']}", f"Mission: {d['mission']}", f"Approval reference: {d['approval']}", '', '## Evidence', ''] + [f'- {x}' for x in d['evidence']] + ['', '## Limitations', ''] + [f'- {x}' for x in d['limitations']] + ['', 'Hashes provide integrity, not authenticity. Secret scanning is incomplete.', '']
    (stage / 'DELIVERY_REPORT.md').write_text('\n'.join(report), encoding='utf-8')
    entries = []
    for path in sorted(stage.rglob('*')):
        if path.is_file():
            data = path.read_bytes()
            scan_content(data, d['known_roots'] + [str(source)])
            name = path.relative_to(stage).as_posix()
            entries.append({'path': name, 'size': len(data), 'sha256': digest(data), 'checks': {'name': 'passed', 'content': 'passed', 'secret_patterns': 'passed', 'workshop_roots': 'passed'}, 'review': reviews.get(name, {'origin': 'generated', 'human_review': 'not_asserted'})})
    manifest = {'schema': 'delivery-manifest/v1', 'excludes': ['MANIFEST.json'], 'files': entries}
    (stage / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    verify(stage)
    os.rename(stage, output)


def verify(directory):
    root = checked_root(directory)
    manifest_path = regular_under(root, PurePosixPath('MANIFEST.json'))
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if set(manifest) != {'schema', 'excludes', 'files'} or manifest['schema'] != 'delivery-manifest/v1' or manifest['excludes'] != ['MANIFEST.json'] or not isinstance(manifest['files'], list):
        raise ValueError('invalid manifest')
    expected = set()
    for entry in manifest['files']:
        if not isinstance(entry, dict) or set(entry) != {'path', 'size', 'sha256', 'checks', 'review'} or not isinstance(entry['checks'], dict) or not isinstance(entry['review'], dict):
            raise ValueError('invalid manifest entry')
        rel = relative_path(entry['path'])
        if str(rel).casefold() in expected or str(rel) == 'MANIFEST.json':
            raise ValueError('duplicate manifest entry')
        expected.add(str(rel).casefold())
        data = regular_under(root, rel).read_bytes()
        if len(data) != entry['size'] or digest(data) != entry['sha256']:
            raise ValueError('integrity mismatch')
    actual = set()
    for path in root.rglob('*'):
        if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & 0x400:
            raise ValueError('link in delivery')
        if path.is_file() and path.relative_to(root).as_posix() != 'MANIFEST.json':
            key = path.relative_to(root).as_posix().casefold()
            if key in actual:
                raise ValueError('case collision in delivery')
            actual.add(key)
    if actual != expected:
        raise ValueError('unexpected or missing files')


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--descriptor', required=True)
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    v = sub.add_parser('verify')
    v.add_argument('--directory', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            prepare(args.descriptor, args.source, args.output)
        else:
            verify(args.directory)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f'Delivery error: {type(exc).__name__}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
