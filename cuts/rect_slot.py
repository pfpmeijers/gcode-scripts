from GCode import GCode
from cuts.line_slot import mill_tabbed_line_slot


def get_sorted_rect_corners(gcode: GCode,
                            xl: float, xr: float, yf: float, yb: float) \
        -> list[tuple[float, float]]:

    if gcode.router_state.x is None or gcode.router_state.y is None:
        raise ValueError('Actual position not known yet. Start with a home_xy() or other explicit xy move.')

    corners = [(xl, yf), (xl, yb), (xr, yb), (xr, yf)]
    i, _ = gcode.router_state.get_closest_xy(corners)
    if i:
        corners = corners[i:] + corners[:i]
    return corners


def get_closest_rect_corner(gcode: GCode,
                            xl: float, xr: float, yf: float, yb: float) \
        -> tuple[float, float]:

    return get_sorted_rect_corners(gcode, xl, xr, yf, yb)[0]


def mill_rect(gcode: GCode, xl: float, xr: float, yf: float, yb: float):

    corners = get_sorted_rect_corners(gcode, xl, xr, yf, yb)
    gcode.mill_line(*corners[0])
    for x, y in corners[1:] + [corners[0]]:
        gcode.mill_line(x, y)


def mill_line_ramp(gcode: GCode,
                   x: float, y: float, z: float, zb: float, d: float, ramp_length: float) \
        -> float:

    z = max(z - gcode.depth_of_cut * d / ramp_length, zb)
    gcode.mill_line(x, y, z, gcode.get_ramp_rate(ramp_length))
    return z


def mill_rect_ramp(gcode: GCode,
                   xl: float, xr: float, yf: float, yb: float, z: float, zb: float) -> float:

    dx = xr - xl
    dy = yb - yf
    ramp_length = 2 * dx + 2 * dy

    corners = get_sorted_rect_corners(gcode, xl, xr, yf, yb)
    px = corners[3][0]
    for x, y in corners[1:] + [corners[0]]:
        d = dx if x != px else dy
        z = mill_line_ramp(gcode, x, y, z, zb, d, ramp_length)
        px = x
    return z


def mill_rect_slot(gcode: GCode, xl: float, xr: float, yf: float, yb: float, zb: float, zt: float):

    gcode.check_coordinate_constraints(xl, xr, yf, yb, zb, zt)
    x0, y0 = get_closest_rect_corner(gcode, xl, xr, yf, yb)
    x, y, z = x0, y0, zt

    if zt - zb > gcode.depth_of_cut:
        gcode.approach(x, y, z)
        while z > zb:
            z = mill_rect_ramp(gcode, xl, xr, yf, yb, z, zb)
    else:
        gcode.plunge(zb)
    mill_rect(gcode, xl, xr, yf, yb)


def mill_tabbed_rect_slot(gcode: GCode,
                          xl: float, xr: float, yf: float, yb: float, zb: float, zt: float):

    gcode.check_coordinate_constraints(xl, xr, yf, yb, zb, zt)

    corners = get_sorted_rect_corners(gcode, xl, xr, yf, yb)
    dt = 0
    for ib in range(4):
        ie = (ib + 1) % 4
        dt = mill_tabbed_line_slot(gcode, corners[ib][0], corners[ie][0], corners[ib][1], corners[ie][1], zb, zt, dt)


def create_rect_slot(gcode: GCode,
                     xl: float, xr: float, yf: float, yb: float, zb: float, zt: float,
                     tabs: bool = False):

    gcode.retract()
    if tabs:
        mill_tabbed_rect_slot(gcode, xl, xr, yf, yb, zb, zt)
    else:
        mill_rect_slot(gcode, xl, xr, yf, yb, zb, zt)
    gcode.retract()
