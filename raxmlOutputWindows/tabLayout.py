# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabLayout.ui'
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

class Ui_tabLayout(object):
    def setupUi(self, tabLayout):
        tabLayout.setObjectName(_fromUtf8("tabLayout"))
        tabLayout.resize(359, 247)
        tabLayout.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(tabLayout)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.unweightedTab = QtGui.QWidget()
        self.unweightedTab.setObjectName(_fromUtf8("unweightedTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.unweightedTab)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.unweightedImage = QtGui.QLabel(self.unweightedTab)
        self.unweightedImage.setText(_fromUtf8(""))
        self.unweightedImage.setObjectName(_fromUtf8("unweightedImage"))
        self.horizontalLayout_3.addWidget(self.unweightedImage)
        self.tabWidget.addTab(self.unweightedTab, _fromUtf8(""))
        self.weightedTab = QtGui.QWidget()
        self.weightedTab.setObjectName(_fromUtf8("weightedTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.weightedTab)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.weightedImage = QtGui.QLabel(self.weightedTab)
        self.weightedImage.setText(_fromUtf8(""))
        self.weightedImage.setObjectName(_fromUtf8("weightedImage"))
        self.horizontalLayout_2.addWidget(self.weightedImage)
        self.tabWidget.addTab(self.weightedTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        tabLayout.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(tabLayout)
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
        tabLayout.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(tabLayout)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        tabLayout.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(tabLayout)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(tabLayout)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.actionUnweightedPNG = QtGui.QAction(tabLayout)
        self.actionUnweightedPNG.setObjectName(_fromUtf8("actionUnweightedPNG"))
        self.actionWeightedPNG = QtGui.QAction(tabLayout)
        self.actionWeightedPNG.setObjectName(_fromUtf8("actionWeightedPNG"))
        self.actionWeightedPDF = QtGui.QAction(tabLayout)
        self.actionWeightedPDF.setObjectName(_fromUtf8("actionWeightedPDF"))
        self.actionUnweightedPDF = QtGui.QAction(tabLayout)
        self.actionUnweightedPDF.setObjectName(_fromUtf8("actionUnweightedPDF"))
        self.menuUnweighted.addAction(self.actionUnweightedPNG)
        self.menuUnweighted.addAction(self.actionUnweightedPDF)
        self.menuWeighted.addAction(self.actionWeightedPNG)
        self.menuWeighted.addAction(self.actionWeightedPDF)
        self.menuExport.addAction(self.menuUnweighted.menuAction())
        self.menuExport.addAction(self.menuWeighted.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(tabLayout)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(tabLayout)

    def retranslateUi(self, tabLayout):
        tabLayout.setWindowTitle(_translate("tabLayout", "Main Window", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unweightedTab), _translate("tabLayout", "Unweighted", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.weightedTab), _translate("tabLayout", "Weighted", None))
        self.menuFile.setTitle(_translate("tabLayout", "File", None))
        self.menuExport.setTitle(_translate("tabLayout", "Export...", None))
        self.menuUnweighted.setTitle(_translate("tabLayout", "Unweighted", None))
        self.menuWeighted.setTitle(_translate("tabLayout", "Weighted", None))
        self.actionPNG.setText(_translate("tabLayout", "PNG", None))
        self.actionPDF.setText(_translate("tabLayout", "PDF", None))
        self.actionUnweightedPNG.setText(_translate("tabLayout", "PNG", None))
        self.actionWeightedPNG.setText(_translate("tabLayout", "PNG", None))
        self.actionWeightedPDF.setText(_translate("tabLayout", "PDF", None))
        self.actionUnweightedPDF.setText(_translate("tabLayout", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tabLayout = QtGui.QMainWindow()
    ui = Ui_tabLayout()
    ui.setupUi(tabLayout)
    tabLayout.show()
    sys.exit(app.exec_())

