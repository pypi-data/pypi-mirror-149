"""
Test the sleep_models.preprocessing module
2022-02-27
"""

import unittest
import os.path

import numpy as np
import anndata
import sleep_models.preprocessing as module
from sleep_models.models.variables import ModelProperties

random_state = 1000
STATIC_DATA_FOLDER = "tests/static_data"
INPUT_H5AD = os.path.join(STATIC_DATA_FOLDER, "test_complex_adata.h5ad")


class TestPreprocessing(unittest.TestCase):
    def test_read_h5ad(self):
        adata = module.read_h5ad(INPUT_H5AD)
        self.assertTrue(isinstance(adata, anndata.AnnData))
        self.assertTrue(isinstance(adata.raw, anndata._core.raw.Raw))
        self.assertFalse(adata.raw is None)

    def test_read_h5ad_raw(self):
        adata = module.read_h5ad(INPUT_H5AD, raw=True)
        self.assertTrue(adata.raw is None)

    def test_read_h5ad_hvg(self):
        # TODO
        pass

    def test_read_h5ad_exclude(self):
        adata = module.read_h5ad(INPUT_H5AD, exclude_genes_file="")
        # TODO

    def test_process_data(self):

        TRAIN_SIZE = 0.5

        adata = module.load_adata(INPUT_H5AD, cluster="y", highly_variable_genes=False)

        model_properties = ModelProperties(
            encoding="ONE_HOT", target="Condition", estimator_type="classifier"
        )

        data_preprocessor = module.Pipeline(
            model_properties=model_properties, random_state=random_state
        )

        X, y = data_preprocessor.process_adata(
            adata, label_mapping={"sleep": 0, "SD": 1}
        )
        labels, counts = np.unique(y.values.argmax(1), return_counts=True)

        X_train, X_test, y_train, y_test = data_preprocessor.split_dataset(
            X, y, train_size=TRAIN_SIZE
        )
        train_ratio = X_train.shape[0] / (X_train.shape[0] + X_test.shape[0])

        self.assertTrue(y.shape[1] == 2)
        self.assertTrue((np.max(counts) - np.min(counts)) <= 1)
        self.assertTrue((train_ratio - TRAIN_SIZE) < 0.01)


class TestConfusionTable(unittest.TestCase):

    def test_make_confusion_long_to_square(self):
        pass



if __name__ == "__main__":
    unittest.main()
