from Utilities.Database import database_loader
from shared_types import StringSetType
# mongodb collection with with already downloaded links
MONGODB_DATASET_LINK_COLLECTION = "LINKS"
# mongodb collection with with already processed files
MONGODB_DATASET_PROCESSED_COLLECTION = "PROCESSED"
# mongodb collection with with already loaded links
MONGODB_DATASET_LOADED_COLLECTION = "LOADED"
# mongodb collection with aviable datasets with number of days from last update
MONGODB_DATASET_COLLECTION = "DATASETS"


def load_ignore_set_links(dataset_name: str) -> StringSetType:
    """
    Loades from database links of already downloaded files by crawler
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    ignore_set = set()

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LINK_COLLECTION]

    data = my_col.find()

    for part in data:
        ignore_set.add(part['name'])

    return ignore_set


def update_ignore_set_links(dataset_name: str, link: str) -> None:
    """
    Adds links of newly crawled files to the database
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LINK_COLLECTION]

    my_col.insert({"name": link})


def reset_ignore_set_links(dataset_name: str) -> None:
    """
    Drops collection of already downloaded links
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LINK_COLLECTION]

    my_col.drop()


def load_ignore_set_processed(dataset_name: str) -> StringSetType:
    """
    Loads from database set of already processed files
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    ignore_set = set()

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_PROCESSED_COLLECTION]

    data = my_col.find()

    for part in data:
        ignore_set.add(part['name'])

    return ignore_set


def update_ignore_set_processed(dataset_name: str, filename: str) -> None:
    """
    Adds files of newly processed files to the database
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_PROCESSED_COLLECTION]

    my_col.insert({"name": filename})


def reset_ignore_set_processed(dataset_name: str) -> None:
    """
    Drops collection of already processed files
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_PROCESSED_COLLECTION]

    my_col.drop()


def load_ignore_set_loaded(dataset_name: str) -> StringSetType:
    """
    Loads from database set of already loaded files in database
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    ignore_set = set()

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LOADED_COLLECTION]

    data = my_col.find()

    for part in data:
        ignore_set.add(part['name'])

    return ignore_set


def update_ignore_set_loaded(dataset_name: str, filename: str) -> None:
    """
    Adds files of newly loaded files to the database
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LOADED_COLLECTION]

    my_col.insert({"name": filename})


def reset_ignore_set_loaded(dataset_name: str) -> None:
    """
    Drops collection of already loaded files
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[dataset_name + MONGODB_DATASET_LOADED_COLLECTION]

    my_col.drop()


def load_updated(dataset_name: str) -> int:
    """
    Loads value of (days from last update) from db
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    updated = 0

    connection = database_loader.create_database_connection()

    my_col = connection[MONGODB_DATASET_COLLECTION]

    data = my_col.find_one({'key-name': dataset_name}, {'updated'})

    updated = int(data['updated'])

    return updated


def update_updated(dataset_name: str, value: int):
    """
    Updates value of (days from last update) in db
    
    Returns:
        dataset_name name of dataset that has existing configuration file
    """

    connection = database_loader.create_database_connection()

    my_col = connection[MONGODB_DATASET_COLLECTION]

    myquery = {'key-name': dataset_name}
    new_values = {"$set": {"updated": value}}

    my_col.update_one(myquery, new_values)
