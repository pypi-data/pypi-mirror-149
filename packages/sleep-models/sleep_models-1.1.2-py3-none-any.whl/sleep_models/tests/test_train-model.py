from genericpath import exists
from random import random
import unittest
import os.path

from sklearn.datasets import make_blobs


from sleep_models.models.train import train_model
import sleep_models.models.utils.config as config_utils
from sleep_models.models.variables import AllConfig
from sleep_models.models import MODELS
import sleep_models.models.utils.torch as torch_utils
from sleep_models.tests import STATIC_DATA_FOLDER


arch="RF"
cluster="EG_1"
random_state=1000
target="Treatment"

device = torch_utils.get_device()

training_config = config_utils.setup_config(arch)
output=os.path.join(STATIC_DATA_FOLDER, "test_train-model")
os.makedirs(output, exist_ok=True)

config = AllConfig(
    model_name=arch,
    training_config=training_config,
    cluster=cluster,
    output=output,
    device=device,
    random_state=random_state,
    target=target,
)

X, y = make_blobs(n_samples=10000, n_features=500, centers=2, random_state=random_state)

X_train = X[:7000]
X_test = X[7000:]
y_train = y[:7000]
y_test = y[7000:]
encoding={0: "Sleep", 1: "Wake"}

class TestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            "datasets": (X_train, y_train, X_test, y_test),
            "encoding": encoding
        }


    def test_rf(self):
        model = MODELS[arch].new_model(
            config,
            # these last three are ignored in the EBM, KNN and MLP
            X_train=self.data["datasets"][0],
            y_train=self.data["datasets"][1],
            encoding=self.data["encoding"],
        )
        train_model(model, self.data["datasets"])


if __name__ == "__main__":
    unittest.main()
