import unittest

import numpy as np

np.random.seed(1000)
import os
import shutil
from sleep_models.models import EBM

TEST_FOLDER = "tests/temp_data/model_cache/"


class TestModelDumpLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._X = np.random.randint(0, 10, (10, 100))
        cls._y = np.random.randint(0, 2, 10)
        os.makedirs(TEST_FOLDER)

        cls._model = EBM("cell_type", output=TEST_FOLDER, random_state=1000)
        cls._model.fit(cls._X, cls._y)

    def test_model_can_be_cached(self):
        self._model.dump("model.joblib")

    def test_model_can_be_reloaded(self):
        self._model = EBM.load(os.path.join(TEST_FOLDER, "model.joblib"))

    def test_model_can_be_reused(self):
        pred = self._model.predict(np.random.randint(0, 100, (1, 100)))
        self.assertTrue(pred == 0)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_FOLDER)


if __name__ == "__main__":
    unittest.main()
