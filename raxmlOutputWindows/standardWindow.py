from PyQt4 import QtGui, QtCore
import sys, os
import matplotlib

matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5 import SubplotToolQt
from matplotlib.backends.backend_qt5 import UiSubplotTool
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets
import numpy as np


# class CustomToolbar(NavigationToolbar):
#     def __init__(self, canvas_, parent_):
#         self.toolitems = (
#             ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
#             ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
#             ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
#             (None, None, None, None),
#             ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
#             ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
#             (None, None, None, None),
#             ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
#             ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
#             ('Custom Button', 'custom btn hover txt', 'warning', 'configure_subplots'),
#             )
#         # self.toolitems = [t for t in self.toolitems if
#         #              t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
#         NavigationToolbar.__init__(self, canvas_, parent_)
#
#     def _icon(self, name):
#         print name
#         pm = QtGui.QPixmap(os.path.join(self.basedir, name))
#         if hasattr(pm, 'setDevicePixelRatio'):
#             pm.setDevicePixelRatio(self.canvas._dpi_ratio)
#         return QtGui.QIcon(pm)
#
#     def pan(self):
#         NavigationToolbar.pan(self)
#         self.mode = "henlo!"  # <--- whatever you want to replace "pan/zoom" goes here
#         self.set_message(self.mode)

class CustomUiSubplotTool(UiSubplotTool):
    def __init__(self, *args, **kwargs):
        super(UiSubplotTool, self).__init__(*args, **kwargs)
        self.setObjectName('SubplotTool')
        self.resize(450, 265)

        gbox = QtWidgets.QGridLayout(self)
        self.setLayout(gbox)

        # groupbox borders
        groupbox = QtWidgets.QGroupBox('Borders', self)
        gbox.addWidget(groupbox, 6, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout(groupbox)
        self.verticalLayout.setSpacing(0)

        # slider top
        self.hboxtop = QtWidgets.QHBoxLayout()
        self.labeltop = QtWidgets.QLabel('Top', self)
        self.labeltop.setMinimumSize(QtCore.QSize(50, 0))
        self.labeltop.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.slidertop = QtWidgets.QSlider(self)
        self.slidertop.setMouseTracking(False)
        self.slidertop.setProperty("value", 0)
        self.slidertop.setOrientation(QtCore.Qt.Horizontal)
        self.slidertop.setInvertedAppearance(False)
        self.slidertop.setInvertedControls(False)
        self.slidertop.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slidertop.setTickInterval(100)

        self.topvalue = QtWidgets.QLabel('0', self)
        self.topvalue.setMinimumSize(QtCore.QSize(30, 0))
        self.topvalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(self.hboxtop)
        self.hboxtop.addWidget(self.labeltop)
        self.hboxtop.addWidget(self.slidertop)
        self.hboxtop.addWidget(self.topvalue)

        # slider bottom
        hboxbottom = QtWidgets.QHBoxLayout()
        labelbottom = QtWidgets.QLabel('Bottom', self)
        labelbottom.setMinimumSize(QtCore.QSize(50, 0))
        labelbottom.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.sliderbottom = QtWidgets.QSlider(self)
        self.sliderbottom.setMouseTracking(False)
        self.sliderbottom.setProperty("value", 0)
        self.sliderbottom.setOrientation(QtCore.Qt.Horizontal)
        self.sliderbottom.setInvertedAppearance(False)
        self.sliderbottom.setInvertedControls(False)
        self.sliderbottom.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderbottom.setTickInterval(100)

        self.bottomvalue = QtWidgets.QLabel('0', self)
        self.bottomvalue.setMinimumSize(QtCore.QSize(30, 0))
        self.bottomvalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(hboxbottom)
        hboxbottom.addWidget(labelbottom)
        hboxbottom.addWidget(self.sliderbottom)
        hboxbottom.addWidget(self.bottomvalue)

        # slider left
        hboxleft = QtWidgets.QHBoxLayout()
        labelleft = QtWidgets.QLabel('Left', self)
        labelleft.setMinimumSize(QtCore.QSize(50, 0))
        labelleft.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.sliderleft = QtWidgets.QSlider(self)
        self.sliderleft.setMouseTracking(False)
        self.sliderleft.setProperty("value", 0)
        self.sliderleft.setOrientation(QtCore.Qt.Horizontal)
        self.sliderleft.setInvertedAppearance(False)
        self.sliderleft.setInvertedControls(False)
        self.sliderleft.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderleft.setTickInterval(100)

        self.leftvalue = QtWidgets.QLabel('0', self)
        self.leftvalue.setMinimumSize(QtCore.QSize(30, 0))
        self.leftvalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(hboxleft)
        hboxleft.addWidget(labelleft)
        hboxleft.addWidget(self.sliderleft)
        hboxleft.addWidget(self.leftvalue)

        # slider right
        hboxright = QtWidgets.QHBoxLayout()
        self.labelright = QtWidgets.QLabel('Right', self)
        self.labelright.setMinimumSize(QtCore.QSize(50, 0))
        self.labelright.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.sliderright = QtWidgets.QSlider(self)
        self.sliderright.setMouseTracking(False)
        self.sliderright.setProperty("value", 0)
        self.sliderright.setOrientation(QtCore.Qt.Horizontal)
        self.sliderright.setInvertedAppearance(False)
        self.sliderright.setInvertedControls(False)
        self.sliderright.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderright.setTickInterval(100)

        self.rightvalue = QtWidgets.QLabel('0', self)
        self.rightvalue.setMinimumSize(QtCore.QSize(30, 0))
        self.rightvalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(hboxright)
        hboxright.addWidget(self.labelright)
        hboxright.addWidget(self.sliderright)
        hboxright.addWidget(self.rightvalue)

        # groupbox spacings
        groupbox = QtWidgets.QGroupBox('Spacings', self)
        gbox.addWidget(groupbox, 7, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout(groupbox)
        self.verticalLayout.setSpacing(0)

        # slider hspace
        hboxhspace = QtWidgets.QHBoxLayout()
        self.labelhspace = QtWidgets.QLabel('hspace', self)
        self.labelhspace.setMinimumSize(QtCore.QSize(50, 0))
        self.labelhspace.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.sliderhspace = QtWidgets.QSlider(self)
        self.sliderhspace.setMouseTracking(False)
        self.sliderhspace.setProperty("value", 0)
        self.sliderhspace.setOrientation(QtCore.Qt.Horizontal)
        self.sliderhspace.setInvertedAppearance(False)
        self.sliderhspace.setInvertedControls(False)
        self.sliderhspace.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderhspace.setTickInterval(100)

        self.hspacevalue = QtWidgets.QLabel('0', self)
        self.hspacevalue.setMinimumSize(QtCore.QSize(30, 0))
        self.hspacevalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(hboxhspace)
        hboxhspace.addWidget(self.labelhspace)
        hboxhspace.addWidget(self.sliderhspace)
        hboxhspace.addWidget(self.hspacevalue)  # slider hspace

        # slider wspace
        hboxwspace = QtWidgets.QHBoxLayout()
        self.labelwspace = QtWidgets.QLabel('wspace', self)
        self.labelwspace.setMinimumSize(QtCore.QSize(50, 0))
        self.labelwspace.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.sliderwspace = QtWidgets.QSlider(self)
        self.sliderwspace.setMouseTracking(False)
        self.sliderwspace.setProperty("value", 0)
        self.sliderwspace.setOrientation(QtCore.Qt.Horizontal)
        self.sliderwspace.setInvertedAppearance(False)
        self.sliderwspace.setInvertedControls(False)
        self.sliderwspace.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderwspace.setTickInterval(100)

        self.wspacevalue = QtWidgets.QLabel('0', self)
        self.wspacevalue.setMinimumSize(QtCore.QSize(30, 0))
        self.wspacevalue.setAlignment(
                QtCore.Qt.AlignRight |
                QtCore.Qt.AlignTrailing |
                QtCore.Qt.AlignVCenter)

        self.verticalLayout.addLayout(hboxwspace)
        hboxwspace.addWidget(self.labelwspace)
        hboxwspace.addWidget(self.sliderwspace)
        hboxwspace.addWidget(self.wspacevalue)

        # button bar
        hbox2 = QtWidgets.QHBoxLayout()
        gbox.addLayout(hbox2, 8, 0, 1, 1)
        self.tightlayout = QtWidgets.QPushButton('Tight Layout', self)
        spacer = QtWidgets.QSpacerItem(
                5, 20, QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum)
        self.resetbutton = QtWidgets.QPushButton('Reset', self)
        self.donebutton = QtWidgets.QPushButton('Close', self)
        self.donebutton.setFocus()
        hbox2.addWidget(self.tightlayout)
        hbox2.addItem(spacer)
        hbox2.addWidget(self.resetbutton)
        hbox2.addWidget(self.donebutton)

        self.donebutton.clicked.connect(self.accept)


class CustomSubplotToolQt(SubplotToolQt, CustomUiSubplotTool):
    def __init__(self, targetfig, parent):
        # UiSubplotTool.__init__(self, None)
        CustomUiSubplotTool.__init__(self, None)

        self.targetfig = targetfig
        self.parent = parent
        self.donebutton.clicked.connect(self.close)
        self.resetbutton.clicked.connect(self.reset)
        self.tightlayout.clicked.connect(self.functight)

        # constraints
        self.sliderleft.valueChanged.connect(self.sliderright.setMinimum)
        self.sliderright.valueChanged.connect(self.sliderleft.setMaximum)
        self.sliderbottom.valueChanged.connect(self.slidertop.setMinimum)
        self.slidertop.valueChanged.connect(self.sliderbottom.setMaximum)

        self.defaults = {}
        for attr in ('left', 'bottom', 'right', 'top', 'wspace', 'hspace',):
            val = getattr(self.targetfig.subplotpars, attr)
            self.defaults[attr] = val
            slider = getattr(self, 'slider' + attr)
            txt = getattr(self, attr + 'value')
            slider.setMinimum(0)
            slider.setMaximum(1000)
            slider.setSingleStep(5)
            # do this before hooking up the callbacks
            slider.setSliderPosition(int(val * 1000))
            txt.setText("%.2f" % val)
            slider.valueChanged.connect(getattr(self, 'func' + attr))
        self._setSliderPositions()
        # SubplotToolQt.__init__(self, targetfig, parent)


class Window(QtGui.QMainWindow):
    def __init__(self, fileName, x=0, y=0, scale=1, parent=None):
        super(Window, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.setCentralWidget(self.centralwidget)

        # menubar
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionPNG = QtGui.QAction(self)
        self.actionPDF = QtGui.QAction(self)
        self.actionSaveAs = QtGui.QAction(self)
        self.menuFile.addAction(self.actionSaveAs)
        self.menubar.addAction(self.menuFile.menuAction())

        self.setWindowTitle("Main Window")
        self.menuFile.setTitle("File")
        self.actionSaveAs.setText("Save As...")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.fileName = fileName
        self.x = x
        self.y = y
        self.scale = scale

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.fileName)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)

        # bind export actions
        # self.actionSaveAs.triggered.connect(self.toolbar.save_figure)
        self.actionSaveAs.triggered.connect(self.box)

    def box(self):
        # dia = SubplotToolQt(self.canvas.figure, self.parent)
        dia = CustomSubplotToolQt(self.canvas.figure, self.parent)
        # dia.setWindowIcon(QtGui.QIcon(image))
        dia.exec_()

    def figureBarPlot(self, data, name, title):
        """
            generates bar chart
        """

        numberOfBars = len(data)
        ind = np.arange(numberOfBars)  # the x locations for the groups
        width = .667  # the width of the bars
        ax = self.figure.add_subplot(111)
        colors = [(43.0 / 255.0, 130.0 / 255.0, 188.0 / 255.0), (141.0 / 255.0, 186.0 / 255.0, 87.0 / 255.0), (26.0 / 255.0, 168.0 / 255.0, 192.0 / 255.0), (83.5 / 255.0, 116.5 / 255.0, 44.5 / 255.0)]

        ax.bar(ind, data, width, color=colors)

        plt.title(title, fontsize=15)
        # plt.savefig(name)
        # plt.show()

        self.canvas.draw()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]

        # create an axis
        # ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False)

        # plot data
        # ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    def setBackgroundColor(self, color):
        """
            change background color to white
        """
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def setWindowPosition(self, x, y):
        """
            positions the window relative to the top left corner of the screen (px)
        """
        self.move(x, y)

    def setWindowSize(self, x, y):
        """
            sets size of window
        """
        self.resize(x, y)

    def closeEvent(self, QCloseEvent):
        self.emit(QtCore.SIGNAL("WINDOW_CLOSED"))

        # def moveEvent(self, QMoveEvent):
        #     print self.fileName, self.pos()


if __name__ == '__main__':
    """
        code is executed if file is run directly -- i.e. not imported
    """

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = Window('../imgs/tree.png', scale=5)
    form.show()
    form.setWindowSize(600, 600)
    form.figureBarPlot([1, 2, 3, 4], 'henlo', 'henlo')
    form.setBackgroundColor(QtCore.Qt.white)

    # and execute the app
    sys.exit(app.exec_())
