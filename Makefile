RUN ?= uv run --python 3.12 --with-requirements requirements-build.txt
PYTHON ?= $(RUN) python

.PHONY: assets ontology cosmos colossal-cave-pua castalia-pua faerie-pua fetch-openmoji all-lines all-gray lines divination naturalist-pua botanical-art body-art animals-art toddler-art field-studies-art patterns-art materials-art sea-art dinosaurs-art field-plate-detail remove-ground animals-simple weather-simple materials-simple science-simple cross-category-simple art-batch art-batch2 art-batch3 art-batch4 art-batch5 people-art people-rich animate-svg check-animation laser-standard laser-pua laser-calibration check-laser outliers-simple brushify-pua trace-brush font color-font site check release-check recognition-ledger check-recognition-release check-release-inputs check-color-font check-pua check-pua-color check-standard-toddler check-catalog check-developmental contact-pua review-pua check-svg check-sumi-e check-sumi-e-benchmarks check-stroke-corpus

fetch-openmoji:
	$(PYTHON) scripts/fetch_openmoji.py

all-lines: fetch-openmoji
	$(RUN) python scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode line
	PYTHONPATH=scripts $(RUN) python scripts/enrich_animal_faces.py --root assets/line-all

all-gray: fetch-openmoji
	$(RUN) python scripts/build_all.py --source-dir .cache/openmoji/black/svg --mode line --output-dir assets/gray-all
	PYTHONPATH=scripts $(RUN) python scripts/enrich_animal_faces.py --root assets/gray-all

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

# Reapply the reviewed concrete-noun silhouettes after generated source assets.
# Recognizability is a hard gate; extra defining strokes are intentional.
toddler-art:
	$(RUN) python scripts/redraw_moon_phases_sumi.py
	$(PYTHON) scripts/strengthen_food_toddler_recognition.py
	$(RUN) python scripts/strengthen_standard_animals_nature.py
	$(PYTHON) scripts/strengthen_standard_travel_places.py
	$(PYTHON) scripts/strengthen_standard_activities.py
	$(PYTHON) scripts/strengthen_standard_flags.py
	$(PYTHON) scripts/strengthen_standard_people_objects.py
	$(PYTHON) scripts/strengthen_standard_remaining.py
	$(RUN) python scripts/redraw_botanical_ink_art.py
	$(RUN) python scripts/redraw_animals_line_anatomy.py
	$(RUN) python scripts/redraw_farm_anatomy.py
	$(RUN) python scripts/redraw_objects_line_anatomy.py
	$(PYTHON) scripts/redraw_object_recognition_outliers.py
	$(RUN) python scripts/redraw_sea_creatures_line_anatomy.py
	$(PYTHON) scripts/redraw_sea_outliers.py
	$(PYTHON) scripts/redraw_pua_toddler_semantic_outliers.py
	$(PYTHON) scripts/strengthen_pua_toddler_referents.py

field-studies-art:
	$(PYTHON) scripts/redraw_field_studies.py
	$(PYTHON) scripts/enrich_field_studies.py
	$(RUN) python scripts/brushify_field_lines.py

patterns-art:
	$(PYTHON) scripts/redraw_patterns_naturalist_art.py

materials-art:
	$(PYTHON) scripts/redraw_materials_naturalist_art.py

sea-art:
	$(RUN) python scripts/enrich_sea_stroke_anatomy.py

dinosaurs-art:
	$(RUN) python scripts/redraw_dinosaurs_stroke_only.py

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
	$(RUN) --with vtracer python scripts/trace_raster_brush.py "$(TRACE_INPUT)" "$(TRACE_OUTPUT)"

divination:
	$(RUN) python scripts/build_divination_svg.py

naturalist-pua:
	$(PYTHON) scripts/build_naturalist_pua.py --manifest

ontology:
	$(PYTHON) scripts/build_ontology.py

colossal-cave-pua:
	$(PYTHON) scripts/build_colossal_cave_pua.py

castalia-pua:
	$(PYTHON) scripts/build_castalia_pua.py

faerie-pua:
	$(PYTHON) scripts/build_faerie_pua.py

cosmos:
	$(PYTHON) scripts/build_cosmos_pua.py --manifest

