from math import sqrt, pi, atan, sin, cos
from typing import Tuple

from utils.misc import normalize


def to_polar(x: float, y: float, xc: float = 0, yc: float = 0) -> Tuple[float, ...]:

    x -= xc
    y -= yc
    r = sqrt(x ** 2 + y ** 2)
    if x == 0:
        a = pi / 2 if y >= 0 else pi * 3 / 2
    else:
        a = atan(y / x) + (pi if x < 0 else 0)
        if a < 0:
            a += 2 * pi

    return r, a


def from_polar(r: float, a: float, xc: float = 0, yc: float = 0) -> Tuple[float, ...]:

    return r * cos(a) + xc, r * sin(a) + yc


def get_angle_delta(a1: float, a2: float) -> float:

    da = abs(a1 - a2)
    if da > pi:
        da = 2 * pi - da

    return da


def shift_radial(x: float, y: float, xc: float, yc: float, dr: float) -> Tuple[float, float]:

    dx, dy = normalize(xc, x, yc, y)
    x += dr * dx
    y += dr * dy

    return x, y
