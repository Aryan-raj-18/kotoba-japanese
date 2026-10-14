"""Build 60 regression: source coverage and Android mirror parity for search controls."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent
ANDROID = ROOT / 'android/app/src/main/python/kotoba_app'

class SearchLayoutBuild60(unittest.TestCase):
    def test_catalog_fields_keep_ids_and_dedicated_voice_slot(self):
        pages = {'templates/kanji_list.html':'kanji-filter', 'templates/jlpt_level.html':'kanji-filter', 'templates/verbs.html':'verb-filter'}
        for path, element_id in pages.items():
            with self.subTest(path=path):
                html = (ROOT / path).read_text('utf-8')
                self.assertIn('class="voice-field catalog-search-field"', html)
                self.assertRegex(html, r'id="'+element_id+r'"[^>]*class="filter-input"')
                self.assertIn('aria-label=', html)

    def test_header_uses_one_microphone_not_two(self):
        # Build 62: that single mic is inside the search bar (plus a phone-only twin).
        html = (ROOT/'templates/base.html').read_text('utf-8')
        voice = (ROOT/'static/js/voice-search.js').read_text('utf-8')
        self.assertIn('id="voice-search-global"', html)
        selector = voice.split("document.querySelectorAll('.filter-input, ", 1)[1].split('.forEach(addButton)', 1)[0]
        self.assertNotIn('form.header-search input[name="q"]', selector)
        self.assertIn('form.hero-search input[name="q"]', selector)

    def test_search_layout_css(self):
        css = (ROOT/'static/css/liquid-glass.css').read_text('utf-8')
        self.assertIn('.catalog-search-field > .voice-inline-btn', css)
        self.assertIn('position: static !important', css)
        self.assertIn('flex: 0 0 46px', css)
        self.assertIn('max-width: 560px', css)
        self.assertIn('.header-search > button[type="submit"]', css)

    def test_android_mirror_and_cache(self):
        files = ('templates/base.html','templates/kanji_list.html','templates/jlpt_level.html','templates/verbs.html','static/css/liquid-glass.css','static/js/voice-search.js','static/sw.js')
        for path in files:
            with self.subTest(path=path):
                self.assertEqual((ROOT/path).read_bytes(), (ANDROID/path).read_bytes())
        self.assertGreaterEqual(int(re.search(r'ASSET_BUILD = "(\d+)"', (ROOT/'app.py').read_text('utf-8')).group(1)), 60)
        self.assertGreaterEqual(int(re.search(r'versionCode (\d+)', (ROOT/'android/app/build.gradle').read_text('utf-8')).group(1)), 60)
        self.assertRegex((ROOT/'static/sw.js').read_text('utf-8'), r'kotoba-shell-v100-build\d+')

if __name__ == '__main__': unittest.main()
