#!/usr/bin/env python3
"""Create a restrained grayscale, hand-drawn pass from a Noto SVG.

This intentionally uses only widely supported SVG primitives. It is an asset
preprocessor, not an SVG renderer for the ESP32.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
STYLE_FILL = re.compile(r"(?:^|;)\s*fill\s*:\s*([^;]+)")
HEX_ANY = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?")


def gray(value: str) -> str:
    match = HEX.match(value.strip())
    if not match:
        return value
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    r, g, b = (int(digits[i : i + 2], 16) for i in (0, 2, 4))
    # Luma keeps dark Noto details dark while removing chroma.
    # Naturalist plates leave the paper visible: preserve tonal hierarchy but
    # lift Noto's saturated fills into pale wash rather than solid ink blocks.
    y = 170 + round((0.2126 * r + 0.7152 * g + 0.0722 * b) * 0.33)
    return f"#{y:02x}{y:02x}{y:02x}"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def fill_value(element: ET.Element) -> str | None:
    value = element.get("fill")
    if value:
        return value
    style = STYLE_FILL.search(element.get("style", ""))
    return style.group(1).strip() if style else None


def grayscale_attributes(root: ET.Element) -> None:
    for element in root.iter():
        for key, value in list(element.attrib.items()):
            element.set(key, HEX_ANY.sub(lambda match: gray(match.group(0)), value))


def convert(source: Path, target: Path, name: str) -> None:
    root = ET.parse(source).getroot()
    root.set("id", f"castalia-emoji-{name}")
    root.set("role", "img")
    root.set("aria-label", name.replace("-", " "))
    grayscale_attributes(root)

    defs = ET.Element(f"{{{SVG_NS}}}defs")
    style = ET.SubElement(defs, f"{{{SVG_NS}}}style")
    style.text = """.ink-outline{stroke:#292929;stroke-width:1.7;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}.ink-echo{fill:none;stroke:#464646;stroke-width:1.15;stroke-linejoin:round;stroke-linecap:round;opacity:.62;transform:translate(1.7px,1.1px) rotate(.45deg 64px 64px);vector-effect:non-scaling-stroke}.ink-echo-two{fill:none;stroke:#6b6b6b;stroke-width:.72;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:17 3 5 2 11 4;opacity:.58;transform:translate(-1.3px,.8px) rotate(-.7deg 64px 64px);vector-effect:non-scaling-stroke}.ink-pencil{fill:none;stroke:#888;stroke-width:.48;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:3 2 12 2;opacity:.52;transform:translate(.4px,-1.6px);vector-effect:non-scaling-stroke}.ink-hatch{fill:none;stroke:#353535;stroke-width:.55;stroke-linecap:round;opacity:.17;vector-effect:non-scaling-stroke}.ink-hatch-cross{fill:none;stroke:#353535;stroke-width:.45;stroke-linecap:round;opacity:.08;vector-effect:non-scaling-stroke}.ink-stipple{fill:#353535;opacity:.16}"""
    hatch_count = 0
    root.insert(0, defs)

    for element in list(root.iter()):
        if local(element.tag) not in {"path", "circle", "ellipse", "rect", "polygon", "polyline"}:
            continue
        fill = fill_value(element)
        if fill and fill != "none":
            element.set("fill", gray(fill))
            element.attrib.pop("style", None)
            element.set("class", "ink-outline")
            echo = ET.fromstring(ET.tostring(element, encoding="unicode"))
            echo.set("class", "ink-echo")
            echo.set("fill", "none")
            echo_two = ET.fromstring(ET.tostring(element, encoding="unicode"))
            echo_two.set("class", "ink-echo-two")
            echo_two.set("fill", "none")
            pencil = ET.fromstring(ET.tostring(element, encoding="unicode"))
            pencil.set("class", "ink-pencil")
            pencil.set("fill", "none")
            parent = next((p for p in root.iter() if element in list(p)), None)
            if parent is not None:
                index = list(parent).index(element)
                parent.insert(index + 1, echo)
                parent.insert(index + 2, echo_two)
                parent.insert(index + 3, pencil)
                if hatch_count < 4:
                    clip_id = f"ink-clip-{hatch_count}"
                    clip = ET.SubElement(defs, f"{{{SVG_NS}}}clipPath", {"id": clip_id})
                    clip.append(ET.fromstring(ET.tostring(element, encoding="unicode")))
                    hatch = ET.Element(f"{{{SVG_NS}}}g", {"class": "ink-hatch", "clip-path": f"url(#{clip_id})"})
                    for offset in range(-128, 257, 16):
                        ET.SubElement(hatch, f"{{{SVG_NS}}}line", {"x1": str(offset), "y1": "0", "x2": str(offset + 128), "y2": "128"})
                    cross = ET.Element(f"{{{SVG_NS}}}g", {"class": "ink-hatch-cross"})
                    for offset in range(-128, 257, 24):
                        ET.SubElement(cross, f"{{{SVG_NS}}}line", {"x1": str(offset), "y1": "128", "x2": str(offset + 128), "y2": "0"})
                    hatch.append(cross)
                    stipple = ET.Element(f"{{{SVG_NS}}}g", {"class": "ink-stipple"})
                    for x, y in ((18, 27), (43, 39), (76, 24), (104, 49), (28, 79), (62, 93), (94, 82), (113, 108)):
                        ET.SubElement(stipple, f"{{{SVG_NS}}}circle", {"cx": str(x), "cy": str(y), "r": "1.1"})
                    hatch.append(stipple)
                    parent.insert(index + 3, hatch)
                    hatch_count += 1

    root.set("data-castalia-style", "naturalist-pen-v2")
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    convert(args.input, args.output, args.name)


if __name__ == "__main__":
    main()
