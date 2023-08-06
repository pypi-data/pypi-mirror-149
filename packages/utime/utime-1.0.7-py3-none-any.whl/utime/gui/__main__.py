from PyQt5 import QtWidgets
from PyQt5 import QtCore
from utime.gui.main_window import DeepSleepMainWindow
from utime.gui.predictor import Predictor
from utime.gui.utils import get_attrs_from_model_dir

import os
import sys


class ModelLoaderThread(QtCore.QThread):
    model_loaded = QtCore.pyqtSignal(object)

    def __init__(self, build_hparams, weights, status_label=None):
        super(ModelLoaderThread, self).__init__()
        self.build_hparams = build_hparams
        self.weights = weights
        self.status_label = status_label

    def run(self):
        from utime.models.model_init import init_model
        from MultiPlanarUNet.logging.default_logger import ScreenLogger
        logger = ScreenLogger(print_to_screen=False)
        self.status_label.setText("Initializing model.....")
        self.build_hparams["data_per_prediction"] = 1
        self.build_hparams["eval_mode"] = True
        model = init_model(self.build_hparams, logger, clear_previous=True)
        self.status_label.setText("Loading weights.....")
        model.load_weights(self.weights, by_name=True)
        self.status_label.setText("Model loaded")
        self.model_loaded.emit(model)


class FileLoaderThread(QtCore.QThread):
    file_loaded = QtCore.pyqtSignal(object)
    attributes_extracted = QtCore.pyqtSignal(dict)
    data_ready = QtCore.pyqtSignal(object, int, int)

    def __init__(self, subject_dir, hparams, status_label=None):
        super(FileLoaderThread, self).__init__()
        self.subject_dir = subject_dir
        self.hparams = hparams
        self.status_label = status_label

    def set_hparams(self, hparams):
        self.hparams = hparams

    def run(self):
        from utime.dataset import SleepStudyDataset
        from utime.utils.scriptutils import select_sample_strip_scale_quality
        from MultiPlanarUNet.logging.default_logger import ScreenLogger

        if not self.hparams:
            self.status_label.setText("File ready, but waiting for model.....")
            while not self.hparams:
                self.msleep(500)

        logger = ScreenLogger(print_to_screen=False)
        self.status_label.setText("Initializing dataset.....")

        # Extract important hyperparameters
        period_length = self.hparams['train_data'].get("period_length_sec")
        sample_rate = self.hparams['train_data'].get("set_sample_rate")

        annot = self.hparams.get("sleep_stage_annotations")

        # Load and preprocess the data
        f, r = os.path.split(self.subject_dir)
        ssd = SleepStudyDataset(data_dir=f, folder_regex=r,
                                period_length_sec=period_length,
                                set_sample_rate=sample_rate,
                                annotation_dict=annot, logger=logger)
        select_sample_strip_scale_quality(ssd, hparams=self.hparams, logger=logger)
        self.status_label.setText("Loading data.....")
        ssd.load()
        self.status_label.setText("PSG file loaded")

        # Get sequence objects
        seq = ssd.get_batch_sequence(random_batches=False,
                                     augmenters=self.hparams.get("augmenters"),
                                     **self.hparams["fit"], no_log=True)
        seq.augmentation_enabled = False

        # Dispatch the data for plotting
        s = ssd.pairs[0]
        self.data_ready.emit(seq, s.sample_rate, s.period_length_sec)

        # Update widget attributes
        cls_dict = s.get_class_counts(as_dict=True)
        qa = s.quality_control_func[0] if s.quality_control_func else None
        attrs = {
            "identifier": s.identifier,
            "Length": f"{s.recording_length_sec} sec",
            "Segments": s.n_periods,
            "True classes": list(cls_dict.keys()),
            "True counts": list(cls_dict.values()),
            "N channels": len(s.select_channels),
            "Loaded channels": "\n".join(s.select_channels),
            "Sample rate": f"{s.sample_rate} Hz",
            "Staging rate": f"1/{s.period_length_sec} Hz",
            "Scaler": s.scaler,
            "Date": s.date,
            "Strip func": s.strip_func,
            "QA func": qa
        }
        self.attributes_extracted.emit(attrs)
        self.file_loaded.emit(seq)


