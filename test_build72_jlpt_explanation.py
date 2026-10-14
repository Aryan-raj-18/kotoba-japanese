"""Regression checks for the N5–N1 JLPT Exam Q&A answer/explanation layout."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANDROID = ROOT / 'android/app/src/main/python/kotoba_app'

class JLPTExplanation72(unittest.TestCase):
    def test_all_jlpt_levels_have_explanations_with_readings(self):
        data = json.loads((ROOT / 'data/jlpt_exam_questions.json').read_text(encoding='utf-8'))
        for level in ('N5', 'N4', 'N3', 'N2', 'N1'):
            with self.subTest(level=level):
                self.assertTrue(any(q.get('explanation_blocks') for q in data[level]))

    def test_same_renderer_powers_feedback_and_final_review(self):
        js = (ROOT / 'static/js/jlpt_exam_practice.js').read_text(encoding='utf-8')
        self.assertIn('renderExplanation(feedbackExplanation, q.explanation_blocks, q.explanation)', js)
        self.assertIn('renderExplanation(explanation, answer.explanationBlocks, answer.explanation)', js)
        self.assertIn("p.lang = 'ja';", js)
        self.assertIn("ruby.setAttribute('lang', 'ja')", js)

    def test_reading_insets_and_furigana_spacing_cover_both_views(self):
        css = (ROOT / 'static/css/liquid-glass.css').read_text(encoding='utf-8')
        for rule in (
            '#exam-feedback-note.exam-furigana',
            '#exam-review .exam-review-explanation.exam-furigana',
            '#exam-feedback-explanation',
            '.exam-explanation-line',
            '#exam-panel-quiz .exam-feedback',
            "[data-glass=\"on\"]",
            "[data-glass=\"off\"]",
            'ruby-position: over',
            'line-height: 2.55',
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, css)

    def test_native_asset_and_cache_mirrors(self):
        web = (ROOT / 'app.py').read_text(encoding='utf-8')
        version = re.search(r'ASSET_BUILD = "(\d+)"', web).group(1)
        self.assertGreaterEqual(int(version), 72)
        self.assertIn(f'ASSET_BUILD = "{version}"', (ANDROID / 'app.py').read_text(encoding='utf-8'))
        self.assertIn(f'versionCode {version}', (ROOT / 'android/app/build.gradle').read_text(encoding='utf-8'))
        sw = (ROOT / 'static/sw.js').read_text(encoding='utf-8')
        self.assertIn(f'build{version}', sw)
        self.assertIn(f'?v={version}', sw)
        for name in ('static/css/liquid-glass.css', 'static/js/jlpt_exam_practice.js', 'static/sw.js'):
            self.assertEqual((ROOT / name).read_bytes(), (ANDROID / name).read_bytes())

if __name__ == '__main__':
    unittest.main()
