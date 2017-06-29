# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allTreesLayout.ui'
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

class Ui_allTrees(object):
    def setupUi(self, allTrees):
        allTrees.setObjectName(_fromUtf8("allTrees"))
        allTrees.resize(503, 390)
        allTrees.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(allTrees)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allTreesImage = QtGui.QLabel(self.centralwidget)
        self.allTreesImage.setText(_fromUtf8(""))
        self.allTreesImage.setObjectName(_fromUtf8("allTreesImage"))
        self.horizontalLayout.addWidget(self.allTreesImage)
        allTrees.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(allTrees)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 503, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        allTrees.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(allTrees)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        allTrees.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(allTrees)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(allTrees)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.menuExport.addAction(self.actionPNG)
        self.menuExport.addAction(self.actionPDF)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(allTrees)
        QtCore.QMetaObject.connectSlotsByName(allTrees)

    def retranslateUi(self, allTrees):
        allTrees.setWindowTitle(_translate("allTrees", "All Trees", None))
        self.menuFile.setTitle(_translate("allTrees", "File", None))
        self.menuExport.setTitle(_translate("allTrees", "Export...", None))
        self.actionPNG.setText(_translate("allTrees", "PNG", None))
        self.actionPDF.setText(_translate("allTrees", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    allTrees = QtGui.QMainWindow()
    ui = Ui_allTrees()
    ui.setupUi(allTrees)
    allTrees.show()
    sys.exit(app.exec_())

