import pipeline
import os

# Path to configuration files
CONFIG_FILES_PATH = "DatasetConfigs/"


def run_pipeline_for_all_datasets() -> None:
    """
    Runs whole DataScript pipeline for every dataset that has existing configuration file
    """
    files_in_dir = os.listdir(CONFIG_FILES_PATH)

    for file in files_in_dir:
        name = file.split('.')[0]
        pipeline.run_full_pipeline_crone(name)


def main() -> None:
    run_pipeline_for_all_datasets()


if __name__ == "__main__":
    main()
