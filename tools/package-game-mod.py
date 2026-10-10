"""Package an authored release payload, adding independent UE4SS activation markers."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('payload', type=Path, help='Release-only payload directory; no diagnostic/dev scripts')
    parser.add_argument('--name', required=True)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.name) or not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?', args.version):
        parser.error('name must be a plain package name; version must be semantic')
    payload = args.payload.resolve(strict=True)
    if not payload.is_dir():
        parser.error('payload must be a directory')
    contents = {}
    for file in sorted(payload.rglob('*')):
        if file.is_symlink():
            raise ValueError(f'symlink not permitted in release payload: {file}')
        if file.is_file():
            relative = file.relative_to(payload).as_posix()
            if file.name.lower() in {'diagnostic.lua', 'devbridge.lua', 'probes.lua', 'command.lua'}:
                raise ValueError(f'development script present in release payload: {relative}')
            contents[relative] = file.read_bytes()
    added = []
    for relative in list(contents):
        match = re.match(r'^(.*(?:^|/)Mods/[^/]+)/(?:scripts/main\.lua|dlls/main\.dll)$', relative, re.I)
        if match:
            marker = match[1] + '/enabled.txt'
            if not any(name.lower() == marker.lower() for name in contents):
                contents[marker] = b''
                added.append(marker)
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    manifest = evidence / f'{args.name}-{args.version}-archive-paths.json'
    manifest.write_text(json.dumps(sorted(contents), indent=2) + '\n', encoding='utf-8')
    result = subprocess.run(['node', str(ROOT / 'tools' / 'check-archive.js'), str(manifest)], capture_output=True, text=True)
    (evidence / f'{args.name}-{args.version}-routing.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'archive routing rejected (exit {result.returncode}): {result.stderr.strip()}')
    instructions = json.loads(result.stdout)['instructions']
    target = ROOT / 'dist' / f'{args.name}-{args.version}.zip'
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 10, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(contents):
            raise ValueError('game mod ZIP integrity/path verification failed')
    receipt = {'archive': target.name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
               'activationMarkersAdded': added, 'instructions': instructions,
               'status': 'packaging-verified; gameplay acceptance is separate'}
    target.with_suffix('.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: package game mod: {error}') from error
