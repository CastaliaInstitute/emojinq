# PUA visual review

Emojinq PUA glyphs use a restrained sumi-e/naturalist language: a readable silhouette first, a small number of descriptive interior marks second, and texture only where it clarifies the subject. The artwork is monochrome and remains portable SVG rather than relying on filters or embedded raster images.

## Acceptance criteria

- The subject is recognizable at 128px and remains centered inside the 72×72 viewBox.
- Primary contours use rounded, slightly varied ink strokes rather than uniform geometric outlines.
- Secondary marks describe structure, motion, material, or atmosphere; they do not become decorative noise.
- Detached marks are allowed only when they have semantic purpose: motion, sound, stars, counting groups, diagram nodes, or environmental brush texture.
- Every glyph carries `data-castalia-style="sumi-e-ink-wash-v1"` and `data-ink-stroke-system="tapered-v1"`.
- Every glyph is scalable vector art with paths, no embedded images, and no SVG filters.

## Categories

The current inventory contains 751 PUA glyphs across 13 categories:

`animals`, `body`, `farm`, `flora`, `herbs`, `locations`, `materials`, `objects`, `patterns`, `people`, `plants`, `science`, and `weather_sky`.

The categories are reviewed through generated contact sheets in `build/pua-contact-sheets/`. Regenerate them with:

```sh
make contact-pua
```

## Release gate

Run the complete gate before rebuilding or publishing the font:

```sh
make check
```

This checks SVG raster quality, vector portability, 128px legibility, detached-fragment candidates, category coverage, sumi-e metadata, browser catalog references, and the TTF cmap/GSUB mapping. Detached-component output is a review queue, not an automatic rejection: intentional multi-part compositions remain valid when their marks communicate meaning.
