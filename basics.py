import config
from state import state
from gcode import select_tool, goto_xy, goto_z, mill
from axis import Axis


def start(tool: int = 1):
    select_tool(tool)


def retract(zr: float = None, force: bool = False):
    if zr is None:
        zr = config.RETRACT_HEIGHT
    if force:
        # First cancel a possible lazy retract.
        cancel_retract()
    goto_z(zr, lazy=not force)


def cancel_retract():
    goto_z(state.z)
    # This will remove a postponed z update to retract.
    # Note that it is always safe to call this function at any point in time, since it actually does not change the position.


def approach(x: float, y: float, z: float):
    goto_xy(x, y)
    goto_z(z)


def plunge(z: float):
    mill(Axis.Z, z, config.PLUNGE_RATE)


def finish():
    goto_z(config.RETRACT_HEIGHT)