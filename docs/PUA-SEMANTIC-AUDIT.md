# PUA semantic and toddler-recognition audit

This audit separates two questions that an automated geometry check cannot
answer:

1. Does the label denote one visually nameable object or organism?
2. Does the unlabeled drawing retain that subject's defining parts at 32 CSS
   pixels?

The source-level decisions live in `scripts/rank_developmental_vocabulary.py`.
The resulting object-scale queue is written to
`assets/pua-recognition-review.json`; it requires real label-blind observations
from a child aged 12–47 months and never self-approves generated artwork.

## Manual taxonomy correction

The August 2026 contact-sheet audit removed 53 false object candidates. These
remain supported glyphs, but belong to the contextual scene/system/material
track and are not represented as evidence-backed toddler objects.

- **Body systems or substances:** blood, muscles, nerves, skin.
- **Materials:** clay, cloth, fiber, glass, leather, metal, paper, plastic,
  sand, stone, thread.
- **Landscape scenes and place relationships:** canyon, ceiling, coast, delta,
  glacier, jungle, lake, park, pasture, plateau, reef, sand, savanna, spring,
  tide, tundra, valley, wave.
- **Systems, materials, activities, and generic object classes:** circuit,
  clay, forest, foundation, game, goods, handle, mural, port, spice, stage,
  steam.
- **Plant materials or scenes:** compost, dirt, moss, soil, stream.
- **Scientific systems or generic historical classes:** relic, reservoir,
  sensor.

This is not a loophole for an unclear drawing. Each decision is based on the
label lacking a single canonical, toddler-nameable silhouette. Physical nouns
with a stable whole-object form—such as `cave`, `barn`, `bench`, `clinic`,
`bowl`, `doll`, `stroller`, `pulley`, and `whistle`—remain in the strict queue.

## Manual drawing correction

`scripts/redraw_pua_semantic_audit_batch.py` is the final authoring pass for
the label-dependent outliers found in the same contact sheets. It replaces
sparse hints with complete, pressure-shaped constructions: connected wheels
and shaft for an axle; head, shank, and point for a nail; rope, grooved wheel,
and suspended load for a pulley; ladder, platform, and chute for a slide; frame,
ropes, and seat for a swing; hole, earth mound, and animal cue for a burrow; and
equivalent defining structures for every source in the script.

The script runs after canonical emoji transplants and before the object-scale
strengthening pass. This guarantees that a clean build uses the reviewed art,
and that the ink and color/fallback hashes recorded by the recognition ledger
refer to the same final assets.

## Release interpretation

Passing `make check` proves coverage, rendering, style, catalog, metadata, and
font integrity. It does not prove that a child recognized a glyph. Only
`make release-check`, with all current hash-bound observations approved, closes
the recognition requirement.

## Detached-component review

The connected-component detector is deliberately conservative: a hammer above
an anvil, two people in a relationship, or ten counting dots all look
"detached" to a raster flood fill. The 60 highest-area findings were rendered
as two severity-ranked sheets and inspected individually. Their source-specific
decisions live in `scripts/mark_intentional_pua_components.py`; the audit now
reports them separately from unresolved candidates. No category-wide exemption
exists, so lower-ranked sources remain in the queue until they receive the same
review or a vector correction.
