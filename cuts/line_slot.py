from math import sqrt

from GCode import GCode
from utils.line import expand_xy_line, shift_xy_line
from utils.loop import loop_z


def mill_line_slot(gcode: GCode,
                   xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                   contract_mill_radius: bool = False,
                   expand: float = 0,
                   shift: float = 0):

    if contract_mill_radius:
        expand -= gcode.mill_radius

    gcode.check_z_coordinate_constraints(zb, zt)
    xb, xe, yb, ye = expand_xy_line(xb, xe, yb, ye, expand)
    xb, xe, yb, ye = shift_xy_line(xb, xe, yb, ye, shift)
    xb, xe, yb, ye = gcode.router_state.swap_to_closest_xy(xb, xe, yb, ye)

    x, y, z = xb, yb, zt
    gcode.approach(x, y, z)

    for z in loop_z(zb, zt, gcode.depth_of_cut):
        gcode.plunge(z)
        x = xe if x == xb else xb
        y = ye if y == yb else yb
        gcode.mill_line(x, y)


def mill_tabbed_line_slot(gcode: GCode,
                          xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                          dt: float = 0,
                          contract_mill_radius: bool = False,
                          expand: float = 0,
                          shift: float = 0) \
        -> float:
    """
    Mill a xy slot with tabs.
    :param gcode: gcode-writer object.
    :param xb: Begin x position
    :param xe: End x position
    :param yb: Begin y position
    :param ye: End y position
    :param zb: Bottom line slot height at which the tab bumps to create. Tab tops are milled TAB_HEIGHT above zb.
    :param zt: Top line slot height
    :param dt: Distance to next tab
    :param contract_mill_radius: Contract the line length inward at both ends with the mill radius.
    :param expand: Expand the line length outward at both sides with specified size.
    :param shift: Shift the line orthogonal to the line direction
    :return: Distance to next tab
    """

    if contract_mill_radius:
        expand -= gcode.mill_radius

    gcode.check_z_coordinate_constraints(zb, zt)
    xb, xe, yb, ye = expand_xy_line(xb, xe, yb, ye, expand)
    xb, xe, yb, ye = shift_xy_line(xb, xe, yb, ye, shift)

    if zt > zb + gcode.tab_height:
        mill_line_slot(gcode, xb, xe, yb, ye, zb + gcode.tab_height, zt)
        # Make sure to finish at the begin position, such that tab cut will finish at the end position,
        # in order to hand over the right tab distance to a possibly next concatenated slot.
        gcode.goto_xy(xb, yb)
    zt = zb + gcode.tab_height

    dx = xe - xb
    dy = ye - yb
    d = sqrt(dx ** 2 + dy ** 2)
    dx /= d
    dy /= d

    while d > 0:
        # Mill up to next tab
        if dt >= gcode.tab_width + gcode.mill_diameter:
            # Go to next tab
            dd = min(d, gcode.tab_distance - dt)
            if dd == 0:
                break
            d -= dd
            xe = xb + dd * dx
            ye = yb + dd * dy
            mill_line_slot(gcode, xb, xe, yb, ye, zb, zt)
            xb = xe
            yb = ye
            dt += dd
            if dt >= gcode.tab_distance:
                dt = 0
        if d == 0:
            break
        if d == 0:
            break
        # Finalize or create tab (by moving over)
        dd = min(d, gcode.tab_width + gcode.mill_diameter - dt)
        if dt == 0:
            gcode.retract(zt)
        d -= dd
        xe = xb + dd * dx
        ye = yb + dd * dy
        gcode.goto_xy(xe, ye)
        xb = xe
        yb = ye
        dt += dd

    return dt


def create_line_slot(gcode: GCode,
                     xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                     contract_mill_radius: bool = False,
                     expand: float = 0,
                     shift: float = 0,
                     tabs: bool = False):

    gcode.retract()
    if tabs:
        mill_tabbed_line_slot(gcode, xb, xe, yb, ye, zb, zt, 0, contract_mill_radius, expand, shift)
    else:
        mill_line_slot(gcode, xb, xe, yb, ye, zb, zt, contract_mill_radius, expand, shift)
    gcode.retract()


def create_x_line_slot(gcode: GCode,
                       xl: float, xr: float, y: float, zb: float, zt: float,
                       contract_mill_radius: bool = False,
                       expand: float = 0,
                       shift: float = 0,
                       tabs: bool = False):

    create_line_slot(gcode, xl, xr, y, y, zb, zt, contract_mill_radius, expand, shift, tabs)


def create_y_line_slot(gcode: GCode,
                       x: float, yf: float, yb: float, zb: float, zt: float,
                       contract_mill_radius: bool = False,
                       expand: float = 0,
                       shift: float = 0,
                       tabs: bool = False):

    create_line_slot(gcode, x, x, yf, yb, zb, zt, contract_mill_radius, expand, shift, tabs)
