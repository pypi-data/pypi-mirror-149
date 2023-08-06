# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import main_window_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1235, 960)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/images/ctid-logo.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.action_preferences = QAction(MainWindow)
        self.action_preferences.setObjectName(u"action_preferences")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.common_group = QGroupBox(self.centralwidget)
        self.common_group.setObjectName(u"common_group")
        self.common_group.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.common_group.sizePolicy().hasHeightForWidth())
        self.common_group.setSizePolicy(sizePolicy1)
        self.common_group.setSizeIncrement(QSize(0, 0))
        self.common_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.gridLayout = QGridLayout(self.common_group)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_23 = QLabel(self.common_group)
        self.label_23.setObjectName(u"label_23")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)

        self.gridLayout.addWidget(self.label_23, 7, 0, 1, 2)

        self.r_source_spinbox = QSpinBox(self.common_group)
        self.r_source_spinbox.setObjectName(u"r_source_spinbox")
        self.r_source_spinbox.setMaximum(10000000)

        self.gridLayout.addWidget(self.r_source_spinbox, 6, 2, 1, 1)

        self.chip_combo = QComboBox(self.common_group)
        self.chip_combo.addItem("")
        self.chip_combo.addItem("")
        self.chip_combo.addItem("")
        self.chip_combo.setObjectName(u"chip_combo")

        self.gridLayout.addWidget(self.chip_combo, 0, 2, 1, 1)

        self.auto_serial_checkbox = QCheckBox(self.common_group)
        self.auto_serial_checkbox.setObjectName(u"auto_serial_checkbox")

        self.gridLayout.addWidget(self.auto_serial_checkbox, 5, 2, 1, 1)

        self.serial_spinbox = QSpinBox(self.common_group)
        self.serial_spinbox.setObjectName(u"serial_spinbox")
        self.serial_spinbox.setMaximum(16777215)

        self.gridLayout.addWidget(self.serial_spinbox, 4, 2, 1, 1)

        self.sensor_type_combo = QComboBox(self.common_group)
        self.sensor_type_combo.setObjectName(u"sensor_type_combo")
        self.sensor_type_combo.setEditable(False)

        self.gridLayout.addWidget(self.sensor_type_combo, 2, 2, 1, 1)

        self.label_10 = QLabel(self.common_group)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 2)

        self.label_9 = QLabel(self.common_group)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 2)

        self.r_load_spinbox = QSpinBox(self.common_group)
        self.r_load_spinbox.setObjectName(u"r_load_spinbox")
        self.r_load_spinbox.setMaximum(10000000)

        self.gridLayout.addWidget(self.r_load_spinbox, 7, 2, 1, 1)

        self.mfg_combo = QComboBox(self.common_group)
        self.mfg_combo.addItem("")
        self.mfg_combo.setObjectName(u"mfg_combo")

        self.gridLayout.addWidget(self.mfg_combo, 1, 2, 1, 1)

        self.label_11 = QLabel(self.common_group)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_3 = QLabel(self.common_group)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)

        self.label_24 = QLabel(self.common_group)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font)

        self.gridLayout.addWidget(self.label_24, 6, 0, 1, 2)

        self.label_5 = QLabel(self.common_group)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 2)

        self.model_lineEdit = QLineEdit(self.common_group)
        self.model_lineEdit.setObjectName(u"model_lineEdit")

        self.gridLayout.addWidget(self.model_lineEdit, 3, 2, 1, 1)


        self.verticalLayout.addWidget(self.common_group)

        self.param_group = QGroupBox(self.centralwidget)
        self.param_group.setObjectName(u"param_group")
        sizePolicy.setHeightForWidth(self.param_group.sizePolicy().hasHeightForWidth())
        self.param_group.setSizePolicy(sizePolicy)
        self.param_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.param_group.setFlat(False)

        self.verticalLayout.addWidget(self.param_group)

        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.load_template_btn = QPushButton(self.centralwidget)
        self.load_template_btn.setObjectName(u"load_template_btn")

        self.horizontalLayout_1.addWidget(self.load_template_btn)

        self.save_template_btn = QPushButton(self.centralwidget)
        self.save_template_btn.setObjectName(u"save_template_btn")

        self.horizontalLayout_1.addWidget(self.save_template_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.read_btn = QPushButton(self.centralwidget)
        self.read_btn.setObjectName(u"read_btn")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.read_btn.sizePolicy().hasHeightForWidth())
        self.read_btn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.read_btn)

        self.reprogram_after_cal_btn = QPushButton(self.centralwidget)
        self.reprogram_after_cal_btn.setObjectName(u"reprogram_after_cal_btn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.reprogram_after_cal_btn.sizePolicy().hasHeightForWidth())
        self.reprogram_after_cal_btn.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.reprogram_after_cal_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.program_btn = QPushButton(self.centralwidget)
        self.program_btn.setObjectName(u"program_btn")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.program_btn.sizePolicy().hasHeightForWidth())
        self.program_btn.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.program_btn)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy5)
        font1 = QFont()
        font1.setFamily(u"Droid Sans Mono")
        self.plainTextEdit.setFont(font1)
        self.plainTextEdit.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.plainTextEdit.setFocusPolicy(Qt.NoFocus)
        self.plainTextEdit.setStyleSheet(u"background-color: black; color: white")
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.plainTextEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1235, 21))
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.chip_combo, self.mfg_combo)
        QWidget.setTabOrder(self.mfg_combo, self.sensor_type_combo)
        QWidget.setTabOrder(self.sensor_type_combo, self.serial_spinbox)
        QWidget.setTabOrder(self.serial_spinbox, self.auto_serial_checkbox)
        QWidget.setTabOrder(self.auto_serial_checkbox, self.r_source_spinbox)
        QWidget.setTabOrder(self.r_source_spinbox, self.r_load_spinbox)
        QWidget.setTabOrder(self.r_load_spinbox, self.load_template_btn)
        QWidget.setTabOrder(self.load_template_btn, self.save_template_btn)

        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menuEdit.addAction(self.actionPreferences)
        self.menu_Help.addAction(self.action_About)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CTid\u00ae Programmer", None))
        self.action_preferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
#if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.common_group.setTitle(QCoreApplication.translate("MainWindow", u"Common Information", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Test Load Impedance", None))
        self.r_source_spinbox.setSuffix(QCoreApplication.translate("MainWindow", u" \u03a9", None))
        self.chip_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Auto Detect", None))
        self.chip_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"ATtiny9", None))
        self.chip_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"ATtiny10", None))

        self.auto_serial_checkbox.setText(QCoreApplication.translate("MainWindow", u"Automatically Select Serial Number", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Sensor Type", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Serial Number", None))
        self.r_load_spinbox.setSuffix(QCoreApplication.translate("MainWindow", u" \u03a9", None))
        self.mfg_combo.setItemText(0, "")

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Microchip", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Manufacturer", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Sensor Impedance", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Model Name", None))
        self.param_group.setTitle(QCoreApplication.translate("MainWindow", u"Sensor Parameters", None))
        self.load_template_btn.setText(QCoreApplication.translate("MainWindow", u"Load Template", None))
        self.save_template_btn.setText(QCoreApplication.translate("MainWindow", u"Save as Template", None))
        self.read_btn.setText(QCoreApplication.translate("MainWindow", u"Read", None))
        self.reprogram_after_cal_btn.setText(QCoreApplication.translate("MainWindow", u"Reprogram after Cal", None))
        self.program_btn.setText(QCoreApplication.translate("MainWindow", u"Program", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

