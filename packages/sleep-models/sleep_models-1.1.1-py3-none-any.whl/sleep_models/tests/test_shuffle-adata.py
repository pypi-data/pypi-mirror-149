import unittest
import os.path

from sleep_models.tests import STATIC_DATA_FOLDER
import sleep_models.preprocessing as pp

ADATA_FILE = os.path.join(STATIC_DATA_FOLDER, "test_adata.h5ad")
ADATA_OUTPUT_FILE = os.path.join(STATIC_DATA_FOLDER, "shuffled_adata.h5ad")

class TestShuffleAdata(unittest.TestCase):
    
    
    def setUp(self):
        self.adata = pp.read_h5ad(ADATA_FILE)

    def test_shuffle_adata(self):
        pinned_columns=["Treatment", "Condition"]

        adata_shuffled=pp.shuffle_adata(self.adata, ADATA_OUTPUT_FILE, pinned_columns=pinned_columns)
        self.assertTrue(self.adata.shape == adata_shuffled.shape)
        for column in pinned_columns:
            for level in self.adata.obs[column]:
                cells_shuffled = adata_shuffled.obs.loc[adata_shuffled.obs["Treatment"] == level].index
                cells_original = self.adata.obs.loc[self.adata.obs["Treatment"] == level].index

                cells_shuffled=tuple(sorted(cells_shuffled.values.copy().tolist()))
                cells_original=tuple(sorted(cells_original.values.copy().tolist()))

                self.assertEqual(cells_shuffled, cells_original)


if __name__ == "__main__":
    unittest.main()
