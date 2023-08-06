# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'template_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Template_Dialog(object):
    def setupUi(self, Template_Dialog):
        if not Template_Dialog.objectName():
            Template_Dialog.setObjectName(u"Template_Dialog")
        Template_Dialog.setWindowModality(Qt.ApplicationModal)
        Template_Dialog.resize(809, 530)
        Template_Dialog.setModal(True)
        self.horizontalLayout_2 = QHBoxLayout(Template_Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.template_name_frame = QFrame(Template_Dialog)
        self.template_name_frame.setObjectName(u"template_name_frame")
        self.template_name_frame.setFrameShape(QFrame.StyledPanel)
        self.template_name_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.template_name_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.template_name_frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.template_name_frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout_2.addWidget(self.template_name_frame)

        self.existing_templates_frame = QFrame(Template_Dialog)
        self.existing_templates_frame.setObjectName(u"existing_templates_frame")
        self.existing_templates_frame.setFrameShape(QFrame.StyledPanel)
        self.existing_templates_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.existing_templates_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.existing_templates_frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.listWidget = QListWidget(self.existing_templates_frame)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.verticalLayout.addWidget(self.listWidget)


        self.verticalLayout_2.addWidget(self.existing_templates_frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.buttonBox = QDialogButtonBox(Template_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Open|QDialogButtonBox.Save)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Template_Dialog)
        self.buttonBox.accepted.connect(Template_Dialog.accept)
        self.buttonBox.rejected.connect(Template_Dialog.reject)

        QMetaObject.connectSlotsByName(Template_Dialog)
    # setupUi

    def retranslateUi(self, Template_Dialog):
        Template_Dialog.setWindowTitle(QCoreApplication.translate("Template_Dialog", u"CTid Templates", None))
        self.label_2.setText(QCoreApplication.translate("Template_Dialog", u"New template name:", None))
        self.label.setText(QCoreApplication.translate("Template_Dialog", u"Existing Templates (right click to rename or delete):", None))
    # retranslateUi

