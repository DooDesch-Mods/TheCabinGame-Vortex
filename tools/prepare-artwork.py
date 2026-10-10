"""Build the Vortex thumbnail from a pinned official Steam screenshot."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4406280/988df32abf01cc99c07001c6634717522ea873d7/ss_988df32abf01cc99c07001c6634717522ea873d7.1920x1080.jpg?t=1787842454'
SOURCE_SHA256 = '06fd32245ad5df95babcd7d3d26490f5f9b0c697b0e3fd92f9897802b5d1f686'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, help='Local copy of the pinned original JPEG; otherwise download from Steam')
    args = parser.parse_args()
    if args.source:
        data = args.source.read_bytes()
    else:
        request = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'DooDesch-Vortex-Artwork/1.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise ValueError(f'Steam screenshot HTTP status: {response.status}')
            data = response.read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != SOURCE_SHA256:
        raise ValueError(f'original screenshot hash differs: expected={SOURCE_SHA256}, actual={actual}')
    with Image.open(io.BytesIO(data)) as image:
        if image.size != (1920, 1080):
            raise ValueError(f'original screenshot dimensions differ: {image.size}')
        output = image.convert('RGB').resize((640, 360), Image.Resampling.LANCZOS)
        target = ROOT / 'extension/gameart.png'
        output.save(target, format='PNG', optimize=True)
    with Image.open(target) as image:
        if image.format != 'PNG' or image.size != (640, 360) or target.stat().st_size > 1_000_000:
            raise ValueError('Vortex thumbnail must be PNG, 640x360 and at most 1 MB')
    print(json.dumps({'status': 'confirmed', 'source': SOURCE_URL, 'sourceSha256': actual, 'thumbnail': str(target), 'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: prepare Vortex artwork: {error}') from error
