# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/fetargo/Kursach/Modules/security.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Security(object):
    def setupUi(self, Security):
        Security.setObjectName("Security")
        Security.resize(350, 485)
        self.centralwidget = QtWidgets.QWidget(Security)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 8, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.labelObjectName = QtWidgets.QLabel(self.centralwidget)
        self.labelObjectName.setText("")
        self.labelObjectName.setObjectName("labelObjectName")
        self.gridLayout.addWidget(self.labelObjectName, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.labelOwnerName = QtWidgets.QLabel(self.centralwidget)
        self.labelOwnerName.setText("")
        self.labelOwnerName.setObjectName("labelOwnerName")
        self.gridLayout.addWidget(self.labelOwnerName, 4, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 10, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSetSec = QtWidgets.QPushButton(self.centralwidget)
        self.btnSetSec.setObjectName("btnSetSec")
        self.horizontalLayout_2.addWidget(self.btnSetSec)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        Security.setCentralWidget(self.centralwidget)

        self.retranslateUi(Security)
        QtCore.QMetaObject.connectSlotsByName(Security)

    def retranslateUi(self, Security):
        _translate = QtCore.QCoreApplication.translate
        Security.setWindowTitle(_translate("Security", "Sequrity"))
        self.label_2.setText(_translate("Security", "Security Level:"))
        self.label.setText(_translate("Security", "Object Name:"))
        self.label_5.setText(_translate("Security", "Owner:"))
        self.label_4.setText(_translate("Security", "Users:"))
        self.btnSetSec.setText(_translate("Security", "Apply"))

