# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'standardLayout.ui'
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

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(340, 286)
        mainWindow.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.image = QtGui.QLabel(self.centralwidget)
        self.image.setText(_fromUtf8(""))
        self.image.setObjectName(_fromUtf8("image"))
        self.horizontalLayout.addWidget(self.image)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(mainWindow)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(mainWindow)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "Main Window", None))
        self.menuFile.setTitle(_translate("mainWindow", "File", None))
        self.menuExport.setTitle(_translate("mainWindow", "Export...", None))
        self.actionPNG.setText(_translate("mainWindow", "PNG", None))
        self.actionPDF.setText(_translate("mainWindow", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

