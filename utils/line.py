from math import sqrt
from typing import Tuple

import config


def get_normalized_direction(xb: float, xe: float, yb: float, ye: float) -> Tuple[float, float]:

    dx = xe - xb
    dy = ye - yb
    d = sqrt(dx ** 2 + dy ** 2)
    if d == 0:
        raise ValueError("Cannot normalize line direction if it has no length")
    dx /= d
    dy /= d

    return dx, dy


def expand_line(xb: float, xe: float, yb: float, ye: float,
                expand: float = None) -> Tuple[float, float, float, float]:

    if expand is not None:
        expand -= config.MILL_DIAMETER / 2
        dx, dy = get_normalized_direction(xb, xe, yb, ye)
        xb -= expand * dx
        xe += expand * dx
        yb -= expand * dy
        ye += expand * dy

    return xb, xe, yb, ye


def expand_rect(xl: float, xr: float, yf: float, yb: float,
                contract_mill_radius = False,
                expand: float = 0) -> Tuple[float, float, float, float]:
    """
    Adjusts a set of xy-plane rectangle coordinates by means of contracting the mill radius and/or expanding all sides
    outward.

    :param xl: Left side coordinate of the rectangle.
    :param xr: Right side coordinate of the rectangle.
    :param yf: Front side coordinate of the rectangle.
    :param yb: Back side coordinate of the rectangle.
    :param contract_mill_radius: Contract the rectangle coordinates with the mill radius.
    :param expand: The amount to expand the rectangle on all sides outward.
    :return: Adjusted rectangle coordinates.
    """

    if contract_mill_radius:
        expand -= config.MILL_DIAMETER / 2
    xl -= expand
    xr += expand
    yf -= expand
    yb += expand

    return xl, xr, yf, yb


def shift_line(xb: float, xe: float, yb: float, ye: float, shift: float = 0) -> Tuple[float, float, float, float]:

    if shift != 0:
        dx, dy = get_normalized_direction(xb, xe, yb, ye)
        xb += shift * dy
        xe += shift * dy
        yb -= shift * dx
        ye -= shift * dx

    return xb, xe, yb, ye


