# Kotoba 1.0.0 — Build 77

This release matches the existing Google Play app entry, `com.kotoba_japanese.app`.
Build 76 used `com.kotoba.app`, which Play rejected for a package mismatch and
an existing `com.kotoba.app.androidx-startup` provider authority.

- Android application ID: `com.kotoba_japanese.app`.
- Public version: `1.0.0`; version code and web cache build: `77`.
- AndroidX Startup must merge to `com.kotoba_japanese.app.androidx-startup`.
- The Kotlin namespace stays `com.kotoba.app`. The manifest explicitly names
  the existing MainActivity and three receivers, avoiding package-relative
  class resolution after changing the application ID.
- Kanji notification actions use the new application ID prefix.
- Original course JSON files are checked against `release-content-hashes.json`.
- CI regenerates the Android mirror and search caches from source before
  packaging. The signed APK and AAB must contain identical code and assets.
- The final APK/AAB verifier checks the package, provider authorities, component
  names, version, signing certificates, bundle validity and 16 KB native alignment.

The Play workflow uses the existing GitHub signing secrets. Upload the new
signed AAB to the existing Play listing; no production publishing is automated.

Changing the application ID creates a separate installation from older sideloaded
`com.kotoba.app` builds. Use the existing manual Backup and Restore feature to
transfer progress if needed. This release does not migrate private app storage
between Android application IDs.

This build addresses the two reported identity errors. Play Console must still
validate the upload, signing registration and the publisher's declarations.