font: all-gray divination
	$(RUN) python scripts/build_alpha_svg.py
	$(RUN) python scripts/rank_developmental_vocabulary.py
	$(MAKE) toddler-art
	$(RUN) python scripts/rank_developmental_vocabulary.py
	$(RUN) python scripts/build_font.py --source-dir assets/gray-all --manifest assets/gray-all/manifest.json --alpha-dir assets/alpha-ink --alpha-manifest assets/alpha-ink/manifest.json --extra-dir assets/divination --extra-manifest assets/divination/manifest.json --extra-dir assets/pua --extra-manifest assets/pua/manifest.json --output fonts/Emojinq-Regular.ttf

color-font: font
	$(PYTHON) scripts/build_color_assets.py
	$(PYTHON) scripts/build_pua_color_variants.py
	$(RUN) python scripts/build_color_font.py
	$(MAKE) check-color-font

site:
	$(PYTHON) scripts/assemble_site.py

check-color-font:
	$(RUN) python scripts/check_color_font.py fonts/Emojinq-Color.ttf

check:
	$(PYTHON) scripts/check_quality.py
	$(PYTHON) scripts/check_ontology.py
	$(MAKE) check-pua
	$(MAKE) check-pua-color
	$(MAKE) check-sumi-e
	$(MAKE) check-sumi-e-benchmarks
	$(MAKE) check-standard-toddler
	$(MAKE) check-stroke-corpus
	$(MAKE) check-catalog
	$(MAKE) check-developmental
	$(MAKE) check-release-inputs
	$(RUN) python scripts/check_font.py
	$(RUN) python scripts/check_alpha_font.py fonts/Emojinq-Regular.ttf
	$(PYTHON) scripts/check_pua_font_render.py fonts/Emojinq-Regular.ttf
	@if [ -f fonts/Emojinq-Color.ttf ]; then $(MAKE) check-color-font; fi

check-catalog:
	$(PYTHON) scripts/check_catalog.py

check-developmental:
	$(PYTHON) scripts/check_developmental_metadata.py

recognition-ledger:
	$(PYTHON) scripts/build_pua_recognition_review.py

check-recognition-release:
	$(PYTHON) scripts/check_pua_recognition_evidence.py

check-release-inputs:
	$(PYTHON) scripts/check_release_inputs.py

release-check: check check-recognition-release

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
	$(PYTHON) scripts/check_pua_toddler_referents.py

check-pua-color:
	$(PYTHON) scripts/check_pua_color_variants.py

check-svg:
	$(PYTHON) scripts/check_svg_set.py --source-dir assets/gray-all

check-sumi-e:
	$(PYTHON) scripts/check_sumi_e_style.py --root assets

check-sumi-e-benchmarks:
	$(PYTHON) scripts/check_sumi_e_benchmarks.py

check-standard-toddler:
	$(PYTHON) scripts/check_standard_toddler_categories.py

check-stroke-corpus:
	$(PYTHON) scripts/check_stroke_corpus.py --root assets

# Emoji-only subset for app bundles (e.g. CastaliaInstitute/atlas).
# Keeps every standard single-codepoint emoji block for headroom; drops the
# Yuji alphabet, flag pairs (regional indicators), skin-tone modifiers, and
# ZWJ sequences — the bulk of the full font that a launcher map never draws.
atlas-subset:
	pyftsubset fonts/Emojinq-Regular.ttf \
	  --output-file=fonts/Emojinq-Atlas.ttf \
	  --unicodes=0020-007E,20E3,FE0E-FE0F,2190-21FF,2300-23FF,25A0-25FF,2600-26FF,2700-27BF,2934-2935,2B00-2BFF,1F000-1F0FF,1F300-1F3FA,1F400-1F5FF,1F600-1F64F,1F680-1F6FF,1F780-1F7FF,1F900-1F9FF,1FA70-1FAFF,F0E00-F0E11,F082D,F084A,F1067,F0C04,F0C07,F0C16,F0C25,F0C29-F0C2A,F0C4C,F0C6F,F0C77,F0C7C,F0403,F0417,F041E,F0420,F0426,F043E,F10A2,F110C,F1117,F1400-F1435,F1440-F145E,F1460-F1469,F14B0-F14B3,F14C0-F14DF,F1500-F1514,F1520-F152A,F15FF \
	  --layout-features='*' \
	  --name-IDs='*'
