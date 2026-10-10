"""Exercise publication guards without making a network request."""
import os
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v' + json.loads((ROOT / 'extension' / 'info.json').read_text(encoding='utf-8'))['version']

class ReleaseGuards(unittest.TestCase):
    def run_preflight(self, values):
        environment = os.environ.copy()
        for name in ['RELEASE_TAG', 'NEXUS_GAME_DOMAIN', 'NEXUS_FILE_GROUP_ID', 'NEXUS_LIVE_TESTED', 'NEXUS_API_KEY', 'GITHUB_OUTPUT', 'GITHUB_STEP_SUMMARY']:
            environment.pop(name, None)
        environment.update(values)
        return subprocess.run(['python', str(ROOT / 'tools' / 'prepare-release.py')],
                              env=environment, capture_output=True, text=True, encoding='utf-8')

    def test_unconfigured_nexus_is_an_explicit_skip_with_a_checked_github_package(self):
        result = self.run_preflight({'RELEASE_TAG': TAG})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('deliberate skip', result.stdout)

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

if __name__ == '__main__':
    unittest.main()
