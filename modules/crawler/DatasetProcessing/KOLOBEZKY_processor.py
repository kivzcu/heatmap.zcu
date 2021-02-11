from Utilities.CSV import csv_data_line
from Utilities import date_formating

from shared_types import DateDict


def process_file(filename: str) -> DateDict:
    """
    Method that take path to crawled file and outputs date dictionary:
    Date dictionary is a dictionary where keys are dates in format YYYY-mm-dd-hh (2018-04-08-15)
    and value is dictionary where keys are devices (specified in configuration file)
    and value is CSVDataLine.csv_data_line with device,date and occurrence

    Args:
    filename: name of processed file

    Returns:
    None if not implemented
    date_dict when implemented
    """
    date_dict = {}

    with open(filename, "r") as file:

        for line in file:

            array = line.split(";")

            date = date_formating.date_time_formatter(array[0][1:-1])
            name = array[1][1:-1]

            if date not in date_dict:
                date_dict[date] = {}

            if name in date_dict[date]:
                date_dict[date][name].occurrence += 1
            else:
                date_dict[date][name] = csv_data_line.CSVDataLine(
                    name, date, 1)

    return date_dict
