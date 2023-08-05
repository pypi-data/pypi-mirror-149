from PyQt5 import QtCore
from queue import Empty, LifoQueue
import numpy as np


class PredictThread(QtCore.QThread):
    pred_out = QtCore.pyqtSignal(int, np.ndarray)

    def __init__(self, model, sequence, in_queue, parent=None):
        super(PredictThread, self).__init__(parent)
        self.model = model
        self.sequence = sequence
        self.in_queue = in_queue
        self.sleep_study = self.sequence.pairs[0]
        self.running = True
        assert len(self.sequence.pairs) == 1

    def run(self):
        while self.running:
            try:
                inds, batch_x, data_per_prediction = self.in_queue.get_nowait()
            except Empty:
                self.msleep(200)
                continue
            # inds are format global/psg start index, local/batch start index,
            # local/batch end index)
            id_, start, end = inds
            n_periods, input_dim = batch_x.shape[1:3]
            if self.model.data_per_prediction != data_per_prediction:
                self.model.set_data_per_prediction(data_per_prediction)
            outs = self.model.predict_on_batch(batch_x)[0]
            if outs.ndim == 3:
                np.expand_dims(outs, axis=-2)  # data_per_prediction == input_dim
            self.pred_out.emit(id_, outs[start:end])


class Predictor(QtCore.QObject):
    pred_out = QtCore.pyqtSignal(int, np.ndarray)

    def __init__(self, parent=None):
        super(Predictor, self).__init__(parent)
        self.model = None
        self.graph = None
        self.sequence = None
        self.pred_thread = None
        self.in_pred_queue = LifoQueue()

    def emit_prediction(self, id_, pred):
        self.pred_out.emit(id_, pred)

    def add_batch_to_queue(self, inds, batch, data_per_period):
        self.in_pred_queue.put((inds, batch, data_per_period))

    def clear_input_queue(self):
        while not self.in_pred_queue.empty():
            try:
                self.in_pred_queue.get_nowait()
            except Empty:
                pass

    def update_model(self, model):
        self.model = model
        if self.sequence:
            self.start_predict_thread()

    def update_sequence(self, sequence):
        self.sequence = sequence
        if self.model:
            self.start_predict_thread()

    def start_predict_thread(self):
        if self.pred_thread:
            self.pred_thread.running = False
        self.pred_thread = PredictThread(self.model, self.sequence,
                                         in_queue=self.in_pred_queue,
                                         parent=self)
        self.pred_thread.pred_out.connect(self.emit_prediction)
        self.pred_thread.start()
