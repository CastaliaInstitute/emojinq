#!/usr/bin/env python3
"""Author the canonical Castalia Emojinq PUA glyph set."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"
OUT = PUA / "castalia"
MANIFEST = PUA / "manifest.json"
ROOK_CODEPOINT = 0xF1520
SEAL_CODEPOINT = 0xF1521
SUBMARINE_CODEPOINT = 0xF1522
MERMAID_CODEPOINT = 0xF1523
PUNCH_CODEPOINT = 0xF1524
JUDY_CODEPOINT = 0xF1525
LEFT_HAND_CODEPOINT = 0xF1526
RIGHT_HAND_CODEPOINT = 0xF1527
PUPPET_SHOE_CODEPOINT = 0xF1528
PIRATE_SHIP_CODEPOINT = 0xF1529

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"
  role="img" aria-label="Castalia rook and three-lobed flame" data-pua="U+F1520"
  data-logo-source="https://castalia.institute/logo.png"
  data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2"
  data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
  <title>Castalia — the Institute rook and three-lobed flame</title>
  <!-- Faithful vector trace of the supplied Institute mark. The narrow,
       crenellated rook and organic three-lobed flame are its identity. -->
  <path class="ink-wash" fill="#4a4943" d="M 35.303,2.937999999999988 C 35.32,4.518999999999991 35.32,4.535999999999987 34.504,6.065999999999995 C 33.705,7.6299999999999955 33.127,9.380999999999993 33.297,9.737999999999992 C 33.348,9.83999999999999 33.263,9.771999999999991 33.127,9.601999999999997 C 32.94,9.363999999999997 32.855,8.904999999999994 32.855,8.105999999999995 C 32.855,7.476999999999997 32.787,6.949999999999996 32.719,6.949999999999996 C 32.413,6.949999999999996 31.801000000000002,7.782999999999994 31.495,8.632999999999996 C 30.543,11.114999999999995 31.648,13.851999999999997 34.045,14.922999999999995 C 35.371,15.517999999999994 35.762,15.347999999999992 35.269,14.412999999999997 C 34.827,13.546 34.878,11.352999999999994 35.371,10.315999999999995 C 35.779,9.448999999999998 36.085,9.142999999999994 36.085,9.584999999999994 C 36.085,9.720999999999997 36.289,10.24799999999999 36.544,10.740999999999993 C 37.105,11.828999999999994 37.19,13.664999999999992 36.714,14.549 C 36.561,14.854999999999997 36.425,15.127000000000002 36.425,15.194999999999993 C 36.425,15.398999999999994 37.258,15.245999999999995 38.04,14.871999999999993 C 40.318,13.800999999999995 41.44,11.25099999999999 40.76,8.734999999999992 C 40.471000000000004,7.663999999999994 39.655,6.269999999999989 39.315,6.269999999999996 C 39.213,6.269999999999996 39.145,6.711999999999996 39.145,7.238999999999997 C 39.145,7.918999999999997 39.043,8.394999999999996 38.805,8.768999999999998 C 38.618,9.074999999999996 38.448,9.329999999999998 38.414,9.329999999999998 C 38.38,9.329999999999998 38.431,8.905000000000001 38.533,8.377999999999993 C 38.737,7.170999999999992 38.465,5.419999999999995 37.853,4.128 C 37.394,3.159000000000006 35.864,1.3400000000000034 35.507,1.3399999999999892 C 35.354,1.3399999999999892 35.303,1.7819999999999823 35.303,2.937999999999988"/>
  <path class="ink-wash" fill="#262522" d="M 32.464,15.908999999999999 C 32.396,15.96 32.345,16.351 32.345,16.758999999999993 C 32.345,17.472999999999992 32.345,17.489999999999995 31.75,17.489999999999995 C 31.240000000000002,17.489999999999995 31.155,17.421999999999997 31.053,17.013999999999996 C 30.849,16.061999999999998 30.9,16.078999999999994 29.659,16.214999999999996 C 29.03,16.282999999999994 28.451999999999998,16.401999999999994 28.366999999999997,16.486999999999995 C 28.265,16.571999999999996 28.366999999999997,17.438999999999993 28.605,18.68 C 28.945,20.533 29.03,20.753999999999998 29.472,21.076999999999998 C 29.744,21.263999999999996 29.965,21.536 29.965,21.671999999999997 C 29.965,21.808 30.169,22.012 30.407,22.113999999999997 L 30.866,22.317999999999998 L 30.747,24.544999999999995 C 30.543,28.437999999999995 29.914,33.333999999999996 29.183,36.547 L 28.927999999999997,37.68599999999999 L 28.247999999999998,37.771 C 27.857,37.821999999999996 27.517,37.89 27.482999999999997,37.924 C 27.448999999999998,37.974999999999994 27.381,38.382999999999996 27.33,38.842 C 27.092,40.864999999999995 27.262,40.644 25.205,41.613 C 24.168,42.105999999999995 23.335,42.548 23.335,42.616 C 23.335,42.684 23.216,43.415 23.097,44.265 C 22.944,45.233999999999995 22.927,45.863 23.012,45.965 C 23.317999999999998,46.271 25.544999999999998,46.39 33.772999999999996,46.492 C 42.256,46.611 48.546,46.407 48.954,45.998999999999995 C 49.09,45.846000000000004 49.09,45.421 48.903,44.265 C 48.784,43.41499999999999 48.665,42.684 48.665,42.616 C 48.665,42.565 47.849000000000004,42.123000000000005 46.846000000000004,41.629999999999995 C 45.843,41.153999999999996 44.959,40.678 44.891,40.559 C 44.823,40.44 44.755,40.032 44.755,39.658 C 44.755,39.266999999999996 44.704,38.723 44.653,38.434 C 44.551,37.958 44.466,37.89 43.803,37.788 C 43.225,37.702999999999996 43.038,37.601 42.97,37.312 C 42.545,35.51 42.341,34.422 42.052,32.449999999999996 C 41.661,29.848999999999997 41.219,25.513999999999996 41.168,23.626999999999995 C 41.134,22.419999999999995 41.150999999999996,22.368999999999993 41.576,22.130999999999993 C 41.831,22.011999999999993 42.035,21.807999999999993 42.035,21.689 C 42.035,21.57 42.256,21.281 42.511,21.059999999999995 C 42.936,20.685999999999993 43.055,20.362999999999992 43.395,18.628999999999998 C 43.633,17.354 43.718,16.555 43.616,16.452999999999996 C 43.531,16.367999999999995 42.936,16.282999999999994 42.29,16.248999999999996 L 41.117,16.214999999999996 L 40.964,16.860999999999997 C 40.811,17.455999999999996 40.76,17.506999999999998 40.267,17.455999999999996 C 39.774,17.404999999999994 39.74,17.354 39.655,16.639999999999993 L 39.57,15.874999999999993 L 38.414,15.823999999999998 C 37.054,15.772999999999996 36.765,15.925999999999995 36.765,16.741999999999997 C 36.765,17.32 36.748,17.32 36.0,17.319999999999993 C 35.252,17.319999999999993 35.235,17.30299999999999 35.235,16.758999999999993 C 35.235,16.452999999999996 35.15,16.112999999999992 35.031,15.993999999999993 C 34.81,15.772999999999996 32.650999999999996,15.704999999999991 32.464,15.908999999999992"/>
</svg>
"""

