# Kotoba Build 72 — JLPT N5–N1 Explanation Alignment

Base: Build 71 Japan Explorer heading fix.

## Fixed
- JLPT Exam Q&A explanation after selecting an answer no longer starts flush against the glass border.
- Correct-answer text and the Japanese sentence/reading have consistent left alignment and inner padding.
- Furigana remains above the matching kanji with larger reading text and more line spacing.
- Each explanatory block has comfortable separation (including multi-line N4 and N1 explanations).
- Final Exam Q&A review uses the same readable sentence/reading layout.
- The explanation inset retains Liquid Glass/Transparent Glass and avoids stacking another blur over the text.
- Language metadata applied to Japanese ruby text and paragraph blocks.
- Android mirrored JS/CSS files updated, plus asset cache and Android version code moved to 72.

## Verified
- 40 Chromium runs of the actual JLPT Exam Q&A client script, across N5–N1, at 320, 390, 768 and 1280 px widths, Light/Dark appearances, and both glass modes. Every run selected a wrong option, opened sentence-and-reading feedback, and reached the final review, with no detected page-level horizontal overflow or explanation text exceeding the feedback box.
- 20 targeted Python regression tests passed, including source / Android mirror and prior Japan Explorer / intro tests.
- JavaScript syntax and Python source compilation passed.

## Not verified
- Physical Android WebView/APK and signed Play Store AAB; those require a device and release CI with the configured signing key.
- Full Flask-dependent integration tests, since Flask is unavailable in this execution environment.
