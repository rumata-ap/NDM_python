import numpy as np
from geometry import point3d, line2d

# %%


class linterp1d:
    def __init__(self, x: list, y: list):
        self.x = x
        self.y = y

    def linterp(self, val):
        if type(val) == float or type(val) == int:
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
                            pt2: point3d = point3d(
                                self.x[i + 1], self.y[i + 1])
                            ln = line2d(pt1, pt2)
                            resList.append(ln.interpolateY(v))
            return resList
