# Build 65 — result screens of tests, practice and timed tests
- Exam Q&A results: the "Review the missed questions…" note was a 52ch block hugging the left of a centred card; now centred (same fix for kanji quiz, mock, placement and sentence-practice result panels).
- Placement result: "Start here" was an inline link, so its margins never applied and it touched the text above; now a block-level button with clear spacing.
- Timed mock results: with 5 score tiles in 2 columns on phones the last tile dangled; it now spans the row. Tile text centred.
- Review cards: consistent padding, left-aligned text, long strings wrap inside the box.
- Flows driven to the final screen at desktop and phone width: kanji quiz, JLPT practice, Exam Q&A, timed mock, placement; no edge-touching or overflow findings remain.
- Build 65; Android mirror synced. Test: test_build65_result_alignment.py.
