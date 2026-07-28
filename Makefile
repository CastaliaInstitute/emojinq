PYTHON ?= python3

.PHONY: assets fetch-noto all-lines lines font

fetch-noto:
	$(PYTHON) scripts/fetch_noto.py

all-lines: fetch-noto
	$(PYTHON) scripts/build_all.py --source-dir .cache/noto-emoji/svg

assets:
	$(PYTHON) scripts/build_set.py

lines:
	$(PYTHON) scripts/collapse_lines.py

font:
	$(PYTHON) scripts/build_font.py
