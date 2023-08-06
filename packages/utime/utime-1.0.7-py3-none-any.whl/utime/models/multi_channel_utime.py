import tensorflow as tf
from utime.models import UTime
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, BatchNormalization, Cropping2D, \
                                    Concatenate, MaxPooling2D, Dense, \
                                    UpSampling2D, ZeroPadding2D, Lambda, Conv2D, \
                                    AveragePooling2D, DepthwiseConv2D
import numpy as np


def assert_data_per_period(data_per_period, input_dims):
    if not isinstance(data_per_period, (int, np.integer)):
        raise TypeError("data_per_prediction must be an integer value")
    if input_dims % data_per_period:
        raise ValueError("'input_dims' ({}) must be evenly divisible by "
                         "'data_per_prediction' ({})".format(input_dims,
                                                         data_per_period))


class MultiChanUTime(UTime):
    """
    1D UNet implementation with batch normalization and complexity factor adj.

    OBS: Uses 2D operations internally with a 'dummy' axis, so that a batch
         of shape [bs, d, c] is processed as [bs, d, 1, c]. These operations
         are currently significantly faster in tf.keras.

    See original U-net paper at http://arxiv.org/abs/1505.04597
    """
    def __init__(self,
                 n_classes,
                 batch_shape,
                 n_channel_mix_filters=16,
                 data_per_prediction=None,
                 eval_mode=False,
                 **kwargs):
        super(MultiChanUTime, self).__init__(
            build=False,
            n_classes=n_classes,
            batch_shape=batch_shape,
            **kwargs
        )
        self.mix_filters = n_channel_mix_filters
        self._data_per_prediction = data_per_prediction

        self.eval_mode = eval_mode
        if self.eval_mode:
            self._stored_seq_model_weights = None
            self.base_model = Model(*self.init_base_model())
            self.seq_model = Model(*self.init_seq_model(self.base_model.outputs[0]))
        else:
            super(UTime, self).__init__(*self.init_model())
            self.log()

    @property
    def data_per_prediction(self):
        return self._data_per_prediction

    @data_per_prediction.setter
    def data_per_prediction(self, value):
        self.set_data_per_prediction(value)

    def set_data_per_prediction(self, value):
        if not self.eval_mode:
            raise RuntimeError("Cannot set data per prediction for model not "
                               "in eval_mode.")
        assert_data_per_period(value, self.input_dims)
        self._data_per_prediction = value
        self.seq_model = Model(*self.init_seq_model(self.base_model.outputs[0]))
        if self._stored_seq_model_weights is not None:
            self.seq_model.set_weights(self._stored_seq_model_weights)

    def load_weights(self, weights, by_name=False):
        self.base_model.load_weights(weights, by_name)
        self.seq_model.load_weights(weights, by_name)
        self._stored_seq_model_weights = self.seq_model.get_weights()

    def predict(self, x):
        if not self.eval_mode:
            return super().predict(x)
        else:
            return self.seq_model.predict(self.base_model.predict(x))

    def predict_on_batch(self, x):
        if not self.eval_mode:
            return super().predict_on_batch(x)
        else:
            return self.seq_model.predict_on_batch(self.base_model.predict_on_batch(x))

    def init_base_model(self):
        inputs = Input(
            shape=[self.n_periods, self.input_dims, self.n_channels])
        chan_ins = Lambda(lambda x: tf.split(x, self.n_channels, axis=-1))(
            inputs)
        chan_outs = []
        for chan_idx, chan in enumerate(chan_ins):
            with tf.name_scope("channel_{}".format(chan_idx)):
                chan_out = super(MultiChanUTime, self).init_model(
                    inputs=chan,
                    create_seg_modeling=False,
                    name_prefix="C{}_".format(chan_idx)
                )[1]
            chan_outs.append(chan_out[0])

        with tf.name_scope("channel_mixture"):
            # Mix channels to form a single prediction output
            chan_outs = Concatenate(axis=-1)(chan_outs)
            dense = self.create_dense_modeling(
                in_=chan_outs,
                filters=self.mix_filters,
                dense_classifier_activation=self.dense_classifier_activation
            )
        return [inputs], [dense]

    def init_seq_model(self, inputs):
        if self.eval_mode:
            inputs = Input(batch_shape=inputs.get_shape())
        dpp = self.data_per_prediction or self.data_per_prediction
        out = self.create_seq_modeling(in_=inputs,
                                       input_dims=self.input_dims,
                                       data_per_period=dpp,
                                       n_periods=self.n_periods,
                                       n_classes=self.n_classes,
                                       transition_window=self.transition_window,
                                       init_biases=self.init_biases)

        return [inputs], [out]

    def init_model(self):
        inputs, dense = self.init_base_model()
        _, out = self.init_seq_model(dense[0])
        return inputs, out
