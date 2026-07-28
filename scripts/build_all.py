#!/usr/bin/env python3
"""Build the line-only Castalia treatment for every Noto SVG input."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path

from collapse_lines import collapse
from import_noto_svg import convert
import xml.etree.ElementTree as ET

CODEPOINTS = re.compile(r"^emoji_u([0-9a-f]+(?:[_-][0-9a-f]+)*)\.svg$", re.IGNORECASE)


def entry(source: Path) -> dict[str, object] | None:
    match = CODEPOINTS.match(source.name)
    if not match:
        return None
    codepoints = [int(value, 16) for value in re.split(r"[_-]", match.group(1))]
    return {"name": source.stem.removeprefix("emoji_u"), "source": source.name, "codepoints": codepoints}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("assets/line-all"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        for source in sorted(args.source_dir.glob("emoji_u*.svg")):
            metadata = entry(source)
            if metadata is None:
                continue
            area = temp / source.name
            target = args.output_dir / source.name
            convert(source, area, str(metadata["name"]))
            tree = ET.parse(area)
            collapse(tree.getroot())
            tree.write(target, encoding="utf-8", xml_declaration=True)
            entries.append(metadata)
    (args.output_dir / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(f"built {len(entries)} line glyphs in {args.output_dir}")


if __name__ == "__main__":
    main()
