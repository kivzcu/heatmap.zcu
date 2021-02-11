<?php

namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class HatmapControllerTest extends WebTestCase {
    public function testPageLoad() {
        $client = static::createClient();
        $client->request('GET', '/heatmap');

        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testPageLoadWithData() {
        $client = static::createClient();
        $client->request('GET', '/heatmap?date=2019-04-11&time=12&type[]=JIS');

        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testPageLoadWithInvalidData() {
        $client = static::createClient();
        $client->request('GET', '/heatmap?date=2019-04-11&time=12&type[]=NIC');
        $this->assertTrue($client->getResponse()->isSuccessful());

        $client->request('GET', '/heatmap?date=2019-04-11&time=25&type[]=KOLOBEZKY');
        $this->assertTrue($client->getResponse()->isSuccessful());

        $client->request('GET', '/heatmap?date=11-04-2019&time=12&type[]=KOLOBEZKY');
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testFormSubmit() {
        $client = static::createClient();
        $client->request('GET', '/heatmap');

        $crawler = $client->submitForm('btn-update-heatmap');
        $this->assertTrue($client->getResponse()->isSuccessful());

        $crawler = $client->submitForm(
            'btn-update-heatmap',
            [
                'date' => '2019-04-11',
                'time' => '0',
                'type[1]' => 'JIS',
            ]
        );
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testFormSubmitInvalid() {
        $client = static::createClient();
        $client->request('GET', '/heatmap');

        $crawler = $client->submitForm(
            'btn-update-heatmap',
            [
                'date' => '11-04-2019',
                'time' => '0',
                'type[1]' => 'JIS',
            ]
        );
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testOpenDataAjax() {
        $client = static::createClient();
        $client->xmlHttpRequest('POST', '/heatmap/opendata', [
            'name' => 'KOLOBEZKY',
            'date' => '2019-04-11',
            'time' => '9',
        ]);
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testAvailableDatasetsAjax() {
        $client = static::createClient();
        $client->xmlHttpRequest(
            'POST',
            '/heatmap/available',
            [
                'date' => '2019-04-11',
            ]
        );
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testDatesWithAvailableDatasetsAjax() {
        $client = static::createClient();
        $client->xmlHttpRequest('POST', '/heatmap/dates');
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testDataSourcePoistionsAjax() {
        $client = static::createClient();
        $client->xmlHttpRequest(
            'POST',
            '/heatmap/positions',
            [
                'name' => 'KOLOBEZKY',
            ]
        );
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    public function testLastAvailableCollectionsAjax() {
        $client = static::createClient();
        $client->xmlHttpRequest('POST', '/heatmap/last');
        $this->assertTrue($client->getResponse()->isSuccessful());
    }
}
