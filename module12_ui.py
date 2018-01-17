from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from . import module12_core as m12core
import numpy as np

class Window(QtWidgets.QDialog):
    def __init__(self, mri_data = None):
        super().__init__()

        self.mri_data = mri_data
        self.xx = []
        self.yy = []
        self.zz = []

        self.figure = Figure()
        self.figure2 = Figure()

        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtWidgets.QPushButton('Get Oblique Image')
        self.button.clicked.connect(self.getobliqueimage)

        self.sliderx = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderx.setFocusPolicy(Qt.StrongFocus)
        self.sliderx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderx.setMaximum(360)
        self.sliderx.setMinimum(0)
        self.sliderx.setTickInterval(10)
        self.sliderx.setSingleStep(1)
        self.sliderx.setValue(0)
        self.sliderx.valueChanged.connect(self.plot)

        self.slidery = QtWidgets.QSlider(Qt.Horizontal)
        self.slidery.setFocusPolicy(Qt.StrongFocus)
        self.slidery.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slidery.setMaximum(360)
        self.slidery.setMinimum(0)
        self.slidery.setTickInterval(10)
        self.slidery.setSingleStep(1)
        self.slidery.setValue(0)
        self.slidery.valueChanged.connect(self.plot)

        self.sliderz = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderz.setFocusPolicy(Qt.StrongFocus)
        self.sliderz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderz.setMaximum(360)
        self.sliderz.setMinimum(0)
        self.sliderz.setTickInterval(10)
        self.sliderz.setSingleStep(1)
        self.sliderz.setValue(0)
        self.sliderz.valueChanged.connect(self.plot)

        self.transbox = QtWidgets.QSpinBox()
        self.transbox.setMaximum(10000)
        self.transbox.setMinimum(-10000)
        self.transbox.setValue(0)
        self.transbox.valueChanged.connect(self.plot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.button)
        layout.addWidget(self.sliderx)
        layout.addWidget(self.slidery)
        layout.addWidget(self.sliderz)
        layout.addWidget(self.transbox)

        self.setLayout(layout)
        self.plot()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        sliderxval = self.sliderx.value()
        slideryval = self.slidery.value()
        sliderzval = self.sliderz.value()
        transboxval = self.transbox.value()

        self.xx, self.yy, self.zz = m12core.transrotateplane(self.mri_data, sliderxval, slideryval, sliderzval, transboxval)

        self.figure.clear()
        # create an axis
        ax = self.figure.gca(projection='3d', azim=250)

        # plot data
        ax.plot_surface(self.xx, self.yy, self.zz)


        # refresh canvas
        self.canvas.draw()

    def getobliqueimage(self):
        interpolatedimage = m12core.interpolatemri(self.mri_data, self.xx, self.yy, self.zz)
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.imshow(interpolatedimage,cmap='gray', aspect='equal')

        self.canvas2.draw()

