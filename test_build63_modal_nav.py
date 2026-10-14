"""Build 63: popups hide the bottom bar; close button is a round glass control."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parent
class Build63(unittest.TestCase):
    def test_sheet_class_and_css(self):
        self.assertIn('kotoba-sheet-open', (ROOT/'static/js/scroll-lock.js').read_text('utf-8'))
        css = (ROOT/'static/css/liquid-glass.css').read_text('utf-8')
        self.assertIn('body.kotoba-sheet-open .kotoba-bottom-nav', css)
        self.assertIn('.modal-card .modal-close', css)
    def test_mirror(self):
        a = ROOT/'android/app/src/main/python/kotoba_app'
        for f in ('static/js/scroll-lock.js','static/css/liquid-glass.css','static/sw.js'):
            self.assertEqual((ROOT/f).read_bytes(), (a/f).read_bytes(), f)
if __name__ == '__main__': unittest.main()
