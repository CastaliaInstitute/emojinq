#!/usr/bin/env python3
"""Build lightweight animated companions beside the static SVG catalogue."""
from pathlib import Path
import json
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "animations" / "generated"
FACE_CODES = set(range(0x1F600, 0x1F650)) | {0x263A, 0x1F914, 0x1F923, 0x1F9D0, 0x1F979, 0x1F972}
FACE_BEHAVIORS = {
    0x1F600: "blink", 0x1F601: "blink", 0x1F603: "blink", 0x1F604: "blink",
    0x1F605: "sweat", 0x1F606: "laugh", 0x1F602: "laugh", 0x1F923: "roll",
    0x1F609: "wink", 0x1F914: "think", 0x1F9D0: "inspect", 0x1F979: "tear",
    0x1F972: "bittersweet", 0x1F644: "look", 0x263A: "breathe",
}
# Give the rest of the classic face sequence an expressive baseline tied to
# its meaning, while preserving explicit overrides above.
for _code in range(0x1F600, 0x1F64B):
    if _code in FACE_BEHAVIORS:
        continue
    if _code in set(range(0x1F606, 0x1F610)):
        FACE_BEHAVIORS[_code] = "laugh"
    elif _code in set(range(0x1F610, 0x1F618)):
        FACE_BEHAVIORS[_code] = "look"
    elif _code in set(range(0x1F618, 0x1F61E)):
        FACE_BEHAVIORS[_code] = "breathe"
    elif _code in set(range(0x1F61E, 0x1F626)):
        FACE_BEHAVIORS[_code] = "tear"
    elif _code in set(range(0x1F626, 0x1F634)):
        FACE_BEHAVIORS[_code] = "sweat"
    elif _code in set(range(0x1F634, 0x1F63A)):
        FACE_BEHAVIORS[_code] = "breathe"
    else:
        FACE_BEHAVIORS[_code] = "blink"
STANDARD_ANIMAL_CODES = (set(range(0x1F400, 0x1F440)) | set(range(0x1F980, 0x1F9A3)) | set(range(0x1FAB6, 0x1FABA)))

