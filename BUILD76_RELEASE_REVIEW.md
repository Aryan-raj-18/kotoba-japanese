# Kotoba 1.0.0 / Build 76

Expanded Japan Explorer now moves its existing map outside frosted ancestors so the map fills the viewport and its controls stay accessible. Zoom buttons, wheel, keyboard, dragging, touch pinch, labels, prefecture details and Back/Escape are covered by live browser regression checks. Closing restores the map to its original page position and restores background interaction.

Glass ON uses stronger frosted surfaces on active practice, exam, roadmap, map, story and settings panes. Glass OFF keeps clear tinted surfaces without backdrop blur. Reduced transparency and lightweight rendering use readable solid surfaces. Shared layout guards wrap long questions and answers and let study cards grow with their content.

The original fonts, logo, learning data and features remain. A 1.3 KB OFL-licensed serif fallback supplies three radical components and the fullwidth quiz blank which were absent from the main Japanese font. It is bundled and precached for offline use. All Japanese glyphs in the 23 public course JSON files are checked against the actual fallback font chain.

Validation before release:
- 32 release regression suites.
- 199 Python unit tests.
- 352 static responsive/glass combinations.
- 141 live rendered pages (47 routes at 320, 390 and 1280 px), active N5–N1 quizzes/exams, mock answer changes/results, learning, review, flashcards, speaking and five games.
- Glass switch persistence in Light/Dark, ON/OFF and reduced-transparency fallback; real Chromium touch pinch and expanded map controls.
- Android source smoke test including 6,974 GET requests.

The release workflow rebuilds generated search caches and the Android mirror, runs these checks, builds signed AAB/APK outputs, runs Android unit tests and release lint, checks both certificates/versions, bundletool validation, 16 KB ELF/APK alignment, identical APK/AAB code and Python payloads, and compares every packaged asset/compiled module with the synchronized source. It reruns regressions against the extracted release package.

Generated search caches are rebuilt by `sync_android.py` before every Android build. The signed artifacts and CI reports, rather than a cached file in the source tree, are the release evidence.

Physical Android install/upgrade, vendor-specific notification/lockscreen behaviour and Play Console internal testing/review remain separate device/platform checks. The workflow does not publish to production.
