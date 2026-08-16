# Bamboo laser output

The source SVGs preserve sumi-e brush geometry, neutral grayscale depth, and
optional draw/wash animation for the browser. For bamboo production, create a
deterministic grayscale vector set and a calibration plate:

```sh
make check-laser
```

This writes `build/laser-standard/`, `build/laser-pua/`, and
`build/laser-calibration.svg`, then validates that the exports have:

- explicit neutral grayscale paint;
- no opacity, filters, masks, raster images, or clipping effects;
- scalable 72×72 vector paths;
- no stroke narrower than 1.0 SVG unit.

## Depth convention

The exported luminance is production data, not a decorative wash:

| SVG value | Intended result |
| --- | --- |
| `#262626` / near black | deepest mark / highest calibrated power |
| mid grays | intermediate engraving depth |
| `#eeeeee` / near white | lightest mark / lowest calibrated power |
| no paint | untouched bamboo |

The calibration plate is required because bamboo species, finish, focus,
speed, and power curve change the physical depth. Run the plate on the actual
material first, record the usable levels, then map the machine's grayscale
power curve to those levels. Do not assume that an RGB value corresponds to a
particular millimetre depth.

The export is intentionally separate from the source SVGs and the TTF. It is a
laser/engraving handoff, while the source remains useful for animation and the
font remains portable for ESP32 rendering. The depth metadata is explicit on
every exported SVG so downstream tooling can preserve the convention.
