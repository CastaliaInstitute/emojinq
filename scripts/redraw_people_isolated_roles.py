#!/usr/bin/env python3
"""Generate isolated full-bodied role and interaction figures in sumi-e SVG."""

from __future__ import annotations

import re
import json
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/pua/people"
MANIFEST = json.loads((ROOT / "assets/pua/manifest.json").read_text(encoding="utf-8"))
PUA_BY_LABEL = {item["label"]: item["codepoints"][0] for item in MANIFEST}


def codepoint_attr(name: str) -> str:
    value = PUA_BY_LABEL.get(f"people/{name}")
    if value is None:
        original = (OUT / f"{name}.svg").read_text(encoding="utf-8")
        match = re.search(r'data-pua="([^"]+)"', original)
        if match:
            return match.group(0)
        raise SystemExit(f"missing PUA code point: {name}")
    return f'data-pua="U+{value:X}"'


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def wash(points, width, seed, color="#262522"):
    return svg_path(
        stroke_path(p(*points), width=width, seed=seed, wobble=.16),
        fill=color,
    ).replace('<path ', '<path data-ink-brush-pass="loaded-ribbon-v2" ')


def dry(points, width, seed):
    return "\n".join(
        svg_path(d, fill="#77746a", class_name="ink-dry").replace(
            '<path ', '<path data-ink-brush-pass="dry-edge-v2" '
        )
        for d in dry_brush_paths(p(*points), width=width, seed=seed, breaks=1)
    )


def stand_base() -> str:
    """Return the approved neutral stand figure as the shared body template.

    Occupation cards must inherit one coherent body/proportion system. Role
    identity is added at the edge as a tool, garment, or gesture cue; it is not
    expressed by regenerating a new torso for every occupation.
    """
    source = (ROOT / "assets/pua/science/body.svg").read_text(encoding="utf-8")
    match = re.search(r'<ns0:g id="line">(.*?)</ns0:g>\s*</ns0:svg>', source, re.S)
    if not match:
        raise SystemExit("neutral stand template is missing its line group")
    return match.group(1).replace("ns0:", "")


TORSO_VARIANTS = {
    "apron": {"names": {"baker", "cook", "cleaner", "chef", "service"}, "path": '<path d="M29 29q7 3 14 0l2 15q-8 4-18 0z" fill="none" stroke="#4a4943" stroke-width="1.35" data-ink-role="torso-variant-apron"/><path d="M31 32q5 2 10 0M32 39h8" fill="none" stroke="#817b70" stroke-width=".8" data-ink-role="torso-detail"/>'},
    "coat": {"names": {"doctor", "nurse", "police", "firefighter", "astronaut", "mechanic"}, "path": '<path d="M29 25l7 7 7-7M36 32v14M31 35l5 3 5-3" fill="none" stroke="#4a4943" stroke-width="1.25" data-ink-role="torso-variant-coat"/>'},
    "vest": {"names": {"builder", "farmer", "fisher", "hunter", "scout", "stewardship", "work", "repair"}, "path": '<path d="M30 25l6 8 6-8M31 31l-2 14M41 31l2 14M33 38h6" fill="none" stroke="#4a4943" stroke-width="1.25" data-ink-role="torso-variant-vest"/>'},
    "robe": {"names": {"ancestor", "sage", "rumi", "laozi", "aristotle", "buddha", "confucius", "socrates", "maimonides", "ibnsina", "hildegard", "prayer", "faith", "pilgrimage", "legacy"}, "path": '<path d="M30 25q6 5 12 0M31 30q5 2 10 0M31 44q5 2 10 0M36 31v15" fill="none" stroke="#4a4943" stroke-width="1.15" data-ink-role="torso-variant-robe"/>'},
    "sash": {"names": {"artist", "art", "creator", "dancer", "trickster", "fool", "hero", "courage", "leadership", "mentor", "seeker", "purpose", "progress"}, "path": '<path d="M30 27q6 3 12 0M30 34q6 3 12 0M31 42q5 2 10 0" fill="none" stroke="#4a4943" stroke-width="1.3" data-ink-role="torso-variant-sash"/>'},
    "uniform": {"names": {"duty", "justice", "law", "rights", "vote", "safety", "protection", "police"}, "path": '<path d="M30 27h12M31 33h10M31 40h10M36 27v17" fill="none" stroke="#4a4943" stroke-width="1.15" data-ink-role="torso-variant-uniform"/>'},
    "tunic": {"names": {"child", "baby", "orphan", "father", "grandparent", "cousin", "neighbor", "humility", "kindness", "compassion", "empathy", "rest"}, "path": '<path d="M30 28q6 3 12 0M31 35q5 2 10 0M32 43q4 1 8 0" fill="none" stroke="#4a4943" stroke-width="1.0" data-ink-role="torso-variant-tunic"/>'},
}


def torso_variant(name: str) -> str:
    for variant, spec in TORSO_VARIANTS.items():
        if name in spec["names"]:
            return spec["path"].replace("torso-variant-", f"torso-variant-{variant}-")
    return '<path d="M30 28q6 3 12 0M31 36q5 2 10 0M32 43q4 1 8 0" fill="none" stroke="#4a4943" stroke-width="1.05" data-ink-role="torso-variant-neutral"/>'


