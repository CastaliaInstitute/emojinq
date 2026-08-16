# Emojinq

An artistic, grayscale treatment of [OpenMoji Black](https://openmoji.org/) with the character of a 19th-century naturalist's field plate, for calm, low-power displays and full-screen glyphs on ESP32-S3 devices.

This is an independent derivative-art project. It is not affiliated with or endorsed by OpenMoji.

## What is here

- `assets/source/` — selected OpenMoji Black SVG inputs, stored with upstream attribution.
- `assets/manifest.json` — names, Unicode code points, and semantic exceptions for the set.
- `assets/canonical/` — reviewed authored stroke-only vector glyphs for the original starter specimens.
- `assets/line/` — generated fill-free line-art output for the specimen and scalable rendering.
- `assets/ink/` — generated stroke-only SVG output for the original starter specimens.
- `scripts/build_set.py` — batch-applies the shared treatment to the manifest.
- `scripts/collapse_lines.py` — removes area fills while preserving scalable pen lines.
- `scripts/fetch_openmoji.py` — sparse-fetches the upstream OpenMoji Black SVG directory.
- `scripts/build_all.py` — builds the full OpenMoji set in canonical stroke mode; the older grayscale importer remains available only when explicitly requested.
- `scripts/build_naturalist_pua.py` — reproducibly builds the dinosaur, sea-creature, and rocket PUA families.
- `scripts/redraw_botanical_ink_art.py` — renders flora and herb PUA families as shared-vocabulary naturalist brush studies.
- `scripts/redraw_body_naturalist_art.py` — replaces diagrammatic body outliers with compact anatomical and gesture brush studies.
- `scripts/redraw_body_actions_naturalist.py` — replaces push, reach, and walk stick figures with articulated naturalist gesture studies.
- `scripts/redraw_animals_naturalist_art.py` — renders the animal concepts as species-cued nineteenth-century naturalist brush studies.
- `scripts/redraw_field_studies.py` — authors the weakest animal, dinosaur, and sea-creature outliers directly as anatomy-led naturalist SVG studies.
- `scripts/enrich_field_studies.py` — adds the second anatomical pass: joints, lower contours, faces, shells, fins, feathers, and other species-defining marks.
- `scripts/brushify_field_lines.py` — converts open field-study contours into tapered pressure ribbons so limbs and tentacles do not render as constant-width stick lines.
- `scripts/redraw_patterns_naturalist_art.py` — renders abstract pattern and pigment marks as irregular vector brush studies.
- `scripts/redraw_materials_naturalist_art.py` — renders the material studies as layered grayscale brush masses with dry edges.
- `scripts/redraw_sea_naturalist_art.py` — renders coral, shellfish, fish, mammals, and cephalopods as species-specific brush studies.
- `scripts/redraw_dinosaurs_naturalist_art.py` — renders the dinosaur and fossil PUA set with species-specific anatomy and dry-brush detail.
- `scripts/enrich_naturalist_plate_detail.py` — adds reusable encyclopedia-style anatomy marks to dinosaur and sea-creature plates.
- `scripts/remove_pua_ground_strokes.py` — removes the legacy non-semantic baseline strokes without touching meaningful landscape marks.
- `scripts/redraw_people_rich_sources.py` — raises sparse people concepts to the reviewed naturalist plate standard with vector-only source studies.
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
- `scripts/cartographic_alphabet.py` — original path grammar for the complete cartographic ASCII alphabet.
- `scripts/build_alpha_svg.py` — renders that grammar as pressure-shaped, animatable map-lettering SVGs.
- `scripts/alpha_skeleton.py` — recovers letter topology, then applies roughening and loaded-middle pressure.
- `scripts/centerline_pua.py` — batch-converts filled authored PUA studies into auditable stroke-only SVGs.
- `scripts/enrich_animals_stroke_anatomy.py` — adds sparse directional anatomy marks to the animal studies.
- `scripts/enrich_sea_stroke_anatomy.py` — adds sparse species cues without hatching or fill masses.
- `scripts/lock_generated_stroke_svg.py` — normalizes all authored legacy SVG directories while preserving upstream source inputs.
- `scripts/check_stroke_corpus.py` — rejects authored fills, raster effects, and incomplete normalized strokes.
- `assets/pua/manifest.json` — the shareable PUA inventory, grouped for the browser catalog and font build.
- `docs/ESP32-S3.md` — rendering and integration notes.

The canonical treatment uses pressure-shaped sumi-e strokes, asymmetric pen contours, broken dry-brush accents, and selective grayscale stroke weight rather than hatch fills, opacity, or filters. The SVG itself must look like a beautiful 19th-century naturalist ink drawing before it is converted into a TTF or laser export; the browser and font are downstream renderings of that source art. Grayscale is retained as an intentional depth cue for engraving while the generated TTF remains a clean monochrome outline font. See [docs/STYLE.md](docs/STYLE.md).

The original authored specimens include person, pin/place, light bulb, heart, star, sun, moon, coffee, sunflower, house, book, and leaf. They now use the same stroke-only contract as the complete OpenMoji Black source set.

## Quick start

Install the one build dependency, generate the batch comparison set, then build the font:

```sh
python3 -m pip install -r requirements-build.txt
make assets
make lines
make font
```

To build the complete OpenMoji Black stroke set locally:

```sh
make all-gray
open http://localhost:8000/docs/all.html
```

`line` is also the default mode. The historical filled/grayscale importer is
kept only for comparison or legacy export work and is not part of the Emojinq
font, gallery, or PUA build.

Use `make all-lines` when a fill-free line-only corpus is needed for rasterization or path conversion.

For bamboo engraving, use the complete checked handoff. It exports both the standard set and PUA artwork, plus a material calibration plate. Primary black marks are intended to engrave deepest; neutral gray marks provide controlled tonal depth:

```sh
make check-laser
```

`build/laser-calibration.svg` must be run on the actual bamboo first. It gives
the laser operator a neutral gray ramp to map to power/speed/depth; grayscale
values are not universal millimetre measurements. The exported SVGs carry the
same explicit convention (`black = deepest`, `white = lightest`) and contain
only scalable vector geometry—no opacity, filters, masks, or raster textures.

The full upstream source is intentionally preserved as reference material; authored output and deterministic build scripts are the shareable source of truth.

The resulting `fonts/Emojinq-Regular.ttf` is a conventional monochrome TrueType font containing the complete generated emoji set, the ASCII alphabet and digits, the divination symbols, and the complete PUA inventory. The original alphabet combines monumental Roman capitals with a compact uncial hand, authored directly as irregular cartographic SVG ink. The compiled font and Atlas paint-on animation consume the same stroke-only source. It maps direct Unicode code points and includes OpenType ligature substitutions for supported emoji sequences.

`make color-font` additionally builds `fonts/Emojinq-Color.ttf`. It retains the
complete TrueType ink outline as a fallback and embeds 4,495 compressed
OpenType-SVG color glyphs. Each uses the corresponding OpenMoji color palette
as a softened, translucent wash beneath Emojinq's pressure-shaped sumi-e ink;
it is a color treatment of the same drawing, not a return to flat emoji art.
The gallery's **Variant** control switches between Ink and Color wash.

Run `make check-pua` to raster-check the complete PUA corpus and report likely detached source fragments before publishing a new font build.

Run `make contact-pua` to regenerate the PUA category contact sheets under `build/pua-contact-sheets/`. Run `make review-pua` to regenerate those sheets and persist the detached-artifact report at `build/pua-artifact-audit.json`. The complete release gate is `make check`: it validates SVG quality, PUA legibility and coverage, the authored stroke-only corpus, sumi-e metadata, browser catalog references, and the rebuilt TTF’s PUA cmap and GSUB tables.

The generated `assets/gray-all/` corpus contains all 4,495 manifest glyphs as scalable, card-ready SVGs. Every glyph is tagged with `data-ink-stroke-system="tapered-v1"`; explicit stroke and default-filled OpenMoji line paths are normalized into tapered ink geometry, with one upstream-empty source glyph preserved and identified rather than invented.

The cartographic alphabet favors broad, uneven Roman capitals, small-cap hierarchy, wedge-like terminals, and sturdy strokes that remain readable over illustrated maps. Deterministic stance, width, baseline, pressure, and dry-edge variation gives repeated labels a restrained sumi-e rhythm without compromising the underlying letterforms. It is an original Emojinq treatment rather than the branded film-title lettering or a redistribution of a non-commercial fan font.

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

The converter keeps the original viewBox, removes chroma, adds pressure-shaped sumi-e variation and organic curve wobble, and avoids SVG filters so the result remains portable to embedded renderers and engraving tools. Preview the output in any browser or vector editor.

### Tracing a naturalist raster reference

For a generated or scanned reference, use the shared raster-to-brush authoring filter:

```sh
make trace-brush \
  TRACE_INPUT=reference.png \
  TRACE_OUTPUT=build/reference-brush.svg
```

The `trace-brush` target is useful when a filled brush ribbon is acceptable. For strict stroke-only output, use the centerline filter directly:

```sh
uv run --python 3.12 --with pillow --with svgpathtools \
  python scripts/raster_to_centerline.py \
  reference.png build/reference-centerline.svg \
  --label "reference study"
```

This invokes AutoTrace’s `--centerline --preserve-width` mode, applies a loaded-middle / tapered-entry-and-lift pressure curve, and emits only ordinary SVG paths with `fill="none"`. Potrace and VTracer are useful for contour or tonal vectorization, but are not the production stroke source because they tend to create filled regions or paired outlines. Install AutoTrace with `brew install autotrace`. The raster reference is never embedded in the font or published SVG.

The standard Unicode build uses OpenMoji Black’s vector line SVGs as its anatomical source, then applies the same pressure treatment in `scripts/line_brush.py`; this preserves small semantic details such as eyes better than centerlining a filled grayscale rendering. Review any generated SVG for recognizable structure before placing it in `assets/pua/`, then run `make check-pua` and `make laser-pua`.

## ESP32-S3 target

The output is designed to be rasterized once at the target display size, then drawn as a bitmap. Use a 1-bit or 4-bit grayscale framebuffer when the panel supports it. Keep the SVG viewBox square and scale the artwork into a safe inset rather than cropping it at the panel edge.

See [docs/ESP32-S3.md](docs/ESP32-S3.md).

## Provenance and licensing

OpenMoji Black artwork is distributed under CC BY-SA 4.0. The upstream license boundary is documented in `LICENSE-OPENMOJI`.

The generated derivative artwork in this repository is released under the applicable upstream share-alike terms. See `LICENSE`, `LICENSE-OPENMOJI`, and `NOTICE` for the project boundary and attribution. Emojinq is an independent project name; do not imply endorsement by OpenMoji.

## Roadmap

- Add optional 1-bit and 4-bit PNG export for firmware packaging.
- Tune stroke weights against the exact ESP32-S3 display geometry.

## Gallery review and deployment

The public gallery includes a per-glyph review form. Reviewers can choose a radio-button rating and leave a note; Cloudflare Pages sends the submission through `/api/feedback`, which creates a structured GitHub issue for review. The GitHub token is stored as a Cloudflare Pages secret and is never exposed to the browser.

Cloudflare deployment and required secrets are documented in [docs/CLOUDFLARE.md](docs/CLOUDFLARE.md).
