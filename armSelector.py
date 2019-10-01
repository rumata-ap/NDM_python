# %% Импорты
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.interpolate import interp1d

dfA = pd.read_csv('Арматура_диаграммы.csv', ';')


def selectArm(c):
    res = dfA[dfA.Class == c]
    c = res[res.Action == 'C']
    cl = res[res.Action == 'CL']
    n = res[res.Action == 'N']
    nl = res[res.Action == 'NL']
    return c, cl, n, nl

# %% Диаграммы деформирования


class diagrA:
    # конструктор
    def __init__(self, classA):
        C, CL, N, NL = selectArm(classA)
        self.frameC = C
        self.frameCL = CL
        self.frameN = N
        self.frameNL = NL

        ε_C = C.ε.to_numpy()
        self.epsC = np.append(ε_C, -ε_C[0])
        σ_C = C.σ.to_numpy().astype(float)
        self.sigC = np.append(σ_C, σ_C[σ_C.size-1])

        ε_CL = CL.ε.to_numpy()
        self.epsCL = np.append(ε_CL, -ε_CL[0])
        σ_CL = CL.σ.to_numpy().astype(float)
        self.sigCL = np.append(σ_CL, σ_CL[σ_CL.size-1])

        ε_N = N.ε.to_numpy()
        self.epsN = np.append(ε_N, -ε_N[0])
        σ_N = N.σ.to_numpy().astype(float)
        self.sigN = np.append(σ_N, σ_N[σ_N.size-1])

        ε_NL = NL.ε.to_numpy()
        self.epsNL = np.append(ε_NL, -ε_NL[0])
        σ_NL = NL.σ.to_numpy().astype(float)
        self.sigNL = np.append(σ_NL, σ_NL[σ_NL.size-1])

        self.int_C = interp1d(self.epsC, self.sigC)
        self.int_CL = interp1d(self.epsCL, self.sigCL)
        self.int_N = interp1d(self.epsN, self.sigN)
        self.int_NL = interp1d(self.epsNL, self.sigNL)

    def sig(self, e):
        """
        Возвращает кортеж напряжений в арматуре согласно 
        функции 'σ(ε)' при различных действиях нагрузки (C, CL, N, NL).
        Параметр 'e' - значение деформации.
        """
        sigA_C = 0.0
        if e < self.epsC[0]:
            sigA_C = self.sigC[0]
        elif e > self.epsC[self.epsC.size-1]:
            sigA_C = self.sigC[self.sigC.size-1]
        else:
            sigA_C = self.int_C(e)*1.

        sigA_CL = 0.0
        if e < self.epsCL[0]:
            sigA_CL = self.sigCL[0]
        elif e > self.epsCL[self.epsCL.size-1]:
            sigA_CL = self.sigCL[self.sigCL.size-1]
        else:
            sigA_CL = self.int_CL(e)*1.

        sigA_N = 0.0
        if e < self.epsN[0]:
            sigA_N = self.sigN[0]
        elif e > self.epsN[self.epsN.size-1]:
            sigA_N = self.sigN[self.sigN.size-1]
        else:
            sigA_N = self.int_N(e)*1.

        sigA_NL = 0.0
        if e < self.epsNL[0]:
            sigA_NL = self.sigNL[0]
        elif e > self.epsNL[self.epsNL.size-1]:
            sigA_NL = self.sigNL[self.sigNL.size-1]
        else:
            sigA_NL = self.int_NL(e)*1.

        return sigA_C, sigA_CL, sigA_N, sigA_NL

# %%


def plotArmDiagr(df):
    c = dfA[dfA.Action != "N"]
    c = c[c.Action != "NL"]
    fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
    fig.update_layout(width=600, height=400,
                      title='Расчетные (CL - при длительном действии нагрузок)')
    fig.show()
    c = dfA[dfA.Action != "C"]
    c = c[c.Action != "CL"]
    fig = px.line(c, x="ε", y="σ_MPa", color='Action', text='Text')
    fig.update_layout(width=600, height=400,
                      title='Норматривные (NL - при длительном действии нагрузок)')
    fig.show()
