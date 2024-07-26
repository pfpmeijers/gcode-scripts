from GCode import GCode
from cuts.rect_pocket import create_rect_pocket

gcode = GCode()
gcode.config.mill.width_of_cut = 10

WIDTH = 330
DEPTH = 394

gcode.start()
create_rect_pocket(gcode, xl=0, xr=WIDTH, yf=0, yb=DEPTH, zb=-1, zt=0)
gcode.finish()

