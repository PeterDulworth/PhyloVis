# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'circleGraphLayout.ui'
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

class Ui_circleGraph(object):
    def setupUi(self, circleGraph):
        circleGraph.setObjectName(_fromUtf8("circleGraph"))
        circleGraph.resize(420, 366)
        circleGraph.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(circleGraph)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.circleGraphImage = QtGui.QLabel(self.centralwidget)
        self.circleGraphImage.setText(_fromUtf8(""))
        self.circleGraphImage.setObjectName(_fromUtf8("circleGraphImage"))
        self.horizontalLayout.addWidget(self.circleGraphImage)
        circleGraph.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(circleGraph)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        circleGraph.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(circleGraph)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        circleGraph.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(circleGraph)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(circleGraph)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.actionTXT = QtGui.QAction(circleGraph)
        self.actionTXT.setObjectName(_fromUtf8("actionTXT"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(circleGraph)
        QtCore.QMetaObject.connectSlotsByName(circleGraph)

    def retranslateUi(self, circleGraph):
        circleGraph.setWindowTitle(_translate("circleGraph", "MainWindow", None))
        self.menuFile.setTitle(_translate("circleGraph", "File", None))
        self.menuExport.setTitle(_translate("circleGraph", "Export...", None))
        self.actionPNG.setText(_translate("circleGraph", "PNG", None))
        self.actionPDF.setText(_translate("circleGraph", "PDF", None))
        self.actionTXT.setText(_translate("circleGraph", "TXT", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    circleGraph = QtGui.QMainWindow()
    ui = Ui_circleGraph()
    ui.setupUi(circleGraph)
    circleGraph.show()
    sys.exit(app.exec_())

