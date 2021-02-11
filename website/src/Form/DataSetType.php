<?php

namespace App\Form;

use App\Utils\Utils;
use App\Entity\DataSet;
use App\Repository\IOpenDataManager;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;

class DataSetType extends AbstractType {
    /**
     * @var IOpenDataManager autowired connection to database
     */
    private $manager;

    /**
     * @param IOpenDataManager autowired connection to database
     */
    public function __construct(IOpenDataManager $manager) {
        $this->manager = $manager;
    }

    /**
     * @see https://symfony.com/doc/current/forms.html
     */
    public function buildForm(FormBuilderInterface $builder, array $options) {
        $builder
            ->add('date', TextType::class)
            // Populate time select with data
            ->add('time', ChoiceType::class, [
                'choices' => [
                    '0:00-1:00' => 0,
                    '1:00-2:00' => 1,
                    '2:00-3:00' => 2,
                    '3:00-4:00' => 3,
                    '4:00-5:00' => 4,
                    '5:00-6:00' => 5,
                    '6:00-7:00' => 6,
                    '7:00-8:00' => 7,
                    '8:00-9:00' => 8,
                    '9:00-10:00' => 9,
                    '10:00-11:00' => 10,
                    '11:00-12:00' => 11,
                    '12:00-13:00' => 12,
                    '13:00-14:00' => 13,
                    '14:00-15:00' => 14,
                    '15:00-16:00' => 15,
                    '16:00-17:00' => 16,
                    '17:00-18:00' => 17,
                    '18:00-19:00' => 18,
                    '19:00-20:00' => 19,
                    '20:00-21:00' => 20,
                    '21:00-22:00' => 21,
                    '22:00-23:00' => 22,
                    '23:00-0:00' => 23,
                ],
            ])
            // Populet type select with data
            ->add('type', ChoiceType::class, [
                'choices' => Utils::prepareDatasetsNames($this->manager->getAvailableCollections()),
            ])
            ->add('submit', SubmitType::class);
    }

    /**
     * @see https://symfony.com/doc/current/forms.html
     */
    public function configureOptions(OptionsResolver $resolver) {
        $resolver->setDefaults([
            'data_class' => DataSet::class,
            'method' => 'GET',
        ]);
    }
}
