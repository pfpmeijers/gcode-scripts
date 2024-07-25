from math import dist


def get_normalized_xy_direction(xb: float, xe: float, yb: float, ye: float) -> tuple[float, float]:

    dx = xe - xb
    dy = ye - yb
    d = dist((xb, yb), (xe, ye))
    if d == 0:
        raise ValueError("Cannot normalize line direction if it has no length")
    dx /= d
    dy /= d

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

    if shift != 0:
        dx, dy = get_normalized_xy_direction(xb, xe, yb, ye)
        xb += shift * dy
        xe += shift * dy
        yb -= shift * dx
        ye -= shift * dx

    return xb, xe, yb, ye
