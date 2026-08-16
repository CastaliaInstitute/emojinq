# PUA visual review

Emojinq PUA glyphs use an expressive sumi-e/naturalist language: a strong subject silhouette, descriptive anatomical or structural brush marks, and tonal variation only where it clarifies the subject. The artwork remains portable vector SVG; grayscale values are intentional engraving-depth cues, never opacity, SVG filters, solid filled subject masses, or embedded raster images.

## Acceptance criteria

- The subject is recognizable at 128px and remains centered inside the 72×72 viewBox.
- Primary contours use rounded, slightly varied ink strokes rather than uniform geometric outlines.
- Secondary marks describe structure, motion, material, or atmosphere; they do not become decorative noise.
- Every visible mark is a stroke; closed contours may be used for anatomy, but their fill must remain `none`.
- Detached marks are allowed only when they have semantic purpose: motion, sound, stars, counting groups, diagram nodes, or environmental brush texture.
- Every glyph carries `data-castalia-style="sumi-e-ink-wash-v1"` and `data-ink-stroke-system="tapered-v1"`.
- Every glyph is scalable vector art with paths, no embedded images, and no SVG filters.

## Categories

The current inventory contains 858 PUA glyphs across 22 categories:

`adventure`, `animals`, `body`, `brc`, `castalia`, `cave_locations`,
`cosmos`, `dinosaurs`, `faerie`, `farm`, `flora`, `herbs`, `locations`,
`materials`, `objects`, `patterns`, `people`, `plants`, `rockets`, `science`,
`sea_creatures`, and `weather_sky`.

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
