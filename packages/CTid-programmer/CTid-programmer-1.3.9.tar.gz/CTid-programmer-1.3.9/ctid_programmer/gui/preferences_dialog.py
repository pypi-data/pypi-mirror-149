# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Preferences_Dialog(object):
    def setupUi(self, Preferences_Dialog):
        if not Preferences_Dialog.objectName():
            Preferences_Dialog.setObjectName(u"Preferences_Dialog")
        Preferences_Dialog.resize(281, 182)
        self.gridLayout = QGridLayout(Preferences_Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Preferences_Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.increment_spinbox = QSpinBox(Preferences_Dialog)
        self.increment_spinbox.setObjectName(u"increment_spinbox")
        self.increment_spinbox.setMinimum(1)
        self.increment_spinbox.setMaximum(10000)

        self.gridLayout.addWidget(self.increment_spinbox, 1, 1, 1, 1)

        self.station_id_spinbox = QSpinBox(Preferences_Dialog)
        self.station_id_spinbox.setObjectName(u"station_id_spinbox")
        self.station_id_spinbox.setMinimum(0)

        self.gridLayout.addWidget(self.station_id_spinbox, 2, 1, 1, 1)

        self.label_2 = QLabel(Preferences_Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Preferences_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.sn_service_combo = QComboBox(Preferences_Dialog)
        self.sn_service_combo.addItem("")
        self.sn_service_combo.addItem(u"eGauge")
        self.sn_service_combo.setObjectName(u"sn_service_combo")

        self.gridLayout.addWidget(self.sn_service_combo, 0, 1, 1, 1)

        self.label_3 = QLabel(Preferences_Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)


        self.retranslateUi(Preferences_Dialog)
        self.buttonBox.accepted.connect(Preferences_Dialog.accept)
        self.buttonBox.rejected.connect(Preferences_Dialog.reject)

        QMetaObject.connectSlotsByName(Preferences_Dialog)
    # setupUi

    def retranslateUi(self, Preferences_Dialog):
        Preferences_Dialog.setWindowTitle(QCoreApplication.translate("Preferences_Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Preferences_Dialog", u"Serial-number increment", None))
#if QT_CONFIG(tooltip)
        self.station_id_spinbox.setToolTip(QCoreApplication.translate("Preferences_Dialog", u"The serial-number modulo the serial-number increment must equal the station number.", None))
#endif // QT_CONFIG(tooltip)
        self.station_id_spinbox.setPrefix("")
        self.label_2.setText(QCoreApplication.translate("Preferences_Dialog", u"Station id", None))
        self.sn_service_combo.setItemText(0, QCoreApplication.translate("Preferences_Dialog", u"none", None))

        self.label_3.setText(QCoreApplication.translate("Preferences_Dialog", u"Serial-number service to use", None))
    # retranslateUi

