# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bootstrapContractionLayout.ui'
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

class Ui_bootstrapContraction(object):
    def setupUi(self, bootstrapContraction):
        bootstrapContraction.setObjectName(_fromUtf8("bootstrapContraction"))
        bootstrapContraction.resize(340, 286)
        bootstrapContraction.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(bootstrapContraction)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bootstrapContractionImage = QtGui.QLabel(self.centralwidget)
        self.bootstrapContractionImage.setText(_fromUtf8(""))
        self.bootstrapContractionImage.setObjectName(_fromUtf8("bootstrapContractionImage"))
        self.horizontalLayout.addWidget(self.bootstrapContractionImage)
        bootstrapContraction.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(bootstrapContraction)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        bootstrapContraction.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(bootstrapContraction)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        bootstrapContraction.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(bootstrapContraction)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(bootstrapContraction)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(bootstrapContraction)
        QtCore.QMetaObject.connectSlotsByName(bootstrapContraction)

    def retranslateUi(self, bootstrapContraction):
        bootstrapContraction.setWindowTitle(_translate("bootstrapContraction", "Bootstrap Contraction", None))
        self.menuFile.setTitle(_translate("bootstrapContraction", "File", None))
        self.menuExport.setTitle(_translate("bootstrapContraction", "Export...", None))
        self.actionPNG.setText(_translate("bootstrapContraction", "PNG", None))
        self.actionPDF.setText(_translate("bootstrapContraction", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    bootstrapContraction = QtGui.QMainWindow()
    ui = Ui_bootstrapContraction()
    ui.setupUi(bootstrapContraction)
    bootstrapContraction.show()
    sys.exit(app.exec_())

