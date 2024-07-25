import sys

sys.path.append('../../')

import config

config.FEED_RATE = 1500
gcode.MILL.DEPTH_OF_CUT = 2

from raamlat import *
from Transformation import transformation
from cuts.basics import start, finish
from cuts.arc_slot import create_arc_slot
from cuts.line_slot import create_line_slot

start(tool=2)

TX = 28
for i in range(2):
    transformation.translate(ty=i * TX, relative=False)
    create_line_slot(XL, XL, YFLB, YBLB, -H, 0, shift=-RM)
    create_arc_slot(XL, XR, YBLB, YBRB, -H, 0, R, shift=RM)
    create_line_slot(XR, XR, YFRB, YBRB, -H, 0, shift=RM)

finish()
