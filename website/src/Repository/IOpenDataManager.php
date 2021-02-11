<?php

namespace App\Repository;

/**
 * interface for database connection management
 * autowired @see website/config/services.yaml and https://symfony.com/doc/current/service_container/autowiring.html.
 */
interface IOpenDataManager {
    /**
     * Provides specific dataset information i.e. position, number and other informations depending on data type.
     *
     * @param string $name dataset name
     * @param string $date dataset date in format YYYY-mm-dd
     * @param string $hour dataset hour, number between 0 - 23
     *
     * @return array with dataset information
     */
    public function getCollectionDataByName($name, $date, $hour);

    /**
     * Provides all available data sets types.
     *
     * @return array with avalable datasets names
     */
    public function getAvailableCollections();

    /**
     * Provides available datasets in given date.
     *
     * @param string $date dataset date in format YYYY-mm-dd
     *
     * @return array with available datasets names
     */
    public function getAvailableCollectionsByDay($date);

    /**
     * Check if dataset with given name is available for given date.
     *
     * @param string $name dataset name
     * @param string $date dataset date in format YYYY-mm-dd
     *
     * @return bool true if dataset with given name is available in given date otherwise false
     */
    public function isCollectionAvailable($name, $date);

    /**
     * Provides dates with at least one available dataset.
     *
     * @return array with dates with at least one available dataset in format YYYY-mm-dd
     */
    public function getDatesWithAvailableCollection();

    /**
     * Provides max value of all locations (data dources) in dataset with given date on given date.
     *
     * @param string $name dataset name
     * @param string $date dataset date in format YYYY-mm-dd
     *
     * @return number max value of all locations (data dources) in dataset with given date on given date
     */
    public function getMaxCollectionNumberAtDay($name, $date);

    /**
     * Provides for dataset with given name all locations.
     *
     * @param string $name dataset name
     *
     * @return array with all locations for dataset with given name as [x => lat, y => lng]
     */
    public function getDataSourcePositions($name);

    /**
     * Provides last available date for each available dataset type.
     *
     * @return array with last available date for each available dataset type as [collection-type-name => YYYY-mm-dd]
     */
    public function getLastAvailableCollections();
}
