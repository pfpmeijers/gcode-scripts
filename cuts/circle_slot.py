from math import pi

from cuts.basics import retract, approach
from utils.main import main_call

from cuts.ramp import get_ramp_rate


def mill_circle_slot(xc: float, yc: float, zb: float, zt: float, r: float):

    x = xc - r
    y = yc
    z = zt
    approach(x, y, z)
    while z > zb:
        z = mill_circle_ramp(xc, yc, z, zb, r)
    mill_circle_ramp(xc, yc, z, zb, r)


def create_circle_slot(xc: float, yc: float, zb: float, zt: float, r: float):

    retract()
    mill_circle_slot(xc, yc, zb, zt, r)
    retract()


if __name__ == "__main__":

    main_call(create_circle_slot)


def mill_arc_ramp(x: float, y: float, z: float, zb: float, r: float, d: float, ramp_length: float, ramp_rate: int, clockwise: bool = True) -> float:

    z = max(z - gcode.MILL.DEPTH_OF_CUT * d / ramp_length, zb)
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
