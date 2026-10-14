"""Build a deterministic extension candidate; real Nexus IDs are explicit inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FILES = ['index.js', 'info.json', 'config.json', 'gameart.png', 'cover.jpg', 'README.md', 'CREDITS.md', 'LICENSE.md']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nexus-domain', help='Actual approved Nexus URL domain, never a guessed slug')
    parser.add_argument('--release', action='store_true', help='Use a release filename without changing the game mapping')
    args = parser.parse_args()
    if args.nexus_domain and not re.fullmatch(r'[a-z0-9]+', args.nexus_domain):
        parser.error('Nexus domain must be the literal lowercase domain from the approved game URL')
    source = ROOT / 'extension'
    info = json.loads((source / 'info.json').read_text(encoding='utf-8'))
    if type(info.get('gameId')) is not int or info['gameId'] <= 0:
        raise ValueError('info.json gameId must be the positive numerical Nexus Mods game ID')
    config = json.loads((source / 'config.json').read_text(encoding='utf-8'))
    if args.nexus_domain:
        config.update(gameId=args.nexus_domain, nexusPageId=args.nexus_domain)
    for file in FILES:
        if not (source / file).is_file():
            raise FileNotFoundError(f'required extension file missing: {file}')
    with Image.open(source / 'gameart.png') as art:
        if art.size != (640, 360) or art.format != 'PNG' or (source / 'gameart.png').stat().st_size > 1_000_000:
            raise ValueError('gameart must be PNG, 640x360, at most 1 MB')
    with Image.open(source / 'cover.jpg') as cover:
        if cover.size != (600, 900) or cover.format != 'JPEG' or (source / 'cover.jpg').stat().st_size > 1_000_000:
            raise ValueError('cover must be JPEG, 600x900, at most 1 MB')
    result = subprocess.run(['node', '--check', str(source / 'index.js')], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'index.js syntax check failed: {result.stderr}')
    releases = ROOT / 'dist'
    releases.mkdir(exist_ok=True)
    suffix = '' if args.nexus_domain or args.release else '-local-candidate'
    target = releases / f'TheCabinGame-Vortex-{info["version"]}{suffix}.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            data = (json.dumps(config, indent=2) + '\n').encode() if name == 'config.json' else (source / name).read_bytes()
            entry = zipfile.ZipInfo(name, (2026, 10, 10, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(FILES):
            raise ValueError('extension archive content/integrity verification failed')
        if json.loads(archive.read('config.json')) != config:
            raise ValueError('packaged Nexus mapping differs from requested mapping')
        if json.loads(archive.read('info.json')) != info:
            raise ValueError('packaged extension metadata differs from source')
    receipt = {'archive': target.name, 'version': info['version'], 'bytes': target.stat().st_size,
               'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'config': config,
               'nexusGameId': info['gameId'],
               'files': FILES, 'status': 'packaged-release' if args.release else 'packaged-candidate',
               'gameMapping': 'configured' if config['nexusPageId'] else 'pending'}
    target.with_suffix('.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: build Vortex extension: {error}') from error
