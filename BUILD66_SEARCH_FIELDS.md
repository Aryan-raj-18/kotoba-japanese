# Build 66 — grammar dictionary (and sibling) search fields
- Grammar Dictionary, Radicals filter, Write > kanji picker and Japan Explorer search had a bare input; the voice script wrapped it in an auto field whose mic was pinned to the far edge of the container (Grammar: input 420px wide, mic ~513px to its right; on phones a few px off-centre).
- These inputs are now wrapped like the Kanji/Verbs/JLPT fields: text + mic in one glass field, mic vertically centred.
- voice-search.js: auto-wrapped `.filter-input` fields also get the catalog field style (safety net); inputs with `data-no-voice` get no mic (Favorites "New list name" is not a search).
- Grammar level buttons: spaced under the field and left-aligned with it.
- Long placeholders shortened so they are not cut off beside the mic on phones.
- Build 66; Android mirror synced. Test: test_build66_search_fields.py.
