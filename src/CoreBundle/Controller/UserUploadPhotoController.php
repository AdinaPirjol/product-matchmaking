<?php

namespace CoreBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\JsonResponse;

class UserUploadPhotoController extends Controller
{

    /**
     * Gets the categories, then renders the view calling it with the retrieved array of categories.
     */
    public function showUploadPageAction()
    {
        $categories = $this->getCategories();
        return $this->render('CoreBundle:UserUploadPhoto:showUploadPage.html.twig',
                             array("categories" => $categories)
                            );
    }

    /**
     * Gets the categories using the method provided by the service.
     */
    private function getCategories() {
        $category = $this->get("update_database");
        $message = $category->getCategories();
        return $message;
    }

    /**
     * This method is called when the user uploads a photo.
     * It then calls the method provided by the service which tries to write to server the file received from the user.
     * On success, the method returns a success string, the catergory id,
     * the name of the newly file added to server and its location.
     * On failure, the method returns a failure string.
     */
    public function ajaxAction()
    {
        $service = $this->get('upload_photo');
        $success = $service->ajax();

        if ($success != "Unable to save this image.")
            return new JSONResponse($success);
        else
            return new JSONResponse("Failed!");
    }
}
