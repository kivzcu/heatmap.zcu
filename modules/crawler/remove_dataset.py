import os
import shutil
from Utilities.Database import database_loader
from Utilities import configure_functions

# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"
# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"
# Path to crawler logs
CRAWLER_LOGS_PATH = "CrawlerLogs/"
# Path to dataset configuration files
CONFIG_FILES_PATH = "DatasetConfigs"
# Path for DatasetCrawlers implementations
CRAWLER_PROGRAM_PATH = "DatasetCrawler"
# Path for DatasetProcessors implementations
PROCESSOR_PROGRAM_PATH = "DatasetProcessing"


def remove_dataset(dataset_name: str) -> None:
    """
    Remove dataset
    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    shutil.rmtree(CRAWLED_DATA_PATH + dataset_name + "/")
    shutil.rmtree(PROCESSED_DATA_PATH + dataset_name + "/")

    os.remove(CRAWLER_PROGRAM_PATH + "/" + dataset_name + "_crawler.py")
    os.remove(PROCESSOR_PROGRAM_PATH + "/" + dataset_name + "_processor.py")
    os.remove(CONFIG_FILES_PATH + "/" + dataset_name + ".yaml")

    print("Dataset " + dataset_name + " odebrán z architektury")

    database_loader.remove_dataset_database(dataset_name)

    print("Dataset " + dataset_name + " odebrán z databáze")


def main() -> None:
    print("Zadejte jméno Datasetu který chcete odstranit:\n")
    dataset_name = input().upper()
    test = configure_functions.check_if_there_is_a_config_file(dataset_name)

    if test == True:
        remove_dataset(dataset_name)
    else:
        print("Tento dataset v architektuře neexistuje")


if __name__ == "__main__":
    main()