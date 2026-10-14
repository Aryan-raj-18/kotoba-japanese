"""Build 52: Liquid Glass and Clear Glass must be different across page types.

These checks are dependency-free and run in both GitHub Actions and the offline
Android app source tree. Browser rendering is additionally verified in Chromium.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent


class ClearGlass52(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = (ROOT / 'static/css/liquid-glass.css').read_text(encoding='utf8')
        cls.shell = (ROOT / 'static/css/journey.css').read_text(encoding='utf8')
        cls.controller = (ROOT / 'static/js/liquid-glass.js').read_text(encoding='utf8')

    def test_both_modes_have_distinct_translucent_surfaces(self):
        for opacity in ('43%', '36%', '23%', '17%', '8%'):
            self.assertIn(opacity + ',transparent)', self.css)
        self.assertIn('--liquid-blur: blur(18px)', self.css)
        self.assertIn('--liquid-reflection: none;', self.css)
        self.assertIn('--shell-surface:var(--liquid-panel)', self.css)
        self.assertIn('--shell-input-bg:var(--liquid-panel-strong)', self.css)
        self.assertNotIn('background-color:var(--card-bg) !important;\n}', self.css)

    def test_screen_specific_opaque_overrides_are_handled(self):
        for cls in ('rm-stage-nav a', 'trace-stage', 'write-panel > .sub-panel',
                    'category-block .everyday-row', 'vocab-section .rad-ex',
                    'kana-chart .kana-tile', 'modal-card', 'story-body',
                    'exam-quiz-card', 'japan-map-card', 'jlpt-entry-card'):
            with self.subTest(cls=cls):
                self.assertIn('.' + cls, self.css)
        self.assertIn('--liquid-dialog', self.css)
        self.assertIn('.modal-overlay {background:rgba(8,15,32,.32);}', self.css)

    def test_no_duplicate_blur_on_child_rows(self):
        self.assertIsNotNone(re.search(r'\.vocab-section \.rad-ex.*?\)\s*\{background-color:var\(--liquid-inset\) !important;', self.css, re.S))
        self.assertIn('backdrop-filter:none !important;', self.css)
        self.assertNotIn('createElementNS', self.controller)

    def test_build_and_android_mirror(self):
        build = re.search(r'ASSET_BUILD = "(\d+)"', (ROOT / 'app.py').read_text()).group(1)
        self.assertGreaterEqual(int(build), 52)  # Build 52 glass contract applies to newer releases
        self.assertIn(f'build{build}', (ROOT/'static/sw.js').read_text())
        for path in ('app.py', 'static/css/liquid-glass.css', 'static/sw.js'):
            with self.subTest(path=path):
                native = ROOT/'android/app/src/main/python/kotoba_app'/path
                self.assertEqual((ROOT/path).read_bytes(), native.read_bytes() if path != 'app.py'
                                 else native.read_bytes().split(b'\n\n_server_lock', 1)[0].rstrip() + b'\n')


if __name__ == '__main__':
    unittest.main()
