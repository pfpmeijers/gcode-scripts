import config
from GCode import mill_line, mill_arc
from basics import retract, approach
from utils.polar import pi
from utils.main import main_call
from line_slot import mill_tabbed_line_slot
from cuts.arc_slot import mill_tabbed_arc_slot


def create_rounded_rect_slot(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float, r: float, tabs: bool = False):

    if xl >= xr or yf >= yb or zb >= zt:
        print("ERROR: Constraints xl < xr, yf < yb, zb < zt not fulfilled.")
        exit()

    if tabs:
        zb += config.TAB_HEIGHT

    # Segment sizes
    dx = xr - xl - 2 * r
    dy = yb - yf - 2 * r
    dr = 2 * pi * r / 4
    if dx < 0 or dy < 0:
        print("ERROR: Rounding radius too big.")
        exit()

    xl -= config.MILL_DIAMETER / 2
    xr += config.MILL_DIAMETER / 2
    yf -= config.MILL_DIAMETER / 2
    yb += config.MILL_DIAMETER / 2
    r += config.MILL_DIAMETER / 2

    retract()

    x = xl + r
    y = yf
    z = zt
    approach(x, y, z)

    ramp_length = 2 * dx + 2 * dy + 4 * dr
    ramp_rate = int(min(config.FEED_RATE, ramp_length / gcode.MILL.DEPTH_OF_CUT * config.PLUNGE_RATE))

    def dz(d):
        return max(z - gcode.MILL.DEPTH_OF_CUT * d / ramp_length, zb)

    done = False
    while not done:
        if z == zb:
            done = True
        z = dz(dx)
        mill_line(xr - r, yf, z, feed_rate=ramp_rate)
        z = dz(dr)
        mill_arc(xr, yf + r, z, r, clockwise=False, feed_rate=ramp_rate)
        z = dz(dy)
        mill_line(xr, yb - r, z, feed_rate=ramp_rate)
        z = dz(dr)
        mill_arc(xr - r, yb, z, r, clockwise=False, feed_rate=ramp_rate)
        z = dz(dx)
        mill_line(xl + r, yb, z, feed_rate=ramp_rate)
        z = dz(dr)
        mill_arc(xl, yb - r, z, r, clockwise=False, feed_rate=ramp_rate)
        z = dz(dy)
        mill_line(xl, yf + r, z, feed_rate=ramp_rate)
        z = dz(dr)
        mill_arc(xl + r, yf, z, r, clockwise=False, feed_rate=ramp_rate)

    retract()

    if tabs:
        zt = zb
        zb -= config.TAB_HEIGHT
        approach(xl, yf, zt)
        dt = mill_tabbed_line_slot(xl + r, xr - r, yf, yf, zb, zt)
        dt = mill_tabbed_arc_slot(xr - r, xr, yf, yf + r, zb, zt, r, dt)
        dt = mill_tabbed_line_slot(xr, xr, yf + r, yb - r, zb, zt, dt)
        dt = mill_tabbed_arc_slot(xr, xr - r, yb - r, yb, zb, zt, r, dt)
        dt = mill_tabbed_line_slot(xr - r, xl + r, yb, yb, zb, zt, dt)
        dt = mill_tabbed_arc_slot(xl + r, xl, yb, yb - r, zb, zt, r, dt)
        dt = mill_tabbed_line_slot(xl, xl, yb - r, yf + r, zb, zt, dt)
        mill_tabbed_arc_slot(xl, xl + r, yf + r, yf, zb, zt, r, dt)

        retract()


if __name__ == "__main__":

    INFO = "Create rectangular slot with rounded corners along vertical edges.\n" \
           "Assumed to be done with flat end mill."
    ARGS_INFO = (
        ("rectangle (xl,yf,zb) to (xr,yb,zt)", "Rectangle to be slotted. Constraints: xl < xr, yf < yb, zb < zt"),
        "Rounding radius",
        "Retract height",
        "Create tabs"
    )

    main_call(create_rounded_rect_slot, INFO, ARGS_INFO)
