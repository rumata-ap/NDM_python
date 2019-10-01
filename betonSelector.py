# %%
#from sympy import Function, S, oo
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.interpolate import interp1d

dfB = pd.read_csv('Бетон_диаграммы.csv', ';')
# %%


def selectBeton(t, c, v):
    return dfB.query('Vlaga == {} and Class=={} and Type =={}'.format(v, c, t))


def plotBetDiagr(df):
    c = dfB[dfB.Action != "N"]
    c = c[c.Action != "NL"]
    fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
    fig.update_layout(width=600, height=400,
                      title='Расчетные (CL - при длительном действии нагрузок)')
    fig.show()
    c = dfB[dfB.Action != "C"]
    c = c[c.Action != "CL"]
    fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
    fig.update_layout(width=600, height=400,
                      title='Норматривные (NL - при длительном действии нагрузок)')
    fig.show()

# %%


class diagrB:
    # конструктор
    def __init__(self, classB, typdiagB, vlag):
        s = selectBeton(typdiagB, classB, vlag)
        C = s[s.Action == 'C']
        CL = s[s.Action == 'CL']
        N = s[s.Action == 'N']
        NL = s[s.Action == 'NL']

        self.frameC = C
        self.frameCL = CL
        self.frameN = N
        self.frameNL = NL

        self.epsC = C.ε.to_numpy()
        self.sigC = C.σ.to_numpy().astype(float)

        self.epsCL = CL.ε.to_numpy()
        self.sigCL = CL.σ.to_numpy().astype(float)

        self.epsN = N.ε.to_numpy()
        self.sigN = N.σ.to_numpy().astype(float)

        self.epsNL = NL.ε.to_numpy()
        self.sigNL = NL.σ.to_numpy().astype(float)

        self.int_C = interp1d(self.epsC, self.sigC)
        self.int_CL = interp1d(self.epsCL, self.sigCL)
        self.int_N = interp1d(self.epsN, self.sigN)
        self.int_NL = interp1d(self.epsNL, self.sigNL)

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
                sigB_C = self.int_C(e)*1.
            return sigB_C
        elif act == 'CL':
            sigB_CL = 0.0
            if e < self.epsCL[0]:
                sigB_CL = 0
            elif e > self.epsCL[self.epsCL.size-1]:
                sigB_CL = self.sigCL[self.sigCL.size-1]
            else:
                sigB_CL = self.int_CL(e)*1.
            return sigB_CL
        elif act == 'N':
            sigB_N = 0.0
            if e < self.epsN[0]:
                sigB_N = 0
            elif e > self.epsN[self.epsN.size-1]:
                sigB_N = self.sigN[self.sigN.size-1]
            else:
                sigB_N = self.int_N(e)*1.
            return sigB_N
        elif act == 'NL':
            sigB_NL = 0.0
            if e < self.epsNL[0]:
                sigB_NL = 0
            elif e > self.epsNL[self.epsNL.size-1]:
                sigB_NL = self.sigNL[self.sigNL.size-1]
            else:
                sigB_NL = self.int_NL(e) * 1.
            return sigB_NL

# %%
