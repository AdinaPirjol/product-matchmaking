<?php

namespace CoreBundle\Repository;

use Doctrine\ORM\EntityRepository;
use Symfony\Component\Validator\Constraints;

/**
 * Class ProductRepository is the Repository class for entity Product
 *
 * @package CoreBundle\Repository
 */
class ProductRepository extends EntityRepository{

    /**
     * Find all products
     *
     * @return array in ascending order
     */
    public function findAll(){
		return $this->findBy(array(), array('name' => 'ASC'));
	}
} 
