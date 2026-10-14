"""Build 65: result screens of tests/practice/timed tests are aligned inside boxes."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parent
class Build65(unittest.TestCase):
    def test_css(self):
        css = (ROOT/'static/css/liquid-glass.css').read_text('utf-8')
        for n in ('Build 65', '#exam-panel-results', '#placement-done #placement-go', '.mock-breakdown > div:last-child:nth-child(odd)'):
            self.assertIn(n, css)
    def test_mirror(self):
        a = ROOT/'android/app/src/main/python/kotoba_app'
        for f in ('static/css/liquid-glass.css','static/sw.js'):
            self.assertEqual((ROOT/f).read_bytes(), (a/f).read_bytes(), f)
if __name__ == '__main__': unittest.main()
