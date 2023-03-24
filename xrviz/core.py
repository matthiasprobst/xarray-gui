import argparse
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QSlider,
                             QDoubleSpinBox, QTextEdit, QPushButton)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ._version import __version__


class XArrayData1DPlotter(QMainWindow):
    """Main window to plot a one-dimensional xr.DataArray"""

    def __init__(self, da: xr.DataArray):
        super().__init__()
        self.da = da

        ymin = float(self.da.min())
        ymax = float(self.da.max())
        opt_step = (ymax - ymin) / 100
        self.current_coord_name = sorted(self.da.coords.keys())[0]

        self.setWindowTitle("Xr.DataArray Plotter")
        self.setGeometry(100, 100, 800, 480)

        # Create the matplotlib figure and canvas
        self.figure = plt.figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Create horizontal layouts for the sliders and text edit widgets and add them to them
        top_layout = QVBoxLayout()

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(QLabel("ymin: "))

        ydelta = ymax - ymin

        self.qspin_ymin = QDoubleSpinBox()
        self.qspin_ymin.setMinimum(ymin - 1000 * ydelta)
        self.qspin_ymin.setMaximum(ymax + 1000 * ydelta)
        self.qspin_ymin.setValue(ymin)
        self.qspin_ymin.setSingleStep(opt_step)
        self.qspin_ymin.valueChanged.connect(self.on_ylim_changed)
        hlayout1.addWidget(self.qspin_ymin)

        self.qspin_ymax = QDoubleSpinBox()
        self.qspin_ymax.setMinimum(ymin - 1000 * ydelta)
        self.qspin_ymax.setMaximum(ymax + 1000 * ydelta)
        self.qspin_ymax.setValue(ymax)
        self.qspin_ymax.setSingleStep(opt_step)
        self.qspin_ymax.valueChanged.connect(self.on_ylim_changed)

        hlayout1.addWidget(QLabel("ymax: "))
        hlayout1.addWidget(self.qspin_ymax)

        self.ylim_reset_btn = QPushButton("reset")
        hlayout1.addWidget(self.ylim_reset_btn)
        self.ylim_reset_btn.clicked.connect(self.on_ylim_reset_clicked)

        # Create horizontal sliders and set their ranges
        # Slider positions are in percent!
        hlayout2 = QHBoxLayout()
        slider1 = QSlider(self)
        slider1.setOrientation(1)  # Set orientation to horizontal
        slider1.setRange(0, 100)
        # set step of slider:
        slider1.setSingleStep(1)
        slider2 = QSlider(self)
        slider2.setOrientation(1)  # Set orientation to horizontal
        slider2.setRange(0, 100)
        slider2.setSingleStep(1)
        slider2.setSliderPosition(100)

        slider1.sliderReleased.connect(self.on_xlim_changed)
        slider2.sliderReleased.connect(self.on_xlim_changed)

        self.slider1 = slider1
        self.slider2 = slider2

        hlayout2.addWidget(slider1)
        hlayout2.addWidget(slider2)

        self.xlim_reset_btn = QPushButton("reset")
        hlayout2.addWidget(self.xlim_reset_btn)
        self.xlim_reset_btn.clicked.connect(self.on_xlim_reset_clicked)

        top_layout.addLayout(hlayout1)
        top_layout.addLayout(hlayout2)

        # Create a horizontal layout for the plotting widget and add it to the main layout
        canvas_layout = QHBoxLayout()
        canvas_layout.addWidget(self.canvas)

        # Create a vertical layout for the dropdown menu and sliders and add them to it
        dropdown_layout = QVBoxLayout()
        dropdown_layout.addWidget(QLabel("Dropdown: "))
        self.combo_box_coords = QComboBox(self)
        self.combo_box_coords.addItems(da.coords.keys())
        self.combo_box_coords.currentIndexChanged.connect(self.on_combobox_changed)
        dropdown_layout.addWidget(self.combo_box_coords)

        # Create a vertical layout for the widgets on the left side and add them to it
        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)
        left_layout.addLayout(canvas_layout)
        left_layout.addLayout(dropdown_layout)
        # left_layout.addStretch(1)

        right_layout = QVBoxLayout()
        self.qtextedit_attributes = QTextEdit("Right Layout")
        self.qtextedit_attributes.setEnabled(False)
        right_layout.addWidget(self.qtextedit_attributes)

        # Create a vertical layout for the main window and add the left and bottom layouts to it
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Create a widget for the main window and set the main layout as its layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_plot()

    @property
    def xmin(self):
        """Return the minimum value of the current coordinate"""
        self.da[self.current_coord_name].min()
        return float(self.da[self.current_coord_name].min())

    @property
    def xmax(self):
        """Return the maximum value of the current coordinate"""
        self.da[self.current_coord_name].min()
        return float(self.da[self.current_coord_name].max())

    @property
    def ymin(self):
        """Return the minimum value of the data array"""
        return self.da.min()

    @property
    def ymax(self):
        """Return the maximum value of the data array"""
        return self.da.max()

    def update_attributes(self):
        """Update the text edit widget with the attributes of the data array"""
        # clear text edit widgets:
        self.qtextedit_attributes.clear()
        self.qtextedit_attributes.append(f'dtype: {self.da.dtype}')
        self.qtextedit_attributes.append(f'shape: {self.da.shape}')
        self.qtextedit_attributes.append('\nAttributes:')
        self.qtextedit_attributes.append('-----------')
        for k, v in self.da.attrs.items():
            self.qtextedit_attributes.append(f'{k}: {v}')

    def update_plot(self):
        """Update the plot with the data array"""
        # Plot the data on the graph
        # clear the figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.da.plot(ax=ax, x=self.current_coord_name)
        ax.set_title("Data")
        self.on_xlim_changed()
        self.on_ylim_changed()

        # Refresh the canvas to show the graph
        self.canvas.draw()

        self.update_attributes()

    def on_combobox_changed(self):
        """Callback function for the combobox"""
        self.current_coord_name = self.combo_box_coords.currentText()
        self.update_plot()

    def on_xlim_changed(self):
        """Callback function for the slider2"""
        delta = self.xmax - self.xmin
        if self.slider1.value() == 100:
            self.slider1.setSliderPosition(99)
        if self.slider2.value() == 0:
            self.slider2.setSliderPosition(1)
        xlim_min = self.xmin + self.slider1.value() / 100 * delta
        xlim_max = self.xmax - (100 - self.slider2.value()) / 100 * delta
        if xlim_min >= xlim_max:
            self.slider2.setSliderPosition(self.slider1.value() + 1)
            xlim_max = self.xmax - (100 - self.slider2.value()) / 100 * delta
        self.xlim = (xlim_min, xlim_max)
        self.figure.gca().set_xlim(self.xlim)
        # self.update_plot()
        self.canvas.draw()

    def on_ylim_reset_clicked(self):
        """Callback function for the reset button"""
        self.qspin_ymin.setValue(self.ymin)
        self.qspin_ymax.setValue(self.ymax)
        self.on_ylim_changed()

    def on_xlim_reset_clicked(self):
        """Callback function for the reset button"""
        self.slider1.setSliderPosition(0)
        self.slider2.setSliderPosition(100)
        self.on_xlim_changed()

    def on_ylim_changed(self):
        """Callback function for the spinbox changing the y limits"""
        delta = self.ymax - self.ymin

        ylim_min = self.qspin_ymin.value()
        ylim_max = self.qspin_ymax.value()

        if ylim_min >= ylim_max:
            self.qspin_ymax.setValue(self.qspin_ymin.value() + delta / 100)

        self.figure.gca().set_ylim((ylim_min, ylim_max))
        # self.update_plot()
        self.canvas.draw()


def start(da):
    """Start the application"""
    app = QApplication(sys.argv)
    window = XArrayData1DPlotter(da)
    window.show()
    sys.exit(app.exec_())


def test():
    """Test the application"""
    # create a sample xr.DataArray with dimensions time:
    da_iteration = xr.DataArray(np.linspace(0, 1, 11), dims='iteration')
    da_time = xr.DataArray(np.linspace(0, 13, 11), dims='iteration')
    da = xr.DataArray(np.random.rand(11, ),
                      dims='iteration',
                      coords={'iteration': da_iteration,
                              'time': da_time},
                      attrs={'title': 'Test Data', })

    da.to_netcdf('test.nc')

    start(da)

    pathlib.Path('test.nc').unlink()


def cli():
    """main command line interface function"""
    parser = argparse.ArgumentParser(description='xrviz command line interface')
    parser.add_argument('-V', '--version',
                        action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-f', '--file', type=str, help='path to netcdf file')
    args = parser.parse_args()
    if args.file:
        da = xr.open_dataarray(args.file)
        start(da)


if __name__ == "__main__":
    test()
