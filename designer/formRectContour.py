# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\YandexDisk\Документы\Python Scripts\NDM_python\designer\formRectContour.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormRectContour(object):
    def setupUi(self, FormRectContour):
        FormRectContour.setObjectName("FormRectContour")
        FormRectContour.resize(579, 250)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(FormRectContour)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(FormRectContour)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBoxB = QtWidgets.QSpinBox(FormRectContour)
        self.spinBoxB.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxB.setMinimum(1)
        self.spinBoxB.setMaximum(10000)
        self.spinBoxB.setProperty("value", 300)
        self.spinBoxB.setObjectName("spinBoxB")
        self.horizontalLayout_2.addWidget(self.spinBoxB)
        self.label_3 = QtWidgets.QLabel(FormRectContour)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.spinBoxH = QtWidgets.QSpinBox(FormRectContour)
        self.spinBoxH.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxH.setMinimum(1)
        self.spinBoxH.setMaximum(10000)
        self.spinBoxH.setProperty("value", 500)
        self.spinBoxH.setObjectName("spinBoxH")
        self.horizontalLayout_2.addWidget(self.spinBoxH)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(FormRectContour)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.spinBoxNum = QtWidgets.QSpinBox(FormRectContour)
        self.spinBoxNum.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxNum.setMinimum(1)
        self.spinBoxNum.setMaximum(1000)
        self.spinBoxNum.setObjectName("spinBoxNum")
        self.horizontalLayout_3.addWidget(self.spinBoxNum)
        self.pushButtonAdd = QtWidgets.QPushButton(FormRectContour)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout_3.addWidget(self.pushButtonAdd)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableViewPointsContour = QtWidgets.QTableView(FormRectContour)
        self.tableViewPointsContour.setObjectName("tableViewPointsContour")
        self.verticalLayout.addWidget(self.tableViewPointsContour)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBoxNums = QtWidgets.QComboBox(FormRectContour)
        self.comboBoxNums.setObjectName("comboBoxNums")
        self.horizontalLayout_4.addWidget(self.comboBoxNums)
        self.pushButtonDel = QtWidgets.QPushButton(FormRectContour)
        self.pushButtonDel.setObjectName("pushButtonDel")
        self.horizontalLayout_4.addWidget(self.pushButtonDel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(FormRectContour)
        self.graphicsView.setMinimumSize(QtCore.QSize(230, 230))
        self.graphicsView.setMaximumSize(QtCore.QSize(230, 230))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)

        self.retranslateUi(FormRectContour)
        QtCore.QMetaObject.connectSlotsByName(FormRectContour)

    def retranslateUi(self, FormRectContour):
        _translate = QtCore.QCoreApplication.translate
        FormRectContour.setWindowTitle(_translate("FormRectContour", "Прямоугольный контур"))
        self.label_2.setText(_translate("FormRectContour", "Ширина В, мм"))
        self.label_3.setText(_translate("FormRectContour", "Высота Н, мм"))
        self.label.setText(_translate("FormRectContour", "Номер контура:"))
        self.pushButtonAdd.setText(_translate("FormRectContour", "Создать"))
        self.pushButtonDel.setText(_translate("FormRectContour", "Удалить"))
