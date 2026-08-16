"""Small dependency-free readers for OpenMoji's generated index."""

from __future__ import annotations

import html
import re
from pathlib import Path


INDEX_ROWS = re.compile(r"<tr>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
INDEX_CELLS = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
INDEX_TAGS = re.compile(r"<[^>]+>")


def openmoji_labels(index: Path) -> dict[str, str]:
    """Read index labels keyed by uppercase SVG filename."""
    if not index.exists():
        return {}
    labels: dict[str, str] = {}
    text = index.read_text(encoding="utf-8")
    for row in INDEX_ROWS.findall(text):
        cells = [
            html.unescape(INDEX_TAGS.sub("", cell)).strip()
            for cell in INDEX_CELLS.findall(row)
        ]
        if len(cells) < 8 or not re.fullmatch(r"[0-9A-Fa-f]+(?:-[0-9A-Fa-f]+)*", cells[4]):
            continue
        if cells[7]:
            labels[f"{cells[4].upper()}.SVG"] = cells[7].strip().title()
    return labels
