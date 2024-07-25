import config

from GCode import GCode
from utils.arc import preprocess_arc, get_arc_center, shift_arc
from utils.loop import loop_z
from utils.polar import to_polar, from_polar, get_angle_delta


def mill_arc_slot(gcode: GCode,
                  xb: float, xe: float, yb: float, ye: float, zb: float, zt: float, r: float, clockwise: bool,
                  shift: float = 0.0):

    gcode.check_z_coordinate_constraints(zb, zt)
    xc, yc = get_arc_center(xb, xe, yb, ye, r, clockwise)
    xb, xe, yb, ye, r = shift_arc(xc, xb, xe, yc, yb, ye, r, shift)
    xb, xe, yb, ye, clockwise = gcode.router_state.swap_to_closest_xy(xb, xe, yb, ye, clockwise)

    x = xb
    y = yb
    z = zt
    approach(x, y, z)
    for z in loop_z(zb, zt):
        plunge(z)
        x = xe if x == xb else xb
        y = ye if y == yb else yb
        mill_arc(x, y, z, r, clockwise == (x == xe))


def mill_tabbed_arc_slot(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float, r: float,
                         clockwise: bool = True, shift: float = 0, dt: float = 0) -> float:
    """
    Mill an xy arc at height z with tabs (vertical bumps upward) according to TAB_xxx settings.
    :param xb: Begin x position
    :param xe: End x position
    :param yb: Begin y position
    :param ye: End y position
    :param zb: Bottom arc slot height at which the tab bumps to create. Tab tops are milled TAB_HEIGHT above zb.
    :param zt: Top arc slot height
    :param r: Radius
    :param clockwise: Mill the arc clockwise from begin to end or counter-clockwise
    :param shift: Shift the arc position by adjusting the radius, though keeping its original center
    :param dt: Distance to next tab
    :return: None
    """

    gcode.check_z_coordinate_constraints(zb, zt)
    xc, yc = get_arc_center(xb, xe, yb, ye, r, clockwise)
    xb, xe, yb, ye, r = shift_arc(xc, xb, xe, yc, yb, ye, r, shift)
    xb, xe, yb, ye, clockwise = gcode.router_state.swap_to_closest_xy(xb, xe, yb, ye, clockwise)

    goto_xy(xb, yb)

    # Angle difference and distance along the arc
    rb, ab = to_polar(xb - xc, yb - yc)
    re, ae = to_polar(xe - xc, ye - yc)
    da = get_angle_delta(ab, ae)
    d = da * r

    a = ab
    da = -1 if clockwise else 1
    while d > 0:
        if dt >= config.TAB_WIDTH + config.MILL_DIAMETER:
            # Go to next tab
            dd = min(d, config.TAB_DISTANCE - dt)
            if dd == 0:
                break
            d -= dd
            a += dd / r * da
            xe, ye = from_polar(r, a, xc, yc)
            mill_arc_slot(xb, xe, yb, ye, zb, zt, r, clockwise)
            dt += dd
            if dt >= config.TAB_DISTANCE:
                dt = 0
        if d == 0:
            break
        # Finalize or create tab (by moving over)
        dd = min(d, config.TAB_WIDTH + config.MILL_DIAMETER - dt)
        if dt == 0:
            retract(zb + config.TAB_HEIGHT)
        d -= dd
        a += dd / r * da
        xe, ye = from_polar(r, a, xc, yc)
        goto_xy(xe, ye)
        xb = xe
        yb = ye
        dt += dd
        if dt >= config.TAB_WIDTH + config.MILL_DIAMETER:
            plunge(zb)

    return dt


# TODO: Add expand option, similar to line_slot
def create_arc_slot(xb: float, xe: float, yb: float, ye: float, zb: float, zt: float, r: float, clockwise: bool = True,
                    shift: float = 0.0, tabs: bool = False):

    retract()
    if tabs:
        if zt > zb + config.TAB_HEIGHT:
            mill_arc_slot(xb, xe, yb, ye, zb + config.TAB_HEIGHT, zt, r, clockwise, shift)
        zt = zb + config.TAB_HEIGHT
        retract()
        mill_tabbed_arc_slot(xb, xe, yb, ye, zb, zt, r, clockwise, shift)
    else:
        mill_arc_slot(xb, xe, yb, ye, zb, zt, r, clockwise, shift)
    retract()
    
    
if __name__ == "__main__":

    main_call(create_arc_slot)
