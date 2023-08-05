from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from utime.gui.base_widgets import (VerticalSeparator,
                                    ListHorizontalSliderWithLabels)
from utime.gui.default_fonts import TitleFont


class Settings(QtWidgets.QWidget):
    """
    Placeholder
    """
    def __init__(self, parent=None):
        """
        Args:
            parent:
        """
        super(Settings, self).__init__(parent)

        # Create 4 sub-layouts for various setting groups
        group_1 = self._get_layout_1()
        pred_settings_layout, self.pred_settings_widgets = self._get_pred_settings_layout()
        group_3 = self._get_layout_3()

        # Set layout
        self.setLayout(QtWidgets.QHBoxLayout())

        self.layout().addLayout(group_1, 1)
        self.layout().addWidget(VerticalSeparator(self))
        self.layout().addLayout(pred_settings_layout, 1)
        self.layout().addWidget(VerticalSeparator(self))
        self.layout().addLayout(group_3, 1)

    @staticmethod
    def _get_default_layout(title=""):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title
        setting = QtWidgets.QLabel(title)
        setting.setFont(TitleFont(bold=False))
        setting.setAlignment(Qt.AlignCenter)
        layout.addWidget(setting)

        return layout

    def connect_settings(self, plot_widget):
        pass

    def _get_layout_1(self):
        layout_1 = self._get_default_layout(title="Placeholder")
        return layout_1

    def _get_pred_settings_layout(self):
        layout_2 = self._get_default_layout(title="Prediction Settings")

        # Slider for controlling pred. overlap
        data_per_pred_lab = QtWidgets.QLabel("Data/prediction")
        slider = ListHorizontalSliderWithLabels()
        l = QtWidgets.QHBoxLayout()
        l.addWidget(data_per_pred_lab), l.addWidget(slider)
        layout_2.addLayout(l), layout_2.setAlignment(Qt.AlignTop)

        # Set dictionary mapping to important widgets
        pred_settings = {
            "data_per_pred_slider": slider
        }

        return layout_2, pred_settings

    def _get_layout_3(self):
        layout_3 = self._get_default_layout(title="Visualization Settings")
        return layout_3
