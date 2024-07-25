from math import dist
from typing import Optional

from Transformation import transformation
from utils.misc import swap


class RouterState:

    def __init__(self):

        # Original non-transformed state
        self.x = None
        self.y = None
        self.z = None

        # Lazy (delayed) z change
        self.zl = None

        # Transformed state
        self.xt = None
        self.yt = None
        self.zt = None

    def reset(self):
        self.__init__()

    def update(self, x: float = None, y: float = None, z: float = None) -> bool:

        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if z is None:
            z = self.z
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
            x = self.x
        if y is None:
            y = self.y
        xt, yt = transformation.transform_xy(x, y)
        zl = None
        if self.zl != 0:
            if xt != self.xt or yt != self.yt:  # New xy position, thus first do the postponed (lazy) z change.
                zl = self.zl
            self.zl = 0
        return zl

    def get_xy_distance(self, x: float = None, y: float = None) -> float:

        xt, yt = transformation.transform_xy(x, y)
        return dist((xt, yt), (self.xt, self.yt))

    def is_above(self, z: float) -> bool:

        above = self.zt > transformation.transform_z(z) if self.zt is not None else None
        return above

    def get_closest_xy(self, points: list[tuple[float, float]]) -> tuple[int, tuple[float, float]]:

        distances = []
        for i, p in enumerate(points):
            distances.append((self.get_xy_distance(*p), i, p))
        distances = sorted(distances)
        return distances[0][1], distances[0][2]

    def swap_to_closest_xy(self, x1: float, x2: float, y1: float, y2: float,
                           clockwise: bool = None) \
            -> tuple[float, float, float, float, bool] | tuple[float, float, float, float]:

        if self.get_xy_distance(x1, y1) > self.get_xy_distance(x2, y2):
            x1, x2 = swap(x1, x2)
            y1, y2 = swap(y1, y2)
            if clockwise is not None:
                clockwise = not clockwise
        return (x1, x2, y1, y2, clockwise) if clockwise is not None else (x1, x2, y1, y2)
