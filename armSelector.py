# %% Импорты
import pandas as pd
import numpy as np
import plotly.express as px
from linearInterpolation import linterp1d

# %% Диаграммы деформирования


class diagrA:
    # конструктор
    def __init__(self, classA):
        self.classA = classA
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
        self.sigNL = np.append(σ_NL, σ_NL[σ_NL.size-1])

        self.int_C = linterp1d(self.epsC, self.sigC)
        self.int_CL = linterp1d(self.epsCL, self.sigCL)
        self.int_N = linterp1d(self.epsN, self.sigN)
        self.int_NL = linterp1d(self.epsNL, self.sigNL)

    def selectArm(self,c):
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

