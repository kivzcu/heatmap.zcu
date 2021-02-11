from Utilities import folder_processor
from Utilities.Crawler import basic_crawler_functions
from shared_types import ConfigType

# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"


def crawl(config: ConfigType):
    """
    Implement crawl method that downloads new data to path_for_files
    For keeping the project structure
    url , regex, and dataset_name from config
    You can use already implemented functions from Utilities/Crawler/basic_crawler_functions.py

    Args:
        config: loaded configuration file of dataset
    """
    dataset_name = config["dataset-name"]
    url = config['url']
    regex = config['regex']
    path_for_files = CRAWLED_DATA_PATH + dataset_name + '/'

    first_level_links = basic_crawler_functions.get_all_links(url)

    filtered_first_level_links = basic_crawler_functions.filter_links(
        first_level_links, "^OD_ZCU")

    OFFSET_YEAR_START = -5
    OFFSET_YEAR_END = -1
    MONTH_SIZE = 2

    #Seperate links by year
    links_by_year = {}
    for item in filtered_first_level_links:
        if item[OFFSET_YEAR_START:OFFSET_YEAR_END] not in links_by_year:
            links_by_year[item[OFFSET_YEAR_START:OFFSET_YEAR_END]] = []
        else:
            links_by_year[item[OFFSET_YEAR_START:OFFSET_YEAR_END]].append(item)

    #Latest links of years to array
    links = []
    for _key, value in links_by_year.items():
        if not value:
            continue
        
        links.append(
            max(value,
                key=lambda x: int(x[OFFSET_YEAR_START - MONTH_SIZE - 1:
                                    OFFSET_YEAR_START - 1])))

    absolute_first_level_links = basic_crawler_functions.create_absolute_links(
        links, url)

    files = []

    for link in absolute_first_level_links:
        second_level_links = basic_crawler_functions.get_all_links(link)
        filtered_second_level_links = basic_crawler_functions.filter_links(
            second_level_links, regex)
        absolute_second_level_links = basic_crawler_functions.create_absolute_links(
            filtered_second_level_links, link)

        for file_link in absolute_second_level_links:
            files.append(file_link)

    files = basic_crawler_functions.remove_downloaded_links(
        files, dataset_name)

    for file in files:
        basic_crawler_functions.download_file_from_url(file, dataset_name)

    folder_processor.unzip_all_csv_zip_files_in_folder(path_for_files)
