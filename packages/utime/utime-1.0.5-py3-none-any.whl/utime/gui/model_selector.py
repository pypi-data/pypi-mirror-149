from PyQt5 import QtWidgets
from PyQt5 import QtCore
from utime.gui.base_widgets import HorizontalSeparator, AttributesWidget
from utime.gui.dialog_boxes import ErrorMessageBox
from utime.gui.default_fonts import TitleFont, COLOR_SHEETS
from utime.utils.scriptutils import assert_project_folder
import os


class ModelSelector(QtWidgets.QWidget):
    """
    Placeholder
    """
    model_dir_updated = QtCore.pyqtSignal(str)
    subject_dir_updated = QtCore.pyqtSignal(str)

    def __init__(self, state, parent=None):
        """
        Args:
            parent:
        """
        super(ModelSelector, self).__init__(parent)
        self.state = state

        # Get buttons
        self.select_model_bot = QtWidgets.QPushButton(text="Select model")
        self.select_file_bot = QtWidgets.QPushButton(text="Select PSG file")
        self.select_model_bot.setFixedWidth(150)
        self.select_file_bot.setFixedWidth(150)
        # self.select_file_bot.setEnabled(False)

        # Bind events
        self.select_model_bot.clicked.connect(self.select_model)
        self.select_file_bot.clicked.connect(self.select_subject_dir)

        # Get handles to model and file widgets
        self.model_widget = AttributesWidget(self.select_model_bot, parent=self)
        self.file_widget = AttributesWidget(self.select_file_bot, parent=self)

        # Set labels
        self.model_widget.title_label.setText("Awaiting model selection...")
        self.model_widget.status_label.setText("")
        self.file_widget.title_label.setText("Awaiting PSG file selection...")
        self.file_widget.status_label.setText("")

        # Set layout
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.model_widget, 1)
        self.layout().addWidget(HorizontalSeparator(self))
        self.layout().addWidget(self.file_widget, 2)

    def select_model(self, model_dir=None):
        model_dir = model_dir or QtWidgets.QFileDialog.getExistingDirectory(
            caption="Select a DeepSleep project folder"
        )
        if not model_dir:
            return
        try:
            assert_project_folder(model_dir, evaluation=True)
        except RuntimeError as e:
            ErrorMessageBox().show_error(str(e))
        else:
            short_path = model_dir.replace(os.path.expanduser("~"), "~")
            self.model_widget.status_label.setText(short_path)
            self.model_dir_updated.emit(model_dir)

    def select_subject_dir(self, subject_dir=None):
        subject_dir = subject_dir or QtWidgets.QFileDialog.getExistingDirectory(
            caption="Select a PSG subject directory to analyse"
        )
        if subject_dir and os.path.exists(subject_dir):
            # Set status label
            short_path = subject_dir.replace(os.path.expanduser("~"), "~")
            self.file_widget.status_label.setText(short_path)
            self.subject_dir_updated.emit(subject_dir)
        elif subject_dir:
            ErrorMessageBox().show_error("Subject dir {} does not "
                                         "exist.".format(subject_dir))
