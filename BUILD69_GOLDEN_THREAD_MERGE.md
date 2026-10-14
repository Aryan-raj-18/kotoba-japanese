# Build 69 — Golden Thread intro added to Build 68

Source base: user-provided `kotoba-japanese-app-build68-japan-sheet-glass-plane-fix.zip`.

- **Replaces** (does not stack) the old train, petals, and Japan-map intro with Golden Thread in the shared web Home and Android pre-server startup. Obsolete old-intro CSS selectors/keyframes are removed.
- Adds the original circular Kotoba mark, soft gold SVG thread, and tagline “Your Japanese journey starts here.”
- Keeps Skip and reduced-motion behavior and the 3-second startup timeline. Uses a fresh Golden Thread session key so the new opening plays once after upgrade, not again on each return to Home.
- Syncs the intro to Android startup before its Flask server is ready. Native startup waits up to 3 seconds before Home unless the user skips.
- Rotates `ASSET_BUILD`, service worker cache and Android `versionCode` to 69; mirrors updated web assets into Android.
- Preserves Build 68's Japan sheet and glass-plane changes and its learning data.

Checks cover file integrity, cache IDs, Android mirror, HTML static parsing and script tests. Android APK compilation and on-device playback remain to be verified on GitHub Actions / device.

## Verification
- 10 targeted Python source checks passed.
- Real Chromium native-opening checks passed at 390, 768 and 1280 px in both glass modes.
- Chromium checks passed for Native Skip, centered logo, flowing SVG thread, absent old-intro elements, and once-per-session web playback.
- Node `jsdom` suite could not run locally because jsdom is unavailable. APK compilation/device playback were not run.
