# Kotoba 1.0.0 (78): closed-test layout and glass corrections

Settings previously forced an opaque, unblurred fill despite Liquid Glass being
enabled. It now follows the saved glass mode, including its dialog tint. The open
sheet is placed outside the header's backdrop root on phones and desktops. On a
phone, page content stays in its original layout and scroll position but is hidden
behind the open settings sheet, so its letters cannot bleed into clear settings.
Closing settings restores it. Low reported device memory now selects a smaller
blur radius instead of disabling a supported effect. Unsupported WebViews and
device reduced-transparency preferences retain a readable fallback with an
explanation in settings.

Roadmap's actual practice panel now has reading insets; counts, prompts, feedback,
combo badges and answers wrap and grow inside the panel. Learning Games use
shrinkable grid tracks, natural-height cards and wrapping answers, with space
around large Japanese glyphs and the game controls. The outer game stage owns
blur, rather than stacking blur on its inner question card.

## Validation

- 200 Python tests and 32 release regression suites.
- 352 static responsive layouts and the existing live-browser regression suite.
- New live-browser coverage: complete learn-to-practice transitions and all quiz
  answers for Hiragana 1, Hiragana 2 and Katakana 1; all five games at Easy, Medium
  and Hard; widths 320/390/560/800; enlarged text at 390; settings at 390/1280 in
  Light/Dark and ON/OFF; persistence, lower-memory blur and unsupported fallback.
- The new checks reproduce missing reading insets and disabled settings blur
  against the previous release's CSS/controllers. They inspect actual text ranges
  against card insets rather than only checking document width.
- The release workflow also runs Android unit tests, lint, signed APK/AAB builds,
  package/version/provider checks, signatures, bundle validation and 16 KB checks.

Package remains `com.kotoba_japanese.app`, version name `1.0.0`; version code and
asset cache advance to `78`. All 23 course-data hashes are unchanged. Fonts,
lesson content and learning logic are unchanged. Android assets are regenerated
from the canonical web source during CI. No physical Android device was available
to the automated runner; closed testers should confirm the fix on their phones.
