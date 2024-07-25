def expand_xy_rect(xl: float, xr: float, yf: float, yb: float,
                   expand: float = 0) \
        -> tuple[float, float, float, float]:
    """
    Adjusts a set of xy-plane rectangle coordinates by means of contracting or expanding all sides.

    :param xl: Left side coordinate of the rectangle.
    :param xr: Right side coordinate of the rectangle.
    :param yf: Front side coordinate of the rectangle.
    :param yb: Back side coordinate of the rectangle.
    :param expand: The amount to expand the rectangle on all sides outward.
    :return: Adjusted rectangle coordinates.
    """

    xl -= expand
    xr += expand
    yf -= expand
    yb += expand

    return xl, xr, yf, yb


