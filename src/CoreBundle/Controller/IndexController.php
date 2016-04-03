<?php

namespace CoreBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class IndexController extends Controller
{

    /**
     *
     * It's called whenever the user gets in the index page.
     */
    public function indexAction()
    {
        return $this->render(
            'CoreBundle:Index:index.html.twig',
            array()
        );
    }

}
