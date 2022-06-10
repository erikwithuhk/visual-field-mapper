get-normal-averages:
	python -m visual_field_mapper average-by-sector data/normal.csv out/normal_averages.csv

get-study-averages:
	python -m visual_field_mapper average-by-sector data/study.csv out/study_averages.csv
