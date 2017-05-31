# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_layout.ui'
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
        self.inputFileBtn = QtGui.QPushButton(self.centralwidget)
        self.inputFileBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.inputFileBtn.setObjectName(_fromUtf8("inputFileBtn"))
        self.horizontalLayout_5.addWidget(self.inputFileBtn)
        self.input_file_entry = QtGui.QLineEdit(self.centralwidget)
        self.input_file_entry.setMinimumSize(QtCore.QSize(0, 21))
        self.input_file_entry.setFocusPolicy(QtCore.Qt.TabFocus)
        self.input_file_entry.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.input_file_entry.setObjectName(_fromUtf8("input_file_entry"))
        self.horizontalLayout_5.addWidget(self.input_file_entry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.window_size_label = QtGui.QLabel(self.centralwidget)
        self.window_size_label.setObjectName(_fromUtf8("window_size_label"))
        self.horizontalLayout_3.addWidget(self.window_size_label)
        self.window_size_entry = QtGui.QLineEdit(self.centralwidget)
        self.window_size_entry.setMinimumSize(QtCore.QSize(40, 21))
        self.window_size_entry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.window_size_entry.setFocusPolicy(QtCore.Qt.TabFocus)
        self.window_size_entry.setObjectName(_fromUtf8("window_size_entry"))
        self.horizontalLayout_3.addWidget(self.window_size_entry)
        self.window_offset_label = QtGui.QLabel(self.centralwidget)
        self.window_offset_label.setObjectName(_fromUtf8("window_offset_label"))
        self.horizontalLayout_3.addWidget(self.window_offset_label)
        self.window_offset_entry = QtGui.QLineEdit(self.centralwidget)
        self.window_offset_entry.setMinimumSize(QtCore.QSize(40, 21))
        self.window_offset_entry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.window_offset_entry.setFocusPolicy(QtCore.Qt.TabFocus)
        self.window_offset_entry.setObjectName(_fromUtf8("window_offset_entry"))
        self.horizontalLayout_3.addWidget(self.window_offset_entry)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.outputDirBtn = QtGui.QPushButton(self.centralwidget)
        self.outputDirBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.outputDirBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputDirBtn.setAcceptDrops(False)
        self.outputDirBtn.setAutoFillBackground(False)
        self.outputDirBtn.setObjectName(_fromUtf8("outputDirBtn"))
        self.horizontalLayout_4.addWidget(self.outputDirBtn)
        self.output_dir_entry = QtGui.QLineEdit(self.centralwidget)
        self.output_dir_entry.setMinimumSize(QtCore.QSize(0, 21))
        self.output_dir_entry.setFocusPolicy(QtCore.Qt.TabFocus)
        self.output_dir_entry.setObjectName(_fromUtf8("output_dir_entry"))
        self.horizontalLayout_4.addWidget(self.output_dir_entry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.runBtn = QtGui.QPushButton(self.centralwidget)
        self.runBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.runBtn.setObjectName(_fromUtf8("runBtn"))
        self.horizontalLayout_6.addWidget(self.runBtn)
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
        self.inputFileBtn.setText(_translate("PhylogenicVisualization", "Select Input File", None))
        self.window_size_label.setText(_translate("PhylogenicVisualization", "Window Size:", None))
        self.window_offset_label.setText(_translate("PhylogenicVisualization", "Window Offset:", None))
        self.outputDirBtn.setText(_translate("PhylogenicVisualization", "Select Output Directory", None))
        self.runBtn.setText(_translate("PhylogenicVisualization", "Run", None))
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

