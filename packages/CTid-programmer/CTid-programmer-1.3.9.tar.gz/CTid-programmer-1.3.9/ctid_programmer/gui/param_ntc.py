# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_ntc.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Param_NTC(object):
    def setupUi(self, Param_NTC):
        if not Param_NTC.objectName():
            Param_NTC.setObjectName(u"Param_NTC")
        Param_NTC.resize(280, 292)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_NTC.sizePolicy().hasHeightForWidth())
        Param_NTC.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Param_NTC)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 24, -1, -1)
        self.groupBox = QGroupBox(Param_NTC)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.ntc_b_lineEdit = QLineEdit(self.groupBox)
        self.ntc_b_lineEdit.setObjectName(u"ntc_b_lineEdit")

        self.gridLayout.addWidget(self.ntc_b_lineEdit, 1, 1, 1, 1)

        self.ntc_a_lineEdit = QLineEdit(self.groupBox)
        self.ntc_a_lineEdit.setObjectName(u"ntc_a_lineEdit")

        self.gridLayout.addWidget(self.ntc_a_lineEdit, 0, 1, 1, 1)

        self.ntc_c_lineEdit = QLineEdit(self.groupBox)
        self.ntc_c_lineEdit.setObjectName(u"ntc_c_lineEdit")

        self.gridLayout.addWidget(self.ntc_c_lineEdit, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(Param_NTC)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setTextFormat(Qt.AutoText)

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.label = QLabel(Param_NTC)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(Param_NTC)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.AutoText)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.ntc_m_lineEdit = QLineEdit(Param_NTC)
        self.ntc_m_lineEdit.setObjectName(u"ntc_m_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ntc_m_lineEdit.sizePolicy().hasHeightForWidth())
        self.ntc_m_lineEdit.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.ntc_m_lineEdit, 0, 1, 1, 1)

        self.ntc_n_lineEdit = QLineEdit(Param_NTC)
        self.ntc_n_lineEdit.setObjectName(u"ntc_n_lineEdit")

        self.gridLayout_2.addWidget(self.ntc_n_lineEdit, 1, 1, 1, 1)

        self.ntc_k_lineEdit = QLineEdit(Param_NTC)
        self.ntc_k_lineEdit.setObjectName(u"ntc_k_lineEdit")

        self.gridLayout_2.addWidget(self.ntc_k_lineEdit, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.ntc_a_lineEdit, self.ntc_b_lineEdit)
        QWidget.setTabOrder(self.ntc_b_lineEdit, self.ntc_c_lineEdit)
        QWidget.setTabOrder(self.ntc_c_lineEdit, self.ntc_m_lineEdit)
        QWidget.setTabOrder(self.ntc_m_lineEdit, self.ntc_n_lineEdit)
        QWidget.setTabOrder(self.ntc_n_lineEdit, self.ntc_k_lineEdit)

        self.retranslateUi(Param_NTC)

        QMetaObject.connectSlotsByName(Param_NTC)
    # setupUi

    def retranslateUi(self, Param_NTC):
        self.groupBox.setTitle(QCoreApplication.translate("Param_NTC", u"Steinhart-Hart Coefficients", None))
        self.label_9.setText(QCoreApplication.translate("Param_NTC", u"A", None))
        self.label_10.setText(QCoreApplication.translate("Param_NTC", u"C", None))
        self.label_5.setText(QCoreApplication.translate("Param_NTC", u"B", None))
        self.label_2.setText(QCoreApplication.translate("Param_NTC", u"<a href=\"https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html\">Look up coefficients</a>", None))
        self.ntc_b_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"[1/K]", None))
        self.ntc_a_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"[1/K]", None))
        self.ntc_c_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"[1/K]", None))
        self.label_4.setText(QCoreApplication.translate("Param_NTC", u"M", None))
        self.label.setText(QCoreApplication.translate("Param_NTC", u"N", None))
        self.label_3.setText(QCoreApplication.translate("Param_NTC", u"K", None))
        self.ntc_m_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"M parameter [V]", None))
        self.ntc_n_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"N parameter [V/\u03a9]", None))
        self.ntc_k_lineEdit.setPlaceholderText(QCoreApplication.translate("Param_NTC", u"K parameter [1/\u03a9]", None))
        pass
    # retranslateUi

