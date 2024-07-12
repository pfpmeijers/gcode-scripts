import config

from utils.polar import pi
from gcode import mill_line, mill_arc
from state import state
from utils.rect import get_sorted_rect_corners


def get_ramp_rate(ramp_length: float) -> int:

    return min(config.FEED_RATE, int(ramp_length / config.DEPTH_OF_CUT * config.PLUNGE_RATE))


def mill_line_ramp(x: float, y: float, z: float, zb: float, d: float, ramp_length: float, ramp_rate: int) -> float:

    z = max(z - config.DEPTH_OF_CUT * d / ramp_length, zb)
    mill_line(x, y, z, ramp_rate)
    return z


def mill_rect_ramp(xl: float, xr: float, yf: float, yb: float, z: float, zb: float) -> float:

    dx = xr - xl
    dy = yb - yf
    ramp_length = 2 * dx + 2 * dy
    ramp_rate = get_ramp_rate(ramp_length)

    corners = get_sorted_rect_corners(xl, xr, yf, yb)
    px = corners[3][0]
    for x, y in corners:
        d = dx if x != px else dy
        z = mill_line_ramp(x, y, z, zb, d, ramp_length, ramp_rate)
        px = x

    return z


def mill_arc_ramp(x: float, y: float, z: float, zb: float, r: float, d: float, ramp_length: float, ramp_rate: int, clockwise: bool = True) -> float:

    z = max(z - config.DEPTH_OF_CUT * d / ramp_length, zb)
    mill_arc(x, y, z, r, clockwise, ramp_rate)

    return z


def mill_circle_ramp(xc: float, yc: float, z: float, zb: float, r: float) -> float:

    # TODO: Optimize direction
    dr = 2 * pi * r / 4
    ramp_length = 4 * dr
    ramp_rate = get_ramp_rate(ramp_length)
    z = mill_arc_ramp(xc, yc + r, z, zb, r, dr, ramp_length, ramp_rate)
    z = mill_arc_ramp(xc + r, yc, z, zb, r, dr, ramp_length, ramp_rate)
    z = mill_arc_ramp(xc, yc - r, z, zb, r, dr, ramp_length, ramp_rate)
    z = mill_arc_ramp(xc - r, yc, z, zb, r, dr, ramp_length, ramp_rate)

    return z
