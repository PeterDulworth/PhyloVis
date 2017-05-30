# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/Peter/PycharmProjects/phylogenicsVisualization/gui/gui_layout.ui'
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

class Ui_PhylogenicVisualization(object):
    def setupUi(self, PhylogenicVisualization):
        PhylogenicVisualization.setObjectName(_fromUtf8("PhylogenicVisualization"))
        PhylogenicVisualization.resize(433, 201)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PhylogenicVisualization.sizePolicy().hasHeightForWidth())
        PhylogenicVisualization.setSizePolicy(sizePolicy)
        PhylogenicVisualization.setMinimumSize(QtCore.QSize(433, 201))
        self.centralwidget = QtGui.QWidget(PhylogenicVisualization)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.input_file_label = QtGui.QLabel(self.centralwidget)
        self.input_file_label.setObjectName(_fromUtf8("input_file_label"))
        self.horizontalLayout_5.addWidget(self.input_file_label)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.window_size_label = QtGui.QLabel(self.centralwidget)
        self.window_size_label.setObjectName(_fromUtf8("window_size_label"))
        self.horizontalLayout_3.addWidget(self.window_size_label)
        self.window_size_entry = QtGui.QLineEdit(self.centralwidget)
        self.window_size_entry.setMinimumSize(QtCore.QSize(40, 21))
        self.window_size_entry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.window_size_entry.setObjectName(_fromUtf8("window_size_entry"))
        self.horizontalLayout_3.addWidget(self.window_size_entry)
        self.window_offset_label = QtGui.QLabel(self.centralwidget)
        self.window_offset_label.setObjectName(_fromUtf8("window_offset_label"))
        self.horizontalLayout_3.addWidget(self.window_offset_label)
        self.window_offset_entry = QtGui.QLineEdit(self.centralwidget)
        self.window_offset_entry.setMinimumSize(QtCore.QSize(40, 21))
        self.window_offset_entry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.window_offset_entry.setObjectName(_fromUtf8("window_offset_entry"))
        self.horizontalLayout_3.addWidget(self.window_offset_entry)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.output_directory_label = QtGui.QLabel(self.centralwidget)
        self.output_directory_label.setObjectName(_fromUtf8("output_directory_label"))
        self.horizontalLayout_4.addWidget(self.output_directory_label)
        self.output_directory_entry = QtGui.QLineEdit(self.centralwidget)
        self.output_directory_entry.setObjectName(_fromUtf8("output_directory_entry"))
        self.horizontalLayout_4.addWidget(self.output_directory_entry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.run_btn = QtGui.QPushButton(self.centralwidget)
        self.run_btn.setObjectName(_fromUtf8("run_btn"))
        self.horizontalLayout_6.addWidget(self.run_btn)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_6.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        PhylogenicVisualization.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PhylogenicVisualization)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 433, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        PhylogenicVisualization.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PhylogenicVisualization)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PhylogenicVisualization.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(PhylogenicVisualization)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(PhylogenicVisualization)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PhylogenicVisualization)
        QtCore.QMetaObject.connectSlotsByName(PhylogenicVisualization)

    def retranslateUi(self, PhylogenicVisualization):
        PhylogenicVisualization.setWindowTitle(_translate("PhylogenicVisualization", "Phylogenic Visualization", None))
        self.input_file_label.setText(_translate("PhylogenicVisualization", "Input File:", None))
        self.window_size_label.setText(_translate("PhylogenicVisualization", "Window Size:", None))
        self.window_offset_label.setText(_translate("PhylogenicVisualization", "Window Offset:", None))
        self.output_directory_label.setText(_translate("PhylogenicVisualization", "Output Directory:", None))
        self.run_btn.setText(_translate("PhylogenicVisualization", "Run", None))
        self.menuFile.setTitle(_translate("PhylogenicVisualization", "File", None))
        self.actionSave.setText(_translate("PhylogenicVisualization", "Save", None))
        self.actionSave_As.setText(_translate("PhylogenicVisualization", "Save As", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PhylogenicVisualization = QtGui.QMainWindow()
    ui = Ui_PhylogenicVisualization()
    ui.setupUi(PhylogenicVisualization)
    PhylogenicVisualization.show()
    sys.exit(app.exec_())

