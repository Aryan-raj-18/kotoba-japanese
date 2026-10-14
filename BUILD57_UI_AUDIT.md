# Kotoba v1.0.0 — Build 57 UI audit

Source base: Build 56. This pass preserves all learning data, route logic, speaking retry, and wallpaper settings.

## Repairs
- Everyday detail popup is more legible over busy wallpapers in Liquid Glass (89% color tint with blur) and Clear Glass (83% color tint without blur); all other panels retain their earlier transparent appearance.
- Corrects stacking: opened word and other `.modal-overlay` panels are raised above the sticky header, not trapped behind the main content's z-index. Retains the existing mobile settings portal logic.
- Ensures the word popup scrolls independently at phone sizes, avoids the first-frame mobile fade flash, resets stale word content while loading, and supports focus trapping, Escape, and focus restoration.
- Adds a glass question/result surface in Learning Games without returning to solid navy options; correct/wrong feedback remains outlined.
- Reserves room for the fixed bottom navigation underneath the mobile footer; protects long Japanese practice text from horizontal clipping.
- Source + Android-bundled files synchronized; app asset cache and Android versionCode changed to 57.

## Executed verification
- 44 templates with representative generated content, inspected at 390, 768, 1366 px in both glass modes in headless Chromium (264 cases). No page-wide horizontal overflow. The 60px passport card scrollWidth excess is caused by its intentionally clipped decorative `::after` circle, not real text.
- 32 focused modal and game-glass style checks (360, 390, 768, 1366 px; Light/Dark; both glass modes): modal fits the viewport, scrollable contents, glass opacity and game selection state checked.
- 8 browser checks of the real Everyday popup JavaScript (four widths × two glass modes): click, load content, scrollability, focus trap, Escape close, focus restoration.
- Four functional Settings-panel browser checks for the real `theme.js` open behavior (mobile body portal, desktop anchored dropdown).
- All locally runnable no-dependency Python unit tests, including new Build 57 regressions, passed. Some full test modules need Flask, which was not installed in this environment and could not be fetched offline.
- CSS brace, JavaScript syntax, Jinja template parsing and Android asset mirrors checked.

## Still requires installed-device release testing
- Actual Chaquopy/Flask server and Android APK build.
- Native speech recognition/audio, background wallpaper images/animations, microphone permission, performance and navigation timing on representative phones.
- All pages populated from the live app API with long/edge-case content; representative template rendering does not prove every possible UI/data state.
