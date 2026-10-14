"""Build 74: runnable without Flask/Android tools; test release packaging invariants."""
import re
import unittest
from pathlib import Path

R=Path(__file__).parent
A=R/'android/app/src/main/python/kotoba_app'

class PlayRelease74(unittest.TestCase):
    def test_release_identity_and_android_api(self):
        source=(R/'app.py').read_text()
        gradle=(R/'android/app/build.gradle').read_text()
        self.assertIn('ASSET_BUILD = "74"',source)
        for token in ('applicationId \'com.kotoba.app\'','versionCode 74',"versionName '1.0.0'",'targetSdk 36'):
            self.assertIn(token,gradle)
    def test_cache_and_mirror(self):
        for path in ('static/sw.js','static/css/liquid-glass.css','static/css/style.css',
                     'static/js/intro.js','templates/base.html','data/roadmap.json'):
            self.assertEqual((R/path).read_bytes(),(A/path).read_bytes(),path)
        self.assertTrue((A/'app.py').read_bytes().startswith((R/'app.py').read_bytes().rstrip()))
        sw=(R/'static/sw.js').read_text()
        self.assertIn('kotoba-shell-v100-build74',sw)
        self.assertIn('?v=74',sw)
    def test_signed_aab_workflow_and_verifier(self):
        flow=(R/'.github/workflows/play-release.yml').read_text()
        for token in ('workflow_dispatch','KOTOBA_UPLOAD_KEYSTORE_BASE64',
                      'KOTOBA_UPLOAD_KEY_ALIAS','KOTOBA_UPLOAD_KEY_PASSWORD',
                      ':app:testDebugUnitTest',':app:lintRelease',':app:bundleRelease',
                      'jarsigner -verify','verify_play_bundle.py',
                      'kotoba-build74-signed-play-aab'):
            self.assertIn(token,flow)
        self.assertTrue((R/'verify_play_bundle.py').is_file())
    def test_only_minimum_permissions_and_no_embedded_signing(self):
        manifest=(R/'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertNotIn('android.permission.READ_SMS',manifest)
        self.assertNotIn('android.permission.MANAGE_EXTERNAL_STORAGE',manifest)
        self.assertNotIn('android:debuggable="true"',manifest)
        self.assertFalse(any((R/'android').rglob('*.jks')))
        self.assertFalse((R/'android/upload-signing.properties').exists())
        self.assertTrue((R/'privacy-policy.html').exists())

if __name__=='__main__':unittest.main()
