import unittest
import numpy as np
from sleep_models.plotting import make_matrixplot

matrix = np.array([
    [255, 127, 0],
    [200, 127, 0],
    [170, 127, 0],
], dtype=np.uint8).T



class TestMakeMatrixPlot(unittest.TestCase):

    def test_legend(self):
        make_matrixplot(
            matrix = matrix,
            clusters = ["a","b","c"],
            filenames= ["test.png"],
            barlimits=[0,100],
            dpi=20
        )

if __name__ == "__main__":
    unittest.main()
