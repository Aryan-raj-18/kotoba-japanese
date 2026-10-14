# Kotoba v1.0.0 — Build 59: Completed JLPT test results

## Why Build 58 could show no visible change

The previous ZIP still had `ASSET_BUILD = "57"`, Android `versionCode 57`, and the old service-worker cache key `kotoba-shell-v100-build57`. An existing browser/app could therefore reuse CSS cached by an older build. Build 59 changes all three identifiers consistently.

## Actual quiz screen fixed

The affected page is **JLPT > N5/N4/N3/N2/N1 > Kanji Practice > Start test > answer every question > Test complete**. This result table is populated by `static/js/jlpt_practice.js` in `#mcq-panel-results` using `.mcq-review-row` elements. The general Kanji Practice page uses the same markup and is fixed too.

- The outer completed-results panel is one Liquid Glass surface with a frosted backdrop when the setting is ON.
- When Liquid Glass is OFF, that same panel switches to Clear Glass, without blur and with a more transparent tint.
- The per-answer rows are lightweight translucent inset cards to avoid creating dozens of GPU blur layers on long tests.
- The result table now fills the available panel width; Japanese glyphs, multi-line English answers and right/wrong marks have three stable columns. The 3-column structure remains intact on narrow phones.
- JLPT Exam Q&A and timed-mock final review surfaces inherit matching glass styling.
- N5–N1 use the same tested result page and renderer; no quiz logic or learning content changed.

## Verification

- Actual Jinja result template and `jlpt_practice.js` were exercised in Chromium with a simulated 20-question quiz (clicked through all answers) at 390, 768 and 1280 CSS-pixel widths, in both glass settings.
- All 20 answer rows rendered; correct/wrong markers remained in their columns; no horizontal overflow in tested layouts.
- In Dark appearance: ON review-row tint alpha 0.36 and panel blur 18px; OFF row alpha 0.17 and panel no blur. Light appearance was also checked.
- CSS, app build identifier, service-worker cache and Android mirrored assets checked for agreement.

Tests used a browser fixture with controlled sample questions, not a complete installed Android app. APK build and phone-specific checks are still required.
