from typing import Tuple
from math import cos, sin, radians

from axis import Axis


class Transformation:

    def __init__(self):

        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.sxy = 1
        self.sz = 1
        self.a = 0

    def reset(self):

        self.__init__()

    def translate(self, tx: float = 0, ty: float = 0, tz: float = 0, relative: bool = True):

        if relative:
            self.tx += tx
            self.ty += ty
            self.tz += tz
        else:
            self.tx = tx
            self.ty = ty
            self.tz = tz

    def scale(self, sxy: float = 1, sz: float = 1, relative: bool = True):

        if relative:
            self.sxy *= sxy
            self.sz *= sz
        else:
            self.sxy = sxy
            self.sz = sz

    def rotate(self, a: float = 0, relative: bool = True):
        # a: clockwise rotation angle in degrees

        if relative:
            self.a += a
        else:
            self.a = a

    def transform_xy(self, x: float, y: float) -> Tuple[float, float]:

        a = radians(-self.a)
        x = (x * cos(a) - y * sin(a)) * self.sxy + self.tx
        y = (x * sin(a) + y * cos(a)) * self.sxy + self.ty
        return x, y

    def transform_z(self, z: float) -> float:

        z = (z + self.tz) * self.sz
        return z

    def transform_r(self, r: float) -> float:

        r = r * self.sxy
        return r

    def transform(self, x: float = 0, y: float = 0, z: float = 0) -> Tuple[float, float, float]:

        x, y = self.transform_xy(x, y)
        z = self.transform_z(z)
        return x, y, z

    def transform_axis(self, axis: Axis, p: float) -> float:

        if axis == Axis.X:
            return self.transform(x=p)[0]
        elif axis == Axis.Y:
            return self.transform(y=p)[1]
        elif axis == Axis.Z:
            return self.transform(z=p)[2]
        else:
            raise ValueError(f"Invalid axis: {p}")


transformation = Transformation()
