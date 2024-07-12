# Rates
SPINDLE_RPM = 12000
FEED_RATE = 1200     # Milling feed_rate rate, i.e., during x,y motion
MOVE_RATE = 2000
PLUNGE_RATE = 100    # Plunging feed_rate rate, i.e., during z motion downward

# Mill  properties
MILL_DIAMETER = 3
MILL_CORNER_DIAMETER = 0   # Use a mill corner radius for a ball end-mill, 0 for a flat end-mill

# Milling step sizes
WIDTH_OF_CUT = 3  # Horizontal step per lane that is cut
DEPTH_OF_CUT = 1  # Vertical step per horizontal plane that is cut
ANGLE_OF_CUT = 5  # Angle steps during creation of fillets

# Contour tabs
TAB_HEIGHT = 1
TAB_WIDTH = 1
TAB_DISTANCE = 10

# Retract height, assumed stock top is at 0
RETRACT_HEIGHT = 10

# Extra margin to avoid (not) hitting wall
MARGIN = 0.25
