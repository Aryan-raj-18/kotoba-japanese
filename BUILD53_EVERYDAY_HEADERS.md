# Kotoba 1.0.0 — Build 53: Everyday section title alignment

Starting from Build 52, added a **scoped** inset to `#everyday-list > .category-block`
and reset each `.category-heading` margin/padding/line height so category titles
and their divider lines remain inside the rounded glass frame. This works for
initial category previews, category filtering, search, and Show all lists, as the
same container/classes are created dynamically by `static/js/everyday.js`.

No learning content, Javascript behaviors, glass effect styling, or other screen
layouts were modified. Mirrored the stylesheet and service-worker cache bump into
the Android Python assets. Android `versionCode` is now 53, with `versionName`
still `1.0.0`.

## Checks completed

- 16 Chromium layout combinations: widths 360, 390, 768 and 1280 px;
  Liquid Glass on/off; dark and light themes; 10 simulated categories per run.
  All heading rectangles were within their card borders without horizontal
  overflow. The blur remained active only when Liquid Glass was on.
- Re-rendering category blocks retained the correct inset and alignment.
- 28 Python unit/regression tests passed (`test_everyday_header_build53` plus
  the existing glass/layout tests); the existing Node Liquid Glass test passed.

This is a CSS-focused visual correction. A full Android APK build/device test
was not run in this environment.
