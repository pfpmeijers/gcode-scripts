from typing import Tuple

import config
from gcode import goto_xy, mill_xy
from state import state
from basics import retract, approach, plunge
from utils.constraints import check_coordinate_constraints
from utils.line import expand_rect
from utils.main import main_call
from rect_slot import mill_rect_slot
from utils.rect import get_sorted_rect_corners, get_closest_rect_corner


def mill_rect_pocket(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float,
                     contract_mill_radius: bool = False,
                     expand: float = 0,
                     meander: bool = True):

    """ Inline version (i.e. without retraction) of create_rect_pocket(). """

    check_coordinate_constraints(xl, xr, yf, yb, zb, zt, mill_fit=True)

    multi_layer = zt - zb > config.DEPTH_OF_CUT
    multi_line = yb - yf > config.MILL_DIAMETER
    if multi_layer or multi_line:
        # Contract little bit, such that a full height contour can create a clean cut.
        expand -= config.MARGIN

    xl, xr, yf, yb = expand_rect(xl, xr, yf, yb, contract_mill_radius, expand)

    x0, y0 = get_closest_rect_corner(xl, xr, yf, yb)
    x, y, z = x0, y0, zt
    approach(x, y, z)

    if multi_line:
        if meander:
            dy = config.WIDTH_OF_CUT
            if y0 == yb:
                dy = -dy

            while z > zb:
                x, y = x0, y0
                goto_xy(x, y)

                z = max(z - config.DEPTH_OF_CUT, zb)
                plunge(z)

                while True:
                    x = xr if x == xl else xl
                    mill_xy(x, y)
                    if dy > 0:
                        if y < yb:
                            y = min(y + dy, yb)
                            mill_xy(x, y)
                        else:
                            break
                    else:
                        if y > yf:
                            y = max(y + dy, yf)
                            mill_xy(x, y)
                        else:
                            break

        else:
            # TODO: Optimize (but note this variant is not that often used ...)
            pass
            # xl_, xr_, yf_, yb_ = xl, xr, yf, yb
            # while xl_ < xr_ or yf_ < yb_:
            #     mill_rect_slot(xl_, xr_, yf_, yb_, zb, zt)
            #
            #     xl_ += config.WIDTH_OF_CUT
            #     xr_ -= config.WIDTH_OF_CUT
            #     if xl_ > xr_:
            #         xl_ = xr_ = (xl_ + xr_) / 2
            #
            #     yf_ += config.WIDTH_OF_CUT
            #     yb_ -= config.WIDTH_OF_CUT
            #     if yf_ > yb_:
            #         yf_ = yb_ = (yf_ + yb_) / 2

    if multi_layer or multi_line:
        # Mill the contour at full height to have a clean cut.

        xl, xr, yf, yb = expand_rect(xl, xr, yf, yb, expand=config.MARGIN)
        x0, y0 = get_closest_rect_corner(xl, xr, yf, yb)
        x, y, z = x0, y0, zt
        approach(x0, y0, z)

        mill_rect_slot(xl, xr, yf, yb, zb, zt)


def create_rect_pocket(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float,
                       contract_mill_radius: bool = False,
                       expand: float = 0,
                       meander: bool = True):
    """
    Mill a xy-plane rectangular pocket.

    :param xl: Left side coordinate of the pocket.
    :param xr: Right side coordinate of the pocket.
    :param yf: Front side coordinate of the pocket.
    :param yb: Back side coordinate of the pocket.
    :param zb: Bottom side coordinate of the pocket.
    :param zt: Top side coordinate of the pocket.
    :param contract_mill_radius: Contract the rectangle coordinates with the mill radius.
    :param expand: Expand the rectangle coordinates outward with specified size.
    :param meander: Use meandering route.
    """
    retract()
    mill_rect_pocket(xl, xr, yf, yb, zb, zt, contract_mill_radius, expand, meander)
    retract()


if __name__ == "__main__":

    main_call(create_rect_pocket)
