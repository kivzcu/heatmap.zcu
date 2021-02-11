from Utilities import configure_functions
import pipeline
import os
import sys

# Path to configuration files
CONFIG_FILES_PATH = "DatasetConfigs/"
WRONG_ARG_MSG = "Do argumentu funkce dejte jméno Datasetu, který chcete aktualizovat (pokud všechny zadejte 'ALL'):\n"
DATASET_NOT_FOUND_MSG = "Tento dataset v architektuře neexistuje"


def run_pipeline_for_one_datasets(dataset_name: str) -> None:
    print("Probíhá update datasetu " + dataset_name)
    pipeline.run_full_pipeline(dataset_name)


def run_pipeline_for_all_datasets() -> None:
    """
    Runs whole DataScript pipeline for every dataset that has existing configuration file
    """
    files_in_dir = os.listdir(CONFIG_FILES_PATH)

    for file in files_in_dir:
        name = file.split('.')[0]
        print("Probíhá update datasetu " + name)
        pipeline.run_full_pipeline(name)


def main() -> None:
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1].upper()
        if dataset_name == "ALL":
            run_pipeline_for_all_datasets()
        else:
            test = configure_functions.check_if_there_is_a_config_file(
                dataset_name)
            if test == True:
                run_pipeline_for_one_datasets(dataset_name)
            else:
                print(DATASET_NOT_FOUND_MSG)
    else:
        print(WRONG_ARG_MSG)


if __name__ == "__main__":
    main()