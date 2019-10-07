# %%
import pandas as pd
import numpy as np
import plotly.express as px
from modules.linearInterpolation import linterp1d


# %%

class Beton:
    descript = ''
    number: int
    # конструктор
    def __init__(self, classB, typdiagB, vlag):
        self.classB = classB
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