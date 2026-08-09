PYTHON ?= python3

.PHONY: assets fetch-openmoji all-lines all-gray lines divination font check check-svg check-sumi-e

fetch-openmoji:
	$(PYTHON) scripts/fetch_openmoji.py

all-lines: fetch-openmoji
	$(PYTHON) scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode line

all-gray: fetch-openmoji
	$(PYTHON) scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode grayscale

assets:
	$(PYTHON) scripts/build_set.py

lines:
	$(PYTHON) scripts/collapse_lines.py

divination:
	$(PYTHON) scripts/build_divination_svg.py

font: all-gray divination
	$(PYTHON) scripts/fetch_yuji_boku.py
	$(PYTHON) scripts/build_alpha_svg.py
	$(PYTHON) scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --alpha-dir assets/alpha-ink --alpha-manifest assets/alpha-ink/manifest.json --extra-dir assets/divination --extra-manifest assets/divination/manifest.json --extra-dir assets/pua --extra-manifest assets/pua/manifest.json --output fonts/Emojinq-Regular.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(PYTHON) scripts/check_font.py

check-svg:
	$(PYTHON) scripts/check_svg_set.py --source-dir assets/gray-all

check-sumi-e:
	$(PYTHON) scripts/check_sumi_e_style.py --root assets

# Emoji-only subset for app bundles (e.g. CastaliaInstitute/atlas).
# Keeps every standard single-codepoint emoji block for headroom; drops the
# Yuji alphabet, flag pairs (regional indicators), skin-tone modifiers, and
# ZWJ sequences — the bulk of the full font that a launcher map never draws.
atlas-subset:
	pyftsubset fonts/Emojinq-Regular.ttf \
	  --output-file=fonts/Emojinq-Atlas.ttf \
	  --unicodes=0023,002A,0030-0039,20E3,FE0E-FE0F,2190-21FF,2300-23FF,25A0-25FF,2600-26FF,2700-27BF,2934-2935,2B00-2BFF,1F000-1F0FF,1F300-1F3FA,1F400-1F5FF,1F600-1F64F,1F680-1F6FF,1F780-1F7FF,1F900-1F9FF,1FA70-1FAFF,F0E00-F0E11,F084A,F1067,F0C16,F0C25,F0403,F0417,F0426,F1117,F1400-F141E \
	  --layout-features='*' \
	  --name-IDs='*'
