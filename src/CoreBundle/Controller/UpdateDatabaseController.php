<?php

namespace CoreBundle\Controller;

use PDOException;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\JsonResponse;

/**
 * Class UpdateDatabaseController is the Controller that works with database
 *
 * @package CoreBundle\Controller
 */
class UpdateDatabaseController extends Controller
{

    /**
     * Main function for UpdateDatabaseController
     *
     * @return \Symfony\Component\HttpFoundation\Response
     */
    public function updateDatabaseAction()
    {

        $message = "";

        if (isset($_POST['formCategory'])) {
            $message = $this->addCategory();
        }

        if (isset($_POST['formProduct'])) {
            $message = $this->addProduct();
        }

        if (isset($_POST['addKeypoint_message'])) {
            $message = $_POST['addKeypoint_message'];
        }

        return $this->render(
            'CoreBundle:UpdateDatabase:updateDatabase.html.twig',
            array('message' => $message));
    }

    /**
     * Add new category in database
     *
     * @return string $message
     */
    private function addCategory()
    {
        $service = $this->get("update_database");
        $message = $service->addCategory($_POST['name']);
        return $message;
    }

    /**
     * Add new product in database
     *
     * @return string $message
     */
    private function addProduct()
    {
        $service = $this->get("update_database");
        $message = $service->addProduct($_POST['category'], $_POST['name'], $_POST['link']);
        return $message;
    }

    /**
     * Get categories from database
     *
     * @return JsonResponse $response
     */
    public function getCategoriesAction()
    {
        $service = $this->get("update_database");
        $response = $service->getCategories();
        return new JSONResponse($response);
    }

    /**
     * Get products from database
     *
     * @return JsonResponse $response
     */
    public function getProductsAction()
    {
        $service = $this->get("update_database");
        $response = $service->getProducts();
        return new JSONResponse($response);
    }
}
