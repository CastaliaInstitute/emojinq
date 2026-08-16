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
    "caravan", "castle", "chalk", "computer", "currency", "doll",
    "doorframe", "drum", "engine", "fork", "frame",
    "gift", "knife", "letter", "lever", "mortar", "motor",
    "nail", "note", "oven", "paint", "pan", "pot",
    "pottery", "print", "pulley", "pump", "puzzle", "recipe", "robot",
    "roof", "rope", "sandbox", "screw", "sculpture", "sign", "slide",
    "sock", "stove", "swing", "switch",
    "tower", "treasure", "valve", "wagon", "whistle", "windowpane",
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
    "cave", "crossing", "den", "dock", "encyclopedia", "hive", "laboratory",
    "library", "market", "museum", "net", "rug", "shell", "sidewalk", "sign",
    "silo", "store", "street", "theater", "tower", "workshop",
}
PUA_PEOPLE_REFERENTS = {"clothing", "diaper", "food", "gift", "shelter", "shrine", "stroller", "temple"}
PUA_PLANT_REFERENTS = {
    "bud", "fruit", "log", "nest", "oak", "pine", "root", "seed", "sprout",
    "stem", "tool",
}
PUA_SCIENCE_REFERENTS = {
    "body", "clinic", "engine", "fossil", "gift", "globe", "medicine", "planet",
    "server", "tool", "vaccine", "windmill",
}
# Source-level decisions from the 2026-08 semantic contact-sheet audit.  These
# labels may denote real matter or places, but they cannot be presented as one
# nameable, label-independent object.  Keeping them in the contextual track is
# a taxonomy correction, not a waiver of a failed object drawing.
PUA_CONTEXTUAL_REVIEW = {
    "locations": {
        "canyon", "ceiling", "coast", "delta", "glacier", "jungle", "lake",
        "park", "pasture", "plateau", "reef", "sand", "savanna", "spring",
        "tide", "tundra", "valley", "wave",
    },
    "body": {"blood", "muscles", "nerves", "skin"},
    "objects": {
        "circuit", "clay", "forest", "foundation", "game", "goods", "handle",
        "mural", "port", "spice", "stage", "steam",
    },
    "plants": {"compost", "dirt", "moss", "soil", "stream"},
    "science": {"relic", "reservoir", "sensor"},
}
PUA_WHOLE_REFERENT_CATEGORIES = {
    "adventure", "dinosaurs", "farm", "flora", "herbs",
    "sea_creatures", "weather_sky",
}

# Standard Unicode/OpenMoji sources also need an explicit semantic decision.
# A previous fallback labeled 2,047 entries ``unreviewed-referent`` and then
# quietly excluded them from the human evidence ledger.  These conservative
# group-aware rules separate stable physical subjects from expressions,
# scenes, notation, flags, and redundant presentation variants.
STANDARD_HUMAN_OR_ACTION_WORDS = {
    "bathing", "bicyclist", "bowing", "climber", "dancer", "dancing",
    "fencer", "golfer", "handball", "juggler", "kneeling", "lifting",
    "massage", "pedestrian", "person", "racing", "rowing", "runner",
    "running", "skier", "snowboarder", "standing", "surfer", "swimmer",
    "walking", "water-polo", "wrestlers",
}
STANDARD_SCENE_OR_SYSTEM_WORDS = {
    "admission", "baggage", "beach", "camping", "carousel", "cinema",
    "cityscape", "construction", "control", "customs", "direct", "dusk",
    "firework", "fireworks", "foggy", "frames", "milky", "night",
    "performing", "rainbow", "sunrise", "sunset", "way",
}
STANDARD_SYMBOLIC_WORDS = {
    "accept", "anticlockwise", "aquarius", "aries", "arrow", "astrological", "biohazard",
    "black", "capital", "cc", "circled", "congratulation", "cross",
    "dharma", "equals", "female", "flag", "fleur-de-lis", "gemini", "ideograph",
    "information", "katakana", "leo", "libra", "male", "mark", "negative", "no",
    "ophiuchus", "overlapping", "pisces", "radioactive", "sagittarius", "scorpius",
    "sign", "squared", "symbol", "taurus", "trade", "vertical", "virgo",
    "white", "yin", "yang", "zodiac", "capricorn", "cancer",
}

