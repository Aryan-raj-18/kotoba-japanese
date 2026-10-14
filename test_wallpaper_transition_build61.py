"""Build 61 fast checks for first-paint wallpaper continuity (no Flask dependency)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent
ANDROID = ROOT / 'android/app/src/main/python/kotoba_app'

class WallpaperNavigationBuild61(unittest.TestCase):
    def test_prepaint_uses_saved_image_before_css(self):
        html = (ROOT / 'templates/base.html').read_text()
        self.assertLess(html.index("localStorage.getItem('kotoba:wallpaper:preview')"), html.index('css/style.css'))
        self.assertIn("root.setAttribute('data-wallpaper-preview', 'ready')", html)
        self.assertNotIn("node.className = 'kotoba-wallpaper kotoba-wallpaper-preview'", html)
    def test_framing_and_dim_read_before_paint(self):
        html = (ROOT / 'templates/base.html').read_text()
        self.assertIn("kotoba:wallpaper:preview:dims", html)
        self.assertIn("--wallpaper-boot-size", html)
        self.assertIn("--wallpaper-boot-position", html)
        self.assertIn("--wallpaper-boot-dim", html)
    def test_css_fallback_and_cross_document_transition(self):
        css=(ROOT/'static/css/ui-shell.css').read_text()
        self.assertIn('html[data-ui-shell="immersive"][data-wallpaper-preview="ready"] body::before',css)
        self.assertIn('var(--wallpaper-boot-image)',css)
        self.assertIn('@view-transition { navigation: auto; }',css)
        self.assertIn('prefers-reduced-motion: reduce',css)
    def test_original_image_is_decoded_before_swap(self):
        js=(ROOT/'static/js/ui-shell.js').read_text()
        start=js.index('function setWallpaper(')
        chunk=js[start:js.index('function clearWallpaper()',start)]
        self.assertLess(chunk.index('loadImageDimensions(nextUrl).then'),chunk.index("wallpaper.style.visibility = 'visible'"))
        self.assertIn('if (currentObjectUrl !== nextUrl)',chunk)
        self.assertIn('preview:dims',chunk)
        self.assertIn('forcePreview',chunk)
    def test_clear_and_stale_state(self):
        js=(ROOT/'static/js/ui-shell.js').read_text()
        self.assertIn("document.documentElement.removeAttribute('data-wallpaper-preview')",js)
        self.assertIn("localStorage.removeItem('kotoba:wallpaper:preview:dims')",js)
    def test_android_and_cache_parity(self):
        for rel in ('templates/base.html','static/css/ui-shell.css','static/js/ui-shell.js','static/sw.js'):
            self.assertEqual((ROOT/rel).read_bytes(),(ANDROID/rel).read_bytes(),rel)
        import re
        self.assertGreaterEqual(int(re.search(r'ASSET_BUILD = "(\d+)"',(ROOT/'app.py').read_text()).group(1)),61)
        self.assertGreaterEqual(int(re.search(r'ASSET_BUILD = "(\d+)"',(ANDROID/'app.py').read_text()).group(1)),61)
        self.assertGreaterEqual(int(re.search(r'versionCode (\d+)',(ROOT/'android/build.gradle' if False else ROOT/'android/app/build.gradle').read_text()).group(1)),61)
        self.assertRegex((ROOT/'static/sw.js').read_text(),r'kotoba-shell-v100-build\d+')

if __name__ == '__main__': unittest.main()