SEAL_SVG = SVG.replace('data-pua="U+F1520"','data-pua="U+F1521"').replace(
  'aria-label="Castalia rook and three-lobed flame"','aria-label="Castalia maker seal"')
# The Institute mark is intentionally tall and narrow on its own. Inside a
# square hanko that original bounding box sat high with most of the lower and
# side field empty. Scale it optically around x=36 and lower it so flame,
# rook and negative space carry comparable visual weight.
SEAL_SVG = SEAL_SVG.replace(
  '  <path class="ink-wash" fill="#4a4943"',
  '  <g transform="matrix(1.35 0 0 1.08 -12.6 10)">\n  <path class="ink-wash" fill="#4a4943"',
  1,
)
SEAL_SVG = SEAL_SVG.replace('</svg>', '''
  </g>
  <!-- Optically balanced double border: still an imperfect carved hanko,
       but with nearly equal opposing margins and quieter inner weight. -->
  <path d="M5.5 6 L66 5.5 L66.5 66 L6 66.5 Z" fill="none" stroke="#262522"
    stroke-width="3" stroke-linecap="square" stroke-linejoin="miter"/>
  <path d="M9.5 10 L62 9.5 L62.5 62 L10 62.5 Z" fill="none" stroke="#4a4943"
    stroke-width="1.1" stroke-linecap="square" opacity=".72"/>
</svg>''')

