# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msRobinsonFouldsLayout.ui'
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

class Ui_msRobinsonFoulds(object):
    def setupUi(self, msRobinsonFoulds):
        msRobinsonFoulds.setObjectName(_fromUtf8("msRobinsonFoulds"))
        msRobinsonFoulds.resize(359, 247)
        msRobinsonFoulds.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(msRobinsonFoulds)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.unweightedTab = QtGui.QWidget()
        self.unweightedTab.setObjectName(_fromUtf8("unweightedTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.unweightedTab)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.msRobinsonFouldsUnweightedImage = QtGui.QLabel(self.unweightedTab)
        self.msRobinsonFouldsUnweightedImage.setText(_fromUtf8(""))
        self.msRobinsonFouldsUnweightedImage.setObjectName(_fromUtf8("msRobinsonFouldsUnweightedImage"))
        self.horizontalLayout_3.addWidget(self.msRobinsonFouldsUnweightedImage)
        self.tabWidget.addTab(self.unweightedTab, _fromUtf8(""))
        self.weightedTab = QtGui.QWidget()
        self.weightedTab.setObjectName(_fromUtf8("weightedTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.weightedTab)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.msRobinsonFouldsWeightedImage = QtGui.QLabel(self.weightedTab)
        self.msRobinsonFouldsWeightedImage.setText(_fromUtf8(""))
        self.msRobinsonFouldsWeightedImage.setObjectName(_fromUtf8("msRobinsonFouldsWeightedImage"))
        self.horizontalLayout_2.addWidget(self.msRobinsonFouldsWeightedImage)
        self.tabWidget.addTab(self.weightedTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        msRobinsonFoulds.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(msRobinsonFoulds)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 359, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuUnweighted = QtGui.QMenu(self.menuExport)
        self.menuUnweighted.setObjectName(_fromUtf8("menuUnweighted"))
        self.menuWeighted = QtGui.QMenu(self.menuExport)
        self.menuWeighted.setObjectName(_fromUtf8("menuWeighted"))
        msRobinsonFoulds.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(msRobinsonFoulds)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        msRobinsonFoulds.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(msRobinsonFoulds)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(msRobinsonFoulds)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.actionUnweightedPNG = QtGui.QAction(msRobinsonFoulds)
        self.actionUnweightedPNG.setObjectName(_fromUtf8("actionUnweightedPNG"))
        self.actionWeightedPNG = QtGui.QAction(msRobinsonFoulds)
        self.actionWeightedPNG.setObjectName(_fromUtf8("actionWeightedPNG"))
        self.actionWeightedPDF = QtGui.QAction(msRobinsonFoulds)
        self.actionWeightedPDF.setObjectName(_fromUtf8("actionWeightedPDF"))
        self.actionUnweightedPDF = QtGui.QAction(msRobinsonFoulds)
        self.actionUnweightedPDF.setObjectName(_fromUtf8("actionUnweightedPDF"))
        self.menuUnweighted.addAction(self.actionUnweightedPNG)
        self.menuUnweighted.addAction(self.actionUnweightedPDF)
        self.menuWeighted.addAction(self.actionWeightedPNG)
        self.menuWeighted.addAction(self.actionWeightedPDF)
        self.menuExport.addAction(self.menuUnweighted.menuAction())
        self.menuExport.addAction(self.menuWeighted.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(msRobinsonFoulds)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(msRobinsonFoulds)

    def retranslateUi(self, msRobinsonFoulds):
        msRobinsonFoulds.setWindowTitle(_translate("msRobinsonFoulds", "MS Robinson Foulds", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unweightedTab), _translate("msRobinsonFoulds", "Unweighted", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.weightedTab), _translate("msRobinsonFoulds", "Weighted", None))
        self.menuFile.setTitle(_translate("msRobinsonFoulds", "File", None))
        self.menuExport.setTitle(_translate("msRobinsonFoulds", "Export...", None))
        self.menuUnweighted.setTitle(_translate("msRobinsonFoulds", "Unweighted", None))
        self.menuWeighted.setTitle(_translate("msRobinsonFoulds", "Weighted", None))
        self.actionPNG.setText(_translate("msRobinsonFoulds", "PNG", None))
        self.actionPDF.setText(_translate("msRobinsonFoulds", "PDF", None))
        self.actionUnweightedPNG.setText(_translate("msRobinsonFoulds", "PNG", None))
        self.actionWeightedPNG.setText(_translate("msRobinsonFoulds", "PNG", None))
        self.actionWeightedPDF.setText(_translate("msRobinsonFoulds", "PDF", None))
        self.actionUnweightedPDF.setText(_translate("msRobinsonFoulds", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    msRobinsonFoulds = QtGui.QMainWindow()
    ui = Ui_msRobinsonFoulds()
    ui.setupUi(msRobinsonFoulds)
    msRobinsonFoulds.show()
    sys.exit(app.exec_())

