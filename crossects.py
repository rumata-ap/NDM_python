# %%
import matplotlib.pyplot as plt
import triangle as tr
from geometry import *
from armSelector import *
from betonSelector import *
from math import pi
import numpy as np
# import triangle
# from scipy.integrate import dblquad
# from sympy.integrals.intpoly import *
#from sympy import Point, Polygon, Float

# %%


class interp1d:
    def __init__(self, x: list, y: list):
        self.x = x
        self.y = y

    def linterp(self, val):
        if type(val)==float or type(val)==int:
            if val < self.x[0]:
                pt1: point3d = point3d(self.x[0], self.y[0])
                pt2: point3d = point3d(self.x[1], self.y[1])
                ln = line2d(pt1, pt2)
                return ln.interpolateY(val)
            elif val >= self.x[len(self.x)-1]:
                pt1: point3d = point3d(
                    self.x[len(self.x)-2], self.y[len(self.x)-2])
                pt2: point3d = point3d(
                    self.x[len(self.x)-1], self.y[len(self.x)-1])
                ln = line2d(pt1, pt2)
                return ln.interpolateY(val)
            else:
                for i in range(0, len(self.x) - 1):
                    if val >= self.x[i] and val < self.x[i+1]:
                        pt1: point3d = point3d(self.x[i], self.y[i])
                        pt2: point3d = point3d(self.x[i + 1], self.y[i + 1])
                        ln = line2d(pt1, pt2)
                        return ln.interpolateY(val)
        elif type(val) == list or type(val) == np.ndarray:
            resList = []
            for v in val:
                if v < self.x[0]:
                    pt1: point3d = point3d(self.x[0], self.y[0])
                    pt2: point3d = point3d(self.x[1], self.y[1])
                    ln = line2d(pt1, pt2)
                    resList.append(ln.interpolateY(v))
                elif v >= self.x[len(self.x)-1]:
                    pt1: point3d = point3d(
                        self.x[len(self.x)-2], self.y[len(self.x)-2])
                    pt2: point3d = point3d(
                        self.x[len(self.x)-1], self.y[len(self.x)-1])
                    ln = line2d(pt1, pt2)
                    resList.append(ln.interpolateY(v))
                else:
                    for i in range(0, len(self.x) - 1):
                        if v >= self.x[i] and v < self.x[i+1]:
                            pt1: point3d = point3d(self.x[i], self.y[i])
                            pt2: point3d = point3d(self.x[i + 1], self.y[i + 1])
                            ln = line2d(pt1, pt2)
                            resList.append(ln.interpolateY(v))
            return resList    

    def linterpList(self, arr: list):
        return list(map(self.linterp, arr))

# %%

class node(point3d):
    def __init__(self, num=0, x=0., y=0., z=0., attr={}):
        point3d.__init__(self, x, y, z)
        self.id = num
        self.attr = attr

    def fromPoint3d(self, pt: point3d):
        self.X = pt.X
        self.Y = pt.Y
        self.Z = pt.Z


# %%


class segment:
    def __init__(self, num: int, i: point3d, j: point3d, attr={}):
        self.i = i
        self.j = j
        self.attr = attr
        self.num = num
        self.line = line2d(i, j)


class boundingBox:
    def __init__(self, minp=point3d(), maxp=point3d()):
        self.minPt = minp
        self.maxPt = maxp


# %%


