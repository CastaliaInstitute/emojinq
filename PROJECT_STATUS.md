# Emojinq project status

Updated: 2026-07-29  
Repository: `CastaliaInstitute/emojinq`

## Current state

- **Readiness:** Deterministic derivative-art and font pipeline for ESP32-S3 grayscale displays.
- **Evidence:** Upstream OpenMoji source assets, manifest, canonical/line/ink outputs, build scripts, font output, and embedded-rendering notes are present.
- **Visual policy:** Existing glyphs are the source-grounded artwork; do not replace them with generated raster art.

## Release gates

- Build the font and complete set in a clean environment.
- Raster-test at each target display geometry and verify supplementary-plane Unicode mapping.
- Keep CC BY-SA attribution and the independent-project boundary visible in every distribution.
