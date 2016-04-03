<?php

namespace CoreBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class UserResponsePageController extends Controller
{

    /**
     * Method called when the python scripts finish to process the image send by the user.
     * It receives through POST the user's photo name, the matched IDs and the number of matches for each ID.
     * It then calls the service to retrieve the matched products from the database and this informations
     * are send to the view to show them to the user.
     */
    public function responsePageAction()
    {
        $services = $this->get("update_database");
        $path = $this->container->getParameter('path') . $_POST['userphoto'];
        $matches = $this->getMatchedResults();
        $nrmatches = $this->getNrMatchedResults();
        $message = $services->getRequiredProducts($matches);

        return $this->render(
            'CoreBundle:UserResponsePage:responsePage.html.twig',
            array(
                "matches" => $message,
                "nrmatches" => $nrmatches,
                "path" => $path
            )
        );
    }

    /**
     * Gets the matched IDs from the POST
     */
    private function getMatchedResults()
    {
        $matches = explode(";", $_POST['matches']);
        $x = array_pop($matches);
        return $matches;
    }

    /**
     * Gets the number of matches for each ID from the POST
     */
    private function getNrMatchedResults()
    {
        $nrmatches = explode(";", $_POST['nrmatches']);
        $x = array_pop($nrmatches);
        return $nrmatches;
    }
}
