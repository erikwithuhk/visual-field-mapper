import csv
from typing import Any, List


class FileReader:
    def read_csv(self, filepath: str):
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                yield dict(row)

    def write_csv(self, filepath: str, rows: List[Any]):
        with open(filepath, "w", encoding="UTF8") as file:
            writer = csv.DictWriter(file)
            writer.writeheader()
            writer.writerows(rows)
