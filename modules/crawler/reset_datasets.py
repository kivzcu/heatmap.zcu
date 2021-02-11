import os
from Utilities import folder_processor
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


def hard_reset_dataset(dataset_name: str) -> None:
    """
    Resets all saved data in dataset except config and implementation
    Args:
        dataset_name: name of dataset that has existing configuration file
    """

    path = CRAWLED_DATA_PATH + dataset_name + "/"
    folder_processor.clean_folder(path)

    path = PROCESSED_DATA_PATH + dataset_name + "/"
    folder_processor.clean_folder(path)

    database_loader.remove_dataset_database(dataset_name)


def soft_reset_dataset(dataset_name: str) -> None:
    """
    Resets all saved data in dataset except config and implementation
    Args:
        dataset_name: name of dataset that has existing configuration file
    """
    path = PROCESSED_DATA_PATH + dataset_name + "/"
    folder_processor.clean_folder(path)

    database_loader.remove_dataset_database(dataset_name)


def soft_reset_all_datasets() -> None:
    """
    Resets all saved data in all datasets with config file except configs and implementation
    """
    datasets = os.listdir(CONFIG_FILES_PATH)

    for dataset in datasets:
        soft_reset_dataset(dataset.split('.')[0])


def hard_reset_all_datasets() -> None:
    """
    Resets all saved data in all datasets with config file except configs and implementation
    """
    datasets = os.listdir(CONFIG_FILES_PATH)

    for dataset in datasets:
        hard_reset_dataset(dataset.split('.')[0])


def main() -> None:
    print(
        "Zadejte jméno Datasetu který chcete resetovat (pokud všechny zadejte '-ALL'):\n"
    )

    dataset_name = input().upper()

    print("Chcete smazat i stažená data ? (ANO/NE) \n")

    input_decision = input().upper()

    if dataset_name == '-ALL':
        if input_decision == 'ANO':
            hard_reset_all_datasets()
        elif input_decision == 'NE':
            soft_reset_all_datasets()
        else:
            print('Neplatný vstup (ANO/NE)')
    else:
        test = configure_functions.check_if_there_is_a_config_file(
            dataset_name)
        if test == True:
            if input_decision == 'ANO':
                hard_reset_dataset(dataset_name)
            elif input_decision == 'NE':
                soft_reset_dataset(dataset_name)
            else:
                print('Neplatný vstup (ANO/NE)')
        else:
            print("Tento dataset v architektuře neexistuje")


if __name__ == "__main__":
    main()