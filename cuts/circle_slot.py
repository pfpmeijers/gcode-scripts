from math import pi

from GCode import GCode
from cuts.arc_slot import mill_arc_ramp, mill_arc_slot


def mill_circle_ramp(gcode: GCode,
                     xc: float, yc: float, zb: float, z: float,
                     r: float) \
        -> float:

    gcode.verify_position(xc - r, yc, z)

    d = 2 * pi * r
    ramp_rate = gcode.get_ramp_rate(d)
    z = mill_arc_ramp(gcode, xc + r, yc, zb, z, r, ramp_fraction=0.5, feed_rate=ramp_rate)
    z = mill_arc_ramp(gcode, xc - r, yc, zb, z, r, ramp_fraction=0.5, feed_rate=ramp_rate)

    return z


def mill_circle_slot(gcode: GCode,
                     xc: float, yc: float, zb: float, zt: float,
                     r: float,
                     tabs: bool = False):

    x, y, z = xc - r, yc, zt
    gcode.approach(x, y, z)

    if tabs:
        zbt = zb + gcode.tab_height
        if zt > zbt:
            mill_circle_slot(gcode, xc, yc, zbt, zt, r)
            zt = zbt

        dt = 0
        dt = mill_arc_slot(gcode, xc - r, xc + r, yc, yc, zb, zt, r, start_closest=False, tabs=True, dt=dt)
        __ = mill_arc_slot(gcode, xc + r, xc - r, yc, yc, zb, zt, r, start_closest=False, tabs=True, dt=dt)

    else:
        while z > zb:
            z = mill_circle_ramp(gcode, xc, yc, zb, z, r)
        mill_circle_ramp(gcode, xc, yc, zb, z, r)
