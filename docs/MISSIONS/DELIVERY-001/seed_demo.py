"""Create the fictional APP-004 demonstration database once, without an API key."""
import json
from pathlib import Path
from app.store import Store


def main():
    directory = Path('var')
    database = directory / 'camisas.sqlite'
    if database.exists():
        raise SystemExit('Database already exists; refusing to overwrite it.')
    directory.mkdir(exist_ok=True)
    photos = []
    for meta_path in sorted((directory / 'images').glob('*.json')):
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        photos.append({'id': meta_path.stem, 'pexels_id': meta['pexels_id']})
    store = Store(database)
    store.initialize()
    if store.complete_collection(photos, directory) != 3 or store.collection_status(directory)[0] != 3:
        raise SystemExit('Could not establish the three-image fictional catalogue.')
    if store.orders():
        raise SystemExit('New database unexpectedly contains orders.')
    print('Created a fictional catalogue with three credited images.')


if __name__ == '__main__':
    main()