class contour:
    def __init__(self, num: int, nodes=[], attr={}):
        self.num = num
        self.nodes = nodes
        self.attr = attr

    def area(self):
        temp = 0.
        if self.segs != None and len(self.segs) > 2:
            for seg in self.segs:
                arrTemp = seg.i
                arrTemp1 = seg.j
                temp = temp + 0.5*(arrTemp.X * arrTemp1.Y -
                                   arrTemp1.X * arrTemp.Y)
        self.A = abs(temp)
        return temp

    def centroid(self):
        if self.segs != None and len(self.segs) > 2:
            area = self.area()
            temp = point3d()
            for seg in self.segs:
                arrTemp = seg.i
                arrTemp1 = seg.j
                temp.X = temp.X + 1 / (6 * area) * (arrTemp.X + arrTemp1.X) * \
                    (arrTemp.X * arrTemp1.Y - arrTemp.Y * arrTemp1.X)
                temp.Y = temp.Y + 1 / (6 * area) * (arrTemp.Y + arrTemp1.Y) * \
                    (arrTemp.X * arrTemp1.Y - arrTemp.Y * arrTemp1.X)
            self.Centr = temp
            return temp

    def createSegments(self):
        self.segs = []
        for i in range(0, len(self.nodes)-1):
            self.segs.append(segment(i + 1, self.nodes[i], self.nodes[i + 1]))
        self.segs.append(
            segment(len(self.segs) + 1, self.nodes[len(self.nodes)-1],
                    self.nodes[0]))

    def getBoundingBox(self):
        xm = []
        ym = []
        if self.nodes == None:
            return boundingBox()
        for node in self.nodes:
            xm.append(node.X)
            ym.append(node.Y)
        maxPt = point3d(max(xm), max(ym))
        minPt = point3d(min(xm), min(ym))
        self.BB = boundingBox(minPt, maxPt)
        return self.BB

    def copy(self):
        return contour(self.num, self.nodes.copy(), self.segs.copy())

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
                              num=xn, endpoint=False)+b/(2*xn))
        ly = list(np.linspace(bb.maxPt.Y, bb.minPt.Y,
                              num=yn, endpoint=False)-h/(2*yn))
        X = []
        for i in range(0, yn):
            X.append(lx)

        Y = []
        for i in range(0, xn):
            Y.append(ly)

        return np.array(X).reshape(xn*yn,), np.array(Y).T.reshape(xn*yn,), (b / xn) * (h / yn)


# %%


class basis:
    def __init__(self, e1=0., e2=0., e3=0., b=0., h=0.):
        self.ε1 = point3d(b / 2, -h / 2, e1)
        self.ε2 = point3d(b / 2, h / 2, e2)
        self.ε3 = point3d(-b / 2, h / 2, e3)

    def eps(self, x: float, y: float):
        pl = plane(self.ε1, self.ε2, self.ε3)
        return pl.inerpolate(x, y)

    def epsCntr(self, cnt: contour):
        pl = plane(self.ε1, self.ε2, self.ε3)
        for i in range(0, len(cnt.nodes)):
            cnt.nodes[i].Z = pl.inerpolate(cnt.nodes[i].X, cnt.nodes[i].Y)
            cnt.nodes[i].attr['eps'] = cnt.nodes[i].Z
            cnt.createSegments()
        return cnt


# %%


class armTmpl_3x3:
    def __init__(self, ds: np.ndarray, ns=np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])):
        self.ds = ds*0.001
        self.As = self.ds * self.ds * pi * 0.25 * ns


# %%


