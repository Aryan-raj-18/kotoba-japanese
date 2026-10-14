# Kotoba 1.0.0 — Build 74 · Google Play signed AAB handoff

**Release status: SOURCE RELEASE CANDIDATE. This project is not yet a signed App Bundle, nor has it been published to Google Play.**

## Package identity

- Android application ID: `com.kotoba.app`
- Display version: `1.0.0`
- Android versionCode: `74` (must be higher than every versionCode already uploaded for this Play app)
- minSdk: 24; targetSdk / compileSdk: 36
- Publishing format: **signed `.aab`**, built by `.github/workflows/play-release.yml`
- Signing: supplied privately as GitHub Actions secrets; no keystore is included in the ZIP

## What changed versus Build 73

1. Incremented app and Android asset-cache build identifiers to 74, including the mirrored Android web bundle.
2. Updated the existing Play Store release workflow artifact names to Build 74, and added Android unit-test and full Python unittest discovery gates.
3. Added a signed AAB archive/native ELF 16 KiB page-alignment check (`verify_play_bundle.py`). It also records a SHA-256 hash and fails on malformed bundles. Device/Play split compatibility still needs separate verification.
4. Updated old tests that expected the literal Build 73 identifier, without weakening their UI-coverage assertions.
5. Added a focused Build 74 packaging/source-verification test.

The UI, curriculum, Golden Thread opening, JLPT exams, and Liquid/Clear Glass code remain unchanged.

## Generate the AAB on GitHub Actions

1. Extract this ZIP into the **root** of your GitHub repository, so `.github/workflows/play-release.yml` is at the repository root (not inside an extra nested folder). Commit and push the project files, **not the ZIP archive**.
2. Go to **GitHub → Settings → Secrets and variables → Actions → New repository secret**. Create these exact four secrets:

   - `KOTOBA_UPLOAD_KEYSTORE_BASE64`: Base64 of your upload `.jks` file, on one line. On Ubuntu, run `base64 -w 0 /path/to/upload-key.jks` locally; copy the value into the GitHub secret. Don't paste it into chat.
   - `KOTOBA_UPLOAD_STORE_PASSWORD`: password for the upload keystore.
   - `KOTOBA_UPLOAD_KEY_ALIAS`: signing-key alias.
   - `KOTOBA_UPLOAD_KEY_PASSWORD`: password for the signing key.

3. **If this Google Play app already has an upload key, reuse that exact key.** Do not make a new key simply because this is a new Build 74 ZIP. If this is truly a brand-new app with no signing key, generate your first upload key privately using Android Studio or locally with `keytool -genkeypair -v -keystore upload-key.jks -alias kotoba-upload -keyalg RSA -keysize 4096 -validity 10000`; store your encrypted backup somewhere safe. Never commit that key to GitHub.
4. Open **GitHub → Actions → Play Store release AAB → Run workflow** on the branch containing Build 74. The workflow will run Python, JavaScript/jsdom, browser/layout and Android tests, run Android lint, build a release App Bundle, validate it and sign it with your upload key.
5. If the workflow is green, open its Artifacts and download **`kotoba-build74-signed-play-aab`**. Extract the artifact and locate `app-release.aab`. The GitHub artifact is the build output; this project ZIP is only source code.
6. If it fails, copy the **first actionable error and the failing step log**, not just GitHub's red failure summary. Do not publish until the actual AAB is verified.

## Play Console — required publisher steps

1. Confirm the chosen app ID `com.kotoba.app` and that 74 is higher than every versionCode previously uploaded. If your Play listing already uses a *different* application ID, changing a shipped package name needs care and usually a new listing.
2. Prepare an accessible **public HTTPS privacy policy URL** and accurate Data safety declarations for local progress, optional cloud sync and its service providers, voice recognition (which may use system services), and notifications. A bundled offline privacy HTML page is **not** an external privacy policy URL.
3. Check image, map, books, generated content, fonts and audio licensing. In particular, use only wallpapers, screenshots, and source assets you are authorized to distribute. A user's custom wallpaper is not necessarily licensed as an app marketing screenshot.
4. Complete the store listing (name, description, icon, graphics, device screenshots), content rating, app access, audience and permission disclosures.
5. Upload the signed AAB to **Internal testing** first. Review automated pre-launch results and install the resulting Play delivery on real Android devices. Test Golden Thread cold start/Skip, Light/Dark, both glass modes, N5–N1 exam feedback and 20-question rounds, audio and speech, offline startup, search, scrolling and keyboard overlap, notifications, Japan Explorer, and saving/restoring progress.
6. If Google Play requires closed testing for your newly created personal developer account, meet the current tester-duration requirement before requesting production access. Roll out gradually after review.

## Test evidence obtained in this workspace

- 44 Jinja templates × four widths × two glass states = **352 static browser layout checks passed**; zero page-wide overflows in the representative rendered templates.
- Python unittest discovery: 97 tests discovered, **86 passed**, **11 blocked by missing Flask** in this workspace; those 11 must be run on the GitHub runner.
- JavaScript syntax check, voice-search eight cases and Liquid Glass source check passed.
- Build 74 source/package checks passed; Android web CSS and app-file prefix are synchronized.
- Not performed here: full Flask integration suite, Gradle unit tests, release lint, actual signed AAB, APK split extraction, physical Android phone tests, or Play Console submission.

**Never upload your keystore, passwords or signing secrets in chat or commit them to a repository.**
