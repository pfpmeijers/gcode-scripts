import config


def check_x_coordinate_constraints(xl: float, xr: float, mill_fit: bool = False):

    if xl >= xr:
        raise ValueError("Left x coordinate must be smaller than right x coordinate")
    if mill_fit and xl >= xr - config.MILL_DIAMETER:
        raise ValueError("Left x coordinate must be smaller than right x coordinate minus mill diameter")


def check_y_coordinate_constraints(yf: float, yb: float, mill_fit:bool = False):

    if yf >= yb:
        raise ValueError("Front y coordinate must be smaller than back y coordinate")
    if mill_fit and yf >= yb - config.MILL_DIAMETER:
        raise ValueError("Front y coordinate must be smaller than back y coordinate minus mill diameter")


def check_z_coordinate_constraints(zb: float, zt: float, zr: float = None):

    if zb > zt:
        raise ValueError("Bottom z coordinate must not be larger than top z coordinate")
    if zr is not None and zr <= zt:
        raise ValueError("Retract z coordinate must be above top z coordinate")


def check_coordinate_constraints(xl: float, xr: float, yf: float, yb: float, zb: float, zt: float, zr: float = None,
                                 mill_fit: bool = False):
    
    check_x_coordinate_constraints(xl, xr, mill_fit)
    check_y_coordinate_constraints(yf, yb, mill_fit)
    check_z_coordinate_constraints(zb, zt, zr)