SUBMARINE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"
  role="img" aria-label="Castalia research submarine" data-pua="U+F1522"
  data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1"
  data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
  <title>Castalia research submarine — rounded hull, portholes and periscope</title>
  <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
    <!-- An original, friendly field-research vessel: the silhouette keeps the
         buoyant optimism of the reference without its characters or details. -->
    <path d="M11 39 C14 28 26 24 43 25 C55 26 63 31 66 38 C63 48 51 52 32 51 C20 51 13 47 11 39 Z" stroke-width="3.4"/>
    <path d="M25 27 C28 19 36 16 44 19 C47 21 49 24 50 28" stroke-width="3.0"/>
    <path d="M34 18 L34 11 L42 11 L42 7" stroke-width="2.7"/>
    <path d="M41 7 L48 7" stroke-width="2.7"/>
    <path d="M15 34 L7 28 L7 49 L15 44" stroke-width="2.8"/>
    <path d="M7 34 C2 32 2 39 7 38 M7 39 C2 39 2 46 7 43" stroke-width="1.8"/>
    <path d="M28 51 L23 58 M46 51 L52 57" stroke-width="2.4"/>
    <path d="M57 33 Q63 37 57 44" stroke-width="1.4" opacity=".72"/>
    <circle cx="25" cy="38" r="4.2" stroke-width="2.2"/>
    <circle cx="38" cy="38" r="4.2" stroke-width="2.2"/>
    <circle cx="51" cy="38" r="4.2" stroke-width="2.2"/>
    <path d="M21 31 Q37 28 56 31 M18 46 Q35 49 55 46" stroke-width="1.1" opacity=".65"/>
    <path d="M16 60 Q30 57 43 60 M48 60 Q56 58 65 61" stroke-width="1.0" opacity=".55"/>
  </g>
</svg>
"""

MERMAID_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"
  role="img" aria-label="Atlas mermaid guide" data-pua="U+F1523"
  data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1"
  data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
  <title>Atlas mermaid guide — full figure with flowing hair and fish tail</title>
  <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="33" cy="15" r="6.2" stroke-width="2.7"/>
    <path d="M28 11 C20 14 22 26 27 30 M28 9 C21 7 18 15 21 22" stroke-width="2.2"/>
    <path d="M38 11 C45 16 42 25 39 29" stroke-width="2.0"/>
    <path d="M29 22 C29 31 25 37 28 43 C31 49 39 49 42 44 C46 37 40 31 38 22" stroke-width="3.0"/>
    <path d="M28 30 L18 36 L11 32 M40 30 L49 35 L57 29" stroke-width="2.6"/>
    <path d="M31 45 C29 54 34 60 43 59 C50 58 54 52 59 50" stroke-width="3.4"/>
    <path d="M59 50 C57 58 60 63 66 66 C58 67 51 64 48 60" stroke-width="2.8"/>
    <path d="M57 29 L61 19 M58 25 L64 25 M59 21 L64 17" stroke-width="1.7"/>
    <path d="M25 43 Q34 47 42 43 M30 37 Q35 40 40 37" stroke-width="1.0" opacity=".68"/>
    <path d="M8 66 Q21 63 34 66 M39 66 Q49 64 60 67" stroke-width="1.0" opacity=".55"/>
  </g>
</svg>
"""

PUNCH_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
 aria-label="Punch hand-puppet torso" data-pua="U+F1524" data-castalia-style="sumi-e-ink-wash-v1"
 data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
 <title>Punch — traditional hooked-nose hand-puppet torso</title>
 <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
  <path d="M19 22 C18 10 29 5 41 10 L50 4 L48 19" stroke-width="3.0"/>
  <path d="M22 17 C13 19 12 31 18 38 C21 42 27 43 33 40" stroke-width="3.2"/>
  <path d="M29 18 C39 14 47 21 44 29 L54 32 L43 35 C41 43 30 45 23 39" stroke-width="3.0"/>
  <circle cx="34" cy="25" r="1.8" stroke-width="1.5"/><path d="M32 35 Q37 39 42 34" stroke-width="1.8"/>
  <path d="M24 42 C17 48 14 60 14 68 M42 42 C50 49 54 59 56 68" stroke-width="3.3"/>
  <path d="M25 43 Q34 50 42 43 M20 51 Q34 58 49 51" stroke-width="2.0"/>
  <path d="M13 68 Q34 63 57 68" stroke-width="2.2"/>
 </g>
