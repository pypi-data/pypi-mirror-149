# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_volt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Param_Volt(object):
    def setupUi(self, Param_Volt):
        if not Param_Volt.objectName():
            Param_Volt.setObjectName(u"Param_Volt")
        Param_Volt.resize(317, 177)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Volt.sizePolicy().hasHeightForWidth())
        Param_Volt.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Param_Volt)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 24, -1, -1)
        self.label_9 = QLabel(Param_Volt)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.scale_spinbox = QDoubleSpinBox(Param_Volt)
        self.scale_spinbox.setObjectName(u"scale_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scale_spinbox.sizePolicy().hasHeightForWidth())
        self.scale_spinbox.setSizePolicy(sizePolicy1)
        self.scale_spinbox.setDecimals(3)
        self.scale_spinbox.setMinimum(-1000000.000000000000000)
        self.scale_spinbox.setMaximum(1000000.000000000000000)

        self.gridLayout.addWidget(self.scale_spinbox, 0, 1, 1, 1)

        self.label_5 = QLabel(Param_Volt)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.offset_spinbox = QDoubleSpinBox(Param_Volt)
        self.offset_spinbox.setObjectName(u"offset_spinbox")
        self.offset_spinbox.setDecimals(3)
        self.offset_spinbox.setMinimum(-1000000.000000000000000)
        self.offset_spinbox.setMaximum(1000000.000000000000000)

        self.gridLayout.addWidget(self.offset_spinbox, 1, 1, 1, 1)

        self.label_10 = QLabel(Param_Volt)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.delay_spinbox = QDoubleSpinBox(Param_Volt)
        self.delay_spinbox.setObjectName(u"delay_spinbox")
        self.delay_spinbox.setDecimals(2)
        self.delay_spinbox.setMinimum(-327.680000000000007)
        self.delay_spinbox.setMaximum(327.670000000000016)

        self.gridLayout.addWidget(self.delay_spinbox, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 42, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        QWidget.setTabOrder(self.scale_spinbox, self.offset_spinbox)
        QWidget.setTabOrder(self.offset_spinbox, self.delay_spinbox)

        self.retranslateUi(Param_Volt)

        QMetaObject.connectSlotsByName(Param_Volt)
    # setupUi

    def retranslateUi(self, Param_Volt):
        self.label_9.setText(QCoreApplication.translate("Param_Volt", u"Scale", None))
        self.scale_spinbox.setSuffix(QCoreApplication.translate("Param_Volt", u" V/V", None))
        self.label_5.setText(QCoreApplication.translate("Param_Volt", u"Offset", None))
        self.offset_spinbox.setSuffix(QCoreApplication.translate("Param_Volt", u" V", None))
        self.label_10.setText(QCoreApplication.translate("Param_Volt", u"Delay", None))
        self.delay_spinbox.setSuffix(QCoreApplication.translate("Param_Volt", u" \u03bcs", None))
        pass
    # retranslateUi

