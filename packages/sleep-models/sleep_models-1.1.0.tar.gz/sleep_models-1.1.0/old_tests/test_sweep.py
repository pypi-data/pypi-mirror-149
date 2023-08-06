import unittest

import logging
import json
import os
from argparse import Namespace

import anndata

from sleep_models.bin.train_model import setup_model_and_datasets

# test sweep


def preprocess_config(config):

    config = config["parameters"]

    for k, v in config.items():
        if "min" in v.keys():
            config[k] = v["min"]
        elif "values" in v.keys():
            config[k] = v["values"][0]

    config.pop("_wandb", None)
    return config


class TestSweep(unittest.TestCase):
    def setUp(self):
        adata = anndata.read_h5ad("./tests/static_data/test_adata.h5ad")
        args = Namespace(model="MLP", random_state=10000, cluster="y", results_dir=None)
        logger = logging.getLogger("sleep_models.tests")
        self._model, _ = setup_model_and_datasets(adata, args, logger)
        self._run = Namespace(name="test")

        with open("./tests/static_data/wandb_config.json") as fh:
            config = preprocess_config(json.load(fh))

        self._config = {"_wandb": None, **config}

    def test__train(self):
        self._model._train(self._run, self._config)


if __name__ == "__main__":
    unittest.main()
