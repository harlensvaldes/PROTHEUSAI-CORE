import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'core'
        self.source.mkdir()
        manifest = json.loads((ROOT / 'bootstrap/allowlist.json').read_text(encoding='utf-8'))
        paths = [entry['source'] for entry in manifest['files']]
        paths += ['bootstrap/allowlist.json', 'scripts/bootstrap001.py']
        for name in set(paths):
            dest = self.source / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        self.git('init', '-q', '--template=', cwd=self.source)
        self.git('add', '--all', cwd=self.source)
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'synthetic fixture', cwd=self.source)

    def git(self, *args, cwd):
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
        env['GIT_CONFIG_NOSYSTEM'] = '1'
        env['GIT_CONFIG_GLOBAL'] = os.devnull
        return subprocess.run(['git', *args], cwd=cwd, env=env, check=True,
                              capture_output=True, text=True)

    def run_bootstrap(self, destination, env=None, name='Fictional Product', ident='fictional-product'):
        return subprocess.run([sys.executable, '-B', str(self.source / 'scripts/bootstrap001.py'),
                               '--name', name, '--id', ident, '--destination', str(destination)],
                              cwd=self.base, env=env, capture_output=True, text=True)

    def test_new_project_is_independent_and_can_start_mission(self):
        dest = self.base / 'product'
        result = self.run_bootstrap(dest)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(dest.resolve(), Path(self.git('rev-parse', '--show-toplevel', cwd=dest).stdout.strip()).resolve())
        self.assertEqual('', self.git('remote', cwd=dest).stdout.strip())
        self.assertIn('Fictional Product', (dest / 'README.md').read_text(encoding='utf-8'))
        self.assertTrue((dest / 'prompts/00_START_PROJECT.md').is_file())
        self.assertFalse((dest / 'docs/MISSIONS/DELIVERY-001').exists())
        self.assertFalse((dest / 'docs/MISSIONS/DESIGN-001').exists())
        role = 'agents/creative_director.md'
        self.assertEqual((self.source / role).read_bytes(), (dest / role).read_bytes())
        provenance = json.loads((dest / 'bootstrap-provenance.json').read_text(encoding='utf-8'))
        self.assertIn({'source': role, 'destination': role,
                       'sha256': hashlib.sha256((dest / role).read_bytes()).hexdigest()},
                      provenance['files'])
        for path in ('docs/CONTEXT-001.md', 'docs/templates/CHECKPOINT.md',
                     'scripts/met001.py', 'docs/MET-001.md', 'tests/test_met001.py'):
            self.assertEqual((self.source / path).read_bytes(), (dest / path).read_bytes(), path)
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                                 '-s', 'tests', '-p', 'test_met001.py'], cwd=dest,
                                capture_output=True, text=True)
        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        match = re.search(r'Ran (\d+) tests? in ', output)
        self.assertIsNotNone(match, output)
        self.assertGreater(int(match.group(1)), 0, output)
        result = subprocess.run([sys.executable, '-B', 'scripts/new_mission.py', '--id', 'TEST-900',
                                 '--title', 'Fictional', '--risk', 'LOW', '--orchestrator', 'orch'],
                                cwd=dest, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        result = subprocess.run([sys.executable, '-B', 'scripts/quality_cli.py', 'validate'],
                                cwd=dest, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, '-B', 'scripts/new_mission.py', '--id', 'TEST-901',
                                 '--title', 'Fictional v5', '--risk', 'HIGH', '--orchestrator', 'orch',
                                 '--profile', 'LOCAL_FICTIONAL_EXPERIMENTAL', '--project-id', 'fixture',
                                 '--owner-decision-ref', 'fixture'], cwd=dest, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        result = subprocess.run([sys.executable, '-B', 'scripts/quality_cli.py', 'validate'], cwd=dest,
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        mission_doc = (dest / 'docs/MISSIONS/README.md').read_text(encoding='utf-8')
        for token in ('v3', 'v4', 'v5', 'gate1_waiver', 'scope_digest'):
            self.assertIn(token, mission_doc)

    def test_existing_destination_and_invalid_id_are_rejected(self):
        dest = self.base / 'existing'
        dest.mkdir()
        marker = dest / 'marker'
        marker.write_text('keep', encoding='utf-8')
        self.assertNotEqual(0, self.run_bootstrap(dest).returncode)
        self.assertEqual('keep', marker.read_text(encoding='utf-8'))
        invalid = self.base / 'invalid'
        self.assertNotEqual(0, self.run_bootstrap(invalid, ident='../escape').returncode)
        self.assertFalse(invalid.exists())
        self.assertNotEqual(0, self.run_bootstrap(self.base / 'invalid-name', name='A\u2028B').returncode)
        self.assertFalse((self.base / 'invalid-name').exists())
        self.assertNotEqual(0, self.run_bootstrap(self.base / 'control-name', name='A\u0081B').returncode)
        self.assertFalse((self.base / 'control-name').exists())
        self.assertNotEqual(0, self.run_bootstrap('C:relative').returncode)
        self.assertNotEqual(0, self.run_bootstrap(str(self.base / 'x' / '..' / 'ambiguous')).returncode)
        self.assertFalse((self.base / 'ambiguous').exists())

    def test_reproducible_tree_and_project_specific_exclusions(self):
        first, second = self.base / 'first', self.base / 'second'
        self.assertEqual(0, self.run_bootstrap(first).returncode)
        self.assertEqual(0, self.run_bootstrap(second).returncode)
        def files(root):
            return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(root).parts}
        self.assertEqual(files(first), files(second))
        content = b'\n'.join(files(first).values()).lower()
        self.assertNotIn(b'camisas chatgpt', content)
        self.assertFalse((first / 'dist').exists())
        self.assertEqual(['README.md'], sorted(p.name for p in (first / 'docs/MISSIONS').iterdir()))
        provenance = json.loads((first / 'bootstrap-provenance.json').read_text(encoding='utf-8'))
        self.assertEqual(self.git('rev-parse', 'HEAD', cwd=self.source).stdout.strip(), provenance['core_commit'])
        self.assertNotIn(str(self.source).encode(), b'\n'.join(files(first).values()))

    def test_hostile_git_environment_and_template_do_not_redirect(self):
        hostile = self.base / 'hostile'
        hostile.mkdir()
        self.git('init', '-q', cwd=hostile)
        (hostile / 'fixture.txt').write_text('fixture', encoding='utf-8')
        self.git('add', 'fixture.txt', cwd=hostile)
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'fixture', cwd=hostile)
        template = self.base / 'hostile-template'
        (template / 'hooks').mkdir(parents=True)
        hook = template / 'hooks/post-checkout'
        hook.write_text('#!/bin/sh\nprintf triggered > hook-ran\n', encoding='utf-8', newline='\n')
        hook.chmod(0o755)
        self.git('-c', 'core.hooksPath=' + str(template / 'hooks'), 'checkout', '-qb', 'canary', cwd=hostile)
        self.assertTrue((hostile / 'hook-ran').exists(), 'hostile hook must actually execute in canary')
        (hostile / 'hook-ran').unlink()
        config = self.base / 'hostile-config'
        config.write_text('[init]\n\ttemplateDir = ' + str(template).replace('\\', '/') + '\n', encoding='utf-8')
        env = os.environ.copy()
        env.update(GIT_DIR=str(hostile / '.git'), GIT_WORK_TREE=str(hostile),
                   GIT_TEMPLATE_DIR=str(template), GIT_CONFIG_GLOBAL=str(config),
                   GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.hooksPath',
                   GIT_CONFIG_VALUE_0=str(template / 'hooks'))
        before = {p.relative_to(hostile).as_posix(): p.read_bytes() for p in hostile.rglob('*') if p.is_file()}
        dest = self.base / 'isolated'
        result = self.run_bootstrap(dest, env=env)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((dest / '.git').is_dir())
        self.assertFalse((dest / '.git/hooks/post-checkout').exists())
        self.assertFalse((dest / '.git/objects/info/alternates').exists())
        self.assertEqual('', self.git('remote', cwd=dest).stdout.strip())
        self.assertFalse((dest / 'hook-ran').exists())
        after = {p.relative_to(hostile).as_posix(): p.read_bytes() for p in hostile.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertNotIn('hooksPath', (dest / '.git/config').read_text(encoding='utf-8'))

    def test_modified_source_and_nested_repository_are_rejected(self):
        (self.source / 'AGENTS.md').write_text('modified', encoding='utf-8')
        dest = self.base / 'dirty'
        self.assertNotEqual(0, self.run_bootstrap(dest).returncode)
        self.assertFalse(dest.exists())
        nested = self.source / 'nested'
        self.assertNotEqual(0, self.run_bootstrap(nested).returncode)
        self.assertFalse(nested.exists())

    def test_skip_worktree_cannot_hide_modified_source(self):
        self.git('update-index', '--skip-worktree', 'AGENTS.md', cwd=self.source)
        (self.source / 'AGENTS.md').write_text('ALTERED CONTENT', encoding='utf-8')
        dest = self.base / 'hidden-change'
        result = self.run_bootstrap(dest)
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(dest.exists())

    def test_committed_traversal_in_allowlist_is_rejected(self):
        path = self.source / 'bootstrap/allowlist.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        data['files'][0]['destination'] = '../escape'
        path.write_text(json.dumps(data), encoding='utf-8')
        self.git('add', 'bootstrap/allowlist.json', cwd=self.source)
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'adversarial fixture', cwd=self.source)
        dest = self.base / 'bad-manifest'
        self.assertNotEqual(0, self.run_bootstrap(dest).returncode)
        self.assertFalse(dest.exists())
        self.assertFalse((self.base / 'escape').exists())

    def test_existing_symlink_destination_is_rejected(self):
        target = self.base / 'link-target'
        target.mkdir()
        link = self.base / 'link'
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            self.skipTest('symlink privilege unavailable: ' + str(exc))
        self.assertNotEqual(0, self.run_bootstrap(link).returncode)
        self.assertEqual([], list(target.iterdir()))

    def test_concurrent_creations_never_overwrite(self):
        dest = self.base / 'race'
        args = [sys.executable, '-B', str(self.source / 'scripts/bootstrap001.py'),
                '--name', 'Race', '--id', 'race', '--destination', str(dest)]
        a = subprocess.Popen(args, cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        b = subprocess.Popen(args, cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        a.communicate(timeout=60)
        b.communicate(timeout=60)
        self.assertEqual([0, 1], sorted([a.returncode, b.returncode]))
        self.assertTrue((dest / '.git').is_dir())

    def test_post_creation_failure_retains_partial_directory(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('bootstrap_fixture', ROOT / 'scripts/bootstrap001.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        dest = self.base / 'partial'
        with patch.object(module, 'source_files', return_value=('abc', b'{}', [('x', 'file', b'data')])), \
             patch.object(module, 'git', side_effect=ValueError('fixture failure')):
            with self.assertRaisesRegex(ValueError, 'partial destination retained'):
                module.create('Fixture', 'fixture', dest)
        self.assertEqual(b'data', (dest / 'file').read_bytes())

    def test_generated_readme_collision_is_not_overwritten(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('bootstrap_collision', ROOT / 'scripts/bootstrap001.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        dest = self.base / 'collision'
        real_open = Path.open
        def open_with_collision(path, *args, **kwargs):
            if path == dest / 'README.md':
                with real_open(path, 'w', encoding='utf-8') as out:
                    out.write('existing')
            return real_open(path, *args, **kwargs)
        with patch.object(module, 'source_files', return_value=('abc', b'{}', [])), \
             patch.object(Path, 'open', open_with_collision):
            with self.assertRaisesRegex(ValueError, 'partial destination retained'):
                module.create('Fixture', 'fixture', dest)
        self.assertEqual('existing', (dest / 'README.md').read_text(encoding='utf-8'))

    def test_source_reads_are_pinned_if_head_changes(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('bootstrap_pinned', self.source / 'scripts/bootstrap001.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        before = self.git('rev-parse', 'HEAD', cwd=self.source).stdout.strip()
        real = module.committed_bytes
        revisions = []
        def change_head(revision, name):
            revisions.append(revision)
            result = real(revision, name)
            if len(revisions) == 1:
                (self.source / 'unrelated.txt').write_text('new commit', encoding='utf-8')
                self.git('add', 'unrelated.txt', cwd=self.source)
                self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                         'commit', '-qm', 'move head', cwd=self.source)
            return result
        with patch.object(module, 'committed_bytes', side_effect=change_head):
            head, _, _ = module.source_files()
        self.assertEqual(before, head)
        self.assertTrue(all(revision == before for revision in revisions))
        self.assertNotEqual(before, self.git('rev-parse', 'HEAD', cwd=self.source).stdout.strip())

    def test_missing_git_retains_partial_destination(self):
        # Source validation uses Git before creation, so a missing executable makes no destination.
        env = os.environ.copy()
        env['PATH'] = ''
        dest = self.base / 'no-git'
        self.assertNotEqual(0, self.run_bootstrap(dest, env=env).returncode)
        self.assertFalse(dest.exists())


if __name__ == '__main__':
    unittest.main()
