# Kotoba Build 54 — consistent Explore lesson and word panel insets

Build 53 was the source. An expanded, scoped layout correction now adds inner
spacing to all `category-block` (including verbs), `vocab-section` (kanji,
radicals, stories, conversations), `story-body`, `story-quiz`, and `convo`
(including the word-detail popup), as well as the existing favorite list panel.
The existing `rad-section` and `sentence-section` already had glass padding and
are not double-padded. Headings, dividers, word rows and optional long strings
remain inside their glass borders; last rows no longer add dead-bottom margins.

No lesson data, event handlers or learning behaviors were changed. The shared
Liquid/Clear Glass modes remain intact. Desktop Flask and Android embedded app
copies of changed files are kept byte-identical. Asset URL/build and service
worker cache versions advanced to 54, with versionName 1.0.0 unchanged.
