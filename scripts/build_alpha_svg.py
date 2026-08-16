#!/usr/bin/env python3
"""Build the original, SVG-native Emojinq cartographic ASCII alphabet."""

from __future__ import annotations

import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from cartographic_alphabet import strokes
from collapse_lines import roughen_path
from style_contract import SUMI_E_STYLE, SUMI_E_STROKE_SYSTEM
from svgpathtools import parse_path

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

def variation(codepoint: int, index: int) -> float:
    value = math.sin((codepoint * 43 + index * 17) * 12.9898) * 43758.5453
    return value - math.floor(value)

def pressure_pieces(d: str, width: float) -> list[tuple[str,float]]:
    """Split one gesture into overlapping loaded-brush pressure phases."""
    path=parse_path(d)
    samples=51
    points=[path.point(i/(samples-1)) for i in range(samples)]
    profile=(.56,.90,1.16,.98,.64)
    result=[]
    for piece,factor in enumerate(profile):
        start=max(0,piece*10-1); end=min(samples-1,(piece+1)*10+1)
        commands=[f"M {points[start].real:.3f} {points[start].imag:.3f}"]
        commands.extend(f"L {p.real:.3f} {p.imag:.3f}" for p in points[start+1:end+1])
        result.append((" ".join(commands),width*factor))
    return result

def glyph_svg(codepoint: int) -> str:
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox":"0 0 72 72", "role":"img", "aria-label":f"U+{codepoint:04X}",
        "data-castalia-style":SUMI_E_STYLE, "data-ink-stroke-system":SUMI_E_STROKE_SYSTEM,
        "data-ink-animation":"draw-v1", "data-ink-path-units":"normalized",
        "data-ink-coverage":"complete", "data-alpha-source":"original-emojinq-strokes-v1",
        "data-alpha-style":"cartographic-roman-uncial-v2", "data-alpha-flair":"sumi-e-pressure-v1",
    })
    group = ET.SubElement(root, f"{{{NS}}}g", {"fill":"none","stroke-linecap":"round","stroke-linejoin":"round"})
    output_index=0
    for index, raw in enumerate(strokes(chr(codepoint))):
        width = 5.15 + variation(codepoint, index) * 2.05
        d=roughen_path(raw, codepoint * 101 + index * 29, amount=.16)
        # The reference grammar is a tall, economical book hand. Compress the
        # original paths themselves (not CSS) so every SVG and TTF consumer
        # sees the same narrow cartographic rhythm.
        d=parse_path(d).scaled(.72,1).translated(complex(5,0)).d()
        for piece, piece_width in pressure_pieces(d,width):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class":"ink-stroke", "data-ink-stroke":"tapered", "data-ink-role":"cartographic-letter",
                "data-ink-index":str(output_index), "pathLength":"1", "d":piece,
                "stroke":"#262421" if index == 0 else "#3d3a35", "stroke-width":f"{piece_width:.2f}",
            })
            output_index+=1
    return ET.tostring(root, encoding="unicode") + "\n"

def main() -> None:
    output = Path("assets/alpha-ink")
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("*.svg"): stale.unlink()
    entries=[]
    for codepoint in range(32,127):
        filename=f"U+{codepoint:04X}.svg"
        (output/filename).write_text(glyph_svg(codepoint))
        entries.append({"name":f"U+{codepoint:04X}","source":filename,"codepoints":[codepoint]})
    (output/"manifest.json").write_text(json.dumps(entries,indent=2)+"\n")
    print(f"built {len(entries)} original SVG-native cartographic glyphs in {output}")

if __name__ == "__main__": main()
