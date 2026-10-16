"""Regression checks for the Japan Explorer heading inset (Build 71)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent

class JapanExplorerHeroSpacingTest(unittest.TestCase):
    def test_hero_has_internal_padding_and_safe_line_height(self):
        style = (ROOT / 'static/css/style.css').read_text(encoding='utf-8')
        self.assertIn('Build 71 — Japan Explorer hero inset', style)
        self.assertRegex(style, r'\.japan-hero\s*\{\s*box-sizing:\s*border-box;\s*padding:\s*clamp\(18px, 2\.2vw, 28px\)')
        self.assertIn('line-height: 1.1;', style)
        self.assertIn('text-wrap: balance;', style)
        self.assertIn('.japan-hero > .japan-hero-copy', style)

    def test_hero_has_mobile_spacing(self):
        style = (ROOT / 'static/css/style.css').read_text(encoding='utf-8')
        self.assertIn('.japan-hero { padding: 18px; gap: 16px; }', style)
        self.assertIn('line-height: 1.13;', style)

    def test_apple_android_web_css_and_asset_versions_match(self):
        target = ROOT / 'android/app/src/main/python/kotoba_app'
        self.assertEqual((ROOT/'static/css/style.css').read_bytes(), (target/'static/css/style.css').read_bytes())
        self.assertEqual((ROOT/'static/sw.js').read_bytes(), (target/'static/sw.js').read_bytes())
        self.assertIn('ASSET_BUILD = "77"', (ROOT/'app.py').read_text())
        self.assertIn('ASSET_BUILD = "77"', (target/'app.py').read_text())
        self.assertIn('versionCode 77', (ROOT/'android/app/build.gradle').read_text())
        self.assertIn('build77', (ROOT/'static/sw.js').read_text())

if __name__ == '__main__': unittest.main()