</svg>
"""

JUDY_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
 aria-label="Judy hand-puppet torso" data-pua="U+F1525" data-castalia-style="sumi-e-ink-wash-v1"
 data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
 <title>Judy — traditional bonneted hand-puppet torso</title>
 <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
  <path d="M18 25 C14 14 24 7 35 8 C47 8 54 18 50 30" stroke-width="3.0"/>
  <path d="M19 19 Q34 8 49 19 M16 23 Q34 17 53 24" stroke-width="2.5"/>
  <path d="M22 22 C18 29 21 40 31 43 C41 46 49 39 49 29" stroke-width="3.0"/>
  <circle cx="30" cy="28" r="1.5" stroke-width="1.4"/><circle cx="42" cy="28" r="1.5" stroke-width="1.4"/>
  <path d="M31 36 Q36 40 42 35 M19 20 L13 31 M50 20 L57 31" stroke-width="1.8"/>
  <path d="M26 43 C18 49 15 59 14 68 M45 42 C53 49 56 59 58 68" stroke-width="3.2"/>
  <path d="M25 44 Q35 51 46 43 M19 53 Q36 60 52 52" stroke-width="2.0"/>
  <path d="M13 68 Q35 63 59 68" stroke-width="2.2"/>
 </g>
</svg>
"""

LEFT_HAND_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
 aria-label="Puppet left hand" data-pua="U+F1526" data-castalia-style="sumi-e-ink-wash-v1"
 data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
 <title>Puppet left hand — open palm</title>
 <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
  <path d="M23 62 C16 54 13 44 16 34 C18 29 22 30 24 36 L25 20 C25 14 31 14 32 20 L33 12 C34 7 40 8 40 14 L40 20 L42 12 C44 8 49 10 48 15 L47 23 L50 17 C53 13 58 17 56 21 L50 38 C48 48 43 57 35 62 Z" stroke-width="3.5"/>
  <path d="M24 36 Q29 40 33 47 M32 20 L32 38 M40 20 L39 38 M47 23 L45 40" stroke-width="1.5" opacity=".72"/>
 </g>
</svg>
"""

RIGHT_HAND_SVG = LEFT_HAND_SVG.replace("U+F1526", "U+F1527").replace("Puppet left hand", "Puppet right hand").replace('<g fill="none"', '<g transform="translate(72 0) scale(-1 1)" fill="none"')

PUPPET_SHOE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
 aria-label="Puppet shoe" data-pua="U+F1528" data-castalia-style="sumi-e-ink-wash-v1"
 data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
 <title>Puppet shoe — soft stage slipper</title>
 <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
  <path d="M15 23 C22 17 31 18 35 28 L39 39 C48 42 57 42 62 48 C65 52 62 58 56 59 L18 59 C11 58 9 51 12 43 Z" stroke-width="3.7"/>
  <path d="M17 42 Q30 47 40 39 M13 52 Q36 55 60 51 M25 25 Q30 29 34 28" stroke-width="1.7" opacity=".72"/>
 </g>
</svg>
"""

