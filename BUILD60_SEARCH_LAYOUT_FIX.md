# Build 60 — Header, Kanji, JLPT & Verbs search layout

Base: Build 59.

- **Top navigation:** Removed redundant in-field microphone; the separate top-bar microphone still provides voice search. Shortened the placeholder and separated the submit icon from the text area.
- **Kanji / JLPT levels / Verbs:** Wrapped each filter in a deliberately sized search container, with a microphone in its own adjacent 46-pixel-wide control. The voice button no longer overlaps entered text or placeholder text.
- **Both glass modes:** Search borders, tints and focus styling inherit the active glass appearance; Clear Glass has no blur; Liquid Glass follows the existing finish.
- **Small screens:** Filter widths are bounded by their parent and collapse to the available space; the Kanji visible-count stays on its own row if necessary.
- Preserved the filtering IDs/JS handlers, microphone behavior, and all learning content.
- Updated service-worker cache and Android `versionCode` to 60; synchronized web source and Android-packaged files.

Tests: see `test_build60_search_layout.py`. Android APK not compiled or device-tested in this environment.
