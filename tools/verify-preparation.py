"""Check the new release-payload packager and the prepared artifact links."""
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    evidence = ROOT / 'evidence'
    payload = evidence / 'TEST-ONLY-payload'
    script = payload / 'Mods' / 'CabinRejoin' / 'Scripts' / 'main.lua'
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text('-- TEST FIXTURE ONLY: not a gameplay mod\n', encoding='utf-8')
    (payload / 'Fixture_P.pak').write_bytes(b'TEST FIXTURE ONLY: not a valid game container')
    (payload / 'README.md').write_text('TEST ONLY — do not install or upload.\n', encoding='utf-8')
    result = subprocess.run(['python', '-X', 'utf8', str(ROOT / 'tools' / 'package-game-mod.py'),
                             str(payload), '--name', 'TESTONLY', '--version', '0.0.0'],
                            capture_output=True, text=True, encoding='utf-8')
    (evidence / 'package-fixture.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'fixture package failed (exit {result.returncode}): {result.stderr.strip()}')
    receipt = json.loads(result.stdout)
    if receipt['activationMarkersAdded'] != ['Mods/CabinRejoin/enabled.txt']:
        raise ValueError(f'activation marker not added as required: {receipt["activationMarkersAdded"]}')
    target = ROOT / 'dist' / 'TESTONLY-0.0.0.zip'
    with zipfile.ZipFile(target) as archive:
        if archive.read('Mods/CabinRejoin/enabled.txt') != b'':
            raise ValueError('activation marker content is not empty')
        names = archive.namelist()
    # Keep test archives behind the evidence pointer, separate from upload candidates.
    target.replace(evidence / target.name)
    target.with_suffix('.json').replace(evidence / target.with_suffix('.json').name)
    broken = []
    for file in list(ROOT.glob('*.md')) + list((ROOT / 'extension').glob('*.md')) + list((ROOT / 'submission').glob('*.md')):
        for link in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
            if not re.match(r'https?://', link) and not (file.parent / link.split('#')[0]).exists():
                broken.append({'file': str(file.relative_to(ROOT)), 'link': link})
    if broken:
        raise ValueError(f'broken local artifact links: {broken}')
    summary = (ROOT / 'submission' / 'vortex-summary.txt').read_text(encoding='utf-8').strip()
    if len(summary) > 250:
        raise ValueError(f'Nexus summary is too long: {len(summary)}/250')
    report = {'status': 'confirmed', 'markerAddedAndArchived': True, 'fixtureFiles': names,
              'localLinks': 'all checked', 'nexusSummaryCharacters': len(summary),
              'scope': 'package builder and prepared artifact links; not live Vortex/game acceptance'}
    (evidence / 'preparation-check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: verify preparation: {error}') from error
