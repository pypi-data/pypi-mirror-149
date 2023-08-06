import unittest
import os
import os.path
import shutil

import numpy as np

from sleep_models.preprocessing import read_h5ad
from sleep_models.dimensionality_reduction import get_markers
from sleep_models.dimensionality_reduction import (
    get_umap,
    run_umap,
    make_umap_plot,
)
from sleep_models.dimensionality_reduction import (
    Homogenization,
    benchmark_homogenization,
    plot_homogenization,
)


TEST_H5AD = "tests/static_data/test_adata.h5ad"
TEST_H5AD_WO_GENE = "tests/static_data/test_adata_without_gene.h5ad"
MAX_CLUSTERS = 3
TEST_FOLDER = "tests/temp_data/umap"


class TestGetMarkerGenes(unittest.TestCase):
    def setUp(self):
        self._adata = read_h5ad(TEST_H5AD)

    def test_get_markers(self):
        
        cell_type_list = np.unique(self._adata.obs["CellType"].values).tolist()

        markers = get_markers(
            cell_types=cell_type_list,
            marker_dir="tests/static_data/markers",
        )

        self.assertTrue(
            set(markers["gene"]) == set(["gene2", "gene3", "gene4", "gene5"])
        )


class TestHomogenize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._adata = read_h5ad(TEST_H5AD)
        cls._folder = os.path.join(TEST_FOLDER, "threshold-inf")
        cls._reducer = get_umap()

    def setUp(self):
        os.makedirs(self._folder)

    def test_umap(self):
        embedding = run_umap(self._reducer, self._adata.X)
        fig, ax, metrics = make_umap_plot(
            self._folder, "inf", embedding, self._adata, lims=None
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(TEST_FOLDER, "threshold-inf", "UMAP_threshold-inf.png")
            )
        )

    def test_homogenize_evaluation(self):

        centers = {
            cluster: np.float32(np.random.rand(1, 2)) for cluster in ["y", "ab", "abp"]
        }
        distance = {("y", "ab"): 0.5, ("y", "abp"): 0.5, ("ab", "abp"): 0.5}
        silhouette = 0.5
        embedding = np.float32(np.random.rand(9, 2))

        homogenization = Homogenization(embedding, centers, distance, silhouette)

        results = {"inf": (homogenization, None), "inf2": (homogenization, None)}

        benchmark = benchmark_homogenization(TEST_FOLDER, results)

        self.assertTrue(os.path.exists(os.path.join(TEST_FOLDER, "benchmark.csv")))

        plot_homogenization(TEST_FOLDER, self._adata, results, benchmark)
        self.assertTrue(os.path.exists(os.path.join(TEST_FOLDER, "homogenization.png")))

    def tearDown(self):
        shutil.rmtree(TEST_FOLDER)


if __name__ == "__main__":
    unittest.main()
