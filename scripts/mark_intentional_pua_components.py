#!/usr/bin/env python3
"""Persist visual-review decisions for deliberate detached PUA components.

The raster artifact detector cannot infer that ten separate dots mean "ten",
that two figures are required for "performance", or that a hammer belongs
above an anvil.  This registry is deliberately source-specific: only layouts
that were inspected in the severity-ranked contact sheet are exempted from the
unresolved-fragment queue.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"

REVIEWED: dict[str, str] = {
    "science/hygiene.svg": "semantic-multipart-v1",
    "science/many.svg": "counting-marks-v1",
    "science/performance.svg": "figure-and-prop-v1",
    "objects/queen.svg": "figure-and-prop-v1",
    "objects/king.svg": "figure-and-prop-v1",
    "objects/trade.svg": "semantic-multipart-v1",
    "science/compare.svg": "semantic-multipart-v1",
    "science/network.svg": "semantic-multipart-v1",
    "science/ten.svg": "counting-marks-v1",
    "objects/smithing.svg": "figure-and-prop-v1",
    "science/nine.svg": "counting-marks-v1",
    "objects/work.svg": "figure-and-prop-v1",
    "people/trickster.svg": "figure-and-prop-v1",
    "objects/traveler.svg": "figure-and-prop-v1",
    "science/diversity.svg": "semantic-multipart-v1",
    "science/metaphor.svg": "semantic-multipart-v1",
    "people/socrates.svg": "figure-and-prop-v1",
    "people/farmer.svg": "figure-and-prop-v1",
    "objects/forging.svg": "figure-and-prop-v1",
    "people/baker.svg": "figure-and-prop-v1",
    "science/who.svg": "semantic-multipart-v1",
    "objects/wizard.svg": "figure-and-prop-v1",
    "people/care.svg": "figure-and-prop-v1",
    "science/data.svg": "counting-marks-v1",
    "science/seven.svg": "counting-marks-v1",
    "people/kindness.svg": "figure-and-prop-v1",
    "people/healer.svg": "figure-and-prop-v1",
    "science/pattern.svg": "counting-marks-v1",
    "science/count.svg": "counting-marks-v1",
    "science/wonder.svg": "semantic-multipart-v1",
    "locations/rome.svg": "semantic-multipart-v1",
    "locations/tide.svg": "semantic-multipart-v1",
    "science/dialogue.svg": "semantic-multipart-v1",
    "science/harvest.svg": "figure-and-prop-v1",
    "people/tribe.svg": "figure-and-prop-v1",
    "objects/choir.svg": "figure-and-prop-v1",
    "objects/audience.svg": "figure-and-prop-v1",
    "people/ibnsina.svg": "figure-and-prop-v1",
    "science/six.svg": "counting-marks-v1",
    "people/astronaut.svg": "figure-and-prop-v1",
    "science/engineering.svg": "semantic-multipart-v1",
    "people/science.svg": "figure-and-prop-v1",
    "science/argument.svg": "semantic-multipart-v1",
    "people/builder.svg": "figure-and-prop-v1",
    "science/eight.svg": "counting-marks-v1",
    "objects/merchant.svg": "figure-and-prop-v1",
    "objects/message.svg": "semantic-multipart-v1",
    "objects/exchange.svg": "semantic-multipart-v1",
    "objects/gallery.svg": "semantic-multipart-v1",
    "people/cook.svg": "figure-and-prop-v1",
    "people/community.svg": "figure-and-prop-v1",
    "people/name.svg": "figure-and-prop-v1",
    "science/climate.svg": "semantic-multipart-v1",
    "science/translation.svg": "semantic-multipart-v1",
    "locations/graph.svg": "semantic-multipart-v1",
    "people/creator.svg": "figure-and-prop-v1",
    "people/firefighter.svg": "figure-and-prop-v1",
    "science/courage.svg": "figure-and-prop-v1",
    "people/trust.svg": "figure-and-prop-v1",
    "patterns/cube.svg": "semantic-multipart-v1",
}


def main() -> None:
    for source, review_class in REVIEWED.items():
        path = PUA / source
        tree = ET.parse(path)
        root = tree.getroot()
        root.set("data-intentional-components", review_class)
        root.set("data-component-review", "severity-contact-sheet-2026-08-v1")
        tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"marked {len(REVIEWED)} visually reviewed multi-part PUA compositions")


if __name__ == "__main__":
    main()
