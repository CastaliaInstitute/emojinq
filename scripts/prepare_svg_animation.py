#!/usr/bin/env python3
"""Expose a stable, opt-in draw-animation contract on PUA SVG brush marks."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def decorate(path: Path) -> bool:
    root = ET.parse(path).getroot()
    root.set("data-ink-path-units", "normalized")
    path_nodes = [element for element in root.iter() if local(element.tag) == "path"]
    has_stroke = any(
        element.get("stroke") is not None or element.get("stroke-width") is not None
        for element in path_nodes
    )
    animation = "draw-v1" if has_stroke else "wash-v1"
    changed = root.get("data-ink-animation") != animation
    root.set("data-ink-animation", animation)
    for element in root.iter():
        if local(element.tag) != "path":
            continue
        has_stroke = element.get("stroke") is not None or element.get("stroke-width") is not None
        classes = set((element.get("class") or "").split())
        if has_stroke:
            classes.add("ink-stroke")
            if element.get("pathLength") != "1":
                element.set("pathLength", "1")
                changed = True
        else:
            classes.add("ink-wash")
        new_class = " ".join(sorted(classes))
        if element.get("class") != new_class:
            element.set("class", new_class)
            changed = True
    if changed:
        path.write_text(ET.tostring(root, encoding="unicode") + "\n")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    args = parser.parse_args()
    changed = 0
    total = 0
    for path in sorted(args.root.rglob("*.svg")):
        if path.parent.name == "references":
            continue
        total += 1
        changed += int(decorate(path))
    print(f"animation contract checked: {total} SVGs, decorated {changed}")


if __name__ == "__main__":
    main()
