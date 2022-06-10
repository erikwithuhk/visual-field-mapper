get-normal-averages:
	python -m visual_field_mapper average-by-sector data/normal.csv out/normal_averages.csv

get-all-normal-averages:
	python -m visual_field_mapper all-averages out/normal_averages.csv out/normal_averages_all.csv

get-study-averages:
	python -m visual_field_mapper average-by-sector data/study.csv out/study_averages.csv