class rectSect:
    def __init__(self, b: float, h: float, sl: float,
                 atmpl: armTmpl_3x3, n=10, m=10):
        self.b = b
        self.h = h
        self.sl = sl*0.001
        self.n = n
        self.m = m
        self.As = atmpl.As
        self.Xs = np.array([[-b/2, 0, b/2],
                            [-b/2, 0, b/2],
                            [-b/2, 0, b/2]])
        self.Ys = np.array([[h/2, h/2, h/2],
                            [0, 0, 0],
                            [-h/2, -h/2, -h/2]])
        self.Xs[:, 0] = self.Xs[:, 0] + np.max(atmpl.ds[0, :]) * 0.5 + self.sl
        self.Xs[:, 2] = self.Xs[:, 2] - np.max(atmpl.ds[2, :]) * 0.5 - self.sl
        self.Ys[0, :] = self.Ys[0, :] - np.max(atmpl.ds[:, 0]) * 0.5 - self.sl
        self.Ys[2, :] = self.Ys[2, :] + np.max(atmpl.ds[:, 2]) * 0.5 + self.sl
        self.basis = basis(0, 0, 0, b, h)
        nds = [node(1, b / 2, -h / 2), node(2, b / 2, h / 2),
               node(3, -b / 2, h / 2), node(4, -b / 2, -h / 2)]
        self.contour = contour(1, nds)
        self.contour.createSegments()

    def getIntegrateContour(self, act='C',
                            diagB=diagrB(25, 1, 2), diagA=diagrA('A400')):
        # Нахождение контура интегрирования
        self.beton = diagB
        self.armatura = diagA
        minEps = self.beton.epsC[0]

        if act == 'CL':
            minEps = self.beton.epsCL[0]
        elif act == 'N':
            minEps = self.beton.epsN[0]
        elif act == 'NL':
            minEps = self.beton.epsNL[0]

        nodesTemp = []
        integrateContour: contour = self.contour.copy()
        eps = []
        for i in range(0, len(self.contour.segs)):
            eps.append(self.contour.nodes[i].Z)

        if min(eps) < minEps:
            k = 0
            for i in range(0, len(self.contour.segs)):
                se: point3d = self.contour.segs[i].line.start.copy()
                te = se.Z
                se.Z = se.Y
                se.Y = se.X
                se.X = te
                ee: point3d = self.contour.segs[i].line.end.copy()
                te = ee.Z
                ee.Z = ee.Y
                ee.Y = ee.X
                ee.X = te
                ln: line2d = line2d(se, ee)
                tpt: point3d = ln.interpolateEps(minEps)
                l1 = line2d(tpt, self.contour.segs[i].line.start).L
                l2 = line2d(tpt, self.contour.segs[i].line.end).L
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
    
    def functional(self, act='C', trg=False,nt=60):
        intBA = 0.
        intBAA = 0.
        intAA = 0.
        intBX = 0.
        intBAX = 0.
        intBY = 0.
        intBAY = 0.
        intAY = 0.
        intAX = 0.

        interpB = interp1d(self.beton.epsC, self.beton.sigC)
        if act == 'CL':
            interpB = interp1d(self.beton.epsCL, self.beton.sigCL)
        elif act == 'N':
            interpB = interp1d(self.beton.epsN, self.beton.sigN)
        elif act == 'NL':
            interpB = interp1d(self.beton.epsNL, self.beton.sigNL)

        pl = plane(self.basis.ε1, self.basis.ε2, self.basis.ε3)
        ic = self.getIntegrateContour(act, self.beton, self.armatura)
        if trg:
            trngln = ic.triangulate(nt)
            Et = list(map(pl.inerpolate, trngln['X'], trngln['Y']))
            St = interpB.linterp(Et)
            intBA = sum(list(np.array(St) * trngln['A']))
        else:
            X, Y, A = ic.discretization(self.n, self.m)
            E = list(map(pl.inerpolate, X, Y))
            S = []
            for row in E:
                tmp = []
                for vl in row:
                    if act=='C':
                        tmp.append(self.beton.sig(vl)[0])
                    elif act == 'CL':
                        tmp.append(self.beton.sig(vl)[1])
                    elif act == 'N':
                        tmp.append(self.beton.sig(vl)[2])
                    elif act == 'NL':
                        tmp.append(self.beton.sig(vl)[3])
                S.append(tmp)
            intBA = sum(sum(list(np.array(S)*A)))


# %%


def functional1(sec: rectSect, diagB: diagrB = diagrB(25, 1, 2), diagA: diagrA = diagrA('A400')):
    # Нахождение контура интегрирования
    ic = sec.getIntegrateContour('C', diagB, diagA)
    def sigBA(x, y): return sig(x, y, sec.basis, diagB, diagA)[0][0]
    # intBA = float(polytope_integrate(
    # Polygon((0, 0), (0, 1), (1, 0)), sigBA(x, y)))
    intBAA = 0.
    intAA = 0.
    intBX = 0.
    intBAX = 0.
    intBY = 0.
    intBAY = 0.
    intAY = 0.
    intAX = 0.
    return ic


