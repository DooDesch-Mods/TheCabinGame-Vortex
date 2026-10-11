"""Read back the Nexus file version acknowledged by the upload action."""
import json
import os
from pathlib import Path
import argparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before-upload', action='store_true')
    args = parser.parse_args()
    version_id = os.environ.get('NEXUS_VERSION_ID', '')
    file_id = os.environ.get('NEXUS_FILE_GROUP_ID', '')
    version = os.environ.get('RELEASE_VERSION', '')
    key = os.environ.get('NEXUSMODS_API_KEY', '')
    if (not args.before_upload and not version_id.isdigit()) or not file_id.isdigit() or not version or not key:
        raise ValueError('Nexus readback requires version ID, file ID, release version and API key')
    url = f'https://api.nexusmods.com/v3/mod-files/{file_id}/versions'
    request = Request(url, headers={'apikey': key, 'Accept': 'application/json'})
    try:
        with urlopen(request, timeout=45) as response:
            records = json.load(response)['data']['versions']
    except HTTPError as error:
        raise RuntimeError(f'GET {url}: HTTP {error.code}') from error
    except URLError as error:
        raise RuntimeError(f'GET {url}: {error.reason}') from error
    if args.before_upload:
        output = Path('evidence/nexus-before-upload.json')
        output.parent.mkdir(exist_ok=True)
        selected = [{key: row.get(key) for key in ('id', 'version', 'category', 'is_primary', 'name')}
                    for row in records]
        output.write_text(json.dumps({'file_id': file_id, 'versions': selected}, indent=2) + '\n', encoding='utf-8')
        existing = [str(row['id']) for row in records if row['version'] == version]
        if existing:
            raise ValueError(f'file {file_id} already has version {version}: {existing}; inspect before another upload')
        print(f'info: Nexus file {file_id}: version {version} is not present; upload can proceed')
        return
    rows = [row for row in records if str(row['id']) == version_id]
    if len(rows) != 1:
        raise ValueError(f'Nexus version {version_id}: expected one acknowledged record, found {len(rows)}')
    row = rows[0]
    if str(row['file']['id']) != file_id or row['version'] != version or row['category'] != 'main':
        raise ValueError(f'Nexus version {version_id}: file, version or category differs from the release target')
    if not row.get('is_primary', False):
        raise ValueError(f'Nexus version {version_id}: uploaded file is not primary')
    report = {'status': 'confirmed', 'file_id': file_id, 'version_id': version_id,
              'version': row['version'], 'category': row['category'],
              'is_primary': row['is_primary'], 'name': row['name'],
              'game_scoped_id': row['game_scoped_id'],
              'versions': [{key: item.get(key) for key in ('id', 'version', 'category', 'is_primary')}
                           for item in records]}
    output = Path('evidence/nexus-upload-confirmation.json')
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: verify Nexus upload: {error}') from error
