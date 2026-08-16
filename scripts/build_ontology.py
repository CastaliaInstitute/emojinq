#!/usr/bin/env python3
"""Build the complete, deterministic Emojinq semantic/orientation ontology.

Artwork and semantics have different release rhythms.  This catalog gives
every authored glyph an explicit ontological class and an explicit answer to
"which way does its ink face?" so Atlas scenes do not guess from pixels.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("unicode", ROOT / "assets/gray-all/manifest.json"),
    ("alphabet", ROOT / "assets/alpha-ink/manifest.json"),
    ("divination", ROOT / "assets/divination/manifest.json"),
    ("pua", ROOT / "assets/pua/manifest.json"),
)

GROUP_DOMAIN = {
    "Animals & Nature": "nature", "People & Objects": "human-world",
    "Travel & Places": "places-and-transport", "Food & Drink": "food",
    "Activities": "activities", "Smileys & Emotion": "expression",
    "Symbols": "symbols", "Flags": "flags", "Keycaps & Digits": "writing",
    "Other": "symbols",
}

ANIMAL_WORDS = {
    "animal", "ant", "badger", "bat", "bear", "bee", "beetle", "bird", "bison", "boar", "bug",
    "butterfly", "camel", "cat", "chick", "chicken", "cow", "crab", "crocodile", "deer", "dinosaur",
    "dog", "dolphin", "dove", "dragon", "duck", "eagle", "elephant", "ewe", "fish", "flamingo",
    "fly", "fox", "frog", "giraffe", "goat", "goose", "gorilla", "hamster", "hedgehog", "hippopotamus",
    "horse", "insect", "jellyfish", "kangaroo", "koala", "leopard", "lion", "lizard", "llama", "lobster",
    "mammoth", "monkey", "mosquito", "mouse", "octopus", "orangutan", "otter", "owl", "ox", "oyster",
    "panda", "parrot", "peacock", "penguin", "pig", "poodle", "rabbit", "raccoon", "ram", "rat",
    "rhinoceros", "rooster", "scorpion", "seal", "shark", "sheep", "shrimp", "skunk", "sloth", "snail",
    "snake", "spider", "squid", "swan", "tiger", "turtle", "unicorn", "whale", "wolf", "worm", "zebra",
}
FLYING_WORDS = {"bee", "bird", "butterfly", "dragonfly", "duck", "eagle", "fly", "goose", "moth", "mosquito", "owl", "parrot", "pteranodon", "swan"}
WATERFOWL_WORDS = {"duck", "goose", "swan"}
AQUATIC_WORDS = {"crab", "dolphin", "fish", "jellyfish", "lobster", "manta", "nautilus", "octopus", "shark", "shrimp", "squid", "whale"}
VEHICLE_WORDS = {"airplane", "automobile", "bicycle", "boat", "bus", "car", "locomotive", "motorcycle", "rocket", "ship", "submarine", "taxi", "tractor", "train", "truck"}
PLANT_WORDS = {"blossom", "cactus", "flower", "herb", "leaf", "plant", "seedling", "sprout", "tree"}
PERSON_WORDS = {"adult", "baby", "boy", "child", "farmer", "girl", "man", "person", "teacher", "woman", "worker"}


def words(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def classify(namespace: str, item: dict) -> dict:
    source = str(item.get("source", ""))
    label = str(item.get("label") or item.get("name") or "")
    group = str(item.get("group", ""))
    domain = source.split("/", 1)[0] if namespace == "pua" and "/" in source else GROUP_DOMAIN.get(group, namespace)
    tokens = words(label + "-" + source)
    is_animal = domain in {"animals", "dinosaurs", "sea_creatures"} or bool(tokens & ANIMAL_WORDS)
    is_plant = domain in {"plants", "flora", "herbs"} or bool(tokens & PLANT_WORDS)
    is_person = domain in {"people", "body", "faerie"} or bool(tokens & PERSON_WORDS)
    is_vehicle = domain in {"rockets", "vehicles"} or bool(tokens & VEHICLE_WORDS)
    if is_animal: kind, kingdom = "organism", "animalia"
    elif is_plant: kind, kingdom = "organism", "plantae"
    elif is_person: kind, kingdom = "agent", "animalia"
    elif is_vehicle: kind, kingdom = "artifact", None
    elif domain in {"locations", "cave_locations"}: kind, kingdom = "place", None
    elif domain in {"materials"}: kind, kingdom = "substance", None
    elif domain in {"weather_sky"}: kind, kingdom = "phenomenon", None
    elif domain in {"patterns", "symbols", "writing", "divination", "flags"}: kind, kingdom = "symbol", None
    elif domain == "human-world": kind, kingdom = "artifact", None
    elif domain == "places-and-transport": kind, kingdom = "place", None
    elif domain == "food": kind, kingdom = "substance", None
    elif domain == "activities": kind, kingdom = "activity", None
    elif domain in {"nature", "expression"}: kind, kingdom = "phenomenon", None
    else: kind, kingdom = "concept", None

    is_space = domain in {"rockets", "cosmos"} or bool(tokens & {"astronaut", "capsule", "lunar", "orbital", "satellite", "space"})
    is_submarine = "submarine" in tokens
    is_watercraft = bool(tokens & {"boat", "ship"}) and not is_space
    is_cave = domain == "cave_locations" or bool(tokens & {"cave", "cavern", "mine", "underground"})
    stationary = bool(tokens & {"mission", "control"}) or ("station" in tokens and not is_space)
    orbital_fixture = is_space and bool(tokens & {"satellite", "station"})
    if is_plant: mobility, environments, modes = "fixed", ["land"], []
    elif stationary: mobility, environments, modes = "fixed", ["land"], []
    elif orbital_fixture: mobility, environments, modes = "passive", ["space"], ["orbit"]
    elif is_submarine: mobility, environments, modes = "powered", ["underwater", "water-surface"], ["cruise", "dive", "surface"]
    elif is_space and is_vehicle: mobility, environments, modes = "powered", ["space", "air"], ["launch", "coast", "orbit"]
    elif is_person and "astronaut" in tokens: mobility, environments, modes = "self-propelled", ["space", "land"], ["float", "walk"]
    elif is_animal and (domain == "sea_creatures" or tokens & AQUATIC_WORDS): mobility, environments, modes = "self-propelled", ["underwater"], ["swim", "dive", "surface"]
    elif is_animal and tokens & WATERFOWL_WORDS: mobility, environments, modes = "self-propelled", ["water-surface", "air", "land"], ["swim", "fly", "walk"]
    elif is_animal and tokens & FLYING_WORDS: mobility, environments, modes = "self-propelled", ["air", "land"], ["fly", "land"]
    elif is_watercraft: mobility, environments, modes = "powered", ["water-surface"], ["sail"]
    elif is_animal or is_person: mobility, environments, modes = "self-propelled", ["land"], ["walk"]
    elif is_vehicle: mobility, environments, modes = "powered", ["land"], ["drive"]
    elif is_cave: mobility, environments, modes = "fixed", ["subterranean"], []
    else: mobility, environments, modes = "fixed", ["none"], []
    medium = environments[0]
    volume_environment = medium in {"air", "underwater", "space"}
    gravity_response = "microgravity" if medium == "space" else "buoyant" if medium == "underwater" else "lift" if medium == "air" else "supported"
    elevation_range = [-.34, -.03] if medium == "underwater" else [.05, .38] if medium == "air" else [-.42, .42] if medium == "space" else [0, 0]

    # Authored naturalist profiles conventionally look left. Standard emoji
    # people and ambiguous artifacts are treated as frontal/fixed until a
    # reviewed per-glyph override says otherwise.
    frontal = bool(tokens & {"face", "head", "oncoming", "bust", "portrait"})
    profile = (is_animal or is_vehicle or domain in {"dinosaurs", "sea_creatures"}) and not frontal
    intrinsic = "left" if profile else "front" if is_person else "none"
    if mobility == "fixed" or not profile: policy, max_tilt = "fixed", 0
    elif volume_environment: policy, max_tilt = "full-heading", 180
    else: policy, max_tilt = "profile-upright", 32
    return {
        "domain": domain,
        "kind": kind,
        "kingdom": kingdom,
        "typePath": [value for value in ("glyph", kind, kingdom) if value],
        "embodiment": {
            "mobility": mobility,
            "medium": medium,
            "environments": environments,
            "locomotionModes": modes,
            "degreesOfFreedom": 3 if volume_environment else 2 if mobility != "fixed" else 0,
            "gravityResponse": gravity_response,
            "elevationRange": elevation_range,
        },
        "relations": {
            "isA": [value for value in (kind, kingdom) if value],
            "movesThrough": environments if mobility != "fixed" and medium != "none" else [],
            "capableOf": (["self-movement", "sense", "interact"] if mobility == "self-propelled"
                           else ["powered-movement"] if mobility == "powered"
                           else ["environment-driven-movement"] if mobility == "passive" else []),
        },
        "orientation": {
            "intrinsicFacing": intrinsic,
            "vector": [-1, 0] if intrinsic == "left" else [1, 0] if intrinsic == "right" else [0, 0],
            "travelAlignment": policy,
            "mirrorAllowed": profile,
            "maxTiltDegrees": max_tilt,
        },
        "provenance": {"method": "domain-and-label-rules-v1", "reviewed": False},
    }


def main() -> None:
    entries = {}
    for namespace, manifest_path in SOURCES:
        for item in json.loads(manifest_path.read_text()):
            codepoints = item.get("codepoints") or []
            key = "-".join(f"{int(cp):X}" for cp in codepoints) or f"{namespace}:{item.get('name')}"
            entries[key] = {
                "codepoints": codepoints,
                "label": item.get("label") or item.get("name"),
                "namespace": namespace,
                "source": item.get("source"),
                **classify(namespace, item),
            }
    output = {
        "schemaVersion": 1,
        "coordinateSystem": "screen: +x right, +y down; heading 0° right, 90° down",
        "vocabulary": {
            "kind": ["organism", "agent", "artifact", "place", "substance", "phenomenon", "activity", "symbol", "concept"],
            "mobility": ["fixed", "self-propelled", "powered", "passive"],
            "environment": ["land", "air", "water-surface", "underwater", "subterranean", "space", "none"],
            "travelAlignment": ["fixed", "profile-upright", "full-heading"],
        },
        "entries": entries,
    }
    target = ROOT / "assets/ontology.json"
    target.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(entries)} Emojinq ontology entries to {target}")


if __name__ == "__main__":
    main()
