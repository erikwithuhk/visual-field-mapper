all: get-all-normal-averages get-study-averages

get-normal-averages:
	python -m visual_field_mapper average-by-sector

get-all-normal-averages: get-normal-averages
	python -m visual_field_mapper all-averages

get-study-averages:
	python -m visual_field_mapper average-by-sector
