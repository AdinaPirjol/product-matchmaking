<?php

namespace CoreBundle\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class UpdateDatabaseControllerTest extends WebTestCase
{
    public function testUpdatedatabase()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/updateDatabase');
    }

}
