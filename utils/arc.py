from math import sqrt
from typing import Tuple

from utils.constraints import check_z_coordinate_constraints
from utils.misc import normalize
from utils.polar import shift_radial


def get_arc_center(xb: float, xe: float, yb: float, ye: float, r: float, clockwise: bool) -> Tuple[float, float]:

    # See https://www.quora.com/How-do-we-find-the-equation-of-a-circle-when-two-points-on-it-and-the-radius-of-a-circle-are-given
    dx = xe - xb
    dy = ye - yb
    d = dx ** 2 + dy ** 2
    k = sqrt(4 * r ** 2 / d - 1)
    if clockwise:
        k = -k
    xm = (xb + xe) / 2
    ym = (yb + ye) / 2
    xc = xm + k * (yb - ym)
    yc = ym + k * (xm - xb)

    return xc, yc


def shift_arc(xc: float, xb: float, xe: float, yc: float, yb: float, ye: float, r: float, shift: float) -> Tuple[float, float, float, float, float]:

    if shift != 0:
        xb, yb = shift_radial(xb, yb, xc, yc, shift)
        xe, ye = shift_radial(xe, ye, xc, yc, shift)
        r += shift

    return xb, xe, yb, ye, r


def preprocess_arc(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float, r: float, clockwise: bool,
                   shift: float = 0.0) -> Tuple[float, float, float, float, float, float, float]:

    check_z_coordinate_constraints(zb, zt)
    xc, yc = get_arc_center(xb, xe, yb, ye, r, clockwise)
    xb, xe, yb, ye, r = shift_arc(xc, xb, xe, yc, yb, ye, r, shift)

    return xb, xe, yb, ye, xc, yc, r
