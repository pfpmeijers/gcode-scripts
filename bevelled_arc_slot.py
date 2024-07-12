from math import cos, sin, tan, radians, ceil

import config
from basics import cancel_retract
from state import state
from gcode import mill_line
from arc_slot import create_arc_slot
from utils.arc import get_arc_center
from utils.main import main_call
from utils.misc import normalize


# TODO: Remove clockwise param. Let user swap coordinates if counter-clockwise is needed.
def get_bevel_steps(xb: float, xe: float, yb: float, ye: float, r: float, clockwise: bool,
                    zb: float, zt: float,
                    bevel_angle: float, ddz: float):

    # Calculate initial radial and height displacement and step sizes.
    # TODO: Take the mill corner diameter into account. Currently it is assumed to be same as mill diameter.
    assert config.MILL_CORNER_DIAMETER == config.MILL_DIAMETER
    a = radians(90 - bevel_angle)
    ddr = tan(a) * ddz  # Displacement step in radial direction
    dr0 = -cos(a) * config.MILL_DIAMETER / 2  # Initial displacement in radial direction
    dz0 = (sin(a) - 1) * config.MILL_DIAMETER / 2  # Initial displacement in z direction

    # Translate radial displacements into cartesian displacements at both arc ends.
    xc, yc = get_arc_center(xb, xe, yb, ye, r, clockwise)
    dxb, dyb = normalize(xc, xb, yc, yb)
    dxe, dye = normalize(xc, xe, yc, ye)
    dxb0 = dr0 * dxb
    dxe0 = dr0 * dxe
    dyb0 = dr0 * dyb
    dye0 = dr0 * dye
    ddxb = ddr * dxb
    ddyb = ddr * dyb
    ddxe = ddr * dxe
    ddye = ddr * dye

    # Number of steps to take (fractional)
    f = (zt + dz0 - zb) / -ddz

    return dxb0, dxe0, ddxb, ddxe, dyb0, dye0, ddyb, ddye, dz0, f


# TODO: Move arc radius behind xy coordinates, because it related to xy and not z. Remove clockwise.
def create_bevelled_arc_slot(xb: float, xe: float, yb: float, ye: float,
                             zb: float, zt: float,
                             r: float, clockwise: bool,
                             bevel_angle: float, ddz: float):

    """
    IMPORTANT: Don't use this as a stand-alone cut.
    It will only work if the cutting height of the mill is at least the height of the slot.
    If not then make sure a sufficiently wide (perpendicular to the arc) pocket has been cut before.
    """

    dxb0, dxe0, ddxb, ddxe, dyb0, dye0, ddyb, ddye, dz0, f = \
        get_bevel_steps(xb, xe, yb, ye, r, clockwise, zb, zt, bevel_angle, ddz)

    xb0 = xb + dxb0
    xe0 = xe + dxe0
    yb0 = yb + dyb0
    ye0 = ye + dye0
    z0 = zt + dz0
    for j in range(ceil(f + 1)):
        j = min(j, f)
        xb = xb0 + j * ddxb
        xe = xe0 + j * ddxe
        yb = yb0 + j * ddyb
        ye = ye0 + j * ddye
        z = z0 + j * ddz
        if j > 0:
            cancel_retract()
            mill_line(*(state.get_closest(((xb, yb), (xe, ye)))[1]), z)
        create_arc_slot(xb, xe, yb, ye, z, z, r, clockwise)


if __name__ == "__main__":

    main_call(create_bevelled_arc_slot)
