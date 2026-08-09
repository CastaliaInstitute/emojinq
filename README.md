# Emojinq

An artistic, grayscale treatment of [OpenMoji Black](https://openmoji.org/) with the character of a 19th-century naturalist's field plate, for calm, low-power displays and full-screen glyphs on ESP32-S3 devices.

This is an independent derivative-art project. It is not affiliated with or endorsed by OpenMoji.

## What is here

- `assets/source/` — selected OpenMoji Black SVG inputs, stored with upstream attribution.
- `assets/manifest.json` — names, Unicode code points, and semantic exceptions for the set.
- `assets/canonical/` — reviewed authored vector glyphs for the original starter specimens.
- `assets/line/` — generated fill-free line-art output for the specimen and scalable rendering.
- `assets/ink/` — generated grayscale, hand-drawn-style SVG output.
- `scripts/build_set.py` — batch-applies the shared treatment to the manifest.
- `scripts/collapse_lines.py` — removes area fills while preserving scalable pen lines.
- `scripts/fetch_openmoji.py` — sparse-fetches the upstream OpenMoji Black SVG directory.
- `scripts/build_all.py` — builds the full OpenMoji set in grayscale or line mode.
- `scripts/check_svg_set.py` — verifies the complete card-ready tapered SVG corpus.
- `scripts/audit_pua_artifacts.py` — report-only raster audit for detached or cropped PUA fragments.
- `scripts/check_pua_legibility.py` — verifies every PUA glyph has visible ink and a readable 128px footprint.
- `scripts/check_pua_vector.py` — verifies PUA SVGs remain scalable paths without embedded raster images or filters.
- `scripts/check_pua_font_render.py` — renders every PUA code point from the TTF and rejects blank font glyphs.
- `scripts/check_pua_duplicates.py` — rejects exact raster silhouette reuse across distinct PUA names.
- `scripts/check_pua_coverage.py` — verifies all PUA categories are represented in the manifest and review sheets.
- `scripts/check_catalog.py` — verifies the browser catalog points to the current manifests and TTF.
- `scripts/render_pua_contact_sheet.py` — renders repeatable category contact sheets for visual QA.
- `scripts/import_noto_svg.py` — deterministic source-to-ink converter retained for compatibility.
- `scripts/fetch_yuji_boku.py` — fetches the open Yuji Boku base font for alphabet coverage.
- `scripts/build_alpha_svg.py` — converts the Yuji Boku alphabet into the same Emojinq SVG treatment.
- `assets/pua/manifest.json` — the shareable PUA inventory, grouped for the browser catalog and font build.
- `docs/ESP32-S3.md` — rendering and integration notes.

The canonical treatment uses pale washes, asymmetric pen contours, and a few selective interior marks rather than hatch fills or filters. This keeps the SVGs scalable and gives the set a quieter 19th-century ink quality while keeping the generated TTF as clean filled outlines. See [docs/STYLE.md](docs/STYLE.md).

The original authored specimens include person, pin/place, light bulb, heart, star, sun, moon, coffee, sunflower, house, book, and leaf. The batch pipeline now processes the complete OpenMoji Black source set.

## Quick start

Install the one build dependency, generate the batch comparison set, then build the font:

```sh
python3 -m pip install -r requirements-build.txt
make assets
make lines
make font
```

To build the complete OpenMoji Black grayscale set locally:

```sh
make all-gray
open http://localhost:8000/docs/all.html
```

Use `make all-lines` when a fill-free line-only corpus is needed for rasterization or path conversion.

The full upstream source and generated output are intentionally ignored; the manifest and deterministic build scripts are the shareable source of truth.

The resulting `fonts/Emojinq-Regular.ttf` is a conventional monochrome TrueType font containing the complete generated emoji set, the ASCII alphabet and digits, the divination symbols, and the complete PUA inventory. The alphabet is based on Yuji Boku and passes through the same SVG conversion, pressure variation, and outline-building pipeline. It maps direct Unicode code points and includes OpenType ligature substitutions for supported emoji sequences. Centerline SVG strokes are sampled into tapered filled contours, then converted to TrueType quadratic outlines for embedded compatibility.

Run `make check-pua` to raster-check the complete PUA corpus and report likely detached source fragments before publishing a new font build.

Run `make contact-pua` to regenerate the 13 category contact sheets under `build/pua-contact-sheets/`. Run `make review-pua` to regenerate those sheets and persist the detached-artifact report at `build/pua-artifact-audit.json`. The complete release gate is `make check`: it validates SVG quality, PUA legibility and coverage, sumi-e metadata, browser catalog references, and the rebuilt TTF’s PUA cmap and GSUB tables.

The generated `assets/gray-all/` corpus contains all 4,495 manifest glyphs as scalable, card-ready SVGs. Every glyph is tagged with `data-ink-stroke-system="tapered-v1"`; explicit stroke and default-filled OpenMoji line paths are normalized into tapered ink geometry, with one upstream-empty source glyph preserved and identified rather than invented.

Yuji Boku was selected after comparing Yuji Boku, Yuji Syuku, and Yuji Mai: Boku has the most gestural brush character for the small type specimen while remaining legible at display scale. The build can be extended to the other Yuji families later without changing the emoji pipeline.

To view the specimen locally:

```sh
python3 -m http.server 8000 --directory .
open http://localhost:8000/docs/
```

### Rebuilding one SVG

```sh
python3 scripts/import_noto_svg.py \
  --input .cache/openmoji/black/svg/1F464.svg \
  --output assets/ink/person.svg \
  --name person
```

The converter keeps the original viewBox, removes color, adds restrained sumi-e pressure variation and organic curve wobble, and avoids SVG filters so the result remains portable to embedded renderers. Preview the output in any browser or vector editor.

## ESP32-S3 target

The output is designed to be rasterized once at the target display size, then drawn as a bitmap. Use a 1-bit or 4-bit grayscale framebuffer when the panel supports it. Keep the SVG viewBox square and scale the artwork into a safe inset rather than cropping it at the panel edge.

See [docs/ESP32-S3.md](docs/ESP32-S3.md).

## Provenance and licensing

OpenMoji Black artwork is distributed under CC BY-SA 4.0. The upstream license boundary is documented in `LICENSE-OPENMOJI`.

The generated derivative artwork in this repository is released under the applicable upstream share-alike terms. See `LICENSE`, `LICENSE-OPENMOJI`, and `NOTICE` for the project boundary and attribution. Emojinq is an independent project name; do not imply endorsement by OpenMoji.

## Roadmap

- Add optional 1-bit and 4-bit PNG export for firmware packaging.
- Tune stroke weights against the exact ESP32-S3 display geometry.
