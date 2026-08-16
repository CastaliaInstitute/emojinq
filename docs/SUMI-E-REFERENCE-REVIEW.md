# Sumi-e reference review

Reference: *Mindful Artist: Sumi-e Painting* by Virginia Lloyd-Davies (2019),
copied from iCloud Downloads into the repository root.

## Principles that govern Emojinq

The book defines sumi-e as quick-stroke, calligraphy-derived painting: a
picture is built from specific gestures rather than traced contours. Its
introductory exercises distinguish upright and slanted brush handling, load
one brush with gray and black to create tonal movement, and accept dry,
broken, fuzzy, or wet edges as evidence of brush, moisture, motion, and
energy. The worked bamboo, orchid, plum, chrysanthemum, insect, bird, and rock
studies consistently demonstrate these properties:

- one committed press-load-lift motion per structural mark;
- pressure-shaped width, with a loaded entry or body and a fine lift-off;
- dark, medium, and pale ink used structurally rather than decoratively;
- economical marks separated by active negative space, except where more
  defining strokes are required for immediate toddler recognition;
- asymmetry, diagonal energy, and varied brush angle;
- dry-brush breaks and imperfect edges used selectively;
- recognizable subjects suggested by characteristic anatomy, not exhaustive
  outlining;
- color, when present, used sparingly while ink remains the structure.

## Translation into the font system

Emojinq is a monochrome outline font, so it cannot reproduce absorbent paper
or continuous ink dilution directly. It should translate the reference into
portable vector evidence:

1. Every open centerline compiles to an asymmetric calligraphic profile with
   a loaded heel/body and tapered lift.
2. Pre-profiled SVG passes retain loaded joins when compiled, so one source
   gesture does not become several pointed lozenges.
3. Authored naturalist glyphs retain their closed wash and dry-brush ribbons;
   the font builder must not centerline or restroke them.
4. Edge variation is deterministic and restrained so the result remains
   reproducible and readable at 32 pixels.
5. Glyph composition preserves negative space and avoids generic filled
   silhouettes, duplicate contours, filters, opacity tricks, and raster
   texture.

## Review standard

A glyph passes only when its source SVG and compiled TTF rendering both read
as the same brush study, preserve the subject at small size, and show no
clipping, detached artifacts, repeated artificial taper points, or
mechanically mirrored contours. A toddler must be able to identify a concrete
subject without its text label. Add characteristic parts or structural marks
whenever economy makes the subject ambiguous. Metadata alone is not visual
evidence.
