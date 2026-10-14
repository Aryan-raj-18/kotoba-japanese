# Kotoba Build 61 — GitHub Actions CI test fix

Base: Kotoba v1.0.0, Build 61. The app's runtime code, themes, wallpaper, and Android assets are unchanged.

## Why GitHub failed

- `test_catalog_batches.cjs` still tried to set `.value` on `#everyday-filter`, even though the Everyday search and microphone were deliberately removed. It failed with `TypeError: Cannot set properties of null (setting 'value')`.
- A separate outdated assumption in `test_browser_cache.cjs` would fail after that test: the service worker now performs a cache-first exact lookup before its offline `ignoreSearch` fallback, but the test required `ignoreSearch` on every call.

## Changes

1. Update `test_catalog_batches.cjs` to check that the Everyday section still has no search field and to reach the final vocabulary entry through its category tab and `Show more words` paging, opening the exact original word.
2. Update `test_browser_cache.cjs` to cover exact cache hits, offline cache fallback, and exclusion of personal/API/external requests.

## Apply to existing GitHub repository (recommended)

Only replace these two files in the top level of your repository:

- `test_catalog_batches.cjs`
- `test_browser_cache.cjs`

Do not upload the ZIP as one file. Extract it first, copy those two files into the repository root, commit and push them. Alternatively use the included `.patch` and `git apply`.

## Local verification

- Chromium interaction reproduction of category paging and modal open/close passed at widths 390, 768 and 1280 pixels using the real `static/js/everyday.js`, synthetic test catalog and a mocked API.
- Browser cache suite: 4/4 passed.
- Existing Everyday source regressions: 3/3 passed.
- Voice search suite: 8/8 passed.
- Other glass/interface Python unit tests: 19/19 passed.
- Liquid Glass JS test passed.

Limitation: The exact `node test_catalog_batches.cjs` CI command requires Flask and jsdom, which cannot be installed in this offline container. Its test syntax was checked, and the catalog behavior was separately exercised in real Chromium. The complete workflow and Android APK build must be rerun on GitHub Actions.
