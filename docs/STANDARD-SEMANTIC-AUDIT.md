# Standard Unicode semantic and recognition audit

The standard font is not exempt from the human recognition requirement. Every
`gray-all` entry receives an explicit semantic track in
`assets/developmental-vocabulary.json`, and every concrete or referent entry is
included in the same hash-bound ledger as the PUA artwork. The current queue
contains 900 standard glyphs and 242 PUA glyphs.

## What enters the toddler gate

The label-blind 32px gate covers a stable physical or natural subject: an
animal, plant, food, body part, tool, garment, vehicle, building, instrument,
or other object whose identity can be communicated without a written label.
Synonyms may be adjudicated after the child finishes, but neither labels nor
answer choices may be shown during a trial.

Expressions, gestures, relationships, roles, actions, scenes, systems, UI
states, and abstract notation remain part of the font and still receive
mechanical, visual, font, and color checks. They are not falsely presented as
one toddler-nameable object.

## Upstream group corrections

OpenMoji's display groups are useful for browsing but are not a semantic
taxonomy. The audit therefore applies meaning before group fallbacks:

- Subdivision tag sequences stored under `Activities` are flags, not sports
  equipment.
- Newer faces and hand gestures stored under `People & Objects` are expressive
  presentations, not independent objects.
- Heart shapes, identity emblems, arrows, UI states, and explicit `symbol`
  labels are symbolic.
- Skin-tone variants inherit the canonical pose's identity rather than
  requiring a child to distinguish presentation modifiers as new vocabulary.
- Weather composites, relationships, and transient actions are contextual
  scenes.
- The `Other` private-use extension range is explicitly allow-listed. Brand
  marks, emergency instructions, interface commands, named identities, and
  software logos cannot enter the object queue merely because their label
  contains a familiar noun.

There are no `unreviewed-referent` fallbacks. The classifier and its audited
source lists live in `scripts/rank_developmental_vocabulary.py`; the metadata
checker recomputes all 5,492 records and rejects drift.

## Flags and color

Flags are symbolic by definition and have a separate stricter obligation:
their identity depends on exact named color and design. They never borrow a
generic toddler-object approval from the cloth silhouette. The color font and
source SVG checks must preserve the correct field colors, divisions, emblems,
and ordering, while the ink font remains a deliberate monochrome rendering.

## Honest release status

`make check` proves the automated build, SVG, catalog, metadata, and font
invariants. It does not prove toddler recognition. `make release-check` remains
red until every current concrete item has two label-hidden observations—ink
and color—from a child aged 12–47 months, adjudicated and imported against the
exact source hashes. Generated art and automated image analysis cannot
self-approve that evidence.
