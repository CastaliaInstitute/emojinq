# Castalia Emoji style system

The scalable treatment is deliberately simpler than a raster texture effect:

1. Preserve the source silhouette as a semantic starting point.
2. Lift source color into a pale grayscale wash so the paper remains visible.
3. Add a dark primary contour, a slightly misregistered contour, and a broken pencil pass.
4. Add only a few semantic interior marks. Do not fill the glyph with hatch fields.
5. Keep every mark in the same square viewBox and let stroke widths scale with the artwork.
6. When the line-art treatment is preferred, run `make lines`; this removes fills and decorative echo contours, adds deterministic path wobble and intermittent heavier pressure marks, without rasterizing or flattening the vector geometry.

The result is an inked pictogram system, not a literal reproduction of a historical plate. For semantic glyphs, preserve the instantly recognizable sign: `place` must retain a map-pin silhouette, `heart` must remain a heart, and so on.

`scripts/build_set.py` applies the shared treatment to an arbitrary manifest. The files in `assets/canonical/` are the reviewed area-style set; `scripts/collapse_lines.py` derives the fill-free `assets/line/` set used by the specimen. `assets/generated/` is the reproducible batch output for comparison and future expansion.

For the complete upstream set, `make fetch-noto && make all-lines` runs the same treatment over every `emoji_u*.svg` file and writes a manifest for the full gallery. No per-glyph annotations are required.
