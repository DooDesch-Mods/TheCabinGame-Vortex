"""Exercise publication guards without making a network request."""
import os
import json
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v' + json.loads((ROOT / 'extension' / 'info.json').read_text(encoding='utf-8'))['version']

class ReleaseGuards(unittest.TestCase):
    def run_preflight(self, values):
        environment = os.environ.copy()
        for name in ['RELEASE_TAG', 'NEXUS_GAME_DOMAIN', 'NEXUS_FILE_GROUP_ID', 'NEXUS_MOD_ID', 'NEXUS_LIVE_TESTED', 'NEXUS_API_KEY', 'PUBLISH_NEXUS', 'GITHUB_OUTPUT', 'GITHUB_STEP_SUMMARY']:
            environment.pop(name, None)
        environment.update(values)
        # Run the real builder in a disposable fixture. A test-domain ZIP must
        # never appear next to the user's upload candidates in this repository.
        with tempfile.TemporaryDirectory(prefix='cabin-release-guard-') as directory:
            fixture = Path(directory)
            shutil.copytree(ROOT / 'extension', fixture / 'extension')
            (fixture / 'tools').mkdir()
            for name in ['prepare-release.py', 'build-extension.py']:
                shutil.copy2(ROOT / 'tools' / name, fixture / 'tools' / name)
            return subprocess.run(['python', str(fixture / 'tools' / 'prepare-release.py')],
                                  env=environment, capture_output=True, text=True, encoding='utf-8')

    def test_first_upload_is_an_explicit_skip_with_a_final_domain_package(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_LIVE_TESTED': 'true'})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['nexusReady'])
        self.assertIn('deliberate skip', report['nexusStatus'])
        self.assertNotIn('local-candidate', report['asset'])

    def test_tested_release_without_domain_preserves_local_mapping(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_LIVE_TESTED': 'true'})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['gameConfig'], {'gameId': 'thecabingame', 'nexusPageId': None})
        self.assertEqual(report['gameMapping'], 'pending')
        self.assertNotIn('local-candidate', report['asset'])

    def test_upload_without_domain_keeps_game_downloads_unmapped(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_LIVE_TESTED': 'true',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_API_KEY': 'test-fixture-only'})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['nexusReady'])
        self.assertIsNone(report['gameConfig']['nexusPageId'])

    def test_invalid_domain_still_fails(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_LIVE_TESTED': 'true',
                                    'NEXUS_GAME_DOMAIN': 'bad-domain'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('actual lowercase Nexus domain', result.stderr)

    def test_first_upload_without_live_acceptance_fails(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('actual Vortex/game acceptance', result.stderr)

    def test_invalid_file_group_fails(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': 'invalid', 'NEXUS_LIVE_TESTED': 'true'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('numeric API Info', result.stderr)

    def test_configured_target_is_ready_without_an_upload(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_LIVE_TESTED': 'true',
                                    'NEXUS_API_KEY': 'test-fixture-only'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['nexusReady'])

    def test_wrong_tag_fails_before_packaging(self):
        result = self.run_preflight({'RELEASE_TAG': 'mismatched-tag'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('does not match', result.stderr)

    def test_configured_target_without_live_acceptance_fails(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly', 'NEXUS_FILE_GROUP_ID': '123'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('actual Vortex/game acceptance', result.stderr)

    def test_configured_target_without_key_fails(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_LIVE_TESTED': 'true'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('API_KEY is unavailable', result.stderr)

    def test_manual_run_without_upload_selection_does_not_need_a_key(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_LIVE_TESTED': 'true',
                                    'PUBLISH_NEXUS': 'false'})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['nexusReady'])
        self.assertIn('upload not requested', report['nexusStatus'])

    def test_manual_run_cannot_bypass_live_acceptance(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'PUBLISH_NEXUS': 'false'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('actual Vortex/game acceptance', result.stderr)

    def test_upload_selection_requires_an_explicit_boolean(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'PUBLISH_NEXUS': 'maybe'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('PUBLISH_NEXUS must be true or false', result.stderr)

    def test_unique_mod_id_is_preserved_without_numeric_rounding(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_MOD_ID': '9856949946759',
                                    'NEXUS_LIVE_TESTED': 'true', 'NEXUS_API_KEY': 'test-fixture-only'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['modId'], '9856949946759')

    def test_invalid_unique_mod_id_fails_before_packaging(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_MOD_ID': 'not-a-number', 'NEXUS_LIVE_TESTED': 'true'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('API Unique Mod ID', result.stderr)

    def test_missing_mod_id_reports_changelog_skip(self):
        result = self.run_preflight({'RELEASE_TAG': TAG, 'NEXUS_GAME_DOMAIN': 'testonly',
                                    'NEXUS_FILE_GROUP_ID': '123', 'NEXUS_LIVE_TESTED': 'true',
                                    'NEXUS_API_KEY': 'test-fixture-only'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('warn: Nexus changelog tab will be skipped', result.stderr)

if __name__ == '__main__':
    unittest.main()
