# Developmental vocabulary ladder

Emojinq should grow in conceptual complexity without abandoning its sumi-e
brush language. The levels below are an art-direction and review order, not an
age rating or a claim about when a child should know a word.

1. **First words** — one familiar referent, drawn with enough clear gestures
   to be named immediately by a toddler. The glyph should remain spacious and
   iconic, but recognition outranks a low stroke count.

2. **Naturalist referents** — a specific animal, plant, food, tool, or place.
   The glyph earns more anatomy, texture, and species-specific structure so it
   is recognizable rather than generic.

3. **Emotions and relationships** — affect, bodily states, actions, and human
   connection. Avoid stick figures; use expressive body masses, posture,
   clothing, gesture, and selective facial marks.

4. **Scenes and ideas** — social roles, cultural references, systems, actions
   involving several objects, and abstractions. These may use richer
   compositions, but the subject hierarchy must remain clear.

Alphabetic and numeric glyphs are tracked separately as a literacy set. The
first-pass classifier is transparent and carries confidence metadata; semantic
review should replace heuristics before using the ranks as a curriculum.

Each record also tracks `brush_stroke_count`, `stroke_only_marks`,
`filled_marks`, and a stroke-complexity band. The stroke counts measure SVG
brush gestures, including independent move-to subpaths inside a single path
element. `stroke_only_marks` is the stricter measure and only counts visible
geometry with no fill. This distinction is intentional while the existing
corpus is migrated away from filled contours.

The gallery's recognition review is a separate, required human gate. Automated
stroke counts and nonblank renders cannot prove that a child will recognize a
subject. Reviewers should request more defining brush strokes whenever a
glyph's silhouette, characteristic parts, orientation, or action is unclear.

Generate the current machine-readable ranking with:

```sh
python3 scripts/rank_developmental_vocabulary.py
```

The result is `assets/developmental-vocabulary.json`.
