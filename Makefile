draw: get-all-normal-averages get-study-averages get-archetype-fills
	python -m visual_field_mapper draw

get-normal-averages:
	python -m visual_field_mapper average-by-sector data/normal.csv out/normal_mean_td_by_sector.csv

get-all-normal-averages: get-normal-averages
	python -m visual_field_mapper all-averages

get-study-averages:
	python -m visual_field_mapper average-by-sector data/study.csv out/study_mean_td_by_sector.csv

get-archetype-fills:
	python -m visual_field_mapper get-archetype-fills

.PHONY: clean
clean:
	rm -rf out/*
