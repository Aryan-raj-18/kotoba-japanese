# Kotoba 1.0.0 — Build 52 Glass Mode Fix

This is a visual-only correction of Build 51. The app's routes, learning content,
progress, and exercises are unchanged. Android `versionName` remains `1.0.0`.

## What changed

- Fixed `journey.css`/`ui-shell.css` shell variables that still resolved to
  opaque `--card-bg` surfaces in the **Liquid Glass ON** state.
- Tuned the two distinct appearance states: **ON** uses translucent theme-tinted
  panels with native backdrop blur, while **OFF / Clear Glass** shows the user
  wallpaper behind unblurred, lightly tinted cards and controls.
- Applied missing glass styling to Roadmap stage navigation, Writing Practice
  tracing pads and nested panels, kana cards, Everyday Life rows, Radicals
  example rows, dialogs, and other shared cards across the app.
- Removed stacking opacity/blur on child tiles so the parent panel does not
  appear solid or paint rectangular GPU overlays.
- Restored translucent modal dialogs in Clear mode while retaining additional
  tint for text readability; keeps settings dropdown solid for legibility.
- Added older-WebView theme fallbacks for cases without `color-mix()`.
- Increased asset/cache build marker to **52**, service worker cache to
  `kotoba-shell-v100-build52`, and Android `versionCode` to **52** so old
  glass styles are not reused after installation. The public version name
  remains **1.0.0**.
- Synced changed web runtime files to the Android-packaged Python app.

## Verification

- Existing CSS/Android mirror regressions: 21 tests passed.
- New Build 52 no-dependency regression checks: 4 tests passed.
- Existing Node Liquid Glass preference/toggle test: passed.
- Chromium style rendering with the actual project CSS and controller:
  Light and Dark, 1280px desktop and 390px mobile. Each mode tested across
  13 representative panels (including modals), blur behavior, opacity,
  and on/off/on toggle round-trip: passed. See `verification/build52-glass-browser.json`.

The Chromium tests use representative DOM with the app's real CSS/JS, **not** a
full Flask live-site or Android-device run. After building the APK, verify on a
physical device (including wallpaper, settings, and the listed screens).

## Running tests

```bash
python -m unittest test_clear_glass_build52 test_glass_coverage \
    test_glass_surface_41 test_glass_artifacts_42 \
    test_water_glass_build43 test_glass_integration test_responsive_shell
node test_liquid_glass.cjs
```
