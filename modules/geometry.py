import numpy as np
from math import sqrt

# %%


class Point3d:
    def __init__(self, x=0., y=0., z=0.):
        self.X = x
        self.Y = y
        self.Z = z

    def toList(self):
        return [self.X, self.Y, self.Z]

    def copy(self):
        return Point3d(self.X, self.Y, self.Z)

# %%


class Vector3d:
    def __init__(self, pt1: Point3d, pt2: Point3d):
        self.vX = pt2.X - pt1.X
        self.vY = pt2.Y - pt1.Y
        self.vZ = pt2.Z - pt1.Z
        self.norma = sqrt(self.vX ** 2 + self.vY ** 2 + self.vZ ** 2)

    def toList(self):
        return [self.vX, self.vY, self.vZ]

    def toNumpy(self):
        return np.array([self.vX, self.vY, self.vZ])

# %%


class Plane:
    def __init__(self, pt1: Point3d, pt2: Point3d, pt3: Point3d):
        V1 = Vector3d(pt1, pt2)
        V2 = Vector3d(pt1, pt3)

        self.A = V1.vY * V2.vZ - V1.vZ * V2.vY
        self.B = V1.vZ * V2.vX - V1.vX * V2.vZ
        self.C = V1.vX * V2.vY - V1.vY * V2.vX
        self.D = -self.A * pt1.X - self.B * pt1.Y - self.C * pt1.Z

    def inerpolate(self, x: float, y: float):
        return (-self.A * x - self.B * y - self.D) / self.C

# %%


class Line2d:
    def __init__(self, pt1: Point3d, pt2: Point3d):
        self.start = pt1
        self.end = pt2
        self.V = Vector3d(pt1, pt2)
        self.A = pt1.Y - pt2.Y
        self.Az = pt1.Z - pt2.Z
        self.B = pt2.X - pt1.X
        self.C = pt1.X * pt2.Y - pt1.Y * pt2.X
        self.Cz = pt1.X * pt2.Z - pt1.Z * pt2.X
        self.L = sqrt(self.A * self.A + self.B * self.B)

    def interpolate(self, x):
        if self.B == 0.:
            return np.inf
        return (-self.A * x - self.C) / self.B

    def __interpolateY(self, x: float):
        if self.B == 0.:
            return np.inf
        return (-self.A * x - self.C) / self.B

    def __interpolateZ(self, x: float):
        if self.B == 0.:
            return np.inf
        return (-self.Az * x - self.Cz) / self.B

    def interpolateEps(self, x):
        return Point3d(self.__interpolateY(x), self.__interpolateZ(x), x)

# %%


class Line3d:
    def __init__(self, pt1: Point3d, pt2: Point3d):
        self.start = pt1
        self.end = pt2
        self.V = Vector3d(pt1, pt2)
        self.A = pt1.Y - pt2.Y
        self.Az = pt1.Z - pt2.Z
        self.B = pt2.X - pt1.X
        self.C = pt1.X * pt2.Y - pt1.Y * pt2.X
        self.Cz = pt1.X * pt2.Z - pt1.Z * pt2.X
        self.L = sqrt(self.A * self.A + self.B * self.B)

    def ____interpolateY(self, x: float):
        if self.B == 0.:
            return np.inf
        return (-self.A * x - self.C) / self.B

    def ____interpolateZ(self, x: float):
        if self.B == 0.:
            return np.inf
        return (-self.Az * x - self.Cz) / self.B

    def interpolate(self, x):
        y = self.____interpolateY(x)
        z = self.____interpolateZ(x)
        return y, z

    def interpolatePoint(self, x):
        return Point3d(x, self.____interpolateY(x), self.____interpolateZ(x))


# %%
