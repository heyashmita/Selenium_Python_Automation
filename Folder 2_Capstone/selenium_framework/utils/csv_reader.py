
import csv
import os

from utils.config_reader import ConfigReader, PROJECT_ROOT


class CSVReader:

    @staticmethod
    def read(file_name):
        data_dir = os.path.join(PROJECT_ROOT, ConfigReader.get_path("test_data_dir"))
        file_path = os.path.join(data_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    @staticmethod
    def read_as_tuples(file_name):
        rows = CSVReader.read(file_name)
        return [tuple(row.values()) for row in rows]
