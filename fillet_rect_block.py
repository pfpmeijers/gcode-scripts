from utils.polar import sin, cos, pi
import config
from gcode import mill_arc
from basics import retract, approach, plunge
from utils.main import main_call
from fillet import create_fillet
from rect_pocket import create_rect_pocket
from rounded_rect_slot import create_rounded_rect_slot


def mill_rect_fillet_corner(x: float, y: float, sx: int, sy: float, z: float, r: float):

    # Rounded corner begin and end points
    xb = x + sx * r
    xe = x
    yf = y
    ye = y + sy * r

    # Rounding angle
    a = 90

    def ar():
        return a * pi / 180

    def dp():
        return (r + config.MILL_CORNER_DIAMETER) * (cos(ar()) - 1) + config.MILL_DIAMETER / 2

    def dz():
        return (r + config.MILL_CORNER_DIAMETER) * (sin(ar()) - 1)

    def xp():
        return x if x == xb else x - sx * dp()

    def yp():
        return y if y == ye else y - sy * dp()

    def zp():
        return z + dz()

    x = xb
    y = yf
    approach(xp(), yp(), z)

    while a > 0:
        a -= config.ANGLE_OF_CUT
        plunge(zp())
        if x == xe:
            x = xb
            y = yf
        else:
            x = xe
            y = ye
        mill_arc(xp(), yp(), zp(), r + dp(), clockwise=(sx == sy) == (x == xe))


def create_rect_fillet_corner(x: float, y: float, sx: int, sy: float, z: float, r: float):

    retract()
    mill_rect_fillet_corner(x, y, sx, sy, z, r)
    retract()


def create_fillet_rect_block(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float, zs: float, r: float, zr: float = None, tabs: bool = False):
    """

    :param xl: Left x coordinate of the block
    :param xr: Right x coordinate of the block
    :param yf: Front y coordinate of the block
    :param yb: Back y coordinate of the block
    :param zb: Bottom z coordinate of the block
    :param zt: Top z coordinate of the block
    :param zs: Top z coordinate of the stock
    :param r: Fillet radius
    :param zr: Retract z coordinate
    :param tabs: Use tabs on block outside
    :return:
    """
    create_rect_pocket(xl, xr, yf, yb, zt, zs)
    create_rounded_rect_slot(xl, xr, yf, yb, zb, zt, r, tabs)

    create_fillet(xl, xl, yf, yb, zt, r)
    create_fillet(xl, xr, yb, yb, zt, r)
    create_fillet(xr, xr, yb, yf, zt, r)
    create_fillet(xr, xl, yf, yf, zt, r)

    create_rect_fillet_corner(xl, yf, 1, 1, zt, r)
    create_rect_fillet_corner(xr, yf, -1, 1, zt, r)
    create_rect_fillet_corner(xr, yb, -1, -1, zt, r)
    create_rect_fillet_corner(xl, yb, 1, -1, zt, r)


if __name__ == "__main__":

    INFO = "Create fillets (rounded corner) along the edges of a horizontal rectangle."
    ARGS_INFO = (
        ("rectangle (xl,yf,zb) to (xr,yb,zt)", "rectangle to be slotted and rounded inward (xl < xr, yf < yb, zb < zt)"),
        "stock height",
        "rounding radius",
        "retract height",
    )

    main_call(create_fillet_rect_block, INFO, ARGS_INFO)
