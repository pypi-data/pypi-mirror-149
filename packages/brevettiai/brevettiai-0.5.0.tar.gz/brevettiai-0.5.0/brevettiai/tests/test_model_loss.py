import unittest
import tensorflow as tf

from brevettiai.model.losses import WeightedLossV2


class TestModelLoss(unittest.TestCase):
    loss_settings = {
        "label_smoothing": .05,
        "sample_weights": [[1.0], [1.0], [0.2]],
        "sample_weights_bias": [0.0]}

    def test_weighted_loss(self):
        loss_configurator = WeightedLossV2.parse_obj(self.loss_settings)
        loss = loss_configurator.get_loss(reduction='NONE')(tf.eye(4, 3)[None, None], tf.ones((4, 3))[None, None] * .3)
        assert(loss.shape[-1] == 3 and loss.shape[-2] == 4)


if __name__ == '__main__':
    unittest.main()
