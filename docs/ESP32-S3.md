# ESP32-S3 rendering notes

The SVGs are source assets, not a promise that an embedded device can parse arbitrary SVG. For a production build, rasterize them during the host-side asset step and ship the resulting bitmap or packed path data.

Recommended constraints:

- render to a square canvas at the panel's native glyph size;
- use a 12–16% quiet margin on all sides;
- flatten gradients and filters before packaging;
- prefer 1-bit output for e-paper or 4-bit grayscale for LCD/OLED;
- use rounded joins and caps, with a minimum final stroke of two physical pixels;
- test at 64, 128, and 240 px because small details disappear quickly;
- cache the rasterized result in flash and avoid SVG parsing on every wake.

The generated art uses fills, strokes, opacity, and simple transforms only. The import script intentionally does not emit turbulence, blur, masks, or blend modes.

For the current Einq firmware, the clean handoff is a generated bitmap or a renderer-specific path asset in the separate `einq` repository; this repository should remain platform-neutral.
