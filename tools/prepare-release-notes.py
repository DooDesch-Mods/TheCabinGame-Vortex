"""Render one changelog section for GitHub, Nexus file descriptions and changelog entries."""
import argparse
import json
import os
from pathlib import Path
import re
import uuid

ROOT = Path(__file__).resolve().parents[1]

def extract_section(text, version):
    lines = text.splitlines()
    heading = re.compile(r'^## \[' + re.escape(version) + r'\](?:\s.*)?$')
    matches = [i for i, line in enumerate(lines) if heading.fullmatch(line)]
    if len(matches) != 1:
        raise ValueError(f'CHANGELOG.md has {len(matches)} sections for {version}; expected exactly one')
    start = matches[0] + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith('## ')), len(lines))
    section = '\n'.join(lines[start:end]).strip()
    if not section:
        raise ValueError(f'CHANGELOG.md section for {version} is empty')
    return section

def inline(text, plain):
    text = text.replace('`', '')
    text = re.sub(r'\*\*([^*]+)\*\*', lambda m: m[1] if plain else f'[b]{m[1]}[/b]', text)
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
                  lambda m: f'{m[1]} ({m[2]})' if plain else f'[url={m[2]}]{m[1]}[/url]', text)

def render(section, plain=False):
    output, paragraph = [], []
    item = None
    level = 0

    def flush():
        nonlocal item
        if item:
            indent, words = item
            output.append(('  ' if indent else '') + inline(' '.join(words), True) if plain
                          else '[*]' + inline(' '.join(words), False))
            item = None
        if paragraph:
            output.append(inline(' '.join(paragraph), plain))
            paragraph.clear()

    def lists(wanted):
        nonlocal level
        if not plain:
            while level > wanted:
                output.append('[/list]')
                level -= 1
            while level < wanted:
                output.append('[list]')
                level += 1

    for raw in section.splitlines():
        line = raw.rstrip()
        heading = re.match(r'^#+\s+(.+)$', line)
        bullet = re.match(r'^(\s*)[-*]\s+(.+)$', line)
        if not line.strip():
            flush()
            lists(0)
            output.append('')
        elif heading:
            flush()
            lists(0)
            title = inline(heading[1], plain)
            output.append(title if plain else f'[b]{title}[/b]')
        elif bullet:
            flush()
            indent = len(bullet[1]) >= 2
            lists(2 if indent else 1)
            item = (indent, [bullet[2]])
        elif item:
            item[1].append(line.strip())
        else:
            paragraph.append(line.strip())
    flush()
    lists(0)
    return '\n'.join(output).strip()

def write_outputs(path, values):
    with path.open('a', encoding='utf-8') as stream:
        for name, value in values.items():
            delimiter = 'NOTES_' + uuid.uuid4().hex
            stream.write(f'{name}<<{delimiter}\n{value}\n{delimiter}\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'\d+\.\d+\.\d+', args.version):
        raise ValueError(f'invalid release version: {args.version!r}')
    section = extract_section((ROOT / 'CHANGELOG.md').read_text(encoding='utf-8'), args.version)
    repo = os.environ.get('GITHUB_REPOSITORY', 'DooDesch-Mods/TheCabinGame-Vortex')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError(f'invalid repository name: {repo!r}')
    notes = {'markdown': section, 'plain': render(section, plain=True),
             'bbcode': render(section) + f'\n\n[url=https://github.com/{repo}/releases/tag/v{args.version}]Full release notes[/url]'}
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    for name, suffix in [('markdown', 'md'), ('plain', 'txt'), ('bbcode', 'bbcode')]:
        (evidence / f'release-notes.{suffix}').write_text(notes[name] + '\n', encoding='utf-8')
    if output := os.environ.get('GITHUB_OUTPUT'):
        write_outputs(Path(output), notes)
    print(json.dumps({'status': 'confirmed', 'version': args.version, 'formats': list(notes)}))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        raise SystemExit(f'error: prepare release notes: {error}') from error
