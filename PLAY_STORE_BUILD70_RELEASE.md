# Kotoba 1.0.0 — Build 70 Play Store release candidate

Base: Build 69, Golden Thread intro. App package: `com.kotoba.app`.

## Scope and changes

- Preserved all learning content, glass themes, wallpaper behavior, Japan sheets and the Golden Thread intro.
- Incremented `versionCode` and web/service-worker asset cache to **70**. `versionName` remains **1.0.0**.
- Added `.github/workflows/play-release.yml` for a **manual signed AAB** workflow, separate from the debug APK workflow.
- Added `test_release_layout.py` for template-based mobile/tablet/desktop layout checks in both Liquid and Clear Glass states. This checks responsive *structure* but not all dynamic live states.
- Updated old hardcoded build-number test assertions from 69 to 70; no quiz logic or navigation logic changed.

## Verified in the current workspace

- **44 Jinja app templates**, excluding the base template and included fragment, rendered with representative (mock) content and production CSS.
- **352 static visual/layout combinations**: 44 templates × 4 widths (320/390/768/1280) × 2 glass modes. No page-level horizontal overflows or clipped checked headings/controls.
- **54 selected source/unit tests passed.** `node test_liquid_glass.cjs` and all 8 voice-search tests passed.
- **Python syntax compilation**, JavaScript `node --check`, Android XML parsing, and Android/web asset-mirror comparisons passed.
- Full Python discovery saw **81 tests**, with **11 module-import errors** (all require Flask, which is unavailable in this workspace); remaining 70 tests passed. This is a blocked suite, **not** a passing full release test.

## Not yet verified — release gates

- There is **no signed Android App Bundle** in this ZIP. The local environment has no Android SDK or Gradle, and no private upload keystore was supplied.
- Flask-backed functional/smoke tests, full Node/jsdom suites, Gradle lint, build/signature, native 16-KB page compatibility, and a physical device review still need CI/device execution.
- Publisher must confirm Play policy declarations (privacy URL, Data safety, microphone/notifications, content rating, target audience, and rights for images/books/music/data). No Play Console upload has been performed.

## How to build a signed Play Store AAB in GitHub

1. Extract this ZIP **into the root of your GitHub repository** (not as a single nested ZIP) and push to a branch after reviewing the diff.
2. In GitHub **Settings → Secrets and variables → Actions**, create these **repository secrets**:
   - `KOTOBA_UPLOAD_KEYSTORE_BASE64` — Base64 of **your existing Play upload `.jks`** file, all one line. On Linux: `base64 -w0 upload-key.jks`.
   - `KOTOBA_UPLOAD_STORE_PASSWORD` — keystore password.
   - `KOTOBA_UPLOAD_KEY_ALIAS` — upload key alias.
   - `KOTOBA_UPLOAD_KEY_PASSWORD` — alias password.
3. In **Actions → Play Store release AAB → Run workflow**, start the manual workflow. It runs source/unit/DOM/layout tests, package smoke tests, Gradle lint and `bundleRelease`.
4. If all gates pass, download the **`kotoba-build70-signed-play-aab`** artifact from the same workflow run. The `app-release.aab` inside is your signed upload bundle.
5. Use **Google Play Console → Testing → Internal testing → Create new release** first. Upload the AAB, check the pre-launch report, install it on an Android phone, and manually test cold start, Golden Thread intro, both glass modes, JLPT result screens, TTS/microphone, notifications, backups, and Japan sheet scrolling. Promote only after reviewing those checks.

**Do not create or replace the Play upload keystore if a prior version has already been published.** Use the existing keystore (or follow Play's supported upload-key reset process). `versionCode` must be higher than every version already uploaded to Play; adjust it if 70 is already used.

Keystores, passwords, and private learner files are intentionally excluded from source ZIP/artifacts.
