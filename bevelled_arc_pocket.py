from math import ceil

import config
from gcode import mill_line
from state import state
from basics import cancel_retract
from line_slot import create_line_slot
from arc_pocket import create_arc_pocket
from bevelled_arc_slot import get_bevel_steps, create_bevelled_arc_slot
from utils.main import main_call


def create_bevelled_arc_pocket(xb: float, xe: float, yb: float, ye: float,
                               zb: float, zt: float,
                               r: float, clockwise: bool,
                               bevel_angle: float, ddz: float):

    # First do a coarse pocket with maximum depth steps.
    ddzc = -config.DEPTH_OF_CUT
    dxb0, dxe0, ddxb, ddxe, dyb0, dye0, ddyb, ddye, dz0, f = \
        get_bevel_steps(xb, xe, yb, ye, r, clockwise, zb, zt, bevel_angle, ddzc)

    xb2 = xb + dxb0 + f * ddxb
    xe2 = xe + dxe0 + f * ddxe
    yb2 = yb + dyb0 + f * ddyb
    ye2 = ye + dye0 + f * ddye
    for j in range(ceil(f + 1)):
        j = min(j, f)
        xb1 = xb + dxb0 + j * ddxb
        xe1 = xe + dxe0 + j * ddxe
        yb1 = yb + dyb0 + j * ddyb
        ye1 = ye + dye0 + j * ddye
        z = zt + dz0 + j * ddzc
        create_arc_pocket(xb1, xe1, yb1, ye1, r, clockwise, xb2, xe2, yb2, ye2, r, clockwise, z, z)
        # Mill a line to the next layer in order to avoid a retract. Go to the closest end arc's side, which is constant for all layers.
        cancel_retract()
        mill_line(*state.get_closest(((xb2, yb2), (xe2, ye2)))[1], z)

    # Then do the final bevel slot in fine steps.
    # Can be on max speed since only little is to be removed.
    org_feed_rate = config.FEED_RATE  # TODO: Consider a push/pop mechanism for this.
    config.FEED_RATE = config.MOVE_RATE
    create_bevelled_arc_slot(xb, xe, yb, ye, zb, zt, r, clockwise, bevel_angle, ddz)
    config.FEED_RATE = org_feed_rate


if __name__ == "__main__":

    main_call(create_bevelled_arc_pocket)
