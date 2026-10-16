"""Build 73: test state-dependent glass coverage and 20-question UI contracts.

The Chromium interaction checks are documented in BUILD73_GLASS_AND_PRACTICE_FIX.md.
This standard-library suite also runs on the normal offline build machine.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
CSS = (ROOT/'static/css/liquid-glass.css').read_text(encoding='utf-8')

class GlassPractice73(unittest.TestCase):
    def test_critical_quiz_stages_are_re_frosted(self):
        for selector in ('.practice-stage > .stage-panel', '.game-stage',
                         '.exam-practice-stage > .exam-stage-panel',
                         '.stage-panel .quiz-card',
                         '.stage-panel .exam-feedback',
                         '.stage-panel .exam-review-card',
                         '.write-panel .trace-stage'):
            self.assertIn(selector, CSS)

    def test_on_and_off_remain_distinct(self):
        part=CSS[CSS.index('Build 73 — finish consistency'):]
        self.assertIn('[data-glass="on"]',part)
        self.assertIn('[data-glass="off"]',part)
        self.assertIn('86%, transparent',part)
        self.assertIn('23%, transparent',part)
        self.assertIn('backdrop-filter: var(--liquid-blur) !important;',part)

    def test_feedback_and_writing_alignment(self):
        for selector in ('#exam-feedback-note.exam-furigana', '.write-panel .trace-head',
                         '.write-panel .trace-target-meaning','.write-panel .write-output'):
            self.assertIn(selector,CSS)
        self.assertIn('[hidden] { display: none !important; }',CSS)

    def test_quiz_counts_and_modes_not_changed(self):
        for template in ('templates/practice.html','templates/jlpt_practice.html',
                         'templates/jlpt_exam_practice.html','templates/kanji_practice.html'):
            self.assertIn('data-count="20"',(ROOT/template).read_text(),template)
        html=(ROOT/'templates/practice.html').read_text()
        for mode in ('kanji','sentence','mixed'):
            self.assertIn(f'data-mode="{mode}"',html)

    def test_android_web_css_parity_and_version(self):
        android=ROOT/'android/app/src/main/python/kotoba_app'
        self.assertEqual((ROOT/'static/css/liquid-glass.css').read_bytes(),
                         (android/'static/css/liquid-glass.css').read_bytes())
        self.assertEqual((ROOT/'static/sw.js').read_bytes(),
                         (android/'static/sw.js').read_bytes())
        self.assertIn('ASSET_BUILD = "77"',(ROOT/'app.py').read_text())
        self.assertIn('versionCode 77',(ROOT/'android/app/build.gradle').read_text())
        self.assertIn('build77',(ROOT/'static/sw.js').read_text())

if __name__=='__main__':unittest.main()
