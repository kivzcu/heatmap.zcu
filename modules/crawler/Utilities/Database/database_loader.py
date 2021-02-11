from Utilities.Database import database_data_line, database_record_logs
from Utilities import configure_functions
from Utilities.helpers import should_skip, detect_change
from shared_types import ConfigType
from typing import Dict
import pymongo
import re

#
# TODO: set MongoDB credentials
#

# specify mongodb connection
MONGODB_CONNECTION = "mongodb://root:root@database"
# mongodb account name
MONGODB_ACC_NAME = "root"
# mongodb account password
MONGODB_ACC_PASSWORD = "root"
# mongodb data database
MONGODB_DATA_DATABASE = "open-data-db"
# mongodb collection with aviable datasets
MONGODB_DATASET_COLLECTION = "DATASETS"
# mongodb collection with aviable diveces of datasets
MONGODB_DATASET_DEVICES_COLLECTION = "DEVICES"

# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"

DatabaseConnectionType = Dict[str, any]


def create_database_connection() -> pymongo.database.Database:
    """
    Creates connection to mongoDB

    Returns:
        Connection to mongoDB
    """
    client = pymongo.MongoClient(MONGODB_CONNECTION)

    # Authenticating
    client.admin.authenticate(MONGODB_ACC_NAME, MONGODB_ACC_PASSWORD)

    database = client[MONGODB_DATA_DATABASE]

    return database


def get_data_from_file(filename: str, config: ConfigType) -> Dict[str, any]:
    """
        Opens processed file, reads it line by line
        name, ocurrence, date
        searches name in config and adds device map coordinates
        than creates a dictionary with date without hours as key
        and list of data lines as value.
    Args:
        filename: name of processed file
        config: loaded configuration file of dataset

    Returns:
        dictionary with date without hours as key
        and list of Datalines as value
    """
    dataset_name = config["dataset-name"]
    dataset_path = PROCESSED_DATA_PATH + dataset_name + '/'

    f = open(dataset_path + filename, "r")

    devices = config["devices"]
    date_dict = {}

    for line in f:
        line = line[:-1]

        csv_column = line.split(";")

        name = csv_column[0]

        if should_skip(devices[name]):
            continue

        occurrence = csv_column[1]
        date = csv_column[2]
        data_line = database_data_line.DatabaseDataLine(
            name, devices[name]["x"], devices[name]["y"], date, occurrence)

        # if you want to change table split by hours or months change this YYYY-mm-hh-dd
        date_without_hours = date[:-3]
        if date_without_hours not in date_dict:
            date_dict[date_without_hours] = list()

        date_dict[date_without_hours].append(data_line.to_dictionary())

    return date_dict


def load_data_to_database(database_connection: DatabaseConnectionType,
                          dataset_name: str, data_dic: Dict[str, any],
                          file_name: str) -> None:
    """
    Takes data_dic created in method get_data_from_file
    and loads into into database where collection name is dataset_name + data_dic key
    and data lines are line in collection

    Args:
        database_connection: created connection to a MONGODB
        config: loaded configuration file of dataset
        data_dic: dictionary of data lines created in get_data_from_file
        file_name: name of file containing data
    """

    for date in data_dic:
        dataset_collections = database_connection[dataset_name]
        dataset_collections.insert_one({'date': date})
        date_dataset = database_connection[dataset_name + date]
        date_dataset.insert_many(data_dic[date])


def check_or_update_datasets_collection(
        database_connection: DatabaseConnectionType, config: ConfigType):
    """
    Checks if DATASETS collection contains dataset and if display name was not updated

    Args:
        database_connection: created connection to a MONGODB
        config: loaded configuration file of dataset
    """
    # collection where are specified aviable datasets
    compareKeys = ['display-name', 'display-color']
    collection_datasets = database_connection[MONGODB_DATASET_COLLECTION]

    query = {'key-name': config['dataset-name']}

    # check if newly added data already have a dataset specified in collection
    current_dataset = collection_datasets.find_one(query)

    if current_dataset is None:
        collection_datasets.insert_one({
            'key-name': config['dataset-name'],
            'display-name': config['display-name'],
            'display-color': config['display-color'],
            'updated': 0
        })
    elif detect_change(current_dataset, config, compareKeys):
        newVal = {}
        for key in compareKeys:
            newVal[key] = config[key]
        collection_datasets.update_one(query, {"$set": newVal})


def update_devices_collection(config: ConfigType):
    """
    Checks if there are any changes in devices specified in config file against 
    devices processed and loaded into the database

    If there are new devices replaces old device in databse by new ones

    Args:
        config: loaded configuration file of dataset

    Returns:
        True - when changes are found and devices replaced
        False - when there were no changes
    """
    database_connection = create_database_connection()
    dataset_name = config['dataset-name']
    devices = config['devices']

    change_in_devices = False

    collection_devices = database_connection[
        dataset_name + MONGODB_DATASET_DEVICES_COLLECTION]

    devices_cursor = collection_devices.find()

    db_device_dict = {}

    for device in devices_cursor:
        name = device['name']
        db_device_dict[name] = {
            'name': name,
            'x': device['x'],
            'y': device['y']
        }

    valid_devices = configure_functions.return_dictionary_of_valid_devices(
        devices)

    if len(valid_devices.keys()) != len(db_device_dict.keys()):
        change_in_devices = True

    if change_in_devices == False:
        for device in valid_devices.keys():
            if device in db_device_dict:
                config_x = valid_devices[device]['x']
                config_y = valid_devices[device]['y']
                db_x = db_device_dict[device]['x']
                db_y = db_device_dict[device]['y']
                if config_x != db_x or config_y != db_y:
                    change_in_devices = True
                    break

    if change_in_devices == True:
        collection_devices.delete_many({})
        devices_list = list()

        for device in devices.keys():
            if not (should_skip(devices[device])):
                devices_list.append({
                    'name': device,
                    'x': devices[device]['x'],
                    'y': devices[device]['y']
                })

        collection_devices.insert_many(devices_list)

    return change_in_devices


def remove_dataset_database(dataset_name: str):
    """
    Removes dataset entries from database
    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    # Creating connection
    mydb = create_database_connection()

    # collection where are specified aviable datasets
    collection_datasets = mydb[MONGODB_DATASET_COLLECTION]

    collection_datasets.delete_one({"key-name": dataset_name})
    print("Odstraňování záznamu z DATASETS kolekce")

    # Retrieve list of all collections
    collections = mydb.list_collection_names()

    # Drop of all collections
    for name in collections:
        if name.startswith(dataset_name):
            mydb[name].drop()
            print("Odstraňuji: " + name)


def reset_dataset_database(dataset_name: str):
    """
    Reset dataset in database 
     - delete everything from except crawled links and mention in DATASETS collection
    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    # Creating connection
    mydb = create_database_connection()

    pattern = re.compile(dataset_name + '[0-9]+-[0-9]+-+[0-9]+')

    # Retrieve list of all collections
    collections = mydb.list_collection_names()

    # Drop of all collections
    for name in collections:
        if pattern.match(name):
            mydb[name].drop()
            print("Odstraňuji: " + name)

    database_record_logs.reset_ignore_set_loaded(dataset_name)
