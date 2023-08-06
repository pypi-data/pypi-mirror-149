# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_ct.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Param_CT(object):
    def setupUi(self, Param_CT):
        if not Param_CT.objectName():
            Param_CT.setObjectName(u"Param_CT")
        Param_CT.resize(387, 444)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Param_CT.sizePolicy().hasHeightForWidth())
        Param_CT.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Param_CT)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 24, -1, -1)
        self.label_9 = QLabel(Param_CT)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.current_spinbox = QDoubleSpinBox(Param_CT)
        self.current_spinbox.setObjectName(u"current_spinbox")
        self.current_spinbox.setDecimals(1)
        self.current_spinbox.setMaximum(6553.500000000000000)

        self.gridLayout.addWidget(self.current_spinbox, 0, 1, 1, 1)

        self.label_5 = QLabel(Param_CT)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.size_spinbox = QDoubleSpinBox(Param_CT)
        self.size_spinbox.setObjectName(u"size_spinbox")
        self.size_spinbox.setDecimals(1)
        self.size_spinbox.setMaximum(6553.500000000000000)

        self.gridLayout.addWidget(self.size_spinbox, 1, 1, 1, 1)

        self.label_10 = QLabel(Param_CT)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.output_voltage_spinbox = QDoubleSpinBox(Param_CT)
        self.output_voltage_spinbox.setObjectName(u"output_voltage_spinbox")
        self.output_voltage_spinbox.setDecimals(5)
        self.output_voltage_spinbox.setMaximum(0.655350000000000)
        self.output_voltage_spinbox.setSingleStep(0.001000000000000)

        self.gridLayout.addWidget(self.output_voltage_spinbox, 2, 1, 1, 1)

        self.label_23 = QLabel(Param_CT)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)

        self.gridLayout.addWidget(self.label_23, 3, 0, 1, 1)

        self.phase_spinbox = QDoubleSpinBox(Param_CT)
        self.phase_spinbox.setObjectName(u"phase_spinbox")
        self.phase_spinbox.setMinimum(-20.480000000000000)
        self.phase_spinbox.setMaximum(20.469999999999999)

        self.gridLayout.addWidget(self.phase_spinbox, 3, 1, 1, 1)

        self.label_11 = QLabel(Param_CT)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)

        self.voltage_temp_coeff_spinbox = QDoubleSpinBox(Param_CT)
        self.voltage_temp_coeff_spinbox.setObjectName(u"voltage_temp_coeff_spinbox")
        self.voltage_temp_coeff_spinbox.setDecimals(0)
        self.voltage_temp_coeff_spinbox.setMinimum(-640.000000000000000)
        self.voltage_temp_coeff_spinbox.setMaximum(635.000000000000000)
        self.voltage_temp_coeff_spinbox.setSingleStep(5.000000000000000)

        self.gridLayout.addWidget(self.voltage_temp_coeff_spinbox, 4, 1, 1, 1)

        self.label_12 = QLabel(Param_CT)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)

        self.phase_temp_coeff_spinbox = QDoubleSpinBox(Param_CT)
        self.phase_temp_coeff_spinbox.setObjectName(u"phase_temp_coeff_spinbox")
        self.phase_temp_coeff_spinbox.setDecimals(1)
        self.phase_temp_coeff_spinbox.setMinimum(-64.000000000000000)
        self.phase_temp_coeff_spinbox.setMaximum(63.500000000000000)
        self.phase_temp_coeff_spinbox.setSingleStep(0.500000000000000)

        self.gridLayout.addWidget(self.phase_temp_coeff_spinbox, 5, 1, 1, 1)

        self.label_21 = QLabel(Param_CT)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)

        self.gridLayout.addWidget(self.label_21, 6, 0, 1, 1)

        self.bias_voltage_spinbox = QDoubleSpinBox(Param_CT)
        self.bias_voltage_spinbox.setObjectName(u"bias_voltage_spinbox")
        self.bias_voltage_spinbox.setDecimals(3)
        self.bias_voltage_spinbox.setMinimum(-32.768000000000001)
        self.bias_voltage_spinbox.setMaximum(32.767000000000003)
        self.bias_voltage_spinbox.setSingleStep(0.001000000000000)

        self.gridLayout.addWidget(self.bias_voltage_spinbox, 6, 1, 1, 1)

        self.label_13 = QLabel(Param_CT)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)
        self.label_13.setFont(font)
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_13, 7, 0, 1, 1)

        self.params = QGridLayout()
        self.params.setObjectName(u"params")
        self.calp3 = QDoubleSpinBox(Param_CT)
        self.calp3.setObjectName(u"calp3")
        self.calp3.setMinimum(-2.560000000000000)
        self.calp3.setMaximum(2.540000000000000)
        self.calp3.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calp3, 3, 3, 1, 1)

        self.label_14 = QLabel(Param_CT)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.params.addWidget(self.label_14, 1, 1, 1, 1)

        self.calv3 = QDoubleSpinBox(Param_CT)
        self.calv3.setObjectName(u"calv3")
        self.calv3.setMinimum(-2.560000000000000)
        self.calv3.setMaximum(2.540000000000000)
        self.calv3.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calv3, 3, 2, 1, 1)

        self.label_17 = QLabel(Param_CT)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.params.addWidget(self.label_17, 4, 1, 1, 1)

        self.calv2 = QDoubleSpinBox(Param_CT)
        self.calv2.setObjectName(u"calv2")
        self.calv2.setMinimum(-2.560000000000000)
        self.calv2.setMaximum(2.540000000000000)
        self.calv2.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calv2, 2, 2, 1, 1)

        self.calv1 = QDoubleSpinBox(Param_CT)
        self.calv1.setObjectName(u"calv1")
        self.calv1.setMinimum(-2.560000000000000)
        self.calv1.setMaximum(2.540000000000000)
        self.calv1.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calv1, 1, 2, 1, 1)

        self.calp2 = QDoubleSpinBox(Param_CT)
        self.calp2.setObjectName(u"calp2")
        self.calp2.setMinimum(-2.560000000000000)
        self.calp2.setMaximum(2.540000000000000)
        self.calp2.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calp2, 2, 3, 1, 1)

        self.label_16 = QLabel(Param_CT)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.params.addWidget(self.label_16, 3, 1, 1, 1)

        self.label_15 = QLabel(Param_CT)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.params.addWidget(self.label_15, 2, 1, 1, 1)

        self.calp4 = QDoubleSpinBox(Param_CT)
        self.calp4.setObjectName(u"calp4")
        self.calp4.setMinimum(-2.560000000000000)
        self.calp4.setMaximum(2.540000000000000)
        self.calp4.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calp4, 4, 3, 1, 1)

        self.label_20 = QLabel(Param_CT)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.params.addWidget(self.label_20, 0, 1, 1, 1)

        self.calp1 = QDoubleSpinBox(Param_CT)
        self.calp1.setObjectName(u"calp1")
        self.calp1.setMinimum(-2.560000000000000)
        self.calp1.setMaximum(2.540000000000000)
        self.calp1.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calp1, 1, 3, 1, 1)

        self.calv4 = QDoubleSpinBox(Param_CT)
        self.calv4.setObjectName(u"calv4")
        self.calv4.setMinimum(-2.560000000000000)
        self.calv4.setMaximum(2.540000000000000)
        self.calv4.setSingleStep(0.020000000000000)

        self.params.addWidget(self.calv4, 4, 2, 1, 1)

        self.label_18 = QLabel(Param_CT)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.params.addWidget(self.label_18, 0, 2, 1, 1)

        self.label_19 = QLabel(Param_CT)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)

        self.params.addWidget(self.label_19, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.params.addItem(self.horizontalSpacer, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.params, 8, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 9, 0, 1, 1)

        QWidget.setTabOrder(self.current_spinbox, self.size_spinbox)
        QWidget.setTabOrder(self.size_spinbox, self.output_voltage_spinbox)
        QWidget.setTabOrder(self.output_voltage_spinbox, self.phase_spinbox)
        QWidget.setTabOrder(self.phase_spinbox, self.voltage_temp_coeff_spinbox)
        QWidget.setTabOrder(self.voltage_temp_coeff_spinbox, self.phase_temp_coeff_spinbox)
        QWidget.setTabOrder(self.phase_temp_coeff_spinbox, self.calv1)
        QWidget.setTabOrder(self.calv1, self.calp1)
        QWidget.setTabOrder(self.calp1, self.calv2)
        QWidget.setTabOrder(self.calv2, self.calp2)
        QWidget.setTabOrder(self.calp2, self.calv3)
        QWidget.setTabOrder(self.calv3, self.calp3)
        QWidget.setTabOrder(self.calp3, self.calv4)
        QWidget.setTabOrder(self.calv4, self.calp4)

        self.retranslateUi(Param_CT)

        QMetaObject.connectSlotsByName(Param_CT)
    # setupUi

    def retranslateUi(self, Param_CT):
        self.label_9.setText(QCoreApplication.translate("Param_CT", u"Rated Current", None))
        self.current_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" A", None))
        self.label_5.setText(QCoreApplication.translate("Param_CT", u"Size", None))
        self.size_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" mm", None))
        self.label_10.setText(QCoreApplication.translate("Param_CT", u"Output Voltage at Rated Current", None))
        self.output_voltage_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" V", None))
        self.label_23.setText(QCoreApplication.translate("Param_CT", u"Output Phase at Rated Current", None))
        self.phase_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" \u00b0", None))
        self.label_11.setText(QCoreApplication.translate("Param_CT", u"Voltage Temperature Coefficient", None))
        self.voltage_temp_coeff_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" ppm/\u00b0C", None))
        self.label_12.setText(QCoreApplication.translate("Param_CT", u"Phase Temperature Coefficient", None))
        self.phase_temp_coeff_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" m\u00b0/\u00b0C", None))
        self.label_21.setText(QCoreApplication.translate("Param_CT", u"Bias voltage", None))
        self.bias_voltage_spinbox.setSuffix(QCoreApplication.translate("Param_CT", u" mV", None))
        self.label_13.setText(QCoreApplication.translate("Param_CT", u"Calibration Table", None))
        self.calp3.setSuffix(QCoreApplication.translate("Param_CT", u" \u00b0", None))
        self.label_14.setText(QCoreApplication.translate("Param_CT", u"1.5%", None))
        self.calv3.setSuffix(QCoreApplication.translate("Param_CT", u" %", None))
        self.label_17.setText(QCoreApplication.translate("Param_CT", u"50%", None))
        self.calv2.setSuffix(QCoreApplication.translate("Param_CT", u" %", None))
        self.calv1.setSuffix(QCoreApplication.translate("Param_CT", u" %", None))
        self.calp2.setSuffix(QCoreApplication.translate("Param_CT", u" \u00b0", None))
        self.label_16.setText(QCoreApplication.translate("Param_CT", u"15%", None))
        self.label_15.setText(QCoreApplication.translate("Param_CT", u"5%", None))
        self.calp4.setSuffix(QCoreApplication.translate("Param_CT", u" \u00b0", None))
        self.label_20.setText(QCoreApplication.translate("Param_CT", u"Level", None))
        self.calp1.setSuffix(QCoreApplication.translate("Param_CT", u" \u00b0", None))
        self.calv4.setSuffix(QCoreApplication.translate("Param_CT", u" %", None))
        self.label_18.setText(QCoreApplication.translate("Param_CT", u"Voltage Adjustment", None))
        self.label_19.setText(QCoreApplication.translate("Param_CT", u"Phase Adjustment", None))
        pass
    # retranslateUi

