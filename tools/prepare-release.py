"""Fail-visible release preflight; no API call or credential output."""
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    version = json.loads((ROOT / 'extension' / 'info.json').read_text(encoding='utf-8'))['version']
    tag = os.environ.get('RELEASE_TAG', '')
    if tag != f'v{version}':
        raise ValueError(f'release tag {tag!r} does not match info.json version v{version}')
    domain = os.environ.get('NEXUS_GAME_DOMAIN', '')
    group = os.environ.get('NEXUS_FILE_GROUP_ID', '')
    tested = os.environ.get('NEXUS_LIVE_TESTED', '') == 'true'
    has_key = bool(os.environ.get('NEXUS_API_KEY'))
    configured = bool(domain and group)
    if configured and not re.fullmatch(r'\d+', group):
        raise ValueError('NEXUS_FILE_GROUP_ID must be the numeric API Info file-group ID')
    if configured and not tested:
        raise ValueError('Nexus target configured, but NEXUS_LIVE_TESTED is not true; actual Vortex/game acceptance is still pending')
    if configured and not has_key:
        raise ValueError('Nexus target configured, but NEXUSMODS_API_KEY is unavailable')
    command = ['python', str(ROOT / 'tools' / 'build-extension.py')]
    if domain:
        command.extend(['--nexus-domain', domain])
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'extension build failed (exit {result.returncode}): {result.stderr}')
    build = json.loads(result.stdout)
    asset = 'dist/' + build['archive']
    report = {'version': version, 'asset': asset, 'nexusReady': configured,
              'nexusStatus': 'configured' if configured else 'deliberate skip: initial Nexus game/file IDs pending',
              'sha256': build['sha256']}
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    (evidence / 'release-preflight.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if output := os.environ.get('GITHUB_OUTPUT'):
        with open(output, 'a', encoding='utf-8') as stream:
            stream.write(f'version={version}\nasset={asset}\nnexus_ready={str(configured).lower()}\n')
    if summary := os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(summary, 'a', encoding='utf-8') as stream:
            stream.write(f'Package: {asset}\n\nNexus: {report["nexusStatus"]}\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: release preflight: {error}') from error
