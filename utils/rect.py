from typing import Tuple

from gcode import mill_line
from state import state


def get_sorted_rect_corners(xl: float, xr: float, yf: float, yb: float) -> Tuple[Tuple[float, float], ...]:

    distances = []
    corners = (xl, yf), (xl, yb), (xr, yb), (xr, yf)
    for i, corner in enumerate(corners):
        distances.append((state.get_xy_distance(*corner), i))
    i = sorted(distances, key=lambda distance: distance[0])[0][1]  # Index of closest corner.
    if i:
        corners = corners[i:] + corners[:i]
    return corners


def get_closest_rect_corner(xl: float, xr: float, yf: float, yb: float) -> Tuple[float, float]:

    return get_sorted_rect_corners(xl, xr, yf, yb)[0]


def mill_rect(xl: float, xr: float, yf: float, yb: float, z: float):

    corners = get_sorted_rect_corners(xl, xr, yf, yb)
    for x, y in corners:
        z = mill_line(x, y, z)
