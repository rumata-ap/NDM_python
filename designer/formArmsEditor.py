# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\YandexDisk\Документы\Python Scripts\NDM_python\designer\formArmsEditor.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormArmsEditor(object):
    def setupUi(self, FormArmsEditor):
        FormArmsEditor.setObjectName("FormArmsEditor")
        FormArmsEditor.resize(292, 243)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FormArmsEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(FormArmsEditor)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBoxNum = QtWidgets.QSpinBox(FormArmsEditor)
        self.spinBoxNum.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxNum.setMinimum(1)
        self.spinBoxNum.setObjectName("spinBoxNum")
        self.horizontalLayout.addWidget(self.spinBoxNum)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(FormArmsEditor)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBoxClass = QtWidgets.QComboBox(FormArmsEditor)
        self.comboBoxClass.setObjectName("comboBoxClass")
        self.horizontalLayout_2.addWidget(self.comboBoxClass)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(FormArmsEditor)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.doubleSpinBoxGamma_s = QtWidgets.QDoubleSpinBox(FormArmsEditor)
        self.doubleSpinBoxGamma_s.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBoxGamma_s.setSingleStep(0.01)
        self.doubleSpinBoxGamma_s.setProperty("value", 1.0)
        self.doubleSpinBoxGamma_s.setObjectName("doubleSpinBoxGamma_s")
        self.horizontalLayout_5.addWidget(self.doubleSpinBoxGamma_s)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.label_6 = QtWidgets.QLabel(FormArmsEditor)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.plainTextEditDescript = QtWidgets.QPlainTextEdit(FormArmsEditor)
        self.plainTextEditDescript.setObjectName("plainTextEditDescript")
        self.verticalLayout.addWidget(self.plainTextEditDescript)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButtonDel = QtWidgets.QPushButton(FormArmsEditor)
        self.pushButtonDel.setObjectName("pushButtonDel")
        self.horizontalLayout_6.addWidget(self.pushButtonDel)
        self.comboBoxNums = QtWidgets.QComboBox(FormArmsEditor)
        self.comboBoxNums.setObjectName("comboBoxNums")
        self.horizontalLayout_6.addWidget(self.comboBoxNums)
        self.pushButtonEdit = QtWidgets.QPushButton(FormArmsEditor)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.horizontalLayout_6.addWidget(self.pushButtonEdit)
        self.pushButtonAdd = QtWidgets.QPushButton(FormArmsEditor)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout_6.addWidget(self.pushButtonAdd)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(FormArmsEditor)
        QtCore.QMetaObject.connectSlotsByName(FormArmsEditor)

    def retranslateUi(self, FormArmsEditor):
        _translate = QtCore.QCoreApplication.translate
        FormArmsEditor.setWindowTitle(_translate("FormArmsEditor", "Редактор арматуры"))
        self.label.setText(_translate("FormArmsEditor", "Номер:"))
        self.label_2.setText(_translate("FormArmsEditor", "Класс:"))
        self.label_5.setText(_translate("FormArmsEditor", "Коэффициент γs:"))
        self.label_6.setText(_translate("FormArmsEditor", "Описание:"))
        self.pushButtonDel.setText(_translate("FormArmsEditor", "Удалить"))
        self.pushButtonEdit.setText(_translate("FormArmsEditor", "Изменить"))
        self.pushButtonAdd.setText(_translate("FormArmsEditor", "Создать"))
