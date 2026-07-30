PYTHON ?= python3

.PHONY: assets fetch-openmoji all-lines all-gray lines font check

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
	$(PYTHON) scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --output fonts/Emojinq-Regular.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(PYTHON) scripts/check_font.py
