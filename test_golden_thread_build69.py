"""Golden Thread UI / native source gate checks (no Flask dependency)."""
import re, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
APK=ROOT/'android/app/src/main/python/kotoba_app'

class GoldenThread(unittest.TestCase):
    def test_markup_and_copy(self):
        text=(ROOT/'templates/base.html').read_text()
        assert 'kotoba-golden-thread' in text
        intro=text[text.index('<div class="kotoba-intro'):text.index('\n{% endif %}',text.index('<div class="kotoba-intro'))]
        self.assertIn('Your Japanese journey starts here.',intro)
        self.assertIn('kotoba-logo-circle.png',intro)
        self.assertIn('kotoba-thread-line',intro)
        self.assertNotIn('kotoba-intro-map',intro)
        self.assertNotIn('kotoba-intro-orbit',intro)
    def test_css_timeline_and_reduced_motion(self):
        css=(ROOT/'static/css/ui-shell.css').read_text()
        for k in ('golden-thread-draw','golden-progress 3s','prefers-reduced-motion:reduce','kotoba-thread-divider', 'background:transparent !important'):
            self.assertIn(k,css)
        self.assertTrue((ROOT/'static/icons/kotoba-logo-circle.png').is_file())
    def test_native_intro_asset_generated_and_embedded(self):
        html=(ROOT/'android/app/src/main/assets/kotoba-opening.html').read_text()
        self.assertIn('Your Japanese journey starts here.',html)
        self.assertIn('kotoba-golden-thread',html)
        self.assertIn('data:image/png;base64',html)
        self.assertNotIn("{{ url_for",html)
        self.assertIn('KotobaStartupNative.skipIntro()',html)
    def test_android_gate_not_skipping_three_seconds(self):
        s=(ROOT/'android/app/src/main/java/com/kotoba/app/MainActivity.kt').read_text()
        for needle in ('introDurationMs = 3_000L','scheduleLessonsAfterIntro(generation)', 'introDurationMs - elapsed','lessonTransitionQueued','introSkipped'):
            self.assertIn(needle,s)
        self.assertEqual(s.count('webView.loadUrl(serverUrl + "__bootstrap?token=" + nativeSessionToken)'),1)
    def test_versions_and_mirrors(self):
        app=(ROOT/'app.py').read_text()
        self.assertIn('ASSET_BUILD = "74"',app)
        self.assertIn('versionCode 74',(ROOT/'android/app/build.gradle').read_text())
        sw=(ROOT/'static/sw.js').read_text()
        self.assertIn('build74',sw)
        self.assertIn('?v=74',sw)
        for rel in ('templates/base.html','static/css/ui-shell.css','static/sw.js','static/icons/kotoba-logo-circle.png'):
            self.assertEqual((ROOT/rel).read_bytes(),(APK/rel).read_bytes())

if __name__=='__main__':unittest.main()
