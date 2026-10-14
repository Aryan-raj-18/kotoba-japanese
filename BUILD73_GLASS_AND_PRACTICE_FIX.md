# Kotoba 1.0.0 — Build 73

Base: Build 72, including the previous Japan Explorer and JLPT furigana fixes.

## Root cause and fix

The Liquid Glass shell deliberately made some active `.stage-panel` components transparent whenever they contained quiz cards. Another earlier rule reduced the nested quiz card to a 16% opaque tint and removed its backdrop blur. Together those rules made active quizzes and their explanation cards appear to be Clear Glass even when Liquid Glass was enabled.

Build 73 restores a **single blurred glass surface** on the real active panel and applies a stronger, non-blurring inset tint on its inner questions, answer choices, explanations, and review cards. It avoids stacking 20–60 GPU blurs on answer rows.

- Active stages: JLPT N5–N1 Exam Q&A, JLPT Kanji meaning, general Kanji meaning, 20-word Practice (Kanji, Sentence, Mixed), games, Daily Review and speaking.
- Readable panels: dashboard/stat tiles, Japan Explorer hero, review cards, search results, practice explanations and solved-answer feedback.
- Liquid Glass **ON** is now substantially more frosted; Clear Glass **OFF** remains see-through and unblurred.
- Writing Practice: inner padding, Japanese character labels, character counter, controls, keyboard row and output wrapping corrected.
- The JLPT furigana explanation and end-of-round review styling from Build 72 is preserved.
- Invisible `[hidden]` feedback elements retain their actual hidden state.

## Verification

- Local Chromium fixture checks rendered the actual Jinja2 templates, with mocked learning APIs because Flask/Android builds are unavailable in the container. On/off and mobile examples were visually inspected.
- Simulated 20-question completion: JLPT Kanji and general Kanji show 20 review rows; N3 Exam Q&A reaches 20-question results; Kanji, Sentence and Mixed practice each reach 20 out of 20 with mocked correct-answer data. These prove UI traversal with stubbed API responses; **not** server question-bank sampling or actual learner-score accuracy.
- Source unit tests cover stage glass selectors, both modes, counts, writing alignment, Android parity and build/cache version.
- No changes to learning content datasets or scoring implementation.

## Outstanding checks

Full Flask server test suite, Android WebView rendering, and signed Play Store AAB must be verified on a configured build runner and a real device before release. The user-selected wallpaper, its scrim/dim amount, and device font scale may affect legibility.
