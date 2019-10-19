# %%
import sys
import copy
import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
import pandas as pd
import numpy as np
import plotly.express as px
from modules.linearInterpolation import linterp1d
from modules.project import Project


# %%

class Beton:
    # конструктор
    def __init__(self, classB, typdiagB, vlag, gb3=1):
        self.classB = classB
        self.gamma_b_3 = gb3
        self.number = None
        self.descript = ''
        self.type = typdiagB
        self.vlag = vlag
        self.src = self.selectBeton(typdiagB, classB, vlag)
        self.frameC = self.src[self.src.Action == 'C']
        self.frameCL = self.src[self.src.Action == 'CL']
        self.frameN = self.src[self.src.Action == 'N']
        self.frameNL = self.src[self.src.Action == 'NL']

        self.epsC = self.frameC.ε.to_numpy()
        self.sigC = self.frameC.σ.to_numpy().astype(float)

        self.epsCL = self.frameCL.ε.to_numpy()
        self.sigCL = self.frameCL.σ.to_numpy().astype(float)

        self.epsN = self.frameN.ε.to_numpy()
        self.sigN = self.frameN.σ.to_numpy().astype(float)

        self.epsNL = self.frameNL.ε.to_numpy()
        self.sigNL = self.frameNL.σ.to_numpy().astype(float)

        if self.gamma_b_3 != 1.:
            for i in range(len(self.sigC)):
                if self.sigC[i] > 0:
                    self.sigC[i] = self.sigC[i] * self.gamma_b_3
            for i in range(len(self.sigCL)):
                if self.sigCL[i] > 0:
                    self.sigCL[i] = self.sigCL[i] * self.gamma_b_3

        self.int_C = linterp1d(self.epsC, self.sigC)
        self.int_CL = linterp1d(self.epsCL, self.sigCL)
        self.int_N = linterp1d(self.epsN, self.sigN)
        self.int_NL = linterp1d(self.epsNL, self.sigNL)

    def selectBeton(self, t, c, v):
        src = pd.read_csv('Бетон_диаграммы.csv', ';')
        return src.query('Vlaga == {} and Class=={} and Type =={}'.format(v, c, t))

    def plotDiagr(self):
        c = self.src[self.src.Action != "N"]
        c = c[c.Action != "NL"]
        fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
        fig.update_layout(width=600, height=400,
                          title='Расчетные (CL - при длительном действии нагрузок)')
        fig.show()
        c = self.src[self.src.Action != "C"]
        c = c[c.Action != "CL"]
        fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
        fig.update_layout(width=600, height=400,
                          title='Норматривные (NL - при длительном действии нагрузок)')
        fig.show()

    def sig(self, e, act='C'):
        """
        Возвращает кортеж напряжений в бетоне согласно 
        функции 'σ(ε)' при различных действиях нагрузки (C, CL, N, NL).
        Параметр 'e' - значение деформации.
        """
        if act == 'C':
            sigB_C = 0.0
            if e < self.epsC[0]:
                sigB_C = 0
            elif e > self.epsC[self.epsC.size-1]:
                sigB_C = self.sigC[self.sigC.size-1]
            else:
                sigB_C = self.int_C.linterp(e)
            return sigB_C
        elif act == 'CL':
            sigB_CL = 0.0
            if e < self.epsCL[0]:
                sigB_CL = 0
            elif e > self.epsCL[self.epsCL.size-1]:
                sigB_CL = self.sigCL[self.sigCL.size-1]
            else:
                sigB_CL = self.int_CL.linterp(e)
            return sigB_CL
        elif act == 'N':
            sigB_N = 0.0
            if e < self.epsN[0]:
                sigB_N = 0
            elif e > self.epsN[self.epsN.size-1]:
                sigB_N = self.sigN[self.sigN.size-1]
            else:
                sigB_N = self.int_N.linterp(e)
            return sigB_N
        elif act == 'NL':
            sigB_NL = 0.0
            if e < self.epsNL[0]:
                sigB_NL = 0
            elif e > self.epsNL[self.epsNL.size-1]:
                sigB_NL = self.sigNL[self.sigNL.size-1]
            else:
                sigB_NL = self.int_NL.linterp(e)
            return sigB_NL

# %%


