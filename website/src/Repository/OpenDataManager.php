<?php

namespace App\Repository;

use MongoDB\Driver\Query;
use MongoDB\Driver\Manager;

/**
 * Implementation of IOpenDataManager
 * autowired @see website/config/services.yaml and https://symfony.com/doc/current/service_container/autowiring.html.
 *
 * @see IOpenDataManager for methods comments
 */
class OpenDataManager implements IOpenDataManager {
    /**
     * @var IOpenDataManager autowired connection to database
     */
    private $manager;

    /**
     * @param string connection string to database
     */
    public function __construct($connectionString) {
        $this->manager = new Manager(
            $connectionString
        );
    }

    public function getCollectionDataByName($name, $date, $hour) {
        if (null == $name || null == $date || null == $hour) {
            return [];
        }

        // Number has to be two digit
        $valh = $hour < 10 ? '0'.$hour : $hour;
        $openData = $this->manager->executeQuery('open-data-db.'.$name.$date, new Query(['date' => $date.'-'.$valh], []));

        // Converts result to php array
        $openData->setTypeMap([
            'array' => 'array',
            'document' => 'array',
            'root' => 'array',
        ]);

        return $openData->toArray();
    }

    public function getAvailableCollections() {
        $openData = $this->manager->executeQuery('open-data-db.DATASETS', new Query([], ['projection' => ['key-name' => 1, 'display-name' => 1, 'display-color' => 1, '_id' => 0]]));

        // Converts result to php array
        $openData->setTypeMap([
            'array' => 'array',
            'document' => 'array',
            'root' => 'array',
        ]);

        return $openData->toArray();
    }

    public function getAvailableCollectionsByDay($date) {
        $availableInDate = [];
        $available = $this->getAvailableCollections();
        $index = 0;
        foreach ($available as $key => $value) {
            if ($this->isCollectionAvailable($value['key-name'], $date) && false == array_key_exists($value['key-name'], $availableInDate)) {
                $availableInDate[$value['key-name']] = $value['display-name'];
            }
        }

        return $availableInDate;
    }

    public function isCollectionAvailable($name, $date) {
        if (null == $name || null == $date) {
            return false;
        }

        $result = $this->manager->executeQuery('open-data-db.'.$name, new Query(['date' => $date], []));

        return !empty($result->toArray());
    }

    public function getDatesWithAvailableCollection() {
        $available = $this->getAvailableCollections();
        $result = [];

        foreach ($available as $key => $value) {
            $dates = $this->manager->executeQuery('open-data-db.'.$value['key-name'], new Query([], ['projection' => ['date' => true, '_id' => false]]));
            $dates->setTypeMap(['root' => 'array']);
            $result = array_merge($result, array_map(function ($item) {return $item['date']; }, $dates->toArray()));
        }

        return array_values(array_unique($result));
    }

    public function getLastAvailableCollections() {
        $available = $this->getAvailableCollections();
        $result = [];

        foreach ($available as $key => $value) {
            $date = $this->manager->executeQuery('open-data-db.'.$value['key-name'], new Query([], ['sort' => ['date' => -1], 'limit' => 1, 'projection' => ['date' => true, '_id' => false]]));
            $date->setTypeMap(['root' => 'array']);

            $date_array = $date->toArray();
            if (!empty($date_array)) {
                $result[$value['key-name']] = $date_array[0]['date'];
            }
        }

        return $result;
    }

    public function getMaxCollectionNumberAtDay($name, $date) {
        if (null == $name || null == $date) {
            return 0;
        }

        $max = $this->manager->executeQuery('open-data-db.'.$name.$date, new Query([], ['sort' => ['number' => -1], 'limit' => 1]));

        // Converts result to php array
        $max->setTypeMap([
            'array' => 'array',
            'document' => 'array',
            'root' => 'array',
        ]);

        $result = $max->toArray();

        return empty($result) ? 0 : $result[0]['number'];
    }

    public function getDataSourcePositions($name = 'NONE') {
        if (null == $name) {
            return [];
        }

        $positions = $this->manager->executeQuery('open-data-db.'.$name.'DEVICES', new Query([], []));

        // Converts result to php array
        $positions->setTypeMap([
            'array' => 'array',
            'document' => 'array',
            'root' => 'array',
        ]);

        return $positions->toArray();
    }
}
