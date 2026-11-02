"""Build 62: mic inside search bar, nav/mock alignment, answered-state glass."""
from pathlib import Path
import re, unittest
ROOT = Path(__file__).resolve().parent
ANDROID = ROOT / 'android/app/src/main/python/kotoba_app'

class Build62(unittest.TestCase):
    def test_mic_inside_header_search_form(self):
        html = (ROOT/'templates/base.html').read_text('utf-8')
        form = html.split('<form class="header-search"',1)[1].split('</form>',1)[0]
        self.assertIn('id="voice-search-global"', form)
        self.assertLess(form.index('voice-search-global'), form.index('type="submit"'))
        self.assertIn('voice-outside-search', html)
    def test_voice_js_binds_all_global_buttons(self):
        js = (ROOT/'static/js/voice-search.js').read_text('utf-8')
        self.assertIn('[data-voice-global]', js)
    def test_css_rules(self):
        css = (ROOT/'static/css/liquid-glass.css').read_text('utf-8')
        for needle in ('.header-search > .voice-search-global-btn', '.hero-search .voice-field > .voice-inline-btn',
                       '.mock-toolbar > #mock-timer', 'white-space: nowrap', '.mcq-review-row.right', '.reaction-card'):
            self.assertIn(needle, css)
    def test_bottom_nav_single_active(self):
        js = (ROOT/'static/js/ui-shell.js').read_text('utf-8')
        self.assertIn('matchLength', js)
    def test_android_mirror(self):
        for f in ('templates/base.html','static/css/liquid-glass.css','static/js/voice-search.js','static/js/ui-shell.js','static/sw.js'):
            self.assertEqual((ROOT/f).read_bytes(), (ANDROID/f).read_bytes(), f)
        self.assertEqual(re.search(r'ASSET_BUILD = "(\d+)"',(ROOT/'app.py').read_text()).group(1),'78')
        self.assertIn('versionCode 78',(ROOT/'android/app/build.gradle').read_text())
        self.assertIn('build78',(ROOT/'static/sw.js').read_text())
if __name__ == '__main__': unittest.main()
