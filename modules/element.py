# %%
import modules.geometry as geo
import modules.crossects as cs
from math import sqrt


# %%
class Fe(object):
    def __init__(self):
        self.number = 0
        self.sections = []
        self.stiff = 0
        self.typeFe: str = ''  # 'bar' или 'shell'
        self.length = 0
        self.area = 0


class FeBar(Fe):
    def __init__(self, s=cs.Node, e=cs.Node):
        self.i = s
        self.j = e
        self.getLenght()

    def getLenght(self):
        v = cs.Vector3d(self.i, self.j)
        self.length = v.norma
        return self.length


class FeShell(Fe):
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.contour = cs.Contour(1, nodes)


# %%

class Element:
    def __init__(self, number, length=0):
        self.fes = []
        self.number = number
        self.desript = ''
        self.typeEl = ''
        self.length = length

    def getFesNumbers(self):
        res = []
        for item in self.fes:
            res.append(item.number)
        return res

    def getLength(self):
        l = 0

        if len(self.fes) == 0:
            return l
        
        else:
            for item in self.fes:
                if item.typeFe == 'bar':
                    l = l + item.length
            return l


# %%
