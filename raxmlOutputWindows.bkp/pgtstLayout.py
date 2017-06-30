# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pgtstLayout.ui'
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

class Ui_pgtst(object):
    def setupUi(self, pgtst):
        pgtst.setObjectName(_fromUtf8("pgtst"))
        pgtst.resize(399, 348)
        self.centralwidget = QtGui.QWidget(pgtst)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pgtstImage = QtGui.QLabel(self.centralwidget)
        self.pgtstImage.setText(_fromUtf8(""))
        self.pgtstImage.setObjectName(_fromUtf8("pgtstImage"))
        self.horizontalLayout.addWidget(self.pgtstImage)
        pgtst.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(pgtst)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 399, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        pgtst.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(pgtst)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        pgtst.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(pgtst)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(pgtst)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(pgtst)
        QtCore.QMetaObject.connectSlotsByName(pgtst)

    def retranslateUi(self, pgtst):
        pgtst.setWindowTitle(_translate("pgtst", "P(GT | ST)", None))
        self.menuFile.setTitle(_translate("pgtst", "File", None))
        self.menuExport.setTitle(_translate("pgtst", "Export...", None))
        self.actionPNG.setText(_translate("pgtst", "PNG", None))
        self.actionPDF.setText(_translate("pgtst", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    pgtst = QtGui.QMainWindow()
    ui = Ui_pgtst()
    ui.setupUi(pgtst)
    pgtst.show()
    sys.exit(app.exec_())