def wrapper(name: str, href: str, kind: str) -> str:
    title = escape(name.replace("-", " ").title())
    motion = {
        "blink": "@keyframes m{0%,89%,100%{transform:scaleY(1)}94%,97%{transform:scaleY(.08)}}",
        "bob": "@keyframes m{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.5px)}}",
        "walk": "@keyframes m{0%,100%{transform:translateX(0) rotate(0)}50%{transform:translateX(1px) rotate(1deg)}}",
        "stride": "@keyframes m{0%,100%{transform:translate(0,0) rotate(-1deg)}25%{transform:translate(1px,-1px) rotate(1deg)}50%{transform:translate(2px,0) rotate(-1deg)}75%{transform:translate(1px,-1px) rotate(1deg)}}",
        "wingbeat": "@keyframes m{0%,100%{transform:translateY(0) rotate(0)}35%{transform:translateY(-2px) rotate(-2deg)}65%{transform:translateY(1px) rotate(2deg)}}",
        "swim": "@keyframes m{0%,100%{transform:translateX(-1px) rotate(-1deg)}50%{transform:translateX(2px) rotate(1deg)}}",
        "buzz": "@keyframes m{0%,100%{transform:rotate(-1deg)}25%,75%{transform:rotate(1deg)}}",
        "heavy-stride": "@keyframes m{0%,100%{transform:translateY(0) rotate(-1deg)}45%{transform:translateY(-1px) rotate(1deg)}55%{transform:translateY(1px) rotate(0)}}",
        "laugh": "@keyframes m{0%,100%{transform:translateY(0) rotate(-1deg)}50%{transform:translateY(-2px) rotate(1deg)}}",
        "roll": "@keyframes m{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}",
        "sweat": "@keyframes m{0%,100%{transform:translateY(0)}45%{transform:translateY(1px)}60%{transform:translateY(0)}}",
        "wink": "@keyframes m{0%,70%,100%{transform:scaleY(1)}76%,84%{transform:scaleY(.97)}}",
        "think": "@keyframes m{0%,100%{transform:translateX(0)}45%,65%{transform:translateX(1px)}}",
        "inspect": "@keyframes m{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}",
        "tear": "@keyframes m{0%,65%,100%{transform:translateY(0)}80%{transform:translateY(2px)}90%{transform:translateY(4px)}}",
        "bittersweet": "@keyframes m{0%,100%{transform:translateY(0)}50%{transform:translateY(1px)}}",
        "look": "@keyframes m{0%,25%,100%{transform:translateX(0)}45%,60%{transform:translateX(-1px)}75%,90%{transform:translateX(1px)}}",
        "breathe": "@keyframes m{0%,100%{transform:scale(1)}50%{transform:scale(1.015)}}",
    }[kind]
    detail = {
        "blink": '<g class="features" fill="none" stroke="#262421" stroke-width="1.2" stroke-linecap="round"><path class="blink-left" d="M25 31q3-2 6 0"/><path class="blink-right" d="M43 31q3-2 6 0"/></g>',
        "wink": '<g class="features" fill="none" stroke="#262421" stroke-width="1.2" stroke-linecap="round"><path d="M25 31q3-2 6 0"/><path class="wink-eye" d="M43 31h6"/></g>',
        "look": '<g class="features" fill="#262421"><circle class="pupil-left" cx="28" cy="31" r="1.2"/><circle class="pupil-right" cx="46" cy="31" r="1.2"/></g>',
        "think": '<g class="features" fill="#262421"><circle class="pupil-left" cx="28" cy="31" r="1.2"/><circle class="pupil-right" cx="46" cy="31" r="1.2"/><circle class="thought" cx="58" cy="18" r="1.4"/><circle class="thought" cx="62" cy="14" r="2"/></g>',
        "inspect": '<g class="features" fill="none" stroke="#262421" stroke-width="1.1"><circle cx="28" cy="31" r="2"/><circle cx="46" cy="31" r="2"/><path d="M49 33l3 3"/></g>',
        "tear": '<g class="features" fill="#6b8fa3"><ellipse class="tear-left" cx="28" cy="34" rx="1.4" ry="2"/><ellipse class="tear-right" cx="46" cy="34" rx="1.4" ry="2"/></g>',
        "sweat": '<g class="features" fill="#6b8fa3"><path class="sweat-drop" d="M55 25q3 4 0 6q-3-2 0-6z"/></g>',
        "stride": '<g class="limbs" fill="none" stroke="#262421" stroke-width="1" stroke-linecap="round"><path d="M24 55l-2 7M31 55l2 7M43 55l-2 7M50 55l2 7"/><path d="M24 55l2 2M31 55l-2 2M43 55l2 2M50 55l-2 2"/></g>',
        "heavy-stride": '<g class="limbs" fill="none" stroke="#262421" stroke-width="1.3" stroke-linecap="round"><path d="M23 54l-3 8M32 55l2 8M43 55l-2 8M51 54l3 8"/></g>',
        "wingbeat": '<g class="wings" fill="none" stroke="#4a4943" stroke-width="1" stroke-linecap="round"><path d="M26 27q-8-7-10-1M48 27q8-7 10-1"/></g>',
        "swim": '<path class="tail" d="M55 38q7-5 10 0q-7 5-10 0" fill="none" stroke="#4a4943" stroke-width="1"/>',
        "buzz": '<g class="vibrate" fill="none" stroke="#4a4943" stroke-width=".8"><path d="M18 24l-3-2M54 24l3-2M18 28l-4 0M54 28l4 0"/></g>',
    }.get(kind, '')
    feature_motion = {
        "blink": ".features{animation:face-blink 3.8s ease-in-out infinite}@keyframes face-blink{0%,89%,100%{opacity:1}94%,97%{opacity:.1}}",
        "wink": ".wink-eye{animation:face-wink 3.8s ease-in-out infinite}@keyframes face-wink{0%,70%,100%{transform:scaleY(1)}76%,84%{transform:scaleY(.08)}}",
        "look": ".pupil-left,.pupil-right{animation:face-look 4.2s ease-in-out infinite}@keyframes face-look{0%,30%,100%{transform:translateX(0)}50%,65%{transform:translateX(2px)}80%{transform:translateX(-1px)}}",
        "think": ".thought{animation:thought 2.4s ease-in-out infinite}@keyframes thought{0%,100%{opacity:.25}50%{opacity:1}}",
        "tear": ".tear-left,.tear-right{animation:tear-drip 3.8s ease-in infinite}@keyframes tear-drip{0%,55%{transform:translateY(0);opacity:0}65%{opacity:1}90%{transform:translateY(13px);opacity:.8}100%{transform:translateY(18px);opacity:0}}",
        "sweat": ".sweat-drop{animation:sweat-drop 3.8s ease-in infinite}@keyframes sweat-drop{0%,55%{transform:translateY(0);opacity:0}70%{opacity:1}100%{transform:translateY(12px);opacity:0}}",
    }.get(kind, "")
    target = ".body,.limbs,.wings,.tail,.vibrate,.features"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-6 -6 84 84" role="img" aria-label="{title} animated" data-emoji-animation="{kind}-v1"><title>{title} animated</title><g class="body"><image href="{href}" xlink:href="{href}" x="-6" y="-6" width="84" height="84"/></g>{detail}<style>{motion}{feature_motion}.body{{transform-origin:center;animation:m 3.8s ease-in-out infinite}}.limbs,.wings,.tail,.vibrate{{transform-box:fill-box;transform-origin:center;animation:m 3.8s ease-in-out infinite}}@media(prefers-reduced-motion:reduce){{{target}{{animation:none}}}}</style></svg>'''

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    records = []
    for path in sorted((ROOT / "assets" / "color-all").glob("*.svg")):
        try: code = int(path.stem.split("-")[0], 16)
        except ValueError: continue
        if code not in FACE_CODES: continue
        kind = FACE_BEHAVIORS.get(code, "blink")
        (OUT / f"{path.stem}.svg").write_text(wrapper(path.stem, f"../../color-all/{path.name}", kind) + "\n", encoding="utf-8")
        records.append({"name": path.stem, "category": "face", "animation": kind, "static": f"color-all/{path.name}", "source": f"animations/generated/{path.stem}.svg"})
        count += 1
        continue
    for path in sorted((ROOT / "assets" / "color-all").glob("*.svg")):
        try: code = int(path.stem.split("-")[0], 16)
        except ValueError: continue
        if code not in STANDARD_ANIMAL_CODES: continue
        if code in {0x1F426, 0x1F427, 0x1F428, 0x1F42D, 0x1F989, 0x1F99A}: kind = "wingbeat"
        elif code in {0x1F41F, 0x1F420, 0x1F421, 0x1F422, 0x1F988, 0x1F99E}: kind = "swim"
        elif code in {0x1F41D, 0x1F41E, 0x1F98B, 0x1F99F}: kind = "buzz"
        else: kind = "stride"
        (OUT / f"unicode-animal-{path.stem}.svg").write_text(wrapper(f"unicode animal {path.stem}", f"../../color-all/{path.name}", kind) + "\n", encoding="utf-8")
        records.append({"name": path.stem, "category": "animal", "animation": kind, "static": f"color-all/{path.name}", "source": f"animations/generated/unicode-animal-{path.stem}.svg"})
        count += 1
    for root in ("animals", "dinosaurs", "sea_creatures"):
        for path in sorted((ROOT / "assets" / "pua" / root).glob("*.svg")):
            target = OUT / f"{root}-{path.stem}.svg"
            if root == "dinosaurs": kind = "heavy-stride"
            elif root == "sea_creatures": kind = "swim"
            elif path.stem in {"bee", "fly", "mosquito"}: kind = "buzz"
            elif path.stem in {"bird", "chicken", "duck", "owl", "rooster"}: kind = "wingbeat"
            else: kind = "stride"
            target.write_text(wrapper(f"{root} {path.stem}", f"../../pua/{root}/{path.name}", kind) + "\n", encoding="utf-8")
            records.append({"name": path.stem, "category": root, "animation": kind, "static": f"pua/{root}/{path.name}", "source": f"animations/generated/{target.name}"})
            count += 1
    (ROOT / "assets" / "animations" / "manifest.json").write_text(json.dumps({"schemaVersion": 1, "contract": "face-v1 / animal-v1", "companions": records}, indent=2) + "\n", encoding="utf-8")
    print(f"built {count} animated companions in {OUT.relative_to(ROOT)}")

if __name__ == "__main__": main()
