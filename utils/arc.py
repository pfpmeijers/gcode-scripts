from math import sqrt

from utils.polar import shift_radial, to_polar, from_polar


def get_arc_center(xb: float, xe: float, yb: float, ye: float, r: float, clockwise: bool) -> tuple[float, float]:

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


def expand_arc(xc: float, xb: float, xe: float, yc: float, yb: float, ye: float,
               r: float, clockwise: bool,
               expand: float) \
        -> tuple[float, float, float, float]:

    if expand:
        rb, ab = to_polar(xb - xc, yb - yc)
        re, ae = to_polar(xe - xc, ye - yc)
        da = expand / r
        # clockwise indicates the orientation between the arc's begin and end point.
        # Polar coordinate angles increase counter-clockwise.
        # Hence, when expanding a clockwise arc, then the begin angle needs to increase and end angle decrease.
        dab = da if clockwise else -da
        dae = -da if clockwise else da
        xb, yb = from_polar(r, ab + dab, xc, yc)
        xe, ye = from_polar(r, ae + dae, xc, yc)

    return xb, xe, yb, ye


def shift_arc(xc: float, xb: float, xe: float, yc: float, yb: float, ye: float,
              r: float,
              shift: float) \
        -> tuple[float, float, float, float, float]:

    if shift:
        xb, yb = shift_radial(xb, yb, xc, yc, shift)
        xe, ye = shift_radial(xe, ye, xc, yc, shift)
        r += shift

    return xb, xe, yb, ye, r
