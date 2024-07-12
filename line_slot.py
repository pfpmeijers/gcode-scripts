from math import sqrt
from typing import Tuple

import config
from gcode import goto_xy, mill_line
from state import state
from basics import retract, approach, plunge
from utils.line import expand_line, shift_line
from utils.main import main_call
from utils.misc import swap
from utils.constraints import check_z_coordinate_constraints


# TODO: Use utils.misc


def optimize_line_direction(xb: float, xe: float, yb: float, ye: float) -> Tuple[float, float, float, float]:

    if state.get_xy_distance(xb, yb) > state.get_xy_distance(xe, ye):
        xb, xe = swap(xb, xe)
        yb, ye = swap(yb, ye)

    return xb, xe, yb, ye


def mill_line_slot(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                   expand: float = None, shift: float = 0):

    check_z_coordinate_constraints(zb, zt)
    xb, xe, yb, ye = expand_line(xb, xe, yb, ye, expand)
    xb, xe, yb, ye = shift_line(xb, xe, yb, ye, shift)
    xb, xe, yb, ye = optimize_line_direction(xb, xe, yb, ye)

    x = xb
    y = yb
    z = zt
    approach(x, y, z)
    zp = None
    while True:
        z = max(z - config.DEPTH_OF_CUT, zb)
        if z == zp:
            break
        zp = z

        plunge(z)
        x = xe if x == xb else xb
        y = ye if y == yb else yb
        mill_line(x, y, z, config.FEED_RATE)


def mill_tabbed_line_slot(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                          dt: float = 0,
                          expand: float = None, shift: float = 0) -> float:
    """
    Mill an xy slot with tabs (vertical bumps upward) according to TAB_xxx settings.
    :param xb: Begin x position
    :param xe: End x position
    :param yb: Begin y position
    :param ye: End y position
    :param zb: Bottom line slot height at which the tab bumps to create. Tab tops are milled TAB_HEIGHT above zb.
    :param zt: Top line slot height
    :param dt: Distance to next tab
    :param expand: If not None, then expand the line at both ends tangential with the mill radius plus the specified expand
    :param shift: Shift the line orthogonal to the line direction
    :return: None
    """

    # TODO: This set of adjustments is common with tabbed and untabbed version. Move to common function.
    check_z_coordinate_constraints(zb, zt)
    xb, xe, yb, ye = expand_line(xb, xe, yb, ye, expand)
    xb, xe, yb, ye = shift_line(xb, xe, yb, ye, shift)
    xb, xe, yb, ye = optimize_line_direction(xb, xe, yb, ye)

    if zt > zb + config.TAB_HEIGHT:        
        mill_line_slot(xb, xe, yb, ye, zb + config.TAB_HEIGHT, zt)
    zt = zb + config.TAB_HEIGHT

    dx = xe - xb
    dy = ye - yb
    d = sqrt(dx ** 2 + dy ** 2)
    dx /= d
    dy /= d

    while d > 0:
        # Mill up to next tab
        if dt >= config.TAB_WIDTH + config.MILL_DIAMETER:
            # Go to next tab
            dd = min(d, config.TAB_DISTANCE - dt)
            if dd == 0:
                break
            d -= dd
            xe = xb + dd * dx
            ye = yb + dd * dy
            mill_line_slot(xb, xe, yb, ye, zb, zt)
            xb = xe
            yb = ye
            dt += dd
            if dt >= config.TAB_DISTANCE:
                dt = 0
        if d == 0:
            break
        if d == 0:
            break
        # Finalize or create tab (by moving over)
        dd = min(d, config.TAB_WIDTH + config.MILL_DIAMETER - dt)
        if dt == 0:
            retract(zt)
        d -= dd
        xe = xb + dd * dx
        ye = yb + dd * dy
        goto_xy(xe, ye)
        xb = xe
        yb = ye
        dt += dd

    return dt


def create_line_slot(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                     expand: float = None, shift: float = 0, tabs: bool = False):

    retract()
    if tabs:
        mill_tabbed_line_slot(xb, xe, yb, ye, zb, zt, 0, expand, shift)
    else:
        mill_line_slot(xb, xe, yb, ye, zb, zt, expand, shift)
    retract()


def create_x_line_slot(xl: float, xr: float, y: float, zb: float, zt: float,
                       expand: float = None, shift: float = 0, tabs: bool = False):

    create_line_slot(xl, xr, y, y, zb, zt, expand, shift, tabs)


def create_y_line_slot(x: float, yf: float, yb: float, zb: float, zt: float,
                       expand: float = None, shift: float = 0, tabs: bool = False):

    create_line_slot(x, x, yf, yb, zb, zt, expand, shift, tabs)


if __name__ == "__main__":

    main_call(create_line_slot)