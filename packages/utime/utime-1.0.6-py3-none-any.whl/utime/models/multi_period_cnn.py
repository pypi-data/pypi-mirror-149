import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, \
                                    Input, Flatten, Dense, Reshape

from MultiPlanarUNet.logging import ScreenLogger
from utime.models.utils import standardize_batch_shape
from utime.models import DeepFeatureNet


class MultiPeriodCNN(DeepFeatureNet):
    """
    Standard single epoch CNN
    """
    def __init__(self, n_classes, n_periods, batch_shape,
                 activation="relu",
                 l2_reg=None, logger=None, log=True, **kwargs):
        batch_shape = standardize_batch_shape(batch_shape)
        super(MultiPeriodCNN, self).__init__(
            batch_shape=[n_periods*batch_shape[0], batch_shape[1]],
            n_classes=n_classes,
            padding="same",
            activation=activation,
            l2_reg=l2_reg,
            classify=False,
            build=False
        )
        self.logger = logger or ScreenLogger()
        self.seq_batch_shape = batch_shape
        self.n_periods = n_periods
        super(DeepFeatureNet, self).__init__(*self.init_model())
        if log:
            self.log()

    def log(self):
        self.logger("MultiPeriodCNN Model Summary\n"
                    "----------------------------")
        self.logger("Batch shape:       {}".format(self.batch_shape))
        self.logger("N classes:         {}".format(self.n_classes))
        self.logger("N periods:         {}".format(self.n_periods))
        self.logger("l2 reg:            {}".format(self.l2_reg))
        self.logger("Padding:           {}".format(self.padding))
        self.logger("Conv activation:   {}".format(self.activation))
        self.logger("N params:          {}".format(self.count_params()))
        self.logger("Input:             {}".format(self.input))
        self.logger("Output:            {}".format(self.output))

    def init_model(self, inputs=None):
        inputs = Input([self.n_periods] + list(self.seq_batch_shape))
        ins = Reshape(target_shape=self.batch_shape)(inputs)
        _, outs = super(MultiPeriodCNN, self).init_model(inputs=ins)

        encoded = outs[0]
        while encoded.get_shape()[1].value // 2 > self.n_periods:
            encoded = Conv1D(filters=64, kernel_size=7, strides=1,
                             activation=self.activation, padding='same')(encoded)
            encoded = MaxPooling1D(pool_size=2)(encoded)
            encoded = BatchNormalization()(encoded)
        diff = encoded.get_shape()[1].value - self.n_periods
        encoded = Conv1D(filters=64, kernel_size=diff+1)(encoded)

        # Classify
        outs = Conv1D(filters=self.n_classes, kernel_size=1)(encoded)
        return [inputs], [outs]
