# SVG brush animation

PUA SVGs expose an opt-in draw contract without changing their static artwork:

- Stroke-led glyphs carry `data-ink-animation="draw-v1"`.
- Wash-led legacy studies carry `data-ink-animation="wash-v1"`; they remain static masses until they are redrawn as paths.
- Brush paths carry `class="ink-stroke"` and `pathLength="1"`.
- Wash masses carry `class="ink-wash"` and remain visible by default.

Example:

```css
svg[data-ink-animation="draw-v1"] .ink-stroke {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: emojinq-draw 900ms ease-out forwards;
}

@keyframes emojinq-draw {
  to { stroke-dashoffset: 0; }
}
```

The font build ignores animation metadata and continues to consume the same
vector paths, so ESP32 and laser-oriented builds remain static and portable.

## Face animation companions

Face motion lives under `assets/animations/faces/`, beside—not inside—the
static Unicode artwork. These SVGs use `data-emoji-animation="face-v1"` and
layer small expressive overlays over the corresponding static color SVG.
The first vocabulary is:

- `grinning-blink.svg` — periodic two-eye blink
- `winking.svg` — periodic wink
- `looking-around.svg` — curious left/right pupil movement

All three stop moving when `prefers-reduced-motion: reduce` is active. New
face behaviors should follow the same contract, retain an accessible title and
description, and avoid changing the source SVG used by font generation.