class DeepSleepVisualizer(QtCore.QObject):
    load_model_signal = QtCore.pyqtSignal(dict, str)
    load_file_signal = QtCore.pyqtSignal(str)
    hparams_set_signal = QtCore.pyqtSignal(dict)
    model_updated_signal = QtCore.pyqtSignal(object)
    sequence_updated_signal = QtCore.pyqtSignal(object)

    def __init__(self, model_dir=None, subject_dir=None, parent=None):
        super(DeepSleepVisualizer, self).__init__(parent)

        # Create a prediction thread
        self.predictor = Predictor(parent=self)

        self.main_window = DeepSleepMainWindow(predictor=self.predictor,
                                               state=self)
        self.main_window.showMaximized()

        # Connect the model and file selection signals of the model
        # selector widget
        self.main_window.model_selector_widget.model_dir_updated.connect(
            self.load_model
        )
        self.main_window.model_selector_widget.subject_dir_updated.connect(
            self.load_file
        )

        # Connect model and file update signals to the plotting threads
        self.model_updated_signal.connect(self.predictor.update_model)
        self.sequence_updated_signal.connect(self.predictor.update_sequence)

        # Connect pred data to pred thread
        self.main_window.plot_widget.predictor = self.predictor

        # Connect predicted data to visualizer thread
        self.predictor.pred_out.connect(
            self.main_window.plot_widget.add_to_pred_dict
        )

        # Store the loaded model and file
        self.model = None
        self.sequence = None
        self.hparams = None

        # Store worker threads
        self.model_load_thread = None
        self.file_load_thread = None

        # Invoke model and file selection programmatically?
        if model_dir:
            self.main_window.model_selector_widget.select_model(model_dir)
        if subject_dir:
            self.main_window.model_selector_widget.select_subject_dir(subject_dir)

    def _set_model(self, model):
        self.model = model
        self.model_updated_signal.emit(model)

    def _set_sequence(self, sequence):
        self.sequence = sequence
        self.sequence_updated_signal.emit(sequence)

    def load_model(self, model_dir):
        self.model = None

        # Get and load model from directory
        attrs, hparams = get_attrs_from_model_dir(model_dir)
        hparams["fit"]["batch_size"] = 1
        self.hparams = hparams
        self.hparams_set_signal.emit(self.hparams)

        # Update widget attribute list
        self.main_window.model_selector_widget.model_widget.update_attribute_widget(attrs)

        # Start queue for loading model
        weights = f"{model_dir}/model/{attrs['weights']}"

        ms = self.main_window.model_selector_widget.model_widget.title_label
        self.model_load_thread = ModelLoaderThread(hparams["build"],
                                                   weights=weights,
                                                   status_label=ms)
        self.model_load_thread.model_loaded.connect(self._set_model)
        self.model_load_thread.start()

    def load_file(self, subject_dir):
        self.sequence = None

        ms = self.main_window.model_selector_widget.file_widget.title_label
        self.file_load_thread = FileLoaderThread(subject_dir, self.hparams, ms)
        self.file_load_thread.attributes_extracted.connect(
            self.main_window.model_selector_widget.file_widget.update_attribute_widget
        )
        self.hparams_set_signal.connect(self.file_load_thread.set_hparams)
        self.file_load_thread.file_loaded.connect(self._set_sequence)
        self.file_load_thread.data_ready.connect(self.main_window.plot_widget.update_signal)
        self.file_load_thread.start()

    def update_file_attrs(self, attrs):
        self.main_window.model_selector_widget.\
            file_widget.update_attribute_widget(attrs)


def run_gui(**kwargs):
    # Create the app
    app = QtWidgets.QApplication([])
    ex = DeepSleepVisualizer(**kwargs)
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
