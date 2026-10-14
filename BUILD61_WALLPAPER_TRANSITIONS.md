# Kotoba Build 61 — wallpaper transition stability

Base: Build 60. Changes are confined to shared wallpaper loading, display styles and versioned assets.

## Changes
- Render a saved wallpaper JPEG preview through a CSS pseudo-element from the first body paint on every page. Theme, dimming, and crop/frame preferences are restored in the document head before styles are parsed.
- Keep the preview as a fallback until the original wallpaper (image or animated GIF) is loaded and its size is decoded. Old blobs remain visible until a new one is ready.
- Store image dimensions alongside the locally cached wallpaper preview so its crop closely matches the full wallpaper immediately on the next route.
- Remove the fallback cleanly when a wallpaper is reset or the saved Blob is missing.
- Enable cross-document view transitions on browsers that support them, with reduced-motion support; unsupported engines still get the early-paint fallback.
- Update the asset version, service worker cache and Android versionCode to 61. Android mirror includes the same template, CSS and JS.

## Testing performed
- Chromium fixture: 24 first-paint + delayed-full-wallpaper restoration checks across Roadmap, JLPT, Kanji, Practice, widths 390/768/1280, and both glass modes. Fixture navigation loaded new documents via document replacement because normal local URL navigation is restricted in this test container.
- Rendered a test first-paint backdrop and inspected the screenshot to verify the image is genuinely painted, not merely present in computed CSS.
- Existing Python CSS/glass and source parity tests pass.
- Android APK compilation, physical-device verification, and real cross-document navigation could not be performed here. Some older Node.js test suites require the missing jsdom dependency, and Flask integration tests require Flask.

## Verification on your device
After installing, switch Home → Learn → Explore → JLPT → Practice, then back, in both glass modes. Repeat with a custom JPG/PNG and an animated GIF. The animated image may restart on a full-document navigation on older WebView versions; the preview should cover the loading gap.
