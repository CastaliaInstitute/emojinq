# Emojinq style system

The scalable treatment is a vector brush system, not a raster texture effect:

1. Preserve the source silhouette as a semantic starting point.
2. Render primary forms as pressure-shaped sumi-e strokes with visible start, loaded body, and lift-off behavior.
3. Use asymmetric contours, organic curve wobble, broken dry-brush edges, and selective structural marks; do not add a second contour merely to suggest depth.
4. The canonical and engraving variants use neutral grayscale only. The explicitly named Color variant may use the source emoji's familiar hues as restrained translucent washes; it must never invent unrelated colors or replace the ink drawing.
5. Favor premium naturalist observation over traceability or pictographic minimalism. Add anatomical, mechanical, botanical, or environmental detail when it makes the subject more beautiful and recognizable.
5a. Beauty is a review gate, not a post-processing hope: adjacent role cards must not be interchangeable mannequins. Give each movable figure a specific silhouette, gesture, clothing or tool cue, and a deliberate focal brush mark; reject a batch that is merely technically valid but visually repetitive.
6. Keep every mark in the same square viewBox and let stroke widths scale with the artwork.
7. Standard OpenMoji conversion remains line-based, but deliberately authored brush studies use closed ribbon silhouettes when that is necessary to preserve the physical press-load-lift profile.
8. The final SVG corpus contains only intentional brush geometry: either pressure-shaped centerlines or authored `ink-wash`/`ink-dry` ribbons whose silhouette records one brush gesture. Generic solid subject silhouettes and pictogram shading remain forbidden. Color fields are permitted only in the Color variant as subordinate washes beneath the complete ink construction. Do not centerline-recover an authored brush ribbon; that destroys its pressure profile and turns the gesture back into a traced line.

## Color-wash variant

`Emojinq-Color.ttf` preserves the same recognizable sumi-e line construction
as `Emojinq-Regular.ttf`. For standard emoji, the corresponding OpenMoji color
art supplies the semantic palette: yellow faces, red apples, national flag
colors, skin and hair colors, and other familiar cues remain familiar. The
pipeline lowers saturation, mixes in warm paper, reduces opacity, and adds a
faint offset pooling pass before placing the full monochrome brush drawing on
top. Color is therefore supporting evidence for recognition, never the only
evidence.

The monochrome TrueType outlines remain embedded as fallback geometry. PUA,
alphabet, and divination glyphs without canonical emoji color continue to use
the ink rendering rather than receiving invented categorical colors. The
Color variant is for screens and color output; laser and grayscale workflows
continue to use `Emojinq-Regular.ttf` and the neutral SVG corpus.

## SVG-native naturalist goal

The SVG source is the artwork. A browser preview, TTF outline, or laser export
must not be the first place where the sumi-e character appears. Every reviewed
glyph should already read as a nineteenth-century naturalist ink drawing when
its SVG is opened directly: a recognizable silhouette, pressure-shaped brush
gestures, tapered lift-off, asymmetry, and a small number of intentional
anatomical or material marks. A gray stroke may describe volume or engraving
depth, but it must not become a generic closed blob.

For animals and other living subjects, the review question is: “Would a
naturalist identify this from the silhouette and a few observed features?” If
not, the glyph is not ready. For objects and symbols, the same rule applies to
their defining structure. SVG-native also means no embedded raster, filters,
opacity tricks, gradient washes, or decorative duplicate contours; all visual
weight must come from portable vector brush paths. A filled path is valid only
when it is itself an authored `ink-wash` or `ink-dry` gesture in a neutral ink
value, not when it is merely the closed silhouette of an object.

## Figure composition gate

People and animals intended to move through a game scene are isolated figures:
full-bodied, grounded, and readable without a background. A role may use one
small defining prop (for example, a stethoscope for a doctor or a book for a
teacher), but the pose must remain usable as a movable character. Do not use
stick figures, partial torsos, floating heads, or scene furniture to carry the
meaning.

Use multiple figures only when the relationship is the concept itself. Examples
include healer/patient, guardian/child, offering, welcome, help, cooperation,
and conflict. Those interaction glyphs must still show complete bodies,
distinct silhouettes, and an unmistakable action; they are interaction marks,
not replacements for the corresponding movable people.

For animals, preserve the same separation: species cards are isolated agents,
while scene interactions are authored as separate relationship compositions. A
whale, turtle, seahorse, or dinosaur must remain recognizable before it is
placed beside another agent.

## Reference and provenance gate

When a Noun Project silhouette is the clearest structural reference, stage the
downloaded SVG through the authenticated web UI, record its collection or icon
URL, icon ID, creator, access date, and license status, and keep the staged file
alongside the audit record. The reference informs anatomy and pose; it is not
production art. The published SVG must be a Castalia brush transformation and
must retain a machine-readable reference record. Never claim a reference is
licensed for redistribution until the exact production terms have been
verified.

The compiled TrueType font stores both centerlines and brush ribbons as filled
outlines. The source SVG remains the canonical visual artifact, so its brush
role and tonal hierarchy must be legible before compilation.

The result is an inked naturalist symbol system, not a literal reproduction of a historical plate. For semantic glyphs, preserve the instantly recognizable subject while allowing richer observation: `place` must retain a map-pin silhouette, `heart` must remain a heart, and an animal must retain its species-defining anatomy.

## Toddler-recognition gate

Recognition outranks stroke-count economy. Every concrete glyph must be
identifiable as its represented object by a toddler without reading its label.
Preserve or add the subject's defining silhouette, parts, orientation, and
action cues even when that requires more brush strokes. A sparse glyph that is
elegant but ambiguous fails; a richer glyph made from committed, purposeful
brush gestures passes. Abstract vocabulary should use the most concrete,
developmentally familiar visual metaphor available and must be reviewed more
strictly because its label cannot rescue the drawing.

Review source SVGs and compiled font renders both at gallery size and at 32 px.
Passing structural checks, metadata, or a nonblank-render test does not prove
recognizability.

`scripts/build_set.py` applies the shared treatment to an arbitrary manifest. The files in `assets/canonical/`, `assets/line/`, `assets/ink/`, and `assets/generated/` are authored stroke-only specimens; `assets/source/` is the only intentionally unnormalized upstream input directory. `scripts/check_stroke_corpus.py` enforces that boundary.

For the complete upstream set, `make fetch-openmoji && make all-lines` runs the same treatment over every OpenMoji Black SVG and writes a manifest for the full gallery. No per-glyph annotations are required.
