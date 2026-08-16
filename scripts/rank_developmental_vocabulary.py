#!/usr/bin/env python3
"""Rank Emojinq glyphs by developmental vocabulary and visual treatment.

This is a transparent first-pass curriculum classifier, not an age claim. It
creates a reviewable ordering from concrete first words to naturalist
referents, then expressive human/emotional concepts, and finally scenes,
systems, and abstractions.
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHAPES = {"path", "line", "polyline", "polygon", "rect", "circle", "ellipse"}
FAMILY_ROOTS = {
    "gray-all": ROOT / "assets/gray-all",
    "alpha-ink": ROOT / "assets/alpha-ink",
    "divination": ROOT / "assets/divination",
    "pua": ROOT / "assets/pua",
}

STAGES = {
    1: {
        "id": "first-words",
        "name": "First words",
        "description": "A single familiar referent rendered with enough clear sumi-e gestures for immediate toddler recognition.",
        "art_direction": "simple-sumi-e",
    },
    2: {
        "id": "naturalist",
        "name": "Naturalist referents",
        "description": "A specific animal, plant, food, tool, or place with enough anatomy to identify it.",
        "art_direction": "naturalist-ink-study",
    },
    3: {
        "id": "emotion-and-relationship",
        "name": "Emotions and relationships",
        "description": "An expressive face, body state, gesture, or relationship shown through posture and brush movement.",
        "art_direction": "expressive-figure-study",
    },
    4: {
        "id": "scenes-and-ideas",
        "name": "Scenes and ideas",
        "description": "A multi-part scene, social role, cultural reference, system, or abstract idea.",
        "art_direction": "contextual-ink-scene",
    },
}

ALPHA_STAGE = {
    "id": "literacy-symbols",
    "name": "Literacy symbols",
    "description": "Alphabetic, numeric, and punctuation glyphs; ranked separately from image vocabulary.",
    "art_direction": "calligraphic-letterform",
}

# PUA category defaults are intentionally explicit. Previously every concept
# that escaped the word lists became an ``unreviewed-referent`` and was then
# admitted to the toddler-object gate, which mislabeled actions such as
# ``create`` and abstractions such as ``value`` as concrete objects.
PUA_OBJECT_REFERENTS = {
    "arch", "axle", "beam", "bill", "board", "bowl", "brush", "canvas",
    "caravan", "castle", "chalk", "circuit", "clay", "computer", "currency", "doll",
    "doorframe", "drum", "engine", "fork", "foundation", "frame", "game",
    "gift", "goods", "handle", "knife", "letter", "lever", "mortar", "motor",
    "mural", "nail", "note", "oven", "paint", "pan", "port", "pot",
    "pottery", "print", "pulley", "pump", "puzzle", "recipe", "robot",
    "roof", "rope", "sandbox", "screw", "sculpture", "sign", "slide",
    "sock", "spice", "stage", "steam", "stove", "swing", "switch",
    "tower", "treasure", "valve", "wagon", "whistle", "windowpane", "forest",
}
PUA_ROCKET_REFERENTS = {"booster", "capsule", "lunar-lander", "rover"}
PUA_CASTALIA_REFERENTS = {
    "maker-seal", "research-submarine", "puppet-left-hand",
    "puppet-right-hand", "puppet-shoe", "pirate-ship", "police-box",
}
PUA_BODY_REFERENTS = {"blood", "bones", "muscles", "nerves", "skin", "stomach"}
PUA_BRC_REFERENTS = {"art-car", "temple"}
PUA_ANIMAL_REFERENTS = {"calf", "lamb", "squirrel"}
PUA_COSMOS_REFERENTS = {
    "sun", "earth", "moon", "comet", "asteroid", "star", "galaxy", "satellite",
    "space-station", "probe", "rover", "meteor", "asteroid-belt", "nebula",
    "black-hole", "eclipse",
}
PUA_LOCATION_REFERENTS = {
    "academy", "archive", "bakery", "barn", "bench", "burrow", "cafe",
    "canyon", "cave", "ceiling", "coast", "crossing", "delta", "den", "dock",
    "encyclopedia", "glacier", "hive", "jungle", "laboratory", "lake", "library",
    "market", "museum", "net", "park", "pasture", "plateau", "reef", "rug",
    "sand", "savanna", "shell", "sidewalk", "sign", "silo", "spring", "store",
    "street", "theater", "tide", "tower", "tundra", "valley", "wave", "workshop",
}
PUA_PEOPLE_REFERENTS = {"clothing", "diaper", "food", "gift", "shelter", "shrine", "stroller", "temple"}
PUA_PLANT_REFERENTS = {
    "bud", "compost", "dirt", "fruit", "log", "moss", "nest", "oak", "pine",
    "root", "seed", "soil", "sprout", "stem", "stream", "tool",
}
PUA_SCIENCE_REFERENTS = {
    "body", "clinic", "engine", "fossil", "gift", "globe", "medicine", "planet",
    "relic", "reservoir", "sensor", "server", "tool", "vaccine", "windmill",
}
PUA_WHOLE_REFERENT_CATEGORIES = {
    "adventure", "dinosaurs", "farm", "flora", "herbs",
    "materials", "sea_creatures", "weather_sky",
}


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def codepoint_key(entry: dict) -> str:
    cps = entry.get("codepoints") or []
    return "-".join(f"{int(cp):04X}" for cp in cps)


def label_for(entry: dict) -> str:
    return normalize(" ".join(
        str(entry.get(key, ""))
        for key in ("label", "name", "id", "source", "group")
    ))


def svg_metrics(family: str, source: str | None) -> dict:
    """Count visible SVG marks without mistaking TTF outlines for strokes.

    A single SVG ``path`` can contain several independent brush gestures. SVG
    move-to commands start those subpaths, so the stroke metric counts those
    gestures rather than only counting DOM elements.
    """
    if not source:
        return {"brush_stroke_count": 0, "stroke_only_marks": 0, "filled_marks": 0, "visible_marks": 0, "stroke_only_ready": False, "stroke_complexity": "none"}
    root = ET.parse(FAMILY_ROOTS[family] / source).getroot()
    visible = brush = stroke_only = filled = 0

    def visit(node: ET.Element, inherited_fill: str | None = None, inherited_stroke: str | None = None) -> None:
        nonlocal visible, brush, stroke_only, filled
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"defs", "clipPath", "mask", "symbol"}:
            return
        fill = node.get("fill", inherited_fill)
        stroke = node.get("stroke", inherited_stroke)
        if tag in SHAPES:
            mark_count = 1
            if tag == "path":
                d = node.get("d", "")
                move_count = len(re.findall(r"(?<![A-Za-z])[Mm]", d))
                mark_count = max(1, move_count)
            visible += mark_count
            classes = set(node.get("class", "").split())
            if node.get("data-ink-stroke") or classes.intersection({"ink-stroke", "ink-wash", "ink-dry"}):
                brush += mark_count
            if (fill or "none").lower() == "none" and stroke and stroke.lower() != "none":
                stroke_only += mark_count
            elif fill and fill.lower() != "none":
                filled += mark_count
        for child in node:
            visit(child, fill, stroke)

    visit(root)
    if not brush:
        brush = stroke_only
    if brush == 0:
        band = "none"
    elif brush <= 3:
        band = "1-3"
    elif brush <= 8:
        band = "4-8"
    elif brush <= 16:
        band = "9-16"
    else:
        band = "17+"
    return {
        "brush_stroke_count": brush,
        "stroke_only_marks": stroke_only,
        "filled_marks": filled,
        "visible_marks": visible,
        "stroke_only_ready": bool(brush and not filled),
        "stroke_complexity": band,
    }


def classify(label: str, source: str, *, alpha: bool = False, divination: bool = False) -> tuple[int | None, str, str]:
    if alpha:
        return None, "literacy", "separate literacy track"
    if divination:
        return 4, "symbolic", "cultural and symbolic vocabulary"

    tokens = set(label.split())

    # Route every PUA source before broad Unicode word matching. Substrings such
    # as ``farm`` in ``farmer`` and category names such as ``locations`` once
    # admitted roles, countries, and abstractions to the object-recognition
    # queue. The explicit sets below describe only things that can reasonably
    # be shown as a specific physical subject without relying on their label.
    if "/" in source and not source.startswith(("1F", "00", "20")):
        category, _, filename = source.partition("/")
        stem = Path(filename).stem
        if category in PUA_WHOLE_REFERENT_CATEGORIES:
            return 2, "referent", "reviewed physical or natural referent"
        if category == "animals":
            if stem in PUA_ANIMAL_REFERENTS:
                return 2, "referent", "reviewed individual animal referent"
            return 4, "context", "animal group, behavior, or ecological role"
        if category == "body":
            if stem in PUA_BODY_REFERENTS:
                return 2, "referent", "reviewed physical anatomy referent"
            return 3, "expression", "reviewed body action or state"
        if category == "brc":
            if stem in PUA_BRC_REFERENTS:
                return 2, "referent", "reviewed physical story-world referent"
            return 4, "context", "reviewed person or event-specific referent"
        if category == "castalia":
            if stem in PUA_CASTALIA_REFERENTS:
                return 2, "referent", "reviewed physical story-world referent"
            return 4, "context", "reviewed character, emblem, or narrative scene"
        if category == "cosmos":
            if stem in PUA_COSMOS_REFERENTS:
                return 2, "referent", "reviewed visually distinct astronomical referent"
            return 4, "context", "named world or astronomical notation needing context"
        if category == "cave_locations":
            return 4, "context", "named story-world location requires narrative context"
        if category == "faerie":
            if stem == "dew-drop":
                return 2, "referent", "reviewed physical story-world referent"
            if stem.startswith("season-"):
                return 4, "context", "reviewed seasonal scene"
            return 3, "expression", "reviewed figure gesture or action"
        if category == "locations":
            if stem in PUA_LOCATION_REFERENTS:
                return 2, "referent", "reviewed physical place or object referent"
            return 4, "context", "named culture, region, system, or social setting"
        if category == "objects":
            if stem in PUA_OBJECT_REFERENTS:
                return 2, "referent", "reviewed physical object or place referent"
            return 4, "context", "reviewed action, role, scene, or abstract concept"
        if category == "patterns":
            return 4, "symbolic", "reviewed color, shape, or graphic notation"
        if category == "people":
            if stem in PUA_PEOPLE_REFERENTS:
                return 2, "referent", "reviewed physical object or place referent"
            return 3, "expression", "reviewed person, relationship, role, or social concept"
        if category == "plants":
            if stem in PUA_PLANT_REFERENTS:
                return 2, "referent", "reviewed physical plant or material referent"
            return 4, "context", "reviewed growth action or process"
        if category == "rockets":
            if stem in PUA_ROCKET_REFERENTS:
                return 2, "referent", "reviewed spacecraft referent"
            return 4, "context", "reviewed mission action or operational scene"
        if category == "science":
            if stem in PUA_SCIENCE_REFERENTS:
                return 2, "referent", "reviewed physical scientific referent"
            return 4, "context", "reviewed system, notation, process, or abstract concept"
        return 2, "unreviewed-referent", "unknown PUA category; manual review required"

    # A ZWJ composition may contain a first-word token, but it is no longer the
    # single familiar referent promised by the first-words tier (for example,
    # firefighter = person + fire engine).  Keep those scenes for later review.
    if {"zero", "width", "joiner"}.issubset(tokens):
        return 4, "context", "multi-part emoji composition"

    def has_word(*words: str) -> bool:
        return any(word in tokens for word in words)

    # Explicit early concrete vocabulary.  Match concrete nouns, not color,
    # number, or symbol adjectives embedded in Unicode names (for example,
    # "Playing Card Black Joker" must not enter the toddler-object queue just
    # because it contains "black").
    first_words = {
        "baby", "boy", "girl", "child", "dog", "cat", "bird", "fish", "sun",
        "moon", "star", "cloud", "rain", "snow", "fire", "water", "tree", "flower",
        "apple", "banana", "bread", "cake", "egg", "milk", "coffee", "tea", "heart",
        "eye", "ear", "hand", "foot", "home", "house", "car", "bus", "train", "boat",
        "ball", "book", "key", "bell", "gift", "phone", "camera", "clock", "money",
    }
    if has_word(*first_words):
        return 1, "concrete", "familiar single referent"

    symbolic_words = {
        "asterisk", "card", "chess", "circle", "copyright", "digit", "exclamation",
        "hexagon", "hyphen", "keycap", "mahjong", "minus", "pentagon", "plus",
        "question", "registered", "square", "symbol", "triangle",
    }
    if has_word(*symbolic_words):
        return 4, "symbolic", "symbol or notation rather than a concrete object"

    # Specific living things and material referents benefit from naturalist
    # anatomy, texture, and species cues rather than symbolic outlines.
    naturalist_categories = {
        "animals", "dinosaurs", "sea creatures", "farm", "flora", "herbs", "plants",
        "locations", "materials", "food", "drink", "transportation", "nature",
    }
    if any(category in label or category.replace(" ", "_") in source for category in naturalist_categories):
        return 2, "referent", "specific natural or material subject"
    naturalist_words = {
        "bee", "butterfly", "squirrel", "whale", "shark", "dolphin", "octopus", "crab",
        "dinosaur", "rocket", "planet", "mushroom", "tomato", "watermelon", "melon",
        "rose", "pine", "oak", "fern", "lavender", "rosemary", "canyon", "glacier",
        "lighthouse", "bridge", "castle", "microscope", "hammer", "needle", "brush",
    }
    if has_word(*naturalist_words):
        return 2, "referent", "specific subject needs identifying anatomy"

    # Human affect and bodily action come after concrete referents, but before
    # multi-object scenes and abstract concepts.
    emotion_words = {
        "happy", "sad", "angry", "fear", "surprise", "love", "hate", "joy", "hope",
        "pride", "shame", "calm", "kindness", "compassion", "care", "trust", "peace",
        "help", "welcome", "hug", "kiss", "clap", "dance", "laugh", "cry", "smile",
        "anger", "sadness", "awe", "courage", "humility", "health", "pain", "sleep",
        "breath", "pulse", "muscles", "bones", "skin", "stomach", "blood", "nerves",
        "walk", "run", "reach", "push", "pull", "kick", "grab", "wave", "choice",
        "identity", "relationship", "team", "friend", "family", "community",
    }
    if has_word(*emotion_words):
        return 3, "expression", "emotion, body state, or relationship"
    # Everything that implies an action, role, social arrangement, system, or
    # abstraction is deliberately placed late in the curriculum.
    scene_words = {
        "work", "cook", "build", "teach", "learn", "study", "write", "read", "artist",
        "farmer", "baker", "mechanic", "astronaut", "leader", "mentor", "ancestor", "hero",
        "city", "village", "market", "library", "museum", "laboratory", "school", "theater",
        "conversation", "conflict", "cooperation", "constitution", "culture", "justice",
        "science", "history", "language", "memory", "meaning", "knowledge", "question",
        "why", "how", "because", "evidence", "theory", "algorithm", "network", "system",
        "pattern", "change", "future", "past", "time", "calendar", "tarot", "zodiac",
        "planet", "rocket", "satellite", "station", "divination", "brc",
    }
    if has_word(*scene_words):
        return 4, "context", "scene, role, system, or abstract idea"

    if any(token in source for token in ("people/", "body/")):
        return 3, "expression", "human or bodily concept"

    return 2, "unreviewed-referent", "default concrete referent; manual review needed"


def load_entries() -> list[dict]:
    result: list[dict] = []
    sources = [
        ("gray-all", ROOT / "assets/gray-all/manifest.json", False, False),
        ("alpha-ink", ROOT / "assets/alpha-ink/manifest.json", True, False),
        ("divination", ROOT / "assets/divination/manifest.json", False, True),
        ("pua", ROOT / "assets/pua/manifest.json", False, False),
    ]
    for family, path, alpha, divination in sources:
        for entry in json.loads(path.read_text(encoding="utf-8")):
            label = label_for(entry)
            level, kind, reason = classify(label, str(entry.get("source", "")), alpha=alpha, divination=divination)
            metrics = svg_metrics(family, entry.get("source"))
            result.append({
                "family": family,
                "id": f"{family}:{entry.get('name') or entry.get('label') or codepoint_key(entry)}",
                "name": entry.get("label") or entry.get("name") or entry.get("source"),
                "source": entry.get("source"),
                "codepoints": entry.get("codepoints", []),
                "developmental_level": level,
                "track": kind,
                "reason": reason,
                "confidence": "high" if kind != "unreviewed-referent" else "medium",
                "art_direction": ALPHA_STAGE["art_direction"] if alpha else STAGES[level]["art_direction"],
                **metrics,
            })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "assets/developmental-vocabulary.json")
    args = parser.parse_args()
    entries = load_entries()
    summary = Counter(
        "literacy" if entry["developmental_level"] is None else str(entry["developmental_level"])
        for entry in entries
    )
    payload = {
        "version": 1,
        "method": "heuristic-v2-svg-subpaths",
        "note": "Developmental ordering for art direction and review; not an age-rating system.",
        "stages": {str(key): value for key, value in STAGES.items()},
        "literacy_track": ALPHA_STAGE,
        "summary": dict(summary),
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ranked {len(entries)} glyph records: " + ", ".join(f"{key}={value}" for key, value in sorted(summary.items())))


if __name__ == "__main__":
    main()
