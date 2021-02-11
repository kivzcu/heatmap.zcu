<?php

namespace App\Controller;

use App\Utils\Utils;
use App\Entity\DataSet;
use App\Form\DatasetFormBuilder;
use App\Repository\IOpenDataManager;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class HeatmapController extends AbstractController {
    /**
     * Map page controller.
     *
     * @param IOpenDataManager $manager connection to database autowired
     *
     * @Route("/heatmap", name="heatmap")
     */
    public function index(Request $request, IOpenDataManager $manager) {
        $dataSet = new DataSet();
        $datasetFormBuilder = new DatasetFormBuilder($manager);
        $formBuilder = $datasetFormBuilder->getBuilder();

        $form = $formBuilder->getForm();
        $form->submit($request->query->all());
        $isSubmitted = $form->isSubmitted();
        if ($isSubmitted) {
            $dataSet = $form->getData();
            //check availability
            $notExist = false;
            if ($dataSet->getType() && count($dataSet->getType()) > 0) {
                foreach ($dataSet->getType() as $value) {
                    if (!$manager->isCollectionAvailable($value, $dataSet->getDate())) {
                        $notExist = true;
                        break;
                    }
                }
            } else {
                $notExist = true;
            }
            if ($notExist) {
                // Not? Populate form with empty data
                $formBuilder = $datasetFormBuilder->getBuilder();
                $form = $formBuilder->getForm();
            }
        }
        //ziskej barvy o datasetech a namapuj je na jejich jmena

        return $this->render(
            'heatmap.html.twig',
            [
                'form' => $form->createView(),
                'submitted' => $isSubmitted,
                'data_to_display' => $dataSet,
                'dataset_colors' => Utils::prepareDatasetsColors($manager->getAvailableCollections()),
                'formated_current_time' => $dataSet->getFormattedTime(),
                'current_time' => $dataSet->getTime(),
            ]
        );
    }

    /**
     * Provides specific dataset information i.e. position, number and other informations depending on data type.
     *
     * @param IOpenDataManager $manager connection to database autowired
     * @param string           $name    dataset name
     * @param string           $date    dataset date in format YYYY-mm-dd
     * @param string           $time    dataset time, number between 0 - 23
     *
     * @return json with dataset information
     *
     * @Route("heatmap/opendata/{name}/{date}/{time}", name="opendata")
     */
    public function opendata(IOpenDataManager $manager, $name = 'NONE', $date = '2020-01-01', $time = '1') {
        return $this->json([
            'items' => $manager->getCollectionDataByName($name, $date, $time),
            'max' => $manager->getMaxCollectionNumberAtDay($name, $date),
        ]);
    }

    /**
     * Provides available datasets in given date.
     *
     * @param IOpenDataManager $manager connection to database autowired
     * @param string           $date    dataset date in format YYYY-mm-dd
     *
     * @return json with available datasets names
     *
     * @Route("heatmap/available/{date}", name="available")
     */
    public function availableDatasets(IOpenDataManager $manager, $date = '2020-01-01') {
        return $this->json($manager->getAvailableCollectionsByDay($date));
    }

    /**
     * Provides dates with at least one available dataset.
     *
     * @param IOpenDataManager $manager connection to database
     *
     * @return json with dates with at least one available dataset in format YYYY-mm-dd
     *
     * @Route("heatmap/dates", name="dates")
     */
    public function datesWithAvailableDatasets(IOpenDataManager $manager) {
        return $this->json($manager->getDatesWithAvailableCollection());
    }

    /**
     * Provides for dataset with given name all locations.
     *
     * @param IOpenDataManager $manager connection to database autowired
     * @param string           $name    dataset name
     *
     * @return json with all locations for dataset with given name as [x => lat, y => lng]
     *
     * @Route("heatmap/positions/{name}", name="positions")
     */
    public function dataSourcePoistions(IOpenDataManager $manager, $name = 'NONE') {
        return $this->json($manager->getDataSourcePositions($name));
    }

    /**
     * Provides last available date for each available dataset type.
     *
     * @param IOpenDataManager $manager connection to database autowired
     *
     * @return json with last available date for each available dataset type as [collection-type-name => YYYY-mm-dd]
     *
     * @Route("heatmap/last", name="last")
     */
    public function lastAvailableCollections(IOpenDataManager $manager) {
        return $this->json($manager->getLastAvailableCollections());
    }
}