# %%
ds = armTmpl_3x3(np.array([[20., 0., 20.], [0., 0., 0.], [20., 0., 20.]]))
sc = rectSect(0.4, 0.6, 25., ds)
sc.basis.ε1.Z = -0.0008
sc.basis.ε2.Z = 0.0035
sc.basis.ε3.Z = -0.0006
sc.contour = sc.basis.epsCntr(sc.contour)
icnt = functional1(sc, diagrB(25, 1, 2))
interpolant = interp1d(diagrB(25, 1, 2).epsC, diagrB(25, 1, 2).sigC)
pl = plane(sc.basis.ε1, sc.basis.ε2, sc.basis.ε3)

X, Y, A = icnt.discretization()
E = list(map(pl.inerpolate, X, Y))
S = []
for row in E:
    tmp = []
    for vl in row:
        tmp.append(diagrB(25, 1, 2).sig(vl)[0])
    S.append(tmp)



ar = icnt.area()
trngln = icnt.triangulate(n=60)
Et = list(map(pl.inerpolate, trngln['X'], trngln['Y']))
St = interpolant.linterpList(Et)

polynodes = []
for i in icnt.nodes:
    polynodes.append((i.X, i.Y))
p1, p2, p3 = map(Point, polynodes)
polygon = Polygon(p1, p2, p3)
A = float(polygon.area)
opt = 'qa' + str(round(A/60, 4))
vert = dict(vertices=np.array(polynodes))
mesh = tr.triangulate(vert, opt)


trianglesBuff = {'A': [], 'X': [], 'Y': [], 'eps': [], 'sig': []}
for trgl in mesh['triangles']:
    # p1 = Point((mesh['vertices'][trgl[0]]))
    # p2 = Point((mesh['vertices'][trgl[1]]))
    # p3 = Point((mesh['vertices'][trgl[2]]))
    # polygon = Polygon(p1, p2, p3)
    # centr = polygon.centroid
    p1 = mesh['vertices'][trgl[0]]
    p2 = mesh['vertices'][trgl[1]]
    p3 = mesh['vertices'][trgl[2]]
    s = abs(0.5 * ((p2[0] - p1[0]) * (p3[1] - p1[1]) -
                   (p3[0] - p1[0]) * (p2[1] - p1[1])))
    xm = (p1[0] + p2[0] + p3[0]) / 3
    ym = (p1[1] + p2[1] + p3[1]) / 3
    eps = pl.inerpolate(xm, ym)
    trianglesBuff['A'].append(s)
    trianglesBuff['X'].append(xm)
    trianglesBuff['Y'].append(ym)
    trianglesBuff['eps'].append(eps)
    trianglesBuff['sig'].append(interpolant.linterp(eps))

stress = list(map(lambda x, y: x*y, trianglesBuff['sig'], trianglesBuff['A']))


def linterp(x: list, y: list, val):
    if val < x[0]:
        pt1: point3d = point3d(x[0], y[0])
        pt2: point3d = point3d(x[1], y[1])
        ln = line2d(pt1, pt2)
        return ln.interpolateY(val)
    elif val >= x[len(x)-1]:
        pt1: point3d = point3d(x[len(x)-2], y[len(x)-2])
        pt2: point3d = point3d(x[len(x)-1], y[len(x)-1])
        ln = line2d(pt1, pt2)
        return ln.interpolateY(val)
    else:
        for i in range(0, len(x) - 1):
            if val >= x[i] and val < x[i+1]:
                pt1: point3d = point3d(x[i], y[i])
                pt2: point3d = point3d(x[i + 1], y[i + 1])
                ln = line2d(pt1, pt2)
                return ln.interpolateY(val)


intBA = sum(stress)

# %%


def sig(x: float, y: float, base: basis, diagB: diagrB, diagA: diagrA):
    pl = plane(base.ε1, base.ε2, base.ε3)
    eps = pl.inerpolate(x, y)
    return [diagB.sig(eps), diagA.sig(eps)]
