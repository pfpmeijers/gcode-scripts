from math import dist, ceil

import config
from RouterState import state
from arc_slot import create_arc_slot
from line_slot import create_line_slot
from utils.arc import get_arc_center, shift_arc
from utils.loop import loop_z
from utils.misc import swap

def create_arc_pocket(gcode: GCode,
                      xb1: float, xe1: float, yb1: float, ye1: float, r1: float, clockwise1: bool,
                      xb2: float, xe2: float, yb2: float, ye2: float, r2: float, clockwise2: bool,
                      zb: float, zt: float,
                      shift: float = 0.0):

    """
    Create a pocket in between two arcs.
    The sides of the arc pocket are formed by straight lines between the arc's begin points and end points.
    """
    gcode.check_z_coordinate_constraints(zb, zt)

    xc1, yc1 = get_arc_center(xb1, xe1, yb1, ye1, r1, clockwise1)
    xb1, xe1, yb1, ye1, r1 = shift_arc(xc1, xb1, xe1, yc1, yb1, ye1, r1, shift)

    xc2, yc2 = get_arc_center(xb2, xe2, yb2, ye2, r2, clockwise2)
    xb2, xe2, yb2, ye2, r2 = shift_arc(xc2, xb2, xe2, yc2, yb2, ye2, r2, shift)

    # Let the first arc be the one closest to current position, to avoid an unnecessary far move.
    # Note that selecting the starting point within a single arc is handled by the create_arc_slot itself.
    corners = [(xb1, yb1), (xe1, ye1), (xb2, yb2), (xe2, ye2)]
    i, _ = state.get_closest(corners)
    if i >= 2:
        xb1, xb2 = swap(xb1, xb2)
        xe1, xe2 = swap(xe1, xe2)
        yb1, yb2 = swap(yb1, yb2)
        ye1, ye2 = swap(ye1, ye2)
        r1, r2 = swap(r1, r2)

    db = dist((xb1, yb1), (xb2, yb2))
    de = dist((xe1, ye1), (xe2, ye2))
    dm = max(db, de)
    km = dm / config.WIDTH_OF_CUT
    n = ceil(km + 1)  # Number of strokes per z level.

    dxb = xb2 - xb1
    dxe = xe2 - xe1
    dyb = yb2 - yb1
    dye = ye2 - ye1
    dr = r2 - r1

    for z in loop_z(zb, zt):
        xb = xb1
        xe = xe1
        yb = yb1
        ye = ye1
        r = r1
        k = 0
        j2 = n - 1
        for j in range(n):
            if j > 0:
                # Mill towards the beginning of the next stroke in order to avoid a retract.
                xbp = xb
                xep = xe
                ybp = yb
                yep = ye
                if k <= km:  # Next stroke is not beyond 2nd arc.
                    f = j / j2
                    xb = xb1 + f * dxb
                    xe = xe1 + f * dxe
                    yb = yb1 + f * dyb
                    ye = ye1 + f * dye
                    r = r1 + f * dr
                else:
                    # Clip to 2nd arc.
                    xb = xb2
                    xe = xe2
                    yb = yb2
                    ye = ye2
                    r = r2
                # Choose the pocket side where ended.
                if state.get_xy_distance(xb, yb) < state.get_xy_distance(xe, ye):
                    create_line_slot(xbp, xb, ybp, yb, z, z)
                else:
                    create_line_slot(xep, xe, yep, ye, z, z)
            create_arc_slot(xb, xe, yb, ye, z, z, r)
            k += 1


if __name__ == "__main__":

    main_call(create_arc_pocket)
