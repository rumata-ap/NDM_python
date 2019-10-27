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
from designer.formBetonsEditor import Ui_FormBetonEditor


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


class BetonEditorWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.prj: Project = parent.prj

        self.form = Ui_FormBetonEditor()
        self.form.setupUi(self)
        form = self.form
        form.comboBoxClass.addItems(
            ['B10', 'B15', 'B20', 'B25', 'B30', 'B35', 'B40', 'B45', 'B50', 'B55', 'B60'])
        form.comboBoxClass.setCurrentText('B25')
        form.comboBoxDiagr.addItems(['Трехлинейная', 'Двухлинейная'])
        form.comboBoxVlag.addItems(["Ниже 40%", "40% - 75%", "Выше 75%"])
        form.comboBoxVlag.setCurrentIndex(1)
        form.comboBoxGamma_b3.addItems(['1.0', '0.85'])
        form.plainTextEditDescript.setPlainText('Бетон:')
        if len(self.prj.materials['b']) > 0:
            form.spinBoxNum.setValue(len(self.prj.materials['b'])+1)
        else:
            form.spinBoxNum.setValue(1)
        form.pushButtonAdd.clicked.connect(self.on_add)
        form.pushButtonEdit.clicked.connect(self.on_edit)
        form.pushButtonDel.clicked.connect(self.on_del)
        form.comboBoxNums.activated.connect(self.on_changeNum)

    def showEvent(self, е):
        if len(self.prj.materials['b']) == 0:
            self.form.spinBoxNum.setValue(1)
        else:
            keys = list(self.prj.materials['b'].keys())
            for betonsKey in self.prj.materials['b'].keys():
                self.form.comboBoxNums.addItem(str(betonsKey))
            self.form.spinBoxNum.setValue(keys[len(keys)-1])

        QtWidgets.QWidget.showEvent(self, е)

    @QtCore.pyqtSlot()
    def on_add(self):
        ic = self.form.comboBoxClass.currentIndex()
        dc = self.form.plainTextEditDescript.toPlainText()+'\nкласс - ' + \
            self.form.comboBoxClass.currentText()
        it = self.form.comboBoxDiagr.currentIndex() + 1
        dc = dc + '\nдиаграмма - ' + self.form.comboBoxDiagr.currentText()
        iv = self.form.comboBoxVlag.currentIndex() + 1
        dc = dc + '\nвлажность среды - ' + self.form.comboBoxVlag.currentText()
        gb3 = float(self.form.comboBoxGamma_b3.currentText())
        dc = dc + '\nγb3 - ' + self.form.comboBoxGamma_b3.currentText()
        clsB = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
        bet = Beton(clsB[ic], it, iv, gb3)
        bet.number = self.form.spinBoxNum.value()
        bet.descript = dc
        self.prj.materials['b'][bet.number] = bet
        self.prj.selectedBeton = bet
        # self.teDescript.setPlainText(dc)
        self.form.comboBoxNums.addItem(str(bet.number))
        self.form.spinBoxNum.stepUp()

    @QtCore.pyqtSlot()
    def on_edit(self):
        if len(self.prj.materials['b']) == 0:
            return
        ic = self.form.comboBoxClass.currentIndex()
        dc = self.form.plainTextEditDescript.toPlainText() + '\nкласс - ' + \
            self.form.comboBoxClass.currentText()
        it = self.form.comboBoxDiagr.currentIndex() + 1
        dc = dc + '\nдиаграмма - ' + self.form.comboBoxDiagr.currentText()
        iv = self.form.comboBoxVlag.currentIndex() + 1
        dc = dc + '\nвлажность среды - ' + self.form.comboBoxVlag.currentText()
        gb3 = float(self.form.comboBoxGamma_b3.currentText())
        dc = dc+'\nγb3 - '+self.form.comboBoxGamma_b3.currentText()
        clsB = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
        bet = Beton(clsB[ic], it, iv, gb3)
        bet.number = int(self.form.comboBoxNums.currentText())
        bet.descript = dc
        self.prj.materials['b'][int(
            self.form.comboBoxNums.currentText())] = bet
        self.prj.selectedBeton = self.prj.materials['b'][int(
            self.form.comboBoxNums.currentText())]

    @QtCore.pyqtSlot()
    def on_del(self):       
        if len(self.prj.materials['b']) > 0:
            keys = list(self.prj.materials['b'].keys())
            del self.prj.materials['b'][int(
                self.form.comboBoxNums.currentText())]
            self.form.comboBoxNums.clear()
            for betonsKey in self.prj.materials['b'].keys():
                self.form.comboBoxNums.addItem(str(betonsKey))
            # self.form.spinBoxNum.setValue(keys[len(keys)-1]+1)

    @QtCore.pyqtSlot()
    def on_changeNum(self):
        self.prj.selectedBeton = self.prj.materials['b'][int(
            self.form.comboBoxNums.currentText())]
        self.form.comboBoxClass.setCurrentText(
            'B' + str(self.prj.selectedBeton.classB))
        self.form.comboBoxDiagr.setCurrentIndex(self.prj.selectedBeton.type - 1)
        self.form.comboBoxVlag.setCurrentIndex(self.prj.selectedBeton.vlag - 1)
        self.form.comboBoxGamma_b3.setCurrentText(str(self.prj.selectedBeton.gamma_b_3))
        self.form.plainTextEditDescript.setPlainText('Бетон: изм.')
        # self.form.plainTextEditDescript.setPlainText(
        #     self.prj.selectedBeton.descript)