from typing import Tuple

import config
from basics import retract, approach, plunge
from state import state
from utils.main import main_call
from utils.constraints import check_coordinate_constraints
from ramp import mill_rect_ramp
from line_slot import mill_tabbed_line_slot
from utils.rect import get_closest_rect_corner


def mill_rect_slot(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float):

    check_coordinate_constraints(xl, xr, yf, yb, zb, zt)
    x0, y0 = get_closest_rect_corner(xl, xr, yf, yb)
    if (state.x, state.y) != (x0, y0):
        raise ValueError("Function assumes current position already to be at closest rect corner.")
    x, y, z = x0, y0, zt

    if zt - zb > config.DEPTH_OF_CUT:
        approach(x, y, z)
        while z > zb:
            z = mill_rect_ramp(xl, xr, yf, yb, z, zb)
    else:
        if state.z > z:
            approach(x, y, z)
        z = zb
        if state.z > z:
            plunge(zb)
    mill_rect_ramp(xl, xr, yf, yb, z, zb)


def mill_tabbed_rect_slot(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float):

    check_coordinate_constraints(xl, xr, yf, yb, zb, zt)

    dt = mill_tabbed_line_slot(xl, xr, yf, yf, zb, zt)
    dt = mill_tabbed_line_slot(xl, xl, yf, yb, zb, zt, dt)
    dt = mill_tabbed_line_slot(xr, xl, yb, yb, zb, zt, dt)
    mill_tabbed_line_slot(xl, xl, yb, yf, zb, zt, dt)


def create_rect_slot(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float, tabs: bool = False):

    retract()
    if tabs:
        mill_tabbed_rect_slot(xl, xr, yf, yb, zb, zt)
    else:
        mill_rect_slot(xl, xr, yf, yb, zb, zt)
    retract()


if __name__ == "__main__":

    main_call(create_rect_slot)
