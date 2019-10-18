# %%
import matplotlib.pyplot as plt
import triangle as tr
from modules.geometry import Point3d, Vector3d, Line2d, Plane
from modules.armSelector import Armatura
from modules.betonSelector import Beton
from math import pi, sqrt
import numpy as np


# import triangle
# from scipy.integrate import dblquad
# from sympy.integrals.intpoly import *
# from sympy import Point, Polygon, Float

# %%

class Node(Point3d):
    def __init__(self, num=0, x=0., y=0., z=0., attr={}):
        Point3d.__init__(self, x, y, z)
        self.id = num
        self.attr = attr

    def fromPoint3d(self, pt: Point3d):
        self.X = pt.X
        self.Y = pt.Y
        self.Z = pt.Z


# %%


class Segment:
    def __init__(self, num: int, i: Point3d, j: Point3d, attr={}):
        self.i = i
        self.j = j
        self.attr = attr
        self.num = num
        self.line = Line2d(i, j)


class BoundingBox:
    def __init__(self, minp=Point3d(), maxp=Point3d()):
        self.minPt = minp
        self.maxPt = maxp


# %%


class Contour:
    def __init__(self, num: int, nodes=[], attr={}):
        self.num = num
        self.nodes = nodes
        self.attr = attr
        self.segs = []

    def area(self):
        temp = 0.
        if self.segs != None and len(self.segs) > 2:
            for seg in self.segs:
                arrTemp = seg.i
                arrTemp1 = seg.j
                temp = temp + 0.5 * (arrTemp.X * arrTemp1.Y -
                                     arrTemp1.X * arrTemp.Y)
        self.A = abs(temp)
        return temp

    def centroid(self):
        if self.segs != None and len(self.segs) > 2:
            area = self.area()
            temp = Point3d()
            for seg in self.segs:
                arrTemp = seg.i
                arrTemp1 = seg.j
                temp.X = temp.X + 1 / (6 * area) * (arrTemp.X + arrTemp1.X) * \
                         (arrTemp.X * arrTemp1.Y - arrTemp.Y * arrTemp1.X)
                temp.Y = temp.Y + 1 / (6 * area) * (arrTemp.Y + arrTemp1.Y) * \
                         (arrTemp.X * arrTemp1.Y - arrTemp.Y * arrTemp1.X)
            self.Centr = temp
            return temp

    def getI(self):
        if len(self.segs)<3:
            return

        tempX = 0
        tempY = 0
        for seg in self.segs:           
            arrTemp: Point3d = seg.i
            arrTemp1: Point3d = seg.j
            tempX = tempX + arrTemp.X**2 + arrTemp.X * arrTemp1.X + \
                arrTemp1.X**2 * (arrTemp.X * arrTemp1.Y -
                                 arrTemp.Y * arrTemp1.X)
            tempY = tempY + arrTemp.Y**2 + arrTemp.Y * arrTemp1.Y + \
                arrTemp1.Y**2 * (arrTemp.X * arrTemp1.Y -
                                 arrTemp.Y * arrTemp1.X)
        
        return tempX/12, tempY/12            

    def createSegments(self):
        self.segs = []
        for i in range(0, len(self.nodes) - 1):
            self.segs.append(Segment(i + 1, self.nodes[i], self.nodes[i + 1]))
        self.segs.append(
            Segment(len(self.segs) + 1, self.nodes[len(self.nodes) - 1],
                    self.nodes[0]))

    def getBoundingBox(self):
        xm = []
        ym = []
        if self.nodes == None:
            return BoundingBox()
        for node in self.nodes:
            xm.append(node.X)
            ym.append(node.Y)
        maxPt = Point3d(max(xm), max(ym))
        minPt = Point3d(min(xm), min(ym))
        self.BB = BoundingBox(minPt, maxPt)
        return self.BB

    def copy(self):
        return Contour(self.num, self.nodes.copy(), self.segs.copy())

    def triangulate(self, n=100):
        area = self.area()
        opt = 'qa' + str(round(area / n, 5))
        polynodes = []
        for i in self.nodes:
            polynodes.append((i.X, i.Y))

        vert = dict(vertices=np.array(polynodes))
        mesh = tr.triangulate(vert, opt)
        trianglesBuff = {'A': [], 'X': [], 'Y': []}

        for trgl in mesh['triangles']:
            p1 = mesh['vertices'][trgl[0]]
            p2 = mesh['vertices'][trgl[1]]
            p3 = mesh['vertices'][trgl[2]]
            s = abs(0.5 * ((p2[0] - p1[0]) * (p3[1] - p1[1]) -
                           (p3[0] - p1[0]) * (p2[1] - p1[1])))
            xm = (p1[0] + p2[0] + p3[0]) / 3
            ym = (p1[1] + p2[1] + p3[1]) / 3
            trianglesBuff['A'].append(s)
            trianglesBuff['X'].append(xm)
            trianglesBuff['Y'].append(ym)

        return trianglesBuff

    def discretization(self, xn=10, yn=10):
        bb = self.getBoundingBox()
        b = bb.maxPt.X - bb.minPt.X
        h = bb.maxPt.Y - bb.minPt.Y
        lx = list(np.linspace(bb.minPt.X, bb.maxPt.X,
                              num=xn, endpoint=False) + b / (2 * xn))
        ly = list(np.linspace(bb.maxPt.Y, bb.minPt.Y,
                              num=yn, endpoint=False) - h / (2 * yn))
        X = []
        for i in range(0, yn):
            X.append(lx)

        Y = []
        for i in range(0, xn):
            Y.append(ly)

        return np.array(X).reshape(xn * yn, ), np.array(Y).T.reshape(xn * yn, ), (b / xn) * (h / yn)