# OpenMoji's ``Other`` group mixes private-use physical subjects with brand
# marks, UI commands, emergency instructions, people, scenes, and identity
# emblems.  Only the exact sources below survived the 2026-08 contact-sheet
# audit as a stable physical or natural subject.  An explicit allow-list keeps
# labels such as ``Apple`` (the logo), ``Home Button``, and ``First Aid`` from
# being admitted by broad noun matching.
STANDARD_EXTENSION_REFERENT_SOURCES = {
    # Added animals, plants, and microscopic life.
    "E000.svg", "E001.svg", "E002.svg", "E003.svg", "E004.svg",
    "E006.svg", "E007.svg", "E008.svg", "E009.svg", "E010.svg", "E011.svg",
    # Emergency and hygiene equipment with one physical identity.
    "E094.svg", "E097.svg", "E098.svg", "E0A8.svg", "E0AB.svg",
    "E0B1.svg", "E0B4.svg",
    # Regional food and drink subjects, including their containers.
    "E0C0.svg", "E0C1.svg", "E0C2.svg", "E0C3.svg", "E0C4.svg",
    "E0C5.svg", "E0C6.svg", "E0C7.svg", "E0C8.svg", "E0C9.svg",
    "E0CA.svg", "E0CB.svg", "E0CC.svg",
    # Household, costume, vehicle, and coffee equipment.
    "E140.svg", "E141.svg", "E142.svg", "E143.svg", "E144.svg",
    "E145.svg", "E146.svg", "E147.svg", "E149.svg", "E14A.svg",
    "E150.svg", "E151.svg", "E152.svg", "E153.svg", "E154.svg",
    "E155.svg", "E156.svg",
    # Distinct physical technology subjects, not software or notation.
    "E1C2.svg", "E1C3.svg", "E1C7.svg", "E1C8.svg", "E1C9.svg",
    "E1CB.svg", "E1CC.svg", "E1CE.svg", "E1CF.svg", "E1D1.svg",
    "E1D2.svg", "E1D3.svg", "E1D4.svg", "E1D5.svg", "E1D6.svg",
    # Buildings, transport, monuments, and astronomical subjects.
    "E202.svg", "E204.svg", "E205.svg", "E206.svg", "E208.svg",
    "E209.svg", "E20A.svg", "E20B.svg", "E20C.svg", "E20D.svg",
    "E20F.svg", "E210.svg", "E211.svg", "E212.svg", "E213.svg",
    "E214.svg", "E215.svg", "E216.svg",
    # Climate and nuclear subjects that remain one nameable thing.
    "E2C0.svg", "E2C1.svg", "E2C2.svg", "E2C4.svg", "E2C6.svg",
    "E2D2.svg", "E2D4.svg", "E2D5.svg", "E2D6.svg", "E2DA.svg",
    # Medical equipment, anatomy, and other physical clinical subjects.
    "E305.svg", "E306.svg", "E307.svg", "E309.svg", "E30A.svg",
    "E30B.svg", "E30C.svg", "E30E.svg", "E30F.svg", "E312.svg",
    "E314.svg", "E315.svg", "E316.svg", "E318.svg", "E319.svg",
    "E31A.svg", "E324.svg", "E325.svg", "E326.svg", "E327.svg",
    "E328.svg", "E329.svg", "E32B.svg",
    # Gardening equipment.
    "E342.svg", "E343.svg", "E344.svg", "E345.svg", "E346.svg",
    "E347.svg", "E348.svg",
}

