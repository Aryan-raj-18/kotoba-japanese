# Kotoba Build 56 — Practice, speaking retry, and navigation

Based on the not-yet-packaged Build 55 adjustments to the Build 54 source.

- Carry forward the Everyday mobile word modal scrolling and layout changes, remove the Everyday-only inline search field/microphone, and preserve the category chips. Global search is untouched.
- Carry forward game answer transparency improvements and remove solid answer-state fills in the other quizzes, roadmap practice, review ratings and match games. Correct/incorrect still uses outlined accents.
- Add an explicit Retry button to Speaking & Shadowing, even after a successful/100% recognition. The current round score reflects the latest attempt for that item; repeat recognitions remain user initiated.
- Suppress Android blue native tap flash while retaining focus-visible keyboard feedback, avoid extra animated ripples on navigation, and use lighter blur on touch screens to reduce composition cost.
- Use versioned cache-first static files in the service worker to reduce repeated stylesheet/script/font network requests during page changes, without caching API/user data or HTML.
- VersionCode 56; static assets synchronized with Android-packaged Python app.

Note: real-world navigation timing/flicker depends on the device, GPU and wallpaper size and requires an installed-device smoke test.
- Adds locally cached *small preview* of the device wallpaper to eliminate the solid theme flash between route loads; full wallpaper is restored asynchronously without uploading or changing it.
