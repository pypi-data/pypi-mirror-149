# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_pulse.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Param_Pulse(object):
    def setupUi(self, Param_Pulse):
        if not Param_Pulse.objectName():
            Param_Pulse.setObjectName(u"Param_Pulse")
        Param_Pulse.resize(343, 161)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Pulse.sizePolicy().hasHeightForWidth())
        Param_Pulse.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Param_Pulse)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 24, -1, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.threshold_spinbox = QDoubleSpinBox(Param_Pulse)
        self.threshold_spinbox.setObjectName(u"threshold_spinbox")
        self.threshold_spinbox.setDecimals(2)
        self.threshold_spinbox.setMaximum(655.350000000000023)

        self.gridLayout.addWidget(self.threshold_spinbox, 0, 1, 1, 1)

        self.label_9 = QLabel(Param_Pulse)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_5 = QLabel(Param_Pulse)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_10 = QLabel(Param_Pulse)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_23 = QLabel(Param_Pulse)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)

        self.gridLayout.addWidget(self.label_23, 3, 0, 1, 1)

        self.debounce_spinbox = QDoubleSpinBox(Param_Pulse)
        self.debounce_spinbox.setObjectName(u"debounce_spinbox")
        self.debounce_spinbox.setDecimals(0)
        self.debounce_spinbox.setMaximum(255.000000000000000)
        self.debounce_spinbox.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.debounce_spinbox, 2, 1, 1, 1)

        self.hysteresis_spinbox = QDoubleSpinBox(Param_Pulse)
        self.hysteresis_spinbox.setObjectName(u"hysteresis_spinbox")
        self.hysteresis_spinbox.setDecimals(2)
        self.hysteresis_spinbox.setMaximum(655.350000000000023)

        self.gridLayout.addWidget(self.hysteresis_spinbox, 1, 1, 1, 1)

        self.edge_comboBox = QComboBox(Param_Pulse)
        self.edge_comboBox.addItem("")
        self.edge_comboBox.addItem("")
        self.edge_comboBox.addItem("")
        self.edge_comboBox.setObjectName(u"edge_comboBox")

        self.gridLayout.addWidget(self.edge_comboBox, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        QWidget.setTabOrder(self.threshold_spinbox, self.hysteresis_spinbox)
        QWidget.setTabOrder(self.hysteresis_spinbox, self.debounce_spinbox)

        self.retranslateUi(Param_Pulse)

        QMetaObject.connectSlotsByName(Param_Pulse)
    # setupUi

    def retranslateUi(self, Param_Pulse):
        self.threshold_spinbox.setSuffix(QCoreApplication.translate("Param_Pulse", u" mV", None))
        self.label_9.setText(QCoreApplication.translate("Param_Pulse", u"Threshold", None))
        self.label_5.setText(QCoreApplication.translate("Param_Pulse", u"Hysteresis", None))
        self.label_10.setText(QCoreApplication.translate("Param_Pulse", u"Debounce time", None))
        self.label_23.setText(QCoreApplication.translate("Param_Pulse", u"Trigger edge", None))
        self.debounce_spinbox.setSuffix(QCoreApplication.translate("Param_Pulse", u" ms", None))
        self.hysteresis_spinbox.setSuffix(QCoreApplication.translate("Param_Pulse", u" mV", None))
        self.edge_comboBox.setItemText(0, QCoreApplication.translate("Param_Pulse", u"rising", None))
        self.edge_comboBox.setItemText(1, QCoreApplication.translate("Param_Pulse", u"falling", None))
        self.edge_comboBox.setItemText(2, QCoreApplication.translate("Param_Pulse", u"rising and falling", None))

        pass
    # retranslateUi

