from typing import Tuple
from math import cos, sin, radians

from Axis import Axis


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

    def scale(self, sxy: float = 1, sz: float = 1, cumulative: bool = True):

        if sz <= 0:
            raise ValueError('z scaling factor must be larger than 0')

        if cumulative:
            self.sxy *= sxy
            self.sz *= sz
        else:
            self.sxy = sxy
            self.sz = sz

    def rotate_xy(self, a: float = 0, cumulative: bool = True):
        # a: clockwise rotation angle in degrees

        if cumulative:
            self.a += a
        else:
            self.a = a

    def transform_xy(self, x: float, y: float) -> Tuple[float, float]:

        if x is None or y is None:
            xt = yt = None
        else:
            a = radians(-self.a)
            xt = (x * cos(a) - y * sin(a)) * self.sxy + self.tx
            yt = (x * sin(a) + y * cos(a)) * self.sxy + self.ty
        return xt, yt

    def transform_z(self, z: float) -> float:

        if z is None:
            zt = None
        else:
            zt = (z + self.tz) * self.sz
        return zt

    def inverse_transform_z(self, zt: float) -> float:

        if zt is None:
            z = None
        else:
            z = zt / self.sz - self.tz
        return z

    def transform_r(self, r: float) -> float:

        r *= self.sxy
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
