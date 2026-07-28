PYTHON ?= python3

.PHONY: font

font:
	$(PYTHON) scripts/build_font.py
