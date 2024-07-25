import sys

sys.path.append('../../')

import config

config.TAB_HEIGHT = 2
config.TAB_DISTANCE = 50
config.TAB_WIDTH = 1
gcode.MILL.DEPTH_OF_CUT = 2

from cuts.basics import start, finish
from Transformation import transformation
from cuts.arc_slot import create_arc_slot
from cuts.line_slot import create_line_slot

# dimensions: 372 x 94 x 20

X0 = 2  # X offset
Y0 = 3  # Y offset
W = 380  # 365  # Width (left-right difference)
H = 18  # Height (top-bottom difference)
DY = 60  # Depth (front-back difference at any x position)
DYLR = 45  # 40  # Y difference between left and right side
R = 1600  # Radius of the arc
WLC = 0  # 60  # Width for cut-off at front-left side
DYLC = 0  # 13  # Y delta  for cut-off at front-left side
RM = config.MILL_DIAMETER / 2

XL = X0
XR = XL + W
YFL = Y0
YBL = Y0 + DY - DYLC
YBR = YBL + DYLR
YFR = YBR - DY

start(tool=2)

transformation.rotate_xy(a=6.5)

create_arc_slot(XL, XR, YBL, YBR, -H, 0, R, shift=RM)
create_line_slot(XR, XR, YBR, YFR, -H, 0, expand=RM, shift=-RM)
create_arc_slot(XR, XL + WLC, YFR, YFL, -H, 0, R, clockwise=False, shift=-RM)
# create_line_slot(XL + WLC, XL, YFL, YFL, -H, 0, expand=RM, shift=-RM)
create_line_slot(XL, XL, YFL, YBL, -H, 0, expand=RM, shift=-RM)

finish()