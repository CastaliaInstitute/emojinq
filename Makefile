PYTHON ?= python3

.PHONY: assets fetch-openmoji all-lines all-gray lines font check check-svg

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

font: all-gray
	$(PYTHON) scripts/fetch_yuji_boku.py
	$(PYTHON) scripts/build_alpha_svg.py
	$(PYTHON) scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --alpha-dir assets/alpha-ink --alpha-manifest assets/alpha-ink/manifest.json --output fonts/Emojinq-Regular.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(PYTHON) scripts/check_font.py

check-svg:
	$(PYTHON) scripts/check_svg_set.py --source-dir assets/gray-all
