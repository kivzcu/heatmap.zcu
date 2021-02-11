import os

# Path to configuration files
CONFIG_FILES_PATH = "DatasetConfigs/"
# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"
# Path to processed data
PROCESSED_DATA_PATH = "ProcessedData/"
# Path to crawler logs
CRAWLER_LOGS_PATH = "CrawlerLogs/"


def prepare_strucure_for_all_datasets() -> None:
    """
    Prepares folders that are necessery but does not contain code so they are excluded from gitlab by gitignore
    """

    if not os.path.isdir(CRAWLED_DATA_PATH):
        try:
            os.mkdir(CRAWLED_DATA_PATH)
        except os.error as e:
            print(e)
            print("Nelze vytvořit adresář %s" % CRAWLED_DATA_PATH)

    if not os.path.isdir(PROCESSED_DATA_PATH):
        try:
            os.mkdir(PROCESSED_DATA_PATH)
        except os.error as e:
            print(e)
            print("Nelze vytvořit adresář %s" % PROCESSED_DATA_PATH)

    if not os.path.isdir(CRAWLER_LOGS_PATH):
        try:
            os.mkdir(CRAWLER_LOGS_PATH)
        except os.error as e:
            print(e)
            print("Nelze vytvořit adresář %s" % CRAWLER_LOGS_PATH)

    files_in_dir = os.listdir(CONFIG_FILES_PATH)

    for file in files_in_dir:
        name = file.split('.')
        prepare_structure(name[0])


def prepare_structure(dataset_name: str) -> None:
    """
    Create folder for every dataset in newly created folder for processed and crawled data
    """

    path = CRAWLED_DATA_PATH + dataset_name
    if not os.path.isdir(path):
        os.mkdir(path)

    path = PROCESSED_DATA_PATH + dataset_name
    if not os.path.isdir(path):
        os.mkdir(PROCESSED_DATA_PATH + dataset_name)


def main() -> None:
    print("Inicializuji počáteční strukturu pro stažená a zpracovaná data")
    prepare_strucure_for_all_datasets()


if __name__ == "__main__":
    main()