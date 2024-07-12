from math import cos, radians

import config

RM = config.MILL_DIAMETER / 2  # Mill radius

# Dimensions: 360 x 60 x 20

X0 = 3  # X offset
Y0 = 1  # Y offset
W = 355  # Width (left-right difference)
H = 19  # Height (top-bottom difference)
DYT = 10  # Y difference (depth; i.e. along y-axis) at top
DYLR = 40  # Y difference between left and right front (or back) side
A = 67.5  # Bevel angle
R = 1600  # Radius of the arc

XL = X0
XR = XL + W

DYFB = DYT + cos(radians(A)) * H  # Y difference between front and back, i.e. y difference at bottom.
YFLB = Y0
YBLB = YFLB + DYFB
YBRB = YBLB + DYLR
YFRB = YFLB + DYLR
YFLT = YBLB - DYT
YFRT = YFLT + DYLR
YBRT = YFRT + DYT
