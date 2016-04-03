<?php

namespace CoreBundle\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class UserResponsePageControllerTest extends WebTestCase
{
    public function testResponsepage()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/responsePage');
    }

}
