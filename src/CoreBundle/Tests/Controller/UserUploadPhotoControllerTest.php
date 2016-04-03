<?php

namespace CoreBundle\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class UserUploadPhotoControllerTest extends WebTestCase
{
    public function testShowuploadpage()
    {
        $client = static::createClient();

        $crawler = $client->request('GET', '/showUploadPage');
    }

}
