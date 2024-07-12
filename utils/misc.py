from math import dist
from typing import Tuple


def swap(a, b):
    return b, a


def normalize(xb: float, xe: float, yb: float, ye: float) -> Tuple[float, float]:

    dx = xe - xb
    dy = ye - yb
    d = dist((xb, yb), (xe, ye))
    if d == 0:
        raise ValueError("Cannot normalize vector if it has no length.")
    dx /= d
    dy /= d

    return dx, dy
