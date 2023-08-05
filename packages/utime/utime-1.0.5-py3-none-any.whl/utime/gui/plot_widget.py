import os
import numpy as np
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from utime.gui.default_fonts import LargeTitleFont
from utime.gui.base_widgets import HorizontalSliderWithLabels

from utime import defaults
defaults.REM[0] = "R"  # Rename for visual purposes in plot


def sys_time_ms():
    return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)


def get_figure(n_channels, pred_fraction=0.4):
    hr = [(1-pred_fraction)/n_channels]*n_channels + [pred_fraction]
    gs = gridspec.GridSpec(1+n_channels, 1, height_ratios=hr)
    figure = plt.figure(num=1, figsize=(21, 7.5))
    axes = [figure.add_subplot(i) for i in gs]
    data_axes = axes[:-1]
    for i in range(len(data_axes)-1):
        data_axes[i].spines['bottom'].set_visible(False)
        data_axes[i+1].spines['top'].set_visible(False)
    pred_ax = axes[-1]
    figure.subplots_adjust(hspace=0, bottom=0.23, top=0.93)
    return figure, data_axes, pred_ax


class SelectionRightClickMenu(QtWidgets.QMenu):
    def __init__(self, plot_widget):
        super(SelectionRightClickMenu, self).__init__(parent=plot_widget)

        # Define and bind actions
        self.delete_action = QtWidgets.QAction('Delete PSG data', parent=self)
        self.delete_action.triggered.connect(plot_widget.delete_psg_data)

        # Add actions
        self.addAction(self.delete_action)


class NoSelectionRightClickMenu(QtWidgets.QMenu):
    def __init__(self, plot_widget):
        super(NoSelectionRightClickMenu, self).__init__(parent=plot_widget)

        # Define and bind actions
        self.restore_action = QtWidgets.QAction('Restore deleted data', parent=self)
        self.restore_action.triggered.connect(plot_widget.restore_deleted_data)

        # Add actions
        self.addAction(self.restore_action)


class DelayedDrawThread(QThread):
    draw_signal = pyqtSignal(bool)

    def __init__(self, draw_delay_ms, parent=None):
        super(DelayedDrawThread, self).__init__(parent)
        if draw_delay_ms <= 50:
            raise NotImplementedError
        self.draw_delay_ms = draw_delay_ms
        self.last_draw_request = None
        self.draw_now = False
        self.draw_psg = False

    def delayed_data_draw(self, draw_psg):
        self.last_draw_request = sys_time_ms()
        self.draw_psg = draw_psg

    def run(self):
        while True:
            if self.last_draw_request:
                t = sys_time_ms()
                if t-self.last_draw_request > self.draw_delay_ms:
                    self.draw_signal.emit(self.draw_psg)
                    self.last_draw_request = None
                    self.draw_psg = False
            self.msleep(20)


