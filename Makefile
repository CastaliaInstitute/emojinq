PYTHON ?= python3

.PHONY: assets lines font

assets:
	$(PYTHON) scripts/build_set.py

lines:
	$(PYTHON) scripts/collapse_lines.py

font:
	$(PYTHON) scripts/build_font.py
