"""Focused no-network guards for Build 57 mobile overlays and glass modes."""
from pathlib import Path
import re
import unittest
from test_android_mirror_helpers import expected_native

ROOT=Path(__file__).resolve().parent
MIRROR=ROOT/'android/app/src/main/python/kotoba_app'

class InterfaceAudit57(unittest.TestCase):
    def test_word_overlay_is_scrollable_and_protected_against_wallpaper_bleed(self):
        css=(ROOT/'static/css/liquid-glass.css').read_text()
        self.assertIn('#word-modal-card.word-detail-modal',css)
        self.assertIn('var(--card-bg) 89%',css)
        self.assertIn('var(--card-bg) 83%',css)
        self.assertIn('overscroll-behavior:contain',css)
        self.assertIn('animation:none !important;',css)
        tmpl=(ROOT/'templates/everyday.html').read_text()
        self.assertIn('aria-modal="true"',tmpl)
    def test_word_detail_has_keyboard_trap_and_safe_focus_restore(self):
        js=(ROOT/'static/js/everyday.js').read_text()
        self.assertIn("if (e.key !== 'Tab') return;",js)
        self.assertIn('returnFocus.focus({preventScroll:true})',js)
        self.assertIn('modal.scrollTop=0',js)
        self.assertIn("modal.setAttribute('aria-hidden','true')",js)
    def test_game_question_and_mobile_footer_have_panes(self):
        css=(ROOT/'static/css/liquid-glass.css').read_text()
        self.assertIn('#game-board > :is(.game-question,.game-finish)',css)
        self.assertIn('padding-bottom:calc(112px + env(safe-area-inset-bottom, 0px))',css)
    def test_android_copy_and_service_worker_version(self):
        for file in ('app.py','templates/everyday.html','static/js/everyday.js','static/css/liquid-glass.css','static/sw.js'):
            with self.subTest(file=file): self.assertEqual(expected_native(ROOT,file),(MIRROR/file).read_bytes())
        build = re.search(r'ASSET_BUILD = "(\d+)"',(ROOT/'app.py').read_text()).group(1)
        self.assertGreaterEqual(int(build),57)
        self.assertIn(f'versionCode {build}',(ROOT/'android/app/build.gradle').read_text())
        self.assertIn(f'kotoba-shell-v100-build{build}',(ROOT/'static/sw.js').read_text())

if __name__=='__main__':unittest.main()