# %%


class Basis:
    def __init__(self, e1=0., e2=0., e3=0., b=0., h=0.):
        self.ε1 = Point3d(b / 2, -h / 2, e1)
        self.ε2 = Point3d(b / 2, h / 2, e2)
        self.ε3 = Point3d(-b / 2, h / 2, e3)

    def eps(self, x: float, y: float):
        pl = Plane(self.ε1, self.ε2, self.ε3)
        return pl.inerpolate(x, y)

    def epsCntr(self, cnt: Contour):
        pl = Plane(self.ε1, self.ε2, self.ε3)
        for i in range(0, len(cnt.nodes)):
            cnt.nodes[i].Z = pl.inerpolate(cnt.nodes[i].X, cnt.nodes[i].Y)
            cnt.nodes[i].attr['eps'] = cnt.nodes[i].Z
            cnt.createSegments()
        return cnt


# %%


class ArmTmpl_3x3:
    def __init__(self, ds: np.ndarray, ns=np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])):
        self.ds = ds * 0.001
        self.As = self.ds * self.ds * pi * 0.25 * ns


# %%


class CrossSect:
    loads = {'C': [], 'CL': [], 'N': [], 'NL': []}
    number: int
    contour: Contour

    def functional(self, act='C', trg=False, nt=60):
        raise NotImplementedError

    def getIb(self):
        raise NotImplementedError

    def getIs(self):
        raise NotImplementedError


# %%


