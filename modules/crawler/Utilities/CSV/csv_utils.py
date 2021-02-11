import inspect
from shared_types import StringSetType
from Utilities.CSV import csv_data_line

# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"


def get_unique_names_from_file(filename: str,
                               column_number: int) -> StringSetType:
    """
        Extract set of unique names from file
    Args:
        filename: path to processed file
        column_number: unique names are expected in csv file on column_number

    Returns:
        set of unique names
    """
    # create set of unique names
    name_set = set()

    with open(filename, "r") as file:
        # go through every line of line
        for x in file:
            # split by csv splitter ;
            array = x.split(";")
            # add string from chosen column to set
            name_set.add(array[column_number])

    return name_set


def export_data_to_csv(filename: str, data_dict) -> None:
    """
        Takes data_dict and export it into a csv file
    Args:
        filename: name of exported file
        data_dict: dictionary containing data from DatasetProcessor
    """
    with open(PROCESSED_DATA_PATH + filename[12:], "w+") as file:

        for date in data_dict:
            if len(date) != 13:
                raise ValueError(
                    "Invalid date format for key value --> YYYY-mm-dd-hh expected!"
                )
            for data in data_dict[date]:
                csv_line = data_dict[date][data]
                if not isinstance(csv_line, csv_data_line.CSVDataLine):
                    raise ValueError(
                        "data_dict is expected to have CSVDataLine as values")
                file.write(csv_line.to_csv() + '\n')