<?php

namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class HomeControllerTest extends WebTestCase {
    public function testMainPage() {
        $client = static::createClient();
        $client->request('GET', '/');
        $this->assertTrue($client->getResponse()->isSuccessful());
    }

    // public function provideLinks() {
    //     return [
    //         ['Logo Západočeské univerzity v Plzni'],
    //         ['Heatmap.ZČU'],
    //         ['Život na ZČU během dne'],
    //         ['Hledání anomálií'],
    //         ['O projektu'],
    //         ['Zobrazit heatmapu'],
    //         ['Vyzkoušet heatmapu'],
    //     ];
    // }

    // /**
    //  * @dataProvider provideLinks
    //  */
    // public function testLinks($link) {
    //     $client = static::createClient();
    //     $crawler = $client->request('GET', '/');
    //     $client->clickLink($link);
    //     $this->assertTrue($client->getResponse()->isSuccessful());
    // }
}
