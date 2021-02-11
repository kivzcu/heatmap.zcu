import os
import zipfile
from shared_types import ConfigType, StringSetType
from Utilities.CSV import csv_utils
from Utilities.Database import database_record_logs


def list_of_all_new_files(ignore_set: StringSetType,
                          path: str) -> StringSetType:
    """
    Get all files from directory and all files written in ignore.txt
    and return the difference
    Args:
        path: path to Directory
        ignore_set: path to Directory
    Returns:
        list with names of all files in directory
    """
    files_in_dir = os.listdir(path)

    return set(files_in_dir).difference(ignore_set)


def get_devices_set(dataset_name: str, path: str) -> StringSetType:
    """
     Goes trough every not loaded file(not contained in ProcessedData/ignore.txt)
     Extracts names from not loaded file which should be in first column
     Creates set of unique devices_names

    Args:
        path: Path to Processed directory

    Returns:
        set of unique names contained in not loaded files
    """
    ignore_set = database_record_logs.load_ignore_set_loaded(dataset_name)
    files_in_dir = list_of_all_new_files(ignore_set, path)

    unique_names = set()

    for file_path in files_in_dir:
        unique_names.update(
            csv_utils.get_unique_names_from_file(path + file_path, 0))

    return unique_names


def get_unknown_devices_set(config: ConfigType,
                            devices: StringSetType) -> StringSetType:
    """
    Compares config and devices a return difference

    Args:
        config:  loaded configuration file of dataset
        devices: set of unique devices contained in dataset

    Returns:
        diffrences between two sets (unkown devices)
    """
    devices_set = set(config["devices"].keys())
    unknown_devices_set = devices.difference(devices_set)

    return unknown_devices_set


def unzip_all_csv_zip_files_in_folder(path: str) -> None:
    """
    Load all files from directory and unzip those which end by .zip
    After unziping deletes the zip file
    Args:
        path: Path to CrawledData directory containing ignore.txt file
    """
    files_in_dir = os.listdir(path)
    zips = []

    for file in files_in_dir:
        if file.endswith(".zip"):
            zips.append(path + file)

    for zip_file in zips:

        with zipfile.ZipFile(zip_file, "r") as unziped_file:
            unziped_file.extractall(path)

        os.remove(zip_file)


def clean_folder(path: str) -> None:
    """
    Deletes all files in folder

    Args:
        path: path to folder
    """
    files = os.listdir(path)

    for file in files:
        os.remove(path + file)
