"""Regression guards for the completed JLPT/Kanji answer table and release cache."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MIRROR=ROOT/'android/app/src/main/python/kotoba_app'

class JLPTResults59(unittest.TestCase):
    def test_quiz_really_renders_results_with_expected_ids_and_classes(self):
        for path in ('templates/jlpt_practice.html','templates/kanji_practice.html'):
            text=(ROOT/path).read_text(encoding='utf-8')
            for id_ in ('mcq-stage','mcq-panel-results','mcq-review'):
                self.assertIn(f'id="{id_}"',text)
        for path in ('static/js/jlpt_practice.js','static/js/kanji_practice.js'):
            text=(ROOT/path).read_text(encoding='utf-8')
            for cls in ('mcq-review-row','mcq-review-kanji','mcq-review-body','mcq-review-mark'):
                self.assertIn(cls,text)

    def test_results_glass_and_alignment_are_targeted_at_real_result_screen(self):
        css=(ROOT/'static/css/liquid-glass.css').read_text(encoding='utf-8')
        self.assertIn('#mcq-stage #mcq-panel-results',css)
        self.assertIn('#mcq-panel-results .mcq-review-row',css)
        self.assertIn('background-color:var(--liquid-panel-strong) !important;',css)
        self.assertIn('background-color:var(--liquid-panel) !important;',css)
        self.assertIn('-webkit-backdrop-filter:var(--liquid-blur) !important;',css)
        self.assertIn('grid-template-columns:40px minmax(0,1fr) 22px;',css)
        self.assertIn('grid-column:3;grid-row:1;',css)
        self.assertIn('#exam-panel-results,#mock-results',css)

    def test_new_cache_and_native_version_are_consistent(self):
        app=(ROOT/'app.py').read_text(encoding='utf-8')
        android_app=(MIRROR/'app.py').read_text(encoding='utf-8')
        build=re.search(r'ASSET_BUILD = "(\d+)"',app).group(1)
        self.assertGreaterEqual(int(build),59)
        self.assertIn(f'ASSET_BUILD = "{build}"',android_app)
        sw=(ROOT/'static/sw.js').read_text(encoding='utf-8')
        self.assertIn(f'kotoba-shell-v100-build{build}',sw)
        self.assertIn(f'.map(path => path + "?v={build}")',sw)
        self.assertIn(f'versionCode {build}',(ROOT/'android/app/build.gradle').read_text())
        for file in ('static/css/style.css','static/css/liquid-glass.css','static/sw.js'):
            self.assertEqual((ROOT/file).read_bytes(),(MIRROR/file).read_bytes())

if __name__=='__main__':unittest.main()