class BetonCreator(QtWidgets.QWidget):
    def __init__(self, prj, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = prj
        self.setWindowTitle('Параметры бетона')
        self.labelClass = QtWidgets.QLabel("Класс:")
        self.labelVlag = QtWidgets.QLabel("Влажность среды:")
        self.labelDiagr = QtWidgets.QLabel("Диаграмма деформирования:")
        self.labelGamma_b_3 = QtWidgets.QLabel("Коэффициент γb3:")
        self.labelDescript = QtWidgets.QLabel("Описание:")
        self.labelNumber = QtWidgets.QLabel("Номер:")
        self.teDescript = QtWidgets.QTextEdit('Бетон:', self)
        self.teDescript.setFixedHeight(50)
        self.cbClass = QtWidgets.QComboBox(self)
        self.cbClass.addItems(
            ['B10', 'B15', 'B20', 'B25', 'B30', 'B35', 'B40', 'B45', 'B50', 'B55', 'B60'])
        self.cbClass.setCurrentText('B25')
        self.cbDiagr = QtWidgets.QComboBox(self)
        self.cbDiagr.addItems(['Трехлинейная', 'Двухлинейная'])
        self.cbVlag = QtWidgets.QComboBox(self)
        self.cbVlag.addItems(["Ниже 40%", "40% - 75%", "Выше 75%"])
        self.cbVlag.setCurrentIndex(1)
        self.cbGamma_b_3 = QtWidgets.QComboBox(self)
        self.cbGamma_b_3.addItems(['1.0', '0.85'])

        #self.lineGamma_b_3 = QtWidgets.QLineEdit('1.0', self)
        #validator = QtGui.QDoubleValidator(0.1, 1, 2, self)
        # validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        # self.lineGamma_b_3.setValidator(validator)
        # self.lineGamma_b_3.setAlignment(QtCore.Qt.AlignCenter)
        self.btnCreate = QtWidgets.QPushButton('Создать')
        self.btnCreate.clicked.connect(self.addBeton)
        self.spinNumber = QtWidgets.QSpinBox(self)
        self.spinNumber.setRange(1, 100000)
        self.spinNumber.setAlignment(QtCore.Qt.AlignCenter)
        if len(self.prj.materials['b']) > 0:
            self.spinNumber.setValue(len(self.prj.materials['b'])+1)
        else:
            self.spinNumber.setValue(1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.labelNumber)
        self.hbox.addWidget(self.spinNumber)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addWidget(self.labelDescript)
        self.hbox2.addWidget(self.teDescript)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.labelGamma_b_3)
        self.hbox1.addWidget(self.cbGamma_b_3)

        self.box = QtWidgets.QVBoxLayout()
        self.box.addLayout(self.hbox)
        self.box.addWidget(self.labelClass)
        self.box.addWidget(self.cbClass)
        self.box.addWidget(self.labelDiagr)
        self.box.addWidget(self.cbDiagr)
        self.box.addWidget(self.labelVlag)
        self.box.addWidget(self.cbVlag)
        self.box.addLayout(self.hbox1)
        self.box.addLayout(self.hbox2)
        self.box.addWidget(self.btnCreate)

        self.setLayout(self.box)

    def addBeton(self):
        ic = self.cbClass.currentIndex()
        dc = self.teDescript.toPlainText()+'\nкласс - '+self.cbClass.currentText()
        it = self.cbDiagr.currentIndex() + 1
        dc = dc+'\nдиаграмма - '+self.cbDiagr.currentText()
        iv = self.cbVlag.currentIndex() + 1
        dc = dc + '\nвлажность среды - ' + self.cbVlag.currentText()
        gb3 = float(self.cbGamma_b_3.currentText())
        dc = dc + '\nγb3 - ' + self.cbGamma_b_3.currentText()
        clsB = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
        bet = Beton(clsB[ic], it, iv, gb3)
        bet.number = self.spinNumber.value()
        bet.descript = dc
        self.prj.materials['b'][bet.number] = bet
        self.prj.selectedBeton = bet
        # self.teDescript.setPlainText(dc)
        self.spinNumber.stepUp()


