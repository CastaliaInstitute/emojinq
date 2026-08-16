#!/usr/bin/env python3
"""Lock category-complete toddler reviews for standard Unicode glyphs."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
COLOR_ASSETS = ROOT / "assets" / "color-all"
MANIFEST = ASSETS / "manifest.json"
REVIEWED = {
    "Food & Drink": (66, "food-complete-v1"),
    "Animals & Nature": (89, "animals-nature-complete-v1"),
    "Travel & Places": (202, "travel-places-complete-v1"),
    "Activities": (266, "activities-complete-v1"),
    "People & Objects": (2667, "people-objects-complete-v1"),
    "Flags": (285, "flags-complete-v1"),
    "Smileys & Emotion": (197, "smileys-emotion-complete-v1"),
    "Symbols": (219, "symbols-complete-v1"),
    "Keycaps & Digits": (12, "keycaps-digits-complete-v1"),
    "Other": (492, "other-complete-v1"),
}
NEWLY_REVIEWED = {"Smileys & Emotion", "Symbols", "Keycaps & Digits", "Other"}
QUEER_FLAGS = {f"E{code:X}.svg" for code in range(0x420, 0x436)}
LINEAR_SYMBOLS = {"23FD.svg"}
PEOPLE_OBJECT_NAME_OVERRIDES = {
    "1FA89.svg": "Harp",
    "1FA8A.svg": "Trombone",
    "1FA8E.svg": "Treasure Chest",
    "1FA8F.svg": "Shovel",
    "1FABE.svg": "Leafless Tree",
    "1FAC6.svg": "Fingerprint",
    "1FAC8.svg": "Hairy Creature",
    "1FACD.svg": "Orca",
    "1FADC.svg": "Root Vegetable",
    "1FADF.svg": "Splatter",
    "1FAE9.svg": "Face With Bags Under Eyes",
    "1FAEA.svg": "Distorted Face",
    "1FAEF.svg": "Fight Cloud",
}
PEOPLE_OBJECT_OUTLIERS = {"1F484.svg", "1FACD.svg"}
FOOD_OUTLIERS = {
    "1F330.svg",
    "1F34B-200D-1F7E9.svg",
    "1F357.svg",
    "1F358.svg",
    "1F359.svg",
    "1F35A.svg",
    "1F35E.svg",
    "1F364.svg",
    "1F365.svg",
    "1F36E.svg",
    "1F375.svg",
    "1F379.svg",
}
REPLACEMENT_WASHES = {"1F330.svg", "1F35E.svg"}
ANIMAL_FACES = {
    "1F42D.svg", "1F42E.svg", "1F42F.svg", "1F430.svg", "1F431.svg",
    "1F432.svg", "1F434.svg", "1F435.svg", "1F436.svg", "1F437.svg",
    "1F438.svg", "1F439.svg", "1F43A.svg", "1F43B.svg", "1F43C.svg",
}
ANIMAL_OUTLIERS = {"1F33D.svg", "1F33E.svg", "1F40B.svg", "1F41A.svg"}


def visible_bounds(path: Path) -> tuple[int, int, int]:
    with Image.open(path).convert("RGBA") as image:
        points = [
            (x, y)
            for y in range(image.height)
            for x in range(image.width)
            if image.getpixel((x, y))[3] >= 24
        ]
    if not points:
        return 0, 0, 0
    xs, ys = zip(*points)
    return max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, len(points)


def main() -> None:
    renderer = shutil.which("rsvg-convert")
    if not renderer:
        raise SystemExit("rsvg-convert is required for the 32px toddler gate")
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checked = 0
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="emojinq-toddler-standard-") as directory:
        raster_dir = Path(directory)
        for group, (expected, review_name) in REVIEWED.items():
            selected = [entry for entry in entries if entry.get("group") == group]
            if len(selected) != expected:
                failures.append(f"{group}: expected {expected} entries, found {len(selected)}")
                continue
            for entry in selected:
                source = ASSETS / entry["source"]
                root = ET.parse(source).getroot()
                if root.get("data-toddler-review") != review_name:
                    failures.append(f"{source}: missing {review_name} category review")
                if group in NEWLY_REVIEWED:
                    if not entry.get("label"):
                        failures.append(f"{source}: missing semantic identity")
                    if root.get("aria-label") != entry.get("label"):
                        failures.append(f"{source}: artwork identity does not match its manifest label")
                widths = [
                    float(element.get("stroke-width", "0"))
                    for element in root.iter()
                    if "stroke-width" in element.attrib
                ]
                uses_filled_brush_mass = root.get("data-ink-stroke-system") == "filled-brush-mass-v2"
                if (not widths or max(widths) < 1.25) and not uses_filled_brush_mass:
                    failures.append(f"{source}: no toddler-scale defining stroke")
                if entry["source"] in FOOD_OUTLIERS:
                    identifiers = {element.get("id") for element in root.iter()}
                    if not identifiers.intersection({"food-recognition-cues", "food-recognition-replacement"}):
                        failures.append(f"{source}: reviewed ambiguity cues are missing")
                if entry["source"] in ANIMAL_FACES and root.get("data-animal-face-source") != "openmoji-front-anatomy-v1":
                    failures.append(f"{source}: front-facing species anatomy is missing")
                if entry["source"] in ANIMAL_OUTLIERS and not any(
                    element.get("id") == "animal-recognition-cues" for element in root.iter()
                ):
                    failures.append(f"{source}: reviewed animal/botanical cues are missing")
                if entry["source"] == "1F6D8.svg":
                    if entry.get("label") != "Landslide" or root.get("aria-label") != "Landslide":
                        failures.append(f"{source}: Unicode 17 landslide identity is missing")
                if entry["source"] in PEOPLE_OBJECT_NAME_OVERRIDES:
                    expected_name = PEOPLE_OBJECT_NAME_OVERRIDES[entry["source"]]
                    if entry.get("label") != expected_name or root.get("aria-label") != expected_name:
                        failures.append(f"{source}: current Unicode identity {expected_name!r} is missing")
                if entry["source"] in PEOPLE_OBJECT_OUTLIERS and not any(
                    element.get("id") == "people-object-recognition-cues" for element in root.iter()
                ):
                    failures.append(f"{source}: reviewed concrete-object cues are missing")
                if entry["source"] == "1FACD.svg" and not any(
                    element.get("id") == "people-object-orca-ink-wash" for element in root.iter()
                ):
                    failures.append(f"{source}: monochrome orca lacks its defining black body wash")
                if entry["source"].startswith(("1F3F3-", "1F3F4-")) and not any(
                    element.get("id") == "activity-flag-recognition-cues" for element in root.iter()
                ):
                    failures.append(f"{source}: flag sequence lacks a pole and finial")
                if group == "Flags" and "-" in source.stem:
                    if not entry.get("label", "").startswith("Flag: "):
                        failures.append(f"{source}: composed flag lacks its country/region identity")
                    if root.get("aria-label") != entry.get("label"):
                        failures.append(f"{source}: flag artwork identity does not match its manifest label")
                    if not any(
                        element.get("id") == "standard-flag-recognition-cues"
                        for element in root.iter()
                    ):
                        failures.append(f"{source}: composed flag lacks pole, finial, and cloth folds")
                if entry["source"] in QUEER_FLAGS and not any(
                    element.get("id") == "extra-flag-recognition-cues" for element in root.iter()
                ):
                    failures.append(f"{source}: named pride flag lacks pole, finial, and cloth folds")
                png = raster_dir / f"{source.stem}.png"
                subprocess.run(
                    [renderer, "-w", "32", "-h", "32", str(source), "-o", str(png)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                width, height, pixels = visible_bounds(png)
                weak_shape = (
                    (width < 2 or height < 12 or pixels < 20)
                    if entry["source"] in LINEAR_SYMBOLS
                    else (width < 4 or height < 4 or pixels < 12)
                )
                if weak_shape:
                    failures.append(
                        f"{source}: weak 32px silhouette ({width}x{height}, {pixels} visible pixels)"
                    )
                color_source = COLOR_ASSETS / entry["source"]
                if not color_source.exists():
                    failures.append(f"{color_source}: familiar-color counterpart is missing")
                else:
                    color_root = ET.parse(color_source).getroot()
                    if entry["source"] in REPLACEMENT_WASHES and not any(
                        element.get("data-color-geometry") == "authored-recognition-silhouette-v1"
                        for element in color_root.iter()
                    ):
                        failures.append(f"{color_source}: wash does not follow the authored silhouette")
                    if entry["source"] in ANIMAL_FACES and not any(
                        element.get("id") == "animal-face-anatomy"
                        for element in color_root.iter()
                    ):
                        failures.append(f"{color_source}: color variant lacks restored front-face anatomy")
                    if entry["source"] in ANIMAL_OUTLIERS and not any(
                        element.get("id") == "animal-recognition-cues" for element in color_root.iter()
                    ):
                        failures.append(f"{color_source}: color variant lacks reviewed anatomy cues")
                    if entry["source"] == "1F6D8.svg" and color_root.get("aria-label") != "Landslide":
                        failures.append(f"{color_source}: color variant lacks the landslide identity")
                    if entry["source"] in PEOPLE_OBJECT_NAME_OVERRIDES:
                        expected_name = PEOPLE_OBJECT_NAME_OVERRIDES[entry["source"]]
                        if color_root.get("aria-label") != expected_name:
                            failures.append(
                                f"{color_source}: color variant lacks current Unicode identity {expected_name!r}"
                            )
                    if entry["source"] in PEOPLE_OBJECT_OUTLIERS and not any(
                        element.get("id") == "people-object-recognition-cues"
                        for element in color_root.iter()
                    ):
                        failures.append(f"{color_source}: color variant lacks reviewed object cues")
                    if entry["source"].startswith(("1F3F3-", "1F3F4-")) and not any(
                        element.get("id") == "activity-flag-recognition-cues"
                        for element in color_root.iter()
                    ):
                        failures.append(f"{color_source}: color flag sequence lacks a pole and finial")
                    if group == "Flags" and "-" in source.stem:
                        if color_root.get("aria-label") != entry.get("label"):
                            failures.append(f"{color_source}: color flag lacks its country/region identity")
                        if not any(
                            element.get("id") == "standard-flag-recognition-cues"
                            for element in color_root.iter()
                        ):
                            failures.append(
                                f"{color_source}: color flag lacks pole, finial, and cloth folds"
                            )
                    if entry["source"] in QUEER_FLAGS:
                        if color_root.get("aria-label") != entry.get("label"):
                            failures.append(f"{color_source}: pride-flag identity is missing")
                        if not any(
                            element.get("id") == "extra-flag-recognition-cues"
                            for element in color_root.iter()
                        ):
                            failures.append(f"{color_source}: pride flag lacks cloth anatomy")
                        familiar_colors = {
                            value.lower()
                            for element in color_root.iter()
                            for key in ("fill", "stroke")
                            if (value := element.get(key, "")).startswith("#")
                            and value.lower() not in {"#262421", "#302e2a", "#4a4943", "#66635b"}
                        }
                        if len(familiar_colors) < 2:
                            failures.append(f"{color_source}: pride flag design lacks familiar color contrast")
                    color_png = raster_dir / f"{source.stem}-color.png"
                    subprocess.run(
                        [renderer, "-w", "32", "-h", "32", str(color_source), "-o", str(color_png)],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    color_width, color_height, color_pixels = visible_bounds(color_png)
                    weak_color_shape = (
                        (color_width < 2 or color_height < 12 or color_pixels < 20)
                        if entry["source"] in LINEAR_SYMBOLS
                        else (color_width < 4 or color_height < 4 or color_pixels < 12)
                    )
                    if weak_color_shape:
                        failures.append(
                            f"{color_source}: weak 32px color silhouette "
                            f"({color_width}x{color_height}, {color_pixels} visible pixels)"
                        )
                checked += 1
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"standard toddler category gate checked: {checked} glyphs across every manifest group "
        "in monochrome and familiar color at 32px"
    )


if __name__ == "__main__":
    main()
