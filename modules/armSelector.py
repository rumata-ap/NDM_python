# %% Импорты
import sys
import copy
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
from modules.linearInterpolation import linterp1d
from PyQt5 import QtCore, QtWidgets, QtGui
from modules.project import Project
from designer.formArmsEditor import Ui_FormArmsEditor

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


class ArmEditorWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = parent.prj

        self.form = Ui_FormArmsEditor()
        self.form.setupUi(self)
        form = self.form
        form.comboBoxClass.addItems(
            ['A240', 'A400', 'A500', 'B500', 'A600', 'A800', 'A1000',
             'Bp500', 'Bp1200', 'Bp1300', 'Bp1400', 'Bp1500', 'Bp1600',
             'K1400', 'K1500', 'K1600', 'K1700'])
        form.comboBoxClass.setCurrentText('A500')
        form.plainTextEditDescript.setPlainText('Арматура:')
        if len(self.prj.materials['a']) > 0:
            form.spinBoxNum.setValue(self.prj.selectedArm.number + 1)
        else:
            form.spinBoxNum.setValue(1)

        form.pushButtonAdd.clicked.connect(self.on_add)
        form.pushButtonEdit.clicked.connect(self.on_edit)
        form.pushButtonDel.clicked.connect(self.on_del)
        form.comboBoxNums.activated.connect(self.on_changeNum)

    def showEvent(self, е):
        if len(self.prj.materials['a']) == 0:
            self.form.spinBoxNum.setValue(1)
        else:
            keys = list(self.prj.materials['a'].keys())
            for armsKey in self.prj.materials['a'].keys():
                self.form.comboBoxNums.addItem(str(armsKey))
            # self.form.spinBoxNum.setValue(keys[len(keys)-1])

        QtWidgets.QWidget.showEvent(self, е)

    @QtCore.pyqtSlot()
    def on_add(self):
        ic = self.form.comboBoxClass.currentText()
        dc = self.form.plainTextEditDescript.toPlainText() + '\nкласс - ' + \
            self.form.comboBoxClass.currentText()
        gs = self.form.doubleSpinBoxGamma_s.value()
        dc = dc + '\nγs - ' + self.form.doubleSpinBoxGamma_s.text()
        arm = Armatura(ic, gs)
        arm.number = self.form.spinBoxNum.value()
        self.form.comboBoxNums.addItem(self.form.spinBoxNum.text())
        arm.descript = dc
        self.prj.materials['a'][arm.number] = arm
        self.prj.selectedArm = arm
        # self.teDescript.setPlainText(dc)      
        self.form.spinBoxNum.stepUp()

    @QtCore.pyqtSlot()
    def on_edit(self):
        if len(self.prj.materials['a']) == 0:
            return
        ic = self.form.comboBoxClass.currentText()
        dc = self.form.plainTextEditDescript.toPlainText() + '\nкласс - ' + \
            self.form.comboBoxClass.currentText()
        # it = self.cbDiagr.currentIndex() + 1
        # dc = dc + '\nдиаграмма - ' + self.cbDiagr.currentText()
        # iv = self.cbVlag.currentIndex() + 1
        # dc = dc + '\nвлажность среды - ' + self.cbVlag.currentText()
        gs = self.form.doubleSpinBoxGamma_s.value()
        dc = dc+'\nγs - '+self.form.doubleSpinBoxGamma_s.text()
        arm = Armatura(ic, gs)
        arm.number = int(self.form.comboBoxNums.currentText())
        arm.descript = dc
        self.prj.materials['a'][int(self.form.comboBoxNums.currentText())] = arm
        self.prj.selectedArm = self.prj.materials['a'][int(
            self.form.comboBoxNums.currentText())]
        # self.teDescript.setPlainText(dc)

    @QtCore.pyqtSlot()
    def on_del(self):
        if len(self.prj.materials['a']) > 0:
            keys = list(self.prj.materials['a'].keys())
            del self.prj.materials['a'][int(
                self.form.comboBoxNums.currentText())]
            self.form.comboBoxNums.clear()
            for armsKey in self.prj.materials['a'].keys():
                self.form.comboBoxNums.addItem(str(armsKey))

    @QtCore.pyqtSlot()
    def on_changeNum(self):
        self.prj.selectedArm = self.prj.materials['a'][int(
            self.form.comboBoxNums.currentText())]
        self.form.comboBoxClass.setCurrentText(self.prj.selectedArm.classA)
        self.form.doubleSpinBoxGamma_s.setValue(self.prj.selectedArm.gamma_s)
        self.form.plainTextEditDescript.setPlainText('Арматура: изм. ')
        # self.teDescript.setPlainText(self.prj.selectedBeton.descript)