import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Conv1D
from tensorflow.signal import fft, ifft


class FourierConv1D(Layer):
    def __init__(self, name='fourier_conv_layer'):
        super().__init__(name=name)

    def build(self, input_shape):
        pass

    def call(self, inputs, **kwargs):
        o = fft(inputs)
        print(o, inputs)
        pass


import numpy as np
import matplotlib.pyplot as plt


y = np.sin(sorted(np.random.rand(3000) * 3)).astype(np.complex)


w = np.sin(sorted(np.random.rand(1000)))
w = np.pad(w, pad_width=np.ceil((len(y)-len(w))/2).astype(np.int),
           mode="constant", constant_values=0)
n1 = np.fft.fft(y * w)



fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.plot(np.abs(y))
#ax2.plot(np.abs(n1))
ax2.plot(y * w)
ax3.plot(np.fft.ifft(n1))
plt.show()