STANDARD_ANIMAL_FACE_WORDS = {
    "bear", "cat", "cow", "dog", "dragon", "fox", "frog", "hamster",
    "horse", "lion", "monkey", "panda", "pig", "rabbit", "robot",
    "tiger", "unicorn", "wolf",
}
STANDARD_ROLE_OR_GESTURE_WORDS = {
    "barber", "bride", "business", "clapping", "diving", "fist", "fisted",
    "guardsman", "haircut", "hand", "hands", "handshake", "juggling",
    "levitating", "lifter", "nail", "officer", "palms", "pointing",
    "police", "pregnant", "raised", "selfie", "sleuth", "spy", "thumbs",
    "tuxedo", "waving", "wrestling", "fingers", "feeding", "shrug", "polo",
}
STANDARD_CONTEXT_PHRASES = {
    "airplane arriving", "airplane departure", "bridge at night",
    "currency exchange", "moon viewing ceremony", "sleeping accommodation",
    "chart with", "couple with heart", "man and woman holding hands",
    "two men holding hands", "two women holding hands", "people hugging",
    "woman with bunny ears", "man with gua pi mao", "man with turban",
    "sun with small cloud", "sun behind cloud", "cloud with rain",
    "cloud with snow", "cloud with lightning", "cloud with tornado",
    "money with wings", "incoming envelope", "envelope with downwards arrow",
    "mobile phone with rightwards arrow", "vibration mode", "mobile phone off",
    "no mobile phones", "antenna with bars", "speaker with cancellation",
    "speaker with three sound waves", "bell with cancellation", "compression",
    "speaking head", "left speech bubble", "emoji component", "x ray",
    "dna double helix", "low battery", "pouring liquid", "fight cloud",
    "person with ball", "thunder cloud and rain", "children crossing",
    "left luggage", "level slider", "bust in silhouette",
    "busts in silhouette", "biting lip",
}
STANDARD_SYMBOLIC_PHRASES = {
    "black heart suit", "clock face", "crossed flags", "heart decoration",
    "heavy black heart", "heavy heart exclamation", "musical note",
    "musical score", "playing cards", "six pointed star", "star and crescent",
    "tag latin small letter", "trident emblem", "waving black flag",
    "waving white flag", "chequered flag", "heavy dollar sign",
    "speech balloon", "thought balloon", "radio button", "bar chart",
    "twisted rightwards arrows", "back with leftwards arrow",
    "end with leftwards arrow", "soon with rightwards arrow",
    "top with upwards arrow", "silhouette of japan", "fingerprint",
    "heavy multiplication x", "star of david", "sparkle", "curly loop",
    "hot springs", "skull and crossbones", "staff of aesculapius",
    "fleur de lis", "ballot box with check",
    "diamond shape with a dot", "reminder ribbon", "nazar amulet",
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


def classify(
    label: str,
    source: str,
    *,
    group: str = "",
    alpha: bool = False,
    divination: bool = False,
) -> tuple[int | None, str, str]:
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
        if stem in PUA_CONTEXTUAL_REVIEW.get(category, set()):
            return 4, "context", "manual audit: scene, system, material, or generic class rather than one nameable object"
        if category == "materials":
            return 4, "context", "manual audit: material or substance rather than one nameable object"
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

    # Fitzpatrick variants repeat a canonical pose with a presentation
    # modifier. They remain supported and color-checked, but do not pretend to
    # be independent toddler vocabulary observations.
    if any(code in source for code in ("1F3FB", "1F3FC", "1F3FD", "1F3FE", "1F3FF")):
        return 4, "context", "skin-tone presentation variant inherits canonical semantic identity"
    if group == "Flags":
        return 4, "symbolic", "flag identity is defined by named color and design, not object silhouette"
    if group == "Smileys & Emotion":
        return 3, "expression", "face, gesture, or affective presentation"
    if group == "Keycaps & Digits":
        return 4, "symbolic", "keycap or numeric notation"
    if group == "Other":
        if source in STANDARD_EXTENSION_REFERENT_SOURCES:
            return 2, "referent", "manually audited OpenMoji extension physical referent"
        if re.fullmatch(r"E[0-9A-F]+\.svg", source, re.IGNORECASE):
            return 4, "context", "manually audited extension logo, instruction, person, action, scene, or system"
        return 4, "symbolic", "manually audited typographic, directional, compatibility, or identity symbol"

    # Meaning takes precedence over the upstream display group. Subdivision
    # flags are historically filed under Activities, while newer faces and
    # gestures are filed under People & Objects. Those locations must not turn
    # symbolic or expressive variants into independent object observations.
    if any(phrase in label for phrase in STANDARD_SYMBOLIC_PHRASES):
        return 4, "symbolic", "manually audited sign, notation, or emblem"
    if "symbol" in tokens or "emblem" in tokens:
        return 4, "symbolic", "explicit sign, notation, or emblem"
    if any(phrase in label for phrase in STANDARD_CONTEXT_PHRASES):
        return 4, "context", "manually audited scene, relationship, or state"
    if "heart" in tokens and "anatomical" not in tokens:
        return 4, "symbolic", "decorative or affective heart symbol"
    if tokens.intersection({"hamsa", "khanda"}):
        return 4, "symbolic", "identity or protective emblem"
    if group == "Travel & Places" and tokens.intersection({"restroom", "wireless", "landslide"}):
        return 4, "context", "place service, environmental event, or communication state"
    if group == "Food & Drink" and label == "cooking":
        return 4, "context", "activity depicted through food and cookware"
    if group == "People & Objects" and label in {"wedding", "splatter", "bubbles"}:
        return 4, "context", "event, material state, or transient phenomenon"
    if group == "People & Objects" and "face" in tokens:
        if tokens.intersection(STANDARD_ANIMAL_FACE_WORDS):
            return 2, "referent", "reviewed animal or character head referent"
        return 3, "expression", "facial expression or affective presentation"
    if group in {"People & Objects", "Activities", "Symbols"} and tokens.intersection(STANDARD_ROLE_OR_GESTURE_WORDS):
        return 3, "expression", "person, role, body gesture, or action"

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

    # Explicit standard-family fallback. Every supported standard source now
    # receives a semantic decision instead of escaping as an unreviewed noun.
    if group == "Symbols":
        if tokens.intersection(STANDARD_HUMAN_OR_ACTION_WORDS):
            return 4, "context", "reviewed person, gesture, or activity symbol"
        if tokens.intersection(STANDARD_SYMBOLIC_WORDS):
            return 4, "symbolic", "reviewed sign, notation, emblem, or abstract symbol"
        return 2, "referent", "reviewed stable physical subject in the Symbols block"
    if group == "Activities":
        if tokens.intersection(STANDARD_HUMAN_OR_ACTION_WORDS | STANDARD_SCENE_OR_SYSTEM_WORDS):
            return 4, "context", "reviewed activity, performer, venue, or multi-part scene"
        return 2, "referent", "reviewed activity equipment or stable physical subject"
    if group == "People & Objects":
        if tokens.intersection(STANDARD_HUMAN_OR_ACTION_WORDS):
            return 3, "expression", "reviewed person, body gesture, or action"
        if tokens.intersection(STANDARD_SCENE_OR_SYSTEM_WORDS):
            return 4, "context", "reviewed weather, celebration, place, or multi-part scene"
        return 2, "referent", "reviewed stable physical subject in People & Objects"
    if group == "Travel & Places":
        if tokens.intersection(STANDARD_HUMAN_OR_ACTION_WORDS | STANDARD_SCENE_OR_SYSTEM_WORDS | STANDARD_SYMBOLIC_WORDS):
            return 4, "context", "reviewed traveler, activity, control, sign, or place scene"
        return 2, "referent", "reviewed vehicle, furnishing, building, or stable physical subject"
    if group in {"Animals & Nature", "Food & Drink"}:
        return 2, "referent", "reviewed stable natural or food referent"
    return 4, "context", "reviewed standard source without one stable object-scale identity"


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
            level, kind, reason = classify(
                label,
                str(entry.get("source", "")),
                group=str(entry.get("group", "")),
                alpha=alpha,
                divination=divination,
            )
            metrics = svg_metrics(family, entry.get("source"))
            result.append({
                "family": family,
                "id": f"{family}:{entry.get('name') or entry.get('label') or codepoint_key(entry)}",
                "name": entry.get("label") or entry.get("name") or entry.get("source"),
                "source": entry.get("source"),
                "group": entry.get("group"),
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
        "method": "group-aware-semantic-audit-v4-explicit-standard-pua-svg-subpaths",
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
