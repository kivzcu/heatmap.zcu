<?php

namespace App\Utils;

/**
 * Class for static helper functions.
 */
class Utils {
    /**
     * Transforms array of arrays in form [['display-name' => whatever, 'key-name' => whatever, ...], ...]
     * to simple array in form [dataset-display-name => dataset-key-name, ...].
     *
     * @param array of arrays for tranformation
     *
     * @return array in form [dataset-display-name => dataset-key-name, ...]
     */
    public static function prepareDatasetsNames($datasets) {
        $names = [];

        foreach ($datasets as $key => $value) {
            if (false == array_key_exists($value['key-name'], $names)) {
                $names[$value['display-name']] = $value['key-name'];
            }
        }

        return $names;
    }

    public static function prepareDatasetsColors($datasets) {
        $colors = [];
        foreach ($datasets as $key => $value) {
            if (false == array_key_exists($value['key-name'], $colors)) {
                $colors[$value['key-name']] = $value['display-color'];
            }
        }

        return $colors;
    }
}