class BetonEditor(QtWidgets.QWidget):
    def __init__(self, prj, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = prj
        self.setWindowTitle('Параметры бетона')
        self.labelClass = QtWidgets.QLabel("Класс:")
        self.labelVlag = QtWidgets.QLabel("Влажность среды:")
        self.labelDiagr = QtWidgets.QLabel("Диаграмма деформирования:")
        self.labelGamma_b_3 = QtWidgets.QLabel("Коэффициент γb3:")
        self.labelDescript = QtWidgets.QLabel("Описание:")
        self.labelNumber = QtWidgets.QLabel("Номер:")
        self.teDescript = QtWidgets.QTextEdit('Бетон:', self)
        self.teDescript.setFixedHeight(50)
        self.cbClass = QtWidgets.QComboBox(self)
        self.cbClass.addItems(
            ['B10', 'B15', 'B20', 'B25', 'B30', 'B35', 'B40', 'B45', 'B50', 'B55', 'B60'])
        self.cbClass.setCurrentText('B25')
        self.cbDiagr = QtWidgets.QComboBox(self)
        self.cbDiagr.addItems(['Трехлинейная', 'Двухлинейная'])
        self.cbVlag = QtWidgets.QComboBox(self)
        self.cbVlag.addItems(["Ниже 40%", "40% - 75%", "Выше 75%"])
        self.cbVlag.setCurrentIndex(1)
        self.cbGamma_b_3 = QtWidgets.QComboBox(self)
        self.cbGamma_b_3.addItems(['1.0', '0.85'])
        self.cbNums = QtWidgets.QComboBox(self)

        if len(self.prj.materials['b']) > 0:
            contentNums = self.prj.materials['b'].keys()
            self.cbNums.addItems(contentNums)
            self.cbNums.setCurrentText(str(self.prj.selectedBeton.number))
            self.cbClass.setCurrentText(
                'B' + str(self.prj.selectedBeton.classB))
            self.cbDiagr.setCurrentIndex(self.prj.selectedBeton.type - 1)
            self.cbVlag.setCurrentIndex(self.prj.selectedBeton.vlag - 1)
            self.teDescript.setPlainText(self.prj.selectedBeton.descript)
            self.cbGamma_b_3.setCurrentText(
                str(self.prj.selectedBeton.gamma_b_3))

        self.cbNums.activated.connect(self.on_changeNum)

        self.btnEdit = QtWidgets.QPushButton('Изменить')
        self.btnEdit.clicked.connect(self.editBeton)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.labelNumber)
        self.hbox.addWidget(self.cbNums)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addWidget(self.labelDescript)
        self.hbox2.addWidget(self.teDescript)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.labelGamma_b_3)
        self.hbox1.addWidget(self.cbGamma_b_3)

        self.box = QtWidgets.QVBoxLayout()
        self.box.addLayout(self.hbox)
        self.box.addWidget(self.labelClass)
        self.box.addWidget(self.cbClass)
        self.box.addWidget(self.labelDiagr)
        self.box.addWidget(self.cbDiagr)
        self.box.addWidget(self.labelVlag)
        self.box.addWidget(self.cbVlag)
        self.box.addLayout(self.hbox1)
        self.box.addLayout(self.hbox2)
        self.box.addWidget(self.btnEdit)

        self.setLayout(self.box)

    def editBeton(self):
        if len(self.prj.materials['b']) == 0:
            return
        ic = self.cbClass.currentIndex()
        dc = self.teDescript.toPlainText() + '\nкласс - ' + self.cbClass.currentText()
        it = self.cbDiagr.currentIndex() + 1
        dc = dc + '\nдиаграмма - ' + self.cbDiagr.currentText()
        iv = self.cbVlag.currentIndex() + 1
        dc = dc + '\nвлажность среды - ' + self.cbVlag.currentText()
        gb3 = float(self.cbGamma_b_3.currentText())
        dc = dc+'\nγb3 - '+self.cbGamma_b_3.currentText()
        clsB = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
        bet = Beton(clsB[ic], it, iv, gb3)
        bet.number = int(self.cbNums.currentText())
        bet.descript = dc
        self.prj.materials['b'][int(self.cbNums.currentText())] = bet
        self.prj.selectedBeton = self.prj.materials['b'][int(
            self.cbNums.currentText())]
        # self.teDescript.setPlainText(dc)

    def on_changeNum(self):
        self.prj.selectedBeton = self.prj.materials['b'][int(
            self.cbNums.currentText())]
        self.cbClass.setCurrentText(
            'B' + str(self.prj.selectedBeton.classB))
        self.cbDiagr.setCurrentIndex(self.prj.selectedBeton.type - 1)
        self.cbVlag.setCurrentIndex(self.prj.selectedBeton.vlag - 1)
        self.cbGamma_b_3.setCurrentText(str(self.prj.selectedBeton.gamma_b_3))
        self.teDescript.setPlainText('Бетон: ')
        # self.teDescript.setPlainText(self.prj.selectedBeton.descript)
