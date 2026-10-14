# Build 62 — mic placement, alignment, answered-state glass

- Header: microphone moved INSIDE the search bar (text | mic | search). Phones, where the bar is hidden, get a twin mic beside the other header controls (`data-voice-global`).
- Home quick-search and Search page: mic is its own flex cell in one glass container; placeholder no longer clipped; search page form widened.
- Top nav: every link shares one box/baseline; header fits one row on desktop.
- Timed mock: toolbar is a grid; the clock no longer wraps.
- Bottom nav: only the most specific tab is active (/kanji/practice = Review only).
- Practice: selected = gold, correct = green, wrong = red translucent glass; post-round review rows, exam feedback and the mascot popup use the same glass finish.
- Version: ASSET_BUILD/versionCode 62, service-worker cache build62; Android mirror synced.

Tests: test_build62_mic_alignment_glass.py (+ build 60/61 pins relaxed to >=). Android APK not compiled or device-tested here.
