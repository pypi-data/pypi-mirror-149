# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_linear.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Param_Linear(object):
    def setupUi(self, Param_Linear):
        if not Param_Linear.objectName():
            Param_Linear.setObjectName(u"Param_Linear")
        Param_Linear.resize(296, 141)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_Linear.sizePolicy().hasHeightForWidth())
        Param_Linear.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Param_Linear)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 32, -1, -1)
        self.scale_spinbox = QDoubleSpinBox(Param_Linear)
        self.scale_spinbox.setObjectName(u"scale_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scale_spinbox.sizePolicy().hasHeightForWidth())
        self.scale_spinbox.setSizePolicy(sizePolicy1)
        self.scale_spinbox.setDecimals(9)

        self.gridLayout.addWidget(self.scale_spinbox, 1, 1, 1, 1)

        self.offset_spinbox = QDoubleSpinBox(Param_Linear)
        self.offset_spinbox.setObjectName(u"offset_spinbox")
        self.offset_spinbox.setDecimals(9)

        self.gridLayout.addWidget(self.offset_spinbox, 2, 1, 1, 1)

        self.label_9 = QLabel(Param_Linear)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_10 = QLabel(Param_Linear)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)

        self.label_11 = QLabel(Param_Linear)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_5 = QLabel(Param_Linear)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 42, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.delay_spinbox = QDoubleSpinBox(Param_Linear)
        self.delay_spinbox.setObjectName(u"delay_spinbox")
        self.delay_spinbox.setDecimals(2)
        self.delay_spinbox.setMinimum(-327.680000000000007)
        self.delay_spinbox.setMaximum(327.670000000000016)

        self.gridLayout.addWidget(self.delay_spinbox, 3, 1, 1, 1)

        self.unit_comboBox = QComboBox(Param_Linear)
        self.unit_comboBox.setObjectName(u"unit_comboBox")

        self.gridLayout.addWidget(self.unit_comboBox, 0, 1, 1, 1)

        QWidget.setTabOrder(self.scale_spinbox, self.offset_spinbox)
        QWidget.setTabOrder(self.offset_spinbox, self.delay_spinbox)

        self.retranslateUi(Param_Linear)

        QMetaObject.connectSlotsByName(Param_Linear)
    # setupUi

    def retranslateUi(self, Param_Linear):
        self.scale_spinbox.setSuffix(QCoreApplication.translate("Param_Linear", u" V/V", None))
        self.offset_spinbox.setSuffix(QCoreApplication.translate("Param_Linear", u" V", None))
        self.label_9.setText(QCoreApplication.translate("Param_Linear", u"Scale", None))
        self.label_10.setText(QCoreApplication.translate("Param_Linear", u"Delay", None))
        self.label_11.setText(QCoreApplication.translate("Param_Linear", u"Measurement", None))
        self.label_5.setText(QCoreApplication.translate("Param_Linear", u"Offset", None))
        self.delay_spinbox.setSuffix(QCoreApplication.translate("Param_Linear", u" \u03bcs", None))
        pass
    # retranslateUi

