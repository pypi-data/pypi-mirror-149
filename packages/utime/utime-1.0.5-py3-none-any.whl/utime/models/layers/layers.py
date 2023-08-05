from tensorflow._api.v1.keras.layers import Layer
from tensorflow._api.v1.keras.initializers import zeros, constant, ones
from tensorflow._api.v1.keras.activations import get
import tensorflow as tf


class BiasedSum(Layer):
    def __init__(self,
                 sum_axis=-2,
                 init_biases=None,
                 activation=None,
                 name="biased_sum_layer"):
        self.init_biases = init_biases
        self.activation = get(activation)
        self.axis = sum_axis
        self.biases = None
        super().__init__(name=name)

    def build(self, input_shape):
        self.biases = self.add_weight(
            name='biases',
            shape=[input_shape[-1]],
            initializer=constant(value=self.init_biases) if self.init_biases is not None else zeros,
            trainable=True,
            dtype=self.dtype
        )
        super().build(input_shape)

    def call(self, inputs, **kwargs):
        return self.activation(tf.reduce_sum(inputs, axis=self.axis) + self.biases)


class LinearTransform(BiasedSum):
    def __init__(self,
                 sum_axis=-2,
                 init_biases=None,
                 activation=None,
                 name="linear_transform_layer"):
        self.slopes = None
        super(LinearTransform, self).__init__(
            sum_axis=sum_axis,
            init_biases=init_biases,
            activation=activation,
            name=name
        )

    def build(self, input_shape):
        self.slopes = self.add_weight(
            name='slopes',
            shape=[1] * (len(input_shape) - 2) + [input_shape[-1]],
            initializer=ones,
            trainable=True,
            dtype=self.dtype
        )
        super().build(input_shape)

    def call(self, inputs, **kwargs):
        x = tf.reduce_sum(inputs, axis=self.axis)
        return self.activation(self.slopes * x + self.biases)
