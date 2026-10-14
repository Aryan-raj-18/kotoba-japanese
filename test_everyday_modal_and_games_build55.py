from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent

class EverydayModalAndGames55(unittest.TestCase):
    def test_everyday_search_removed_and_filter_optional(self):
        html = (ROOT/'templates/everyday.html').read_text(encoding='utf-8')
        js = (ROOT/'static/js/everyday.js').read_text(encoding='utf-8')
        self.assertNotIn('id="everyday-filter"', html)
        self.assertIn("const q=(filterInput?.value||'').trim()", js)
        self.assertIn("if(filterInput)filterInput.addEventListener('input',applyFilters);", js)

    def test_word_modal_mobile_scroll_and_game_glass_rules(self):
        style = (ROOT/'static/css/style.css').read_text(encoding='utf-8')
        glass = (ROOT/'static/css/liquid-glass.css').read_text(encoding='utf-8')
        self.assertIn('body.word-modal-open .kotoba-bottom-nav { display: none !important; }', style)
        self.assertIn('#word-modal.is-open', style)
        self.assertIn('#word-modal-card.word-detail-modal', style)
        self.assertIn('Build 55: mobile Everyday modal', glass)
        self.assertIn(':is(.game-stage,.game-question,.match-tile,.mcq-options .quiz-option)', glass)

    def test_release_versions_and_android_parity(self):
        app = (ROOT/'app.py').read_text(encoding='utf-8')
        android_app = (ROOT/'android/app/src/main/python/kotoba_app/app.py').read_text(encoding='utf-8')
        sw = (ROOT/'static/sw.js').read_text(encoding='utf-8')
        gradle = (ROOT/'android/app/build.gradle').read_text(encoding='utf-8')
        build=re.search(r'ASSET_BUILD = "(\d+)"',app).group(1)
        self.assertGreaterEqual(int(build),55)
        self.assertIn(f'ASSET_BUILD = "{build}"',android_app)
        self.assertIn(f'kotoba-shell-v100-build{build}',sw)
        self.assertIn(f'versionCode {build}',gradle)

if __name__ == '__main__':
    unittest.main()
