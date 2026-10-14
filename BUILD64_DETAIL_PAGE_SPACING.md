# Build 64 — detail-page bullets, box padding and spacing
- Kanji "How to read": bullets were drawn outside the box (a glass rule replaced the list's left padding). The list now has room for its markers; bullets sit inside the box, and entries/examples are spaced.
- "Commonly used" note had ~1px padding; now padded and rounded properly.
- Radical build / origin / tip boxes, radical example rows, vocabulary rows: consistent padding and gaps; rows no longer touch each other; vocabulary reading + speaker button vertically centred.
- All card sections (radical, vocabulary, sentence, stories, conversations) share one inner padding so headings line up with their rows.
- A layout audit (bullets outside boxes, text touching box edges, overflow, horizontal scroll) was run over ~45 pages at desktop and phone width; the real findings on kanji/radical detail pages are fixed.
- Build 64; Android mirror synced. Test: test_build64_detail_spacing.py.
