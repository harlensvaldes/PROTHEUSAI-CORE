"""Evidence: injected write failure must not publish a delivery or alter source."""
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import delivery001

root = Path(tempfile.mkdtemp(prefix='delivery001-copy-failure-'))
source = root / 'source'
source.mkdir()
original = b'fictional input'
(source / 'data.txt').write_bytes(original)
item = {'source': 'data.txt', 'destination': 'data.txt', 'sha256': hashlib.sha256(original).hexdigest(), 'provenance': 'synthetic fixture', 'justification': 'negative test', 'reviewer': 'test fixture', 'review': 'approved', 'review_date': '2026-11-06', 'findings': []}
descriptor = {'schema': 'delivery-001/v1', 'product': 'fixture', 'version': '1', 'mission': 'test', 'approval': 'fixture', 'known_roots': ['/fictional-workshop'], 'files': [item], **{key: ['fixture'] for key in delivery001.FIELDS}}
desc = root / 'descriptor.json'
desc.write_text(json.dumps(descriptor), encoding='utf-8')
with patch.object(Path, 'write_bytes', side_effect=OSError('synthetic failure')):
    try:
        delivery001.prepare(desc, source, root / 'delivery')
    except OSError:
        pass
    else:
        raise AssertionError('failure was not propagated')
assert not (root / 'delivery').exists()
assert (source / 'data.txt').read_bytes() == original
assert list(root.glob('.delivery001-*'))
print('Injected copy failure propagated; no final delivery; source unchanged; stage retained.')
