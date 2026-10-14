"""Build 54: opened Explore lessons share a padded glass frame."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent

class ExplorePanelInsets54(unittest.TestCase):
    def test_opened_lesson_surfaces_are_inset(self):
        css = (ROOT/'static/css/liquid-glass.css').read_text()
        self.assertIn('Build 54: consistent inset',css)
        for cls in ('.category-block', '.vocab-section', '.story-body',
                    '.story-quiz', '.convo', '.favorite-list-block'):
            self.assertIn(cls,css)
        self.assertRegex(css,r'\.modal-card\s+\.convo\s*\{\s*padding:')
        self.assertIn('overflow-wrap: anywhere;',css)

    def test_explore_pages_use_shared_surface_styles(self):
        for template, required in {
            'everyday.html':['category-block','modal-card','modal-convo'],
            'verbs.html':['category-block','everyday-row'],
            'kanji_detail.html':['vocab-section','sentence-section'],
            'radical_detail.html':['vocab-section','rad-section'],
            'story_detail.html':['story-body','vocab-section','story-quiz'],
            'conversation_detail.html':['convo-standalone','vocab-section'],
            'grammar_detail.html':['grammar-detail-card'],
            'jlpt_level.html':['kanji-modal','modal-card'],
        }.items():
            text=(ROOT/'templates'/template).read_text()
            for marker in required:
                with self.subTest(template=template,marker=marker):
                    self.assertIn(marker,text)

    def test_release_parity_and_asset_version(self):
        base=ROOT/'android/app/src/main/python/kotoba_app'
        for path in ('static/css/liquid-glass.css','static/sw.js'):
            self.assertEqual((ROOT/path).read_bytes(),(base/path).read_bytes())
        app=(ROOT/'app.py').read_text()
        sw=(ROOT/'static/sw.js').read_text()
        gradle=(ROOT/'android/app/build.gradle').read_text()
        build=re.search(r'ASSET_BUILD = "(\d+)"',app).group(1)
        self.assertGreaterEqual(int(build),54)
        self.assertIn(f'ASSET_BUILD = "{build}"',(base/'app.py').read_text())
        self.assertIn(f'kotoba-shell-v100-build{build}',sw)
        self.assertIn(f'versionCode {build}',gradle)
        self.assertIn("versionName '1.0.0'",gradle)

if __name__=='__main__': unittest.main()
