import csv


class FileReader:
    def read_csv(self, filepath: str):
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                yield dict(row)
