# Build 67 — Liquid Glass Japan Explorer map

- `static/css/japan-map.css`: the interactive map is now a glass pane.
  - Liquid Glass ON: translucent sea and land, backdrop blur, rim light and reflection; zoom controls, hint and the filter toolbar use the same frosted finish.
  - Liquid Glass OFF (clear glass): same translucent map and controls with no blur, so the wallpaper shows through.
  - Labels, title, compass and scale follow the active theme (light/dark) with a glass-coloured halo.
  - Full-screen map keeps the glass look.
- Build number bumped to 67 (cache bust).

## Build 68
- Location sheet (and the stamps panel) is now Liquid Glass instead of solid: frosted blur when Liquid Glass is ON, clear glass (no blur, ~70% tint for legibility) when OFF. The dimmer behind it is lighter so the map stays visible.
- Airplane marker: positioned with the SVG `transform` attribute (animated in JS) instead of a CSS transform on an SVG group, and its on-screen size now comes from the element box / viewBox instead of `getScreenCTM()`. It now sits exactly on the selected city's pin and stays 26 px at every zoom in Chrome, Firefox and Safari. The train marker uses the same positioning.
