"""Shared visual contract for the Emojinq sumi-e asset pipeline."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

SUMI_E_STYLE = "sumi-e-ink-wash-v1"
SUMI_E_STROKE_SYSTEM = "tapered-v1"


def assert_sumi_e(path: Path) -> None:
    """Raise a useful error when an SVG is not an Emojinq sumi-e asset."""
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise ValueError(f"cannot read SVG {path}: {exc}") from exc
    style = root.get("data-castalia-style")
    stroke_system = root.get("data-ink-stroke-system")
    if style != SUMI_E_STYLE or stroke_system != SUMI_E_STROKE_SYSTEM:
        raise ValueError(
            f"{path}: expected {SUMI_E_STYLE}/{SUMI_E_STROKE_SYSTEM}, "
            f"found {style!r}/{stroke_system!r}"
        )
