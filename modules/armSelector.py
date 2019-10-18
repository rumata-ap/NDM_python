# %% Импорты
import sys
import copy
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
from modules.linearInterpolation import linterp1d
from PyQt5 import QtCore, QtWidgets, QtGui

# %% Диаграммы деформирования


class Armatura:
    # конструктор
    def __init__(self, classA, gs=1.):
        self.number = None
        self.descript = ''
        self.classA = classA
        self.gamma_s = gs
        self.src = self.selectArm(classA)
        self.frameC = self.src[self.src.Action == 'C']
        self.frameCL = self.src[self.src.Action == 'CL']
        self.frameN = self.src[self.src.Action == 'N']
        self.frameNL = self.src[self.src.Action == 'NL']

        ε_C = self.frameC.ε.to_numpy()
        self.epsC = np.append(ε_C, -ε_C[0])
        σ_C = self.frameC.σ.to_numpy().astype(float)
        self.sigC = np.append(σ_C, σ_C[σ_C.size-1])

        ε_CL = self.frameCL.ε.to_numpy()
        self.epsCL = np.append(ε_CL, -ε_CL[0])
        σ_CL = self.frameCL.σ.to_numpy().astype(float)
        self.sigCL = np.append(σ_CL, σ_CL[σ_CL.size-1])

        ε_N = self.frameN.ε.to_numpy()
        self.epsN = np.append(ε_N, -ε_N[0])
        σ_N = self.frameN.σ.to_numpy().astype(float)
        self.sigN = np.append(σ_N, σ_N[σ_N.size-1])

        ε_NL = self.frameNL.ε.to_numpy()
        self.epsNL = np.append(ε_NL, -ε_NL[0])
        σ_NL = self.frameNL.σ.to_numpy().astype(float)
        self.sigNL = np.append(σ_NL, σ_NL[σ_NL.size - 1])

        if self.gamma_s != 1.:
            for i in range(len(self.sigC)):
                self.sigC[i] = self.sigC[i] * self.gamma_s
            for i in range(len(self.sigCL)):
                self.sigCL[i] = self.sigCL[i] * self.gamma_s

        self.int_C = linterp1d(self.epsC, self.sigC)
        self.int_CL = linterp1d(self.epsCL, self.sigCL)
        self.int_N = linterp1d(self.epsN, self.sigN)
        self.int_NL = linterp1d(self.epsNL, self.sigNL)

    def selectArm(self, c):
        src = pd.read_csv('Арматура_диаграммы.csv', ';')
        return src[src.Class == c]
        # return src.query('Class == {}'.format(c))
        # res = self.src[self.src.Class == c]
        # C = res[res.Action == 'C']
        # CL = res[res.Action == 'CL']
        # N = res[res.Action == 'N']
        # NL = res[res.Action == 'NL']
        # return C, CL, N, NL

    def plotArmDiagr(self):
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
        Возвращает кортеж напряжений в арматуре согласно 
        функции 'σ(ε)' при различных действиях нагрузки (C, CL, N, NL).
        Параметр 'e' - значение деформации.
        """
        if act == 'C':
            sigA_C = 0.0
            if e < self.epsC[0]:
                sigA_C = self.sigC[0]
            elif e > self.epsC[self.epsC.size-1]:
                sigA_C = self.sigC[self.sigC.size-1]
            else:
                sigA_C = self.int_C.linterp(e)

            return sigA_C

        elif act == 'CL':
            sigA_CL = 0.0
            if e < self.epsCL[0]:
                sigA_CL = self.sigCL[0]
            elif e > self.epsCL[self.epsCL.size-1]:
                sigA_CL = self.sigCL[self.sigCL.size-1]
            else:
                sigA_CL = self.int_CL.linterp(e)

            return sigA_CL

        elif act == 'N':
            sigA_N = 0.0
            if e < self.epsN[0]:
                sigA_N = self.sigN[0]
            elif e > self.epsN[self.epsN.size-1]:
                sigA_N = self.sigN[self.sigN.size-1]
            else:
                sigA_N = self.int_N.linterp(e)

            return sigA_N

        elif act == 'NL':
            sigA_NL = 0.0
            if e < self.epsNL[0]:
                sigA_NL = self.sigNL[0]
            elif e > self.epsNL[self.epsNL.size-1]:
                sigA_NL = self.sigNL[self.sigNL.size-1]
            else:
                sigA_NL = self.int_NL.linterp(e)

            return sigA_NL


class ArmCreator(QtWidgets.QWidget):
    def __init__(self, prj, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = prj
        self.setWindowTitle('Создание арматуры')
        self.labelClass = QtWidgets.QLabel("Класс:")
        # self.labelDiagr = QtWidgets.QLabel("Диаграмма деформирования:")
        self.labelGamma_s = QtWidgets.QLabel("Коэффициент γs:")
        self.labelDescript = QtWidgets.QLabel("Описание:")
        self.labelNumber = QtWidgets.QLabel("Номер:")
        self.teDescript = QtWidgets.QTextEdit('Арматура:', self)
        self.teDescript.setFixedHeight(50)
        self.cbClass = QtWidgets.QComboBox(self)
        self.cbClass.addItems(
            ['A240', 'A400', 'A500', 'B500', 'A600', 'A800', 'A1000',
                'Bp500', 'Bp1200', 'Bp1300', 'Bp1400', 'Bp1500', 'Bp1600',
             'K1400', 'K1500', 'K1600', 'K1700'])
        self.cbClass.setCurrentText('A500')

        self.lineGamma_s = QtWidgets.QLineEdit('1.0', self)
        validator = QtGui.QDoubleValidator(0.1, 1, 2, self)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.lineGamma_s.setValidator(validator)
        self.lineGamma_s.setAlignment(QtCore.Qt.AlignCenter)
        self.btnCreate = QtWidgets.QPushButton('Создать')
        self.btnCreate.clicked.connect(self.addArm)
        self.spinNumber = QtWidgets.QSpinBox(self)
        self.spinNumber.setRange(1, 100000)
        self.spinNumber.setAlignment(QtCore.Qt.AlignCenter)
        if len(self.prj.materials['a']) > 0:
            self.spinNumber.setValue(self.prj.selectedBeton.number + 1)
        else:
            self.spinNumber.setValue(1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.labelNumber)
        self.hbox.addWidget(self.spinNumber)

        # self.hbox2 = QtWidgets.QHBoxLayout()
        # self.hbox2.addWidget(self.labelDescript)
        # self.hbox2.addWidget(self.teDescript)

        self.hbox3 = QtWidgets.QHBoxLayout()
        self.hbox3.addWidget(self.labelGamma_s)
        self.hbox3.addWidget(self.lineGamma_s)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.labelClass)
        self.hbox1.addWidget(self.cbClass)

        self.box = QtWidgets.QVBoxLayout()
        self.box.addLayout(self.hbox)
        self.box.addLayout(self.hbox1)
        self.box.addLayout(self.hbox3)
        self.box.addWidget(self.labelDescript)
        self.box.addWidget(self.teDescript)
        self.box.addWidget(self.btnCreate)

        self.setLayout(self.box)

    def addArm(self):
        ic = self.cbClass.currentText()
        dc = self.teDescript.toPlainText()+'\nкласс - '+self.cbClass.currentText()
        arm = Armatura(ic)
        arm.number = self.spinNumber.value()
        arm.descript = dc
        self.prj.materials['a'].append(arm)
        self.prj.selectedArm = arm
        # self.teDescript.setPlainText(dc)
        self.spinNumber.stepUp()


# class BetonEditor(QtWidgets.QWidget):
#     def __init__(self, prj, parent=None):
#         QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
#         self.prj: Project = prj
#         self.setWindowTitle('Параметры бетона')
#         self.labelClass = QtWidgets.QLabel("Класс:")
#         self.labelVlag = QtWidgets.QLabel("Влажность среды:")
#         self.labelDiagr = QtWidgets.QLabel("Диаграмма деформирования:")
#         self.labelGamma_b_3 = QtWidgets.QLabel("Коэффициент γb3:")
#         self.labelDescript = QtWidgets.QLabel("Описание:")
#         self.labelNumber = QtWidgets.QLabel("Номер:")
#         self.teDescript = QtWidgets.QTextEdit('Бетон:', self)
#         self.teDescript.setFixedHeight(50)
#         self.cbClass = QtWidgets.QComboBox(self)
#         self.cbClass.addItems(
#             ['B10', 'B15', 'B20', 'B25', 'B30', 'B35', 'B40', 'B45', 'B50', 'B55', 'B60'])
#         self.cbClass.setCurrentText('B25')
#         self.cbDiagr = QtWidgets.QComboBox(self)
#         self.cbDiagr.addItems(['Трехлинейная', 'Двухлинейная'])
#         self.cbVlag = QtWidgets.QComboBox(self)
#         self.cbVlag.addItems(["Ниже 40%", "40% - 75%", "Выше 75%"])
#         self.cbVlag.setCurrentIndex(1)
#         self.cbGamma_b_3 = QtWidgets.QComboBox(self)
#         self.cbGamma_b_3.addItems(['1.0', '0.85'])
#         self.cbNums = QtWidgets.QComboBox(self)

#         if len(self.prj.materials['b']) > 0:
#             contentNums = []
#             for i in range(len(self.prj.materials['b'])):
#                 contentNums.append(str(self.prj.materials['b'][i].number))
#             self.cbNums.addItems(contentNums)
#             self.cbNums.setCurrentText(str(self.prj.selectedBeton.number))
#             self.cbClass.setCurrentText(
#                 'B' + str(self.prj.selectedBeton.classB))
#             self.cbDiagr.setCurrentIndex(self.prj.selectedBeton.type - 1)
#             self.cbVlag.setCurrentIndex(self.prj.selectedBeton.vlag - 1)
#             self.teDescript.setPlainText(self.prj.selectedBeton.descript)
#             self.cbGamma_b_3.setCurrentText(
#                 str(self.prj.selectedBeton.gamma_b_3))

#         self.cbNums.activated.connect(self.on_changeNum)

#         self.btnEdit = QtWidgets.QPushButton('Изменить')
#         self.btnEdit.clicked.connect(self.editBeton)

#         self.hbox = QtWidgets.QHBoxLayout()
#         self.hbox.addWidget(self.labelNumber)
#         self.hbox.addWidget(self.cbNums)

#         self.hbox2 = QtWidgets.QHBoxLayout()
#         self.hbox2.addWidget(self.labelDescript)
#         self.hbox2.addWidget(self.teDescript)

#         self.hbox1 = QtWidgets.QHBoxLayout()
#         self.hbox1.addWidget(self.labelGamma_b_3)
#         self.hbox1.addWidget(self.cbGamma_b_3)

#         self.box = QtWidgets.QVBoxLayout()
#         self.box.addLayout(self.hbox)
#         self.box.addWidget(self.labelClass)
#         self.box.addWidget(self.cbClass)
#         self.box.addWidget(self.labelDiagr)
#         self.box.addWidget(self.cbDiagr)
#         self.box.addWidget(self.labelVlag)
#         self.box.addWidget(self.cbVlag)
#         self.box.addLayout(self.hbox1)
#         self.box.addLayout(self.hbox2)
#         self.box.addWidget(self.btnEdit)

#         self.setLayout(self.box)

#     def editBeton(self):
#         if len(self.prj.materials['b']) == 0:
#             return
#         ic = self.cbClass.currentIndex()
#         dc = self.teDescript.toPlainText() + '\nкласс - ' + self.cbClass.currentText()
#         it = self.cbDiagr.currentIndex() + 1
#         dc = dc + '\nдиаграмма - ' + self.cbDiagr.currentText()
#         iv = self.cbVlag.currentIndex() + 1
#         dc = dc + '\nвлажность среды - ' + self.cbVlag.currentText()
#         gb3 = float(self.cbGamma_b_3.currentText())
#         dc = dc+'\nγb3 - '+self.cbGamma_b_3.currentText()
#         clsB = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
#         bet = Beton(clsB[ic], it, iv, gb3)
#         bet.number = int(self.cbNums.currentText())
#         bet.descript = dc
#         self.prj.materials['b'][self.cbNums.currentIndex()] = bet
#         self.prj.selectedBeton = self.prj.materials['b'][self.cbNums.currentIndex(
#         )]
#         #self.teDescript.setPlainText(dc)

#     def on_changeNum(self):
#         self.prj.selectedBeton = self.prj.materials['b'][self.cbNums.currentIndex(
#         )]
#         self.cbClass.setCurrentText(
#             'B' + str(self.prj.selectedBeton.classB))
#         self.cbDiagr.setCurrentIndex(self.prj.selectedBeton.type - 1)
#         self.cbVlag.setCurrentIndex(self.prj.selectedBeton.vlag - 1)
#         self.cbGamma_b_3.setCurrentText(str(self.prj.selectedBeton.gamma_b_3))
#         self.teDescript.setPlainText('Бетон: ')
#         #self.teDescript.setPlainText(self.prj.selectedBeton.descript)
