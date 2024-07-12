from math import dist
from typing import Tuple, List, Optional

from transformation import transformation
from utils.misc import swap


class State:

    def __init__(self):

        # Original non-transformed state
        self.x = 0
        self.y = 0
        self.z = 0
        self.zl = 0

        # Lazy (delayed) z change
        self.zlt = 0

        # Transformed state
        self.xt = 0
        self.yt = 0
        self.zt = 0

    def update(self, x: float = None, y: float = None, z: float = None) -> bool:

        if x is None:
            x = state.x
        if y is None:
            y = state.y
        if z is None:
            z = state.z
        xt, yt, zt = transformation.transform(x, y, z)
        updated = False
        if xt != self.xt:
            updated = True
            self.xt = xt
            self.x = x
        if yt != self.yt:
            updated = True
            self.yt = yt
            self.y = y
        if zt != self.zt:
            updated = True
            self.zt = zt
            self.z = z
        return updated

    def lazy_z_change(self, z: float):

        zt = transformation.transform_z(z)
        if zt != self.zt:
            self.zl = z

    def pop_lazy_z_change(self, x: float = None, y: float = None) -> Optional[float]:

        if x is None:
            x = state.x
        if y is None:
            y = state.y
        xt, yt = transformation.transform_xy(x, y)
        zl = None
        if self.zl != 0:
            if xt != self.xt or yt != self.yt:
                zl = state.zl
            state.zlt = 0
            state.zl = 0
        return zl

    def get_xy_distance(self, x: float = None, y: float = None) -> float:

        xt, yt = transformation.transform_xy(x, y)
        return dist((xt, yt), (self.xt, self.yt))

    def get_closest(self, points: List[Tuple[float, float]]) -> Tuple[int, Tuple[float, float]]:

        a = []
        for i, p in enumerate(points):
            a.append((self.get_xy_distance(*p), i, p))
        a = sorted(a)
        return a[0][1:3]

    def swap_to_closest_xy(self, xb: float, xe: float, yb: float, ye: float, clockwise: bool = None) -> Tuple[float, float, float, float, bool]:

        if self.get_xy_distance(xb, yb) > self.get_xy_distance(xe, ye):
            xb, xe = swap(xb, xe)
            yb, ye = swap(yb, ye)
            if clockwise is not None:
                clockwise = not clockwise
        return xb, xe, yb, ye, clockwise

    def is_below(self, z: float) -> bool:

        return transformation.transform_z(z) < self.z


state = State()
