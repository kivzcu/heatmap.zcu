<?php

namespace App\Test\Repository;

use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;
use App\Repository\OpenDataManager;

class OpenDataManagerTest extends KernelTestCase {
    private $manager;

    protected function setUp(): void {
        $kernel = self::bootKernel();
        $this->manager = $kernel->getContainer()->get('App\Repository\IOpenDataManager');
    }

    public function testGetCollectionDataByName() {
        $this->assertFalse(empty($this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')));
        $this->assertTrue(array_key_exists('number', $this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')[0]));
        $this->assertTrue(array_key_exists('place', $this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')[0]));
        $this->assertTrue(array_key_exists('x', $this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')[0]));
        $this->assertTrue(array_key_exists('y', $this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')[0]));
        $this->assertTrue(array_key_exists('date', $this->manager->getCollectionDataByName('KOLOBEZKY', '2019-04-11', '9')[0]));
    }

    public function testGetCollectionDataByNameInvalid() {
        $this->assertTrue(empty($this->manager->getCollectionDataByName(null, null, null)));
        $this->assertTrue(empty($this->manager->getCollectionDataByName('NIC', '2019-04-11', '9')));
        $this->assertTrue(empty($this->manager->getCollectionDataByName('NIC', '11-04-2020', '9')));
        $this->assertTrue(empty($this->manager->getCollectionDataByName('NIC', '2019-04-11', '25')));
    }

    public function testAvailableCollections() {
        $this->assertFalse(empty($this->manager->getAvailableCollections()));
    }

    public function testGetAvailableCollectionsByDay() {
        $this->assertFalse(empty($this->manager->getAvailableCollectionsByDay('2019-04-11')));
    }

    public function testGetAvailableCollectionsByDayInvalid() {
        $this->assertTrue(empty($this->manager->getAvailableCollectionsByDay(null)));
        $this->assertTrue(empty($this->manager->getAvailableCollectionsByDay('11-04-2020')));
    }

    public function testIsCollectionAvailable() {
        $this->assertTrue($this->manager->isCollectionAvailable('KOLOBEZKY', '2019-04-11'));
        $this->assertFalse($this->manager->isCollectionAvailable('KOLOBEZKY', '2000-04-11'));
    }

    public function testIsCollectionAvailableInvalid() {
        $this->assertFalse($this->manager->isCollectionAvailable(null, null));
        $this->assertFalse($this->manager->isCollectionAvailable('NIC', '2019-04-11'));
        $this->assertFalse($this->manager->isCollectionAvailable('KOLOBEZKY', '11-04-2019'));
    }

    public function testGetDatesWithAvailableCollection() {
        $this->assertFalse(empty($this->manager->getDatesWithAvailableCollection()));
        $this->assertRegExp('/^(\d{4})-(\d{2})-(\d{2})/', $this->manager->getDatesWithAvailableCollection()[0]);
    }

    public function testGetLastAvailableCollections() {
        $this->assertFalse(empty($this->manager->getLastAvailableCollections()));
        $this->assertRegExp('/^(\d{4})-(\d{2})-(\d{2})/', $this->manager->getLastAvailableCollections()['KOLOBEZKY']);
    }

    public function testGetMaxCollectionNumberAtDay() {
        $this->assertGreaterThan(0, $this->manager->getMaxCollectionNumberAtDay('KOLOBEZKY', '2019-04-11'));
    }

    public function testGetMaxCollectionNumberAtDayInvalid() {
        $this->assertEquals(0, $this->manager->getMaxCollectionNumberAtDay(null, null));
        $this->assertEquals(0, $this->manager->getMaxCollectionNumberAtDay('NIC', '2019-04-11'));
        $this->assertEquals(0, $this->manager->getMaxCollectionNumberAtDay('KOLOBEZKY', '11-04-2019'));
    }

    public function testGetDataSourcePositions() {
        $this->assertFalse(empty($this->manager->getDataSourcePositions('KOLOBEZKY')));
        $this->assertTrue(array_key_exists('x', $this->manager->getDataSourcePositions('KOLOBEZKY')[0]));
        $this->assertTrue(array_key_exists('y', $this->manager->getDataSourcePositions('KOLOBEZKY')[0]));
    }

    public function testGetDataSourcePositionsInvalid() {
        $this->assertTrue(empty($this->manager->getDataSourcePositions(null)));
        $this->assertTrue(empty($this->manager->getDataSourcePositions('NIC')));
    }
}