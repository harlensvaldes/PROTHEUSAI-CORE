import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'delivery001.py'


def reviewed(source, destination, data):
    return {'source': source, 'destination': destination, 'sha256': hashlib.sha256(data).hexdigest(), 'provenance': 'approved revision', 'justification': 'runtime', 'reviewer': 'reviewer-1', 'review': 'approved', 'review_date': '2026-11-06', 'findings': []}


class DeliveryTests(unittest.TestCase):
    def test_review_requires_provenance_hash_and_resolved_findings(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        data = b'fictional content'
        entry = {'source': 'x.txt', 'destination': 'x.txt', 'sha256': hashlib.sha256(data).hexdigest(), 'provenance': 'approved revision', 'justification': 'runtime', 'reviewer': 'reviewer-1', 'review': 'approved', 'review_date': '2026-11-06', 'findings': []}
        delivery001.check_review(entry, data)
        for changes in ({'provenance': ''}, {'sha256': '0' * 64}, {'review': 'pending'}, {'findings': ['unresolved']}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                delivery001.check_review({**entry, **changes}, data)

    def test_paths_secrets_and_existing_output_are_rejected(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        for value in ('../secret', '/absolute', 'C:/absolute', '.git/config', 'a/private.pem', 'x.sqlite', 'a\\b', '.env.production', '.env.example', 'credentials.json', 'data/client.db3', 'data/client.sqlite3', 'log/session.txt', 'id_rsa'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                delivery001.relative_path(value)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'out').mkdir()
            (root / 'source').mkdir()
            descriptor = {'schema': 'delivery-001/v1', 'product': 'p', 'version': '1', 'mission': 'm', 'approval': 'owner', 'known_roots': ['/workshop/project'], 'files': [reviewed('x', 'x', b'x')], **{key: ['none'] for key in delivery001.FIELDS}}
            path = root / 'descriptor.json'
            path.write_text(json.dumps(descriptor))
            with self.assertRaises(ValueError):
                delivery001.prepare(path, root / 'source', root / 'out')

    def test_linked_root_is_rejected(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'real').mkdir()
            try:
                (root / 'link').symlink_to(root / 'real', target_is_directory=True)
            except OSError:
                self.skipTest('directory symlinks unavailable')
            with self.assertRaises(ValueError):
                delivery001.checked_root(root / 'link')

    def test_rejects_secrets_collisions_and_missing_inputs(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'one.txt').write_text('api_key=abcdefghijklmnopqrstuvwxyz123456')
            descriptor = {'schema': 'delivery-001/v1', 'product': 'p', 'version': '1', 'mission': 'm', 'approval': 'owner', 'known_roots': ['/workshop/project'], 'files': [reviewed('one.txt', 'one.txt', (source / 'one.txt').read_bytes())], **{key: ['none'] for key in delivery001.FIELDS}}
            path = root / 'descriptor.json'
            path.write_text(json.dumps(descriptor))
            with self.assertRaises(ValueError):
                delivery001.prepare(path, source, root / 'out1')
            descriptor['files'].append(reviewed('one.txt', 'ONE.txt', (source / 'one.txt').read_bytes()))
            path.write_text(json.dumps(descriptor))
            with self.assertRaises(ValueError):
                delivery001.prepare(path, source, root / 'out2')
            descriptor['files'] = [reviewed('missing', 'missing', b'')]
            path.write_text(json.dumps(descriptor))
            with self.assertRaises(FileNotFoundError):
                delivery001.prepare(path, source, root / 'out3')

    def test_content_scans_detect_database_secret_and_known_root(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        for data in (b'SQLite format 3\x00rest', b'api_key=abcdefghijklmnopqrstuvwxyz123456', b'/workshop/project/hidden'):
            with self.subTest(data=data[:12]), self.assertRaises(ValueError):
                delivery001.scan_content(data, ['/workshop/project'])

    def test_rejects_workshop_root_in_review_metadata_before_json_escaping(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import delivery001
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'x.txt').write_text('fictional')
            entry = reviewed('x.txt', 'x.txt', b'fictional')
            entry['provenance'] = r'C:\workshop\secret-project\file'
            descriptor = {'schema': 'delivery-001/v1', 'product': 'p', 'version': '1', 'mission': 'm', 'approval': 'owner', 'known_roots': [r'C:\workshop\secret-project'], 'files': [entry], **{key: ['none'] for key in delivery001.FIELDS}}
            path = root / 'descriptor.json'
            path.write_text(json.dumps(descriptor))
            with self.assertRaises(ValueError):
                delivery001.prepare(path, source, root / 'out')

    def test_prepare_and_verify_detects_added_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'program.txt').write_text('hello', encoding='utf-8')
            descriptor = root / 'descriptor.json'
            descriptor.write_text(json.dumps({
                'schema': 'delivery-001/v1', 'product': 'sample', 'version': 'v1',
                'mission': 'example', 'approval': 'owner',
                'known_roots': ['/workshop/project'],
                'files': [reviewed('program.txt', 'program.txt', b'hello')],
                'prerequisites': ['Any runtime'], 'install_steps': ['Copy files'],
                'start_steps': ['Run program'], 'configuration': ['None'],
                'verification_steps': ['Check output'], 'evidence': ['Example'],
                'limitations': ['Demonstration'],
            }), encoding='utf-8')
            output = root / 'delivery'
            args = [sys.executable, str(SCRIPT)]
            result = subprocess.run(args + ['prepare', '--descriptor', str(descriptor), '--source', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Run program', (output / 'INSTALL.md').read_text(encoding='utf-8'))
            manifest = json.loads((output / 'MANIFEST.json').read_text(encoding='utf-8'))
            entry = next(item for item in manifest['files'] if item['path'] == 'program.txt')
            self.assertEqual(entry['review']['provenance'], 'approved revision')
            self.assertEqual(entry['checks']['secret_patterns'], 'passed')
            self.assertEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)
            (output / 'program.txt').write_text('changed')
            self.assertNotEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)
            (output / 'program.txt').write_text('hello')
            (output / 'program.txt').unlink()
            self.assertNotEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)
            (output / 'program.txt').write_text('hello')
            (output / 'unexpected').write_text('x')
            self.assertNotEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)
            (output / 'unexpected').unlink()
            (output / 'nested').mkdir()
            (output / 'nested' / 'MANIFEST.json').write_text('{}')
            self.assertNotEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)
            (output / 'nested' / 'MANIFEST.json').unlink()
            (output / 'PROGRAM.TXT').write_text('hello')
            if len(list(output.glob('*[tT][xX][tT]'))) > 1:
                self.assertNotEqual(subprocess.run(args + ['verify', '--directory', str(output)], capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