class RectSect(CrossSect):
    def __init__(self, b: float, h: float, sl: float,
                 atmpl: ArmTmpl_3x3, n=10, m=10):
        self.b = b
        self.h = h
        self.sl = sl * 0.001
        self.n = n
        self.m = m
        self.As = atmpl.As
        self.Xs = np.array([[-b / 2, 0, b / 2],
                            [-b / 2, 0, b / 2],
                            [-b / 2, 0, b / 2]])
        self.Ys = np.array([[h / 2, h / 2, h / 2],
                            [0, 0, 0],
                            [-h / 2, -h / 2, -h / 2]])
        self.Xs[:, 0] = self.Xs[:, 0] + np.max(atmpl.ds[0, :]) * 0.5 + self.sl
        self.Xs[:, 2] = self.Xs[:, 2] - np.max(atmpl.ds[2, :]) * 0.5 - self.sl
        self.Ys[0, :] = self.Ys[0, :] - np.max(atmpl.ds[:, 0]) * 0.5 - self.sl
        self.Ys[2, :] = self.Ys[2, :] + np.max(atmpl.ds[:, 2]) * 0.5 + self.sl
        self.basis = Basis(0, 0, 0, b, h)
        self.beton: Beton = Beton(25, 1, 2)
        self.armatura: Armatura = Armatura('A500')
        nds = [Node(1, b / 2, -h / 2), Node(2, b / 2, h / 2),
               Node(3, -b / 2, h / 2), Node(4, -b / 2, -h / 2)]
        self.contour = Contour(1, nds)
        self.contour.createSegments()

    def setMaterials(self, bet: Beton, reinf: Armatura):
        self.beton = bet
        self.armatura = reinf

    def getIntegrateContour(self, act='C'):
        # Нахождение контура интегрирования
        pl = Plane(self.basis.ε1, self.basis.ε2, self.basis.ε3)
        for nd in self.contour.nodes:
            nd.Z = pl.inerpolate(nd.X, nd.Y)
        self.contour.createSegments()

        minEps = self.beton.epsC[0]
        if act == 'CL':
            minEps = self.beton.epsCL[0]
        elif act == 'N':
            minEps = self.beton.epsN[0]
        elif act == 'NL':
            minEps = self.beton.epsNL[0]

        nodesTemp = []
        integrateContour: Contour = self.contour.copy()
        eps = []
        for i in range(0, len(self.contour.segs)):
            eps.append(self.contour.nodes[i].Z)

        if min(eps) < minEps:
            k = 0
            for i in range(0, len(self.contour.segs)):
                se: Point3d = self.contour.segs[i].line.start.copy()
                te = se.Z
                se.Z = se.Y
                se.Y = se.X
                se.X = te
                ee: Point3d = self.contour.segs[i].line.end.copy()
                te = ee.Z
                ee.Z = ee.Y
                ee.Y = ee.X
                ee.X = te
                ln: Line2d = Line2d(se, ee)
                tpt: Point3d = ln.interpolateEps(minEps)
                l1 = Line2d(tpt, self.contour.segs[i].line.start).L
                l2 = Line2d(tpt, self.contour.segs[i].line.end).L
                l = self.contour.segs[i].line.L
                if l1 < l and l2 < l:
                    k = k + 1
                    integrateContour.nodes.insert(i + k, tpt)
            for j in range(0, len(integrateContour.nodes)):
                if integrateContour.nodes[j].Z >= minEps:
                    nodesTemp.append(integrateContour.nodes[j])
            integrateContour.nodes = nodesTemp
            integrateContour.createSegments()
            return integrateContour

    def actList(self, n, act='C'):
        res = []
        for i in range(0, n):
            res.append(act)
        return res

    def functional(self, act='C', trg=False, nt=60):
        intBA = 0.
        intBX = 0.
        intBY = 0.

        xs = self.Xs.reshape(9, )
        ys = self.Ys.reshape(9, )
        aas = self.As.reshape(9, )

        pl = Plane(self.basis.ε1, self.basis.ε2, self.basis.ε3)
        Es = list(map(pl.inerpolate, xs, ys))
        ic = self.getIntegrateContour(act)

        als = self.actList(len(Es), act)
        Ss = np.array(list(map(self.armatura.sig, Es, als)))
        Sbs = np.array(list(map(self.beton.sig, Es, als)))
        intAA = sum(Ss * aas)
        intAX = sum(Ss * aas * xs)
        intAY = sum(Ss * aas * ys)
        intBAA = sum(Sbs * aas)
        intBAX = sum(Sbs * aas * xs)
        intBAY = sum(Sbs * aas * ys)

        if trg:
            trngln = ic.triangulate(nt)
            Eb = np.array(
                list(map(pl.inerpolate, trngln['X'], trngln['Y'])))
            Sb = np.array(
                list(map(self.beton.sig, Eb, self.actList(len(Eb), act))))
            intBA = sum(Sb * trngln['A'])
            intBX = sum(Sb * trngln['A'] * trngln['X'])
            intBY = sum(Sb * trngln['A'] * trngln['Y'])
        else:
            X, Y, A = ic.discretization(self.n, self.m)
            Eb = np.array(list(map(pl.inerpolate, X, Y)))
            Sb = np.array(
                list(map(self.beton.sig, Eb, self.actList(len(X), act))))
            intBA = sum(Sb * A)
            intBX = sum(Sb * A * X)
            intBY = sum(Sb * A * Y)

        N = intBA - intBAA + intAA
        Mx = intBX - intBAX + intAX
        My = intBY - intBAY + intAY
        return N, Mx, My

    def getIb(self):
        return self.contour.getI()

    def getIs(self):
        ix = self.Xs * self.Xs * self.As
        iy = self.Ys * self.Ys * self.As
        return ix, iy        


# # %%
# ds = ArmTmpl_3x3(np.array([[20., 0., 20.], [0., 0., 0.], [20., 0., 20.]]))
# sc = RectSect(0.4, 0.6, 25., ds)
# sc.Basis.ε1.Z = -0.0008
# sc.Basis.ε2.Z = 0.0035
# sc.Basis.ε3.Z = -0.0006

# #%%
# f=sc.functional('N')
# %%
def test(arg: CrossSect):
    return arg.functional()

# %%
