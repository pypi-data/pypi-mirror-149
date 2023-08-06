from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from utime import __version__
from utime.gui.dialog_boxes import YesNoDialog
from utime.gui.plot_widget import PlotWidget


class DeepSleepMainWindow(QtWidgets.QMainWindow):
    """
    Placeholder
    """
    def __init__(self, state, predictor):
        """
        Args:
            parent:
        """
        super(DeepSleepMainWindow, self).__init__(parent=None)
        self.setWindowTitle(f"DeepSleep v.{__version__}")
        self.setMinimumSize(1000, 400)

        # Set model selector dock widget
        from utime.gui.model_selector import ModelSelector
        model_selector = QtWidgets.QDockWidget("Model and Data Selector", self)
        model_selector.setMinimumWidth(350)
        self.model_selector_widget = ModelSelector(state, parent=self)
        model_selector.setWidget(self.model_selector_widget)
        model_selector.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable)
        model_selector.setAllowedAreas(Qt.LeftDockWidgetArea |
                                       Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, model_selector)

        # Set visualization attribute dock widget
        from utime.gui.settings import Settings
        vis_attrs = QtWidgets.QDockWidget("Settings", self)
        vis_attrs.setMinimumHeight(200)
        vis_attrs_widget = Settings(parent=self)
        self.visualization_attributes_widget = vis_attrs_widget
        vis_attrs.setWidget(self.visualization_attributes_widget)
        vis_attrs.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable)
        vis_attrs.setAllowedAreas(Qt.TopDockWidgetArea |
                                  Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, vis_attrs)

        # Set central widget
        self.plot_widget = PlotWidget(predictor, vis_attrs_widget, parent=self)
        self.setCentralWidget(self.plot_widget)

        # Connect settings to plot widget
        self.visualization_attributes_widget.connect_settings(
            self.plot_widget
        )

    def wheelEvent(self, event):
        self.plot_widget.slide_window(1 if event.angleDelta().y() < 0 else -1)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Q or key == Qt.Key_Escape:
            answer = YesNoDialog().ask("Are you sure you want to quit?", "yes")
            if answer:
                self.close()
