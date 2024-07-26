from GCode import GCode
from utils.line import expand_xy_line, shift_xy_line, get_normalized_xy_direction, get_xy_line_length
from utils.loop import loop_z


def mill_line_ramp(gcode: GCode,
                   x: float, y: float, z: float, zb: float,
                   ramp_ratio: float, ramp_length: float) \
        -> float:

    z = max(z - gcode.depth_of_cut * ramp_ratio, zb)
    gcode.mill_line(x, y, z, gcode.get_ramp_rate(ramp_length))
    return z


def mill_line_slot(gcode: GCode,
                   xb: float, xe: float, yb: float, ye: float, zb: float, zt: float = 0,
                   contract_mill_radius: bool = False,
                   expand: float = 0,
                   shift: float = 0,
                   start_closest: bool = True,
                   tabs: bool = False,
                   dt: float = 0) \
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
    :param contract_mill_radius: Contract the line length inward at both ends with the mill radius.
    :param expand: Expand the line length outward at both sides with specified size.
    :param shift: Shift the line orthogonal to the line direction. See shift_xy_line for details.
    :param start_closest:
    :param tabs:
    :param dt: Distance passed since last tab start of a preceding slot. If 0 then the slot starts with a new tab.
    :return: Distance passed since last tab start
    """

    if contract_mill_radius:
        expand -= gcode.mill_radius

    gcode.check_z_coordinate_constraints(zb, zt)
    xb, xe, yb, ye = expand_xy_line(xb, xe, yb, ye, expand)
    xb, xe, yb, ye = shift_xy_line(xb, xe, yb, ye, shift)
    if start_closest:
        xb, xe, yb, ye = gcode.router_state.swap_to_closest_xy(xb, xe, yb, ye)

    if tabs:
        zbt = zb + gcode.tab_height
        if zt > zbt:
            mill_line_slot(gcode, xb, xe, yb, ye, zbt, zt, start_closest=False)
            zt = zbt

        # Make sure to get at the begin position, such that next tab cuts will finish at the end position,
        # in order to hand over the right tab distance to a possibly next concatenated slot.
        gcode.approach(xb, yb, zt)

        d = get_xy_line_length(xb, xe, yb, ye)
        dx, dy = get_normalized_xy_direction(xb, xe, yb, ye, d)

        while d > 0:  # Remaining length
            if dt >= gcode.tab_width + gcode.mill_diameter:
                # Slot towards next tab
                dd = min(d, gcode.tab_distance - dt)
                if dd > 0:
                    d -= dd
                    xe = xb + dd * dx
                    ye = yb + dd * dy
                    mill_line_slot(gcode, xb, xe, yb, ye, zb, zt)
                    xb, yb = xe, ye
                    dt += dd
                    if dt == gcode.tab_distance:
                        dt = 0
            if d == 0:
                break
            # Finalize or create tab (by moving over)
            dd = min(d, gcode.tab_width + gcode.mill_diameter - dt)
            if dt == 0:
                gcode.goto_z(zb + gcode.tab_height)
            d -= dd
            xe, ye = xb + dd * dx, yb + dd * dy
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
            gcode.mill_line(x, y)

    return dt
