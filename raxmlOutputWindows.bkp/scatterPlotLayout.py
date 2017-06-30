# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scatterPlotLayout.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_scatterPlot(object):
    def setupUi(self, scatterPlot):
        scatterPlot.setObjectName(_fromUtf8("scatterPlot"))
        scatterPlot.resize(422, 327)
        scatterPlot.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(scatterPlot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scatterPlotImage = QtGui.QLabel(self.centralwidget)
        self.scatterPlotImage.setText(_fromUtf8(""))
        self.scatterPlotImage.setObjectName(_fromUtf8("scatterPlotImage"))
        self.horizontalLayout.addWidget(self.scatterPlotImage)
        scatterPlot.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(scatterPlot)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        scatterPlot.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(scatterPlot)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        scatterPlot.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(scatterPlot)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(scatterPlot)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(scatterPlot)
        QtCore.QMetaObject.connectSlotsByName(scatterPlot)

    def retranslateUi(self, scatterPlot):
        scatterPlot.setWindowTitle(_translate("scatterPlot", "Scatter Plot", None))
        self.menuFile.setTitle(_translate("scatterPlot", "File", None))
        self.menuExport.setTitle(_translate("scatterPlot", "Export...", None))
        self.actionPNG.setText(_translate("scatterPlot", "PNG", None))
        self.actionPDF.setText(_translate("scatterPlot", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    scatterPlot = QtGui.QMainWindow()
    ui = Ui_scatterPlot()
    ui.setupUi(scatterPlot)
    scatterPlot.show()
    sys.exit(app.exec_())

