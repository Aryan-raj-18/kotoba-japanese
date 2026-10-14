"""Build 53: Everyday category headings stay inset on every dynamically rendered block."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent


class EverydayHeader53(unittest.TestCase):
    def test_category_padding_scoped_to_everyday_list(self):
        css = (ROOT/'static/css/style.css').read_text(encoding='utf-8')
        self.assertRegex(css, r'#everyday-list\s*>\s*\.category-block\s*\{\s*padding:\s*clamp\(12px,')
        self.assertRegex(css, r'#everyday-list\s*>\s*\.category-block\s*>\s*\.category-heading\s*\{[^}]*margin:\s*0 0 12px;[^}]*line-height:\s*1\.35;',re.S)
        self.assertIn('overflow-wrap: anywhere;', css)

    def test_dynamic_categories_get_same_css(self):
        html = (ROOT/'templates/everyday.html').read_text(encoding='utf-8')
        js = (ROOT/'static/js/everyday.js').read_text(encoding='utf-8')
        self.assertIn('id="everyday-list"', html)
        self.assertIn('class="category-block"', html)
        self.assertIn('class="category-heading"', html)
        self.assertIn("block.className='category-block'", js)
        self.assertIn("h.className='category-heading'", js)

    def test_release_files_match_android_and_version(self):
        prefix = ROOT/'android/app/src/main/python/kotoba_app'
        for file in ('static/css/style.css', 'static/sw.js'):
            self.assertEqual((ROOT/file).read_bytes(), (prefix/file).read_bytes())
        src = (ROOT/'app.py').read_text(encoding='utf-8')
        build = re.search(r'ASSET_BUILD\s*=\s*"(\d+)"',src).group(1)
        self.assertGreaterEqual(int(build),53)
        self.assertIn(f'kotoba-shell-v100-build{build}',(ROOT/'static/sw.js').read_text(encoding='utf-8'))
        self.assertIn(f'versionCode {build}',(ROOT/'android/app/build.gradle').read_text(encoding='utf-8'))


if __name__=='__main__':
    unittest.main()
