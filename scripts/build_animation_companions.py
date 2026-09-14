#!/usr/bin/env python3
"""Build lightweight animated companions beside the static SVG catalogue."""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "animations" / "generated"
FACE_CODES = set(range(0x1F600, 0x1F650)) | {0x263A, 0x1F914, 0x1F9D0, 0x1F979, 0x1F972}
FACE_BEHAVIORS = {
    0x1F600: "blink", 0x1F601: "blink", 0x1F603: "blink", 0x1F604: "blink",
    0x1F605: "sweat", 0x1F606: "laugh", 0x1F602: "laugh", 0x1F923: "roll",
    0x1F609: "wink", 0x1F914: "think", 0x1F9D0: "inspect", 0x1F979: "tear",
    0x1F972: "bittersweet", 0x1F644: "look", 0x263A: "breathe",
}

def wrapper(name: str, href: str, kind: str) -> str:
    title = escape(name.replace("-", " ").title())
    motion = {
        "blink": "@keyframes m{0%,89%,100%{transform:scaleY(1)}94%,97%{transform:scaleY(.08)}}",
        "bob": "@keyframes m{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.5px)}}",
        "walk": "@keyframes m{0%,100%{transform:translateX(0) rotate(0)}50%{transform:translateX(1px) rotate(1deg)}}",
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 84 84" role="img" aria-label="{title} animated" data-emoji-animation="{kind}-v1"><title>{title} animated</title><image href="{href}" x="-6" y="-6" width="84" height="84"/><style>{motion}svg{{transform-origin:center;animation:m 3.8s ease-in-out infinite}}@media(prefers-reduced-motion:reduce){{svg{{animation:none}}}}</style></svg>'''

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted((ROOT / "assets" / "color-all").glob("*.svg")):
        try: code = int(path.stem.split("-")[0], 16)
        except ValueError: continue
        if code not in FACE_CODES: continue
        kind = FACE_BEHAVIORS.get(code, "blink")
        (OUT / f"{path.stem}.svg").write_text(wrapper(path.stem, f"../../color-all/{path.name}", kind) + "\n", encoding="utf-8")
        count += 1
    for root in ("animals", "dinosaurs", "sea_creatures"):
        for path in sorted((ROOT / "assets" / "pua" / root).glob("*.svg")):
            target = OUT / f"{root}-{path.stem}.svg"
            target.write_text(wrapper(f"{root} {path.stem}", f"../../pua/{root}/{path.name}", "walk") + "\n", encoding="utf-8")
            count += 1
    print(f"built {count} animated companions in {OUT.relative_to(ROOT)}")

if __name__ == "__main__": main()
