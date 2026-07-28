# Castalia Emoji style system

The scalable treatment is deliberately simpler than a raster texture effect:

1. Preserve the source silhouette as a semantic starting point.
2. Lift source color into a pale grayscale wash so the paper remains visible.
3. Add a dark primary contour, a slightly misregistered contour, and a broken pencil pass.
4. Add only a few semantic interior marks. Do not fill the glyph with hatch fields.
5. Keep every mark in the same square viewBox and let stroke widths scale with the artwork.

The result is an inked pictogram system, not a literal reproduction of a historical plate. For semantic glyphs, preserve the instantly recognizable sign: `place` must retain a map-pin silhouette, `heart` must remain a heart, and so on.

`scripts/build_set.py` applies the shared treatment to an arbitrary manifest. The files in `assets/canonical/` are the reviewed style set; `assets/generated/` is the reproducible batch output for comparison and future expansion.
