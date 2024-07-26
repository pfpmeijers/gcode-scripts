from math import dist


def get_xy_line_length(xb: float, xe: float, yb: float, ye: float) -> float:
    d = dist((xb, yb), (xe, ye))
    return d


def get_normalized_xy_direction(xb: float, xe: float, yb: float, ye: float, d: float = None) -> tuple[float, float]:
    if d is None:
        d = get_xy_line_length(xb, xe, yb, ye)
    if d == 0:
        raise ValueError("Cannot normalize line direction if it has no length")
    dx, dy = (xe - xb) / d, (ye - yb) / d
    return dx, dy


def expand_xy_line(xb: float, xe: float, yb: float, ye: float,
                   expand: float = 0) \
        -> tuple[float, float, float, float]:

    if expand != 0:
        dx, dy = get_normalized_xy_direction(xb, xe, yb, ye)
        xb -= expand * dx
        xe += expand * dx
        yb -= expand * dy
        ye += expand * dy

    return xb, xe, yb, ye


def shift_xy_line(xb: float, xe: float, yb: float, ye: float,
                  shift: float = 0) \
        -> tuple[float, float, float, float]:

    # A positive shift is 'outward', i.e. away from the center of a clockwise circular approximation of the line.
    # E.g. a vertical line with yb < ye will shift to the left.

    if shift != 0:
        dx, dy = get_normalized_xy_direction(xb, xe, yb, ye)
        xb -= shift * dy
        xe -= shift * dy
        yb += shift * dx
        ye += shift * dx

    return xb, xe, yb, ye
