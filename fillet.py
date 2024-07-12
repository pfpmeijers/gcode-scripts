from utils.polar import sqrt, sin, cos, pi
import config
from gcode import mill_line
from basics import retract, approach
from utils.main import main_call


def mill_fillet(xb: float, xe: float, yf: float, ye: float, z: float, r: float):

    # Edge
    dx = xe - xb
    dy = ye - yf
    length = sqrt(dx ** 2 + dy ** 2)

    # Normalize
    if length > 0:
        dx /= length
        dy /= length

    # Extend edge tangentially to incorporate mill radius
    xb -= dx * config.MILL_DIAMETER / 2
    xe += dx * config.MILL_DIAMETER / 2
    yf -= dy * config.MILL_DIAMETER / 2
    ye += dy * config.MILL_DIAMETER / 2

    # Normal outward
    dxn = -dy
    dyn = dx

    # Rounding angle
    a = 90

    def ar():
        return a * pi / 180

    def dp():
        return (r + config.MILL_CORNER_DIAMETER) * (cos(ar()) - 1) + config.MILL_DIAMETER / 2

    def dz():
        return (r + config.MILL_CORNER_DIAMETER) * (sin(ar()) - 1)

    def xp():
        return x + dxn * dp()

    def yp():
        return y + dyn * dp()

    def zp():
        return z + dz()

    x = xb
    y = yf
    approach(xp(), yp(), z)

    while a > 0:
        a -= config.ANGLE_OF_CUT
        mill_line(xp(), yp(), zp(), config.PLUNGE_RATE)
        x = xe if x == xb else xb
        y = ye if y == yf else yf
        mill_line(xp(), yp(), zp(), config.FEED_RATE)


def create_fillet(xb: float, xe: float, yf: float, ye: float, z: float, r: float):

    retract()
    mill_fillet(xb, xe, yf, ye, z, r)
    retract()


if __name__ == "__main__":

    INFO = "Create a fillet (rounded corner) along a horizontal edge."
    ARGS_INFO = (
        ("line (xb,yf,z) to (xe,ye,z)", "edge to be rounded inward "
                                        "(counter clockwise with respect to the edge vector direction)"),
        "rounding radius",
        "retract height",
    )

    main_call(create_fillet, INFO, ARGS_INFO)
