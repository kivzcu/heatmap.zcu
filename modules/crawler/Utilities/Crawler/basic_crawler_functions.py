import requests
import re
from Utilities import folder_processor
from Utilities.Database import database_record_logs
from bs4 import BeautifulSoup
from typing import List

# Path to crawler logs
CRAWLER_LOGS_PATH = "CrawlerLogs/"
# Path to crawled data
CRAWLED_DATA_PATH = "CrawledData/"
LinksType = List[str]


def get_all_links(url: str) -> LinksType:
    """
    Sends http request to url, downloads all data,
    extract links

    Args:
        url: url of website we want to search

    Returns:
        list of all links
    """
    # create response object
    r = requests.get(url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, 'html5lib')
    links = []

    for link in soup.findAll('a'):
        links.append(link.get('href'))

    return links


def filter_links(links: LinksType, regex: str) -> LinksType:
    """
    Filters list of links using regex

    Args:
        links: list of links
        regex: regex used for filtering

    Returns:
        filtered list of links
    """
    filtered_links = []

    for link in links:
        if re.search(regex, link):
            filtered_links.append(link)

    return filtered_links


def create_absolute_links(links: LinksType, archive: str) -> LinksType:
    """
        Appends archive path to every link in links
    Args:
        links: list of relative links
        archive: archive url

    Returns:
        list of absolute links
    """
    absolute_links = []

    for link in links:
        absolute_links.append(archive + link)

    return absolute_links


def remove_downloaded_links(links: LinksType, dataset_name: str) -> LinksType:
    """
    Loads already downloaded links from CRAWLER_LOGS_PATH ignore.txt
    Args:
        links: list of links
        dataset_name: name of dataset that has existing configuration file

    Returns:
        List of links without already downloaded links
    """
    downloaded_links = database_record_logs.load_ignore_set_links(dataset_name)
    final_links = set(links) - downloaded_links

    return final_links


def download_file_from_url(url: str, dataset_name: str) -> None:
    """
    Downloads file on provided url and saves it to path
    Args:
        url: url file we want to download
        dataset_name: name of dataset that has existing configuration file
    """
    r = requests.get(url, stream=True)

    # splits url and extract last part that contains filename
    url_parts = url.split("/")
    file_name = url_parts[len(url_parts) - 1]

    data_path = CRAWLED_DATA_PATH + dataset_name + '/'

    # download file chunk by chunk so we can download large files
    with open(data_path + file_name, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):

            # writing one chunk at a time to file
            if chunk:
                file.write(chunk)

    # after successful download update list of already downloaded files
    database_record_logs.update_ignore_set_links(dataset_name, url)
