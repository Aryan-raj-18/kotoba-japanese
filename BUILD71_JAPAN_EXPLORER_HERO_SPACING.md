# Kotoba v1.0.0 — Build 71: Japan Explorer heading alignment

Base: Build 70 Play Store source release candidate. This update is a focused UI fix to `/japan`.

## Problem

The `Learn Japanese through places.` heading and Japanese eyebrow text began almost on the left border of the rounded glass hero. The original `.japan-hero-copy` horizontal padding was only 4 px. The large heading also had a line-height of 0.98, leaving text cramped vertically.

## Fix

- Add responsive internal padding to `.japan-hero`, with matching spacing between its text column and passport card.
- Make the copy column respect the container inset on desktop, tablet, and phone layouts.
- Increase heading line height, balance line breaks, and improve the introductory paragraph spacing.
- Preserve the user's selected Liquid Glass or Clear Glass styling and the existing Japan Explorer functionality.
- Mirror CSS and asset-cache identifiers in the Android-packaged app; increment Android `versionCode` to 71.

## Verification

- 40 Playwright Chromium layout checks, using 10 widths from 320 to 1600 pixels, two themes, and both glass modes: **all passed**.
- No page-wide horizontal overflow, heading overflow, or overlap with the passport card in the checked layouts.
- Additional checks at larger browser font sizes (20, 24, 30 px) across phone/tablet/desktop: no horizontal overflow.
- 18 existing focused source tests plus the Build 71 checks passed.
- An installed Android APK and signed Play Store AAB have **not** been built or tested in this environment.

## Unchanged

Learning data, Japan map geography, passport progress logic, Golden Thread intro, other app routes, and GitHub Play Store release workflow remain unchanged.
