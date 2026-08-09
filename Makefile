PYTHON ?= python3

.PHONY: assets cosmos fetch-openmoji all-lines all-gray lines divination naturalist-pua botanical-art body-art animals-art field-studies-art patterns-art materials-art sea-art dinosaurs-art field-plate-detail remove-ground animals-simple weather-simple materials-simple science-simple cross-category-simple art-batch art-batch2 art-batch3 art-batch4 art-batch5 people-art people-rich animate-svg check-animation laser-standard laser-pua laser-calibration check-laser outliers-simple brushify-pua trace-brush font check check-pua check-catalog contact-pua review-pua check-svg check-sumi-e

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

animals-simple:
	$(PYTHON) scripts/redraw_animals_simple.py

weather-simple:
	$(PYTHON) scripts/redraw_weather_simple.py

materials-simple:
	$(PYTHON) scripts/redraw_materials_simple.py

science-simple:
	$(PYTHON) scripts/redraw_science_simple.py

cross-category-simple:
	$(PYTHON) scripts/redraw_cross_category.py

art-batch:
	$(PYTHON) scripts/redraw_art_batch.py

art-batch2:
	$(PYTHON) scripts/redraw_art_batch2.py

art-batch3:
	$(PYTHON) scripts/redraw_art_batch3.py

art-batch4:
	$(PYTHON) scripts/redraw_art_batch4.py

art-batch5:
	$(PYTHON) scripts/redraw_art_batch5.py

people-art:
	$(PYTHON) scripts/redraw_people_art.py

people-rich:
	$(PYTHON) scripts/redraw_people_rich_sources.py

botanical-art:
	$(PYTHON) scripts/redraw_botanical_ink_art.py

body-art:
	$(PYTHON) scripts/redraw_body_naturalist_art.py
	$(PYTHON) scripts/redraw_body_actions_naturalist.py

animals-art:
	$(PYTHON) scripts/redraw_animals_naturalist_art.py

field-studies-art:
	$(PYTHON) scripts/redraw_field_studies.py
	$(PYTHON) scripts/enrich_field_studies.py
	uv run --with svgpathtools python scripts/brushify_field_lines.py

patterns-art:
	$(PYTHON) scripts/redraw_patterns_naturalist_art.py

materials-art:
	$(PYTHON) scripts/redraw_materials_naturalist_art.py

sea-art:
	$(PYTHON) scripts/redraw_sea_naturalist_art.py
	$(PYTHON) scripts/enrich_naturalist_plate_detail.py

dinosaurs-art:
	$(PYTHON) scripts/redraw_dinosaurs_naturalist_art.py
	$(PYTHON) scripts/enrich_naturalist_plate_detail.py

field-plate-detail:
	$(PYTHON) scripts/enrich_naturalist_plate_detail.py

remove-ground:
	$(PYTHON) scripts/remove_pua_ground_strokes.py --root assets/pua

animate-svg:
	$(PYTHON) scripts/prepare_svg_animation.py --root assets/pua

check-animation: animate-svg
	$(PYTHON) scripts/check_svg_animation.py --root assets/pua

laser-standard:
	$(PYTHON) scripts/export_laser_svg.py --source assets/gray-all --output build/laser-standard

laser-pua:
	$(PYTHON) scripts/export_laser_svg.py --source assets/pua --output build/laser-pua

laser-calibration:
	$(PYTHON) scripts/build_laser_calibration.py --output build/laser-calibration.svg

check-laser: laser-standard laser-pua laser-calibration
	$(PYTHON) scripts/check_laser_svg.py --root build/laser-standard
	$(PYTHON) scripts/check_laser_svg.py --root build/laser-pua
	$(PYTHON) scripts/check_laser_svg.py --root build/laser-calibration.svg

outliers-simple:
	$(PYTHON) scripts/redraw_outliers_simple.py

brushify-pua:
	$(PYTHON) scripts/brushify_pua.py

# Authoring filter: raster reference -> grayscale vector brush SVG.
# Usage: make trace-brush TRACE_INPUT=reference.png TRACE_OUTPUT=build/reference.svg
trace-brush:
	@test -n "$(TRACE_INPUT)" -a -n "$(TRACE_OUTPUT)" || (echo "set TRACE_INPUT and TRACE_OUTPUT" && exit 2)
	uv run --with vtracer --with pillow --with svgpathtools python scripts/trace_raster_brush.py "$(TRACE_INPUT)" "$(TRACE_OUTPUT)"

divination:
	$(PYTHON) scripts/build_divination_svg.py

naturalist-pua:
	$(PYTHON) scripts/build_naturalist_pua.py --manifest

cosmos:
	$(PYTHON) scripts/build_cosmos_pua.py --manifest

font: all-gray divination
	$(PYTHON) scripts/fetch_yuji_boku.py
	$(PYTHON) scripts/build_alpha_svg.py
	$(PYTHON) scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --alpha-dir assets/alpha-ink --alpha-manifest assets/alpha-ink/manifest.json --extra-dir assets/divination --extra-manifest assets/divination/manifest.json --extra-dir assets/pua --extra-manifest assets/pua/manifest.json --output fonts/Emojinq-Regular.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(MAKE) check-pua
	$(MAKE) check-sumi-e
	$(MAKE) check-catalog
	uv run --with fonttools python scripts/check_font.py
	$(PYTHON) scripts/check_pua_font_render.py fonts/Emojinq-Regular.ttf

check-catalog:
	$(PYTHON) scripts/check_catalog.py

contact-pua:
	$(PYTHON) scripts/render_pua_contact_sheet.py

review-pua:
	$(MAKE) contact-pua
	$(PYTHON) scripts/audit_pua_artifacts.py --root assets/pua --json build/pua-artifact-audit.json

check-pua:
	$(PYTHON) scripts/check_quality.py --source-dir assets/pua --sample 814
	$(PYTHON) scripts/check_pua_vector.py --root assets/pua
	$(PYTHON) scripts/check_pua_legibility.py --root assets/pua
	$(PYTHON) scripts/check_pua_duplicates.py --root assets/pua
	$(PYTHON) scripts/audit_pua_artifacts.py --root assets/pua
	$(PYTHON) scripts/check_pua_coverage.py

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
	  --unicodes=0023,002A,0030-0039,20E3,FE0E-FE0F,2190-21FF,2300-23FF,25A0-25FF,2600-26FF,2700-27BF,2934-2935,2B00-2BFF,1F000-1F0FF,1F300-1F3FA,1F400-1F5FF,1F600-1F64F,1F680-1F6FF,1F780-1F7FF,1F900-1F9FF,1FA70-1FAFF,F0E00-F0E11,F084A,F1067,F0C16,F0C25,F0403,F0417,F0426,F1117,F1400-F1435,F1440-F145E,F14B0-F14B3 \
	  --layout-features='*' \
	  --name-IDs='*'
