# Build 58 — JLPT & Practice glass / alignment pass

Base: Build 57 overall UI audit.

## Changes made

- Fixed JLPT / Kanji practice result-row alignment.
  - Wider result panel on desktop.
  - Review rows now use a stable 3-column grid: kanji | answer text | result mark.
  - Long answers and correction text wrap cleanly instead of pushing the check/cross marker out of line.
  - Mobile layout collapses cleanly without overflow.
- Extended Liquid Glass / Clear Glass styling to JLPT and practice review surfaces.
  - MCQ review rows
  - JLPT exam review cards
  - JLPT exam category chip
  - Timed mock toolbar / dots / history cards
  - Practice mode buttons now participate in the same glass-control styling pass.
- Prevented opaque blue selected-state regressions in timed mock answer options.
  - Selected options keep the glass surface with accent outline instead of becoming a solid navy slab.
- Mirrored the same CSS changes into the Android packaged web assets under
  `android/app/src/main/python/kotoba_app/static/css/`.

## Environment limitation

`python sync_android.py` could not run in this environment because Flask is not installed here.
To keep the Android package updated anyway, the modified CSS files were copied directly into the Android asset mirror.
