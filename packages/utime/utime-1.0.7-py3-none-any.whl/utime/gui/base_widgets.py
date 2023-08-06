from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from utime.gui.default_fonts import TitleFont
import numpy as np


class HorizontalSeparator(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(HorizontalSeparator, self).__init__(parent)
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Sunken)


class VerticalSeparator(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(VerticalSeparator, self).__init__(parent)
        self.setFrameShape(self.VLine)
        self.setFrameShadow(self.Sunken)


class AttributesWidget(QtWidgets.QWidget):
    def __init__(self, buttom, parent=None):
        super(AttributesWidget, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        # Main label
        self.title_label = QtWidgets.QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(TitleFont())

        # Status label, may be upadted
        self.status_label = QtWidgets.QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)

        # Insert into widget
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.status_label)
        self.layout().addWidget(buttom, 0, Qt.AlignHCenter)

        # Attributes layout
        self.attribute_widget = None
        self.update_attribute_widget(attributes={}, remove_previous=False)

    def update_attribute_widget(self, attributes, remove_previous=True):
        if remove_previous:
            # Clear potential old widget
            self.attribute_widget.setParent(None)
        attr_widget = QtWidgets.QWidget()
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignTop)
        for label_name, value in attributes.items():
            label_name = label_name[0].upper() + label_name[1:].replace("_", " ")
            l = QtWidgets.QLabel(text=f"{label_name}:")
            f = QtWidgets.QLabel(text=f'{value or "None"}')
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.addWidget(l), h_layout.addWidget(f)
            l.setAlignment(Qt.AlignLeft), f.setAlignment(Qt.AlignRight)
            vertical_layout.addLayout(h_layout)
        attr_widget.setLayout(vertical_layout)
        self.layout().addWidget(attr_widget)
        self.attribute_widget = attr_widget


class HorizontalSliderWithLabels(QtWidgets.QWidget):
    def __init__(self,
                 minimum=1,
                 maximum=100,
                 fixed_width=None,
                 start_hidden=False,
                 parent=None):
        super(HorizontalSliderWithLabels, self).__init__(parent=parent)
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.low_label = QtWidgets.QLabel()
        self.high_label = QtWidgets.QLabel()

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        if start_hidden:
            self.setVisible(False)
        if fixed_width:
            self.slider.setFixedWidth(fixed_width)

        # Create layout for the segment slider
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.setAlignment(Qt.AlignHCenter)
        slider_layout.addWidget(self.low_label, 0, Qt.AlignRight)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.high_label, 0, Qt.AlignLeft)
        self.setLayout(slider_layout)

    def setValue(self, value):
        self.slider.setValue(value)

    def setMinimum(self, minimum, label=None):
        self.slider.setMinimum(minimum)
        val = label or minimum
        self.low_label.setText(str(val))

    def setMaximum(self, maximum, label=None):
        self.slider.setMaximum(maximum)
        val = label or maximum
        self.high_label.setText(str(val))


class ListHorizontalSliderWithLabels(HorizontalSliderWithLabels):
    def __init__(self, allowed_values=None):
        super().__init__()
        self.setMaximum(2, " ")
        self.setEnabled(False)
        self._allowed_values = None
        self._func = None
        if allowed_values is not None:
            self.set_allowed_values(allowed_values)
        self.slider.valueChanged.connect(self._redir_value_changed)

    def _redir_value_changed(self, value):
        mapped_val = self._allowed_values[value-1]
        self.low_label.setText(str(mapped_val))
        self._func(mapped_val)

    def set_allowed_values_and_target_func(self, allowed_values, target_func):
        if isinstance(allowed_values, (tuple, list, np.ndarray)):
            self._allowed_values = allowed_values
        else:
            raise ValueError("'allowed_values' must be None or a sequence.")
        if not callable(target_func):
            raise ValueError("'target_func' must be a callable.")

        self._func = target_func
        self.setMinimum(1, self._allowed_values[0])
        self.setMaximum(len(self._allowed_values), " ")
        self.setValue(1)
        self.setEnabled(True)
