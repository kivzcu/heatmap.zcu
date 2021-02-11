from Utilities import folder_processor, configure_functions
from Utilities.Database import database_loader, database_record_logs
from Utilities.CSV import csv_utils
from shared_types import ConfigType
import os
import pymongo

import logging
from datetime import date

# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"
# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"
# Path to crawler logs
CRAWLER_LOGS_PATH = "CrawlerLogs/"
# Path to dataset crawler implementations
CRAWLER_LIB_PATH = "DatasetCrawler."
# Path to dataset processor implementations
PROCESSOR_LIB_PATH = "DatasetProcessing."

#logger
logging.basicConfig(filename=CRAWLER_LOGS_PATH + 'Applicationlog-' +
                    date.today().strftime("%b-%Y") + '.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


def check_last_update(config: ConfigType) -> bool:
    """
    Loads integer from updated.txt in CrawlerLogs/"dataset_name"
    representing number of days from last update if number equals
    number in confing update period updates it and reset number of
    days to zero else increment the number

    Arguments:
        config loaded configuration file of dataset

    Returns:
       True if updating
       Else if incementing days from last update
    """
    dataset_name = config["dataset-name"]

    last_update = database_record_logs.load_updated(dataset_name)

    if config["update-period"] <= last_update:
        logging.info("Dataset " + dataset_name + " is being updated today")
        database_record_logs.update_updated(dataset_name, 0)
        return True
    else:
        last_update_days = last_update + 1
        logging.info("Dataset " + dataset_name + " will be updated in " +
                     str(int(config["update-period"]) - last_update_days) +
                     "days")
        database_record_logs.update_updated(dataset_name, last_update + 1)
        return False


def crawl_data(config: ConfigType) -> None:
    """
      Imports dataset crawler in DatasetCrawler/"dataset_name"_crawler.py
      runs crawler.

    Args:
        config: loaded configuration file of dataset
    """
    dataset_name = config["dataset-name"]

    crawl_func = __import__(CRAWLER_LIB_PATH + dataset_name + "_crawler",
                            globals(), locals(), ['crawl']).crawl
    crawl_func(config)

    dataset_name += '/'


def process_data(config: ConfigType) -> None:
    """
    Goes trough every not processed file(list of processed files is saved in databse)
    Imports dataset processor in DatasetProcessing/"dataset_name"_processor.py
    Runs processor on every file
    After successful processing updates database list of processed files

    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    dataset_name = config["dataset-name"]
    dataset_path = dataset_name + '/'

    process_file_func = __import__(
        PROCESSOR_LIB_PATH + dataset_name + "_processor", globals(), locals(),
        ['process_file']).process_file

    ignore_set = database_record_logs.load_ignore_set_processed(dataset_name)
    not_processed_files = folder_processor.list_of_all_new_files(
        ignore_set, CRAWLED_DATA_PATH + dataset_path)
    logging.info(dataset_name + " found " + str(len(not_processed_files)) +
                 " not processed files")

    for not_processed_file in not_processed_files:
        path = CRAWLED_DATA_PATH + dataset_path + not_processed_file
        date_dic = process_file_func(path)
        csv_utils.export_data_to_csv(path, date_dic)
        print("Vytvářím: " + not_processed_file)
        database_record_logs.update_ignore_set_processed(
            dataset_name, not_processed_file)

    logging.info(dataset_name + " has processed " +
                 str(len(not_processed_files)) + " newly crawled files")


def process_data_crone(config: ConfigType) -> None:
    """
    Goes trough every not processed file(list of processed files is saved in database)
    Imports dataset processor in DatasetProcessing/"dataset_name"_processor.py
    Runs processor on every file
    After successful processing updates database list of processed files

    Lightweight version for crone and production only
    - excludes checks for changes of config file and coordinates and names
    after these changes force_update_datasets.py should be called

    Args:
        dataset_name: name of dataset that has existing configuration file
    """

    dataset_name = config["dataset-name"]
    dataset_path = dataset_name + '/'

    process_file_func = __import__(
        PROCESSOR_LIB_PATH + dataset_name + "_processor", globals(), locals(),
        ['process_file']).process_file

    ignore_set = database_record_logs.load_ignore_set_processed(dataset_name)
    not_processed_files = folder_processor.list_of_all_new_files(
        ignore_set, CRAWLED_DATA_PATH + dataset_path)
    logging.info(dataset_name + " found " + str(len(not_processed_files)) +
                 " not processed files")

    for not_processed_file in not_processed_files:
        path = CRAWLED_DATA_PATH + dataset_path + not_processed_file
        date_dic = process_file_func(path)
        csv_utils.export_data_to_csv(path, date_dic)
        database_record_logs.update_ignore_set_processed(
            dataset_name, not_processed_file)

    logging.info(dataset_name + " has processed " +
                 str(len(not_processed_files)) + " newly crawled files")


def validate_process_data(config: ConfigType) -> bool:
    """
    Function goes through newly processed data and checks theirs status

    Args:
        config: loaded configuration file of dataset

    Returns:
        boolean variable TRUE/FALSE.
        Data processed correctly - TRUE
        Wrong format or NEW unknown devices - FALSE
    """
    dataset_name = config["dataset-name"]

    processed_devices_set = folder_processor.get_devices_set(
        dataset_name, PROCESSED_DATA_PATH + dataset_name + '/')
    unknown_devices_set = folder_processor.get_unknown_devices_set(
        config, processed_devices_set)
    unknown_devices_size = len(unknown_devices_set)

    if unknown_devices_size != 0:
        logging.info("There is " + str(unknown_devices_size) +
                     " unknown devices")
        logging.info("Adding devices to " + dataset_name + " config file")
        configure_functions.update_configuration(dataset_name,
                                                 unknown_devices_set)
        return False

    for device in config["devices"]:
        device = config["devices"][device]
        if device["x"] == "UNKNOWN!" or device["y"] == "UNKNOWN!":
            logging.info(
                dataset_name +
                " config file contains devices with UNKOWN! values please update them!!"
            )
            #return False

    return True


def load_data_to_database(config: ConfigType) -> None:
    """
    Goes trough every not loaded file(list of loaded files is saved in database)
    loads data appends coordination from configurations
    and exports it into the database
    After successful processing updates database list of loaded files

    Args:
        config: loaded configuration file of dataset
    """
    dataset_name = config["dataset-name"]
    dataset_path = dataset_name + '/'

    database_connection = database_loader.create_database_connection()

    database_loader.check_or_update_datasets_collection(
        database_connection, config)

    changes_in_devices = database_loader.update_devices_collection(config)

    if changes_in_devices == True:
        logg_string = dataset_name + " contains changes in devices configuration. Deleting old data and preparing new"
        logg_string_cs = dataset_name + " obsahuje změny v konfiguračním souboru. Probíha odstraňování starých dat a připravení nových."
        logging.info(logg_string)
        print(logg_string_cs)
        database_loader.reset_dataset_database(dataset_name)

    # get all unprocessed files from dataset
    ignore_set = database_record_logs.load_ignore_set_loaded(dataset_name)
    not_loaded_files = folder_processor.list_of_all_new_files(
        ignore_set, PROCESSED_DATA_PATH + dataset_path)

    # load every file
    for not_loaded_file in not_loaded_files:
        # load processed data
        processed_data = database_loader.get_data_from_file(
            not_loaded_file, config)
        # load processed data to database
        database_loader.load_data_to_database(database_connection,
                                              dataset_name, processed_data,
                                              not_loaded_file)
        database_record_logs.update_ignore_set_loaded(dataset_name,
                                                      not_loaded_file)

    logg_string = dataset_name + " has loaded to database " + str(
        len(not_loaded_files)) + " newly processed files."
    logg_string_cs = dataset_name + " načetl " + str(
        len(not_loaded_files)) + " nových zpracovaných souborů \n"

    logging.info(logg_string)
    print(logg_string_cs)

    client = pymongo.MongoClient()
    client.close()


def load_data_to_database_crone(config: ConfigType) -> None:
    """
    Goes trough every not loaded file(list of loaded files is saved in database)
    loads data appends coordination from configurations
    and exports it into the database
    After successful processing updates database list of loaded files
    
    Lightweight version for crone and production only
    - excludes checks for changes of config file and coordinates and names
    after these changes force_update_datasets.py should be called

    Args:
        config: loaded configuration file of dataset
    """
    dataset_name = config["dataset-name"]
    dataset_path = dataset_name + '/'

    database_connection = database_loader.create_database_connection()

    # get all unprocessed files from dataset
    ignore_set = database_record_logs.load_ignore_set_loaded(dataset_name)
    not_loaded_files = folder_processor.list_of_all_new_files(
        ignore_set, PROCESSED_DATA_PATH + dataset_path)

    # load every file
    for not_loaded_file in not_loaded_files:
        # load processed data
        processed_data = database_loader.get_data_from_file(
            not_loaded_file, config)
        # load processed data to database
        database_loader.load_data_to_database(database_connection,
                                              dataset_name, processed_data,
                                              not_loaded_file)
        database_record_logs.update_ignore_set_loaded(dataset_name,
                                                      not_loaded_file)

    logging.info(dataset_name + " has loaded to database " +
                 str(len(not_loaded_files)) + " newly processed files.")

    client = pymongo.MongoClient()
    client.close()


def run_full_pipeline(dataset_name: str) -> None:
    """
    Loads config file and starts full pipeline
    -crawl data
    -process data
    -load data to database

    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    logging.info("Starting pipeline for dataset " + dataset_name)
    print("Zpracovávám dataset " + dataset_name +
          ", průběh lze sledovat v logu umístěném v adresáři CrawlerLogs")

    config = configure_functions.load_configuration(dataset_name)
    crawl_data(config)
    process_data(config)

    validation_test = validate_process_data(config)

    if validation_test:
        load_data_to_database(config)


def run_full_pipeline_crone(dataset_name: str) -> None:
    """
    Loads config file and starts full pipeline
    -crawl data
    -process data
    -load data to database

    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    logging.info("Starting pipeline for dataset " + dataset_name)

    config = configure_functions.load_configuration(dataset_name)
    update_test = check_last_update(config)
    if update_test:
        crawl_data(config)
        process_data_crone(config["dataset-name"])

        validation_test = validate_process_data(config)

        if validation_test:
            load_data_to_database_crone(config)