def common_from_stand(name: str, role: str, reference: str, prop: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint_attr(name)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-figure-composition="isolated-full-bodied-v1" data-naturalist-construction="shared-neutral-stand-template-v1" data-figure-interaction="movable-agent-v1" data-agent-capabilities="walk;face-user;gesture;talk" data-intentional-components="figure-and-prop-v1" data-component-review="severity-contact-sheet-2026-08-v1" data-reference-source="{reference}" data-reference-role="Noun Project line silhouette used for proportion and role-cue orientation only" data-reference-record="docs/references/noun-project-people-line.md" data-license-status="reference-only; exact production license not asserted">
  <title>people / {name} — isolated full-bodied {role}, shared neutral stand sumi-e study</title>
  <g id="shared-neutral-stand">{stand_base()}</g>
  <g id="occupation-torso-variant" data-torso-variant="{next((v for v, s in TORSO_VARIANTS.items() if name in s["names"]), "neutral")}">{torso_variant(name)}</g>
  {prop}
  <path class="ink-dry" d="M17 65c12-1 27-1 39 0" fill="none" stroke="#bcb9af" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>
</svg>
'''


def common(name: str, role: str, reference: str, prop: str, pose: str) -> str:
    return common_from_stand(name, role, reference, prop)

    # One continuous loaded brush gesture for each body region keeps the
    # figure substantial without turning it into a closed pictogram silhouette.
    if name in {"baby", "child", "orphan"}:
        archetype = "compact"
    elif name in {"ancestor", "grandparent", "sage", "rumi", "laozi", "aristotle", "buddha", "confucius", "socrates", "maimonides", "ibnsina", "hildegard"}:
        archetype = "elder"
    elif name in {"builder", "farmer", "firefighter", "mechanic", "police", "hero", "destroyer"}:
        archetype = "broad"
    elif name in {"artist", "astronaut", "seeker", "dancer", "creator", "trickster", "fool"}:
        archetype = "active"
    else:
        archetype = "standard"
    pose = {
        "nurse": "reach",
        "cleaner": "sweep",
        "farmer": "carry",
        "builder": "hammer",
        "artist": "reach",
        "cook": "carry",
    }.get(name, pose)
    if pose == "left":
        arm_l = [(31, 31, .2), (26, 37, .82), (22, 45, .72), (18, 50, .18)]
        arm_r = [(41, 31, .2), (47, 37, .8), (51, 43, .7), (55, 46, .18)]
        leg_l = [(33, 47, .2), (31, 54, .9), (28, 61, .2)]
        leg_r = [(39, 47, .2), (42, 54, .9), (46, 61, .2)]
    elif pose == "stride":
        arm_l = [(31, 31, .2), (25, 35, .82), (20, 41, .72), (16, 45, .18)]
        arm_r = [(41, 31, .2), (48, 35, .8), (54, 40, .7), (59, 43, .18)]
        leg_l = [(33, 47, .2), (28, 53, .9), (22, 59, .2)]
        leg_r = [(39, 47, .2), (44, 53, .9), (51, 58, .2)]
    elif pose == "wide":
        arm_l = [(31, 31, .2), (25, 38, .82), (20, 47, .72), (15, 52, .18)]
        arm_r = [(41, 31, .2), (48, 38, .8), (54, 47, .7), (59, 52, .18)]
        leg_l = [(33, 47, .2), (29, 55, .9), (23, 62, .2)]
        leg_r = [(39, 47, .2), (43, 55, .9), (49, 62, .2)]
    elif pose == "work":
        arm_l = [(31, 31, .2), (27, 37, .82), (24, 45, .72), (24, 52, .18)]
        arm_r = [(41, 31, .2), (46, 36, .8), (50, 43, .7), (55, 47, .18)]
        leg_l = [(33, 47, .2), (30, 54, .9), (25, 61, .2)]
        leg_r = [(39, 47, .2), (43, 53, .9), (48, 60, .2)]
    elif pose == "reach":
        arm_l = [(31, 31, .2), (26, 36, .82), (22, 43, .72), (19, 48, .18)]
        arm_r = [(41, 31, .2), (47, 29, .8), (54, 32, .7), (60, 29, .18)]
        leg_l = [(33, 47, .2), (31, 54, .9), (27, 61, .2)]
        leg_r = [(39, 47, .2), (43, 54, .9), (47, 61, .2)]
    elif pose == "sweep":
        arm_l = [(31, 31, .2), (26, 37, .82), (22, 44, .72), (20, 50, .18)]
        arm_r = [(41, 31, .2), (47, 36, .8), (53, 43, .7), (58, 50, .18)]
        leg_l = [(33, 47, .2), (29, 53, .9), (22, 58, .2)]
        leg_r = [(39, 47, .2), (44, 53, .9), (51, 58, .2)]
    elif pose == "carry":
        arm_l = [(31, 31, .2), (26, 37, .82), (23, 44, .72), (22, 49, .18)]
        arm_r = [(41, 31, .2), (46, 37, .8), (48, 43, .7), (48, 49, .18)]
        leg_l = [(33, 47, .2), (30, 54, .9), (26, 61, .2)]
        leg_r = [(39, 47, .2), (43, 54, .9), (49, 61, .2)]
    elif pose == "hammer":
        arm_l = [(31, 31, .2), (26, 37, .82), (24, 44, .72), (22, 49, .18)]
        arm_r = [(41, 31, .2), (46, 25, .8), (52, 20, .7), (57, 17, .18)]
        leg_l = [(33, 47, .2), (30, 54, .9), (25, 61, .2)]
        leg_r = [(39, 47, .2), (43, 54, .9), (48, 61, .2)]
    else:
        arm_l = [(31, 31, .2), (26, 37, .82), (22, 43, .72), (18, 46, .18)]
        arm_r = [(41, 31, .2), (47, 37, .8), (51, 45, .7), (55, 51, .18)]
        leg_l = [(33, 47, .2), (31, 54, .9), (28, 61, .2)]
        leg_r = [(39, 47, .2), (42, 54, .9), (46, 61, .2)]
    head = {
        "compact": '<ellipse class="ink-wash" cx="36" cy="18" rx="5.7" ry="5.4" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        "elder": '<ellipse class="ink-wash" cx="36" cy="17" rx="5.4" ry="5.6" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        "active": '<ellipse class="ink-wash" cx="36" cy="16.5" rx="5.0" ry="5.2" transform="rotate(-7 36 16.5)" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        "standard": '<ellipse class="ink-wash" cx="36" cy="17" rx="5.2" ry="5.4" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        "broad": '<ellipse class="ink-wash" cx="36" cy="17" rx="5.5" ry="5.3" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
    }[archetype]
    torso = {
        "compact": ([(31, 24, .2), (27, 30, .8), (28, 39, 1.0), (32, 47, .2)], 9.0, [(41, 24, .2), (45, 30, .8), (44, 39, 1.0), (40, 47, .2)], 8.5),
        "elder": ([(29, 23, .2), (24, 30, .8), (25, 41, 1.0), (31, 48, .2)], 10.5, [(43, 23, .2), (48, 30, .8), (47, 41, 1.0), (41, 48, .2)], 10.0),
        "active": ([(30, 23, .2), (24, 29, .8), (27, 39, 1.0), (33, 47, .2)], 10.0, [(42, 22, .2), (48, 28, .8), (45, 39, 1.0), (40, 47, .2)], 9.5),
        "standard": ([(30, 23, .2), (25, 29, .8), (26, 39, 1.0), (31, 47, .2)], 11.0, [(42, 23, .2), (47, 29, .8), (46, 39, 1.0), (41, 47, .2)], 10.0),
        "broad": ([(29, 23, .2), (23, 29, .8), (24, 39, 1.0), (31, 47, .2)], 12.0, [(43, 23, .2), (49, 29, .8), (48, 39, 1.0), (41, 47, .2)], 11.0),
    }[archetype]
    headwear = {
        "compact": '<path class="ink-wash" d="M32 15q4-5 8-1l2 3H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/>',
        "elder": '<path class="ink-wash" d="M30 14q2-5 6-4 7-2 9 4l-2 3H31z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-dry" d="M30 18q-2 4-1 7M42 18q2 4 1 7" fill="none" stroke="#77746a" stroke-width=".8" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>',
        "active": '<path class="ink-wash" d="M31 14q3-5 8-4 5 1 6 5l-2 2H31z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M31 15q-4 0-5 4" fill="none" stroke="#4a4943" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        "broad": '<path class="ink-wash" d="M29 14q3-4 7-4 6 0 8 4l-1 3H29z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/>',
        "standard": '<path class="ink-wash" d="M31 14c2-4 9-5 12 0l-1 3H31z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/>',
    }[archetype]
    face = {
        "compact": '<path class="ink-stroke" d="M33 19q1 1 2 0M37 19q1 1 2 0M34 22q2 1 4 0" fill="none" stroke="#262522" stroke-width=".75" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        "elder": '<path class="ink-stroke" d="M33 18q1 1 2 0M37 18q1 1 2 0M34 22q2 1 4 0M32 20h2M38 20h2" fill="none" stroke="#262522" stroke-width=".7" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        "active": '<path class="ink-stroke" d="M33 18q1 1 2 0M37 18q1 1 2 0M34 21q2 2 4 0" fill="none" stroke="#262522" stroke-width=".75" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        "broad": '<path class="ink-stroke" d="M33 18q1 1 2 0M37 18q1 1 2 0M34 21q2 1 4 0" fill="none" stroke="#262522" stroke-width=".75" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        "standard": '<path class="ink-stroke" d="M34 18c1 1 3 1 5 0M35 21c1 1 2 1 3 0" fill="none" stroke="#262522" stroke-width=".75" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
    }[archetype]
    parts = [
        head,
        headwear,
        face,
        wash(torso[0], torso[1], f"{name}-torso-left", "#4a4943"),
        wash(torso[2], torso[3], f"{name}-torso-right", "#262522"),
        wash(arm_l, 3.5, f"{name}-left-arm"),
        wash(arm_r, 3.4, f"{name}-right-arm", "#4a4943"),
        wash(leg_l, 3.7, f"{name}-left-leg"),
        wash(leg_r, 3.8, f"{name}-right-leg", "#4a4943"),
        '<path class="ink-stroke" d="M25 63c3-2 6-2 9 0M43 63c3-2 6-2 9 0" fill="none" stroke="#262522" stroke-width="1.35" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        '<path class="ink-stroke" d="M33 28c2 1 5 1 7 0M33 34c2 1 5 1 7 0M34 40c2 1 4 1 6 0" fill="none" stroke="#77746a" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>',
    ]
    garment = {
        "nurse": '<path class="ink-stroke" d="M29 25l5 4 2-2 2 2 5-4M31 29v15M41 29v15" fill="none" stroke="#77746a" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v2"/>',
        "baker": '<path class="ink-wash" d="M29 29q7 3 14 0l2 15q-8 4-18 0z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M31 32q5 2 10 0M32 38h8" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="material-cue-v1"/>',
        "cook": '<path class="ink-wash" d="M29 29q7 3 14 0l2 15q-8 4-18 0z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M31 32q5 2 10 0M32 38h8" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="material-cue-v1"/>',
        "farmer": '<path class="ink-stroke" d="M31 25l2 20M41 25l-2 20M33 35h6" fill="none" stroke="#77746a" stroke-width="1.1" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v2"/>',
        "artist": '<path class="ink-wash" d="M31 25q5 3 10 0l3 19q-8 3-16 0z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M34 30l4 0M33 35l5 0M32 40l6 0" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="material-cue-v1"/>',
        "astronaut": '<ellipse class="ink-stroke" cx="36" cy="17" rx="7.2" ry="7.5" fill="none" stroke="#77746a" stroke-width="1.1" data-ink-brush-pass="recognition-cue-v2"/><path class="ink-stroke" d="M30 28q6 3 12 0M31 33h10M32 39h8" fill="none" stroke="#77746a" stroke-width=".9" data-ink-brush-pass="material-cue-v1"/>',
        "mechanic": '<path class="ink-wash" d="M29 29q7 3 14 0l2 15q-8 4-18 0z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M32 32l3 3 3-3M32 40h8" fill="none" stroke="#77746a" stroke-width=".9" data-ink-brush-pass="material-cue-v1"/>',
    }.get(name, "")
    if garment:
        parts.append(garment)
    parts.append(prop)
    parts.append('<path class="ink-dry" d="M17 65c12-1 27-1 39 0" fill="none" stroke="#bcb9af" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>')
    original = (OUT / f"{name}.svg").read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA code point: {name}")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-figure-composition="isolated-full-bodied-v1" data-naturalist-construction="isolated-figure-role-v1" data-intentional-components="figure-and-prop-v1" data-component-review="severity-contact-sheet-2026-08-v1" data-reference-source="{reference}" data-reference-role="Noun Project line silhouette used for anatomy and prop orientation only" data-reference-record="docs/references/noun-project-people-line.md" data-license-status="reference-only; exact production license not asserted">

  <title>people / {name} — isolated full-bodied {role} sumi-e study</title>
  {''.join(parts)}
</svg>
'''


def healer_svg() -> str:
    name = "healer"
    original = (OUT / f"{name}.svg").read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit("missing PUA code point: healer")
    marks = [
        '<ellipse class="ink-wash" cx="22" cy="18" rx="4.3" ry="4.7" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        '<path class="ink-wash" d="M18 15c2-4 8-5 11-1l-1 3H18z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/>',
        '<path class="ink-stroke" d="M20 18q2 1 4 0M21 21q2 1 3 0" fill="none" stroke="#262522" stroke-width=".7" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        wash([(19, 23, .2), (16, 29, .8), (17, 39, 1.0), (21, 47, .2)], 9.0, "healer-torso", "#4a4943"),
        wash([(19, 30, .2), (27, 34, .75), (33, 39, .2)], 3.0, "healer-reaching-arm"),
        wash([(21, 47, .2), (19, 54, .9), (16, 61, .2)], 3.5, "healer-left-leg"),
        wash([(25, 47, .2), (28, 54, .9), (31, 61, .2)], 3.5, "healer-right-leg", "#4a4943"),
        '<path class="ink-stroke" d="M13 63c3-2 6-2 9 0M28 63c3-2 6-2 9 0" fill="none" stroke="#262522" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        '<ellipse class="ink-wash" cx="50" cy="34" rx="4.0" ry="4.3" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        '<path class="ink-stroke" d="M48 34q2 1 4 0M49 37q2 1 3 0" fill="none" stroke="#262522" stroke-width=".7" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        wash([(47, 39, .2), (43, 44, .8), (45, 51, 1.0), (51, 54, .2)], 8.0, "patient-torso", "#4a4943"),
        wash([(47, 42, .2), (40, 45, .8), (35, 46, .2)], 3.1, "patient-resting-arm", "#77746a"),
        wash([(49, 53, .2), (55, 56, .8), (59, 59, .2)], 3.4, "patient-leg", "#262522"),
        '<path class="ink-stroke" d="M56 61c3-2 6-2 9 0" fill="none" stroke="#262522" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        '<path class="ink-stroke" d="M32 39c3-2 5-2 7 0M38 39c1 2 1 3 0 4" fill="none" stroke="#262522" stroke-width="1.15" stroke-linecap="round" data-ink-brush-pass="healing-action-v1"/>',
        '<path class="ink-wash" d="M30 51c4-2 8-2 12 0l-1 4H31z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/>',
        '<path class="ink-stroke" d="M33 52c2 1 5 1 7 0M35 50v4" fill="none" stroke="#262522" stroke-width=".85" data-ink-brush-pass="recognition-cue-v1"/>',
        '<path class="ink-dry" d="M10 65c17-1 37-1 54 0" fill="none" stroke="#bcb9af" stroke-width="1" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>',
    ]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / healer" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-figure-composition="interaction-healer-patient-v1" data-naturalist-construction="interaction-healer-patient-v1" data-intentional-components="figure-and-prop-v1" data-component-review="severity-contact-sheet-2026-08-v1" data-reference-source="https://thenounproject.com/browse/icons/term/healer/" data-reference-role="Noun Project line silhouette used for interaction anatomy and prop orientation only" data-reference-record="docs/references/noun-project-people-line.md" data-license-status="reference-only; exact production license not asserted">
  <title>people / healer — healer and patient interaction sumi-e study</title>
  {''.join(marks)}
</svg>
'''


def relationship_svg(name: str, title: str, reference: str, action: str) -> str:
    original = (OUT / f"{name}.svg").read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA code point: {name}")
    marks = [
        '<ellipse class="ink-wash" cx="21" cy="18" rx="4.3" ry="4.7" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        '<path class="ink-wash" d="M17 15c2-4 8-5 11-1l-1 3H17z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/>',
        '<path class="ink-stroke" d="M19 18q2 1 4 0M20 21q2 1 3 0" fill="none" stroke="#262522" stroke-width=".7" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        wash([(18, 23, .2), (15, 30, .8), (17, 40, 1.0), (21, 48, .2)], 9.0, f"{name}-left-torso", "#4a4943"),
        wash([(20, 48, .2), (18, 55, .9), (15, 62, .2)], 3.5, f"{name}-left-leg"),
        wash([(24, 48, .2), (27, 55, .9), (30, 62, .2)], 3.5, f"{name}-left-leg-right", "#4a4943"),
        '<path class="ink-stroke" d="M12 64c3-2 6-2 9 0M27 64c3-2 6-2 9 0" fill="none" stroke="#262522" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        '<ellipse class="ink-wash" cx="50" cy="20" rx="4.3" ry="4.7" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
        '<path class="ink-wash" d="M46 17c2-4 8-5 11-1l-1 3H46z" fill="#262522" data-ink-brush-pass="loaded-mass-v2"/>',
        '<path class="ink-stroke" d="M48 20q2 1 4 0M49 23q2 1 3 0" fill="none" stroke="#262522" stroke-width=".7" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
        wash([(47, 25, .2), (44, 32, .8), (46, 42, 1.0), (50, 49, .2)], 9.0, f"{name}-right-torso", "#4a4943"),
        wash([(49, 49, .2), (47, 56, .9), (44, 62, .2)], 3.5, f"{name}-right-leg"),
        wash([(53, 49, .2), (56, 56, .9), (59, 62, .2)], 3.5, f"{name}-right-leg-right", "#4a4943"),
        '<path class="ink-stroke" d="M41 64c3-2 6-2 9 0M56 64c3-2 6-2 9 0" fill="none" stroke="#262522" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
    ]
    if action == "help":
        marks += [
            wash([(19, 31, .2), (27, 35, .8), (35, 40, .2)], 3.0, "help-supporting-arm"),
            wash([(46, 33, .2), (40, 37, .8), (35, 40, .2)], 3.0, "help-reaching-arm", "#262522"),
            '<path class="ink-stroke" d="M33 40q3 3 6 0M34 38q2-3 4 0" fill="none" stroke="#262522" stroke-width="1.05" stroke-linecap="round" data-ink-brush-pass="help-contact-v1"/>',
        ]
    elif action == "cooperation":
        marks += [
            wash([(19, 32, .2), (27, 37, .8), (34, 42, .2)], 3.0, "cooperation-left-grip"),
            wash([(49, 32, .2), (42, 37, .8), (34, 42, .2)], 3.0, "cooperation-right-grip", "#262522"),
            '<path class="ink-wash" d="M27 39q7-3 14 0l1 8q-8 3-16 0z" fill="#77746a" data-ink-brush-pass="shared-load-v1"/>',
            '<path class="ink-stroke" d="M30 42h10M30 45h10" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="shared-load-detail-v1"/>',
        ]
    elif action == "welcome":
        marks += [
            wash([(18, 32, .2), (12, 28, .8), (8, 29, .2)], 3.0, "welcome-left-open-arm", "#4a4943"),
            wash([(49, 32, .2), (56, 28, .8), (63, 29, .2)], 3.0, "welcome-right-open-arm", "#262522"),
            '<path class="ink-stroke" d="M9 29q3-3 6 0M57 29q3-3 6 0" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="welcome-gesture-v1"/>',
        ]
    elif action == "guardian":
        marks += [
            wash([(19, 31, .2), (27, 35, .8), (37, 43, .2)], 3.1, "guardian-protective-arm", "#262522"),
            '<path class="ink-wash" d="M26 36q9-7 18 0l-1 16q-8 4-16 0z" fill="#77746a" data-ink-brush-pass="protective-shield-v1"/>',
            '<path class="ink-stroke" d="M30 40q5-3 10 0M30 44q5-3 10 0" fill="none" stroke="#262522" stroke-width=".85" data-ink-brush-pass="guardian-cue-v1"/>',
        ]
    else:
        marks += [
            wash([(19, 32, .2), (27, 37, .8), (34, 42, .2)], 3.0, "conflict-left-gesture", "#262522"),
            wash([(49, 32, .2), (42, 37, .8), (35, 42, .2)], 3.0, "conflict-right-gesture", "#4a4943"),
            '<path class="ink-stroke" d="M33 40l3 3 3-3M34 45l2-2 2 2" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="conflict-tension-v1"/>',
        ]
    marks.append('<path class="ink-dry" d="M9 66c17-1 37-1 54 0" fill="none" stroke="#bcb9af" stroke-width="1" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-figure-composition="interaction-{action}-v1" data-naturalist-construction="interaction-{action}-v1" data-intentional-components="figure-and-prop-v1" data-component-review="severity-contact-sheet-2026-08-v1" data-reference-source="{reference}" data-reference-role="Noun Project line silhouettes used for interaction anatomy and gesture only" data-reference-record="docs/references/noun-project-people-line.md" data-license-status="reference-only; exact production license not asserted">
  <title>people / {name} — {title} interaction sumi-e study</title>
  {''.join(marks)}
</svg>
'''


def group_svg(name: str, title: str, reference: str) -> str:
    original = (OUT / f"{name}.svg").read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA code point: {name}")
    marks = []
    for index, x in enumerate((18, 36, 54)):
        tone = "#262522" if index == 1 else "#4a4943"
        marks.extend([
        f'<ellipse class="ink-wash" cx="{x}" cy="18" rx="4.0" ry="4.4" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>',
            f'<path class="ink-stroke" d="M{x-2} 18q2 1 4 0M{x-1} 21q2 1 3 0" fill="none" stroke="#262522" stroke-width=".65" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>',
            wash([(x - 3, 23, .2), (x - 5, 30, .8), (x - 3, 40, 1.0), (x, 48, .2)], 7.8, f"{name}-{index}-torso", tone),
            wash([(x - 1, 48, .2), (x - 3, 56, .9), (x - 5, 62, .2)], 3.1, f"{name}-{index}-leg-a"),
            wash([(x + 2, 48, .2), (x + 4, 56, .9), (x + 6, 62, .2)], 3.1, f"{name}-{index}-leg-b", tone),
            f'<path class="ink-stroke" d="M{x-8} 64q3-2 6 0M{x+1} 64q3-2 6 0" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="loaded-contour-v2"/>',
        ])
    marks += [
        wash([(18, 33, .2), (26, 36, .8), (34, 40, .2)], 2.5, f"{name}-left-link"),
        wash([(38, 40, .2), (46, 36, .8), (54, 33, .2)], 2.5, f"{name}-right-link", "#262522"),
        '<path class="ink-stroke" d="M27 43q9-5 18 0" fill="none" stroke="#77746a" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="shared-bond-v1"/>',
        '<path class="ink-dry" d="M8 66c18-1 38-1 56 0" fill="none" stroke="#bcb9af" stroke-width="1" stroke-linecap="round" data-ink-brush-pass="dry-edge-v2"/>',
    ]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-figure-composition="interaction-group-v1" data-naturalist-construction="interaction-group-v1" data-intentional-components="figure-and-prop-v1" data-component-review="severity-contact-sheet-2026-08-v1" data-reference-source="{reference}" data-reference-role="Noun Project line silhouettes used for group anatomy and shared gesture only" data-reference-record="docs/references/noun-project-people-line.md" data-license-status="reference-only; exact production license not asserted">
  <title>people / {name} — {title} interaction sumi-e study</title>
  {''.join(marks)}
</svg>
'''


ART = {
    "nurse": (
        "medical worker", "https://thenounproject.com/icon/nurse-1614307/",
        '<path class="ink-stroke" d="M46 38h12v12H46zM52 40v8M48 44h8" fill="none" stroke="#262522" stroke-width="1.15" data-ink-brush-pass="recognition-cue-v1"/>', "work",
    ),
    "baker": (
        "baker", "https://thenounproject.com/browse/collection-icon/cooking-line-274627/",
        '<path class="ink-wash" d="M14 15c1-5 6-7 10-4 3-5 11-4 12 2 4-2 8 1 7 6H14z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M19 52c5-3 10-3 15 0" fill="none" stroke="#262522" stroke-width="1.2" data-ink-brush-pass="recognition-cue-v1"/>', "work",
    ),
    "cook": (
        "cook", "https://thenounproject.com/browse/collection-icon/cooking-line-274627/",
        '<path class="ink-wash" d="M48 43c4-4 12-3 14 2l-2 7H48z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 44c3 2 6 2 9 0" fill="none" stroke="#262522" stroke-width="1.1" data-ink-brush-pass="recognition-cue-v1"/>', "work",
    ),
    "firefighter": (
        "firefighter", "https://thenounproject.com/browse/collection-icon/fire-fighter-line-icons-76347/",
        '<path class="ink-wash" d="M29 14c2-6 12-7 15 0l-2 4H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M33 14h7M36 11v7" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "wide",
    ),
    "babysitter": (
        "babysitter", "https://thenounproject.com/browse/icons/term/babysitter/",
        '<path class="ink-wash" d="M48 47c-1-6 3-10 8-10s8 4 7 10c-2 4-12 4-15 0z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M52 43c2 1 5 1 7 0" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "farmer": (
        "farmer", "https://thenounproject.com/browse/icons/term/farmer/",
        '<path class="ink-wash" d="M27 14c4-4 14-4 18 0l-1 2H27z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M47 41l10 10M55 51l-3 3" fill="none" stroke="#262522" stroke-width="1.15" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "work",
    ),
    "builder": (
        "builder", "https://thenounproject.com/browse/icons/term/builder/",
        '<path class="ink-wash" d="M30 14h12l2 5H28z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 40l7 7M53 36l5 5" fill="none" stroke="#262522" stroke-width="1.2" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "work",
    ),
    "cleaner": (
        "cleaner", "https://thenounproject.com/browse/icons/term/cleaner/",
        '<path class="ink-stroke" d="M49 36l9 18M55 53h7" fill="none" stroke="#262522" stroke-width="1.25" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/><path class="ink-wash" d="M48 53c4-2 10-2 13 0v8H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/>', "work",
    ),
    "mechanic": (
        "mechanic", "https://thenounproject.com/browse/icons/term/mechanic/",
        '<path class="ink-wash" d="M29 14c3-4 11-4 14 0v4H29z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 43c3-3 6-3 9 0l-3 3 3 3c-3 2-6 1-8-1" fill="none" stroke="#262522" stroke-width="1.05" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "police": (
        "police officer", "https://thenounproject.com/browse/icons/term/police/",
        '<path class="ink-wash" d="M29 15c2-5 12-6 15 0l-2 3H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M46 39h8v8h-8zM48 41h4v4h-4z" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "ancestor": (
        "ancestor", "https://thenounproject.com/browse/icons/term/ancestor/",
        '<path class="ink-wash" d="M48 36c4-3 9-2 11 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 38c2 1 4 1 6 0M52 45l5 5" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "artist": (
        "artist", "https://thenounproject.com/browse/icons/term/artist/",
        '<path class="ink-wash" d="M47 40c5-4 11-2 12 3-2 4-8 6-13 4z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 42c3-2 6-2 9 0M54 39l4-4" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "citizen": (
        "citizen", "https://thenounproject.com/browse/icons/term/citizen/",
        '<path class="ink-wash" d="M48 37h12v12H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 40h6M51 44h6" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "creator": (
        "creator", "https://thenounproject.com/browse/icons/term/creator/",
        '<path class="ink-wash" d="M47 47c1-6 5-9 10-8 3 2 3 7 0 10-4 2-8 1-10-2z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 45c2-2 5-2 7 0M47 52l8 3" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "leader": (
        "leader", "https://thenounproject.com/browse/icons/term/leader/",
        '<path class="ink-wash" d="M48 26l2 22h3l2-22z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 27c3-3 6-3 9-1M51 35h5M51 41h5" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "aristotle": (
        "Aristotle", "https://thenounproject.com/browse/icons/term/aristotle/",
        '<path class="ink-wash" d="M48 40c4-4 10-3 12 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42c3-2 6-2 9 0M50 47h8" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "buddha": (
        "Buddha", "https://thenounproject.com/browse/icons/term/buddha/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 43q4-4 8 0M50 47q3 2 6 0" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "confucius": (
        "Confucius", "https://thenounproject.com/browse/icons/term/confucius/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 39h11v10H48zM50 42h7M50 46h6" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "curie": (
        "Marie Curie", "https://thenounproject.com/browse/icons/term/marie-curie/",
        '<path class="ink-wash" d="M29 15c3-4 11-4 14 0l-1 3H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 43c4-3 9-2 11 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 44q3-2 6 0M52 48h5" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "newton": (
        "Isaac Newton", "https://thenounproject.com/browse/icons/term/isaac-newton/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M49 40c4-3 9-2 11 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><circle class="ink-wash" cx="56" cy="52" r="2.2" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/>', "left",
    ),
    "socrates": (
        "Socrates", "https://thenounproject.com/browse/icons/term/socrates/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 41h8M50 45h7" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "hypatia": (
        "Hypatia", "https://thenounproject.com/browse/icons/term/hypatia/",
        '<path class="ink-wash" d="M29 15c3-4 11-4 14 0l-1 3H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><circle class="ink-stroke" cx="56" cy="44" r="4" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "laozi": (
        "Laozi", "https://thenounproject.com/browse/icons/term/laozi/",
        '<path class="ink-wash" d="M28 14c4-5 12-5 15 0l-2 4H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M49 34l3 26h3l-1-26z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 38h6M50 45h5M51 52h5" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "maimonides": (
        "Maimonides", "https://thenounproject.com/browse/icons/term/maimonides/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42h8M50 46h7M52 50h5" fill="none" stroke="#262522" stroke-width=".85" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "ibnsina": (
        "Ibn Sina", "https://thenounproject.com/browse/icons/term/ibn-sina/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42q4-2 8 0M50 46q4-2 8 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "hildegard": (
        "Hildegard", "https://thenounproject.com/browse/icons/term/hildegard/",
        '<path class="ink-wash" d="M29 15c3-4 11-4 14 0l-1 3H30z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42l8-2M50 46l8-2M52 49l5-1" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "astronaut": (
        "astronaut", "https://thenounproject.com/browse/icons/term/astronaut/",
        '<path class="ink-wash" d="M47 38c4-4 10-3 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 40h9M49 44h8" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "seeker": (
        "seeker", "https://thenounproject.com/browse/icons/term/seeker/",
        '<path class="ink-wash" d="M48 37c4-3 9-2 11 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M54 40v10M50 46h8" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "stewardship": (
        "steward", "https://thenounproject.com/browse/icons/term/stewardship/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 45q4-4 8 0M52 42l3-3" fill="none" stroke="#262522" stroke-width=".95" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "service": (
        "service worker", "https://thenounproject.com/browse/icons/term/service/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 43h9M50 47h7" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "trickster": (
        "trickster", "https://thenounproject.com/browse/icons/term/trickster/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 41q4-4 8 0M49 46q4-4 8 0" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "fool": (
        "fool", "https://thenounproject.com/browse/icons/term/fool/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 40q4-3 9 0M48 45q4-3 9 0" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "hero": (
        "hero", "https://thenounproject.com/browse/icons/term/hero/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42l3 3 5-6" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "sage": (
        "sage", "https://thenounproject.com/browse/icons/term/sage/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M50 33l3 28h3l-1-28z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 38h7M50 45h6M51 52h5" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "rumi": (
        "Rumi", "https://thenounproject.com/browse/icons/term/rumi/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42q4-2 8 0M50 46q4-2 8 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "courage": (
        "courage", "https://thenounproject.com/browse/icons/term/courage/",
        '<path class="ink-wash" d="M48 38c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 40l3 3 3-3M54 39v8" fill="none" stroke="#262522" stroke-width=".95" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "mentor": (
        "mentor", "https://thenounproject.com/browse/icons/term/mentor/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42h8M50 46h7" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "grandparent": (
        "grandparent", "https://thenounproject.com/browse/icons/term/grandparent/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M49 33l3 28h3l-1-28z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 39h7M50 46h6M51 53h5" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "cousin": (
        "cousin", "https://thenounproject.com/browse/icons/term/cousin/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42q4-2 8 0M50 46q4-2 8 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "neighbor": (
        "neighbor", "https://thenounproject.com/browse/icons/term/neighbor/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 47c4-3 10-2 12 2l-2 6H48z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 43h8M50 47h7" fill="none" stroke="#262522" stroke-width=".85" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "child": (
        "child", "https://thenounproject.com/browse/icons/term/child/",
        '<path class="ink-wash" d="M48 42c4-3 10-2 12 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 44q4-2 8 0M51 48h6" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "baby": (
        "baby", "https://thenounproject.com/browse/icons/term/baby/",
        '<path class="ink-wash" d="M48 42c4-3 10-2 12 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M49 49c3-2 8-2 11 0l-2 5H49z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/>', "left",
    ),
    "duty": (
        "duty", "https://thenounproject.com/browse/icons/term/duty/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 41h8v8h-8zM52 43h4M52 46h4" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "work": (
        "work", "https://thenounproject.com/browse/icons/term/work/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 43l8 5M57 43l-8 5" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "repair": (
        "repair", "https://thenounproject.com/browse/icons/term/repair/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 41l8 8M58 41l-8 8M52 40l4 4" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "vote": (
        "vote", "https://thenounproject.com/browse/icons/term/vote/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 40h9v11h-9zM52 43l2 2 3-4" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "promise": (
        "promise", "https://thenounproject.com/browse/icons/term/promise/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 44q4-4 8 0M50 48q4-4 8 0" fill="none" stroke="#262522" stroke-width="1.0" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "treaty": (
        "treaty", "https://thenounproject.com/browse/icons/term/treaty/",
        '<path class="ink-wash" d="M27 40c4-3 10-2 12 2l-2 7H27z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M45 40c4-3 10-2 12 2l-2 7H45z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M35 44q2-3 4 0M37 44q2 3 4 0" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="treaty-handshake-v1"/>', "right",
    ),
    "offering": (
        "offering", "https://thenounproject.com/browse/icons/term/offering/",
        '<path class="ink-wash" d="M43 41c5-3 11-1 13 3l-2 6H43z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M45 46q5-4 10 0M47 50h7" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "prayer": (
        "prayer", "https://thenounproject.com/browse/icons/term/prayer/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M31 34q5-7 10 0M31 35q5 6 10 0M36 29v9" fill="none" stroke="#262522" stroke-width="1.05" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "faith": (
        "faith", "https://thenounproject.com/browse/icons/term/faith/",
        '<path class="ink-wash" d="M29 14c3-5 11-5 14 0l-2 4H31z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M47 41l5-6 5 6-5 6zM52 35v12" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "choice": (
        "choice", "https://thenounproject.com/browse/icons/term/choice/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 50L46 42M51 50l6-8M46 42h5M57 42h-5" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "justice": (
        "justice", "https://thenounproject.com/browse/icons/term/justice/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 35v16M47 39h12M48 39l-3 5h6zM55 39l-3 5h6z" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "learning": (
        "learning", "https://thenounproject.com/browse/icons/term/learning/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 42h11v9H48zM50 44h7M50 47h6" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "purpose": (
        "purpose", "https://thenounproject.com/browse/icons/term/purpose/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 47l5-10 5 10-5-3z" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "safety": (
        "safety", "https://thenounproject.com/browse/icons/term/safety/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 36l7 3v6c0 4-4 7-7 8-3-1-7-4-7-8v-6zM50 45l2 2 4-5" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "value": (
        "value", "https://thenounproject.com/browse/icons/term/value/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><circle class="ink-wash" cx="55" cy="45" r="5" fill="#77746a" data-ink-brush-pass="loaded-dab-v2"/><path class="ink-stroke" d="M55 41v8M52 43q3-2 6 0M52 47q3 2 6 0" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "role": (
        "role", "https://thenounproject.com/browse/icons/term/role/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 42q4-3 8 0v7q-4 3-8 0zM52 39q2-2 4 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "language": (
        "language", "https://thenounproject.com/browse/icons/term/language/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 40h10v8H48zM50 43h6M50 46h5" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "meaning": (
        "meaning", "https://thenounproject.com/browse/icons/term/meaning/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 39v10M49 44h8M50 41l6 6M56 41l-6 6" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "memory": (
        "memory", "https://thenounproject.com/browse/icons/term/memory/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 41h10v10H48zM51 44q2-3 4 0v4h-4z" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "name": (
        "name", "https://thenounproject.com/browse/icons/term/name/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 41h10v9H48zM50 44h6M50 47h5" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "secret": (
        "secret", "https://thenounproject.com/browse/icons/term/secret/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 43q3-3 6 0v7h-6zM52 47h2" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "shadow": (
        "shadow", "https://thenounproject.com/browse/icons/term/shadow/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M48 51q7-5 13 0l-2 9H49z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/>', "right",
    ),
    "dream": (
        "dream", "https://thenounproject.com/browse/icons/term/dream/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42q4-6 8 0q-4 5-8 0M55 36l1-2M59 39l2-1" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "myth": (
        "myth", "https://thenounproject.com/browse/icons/term/myth/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 48q5-8 10-1q-5 4-10 1zM51 44l4-4" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "story": (
        "story", "https://thenounproject.com/browse/icons/term/story/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 41h10v10H48zM50 44h6M50 47h7" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "father": (
        "father", "https://thenounproject.com/browse/icons/term/father/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 42q4-2 8 0M50 46q4-2 8 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "humility": (
        "humility", "https://thenounproject.com/browse/icons/term/humility/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 45q4 4 9 0M50 48q3 2 6 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "kindness": (
        "kindness", "https://thenounproject.com/browse/icons/term/kindness/",
        '<path class="ink-wash" d="M48 40c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 39q-5 4 0 10q5-6 0-10z" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "leadership": (
        "leadership", "https://thenounproject.com/browse/icons/term/leadership/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M54 49V35M50 39l4-4 4 4" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "orphan": (
        "orphan", "https://thenounproject.com/browse/icons/term/orphan/",
        '<path class="ink-wash" d="M48 42c4-3 10-2 12 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 46h9v6h-9zM51 49h5" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "pilgrimage": (
        "pilgrimage", "https://thenounproject.com/browse/icons/term/pilgrimage/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-wash" d="M55 33l2 28h2l-1-28z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M54 39h5M55 46h5M55 53h5" fill="none" stroke="#262522" stroke-width=".8" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "destroyer": (
        "destroyer", "https://thenounproject.com/browse/icons/term/destroyer/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 39l8 10M58 39l-8 10M52 42h4" fill="none" stroke="#262522" stroke-width="1.1" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "art": (
        "art", "https://thenounproject.com/browse/icons/term/art/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 48l8-10M51 49l7-2M50 41l3 2" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "science": (
        "science", "https://thenounproject.com/browse/icons/term/science/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M51 39v6l-4 6h11l-4-6v-6M49 48h7" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "law": (
        "law", "https://thenounproject.com/browse/icons/term/law/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 35v16M47 39h12M48 39l-3 5h6zM55 39l-3 5h6z" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "rights": (
        "rights", "https://thenounproject.com/browse/icons/term/rights/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 40h10v11H49zM51 43h6M51 47h5" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "progress": (
        "progress", "https://thenounproject.com/browse/icons/term/progress/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M48 49l6-10 6 10M51 45h6" fill="none" stroke="#262522" stroke-width="1.0" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "protection": (
        "protection", "https://thenounproject.com/browse/icons/term/protection/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M53 36l7 3v6c0 4-4 7-7 8-3-1-7-4-7-8v-6zM50 45l2 2 4-5" fill="none" stroke="#262522" stroke-width=".9" stroke-linecap="round" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
    "rest": (
        "rest", "https://thenounproject.com/browse/icons/term/rest/",
        '<path class="ink-wash" d="M48 42c4-3 10-2 12 2l-2 6H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M49 51q5-5 10 0M51 48q3-3 6 0" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "left",
    ),
    "legacy": (
        "legacy", "https://thenounproject.com/browse/icons/term/legacy/",
        '<path class="ink-wash" d="M48 39c4-3 10-2 12 2l-2 7H48z" fill="#77746a" data-ink-brush-pass="loaded-mass-v2"/><path class="ink-stroke" d="M50 43h8v8h-8zM52 46h4M52 49h4" fill="none" stroke="#262522" stroke-width=".9" data-ink-brush-pass="recognition-cue-v1"/>', "right",
    ),
}

for name, (role, reference, prop, pose) in ART.items():
    (OUT / f"{name}.svg").write_text(common(name, role, reference, prop, pose), encoding="utf-8")

dream = OUT / "dream.svg"
dream.write_text(
    dream.read_text().replace(
        'data-intentional-components="figure-and-prop-v1"',
        'data-intentional-components="semantic-multipart-v1"',
    ),
    encoding="utf-8",
)

for _name in ("law", "protection"):
    _path = OUT / f"{_name}.svg"
    _path.write_text(
        _path.read_text().replace(
            'data-intentional-components="figure-and-prop-v1"',
            'data-intentional-components="semantic-multipart-v1"',
        ),
        encoding="utf-8",
    )

(OUT / "healer.svg").write_text(healer_svg(), encoding="utf-8")
(OUT / "help.svg").write_text(relationship_svg("help", "help", "https://thenounproject.com/browse/icons/term/help/", "help"), encoding="utf-8")
(OUT / "cooperation.svg").write_text(relationship_svg("cooperation", "cooperation", "https://thenounproject.com/browse/icons/term/cooperation/", "cooperation"), encoding="utf-8")
(OUT / "welcome.svg").write_text(relationship_svg("welcome", "welcome", "https://thenounproject.com/browse/icons/term/welcome/", "welcome"), encoding="utf-8")
(OUT / "conflict.svg").write_text(relationship_svg("conflict", "conflict", "https://thenounproject.com/browse/icons/term/conflict/", "conflict"), encoding="utf-8")
(OUT / "guardian.svg").write_text(relationship_svg("guardian", "guardian", "https://thenounproject.com/browse/icons/term/guardian/", "guardian"), encoding="utf-8")
(OUT / "treaty.svg").write_text(relationship_svg("treaty", "treaty", "https://thenounproject.com/browse/icons/term/treaty/", "cooperation"), encoding="utf-8")
(OUT / "friend.svg").write_text(relationship_svg("friend", "friendship", "https://thenounproject.com/browse/icons/term/friend/", "help"), encoding="utf-8")
(OUT / "alliance.svg").write_text(relationship_svg("alliance", "alliance", "https://thenounproject.com/browse/icons/term/alliance/", "cooperation"), encoding="utf-8")
(OUT / "team.svg").write_text(relationship_svg("team", "teamwork", "https://thenounproject.com/browse/icons/term/team/", "cooperation"), encoding="utf-8")
(OUT / "care.svg").write_text(relationship_svg("care", "care", "https://thenounproject.com/browse/icons/term/care/", "help"), encoding="utf-8")
(OUT / "trust.svg").write_text(relationship_svg("trust", "trust", "https://thenounproject.com/browse/icons/term/trust/", "help"), encoding="utf-8")
(OUT / "share.svg").write_text(relationship_svg("share", "sharing", "https://thenounproject.com/browse/icons/term/share/", "cooperation"), encoding="utf-8")
(OUT / "compassion.svg").write_text(relationship_svg("compassion", "compassion", "https://thenounproject.com/browse/icons/term/compassion/", "help"), encoding="utf-8")
(OUT / "empathy.svg").write_text(relationship_svg("empathy", "empathy", "https://thenounproject.com/browse/icons/term/empathy/", "help"), encoding="utf-8")
(OUT / "invite.svg").write_text(relationship_svg("invite", "invitation", "https://thenounproject.com/browse/icons/term/invite/", "welcome"), encoding="utf-8")
(OUT / "game.svg").write_text(relationship_svg("game", "game", "https://thenounproject.com/browse/icons/term/game/", "cooperation"), encoding="utf-8")
(OUT / "council.svg").write_text(group_svg("council", "council", "https://thenounproject.com/browse/icons/term/council/"), encoding="utf-8")
(OUT / "ritual.svg").write_text(group_svg("ritual", "ritual", "https://thenounproject.com/browse/icons/term/ritual/"), encoding="utf-8")
(OUT / "trade.svg").write_text(relationship_svg("trade", "trade", "https://thenounproject.com/browse/icons/term/trade/", "cooperation"), encoding="utf-8")
(OUT / "group.svg").write_text(group_svg("group", "group", "https://thenounproject.com/browse/icons/term/group/"), encoding="utf-8")
(OUT / "community.svg").write_text(group_svg("community", "community", "https://thenounproject.com/browse/icons/term/community/"), encoding="utf-8")
(OUT / "tribe.svg").write_text(group_svg("tribe", "tribe", "https://thenounproject.com/browse/icons/term/tribe/"), encoding="utf-8")
(OUT / "diversity.svg").write_text(group_svg("diversity", "diversity", "https://thenounproject.com/browse/icons/term/diversity/"), encoding="utf-8")
(OUT / "peace.svg").write_text(relationship_svg("peace", "peace", "https://thenounproject.com/browse/icons/term/peace/", "welcome"), encoding="utf-8")

print(f"redrew {len(ART)} isolated full-bodied role figures and three interaction studies")
