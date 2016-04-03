<?php

namespace CoreBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Product
 *
 * @ORM\Table(name="Products", uniqueConstraints={@ORM\UniqueConstraint(name="UNIQ_4ACC380C5E237E06", columns={"name"}),
 *                                                @ORM\UniqueConstraint(name="UNIQ_4ACC380C73C4BCEA", columns={"link_emag"})},
 *                             indexes={@ORM\Index(name="IDX_4ACC380C5697F554", columns={"id_category"})})
 * @ORM\Entity(repositoryClass="CoreBundle\Repository\ProductRepository")
 */
class Product
{
    /**
     * @var integer
     *
     * @ORM\Column(name="id_product", type="integer")
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="IDENTITY")
     */
    private $id_product;

    /**
     * @var string
     *
     * @ORM\Column(name="name", type="string", length=250, nullable=false)
     */
    private $name;

    /**
     * @var string
     *
     * @ORM\Column(name="link_emag", type="string", length=250, nullable=false)
     */
    private $link_emag;

    /**
     * @var Category
     *
     * @ORM\ManyToOne(targetEntity="CoreBundle\Entity\Category", inversedBy="products")
     * @ORM\JoinColumns({
     *   @ORM\JoinColumn(name="id_category", referencedColumnName="id_category")
     * })
     */
    private $category;

    /**
     * Get id_product
     *
     * @return integer 
     */
    public function getIdProduct()
    {
        return $this->id_product;
    }

    /**
     * Set name
     *
     * @param string $name
     * @return Product
     */
    public function setName($name)
    {
        $this->name = $name;

        return $this;
    }

    /**
     * Get name
     *
     * @return string 
     */
    public function getName()
    {
        return $this->name;
    }

    /**
     * Set link_emag
     *
     * @param string $linkEmag
     * @return Product
     */
    public function setLinkEmag($linkEmag)
    {
        $this->link_emag = $linkEmag;

        return $this;
    }

    /**
     * Get link_emag
     *
     * @return string 
     */
    public function getLinkEmag()
    {
        return $this->link_emag;
    }

    /**
     * Set category
     *
     * @param Category $category
     * @return Product
     */
    public function setCategory(Category $category)
    {
        $this->category = $category;

        return $this;
    }

    /**
     * Get category
     *
     * @return Category
     */
    public function getCategory()
    {
        return $this->category;
    }
}
