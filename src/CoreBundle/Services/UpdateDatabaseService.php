<?php
namespace CoreBundle\Services;

use Doctrine\DBAL\DBALException;
use CoreBundle\Entity\Category;
use CoreBundle\Entity\Product;
use Exception;
use Symfony\Component\DependencyInjection\Container as Container;

/**
 * Class UpdateDatabaseService is the Service that works with database
 *
 * @package CoreBundle\Services
 */
class UpdateDatabaseService {

    /**
     * @var \Symfony\Component\DependencyInjection\Container $container
     */
    private $container = null;

    /**
     * @var \Doctrine\ORM\EntityManager $em
     */
    private $em = null;

    /**
     * @var \Symfony\Component\Validator\Validator\LegacyValidator $validator
     */
    private $validator = null;

    /**
     * Class Constructor
     *
     * @param Container $container
     */
    function __construct(Container $container){

        $this->container = $container;
        $this->em = $this->container->get('doctrine')->getManager();
        $this->validator = $this->container->get('validator');
    }

    /**
     * Add new category in database
     *
     * @param $name
     * @return string $message
     *
     * If an error occurs it returns the error message
     */
    public function addCategory($name){

        $message = "1 record added";
        $category = new Category();
        $category->setName($name);
        $errors = $this->validator->validate($category);

        if( count($errors)> 0 ){

            $message = $errors;
        } else {

            try{
                $this->em->persist($category);
                $this->em->flush();
            }catch(DBALException $e){
                $message = $e->getMessage();
            }
        }

        return $message;
    }

    /**
     * Get categories from database
     *
     * @return array $response
     *         string for error message
     */
    public function getCategories(){

        try {
            $categories = $this->em->getRepository("CoreBundle:Category")->findAll();
        }catch(Exception $e){
            return $e->getMessage();
        }

        $response = array();
        if( count($categories)> 0 ){
            foreach($categories as $category){
                $response[] = array('id'=>$category->getIdCategory(), 'name'=>$category->getName() );
            }
        }

        return $response;
    }

    /**
     * Add new product in database
     *
     * @param int $category
     * @param string $name
     * @param string $link
     * @return string
     *
     * If an error occurs it returns the error message
     */
    public function addProduct($category,$name,$link){

        try{

            //try to get the instance of the category with the imput id
            $categ = $this->em->getRepository("CoreBundle:Category")->findOneBy( array('id_category' => $category) );

            $message = "1 record added";
            $product = new Product();
            $product->setCategory($categ);
            $product->setName($name);
            $product->setLinkEmag($link);
            $errors = $this->validator->validate($product);

            if( count($errors)> 0 ){

                $message = $errors;
            } else {

                try{
                    $this->em->persist($product);
                    $this->em->flush();
                }catch(DBALException $e){
                    $message = $e->getMessage();
                }
            }

            return $message;

        }catch(Exception $e){

            //if the searched category doesn't exist
            return $e->getMessage();
        }

    }

    /**
     * Get products from database
     *
     * @return array $response
     *         string for error message
     */
    public function getProducts(){

        try{
             $products = $this->em->getRepository("CoreBundle:Product")->findAll();
        }catch(Exception $e){
             return $e->getMessage();
        }

        $response = array();
        if( count($products)> 0 ){
            foreach($products as $product){
                $response[] = array('id'=>$product->getIdProduct(), 'name'=>$product->getName(), 'category' =>$product->getCategory()->getIdCategory() );
            }
        }

        return $response;
    }

    /**
     * Get matched products from database by id
     *
     * @param $array
     * @return array $response
     *         int for empty array
     *         string for error message
     */
    public function getRequiredProducts($array){

        $response = array();
        try {
            if(empty($array))
                return -1;
            else{
                foreach($array as $id){
                    $product = $this->em->getRepository("CoreBundle:Product")->findOneBy( array( 'id_product' => $id ) );
                    $response[] = array( 'name' => $product->getName() , 'link' => $product->getLinkEmag(), 'category' => $product->getCategory()->getIdCategory(), 'id' => $id );
                }
                return $response;
            }
        } catch (Exception $e) {
            return $e->getMessage();
        }
    }
} 
