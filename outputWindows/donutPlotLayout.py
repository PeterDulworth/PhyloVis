# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'donutPlotLayout.ui'
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

class Ui_donutPlot(object):
    def setupUi(self, donutPlot):
        donutPlot.setObjectName(_fromUtf8("donutPlot"))
        donutPlot.resize(340, 286)
        donutPlot.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(donutPlot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.donutPlotImage = QtGui.QLabel(self.centralwidget)
        self.donutPlotImage.setText(_fromUtf8(""))
        self.donutPlotImage.setObjectName(_fromUtf8("donutPlotImage"))
        self.horizontalLayout.addWidget(self.donutPlotImage)
        donutPlot.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(donutPlot)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        donutPlot.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(donutPlot)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        donutPlot.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(donutPlot)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(donutPlot)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(donutPlot)
        QtCore.QMetaObject.connectSlotsByName(donutPlot)

    def retranslateUi(self, donutPlot):
        donutPlot.setWindowTitle(_translate("donutPlot", "Donut Plot", None))
        self.menuFile.setTitle(_translate("donutPlot", "File", None))
        self.menuExport.setTitle(_translate("donutPlot", "Export...", None))
        self.actionPNG.setText(_translate("donutPlot", "PNG", None))
        self.actionPDF.setText(_translate("donutPlot", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    donutPlot = QtGui.QMainWindow()
    ui = Ui_donutPlot()
    ui.setupUi(donutPlot)
    donutPlot.show()
    sys.exit(app.exec_())

