import os
# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"
# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"
# Path for DatasetCrawlers implementations
CRAWLER_PROGRAM_PATH = "DatasetCrawler"
# Path for DatasetProcessors implementations
PROCESSOR_PROGRAM_PATH = "DatasetProcessing"
# Path to dataset configuration files
CONFIG_FILES_PATH = "DatasetConfigs"
# Default color for visualization of dataset (buble info in map)
DEFAULT_COLOR = "#000000"


def create_default_config_file(dataset_name: str) -> None:
    """
    Creates default config file

    Args:
        dataset_name: Name of newly created dataset
    """
    with open(CONFIG_FILES_PATH + "/" + dataset_name + ".yaml", "w") as file:
        file.write("# Name of the dataset inside the application\n")
        file.write("display-name: " + dataset_name + "\n")
        file.write(
            "# Color for the dataset in a hex value (default value #000000)\n")
        file.write(f'display-color: \'{DEFAULT_COLOR}\' \n')
        file.write(
            "# One word dataset name (structure of all modules will be affected by this)\n"
        )
        file.write("dataset-name: " + dataset_name + "\n")
        file.write("# Url for the source of this dataset\n")
        file.write("url: ENTER URL HERE\n")
        file.write(
            "# Optional parameter which specifies a pattern of the datasets name\n"
        )
        file.write(
            "# Example: DATASET_NAME_[0-9][0-9]_[0-9][0-9][0-9][0-9].zip\n")
        file.write(
            "# - DATASET_NAME_01_2020.zip where '01_2020' specifies date in this dataset\n"
        )
        file.write("regex: ENTER REGEX HERE\n")
        file.write(
            "# Optional parameter which specifies the way of searching new datasets (if empty the period is set to every day)\n"
        )
        file.write("update-period: ENTER UPDATE PERIOD HERE\n")
        file.write("# Coordinates of every datasets device (entinty)\n")
        file.write("devices:\n")


def create_default_processor(dataset_name: str) -> None:
    """
    Creates default processor for dataset

    Args:
        dataset_name: Name of newly created dataset
    """
    with open(PROCESSOR_PROGRAM_PATH + "/" + dataset_name + "_processor.py",
              "w") as file:
        file.write("from Utilities.CSV import csv_data_line\n")
        file.write("from shared_types import DateDict")
        file.write("\n")
        file.write("\n")
        file.write("def process_file(filename: str) -> DateDict:\n")
        file.write("    \"\"\"\n")
        file.write(
            "    Method that takes the path to crawled file and outputs date dictionary:\n"
        )
        file.write(
            "    Date dictionary is a dictionary where keys are dates in format YYYY-mm-dd-hh (2018-04-08-15)\n"
        )
        file.write(
            "    and value is dictionary where keys are devices (specified in configuration file)\n"
        )
        file.write(
            "    and value is CSVDataLine.csv_data_line with device,date and occurrence\n"
        )
        file.write("\n")
        file.write("    Args:\n")
        file.write("    filename: name of the processed file\n")
        file.write("\n")
        file.write("    Returns:\n")
        file.write("    None if not implemented\n")
        file.write("    date_dict when implemented\n")
        file.write("    \"\"\"\n")
        file.write("    date_dict: DateDict = {}\n")
        file.write("\n")
        file.write("    #with open(filename, \"r\") as file:\n")
        file.write(
            "    print(\"You must implement the process_file method first!\")\n"
        )
        file.write("    return date_dict\n")


def create_default_crawler(dataset_name: str) -> None:
    """
    Creates default crawler for dataset

    Args:
        dataset_name: Name of newly created dataset
    """

    with open(CRAWLER_PROGRAM_PATH + "/" + dataset_name + "_crawler.py",
              "w") as file:
        file.write("from shared_types import ConfigType\n")
        file.write("# Path to crawled data\n")
        file.write(f'CRAWLED_DATA_PATH = "{CRAWLED_DATA_PATH}" \n')
        file.write("\n")
        file.write("\n")
        file.write("def crawl(config: ConfigType):\n")
        file.write("    \"\"\"\n")
        file.write(
            "    Implementation the crawl method which downloads new data to the path_for_files\n"
        )
        file.write("    For keeping the project structure\n")
        file.write("    url , regex, and dataset_name from config\n")
        file.write(
            "    You can use already implemented functions from Utilities/Crawler/BasicCrawlerFunctions.py\n"
        )
        file.write("\n")
        file.write("    Args:\n")
        file.write("        config: loaded configuration file of dataset\n")
        file.write("    \"\"\"\n")
        file.write("    dataset_name = config[\"dataset-name\"]\n")
        file.write("    url = config['url']\n")
        file.write("    regex = config['regex']\n")
        file.write(
            "    path_for_files = CRAWLED_DATA_PATH + dataset_name + '/'\n")
        file.write(
            "    print(\"Není implementován crawler pro získávání dat!\")\n")


def prepare_dataset_structure(dataset_name: str) -> None:
    """
    Prepares folders for new dataset
    Args:
        dataset_name: Name of newly created dataset
    """

    # create folder for crawled data
    path = CRAWLED_DATA_PATH + dataset_name
    try:
        os.mkdir(path)
    except os.error as e:
        print(e)
        print("Creation of the directory %s failed" % path)

    # create folder for processed data
    path = PROCESSED_DATA_PATH + dataset_name
    try:
        os.mkdir(path)
    except OSError:
        print("Nelze vytvořit adresář %s" % path)

    create_default_crawler(dataset_name)
    create_default_processor(dataset_name)
    create_default_config_file(dataset_name)


def main() -> None:
    print("Zadejte jméno nového datasetu:\n")
    dataset_name = input().upper()

    if dataset_name.isalpha():
        prepare_dataset_structure(dataset_name)
        print("Architektura vytvořena \n")
    else:
        print("Jméno musí obsahovat pouze písmena z abecedy (bez mezer)\n")


if __name__ == "__main__":
    main()