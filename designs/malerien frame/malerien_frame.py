import sys

sys.path.append('../../')

gcode.MILL.DEPTH_OF_CUT = 2

from cuts.basics import start, finish
from cuts.arc_slot import create_arc_slot
from cuts.line_slot import create_line_slot

# Text size
DXT = 250
DYT = 75

DY = 120
DX = 320
R = 30
XL = -(DX - DXT)/2
XR = XL + DX
YB = -(DY - DYT)/2
YT = YB + DY

ZB = -2

start(tool=2)

create_arc_slot(XL, XL + R, YB + R, YB, ZB, 0, R)
create_line_slot(XL + R, XR - R, YB, YB, ZB, 0)
create_arc_slot(XR - R, XR, YB, YB + R, ZB, 0, R)
create_line_slot(XR, XR, YB + R, YT - R, ZB, 0)
create_arc_slot(XR, XR - R, YT - R, YT, ZB, 0, R)
create_line_slot(XR - R, XL + R, YT, YT, ZB, 0)
create_arc_slot(XL + R, XL, YT, YT - R, ZB, 0, R)
create_line_slot(XL, XL, YT - R, YB + R, ZB, 0)

finish()
