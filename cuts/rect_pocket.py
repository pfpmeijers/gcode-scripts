from GCode import GCode
from cuts.rect_slot import mill_rect, get_closest_rect_corner
from utils.loop import loop_z
from utils.rect import expand_xy_rect


def mill_rect_pocket(gcode: GCode,
                     xl: float, xr: float, yf: float, yb: float, zb: float, zt: float,
                     contract_mill_radius: bool = False,
                     expand: float = 0,
                     meander: bool = True):

    """ Inline version (i.e. without retraction) of create_rect_pocket(). """

    gcode.check_coordinate_constraints(xl, xr, yf, yb, zb, zt, mill_fit=True)

    multi_layer = zt - zb > gcode.depth_of_cut
    multi_lane = yb - yf > gcode.mill_diameter
    if multi_layer or multi_lane:
        # Contract little bit, such that a full height contour path at the end can create a clean cut.
        expand -= gcode.milling_margin_xy

    if contract_mill_radius:
        expand -= gcode.mill_radius
    xl, xr, yf, yb = expand_xy_rect(xl, xr, yf, yb, expand)

    x0, y0 = get_closest_rect_corner(gcode, xl, xr, yf, yb)
    x, y, z = x0, y0, zt
    gcode.approach(x, y, z)

    if multi_lane:
        if meander:
            dy = gcode.width_of_cut
            if y0 == yb:
                dy = -dy

            while z > zb:
                x, y = x0, y0
                gcode.goto_xy(x, y)

                z = max(z - gcode.depth_of_cut, zb)
                gcode.plunge(z)

                while True:
                    x = xr if x == xl else xl
                    gcode.mill_line(x, y)
                    if dy > 0:
                        if y < yb:
                            y = min(y + dy, yb)
                            gcode.mill_line(x, y)
                        else:
                            break
                    else:
                        if y > yf:
                            y = max(y + dy, yf)
                            gcode.mill_line(x, y)
                        else:
                            break
        else:
            for z in loop_z(zb, zt, gcode.depth_of_cut):
                gcode.plunge(z)

                xl_, xr_, yf_, yb_ = xl, xr, yf, yb
                while xl_ < xr_ or yf_ < yb_:
                    mill_rect(gcode, xl_, xr_, yf_, yb_)

                    xl_ += gcode.width_of_cut
                    xr_ -= gcode.width_of_cut
                    if xl_ > xr_:
                        xl_ = xr_ = (xl_ + xr_) / 2

                    yf_ += gcode.width_of_cut
                    yb_ -= gcode.width_of_cut
                    if yf_ > yb_:
                        yf_ = yb_ = (yf_ + yb_) / 2

    if multi_layer or multi_lane:
        xl, xr, yf, yb = expand_xy_rect(xl, xr, yf, yb, expand=gcode.milling_margin_xy)

        x0, y0 = get_closest_rect_corner(gcode, xl, xr, yf, yb)
        x, y, z = x0, y0, zb
        gcode.approach(x0, y0, z)

    mill_rect(gcode, xl, xr, yf, yb)


def create_rect_pocket(gcode: GCode,
                       xl: float, xr: float, yf: float, yb: float, zb: float, zt: float,
                       contract_mill_radius: bool = False,
                       expand: float = 0,
                       meander: bool = True):
    """
    Mill a xy-plane rectangular pocket.

    :param gcode: gcode-writer object.
    :param xl: Left side coordinate of the pocket.
    :param xr: Right side coordinate of the pocket.
    :param yf: Front side coordinate of the pocket.
    :param yb: Back side coordinate of the pocket.
    :param zb: Bottom side coordinate of the pocket.
    :param zt: Top side coordinate of the pocket.
    :param contract_mill_radius: Contract the rectangle coordinates with the mill radius.
    :param expand: Expand the rectangle coordinates outward with specified size.
    :param meander: Create a meandering route. Alternatively a route with contracting rectangles is created.
    """
    gcode.retract()
    mill_rect_pocket(gcode, xl, xr, yf, yb, zb, zt, contract_mill_radius, expand, meander)
    gcode.retract()
