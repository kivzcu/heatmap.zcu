import yaml
import os
from typing import Dict, Set
from shared_types import StringSetType
from Utilities.Database import database_record_logs
from Utilities.helpers import should_skip

# Path to dataset configuration files
CONFIG_FILES_PATH = "DatasetConfigs/"
# Config file type
CONFIG_FILE_TYPE = ".yaml"


def load_configuration(dataset_name: str) -> Dict[str, any]:
    """
    Loads yaml configuration file into memory

    Args:
        dataset_name: name of dataset that has existing configuration file

    Returns:
        yaml configuration file as dictionary
    """
    with open(CONFIG_FILES_PATH + dataset_name + CONFIG_FILE_TYPE, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    devices_dic = {}

    if data["devices"] is not None:
        for item in data["devices"]:
            devices_dic.update(item)

    data["devices"] = devices_dic

    return data


def update_configuration(dataset_name: str,
                         new_devices: StringSetType) -> None:
    """
    Open dataset and appends new_devices to the end

    Args:
        dataset_name: name of dataset that has existing configuration file
        new_devices: list or set of new devices for dataset
    """

    with open(CONFIG_FILES_PATH + dataset_name + CONFIG_FILE_TYPE,
              "a") as file:
        for device in new_devices:
            if device == "":
                continue
            file.write("  - " + device + ":\n")
            file.write("      x: UNKNOWN!\n")
            file.write("      y: UNKNOWN!\n")
            file.write("\n")


def check_if_there_is_a_config_file(dataset_name: str) -> bool:
    """
    Goes trough all config files (represeting valid dataset in database)
    and checks if dataset_name is there

    Args:
        dataset_name: name of dataset that has existing configuration file

    Returns:   
        True - if contains
        False - if not
    """
    datasets = os.listdir(CONFIG_FILES_PATH)

    for dataset in datasets:
        name = dataset.split('.')
        if name[0] == dataset_name:
            return True

    return False


def return_dictionary_of_valid_devices(
        devices: Dict[str, any]) -> Dict[str, Dict[str, any]]:
    """
    Iterates over all devices specified in config file

    Extracts only valid one (have both specified coordinates no UNKOWN! OR SKIP)

    Args:
        devices: dictionary of devices contained in config file

    Returns:   
        Dictonary containing only valid devices
    """
    valid_devices = {}

    for device in devices.keys():
        if not should_skip(devices[device]):
            valid_devices[device] = {
                'name': device,
                'x': devices[device]['x'],
                'y': devices[device]['y']
            }

    return valid_devices