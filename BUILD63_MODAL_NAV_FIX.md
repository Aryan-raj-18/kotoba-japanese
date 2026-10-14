# Build 63 — popup / bottom-bar overlap
- Tapping a Hiragana/Katakana tile (and Kanji, Verb popups) left the bottom navigation drawn over the popup and dimmed page. The popups sit inside the page layer, below the fixed bar, so z-index could not help.
- scroll-lock.js now toggles `body.kotoba-sheet-open` while any `.modal-overlay` is visible; CSS hides the bottom bar then and restores it on close.
- The popup close button is a round 40px glass control instead of a square patch.
- ASSET_BUILD/versionCode 63, cache build63, Android mirror synced. Test: test_build63_modal_nav.py.
