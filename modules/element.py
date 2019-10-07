# %%
import pandas as pd
import numpy as np
import pickle
import modules.geometry as geo
import modules.crossects as cs
# import Lira.rsu_lira_parser as lp
from math import sqrt


# %%
class Fe:
    number: int
    sections = []
    stiff: pd.DataFrame
    typeFe: str #'bar' или 'plate'


class FeBar(Fe):
    i: cs.Node
    j: cs.Node
    length: float

    def __init__(self, s=cs.Node(), e=cs.Node()):
        self.i = s
        self.j = e
        self.getLenght()

    def getLenght(self):
        v = cs.Vector3d(self.i, self.j)
        self.length = v.norma
        return self.length


class FePlate(Fe):
    nodes: list
    contour: cs.Сontour


# %%

class Element:
    number: int
    elType = ''
    desript: str
    fes: list
    selectedFe: Fe

    def __init__(self, number):
        self.fes = []
        self.number = number
        self.desript = ''

    def getRSU(self, parameter_list):
        pass

    def getFesNumbers(self):
        res = []
        for item in self.fes:
            res.append(item.number)
        return res

# %%
