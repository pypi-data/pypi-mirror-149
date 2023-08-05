from PyQt5 import QtWidgets
from utime.gui.default_fonts import TitleFont
from PyQt5.QtCore import Qt


class YesNoDialog(QtWidgets.QMessageBox):
    def __init__(self, parent=None):
        super(YesNoDialog, self).__init__(parent)

    def ask(self, yes_no_question, default="no"):
        self.setText(yes_no_question)
        self.setStandardButtons(self.Yes | self.No)
        self.setDefaultButton(self.No if default.lower() == "no" else self.Yes)
        return True if self.exec() == self.Yes else False


class ErrorMessageBox(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ErrorMessageBox, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()

        # Main label
        self.text_label = QtWidgets.QLabel()
        self.text_label.setFont(TitleFont())

        # Error information label
        self.informative_label = QtWidgets.QLabel()
        self.informative_label.setWordWrap(True)
        continue_bot = QtWidgets.QPushButton("Continue")
        continue_bot.setFixedWidth(200)
        continue_bot.clicked.connect(self.quit)

        # Set layout
        layout.addWidget(self.text_label)
        layout.addWidget(self.informative_label)
        layout.addWidget(continue_bot)
        layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(layout)

    def show_error(self, error_msg, title="An error occurred"):
        self.text_label.setText(title)
        self.informative_label.setText(error_msg)
        self.show()
        self.setFixedSize(self.size())
        self.exec()

    def quit(self):
        self.close()
