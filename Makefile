PYTHON ?= python3

.PHONY: assets cosmos colossal-cave-pua fetch-openmoji all-lines all-gray lines divination naturalist-pua botanical-art body-art animals-art field-studies-art patterns-art materials-art sea-art dinosaurs-art field-plate-detail remove-ground animals-simple weather-simple materials-simple science-simple cross-category-simple art-batch art-batch2 art-batch3 art-batch4 art-batch5 people-art people-rich animate-svg check-animation laser-standard laser-pua laser-calibration check-laser outliers-simple brushify-pua trace-brush font check check-pua check-catalog contact-pua review-pua check-svg check-sumi-e check-stroke-corpus

fetch-openmoji:
	$(PYTHON) scripts/fetch_openmoji.py

all-lines: fetch-openmoji
	uv run --python 3.12 --with svgpathtools python scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode line
	PYTHONPATH=scripts uv run --python 3.12 --with svgpathtools python scripts/enrich_animal_faces.py --root assets/line-all

all-gray: fetch-openmoji
	uv run --python 3.12 --with svgpathtools python scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode line --output-dir assets/gray-all
	PYTHONPATH=scripts uv run --python 3.12 --with svgpathtools python scripts/enrich_animal_faces.py --root assets/gray-all

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
	$(PYTHON) scripts/redraw_animals_line_anatomy.py
	$(PYTHON) scripts/enrich_animals_stroke_anatomy.py

field-studies-art:
	$(PYTHON) scripts/redraw_field_studies.py
	$(PYTHON) scripts/enrich_field_studies.py
	uv run --with svgpathtools python scripts/brushify_field_lines.py

patterns-art:
	$(PYTHON) scripts/redraw_patterns_naturalist_art.py

materials-art:
	$(PYTHON) scripts/redraw_materials_naturalist_art.py

sea-art:
	uv run --with svgpathtools python scripts/enrich_sea_stroke_anatomy.py

dinosaurs-art:
	uv run --with svgpathtools python scripts/redraw_dinosaurs_stroke_only.py

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
	uv run --python 3.12 --with vtracer --with pillow --with svgpathtools python scripts/trace_raster_brush.py "$(TRACE_INPUT)" "$(TRACE_OUTPUT)"

divination:
	$(PYTHON) scripts/build_divination_svg.py

naturalist-pua:
	$(PYTHON) scripts/build_naturalist_pua.py --manifest

colossal-cave-pua:
	$(PYTHON) scripts/build_colossal_cave_pua.py

cosmos:
	$(PYTHON) scripts/build_cosmos_pua.py --manifest

font: all-gray divination
	$(PYTHON) scripts/fetch_yuji_boku.py
	uv run --with scikit-image --with pillow --with svgpathtools python scripts/build_alpha_svg.py
	uv run --python 3.12 --with fonttools --with svgpathtools python scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --alpha-dir assets/alpha-ink --alpha-manifest assets/alpha-ink/manifest.json --extra-dir assets/divination --extra-manifest assets/divination/manifest.json --extra-dir assets/pua --extra-manifest assets/pua/manifest.json --output fonts/Emojinq-Regular.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(MAKE) check-pua
	$(MAKE) check-sumi-e
	$(MAKE) check-stroke-corpus
	$(MAKE) check-catalog
	uv run --with fonttools python scripts/check_font.py
	uv run --with pillow --with fonttools python scripts/check_alpha_font.py fonts/Emojinq-Regular.ttf
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

check-stroke-corpus:
	$(PYTHON) scripts/check_stroke_corpus.py --root assets

# Emoji-only subset for app bundles (e.g. CastaliaInstitute/atlas).
# Keeps every standard single-codepoint emoji block for headroom; drops the
# Yuji alphabet, flag pairs (regional indicators), skin-tone modifiers, and
# ZWJ sequences — the bulk of the full font that a launcher map never draws.
atlas-subset:
	pyftsubset fonts/Emojinq-Regular.ttf \
	  --output-file=fonts/Emojinq-Atlas.ttf \
	  --unicodes=0023,002A,0030-0039,20E3,FE0E-FE0F,2190-21FF,2300-23FF,25A0-25FF,2600-26FF,2700-27BF,2934-2935,2B00-2BFF,1F000-1F0FF,1F300-1F3FA,1F400-1F5FF,1F600-1F64F,1F680-1F6FF,1F780-1F7FF,1F900-1F9FF,1FA70-1FAFF,F0E00-F0E11,F084A,F1067,F0C16,F0C25,F0403,F0417,F041E,F0420,F0426,F043E,F10A2,F110C,F1117,F1400-F1435,F1440-F145E,F14B0-F14B3,F14C0-F14DF \
	  --layout-features='*' \
	  --name-IDs='*'
