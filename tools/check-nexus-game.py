"""Read Nexus game metadata without changing game, mod or file records."""
import argparse
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def read_json(url, api_key):
    request = Request(url, headers={
        'apikey': api_key,
        'Accept': 'application/json',
        'Application-Name': 'TheCabinGame-Vortex',
        'Application-Version': '0.1.1',
    })
    try:
        with urlopen(request, timeout=45) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f'GET {url}: HTTP {error.code}') from error
    except URLError as error:
        raise RuntimeError(f'GET {url}: {error.reason}') from error


def read_games(include_unapproved, api_key):
    url = ('https://api.nexusmods.com/v1/games.json?include_unapproved='
           + str(include_unapproved).lower())
    games = read_json(url, api_key)
    if not isinstance(games, list):
        raise ValueError(f'GET {url}: expected a game list, got {type(games).__name__}')
    return games


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-id', type=int, default=10562)
    parser.add_argument('--mod-file-id', type=int, default=8127426)
    parser.add_argument('--output', type=Path, default=Path('nexus-game.json'))
    args = parser.parse_args()
    if args.game_id <= 0:
        raise ValueError('game-id must be positive')
    api_key = os.environ.get('NEXUSMODS_API_KEY')
    if not api_key:
        raise ValueError('NEXUSMODS_API_KEY is missing')
    approved = read_games(False, api_key)
    all_games = read_games(True, api_key)
    rows = [game for game in all_games if str(game.get('id')) == str(args.game_id)]
    if len(rows) > 1:
        raise ValueError(f'game {args.game_id}: duplicate API records')
    report = {
        'game_id': args.game_id,
        'found_in_all_games': bool(rows),
        'found_in_approved_games': any(str(game.get('id')) == str(args.game_id) for game in approved),
        'approved_list_count': len(approved),
        'all_list_count': len(all_games),
    }
    file_record = read_json(f'https://api.nexusmods.com/v3/mod-files/{args.mod_file_id}', api_key)
    file_data = file_record['data']
    if str(file_data['id']) != str(args.mod_file_id):
        raise ValueError(f'mod file {args.mod_file_id}: returned file ID differs')
    report['mod_file'] = {key: file_data.get(key) for key in
                          ('id', 'name', 'is_active', 'versions_count')}
    report['domain_confirmed'] = False
    if rows:
        game = rows[0]
        domain = game.get('domain_name')
        if not isinstance(domain, str) or not re.fullmatch(r'[a-z0-9]+', domain):
            raise ValueError(f'game {args.game_id}: invalid domain_name')
        report['game'] = {key: game.get(key) for key in
                          ('id', 'name', 'domain_name', 'approved_date')}
        report['domain_confirmed'] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    if not rows:
        print(f'warn: game {args.game_id} is absent from the legacy API game list; approval is not confirmed')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'error: read Nexus game metadata: {error}')
        raise
