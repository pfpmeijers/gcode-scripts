from GCode import GCode
from utils.arc import get_arc_center, shift_arc, expand_arc
from utils.loop import loop_z
from utils.polar import to_polar, from_polar, get_angle_delta


def mill_arc_ramp(gcode: GCode,
                  x: float, y: float, zb: float, z: float,
                  r: float, clockwise: bool = True,
                  ramp_fraction: float = 1,
                  feed_rate: int = None) \
        -> float:

    z = max(z - gcode.depth_of_cut * ramp_fraction, zb)
    gcode.mill_arc(x, y, z, r, clockwise, feed_rate)

    return z


def mill_arc_slot(gcode: GCode,
                  xb: float, xe: float, yb: float, ye: float, zb: float, zt: float,
                  r: float,
                  clockwise: bool = True,
                  contract_mill_radius: bool = False,
                  expand: float = 0,
                  shift: float = 0,
                  start_closest: bool = True,
                  tabs: bool = False,
                  dt: float = 0) \
        -> float:

    """
    TODO: Sync description with tabbed line slot.
    Mill a xy arc at height z with tabs (vertical bumps upward).
    :param gcode: gcode-writer object
    :param xb: Begin x position
    :param xe: End x position
    :param yb: Begin y position
    :param ye: End y position
    :param zb: Bottom arc slot height at which the tab bumps to create. Tab tops are milled TAB_HEIGHT above zb.
    :param zt: Top arc slot height
    :param r: Radius
    :param clockwise: Mill the arc clockwise from begin to end or counter-clockwise
    :param contract_mill_radius: Contract the line length inward at both ends with the mill radius.
    :param expand: Expand the line length outward at both sides with specified size.
    :param shift: Shift the arc position by adjusting the radius, though keeping its original center
    :param start_closest:
    :param dt:
    :return:
    """

    if contract_mill_radius:
        expand -= gcode.mill_radius

    gcode.check_z_coordinate_constraints(zb, zt)
    xc, yc = get_arc_center(xb, xe, yb, ye, r, clockwise)
    xb, xe, yb, ye = expand_arc(xc, xb, xe, yc, yb, ye, r, clockwise, expand)
    xb, xe, yb, ye, r = shift_arc(xc, xb, xe, yc, yb, ye, r, shift)
    if start_closest:
        xb, xe, yb, ye, clockwise = gcode.router_state.swap_to_closest_xy(xb, xe, yb, ye, clockwise)

    if tabs:
        zbt = zb + gcode.tab_height
        if zt > zbt:
            mill_arc_slot(gcode, xb, xe, yb, ye, zbt, zt, r, clockwise, start_closest=False)
            zt = zbt

        # Make sure to get at the begin position, such that next tab cuts will finish at the end position,
        # in order to hand over the right tab distance to a possibly next concatenated slot.
        gcode.approach(xb, yb, zt)

        # Angle difference and distance along the arc
        rb, ab = to_polar(xb - xc, yb - yc)
        re, ae = to_polar(xe - xc, ye - yc)
        da = get_angle_delta(ab, ae)
        d = da * r  # Remaining length

        a = ab
        da = -1 if clockwise else 1
        while d > 0:
            # Mill up to next tab
            if dt >= gcode.tab_width + gcode.mill_diameter:
                # Go to next tab
                dd = min(d, gcode.tab_distance - dt)
                if dd > 0:
                    d -= dd
                    a += dd / r * da
                    xe, ye = from_polar(r, a, xc, yc)
                    mill_arc_slot(gcode, xb, xe, yb, ye, zb, zt, r, clockwise)
                    dt += dd
                    if dt >= gcode.tab_distance:
                        dt = 0
            if d == 0:
                break
            # Finalize or create tab (by moving over)
            dd = min(d, gcode.tab_width + gcode.mill_diameter - dt)
            if dt == 0:
                gcode.goto_z(zb + gcode.tab_height)
            d -= dd
            a += dd / r * da
            xe, ye = from_polar(r, a, xc, yc)
            gcode.goto_xy(xe, ye)
            xb, yb = xe, ye
            dt += dd

    else:
        # No tabs

        x, y, z = xb, yb, zt
        gcode.approach(x, y, z)

        for z in loop_z(zb, zt, gcode.depth_of_cut):
            gcode.plunge(z)
            x = xe if x == xb else xb
            y = ye if y == yb else yb
            gcode.mill_arc(x, y, z, r, clockwise == (x == xe))

    return dt
