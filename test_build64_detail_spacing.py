"""Build 64: detail-page bullets stay inside boxes; consistent inner spacing."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parent
class Build64(unittest.TestCase):
    def test_css(self):
        css = (ROOT/'static/css/liquid-glass.css').read_text('utf-8')
        for needle in ('Build 64', '.rad-read-list {', 'padding: 16px 20px 16px 40px !important',
                       '.sentence-usage {', '.vocab-section .rad-ex {', '.rad-ex-parts span'):
            self.assertIn(needle, css)
    def test_mirror(self):
        a = ROOT/'android/app/src/main/python/kotoba_app'
        self.assertEqual((ROOT/'static/css/liquid-glass.css').read_bytes(), (a/'static/css/liquid-glass.css').read_bytes())
        self.assertEqual((ROOT/'static/sw.js').read_bytes(), (a/'static/sw.js').read_bytes())
if __name__ == '__main__': unittest.main()
