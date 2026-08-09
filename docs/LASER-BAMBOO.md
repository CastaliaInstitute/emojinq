# Bamboo laser output

The source SVGs preserve sumi-e wash, opacity, and optional draw animation for
the browser. For bamboo production, create a deterministic binary vector set:

```sh
make check-laser
```

This writes `build/laser-pua/` and validates that the export has:

- black-only paint;
- no opacity, filters, masks, raster images, or clipping effects;
- scalable 72×72 vector paths;
- no stroke narrower than 1.0 SVG unit.

The export is intentionally separate from the source SVGs and the TTF. It is a
laser/engraving handoff, while the source remains useful for animation and the
font remains portable for ESP32 rendering.
