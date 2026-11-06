#!/usr/bin/env python3
"""Create an independent project from an explicit committed CORE allowlist."""
import argparse
import hashlib
import json
import ntpath
import os
import re
import stat
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'bootstrap/allowlist.json'


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT='0', GIT_OPTIONAL_LOCKS='0')
    return env


def git(cwd, *args):
    result = subprocess.run(['git', *args], cwd=cwd, env=git_env(),
                            capture_output=True, text=True)
    if result.returncode:
        raise ValueError('Git failed: ' + (result.stderr.strip() or 'operation failed'))
    return result.stdout.strip()


def committed_bytes(revision, name):
    result = subprocess.run(['git', 'cat-file', 'blob', revision + ':' + name], cwd=ROOT,
                            env=git_env(), capture_output=True)
    if result.returncode:
        raise ValueError('source not present in commit: ' + name)
    return result.stdout


def relative_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('invalid manifest path')
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value or any(x in ('', '.', '..') for x in path.parts):
        raise ValueError('invalid manifest path')
    if any(x.lower() == '.git' for x in path.parts):
        raise ValueError('Git metadata forbidden')
    return path


def no_links(path):
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if not current.exists() and not current.is_symlink():
            continue
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('symlink or reparse point forbidden: ' + str(current))


def source_files():
    head = git(ROOT, 'rev-parse', '--verify', 'HEAD')
    raw = committed_bytes(head, MANIFEST)
    no_links(ROOT / MANIFEST)
    working_manifest = (ROOT / MANIFEST).read_bytes()
    if working_manifest != raw and working_manifest.replace(b'\r\n', b'\n') != raw:
        raise ValueError('source differs from committed bytes: ' + MANIFEST)
    data = json.loads(raw.decode('utf-8'))
    if set(data) != {'schema', 'files'} or data['schema'] != 1 or not isinstance(data['files'], list) or not data['files']:
        raise ValueError('invalid allowlist')
    entries, sources, destinations = [], set(), set()
    for item in data['files']:
        if not isinstance(item, dict) or set(item) != {'source', 'destination', 'reason'} or not isinstance(item['reason'], str) or not item['reason'].strip():
            raise ValueError('invalid allowlist entry')
        source, dest = str(relative_path(item['source'])), str(relative_path(item['destination']))
        if source.casefold() in sources or dest.casefold() in destinations:
            raise ValueError('duplicate allowlist path')
        if dest.casefold() in {'readme.md', 'bootstrap-provenance.json'}:
            raise ValueError('generated path collision')
        sources.add(source.casefold()); destinations.add(dest.casefold())
        path = ROOT.joinpath(*PurePosixPath(source).parts)
        no_links(path)
        if not path.is_file():
            raise ValueError('missing source: ' + source)
        entries.append((source, dest, None))
    paths = [MANIFEST, 'scripts/bootstrap001.py'] + [item[0] for item in entries]
    blobs = {}
    for name in paths:
        path = ROOT.joinpath(*PurePosixPath(name).parts)
        no_links(path)
        working = path.read_bytes()
        blob = committed_bytes(head, name)
        if working != blob and working.replace(b'\r\n', b'\n') != blob:
            raise ValueError('source differs from committed bytes: ' + name)
        blobs[name] = blob
    return head, blobs[MANIFEST], [(s, d, blobs[s]) for s, d, _ in entries]


def create(name, project_id, destination):
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 120 or name != name.strip() or any(unicodedata.category(c).startswith('C') or c in '\u2028\u2029' for c in name):
        raise ValueError('invalid project name')
    if not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?', project_id):
        raise ValueError('invalid project id')
    drive, tail = ntpath.splitdrive(str(destination))
    if (drive and not tail.startswith(('\\', '/'))) or any(part in ('.', '..') for part in re.split(r'[\\/]', str(destination))):
        raise ValueError('ambiguous destination')
    target = Path(os.path.abspath(destination))
    no_links(target)
    if target.exists() or target.is_symlink() or not target.parent.is_dir():
        raise ValueError('destination exists or parent is missing')
    source = ROOT.resolve()
    if target == source or target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError('destination overlaps CORE')
    for parent in (target.parent, *target.parent.parents):
        if (parent / '.git').exists() or (parent / '.git').is_symlink():
            raise ValueError('destination inside existing Git repository')
    head, raw, entries = source_files()
    target.mkdir(exist_ok=False)
    try:
        for source_name, dest_name, content in entries:
            path = target.joinpath(*PurePosixPath(dest_name).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as out:
                out.write(content)
        readme = (f'# {name}\n\nPropósito, alcance y funcionalidades: pendientes de Discovery.\n\n'
                  '## Instalación, configuración y dependencias\n\nPendiente de definir.\n\n'
                  '## Ejecución y pruebas\n\nPendientes de definir y ejecutar.\n\n'
                  '## Limitaciones\n\nProducto aún no definido. Inicio: `prompts/00_START_PROJECT.md`.\n')
        with (target / 'README.md').open('x', encoding='utf-8', newline='\n') as out:
            out.write(readme)
        provenance = {'project_id': project_id, 'core_commit': head,
                      'allowlist_sha256': hashlib.sha256(raw).hexdigest(),
                      'files': [{'source': s, 'destination': d, 'sha256': hashlib.sha256(b).hexdigest()} for s, d, b in entries]}
        with (target / 'bootstrap-provenance.json').open('x', encoding='utf-8', newline='\n') as out:
            out.write(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
        template = target / '.bootstrap-empty-template'
        template.mkdir()
        git(target, '-c', 'core.hooksPath=' + os.devnull, 'init', '--template=' + str(template), '.')
        template.rmdir()
        if Path(git(target, 'rev-parse', '--show-toplevel')).resolve() != target.resolve():
            raise ValueError('Git worktree mismatch')
        if Path(git(target, 'rev-parse', '--absolute-git-dir')).resolve() != (target / '.git').resolve():
            raise ValueError('Git directory mismatch')
        if git(target, 'remote') or (target / '.git/objects/info/alternates').exists():
            raise ValueError('Git repository is not independent')
        hooks = target / '.git/hooks'
        if hooks.exists() and any(hooks.iterdir()):
            raise ValueError('unexpected Git hooks')
    except Exception as exc:
        raise ValueError(f'partial destination retained: {target}: {exc}') from exc
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    try:
        print(create(args.name, args.id, args.destination))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
