"""Prepare the APP-004 demonstration source from a fixed commit and selected assets."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

COMMIT = '0cf56f78c090783f24e93aaedbc2b523d37ba82b'
IMAGES = ('4d7aba565d1e4363b8a05ebdd4a6b649', '8ca6676b9d6549979093f0ba8da2e736', 'e2ffc234dd894309b2a839e2615456a9')
CORE = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', required=True)
    parser.add_argument('--workspace', required=True, help='New directory for intermediate source and delivery')
    args = parser.parse_args()
    app = Path(args.app).resolve(strict=True)
    work = Path(args.workspace).absolute()
    work.mkdir(parents=True, exist_ok=False)
    source = work / 'source'
    source.mkdir()
    git = ['git', '-c', f'safe.directory={app.as_posix()}', '-C', str(app)]
    paths = subprocess.check_output(git + ['ls-tree', '-r', '--name-only', COMMIT, '--', 'app'], text=True).splitlines()
    for name in paths:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(git + ['show', f'{COMMIT}:{name}']))
    for ident in IMAGES:
        for suffix in ('.jpg', '.json'):
            name = f'var/images/{ident}{suffix}'
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(app / name, target)
    shutil.copyfile(CORE / 'docs/MISSIONS/DELIVERY-001/seed_demo.py', source / 'seed_demo.py')
    (source / 'config.example.txt').write_text('No API key is required for the included demonstration.\n', encoding='utf-8')
    (source / 'IMAGE_SOURCES.md').write_bytes(subprocess.check_output(git + ['show', f'{COMMIT}:docs/IMAGE_SOURCES.md']))
    files = sorted(p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file())
    review_path = CORE / 'docs/MISSIONS/DELIVERY-001/APP004-REVISION.json'
    reviewed = json.loads(review_path.read_text(encoding='utf-8'))
    if sorted(item['source'] for item in reviewed) != files or any(item['source'] != item['destination'] for item in reviewed):
        raise SystemExit('The source does not match the independently reviewed allowlist.')
    descriptor = {
        'schema': 'delivery-001/v1', 'product': 'CAMISAS CHATGPT', 'version': COMMIT,
        'mission': 'APP-004 / CAMISAS-004', 'approval': 'Owner functional acceptance recorded in CAMISAS-004/06-DECISION.md',
        'files': reviewed,
        'known_roots': [str(app), app.as_posix(), str(CORE), CORE.as_posix()],
        'prerequisites': ['Python 3.12 and its standard library; no additional packages.'],
        'configuration': ['No API key is needed for the included catalogue; payment, email and admin access are simulated.'],
        'install_steps': ['From the delivery root, run: python seed_demo.py', 'Run the seed only once; it refuses to overwrite an existing database.'],
        'start_steps': ['From the delivery root, run: python -m app.server', 'Open http://127.0.0.1:8000/ in a browser.'],
        'verification_steps': ['Check that the catalogue contains three fictional products and credited photos.'],
        'evidence': ['Code selected directly from approved commit; images and associated credits supplied separately.', 'See IMAGE_SOURCES.md for photographic provenance.', 'A prior package with manifest SHA-256 1c2404ce4d5fa5b6b08bbd7debe28eae7d8dd84e0f04ad6e61321490af571f2b passed an isolated Python 3.12.3 API and persistence smoke; this evidence does not authenticate or automatically cover this package.', 'DELIVERY-001 MET-001 observed at 2026-11-06T14:43:57Z: 179 responses, 16967848 input tokens including 16630272 cached, 51868 output tokens; actual cost unknown.'],
        'limitations': ['Local fictional pilot; do not use real customer data or publish.', 'E2E NOT RUN; Pexels usage is subject to its current terms.', 'Independent clean-environment execution of this exact package must be separately recorded.', 'MET-001 includes observed records only; completeness and billing are not established.'],
    }
    descriptor_path = work / 'descriptor.json'
    descriptor_path.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2), encoding='utf-8')
    subprocess.run([sys.executable, str(CORE / 'scripts/delivery001.py'), 'prepare', '--descriptor', str(descriptor_path), '--source', str(source), '--output', str(work / 'delivery')], check=True)
    print(f'Delivery prepared: {work / "delivery"}')


if __name__ == '__main__':
    main()
