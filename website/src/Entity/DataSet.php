<?php

namespace App\Entity;

/**
 * Class wich represent From on heatmap page and is bind to that form.
 *
 * @see https://symfony.com/doc/current/forms.html
 */
class DataSet {
    protected $time;
    protected $date;
    protected $type;

    public function setTime($time) {
        $this->time = $time;
    }

    public function getTime() {
        return $this->time;
    }

    public function getFormattedTime() {
        return (strlen($this->time) <= 2) ? date('H:i', strtotime($this->time.':00')) : $this->time;
    }

    public function setDate($date) {
        $this->date = date('Y-m-d', strtotime($date));
    }

    public function getDate() {
        return $this->date;
    }

    public function setType($type) {
        $this->type = $type;
    }

    public function getType() {
        return $this->type;
    }
}
