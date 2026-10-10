"""Check release-note boundaries and formats without contacting a publishing service."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release_notes', ROOT / 'tools/prepare-release-notes.py')
notes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notes)

class ReleaseNotes(unittest.TestCase):
    def test_exact_version_section_excludes_other_versions(self):
        text = '# Changelog\n\n## [Unreleased]\nNew work\n\n## [1.2.3] - 2026-10-11\n### Added\n- Target\n\n## [1.2.2]\n- Old\n'
        self.assertEqual(notes.extract_section(text, '1.2.3'), '### Added\n- Target')

    def test_missing_section_fails(self):
        with self.assertRaisesRegex(ValueError, '0 sections'):
            notes.extract_section('## [1.2.2]\nOld', '1.2.3')

    def test_duplicate_sections_fail(self):
        with self.assertRaisesRegex(ValueError, '2 sections'):
            notes.extract_section('## [1.2.3]\nFirst\n## [1.2.3]\nSecond', '1.2.3')

    def test_empty_section_fails(self):
        with self.assertRaisesRegex(ValueError, 'is empty'):
            notes.extract_section('## [1.2.3]\n\n## [1.2.2]\nOld', '1.2.3')

    def test_nexus_description_converts_markup_and_wrapped_items(self):
        section = '### Added\n\n- **Game support** for `PAK` files\n  and [details](https://example.com/guide).\n- Another change'
        self.assertEqual(notes.render(section), '[b]Added[/b]\n\n[list]\n[*][b]Game support[/b] for PAK files and [url=https://example.com/guide]details[/url].\n[*]Another change\n[/list]')

    def test_plain_changelog_contains_no_bbcode_or_markdown(self):
        section = '### Added\n\n- **Support** for `PAK` files\n  and [details](https://example.com/guide).'
        self.assertEqual(notes.render(section, plain=True), 'Added\n\nSupport for PAK files and details (https://example.com/guide).')

    def test_nested_lists_close_before_the_next_heading(self):
        section = '- Parent\n  - Child\n- Next\n\n### Fixed\n\nParagraph\ncontinues.'
        self.assertEqual(notes.render(section), '[list]\n[*]Parent\n[list]\n[*]Child\n[/list]\n[*]Next\n[/list]\n\n[b]Fixed[/b]\n\nParagraph continues.')

    def test_multiline_outputs_preserve_text_and_use_distinct_delimiters(self):
        values = {'bbcode': 'A\nNOTES_END\nB', 'plain': 'Ümlaut and ß'}
        with tempfile.TemporaryDirectory(prefix='cabin-notes-') as directory:
            output = Path(directory) / 'output.txt'
            notes.write_outputs(output, values)
            lines = output.read_text(encoding='utf-8').splitlines()
        decoded, delimiters = {}, []
        index = 0
        while index < len(lines):
            name, delimiter = lines[index].split('<<')
            delimiters.append(delimiter)
            index += 1
            start = index
            while lines[index] != delimiter:
                index += 1
            decoded[name] = '\n'.join(lines[start:index])
            index += 1
        self.assertEqual(decoded, values)
        self.assertEqual(len(set(delimiters)), 2)

if __name__ == '__main__':
    unittest.main()
