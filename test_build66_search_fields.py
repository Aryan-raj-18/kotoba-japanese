"""Build 66: every search field keeps its mic inside the field."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parent
class Build66(unittest.TestCase):
    def test_templates_wrap_inputs(self):
        for t, i in (('grammar','grammar-filter'),('radicals','rad-filter'),('write','kanji-pick-filter'),('japan_explorer','japan-search')):
            html = (ROOT/f'templates/{t}.html').read_text('utf-8')
            self.assertRegex(html, r'<div class="voice-field catalog-search-field"><input[^>]*id="%s"' % i)
    def test_list_name_has_no_mic(self):
        self.assertIn('data-no-voice', (ROOT/'templates/favorites.html').read_text('utf-8'))
        self.assertIn('data-no-voice', (ROOT/'static/js/voice-search.js').read_text('utf-8'))
    def test_mirror(self):
        a = ROOT/'android/app/src/main/python/kotoba_app'
        for f in ('templates/grammar.html','templates/radicals.html','templates/write.html','templates/japan_explorer.html','templates/favorites.html','static/js/voice-search.js','static/css/liquid-glass.css','static/sw.js'):
            self.assertEqual((ROOT/f).read_bytes(), (a/f).read_bytes(), f)
if __name__ == '__main__': unittest.main()
