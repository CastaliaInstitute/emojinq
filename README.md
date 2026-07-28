# Castalia Emoji

An artistic, grayscale treatment of [Noto Color Emoji](https://github.com/googlefonts/noto-emoji) with the character of a 19th-century naturalist's field plate, for calm, low-power displays and full-screen glyphs on ESP32-S3 devices.

This is an independent derivative-art project. It is not affiliated with or endorsed by Google or the Noto project.

## What is here

- `assets/source/` — selected Noto SVG inputs, stored with upstream attribution.
- `assets/manifest.json` — names, Unicode code points, and semantic exceptions for the set.
- `assets/canonical/` — reviewed authored vector glyphs for the full 12-glyph set.
- `assets/ink/` — generated grayscale, hand-drawn-style SVG output.
- `scripts/build_set.py` — batch-applies the shared treatment to the manifest.
- `scripts/import_noto_svg.py` — deterministic source-to-ink converter.
- `docs/ESP32-S3.md` — rendering and integration notes.

The canonical treatment uses pale washes, asymmetric pen contours, and a few selective interior marks rather than hatch fills or filters. This keeps the SVGs scalable and gives the set a quieter 19th-century ink quality while keeping the generated TTF as clean filled outlines. See [docs/STYLE.md](docs/STYLE.md).

The starter set includes person, pin/place, light bulb, heart, star, sun, moon, coffee, sunflower, house, book, and leaf. The same pipeline can process any Noto SVG whose source file is available.

## Quick start

Install the one build dependency, generate the batch comparison set, then build the font:

```sh
python3 -m pip install -r requirements-build.txt
make assets
make font
```

The resulting `fonts/CastaliaEmoji-Regular.ttf` is a conventional monochrome TrueType font. It maps the starter set to their normal Unicode code points, so normal Unicode text rendering works in browsers and font stacks that support the supplementary plane. The font build converts the SVG curves to TrueType quadratic outlines for embedded compatibility.

To view the specimen locally:

```sh
python3 -m http.server 8000 --directory .
open http://localhost:8000/docs/
```

### Rebuilding one SVG

```sh
python3 scripts/import_noto_svg.py \
  --input assets/source/emoji_u1f464.svg \
  --output assets/ink/person.svg \
  --name person
```

The converter keeps the original viewBox, removes color, adds a restrained ink outline and offset sketch pass, and avoids SVG filters so the result remains portable to embedded renderers. Preview the output in any browser or vector editor.

## ESP32-S3 target

The output is designed to be rasterized once at the target display size, then drawn as a bitmap. Use a 1-bit or 4-bit grayscale framebuffer when the panel supports it. Keep the SVG viewBox square and scale the artwork into a safe inset rather than cropping it at the panel edge.

See [docs/ESP32-S3.md](docs/ESP32-S3.md).

## Provenance and licensing

Noto SVG artwork is copyright Google and is distributed under the Apache License 2.0. The upstream license is preserved in `LICENSE-NOTO-EMOJI`.

The generated derivative artwork in this repository is also released under Apache-2.0. See `LICENSE` and `NOTICE` for the project boundary and attribution. Castalia Emoji is an independent project name; do not imply endorsement by Noto or Google.

## Roadmap

- Add a batch manifest for the full emoji set.
- Add optional 1-bit and 4-bit PNG export for firmware packaging.
- Tune stroke weights against the exact ESP32-S3 display geometry.