class PlotWidget(QtWidgets.QGraphicsView):
    def __init__(self, predictor, vis_settings, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.installEventFilter(self)

        """ PROPERTIES """
        # Store the data to plot
        self.sleep_study = None
        self.sequence = None
        self.pred = {}
        self.sample_rate = None
        self.period_length_sec = None
        self._margin = 0
        self._center_segment = 0
        self._data_per_prediction = 1
        self._valid_data_per_period = None
        self._data_memory = None
        self.ticks = None
        self.xlim = None
        self.ylims = None

        # Store data selection, selected by mouse click-drag-release
        self._mouse_start = None
        self._mouse_start_temp = None
        self._mouse_end = None
        self._mouse_down_time = None
        self._selected_channels = None

        # Reference to the predictor thread started in the main window
        self.predictor = predictor

        # Reference to widget storing and handling updates to settings
        self.settings = vis_settings
        self.signal_color = "black"
        self.separator_color = "darkgray"
        self.pred_colors = defaults.STAGE_COLORS

        """ LAYOUT """
        self.status_label = QtWidgets.QLabel("Data will appear when a model "
                                             "and PSG file has been "
                                             "loaded.....")
        self.status_label.setFont(LargeTitleFont())
        self.status_label.setAlignment(Qt.AlignHCenter)

        # A slider for scrolling through the data
        self.margin_slider, self.segment_slider = self.get_sliders()

        # Add temp. main figure to a Canvas object, hide until data is ready
        self.figure, self.data_axes, self.pred_ax = get_figure(n_channels=1)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.mpl_connect("button_press_event", self.mouse_select_start)
        self.canvas.mpl_connect("button_release_event", self.mouse_select_end)
        self.canvas.hide()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self.get_slider_container())
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # We redraw the canvas with data and predictions only after X ms of
        # no user inputs changing the selected window
        self.draw_thread = DelayedDrawThread(100, self)
        self.draw_thread.draw_signal.connect(self._add_data_and_draw)
        self.draw_thread.start()

    def get_slider_container(self):
        slider_layout = QtWidgets.QVBoxLayout()
        slider_layout.setAlignment(Qt.AlignTop)
        slider_layout.addWidget(self.status_label)
        slider_layout.addWidget(self.margin_slider)
        slider_layout.addWidget(self.segment_slider)
        slider_container = QtWidgets.QWidget()
        slider_container.setLayout(slider_layout)
        slider_container.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                       QtWidgets.QSizePolicy.Maximum)
        return slider_container

    def get_sliders(self):
        kwargs = {"start_hidden": True, "fixed_width": 800}
        margin_slider = HorizontalSliderWithLabels(**kwargs)
        margin_slider.setMinimum(0, label=1)
        margin_slider.slider.valueChanged.connect(self.set_margin)
        margin_slider.setValue(self.margin)
        segment_slider = HorizontalSliderWithLabels(**kwargs)
        segment_slider.setMinimum(0, label=1)
        segment_slider.slider.valueChanged.connect(self.set_window)
        segment_slider.setValue(self.center_segment)
        return margin_slider, segment_slider

    @property
    def axes(self):
        return self.data_axes + [self.pred_ax]

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Left:
                self.slide_window(-1)
            elif key == Qt.Key_Right:
                self.slide_window(1)
            elif key == Qt.Key_Up:
                self.adjust_window(1)
            elif key == Qt.Key_Down:
                self.adjust_window(-1)
            elif key == Qt.Key_Plus:
                self.slide_window(100)
            elif key == Qt.Key_Minus:
                self.slide_window(-100)
            elif key == Qt.Key_4:
                s = self.settings.pred_settings_widgets['data_per_pred_slider']
                s.setValue(s.slider.value() - 1)
            elif key == Qt.Key_6:
                s = self.settings.pred_settings_widgets['data_per_pred_slider']
                s.setValue(s.slider.value() + 1)
            elif key == Qt.Key_S:
                self.save_figure()
        return super().eventFilter(source, event)

    def clear_mouse_selection(self):
        self._mouse_start = None
        self._mouse_end = None
        self._mouse_start_temp = None
        self._selected_channels = None
        self.plot_current()

    def invoke_right_click_menu(self):
        if self._mouse_start and self._mouse_end:
            menu = SelectionRightClickMenu(plot_widget=self)
        else:
            menu = NoSelectionRightClickMenu(plot_widget=self)
            menu.restore_action.setEnabled(
                self._data_memory is not None
            )
        menu.popup(QtGui.QCursor.pos())

    def delete_psg_data(self):
        # 'delete' (set to 0) the data in the specified segment
        start_sec_plot = (self.center_segment - self.margin) * self.period_length_sec
        start_idx_plot = start_sec_plot * self.sample_rate
        start_idx = start_idx_plot + self._mouse_start
        end_idx = start_idx_plot + self._mouse_end
        for i, selected in enumerate(self._selected_channels):
            if selected:
                self.sleep_study.psg[start_idx:end_idx, i] = 0.0

        # Reset and predict again
        self.reset_predictions()
        self.clear_mouse_selection()

    def restore_deleted_data(self):
        if self._data_memory is not None:
            self.sleep_study._psg = self._data_memory
            self._data_memory = None

            # Reset and predict again
            self.reset_predictions()
            self.plot_current()

    def mouse_select_start(self, event):
        if event.button == 3:
            self.invoke_right_click_menu()
        elif event.button == 1:
            if event.xdata is None or event.ydata is None:
                self.clear_mouse_selection()
            else:
                self._mouse_down_time = sys_time_ms()
                self._mouse_start_temp = int(np.floor(event.xdata))
        else:
            pass

    def _click_is_in_selection(self, event):
        """


        Args:
            event:

        Returns:
            (bool) Click was inside the currently selected area. Returns False
                   if no selection is currently made
            (int)  If click was in selection, returns the clicked channel index
                   Else returns None
        """
        no_sel_return = (False, None)
        if self._mouse_end is None:
            # No current selection
            return no_sel_return
        else:
            if event.xdata < self._mouse_start or event.xdata > self._mouse_end:
                # Selection exists, but click was outside selected region
                return no_sel_return
            else:
                ind = self.data_axes.index(event.inaxes)
                return True, ind

    def mouse_select_end(self, event):
        if event.button == 1 and self._mouse_start_temp:
            time = sys_time_ms()
            if time - self._mouse_down_time < 200:
                # Short click. If outside selection, clear, else add/remove
                # channel-wise selections
                in_sel, chan_ind = self._click_is_in_selection(event)
                if not in_sel:
                    self.clear_mouse_selection()
                else:
                    # Invert the clicked channel selection and replot
                    self._selected_channels[chan_ind] = not self._selected_channels[chan_ind]
                    if not np.any(self._selected_channels):
                        self.clear_mouse_selection()
                    self.plot_current()
            else:
                self._mouse_start = self._mouse_start_temp
                self._mouse_end = int(np.floor(event.xdata))
                self._selected_channels = np.ones(self.sequence.n_channels).astype(np.bool)
                if self._mouse_start == self._mouse_end:
                    self.clear_mouse_selection()
                self.plot_current()
        else:
            pass

    @property
    def center_segment(self):
        return self._center_segment

    @center_segment.setter
    def center_segment(self, value):
        if self.sleep_study is None:
            value = self.margin  # Ensure we are within bounds at init time
        else:
            min_ = self.margin
            max_ = self.sleep_study.n_periods - self.margin - 1
            value = min(max(min_, value), max_)
        self._center_segment = value
        self.segment_slider.setValue(value)
        self.plot_current()

    @property
    def data_per_prediction(self):
        return self._data_per_prediction

    @data_per_prediction.setter
    def data_per_prediction(self, value):
        if self.sleep_study is None:
            return
        min_ = 1
        max_ = int(self.sample_rate * self.period_length_sec)
        value = min(max(min_, value), max_)
        self._data_per_prediction = value
        self.reset_predictions()  # TODO: Check if this is the best solution.
        self.plot_current()

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, value):
        min_ = 0
        if self.sleep_study is None:
            max_ = 0
        else:
            max_ = self.sequence.margin
        new_margin = min(max(min_, value), max_)
        if new_margin == self.margin:
            return
        if self.center_segment - new_margin < 0:
            self.center_segment -= self.center_segment - new_margin
        if self.center_segment + new_margin >= self.sleep_study.n_periods:
            self.center_segment = self.sleep_study.n_periods - new_margin - 1
        self._margin = new_margin
        self.margin_slider.setValue(new_margin)
        self.reset_predictions()  # TODO: Check if this is the best solution.
        self.plot_current()

    def draw(self):
        self.canvas.draw()
        self.canvas.show()

    def reset_predictions(self):
        self.predictor.clear_input_queue()
        self.pred = {}

    def set_window(self, value):
        if self.sleep_study is None or self.sequence is None:
            return
        self.center_segment = value

    def set_margin(self, value):
        if self.sleep_study is None or self.sequence is None:
            return
        self.margin = value

    def set_data_per_prediction(self, value):
        if self.sleep_study is None or self.sequence is None:
            return
        self.data_per_prediction = value

    def slide_window(self, change):
        self.set_window(self.center_segment+change)

    def adjust_window(self, change):
        if self.sleep_study is None or self.sequence is None:
            return
        self.margin = self.margin + change

    def add_to_pred_dict(self, id_, pred):
        if self.pred is None:
            return
        if len(pred) != self.margin * 2 + 1:
            # Discord the prediction, the window was changed
            return
        self.pred[id_] = pred
        self.plot_current(draw_psg=False)

    def update_signal(self, sequence, sample_rate, period_length_sec):
        self.sequence = sequence
        self.sleep_study = sequence.pairs[0]
        self._data_memory = self.sleep_study.psg.copy()  # Copy of original
        self.sample_rate = sample_rate
        self.period_length_sec = period_length_sec
        ylims = [
            (np.min(self.sleep_study.psg[..., i]),
             np.max(self.sleep_study.psg[..., i]))
            for i in range(self.sleep_study.psg.shape[-1])
        ]
        self.ylims = [(-np.max(np.abs(y)), np.max(np.abs(y))) for y in ylims]

        n_chans = sequence.n_channels
        if n_chans != len(self.data_axes):
            plt.close(self.figure)
            self.figure, self.data_axes, self.pred_ax = get_figure(n_chans)
            self.canvas.figure = self.figure

        # Set segment slider
        self.segment_slider.setVisible(True)
        self.segment_slider.setMaximum(self.sleep_study.n_periods-1,
                                       label=self.sleep_study.n_periods)

        # Set margin slider
        self.margin_slider.setVisible(True)
        self.margin_slider.setMaximum(self.sequence.margin,
                                      label=self.sequence.margin*2+1)

        # Set segmentation freq slider
        s = self.settings.pred_settings_widgets['data_per_pred_slider']
        max_ = int(self.period_length_sec*self.sample_rate)
        temp = np.arange(1, max_+1)
        s.set_allowed_values_and_target_func(
            allowed_values=temp[np.where(max_ % temp == 0)],
            target_func=self.set_data_per_prediction
        )

        self.reset_predictions()
        self.plot_current()

    def _clear_axes(self, psg, pred):
        if psg:
            for ax in self.data_axes:
                ax.clear()
        if pred:
            self.pred_ax.clear()

    def plot_current(self, draw_psg=True):
        if self.sequence is None or self.sleep_study is None:
            return
        # Show window settings over plot
        s = "{} segments - {} to {}".format(self.margin*2 + 1,
                                            self.center_segment-self.margin+1,
                                            self.center_segment+self.margin+1)
        self.status_label.setText(s)
        self.draw_thread.delayed_data_draw(draw_psg)

    def _add_data_and_draw(self, draw_psg):
        if draw_psg and (self.sequence is None or self.sleep_study is None):
            return
        self._clear_axes(draw_psg, True)
        if draw_psg:
            psg, hyp = self.prepare_data()
            self.plot_psg_data(psg, hyp)
        self.try_plot_pred_data()
        self.finalize_drawing()
        self.draw()

    def prepare_data(self):
        # Get PSG and hyp data to predict on
        margin = self.sequence.margin
        X, y, shift_ind = self.sequence.get_period(self.sleep_study.identifier,
                                                   self.center_segment,
                                                   return_shifted_idx=True,
                                                   margin=margin)
        X, y = self.sequence.process_batch(X, y)  # normalize etc.

        # Extract the actual periods to plot from the larger input window
        shift_diff = shift_ind - self.center_segment
        local_start = (X.shape[1] // 2) - self.margin - shift_diff
        local_end = local_start + (self.margin * 2 + 1)

        # add data to pred queue if not already predicted
        if self.center_segment not in self.pred:
            """
            OBS: We clear the input pred queue before adding the new segment.
            Remove this line to continue running predictions on segments that 
            were in the queue already (eg. continue in background to predict on
            segments quickly glanced over by the user that are no longer 
            displayed)
            """
            self.predictor.clear_input_queue()
            # Add new data to the pred queue
            inds = (self.center_segment, local_start, local_end)
            self.predictor.add_batch_to_queue(inds, X, self.data_per_prediction)
        return X[0, local_start:local_end], y[0, local_start:local_end]

    def plot_psg_data(self, psg, hyp):
        # Plot PSG periods data
        psg_flat = psg.reshape(-1, psg.shape[-1])
        hyp_flat = hyp.flatten()
        xs = np.arange(len(psg_flat))
        for i, (psg_chan, ax) in enumerate(zip(psg_flat.T, self.data_axes)):
            ax.plot(xs, psg_chan, color=self.signal_color, linewidth=1.5)
            ax.axhline(0, linewidth=1, linestyle="-",
                       color=self.separator_color, zorder=-2)

        # Annotate
        d = len(psg[0])
        ticks = [d * i for i in range(self.margin*2+2)]
        stage_positions = [d // 2 + (d * i) for i in range(self.margin*2+1)]
        for t in ticks:
            for ax in self.data_axes:
                ax.axvline(t, linewidth=1, linestyle='-',
                           color=self.separator_color,
                           alpha=0.95, zorder=-1)

        # Set sleep stages above the signal plot
        trans = transforms.blended_transform_factory(self.data_axes[0].transData,
                                                     self.data_axes[0].transAxes)
        labels = [defaults.class_int_to_stage_string[int(y)] for y in hyp_flat]
        colors = [self.pred_colors[y] for y in hyp_flat]
        for sp, lab, col in zip(stage_positions, labels, colors):
            self.data_axes[0].annotate(s=lab, xy=(sp, 1.05), xycoords=trans,
                                       size=max(2.0, 28 - self.margin*0.8),
                                       ha="center", va="bottom", color=col)
        self.ticks = ticks
        self.xlim = (xs[0], xs[-1])

        # Set selected region, if selected
        if self._mouse_start and self._mouse_end:
            for i, ax in enumerate(self.data_axes):
                if self._selected_channels is not None and self._selected_channels[i]:
                    ax.axvspan(self._mouse_start, self._mouse_end,
                               color="gray", alpha=0.4)

    def try_plot_pred_data(self):

        # Check if prediction exists
        pred = self.pred.get(self.center_segment)
        if pred is None:
            # Add this section to the pred queue
            self.pred_ax.annotate(s="Predicting...", fontsize=24,
                                  xy=(0.5, 0.5), va="center", ha="center",
                                  xycoords=self.pred_ax.transAxes)
            return
        pred = pred.reshape(-1, pred.shape[-1])
        axis_length = self.sequence.data_per_period * (self.margin * 2 + 1)
        xs = np.arange(axis_length)
        if pred.shape[0] != axis_length:
            pred = np.repeat(pred, int(axis_length/pred.shape[0]), axis=0)

        # Plot
        self.pred_ax.stackplot(xs, pred.T,
                               labels=[defaults.class_int_to_stage_string[i]
                                       for i in range(5)],
                               colors=self.pred_colors, alpha=0.65)
        self.pred_ax.set_ylim(0, 1)

        # Add legend
        l = self.pred_ax.legend(loc='upper center',
                                bbox_to_anchor=(0.5, -0.455),
                                ncol=5, fontsize=21)
        l.get_frame().set_linewidth(0)

    def finalize_drawing(self):
        # Remove ticks and labels
        for ax, chan in zip(self.data_axes, self.sleep_study.select_channels):
            ax.set_xticklabels([]), ax.set_xticks([])
            ax.set_yticklabels([chan]), ax.set_yticks([0])
            ax.set_xlim(*self.xlim)
        for ax, ylim in zip(self.data_axes, self.ylims):
            ax.set_ylim(*ylim)
        self.pred_ax.set_xlabel("Time (s)", size=22)
        self.pred_ax.set_ylabel("Confidence\nScore", size=22)

        # Set seconds on x-axis of pred axis
        labels = [str(((self.center_segment-self.margin) *
                       self.period_length_sec) +
                      (self.period_length_sec * i))
                  for i in range(self.margin*2+2)]
        self.pred_ax.set_xticks(self.ticks)
        self.pred_ax.set_xticklabels(labels, rotation=45)
        self.pred_ax.set_yticks([0, 0.5, 1.0])
        self.pred_ax.set_yticklabels([0, 0.5, 1.0])
        self.pred_ax.set_xlim(*self.xlim)

        # Ax label size
        for ax in self.axes:
            ax.tick_params(axis='both', which='major', labelsize=12)

    def save_figure(self, dpi=450):
        dialog = QtWidgets.QFileDialog(parent=self)
        file_name, _ = dialog.getSaveFileName()
        ext = os.path.splitext(file_name)[-1].strip(".")
        if not ext:
            file_name += ".png"
        elif ext not in ("png", "pdf"):
            from utime.gui.dialog_boxes import ErrorMessageBox
            box = ErrorMessageBox(parent=self)
            box.show_error("File extension must be .png or "
                           ".pdf (got .{})".format(ext))
        else:
            self.figure.savefig(file_name, dpi=dpi)
