"""Run inside a separately constructed chroot; never reaches the workshop."""
import json
import hashlib
import os
import sqlite3
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def start():
    return subprocess.Popen([sys.executable, '-m', 'app.server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def fetch(path):
    for _ in range(50):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000' + path, timeout=1) as response:
                return response.status, response.read()
        except OSError:
            time.sleep(.1)
    raise RuntimeError('server unavailable')


def post(path, data):
    request = urllib.request.Request('http://127.0.0.1:8000' + path, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json', 'X-Local-Test': '1'})
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read())['result']


def main():
    manifest = json.loads(Path('MANIFEST.json').read_text(encoding='utf-8'))
    expected = {entry['path'] for entry in manifest['files']}
    actual = {p.as_posix() for p in Path('.').rglob('*') if p.is_file()} - {'MANIFEST.json', 'smoke.py'}
    assert actual == expected
    for entry in manifest['files']:
        contents = Path(entry['path']).read_bytes()
        assert len(contents) == entry['size'] and hashlib.sha256(contents).hexdigest() == entry['sha256']
    print('Delivery manifest integrity before installation: OK')
    print('Original Windows mounts absent:', not Path('/mnt/c').exists())
    print('Workspace mount absent:', not Path('/workshop').exists())
    if Path('/mnt/c').exists() or Path('/workshop').exists():
        raise RuntimeError('workshop path remains visible')
    print('Python:', sys.version.split()[0])
    assert 'PEXELS_API_KEY' not in os.environ
    print('API key absent:', True)
    subprocess.run([sys.executable, 'seed_demo.py'], check=True)
    with sqlite3.connect('var/camisas.sqlite') as db:
        integrity = db.execute('pragma integrity_check').fetchone()[0]
        orders = db.execute('select count(*) from orders').fetchone()[0]
        reservations = db.execute('select count(*) from reservations').fetchone()[0]
        assert integrity == 'ok' and orders == reservations == 0
        print('SQLite integrity:', integrity)
        print('Orders/reservations:', orders, reservations)
    server = start()
    try:
        status, body = fetch('/api/products')
        products = json.loads(body)['products']
        print('Catalogue:', status, len(products))
        assert len(products) == 3
        for product in products:
            assert product.get('photo_credit')
            image_status, image = fetch('/api/images/' + product['image'])
            assert image_status == 200 and image.startswith(b'\xff\xd8\xff')
        print('Three credited JPEG resources: OK')
        reservation = post('/api/reservations', {'items': [{'variant_id': products[0]['variants'][0]['id'], 'quantity': 1}]})
        order = post('/api/reservations/' + reservation['id'] + '/confirm', {'name': 'Demo', 'address': '1 Rue fictive', 'email': 'demo@example.invalid'})
        order_id = order['id']
        print('Fictional reservation and confirmation: OK')
    finally:
        server.terminate()
        server.wait(timeout=10)
    server = start()
    try:
        _, body = fetch('/api/products')
        assert len(json.loads(body)['products']) == 3
        _, body = fetch('/api/admin/orders')
        assert any(item['id'] == order_id for item in json.loads(body)['orders'])
        print('Catalogue and fictional order persisted across restart: OK')
    finally:
        server.terminate()
        server.wait(timeout=10)


if __name__ == '__main__':
    main()
