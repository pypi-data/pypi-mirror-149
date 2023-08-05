import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, \
                                    Input, Flatten, Dense

from MultiPlanarUNet.logging import ScreenLogger
from utime.utils import exactly_one_specified
from utime.models.utils import standardize_batch_shape


class TrivialCNN(tf.keras.Model):
    """
    Standard single epoch CNN
    """
    def __init__(self, n_classes, filters, batch_shape=None, input_tensor=None,
                 out_activation="softmax",
                 activation="relu", kernel_size=3, padding="same",
                 l2_reg=None, logger=None, **kwargs):
        super(TrivialCNN, self).__init__()
        if not exactly_one_specified(batch_shape, input_tensor):
            raise ValueError("Must specify exactly either 'batch_shape' or "
                             "'input_tensor'.")

        # Set various attributes
        self.logger = logger or ScreenLogger()
        self.batch_shape = standardize_batch_shape(batch_shape)
        self.input_tensor = input_tensor
        self.filters = filters
        self.n_classes = n_classes
        self.kernel_size = kernel_size
        self.activation = activation
        self.out_activation = out_activation
        self.padding = padding
        self.l2_reg = l2_reg

        # Build model and init base keras Model class
        super(TrivialCNN, self).__init__(*self.init_model())
        self.log()

    def init_model(self):
        if self.batch_shape:
            inputs = Input(shape=self.batch_shape)
        else:
            inputs = Input(tensor=self.input_tensor)

        # Apply regularization if not None or 0
        kr = tf.keras.regularizers.l2(self.l2_reg) if self.l2_reg else None

        # Encoder
        in_ = inputs
        for i, filters in enumerate(self.filters):
            l_name = "encoder" + "_L%i" % i
            conv = Conv1D(filters, self.kernel_size,
                          activation=self.activation, padding=self.padding,
                          kernel_regularizer=kr, name=l_name + "_conv1")(in_)
            bn = BatchNormalization(name=l_name + "_BN")(conv)
            in_ = MaxPooling1D(pool_size=(2,), name=l_name + "_pool")(bn)

        # Classifier
        with tf.name_scope("classifier"):
            flat = Flatten()(in_)
            outs = Dense(self.n_classes, self.out_activation)(flat)

        return [inputs], [outs]

    def log(self):
        self.logger("TrivialCNN Model Summary\n------------------------")
        self.logger("Batch shape:       {}".format(self.batch_shape))
        self.logger("Filters:           {}".format(self.filters))
        self.logger("N classes:         {}".format(self.n_classes))
        self.logger("l2 reg:            {}".format(self.l2_reg))
        self.logger("Padding:           {}".format(self.padding))
        self.logger("Conv activation:   {}".format(self.activation))
        self.logger("Out activation:    {}".format(self.out_activation))
        self.logger("N params:          {}".format(self.count_params()))
        self.logger("Output:            {}".format(self.output))
