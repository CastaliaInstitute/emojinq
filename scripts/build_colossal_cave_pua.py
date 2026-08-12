#!/usr/bin/env python3
"""Author compact naturalist marks for Atlas's Colossal Cave locations/items."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
PUA=ROOT/'assets'/'pua'; MANIFEST=PUA/'manifest.json'
STYLE='data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1"'

GLYPHS={
  0xF14C0:('cave_locations','end-of-road','<path d="M8 57 Q20 43 31 40 Q42 36 63 17 M38 49 L38 27 L57 27 L57 46 M35 28 L47 18 L60 28 M10 52 Q20 57 29 52"/>'),
  0xF14C1:('cave_locations','outside-grate','<path d="M9 26 Q36 12 63 26 L55 57 Q36 66 17 57 Z M21 31 L52 31 L49 51 L24 51 Z M28 30 L27 52 M36 29 L36 53 M44 30 L45 52 M22 38 L51 38 M23 45 L50 45"/>'),
  0xF14C2:('cave_locations','debris-room','<path d="M8 54 Q12 20 36 12 Q60 20 64 54 M13 55 L22 43 L30 55 L39 39 L47 54 L56 45 L63 55 M26 30 L46 30 M30 34 L42 42 M42 34 L31 43"/>'),
  0xF14C3:('cave_locations','bird-chamber','<path d="M8 57 Q12 18 36 12 Q60 18 64 57 M18 50 Q31 43 46 48 M25 39 Q28 26 39 28 Q49 31 44 41 Q38 48 28 43 Z M42 31 L51 34 L43 36 M31 43 L29 51 M37 44 L39 51"/>'),
  0xF14C4:('cave_locations','hall-of-mists','<path d="M8 60 Q10 17 36 10 Q62 17 64 60 M31 13 Q29 29 32 47 Q34 57 26 64 M39 13 Q42 31 39 48 Q37 57 45 64 M14 55 Q25 50 35 56 Q47 62 59 54"/>'),
  0xF14C5:('cave_locations','plover-room','<path d="M8 58 Q12 18 36 12 Q60 18 64 58 M36 25 L49 38 L36 56 L23 38 Z M36 25 L36 56 M23 38 L49 38 M29 31 L43 47 M43 31 L29 47"/>'),
  # Adventure inventory is deliberately its own semantic category. These
  # marks can be reused by later Atlas explorations without importing a
  # Colossal Cave-specific object namespace.
  0xF14D0:('adventure','brass-lamp','<path d="M26 28 Q36 18 46 28 L50 48 Q36 55 22 48 Z M29 25 L31 15 L41 15 L44 25 M22 48 L18 57 L54 57 L50 48 M30 35 Q36 29 42 35"/>'),
  0xF14D1:('adventure','keys','<path d="M17 27 A10 10 0 1 0 37 27 A10 10 0 1 0 17 27 M36 29 L61 54 M48 42 L53 37 M54 48 L59 43"/>'),
  0xF14D2:('adventure','black-rod','<path d="M17 56 Q34 35 54 13 M15 58 L20 54 M51 16 L57 10 M27 45 Q31 49 35 44"/>'),
  0xF14D3:('adventure','little-bird','<path d="M16 43 Q22 25 39 26 Q54 27 56 40 Q52 53 35 53 Q22 52 16 43 Z M42 29 Q49 18 56 24 M54 34 L65 38 L55 42 M28 51 L26 61 M37 52 L39 61 M21 42 Q30 38 38 43"/>'),
  0xF14D4:('adventure','gold-nugget','<path d="M16 49 Q11 36 23 28 Q27 15 41 20 Q55 17 59 31 Q66 42 55 51 Q47 62 33 56 Q21 60 16 49 Z M27 33 Q36 27 47 32 M24 44 Q37 49 53 41"/>'),
  0xF14D5:('adventure','emerald','<path d="M36 9 L58 26 L53 51 L36 64 L18 51 L14 26 Z M14 26 L36 33 L58 26 M36 33 L36 64 M22 18 L36 33 L50 18 M18 51 L36 33 L53 51"/>'),
  0xF14D6:('adventure','silver-chest','<path d="M12 31 Q14 16 36 15 Q58 16 60 31 L60 58 L12 58 Z M12 33 L60 33 M30 31 L42 31 L42 44 L30 44 Z M20 45 L20 57 M52 45 L52 57"/>'),
}

def make_svg(cat,name,cp,body):
  return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="{name}" data-pua="U+{cp:05X}" {STYLE}>
<title>{name.replace('-', ' ')} — naturalist field mark</title><g fill="none" stroke="#302d28" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" data-ink-brush-pass="v2">{body}</g></svg>'''

manifest=json.loads(MANIFEST.read_text())
manifest=[e for e in manifest if not (0xF14C0 <= e['codepoints'][0] <= 0xF14DF)]
# Remove the superseded prototype category so its files cannot drift back into
# a hand-built catalog or laser export.
old=PUA/'cave_objects'
if old.exists():
  for path in old.glob('*.svg'): path.unlink()
  try: old.rmdir()
  except OSError: pass
for cp,(cat,name,body) in GLYPHS.items():
  folder=PUA/cat; folder.mkdir(parents=True,exist_ok=True)
  (folder/f'{name}.svg').write_text(make_svg(cat,name,cp,body))
  manifest.append({'name':f'{cp:X}','source':f'{cat}/{name}.svg','codepoints':[cp],'label':f'{cat}/{name}'})
manifest.sort(key=lambda e:e['codepoints'])
MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
print(f'build_colossal_cave_pua: wrote {len(GLYPHS)} glyphs')
