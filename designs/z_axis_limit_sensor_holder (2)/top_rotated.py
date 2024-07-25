import sys; sys.path.append('../../')

from common import *
from GCode import select_tool
from cuts.rect_pocket import create_rect_pocket
from cuts.line_slot import create_x_line_slot, create_y_line_slot

X1 = -4
X2 = -6
X3 = -12

Y1 = 4
Y2 = 7.5
Y3 = 14.5
Y4 = 18.5
Y5 = 27.5

Z1 = -3.5
Z2 = -9.5
Z3 = -13.5

select_tool()

# P1
create_rect_pocket(xl=X3, xr=0 - M, yf=0, yb=Y4, zb=Z1, zt=0, contract_mill_radius=True, expand=D)

# P2
create_rect_pocket(xl=X3 - (D - M), xr=0 + (D - M), yf=Y1, yb=Y4 + D - M, zb=Z2, zt=Z1)

# P4
create_y_line_slot(x=X2,
                   yf=Y2, yb=Y3,
                   zb=Z3 - M, zt=Z2)

# P3
create_x_line_slot(xl=X3, xr=0,
                   y=Y4 + R,
                   zb=Z3, zt=Z1,
                   expand=D - M,
                   tabs=True)

# P5
create_y_line_slot(x=X3 - R,
                   yf=0, yb=Y4,
                   zb=Z3, zt=Z1,
                   expand=D - M,
                   tabs=True)
