# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'heatMapLayout.ui'
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

class Ui_heatMap(object):
    def setupUi(self, heatMap):
        heatMap.setObjectName(_fromUtf8("heatMap"))
        heatMap.resize(422, 327)
        heatMap.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(heatMap)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.heatMapImage = QtGui.QLabel(self.centralwidget)
        self.heatMapImage.setText(_fromUtf8(""))
        self.heatMapImage.setObjectName(_fromUtf8("heatMapImage"))
        self.horizontalLayout.addWidget(self.heatMapImage)
        heatMap.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(heatMap)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        heatMap.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(heatMap)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        heatMap.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(heatMap)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(heatMap)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(heatMap)
        QtCore.QMetaObject.connectSlotsByName(heatMap)

    def retranslateUi(self, heatMap):
        heatMap.setWindowTitle(_translate("heatMap", "Heat Map", None))
        self.menuFile.setTitle(_translate("heatMap", "File", None))
        self.menuExport.setTitle(_translate("heatMap", "Export...", None))
        self.actionPNG.setText(_translate("heatMap", "PNG", None))
        self.actionPDF.setText(_translate("heatMap", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    heatMap = QtGui.QMainWindow()
    ui = Ui_heatMap()
    ui.setupUi(heatMap)
    heatMap.show()
    sys.exit(app.exec_())

