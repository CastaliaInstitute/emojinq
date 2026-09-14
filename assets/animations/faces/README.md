# Face animations

These are opt-in animated companions to the static emoji SVGs. The original
artwork is loaded as an SVG `<image>` and the expressive features are layered
on top, so static artwork, font builds, and embedded-device builds are not
changed.

Each file uses `data-emoji-animation="face-v1"` and honors
`prefers-reduced-motion`. It can be used anywhere an SVG can be used:

```html
<img src="assets/animations/faces/grinning-blink.svg" alt="Grinning face">
```

The intended dynamics vocabulary is semantic rather than generic: tears drip,
laughter bobs or rolls, eyes glance or blink, and each face gets behavior that
belongs to its expression. Future animal companions will use the same
parallel-asset pattern for gait and body motion.
