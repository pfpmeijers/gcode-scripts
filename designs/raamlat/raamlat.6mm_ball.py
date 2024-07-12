import sys

sys.path.append('../../')

import config
import presets.wood_6mm_ball

config.FEED_RATE = 1500
config.DEPTH_OF_CUT = 1
config.DEPTH_OF_CUT = config.MILL_DIAMETER / 2

from raamlat import *
from transformation import transformation
from basics import start, finish, retract
from bevelled_arc_pocket import create_bevelled_arc_pocket

start(tool=1)

DDZ = -1  # Z step size for bevel.

N = 3  # Duplicates
TY = 24  # Translation per duplicate

transformation.rotate(6)

for i in range(N):
    transformation.translate(ty=i * TY, relative=False)
    create_bevelled_arc_pocket(XL, XR, YFLT, YFRT, -H, 0, R, True, A, DDZ)
    retract(force=True)

finish()
