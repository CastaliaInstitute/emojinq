PYTHON ?= python3

.PHONY: assets font

assets:
	$(PYTHON) scripts/build_set.py

font:
	$(PYTHON) scripts/build_font.py