PIRATE_SHIP_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img"
 aria-label="Castalia sailing ship" data-pua="U+F1529" data-castalia-style="sumi-e-ink-wash-v1"
 data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized" data-ink-coverage="complete">
 <title>Castalia sailing ship — square rig, compass pennant and teaching vessel</title>
 <g fill="none" stroke="#302d28" stroke-linecap="round" stroke-linejoin="round">
  <path d="M10 49 Q34 56 61 48 L55 59 Q34 65 16 58 Z" stroke-width="3.5"/>
  <path d="M35 48 L35 10 M19 48 L19 22 M51 49 L51 20" stroke-width="2.7"/>
  <path d="M34 13 Q24 20 22 34 L34 35 Z M37 14 Q49 19 50 34 L37 35 Z" stroke-width="2.6"/>
  <path d="M18 24 Q12 31 12 41 L18 42 Z M52 22 Q61 28 62 41 L52 42 Z" stroke-width="2.2"/>
  <path d="M35 10 L47 13 L35 17" stroke-width="1.9"/>
  <path d="M22 48 L22 55 M30 51 L30 58 M39 52 L39 59 M48 51 L48 57" stroke-width="1.2" opacity=".68"/>
  <path d="M7 65 Q18 62 29 65 M34 65 Q46 62 65 65" stroke-width="1.1" opacity=".58"/>
 </g>
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rook-flame.svg").write_text(SVG)
    (OUT / "maker-seal.svg").write_text(SEAL_SVG)
    (OUT / "research-submarine.svg").write_text(SUBMARINE_SVG)
    (OUT / "mermaid-guide.svg").write_text(MERMAID_SVG)
    (OUT / "punch-torso.svg").write_text(PUNCH_SVG)
    (OUT / "judy-torso.svg").write_text(JUDY_SVG)
    (OUT / "puppet-left-hand.svg").write_text(LEFT_HAND_SVG)
    (OUT / "puppet-right-hand.svg").write_text(RIGHT_HAND_SVG)
    (OUT / "puppet-shoe.svg").write_text(PUPPET_SHOE_SVG)
    (OUT / "pirate-ship.svg").write_text(PIRATE_SHIP_SVG)
    entries = json.loads(MANIFEST.read_text())
    entries = [entry for entry in entries if not {ROOK_CODEPOINT, SEAL_CODEPOINT, SUBMARINE_CODEPOINT, MERMAID_CODEPOINT, PUNCH_CODEPOINT, JUDY_CODEPOINT, LEFT_HAND_CODEPOINT, RIGHT_HAND_CODEPOINT, PUPPET_SHOE_CODEPOINT, PIRATE_SHIP_CODEPOINT}.intersection(entry.get("codepoints", []))]
    entries.extend([
        {"name": f"{ROOK_CODEPOINT:X}", "source": "castalia/rook-flame.svg", "codepoints": [ROOK_CODEPOINT], "label": "castalia/rook-flame"},
        {"name": f"{SEAL_CODEPOINT:X}", "source": "castalia/maker-seal.svg", "codepoints": [SEAL_CODEPOINT], "label": "castalia/maker-seal"},
        {"name": f"{SUBMARINE_CODEPOINT:X}", "source": "castalia/research-submarine.svg", "codepoints": [SUBMARINE_CODEPOINT], "label": "castalia/research-submarine"},
        {"name": f"{MERMAID_CODEPOINT:X}", "source": "castalia/mermaid-guide.svg", "codepoints": [MERMAID_CODEPOINT], "label": "castalia/mermaid-guide"},
        {"name": f"{PUNCH_CODEPOINT:X}", "source": "castalia/punch-torso.svg", "codepoints": [PUNCH_CODEPOINT], "label": "castalia/punch-torso"},
        {"name": f"{JUDY_CODEPOINT:X}", "source": "castalia/judy-torso.svg", "codepoints": [JUDY_CODEPOINT], "label": "castalia/judy-torso"},
        {"name": f"{LEFT_HAND_CODEPOINT:X}", "source": "castalia/puppet-left-hand.svg", "codepoints": [LEFT_HAND_CODEPOINT], "label": "castalia/puppet-left-hand"},
        {"name": f"{RIGHT_HAND_CODEPOINT:X}", "source": "castalia/puppet-right-hand.svg", "codepoints": [RIGHT_HAND_CODEPOINT], "label": "castalia/puppet-right-hand"},
        {"name": f"{PUPPET_SHOE_CODEPOINT:X}", "source": "castalia/puppet-shoe.svg", "codepoints": [PUPPET_SHOE_CODEPOINT], "label": "castalia/puppet-shoe"},
        {"name": f"{PIRATE_SHIP_CODEPOINT:X}", "source": "castalia/pirate-ship.svg", "codepoints": [PIRATE_SHIP_CODEPOINT], "label": "castalia/pirate-ship"},
    ])
    entries.sort(key=lambda entry: entry["codepoints"])
    MANIFEST.write_text(json.dumps(entries, indent=2) + "\n")
    print("build_castalia_pua: wrote U+F1520–U+F1529")


if __name__ == "__main__":
    main()
