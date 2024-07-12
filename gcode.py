import config
from axis import Axis
from state import state
from transformation import transformation


def select_tool(tool: int = 1):
    print("M06 T{}".format(tool))


def update_state(x: float = None, y: float = None, z: float = None) -> bool:

    zl = state.pop_lazy_z_change(x, y)
    if zl is not None:
        goto_z(zl)
    return state.update(x, y, z)


def update_axis_state(axis: Axis, p: float) -> bool:

    if axis == Axis.X:
        return update_state(x=p)
    elif axis == Axis.Y:
        return update_state(y=p)
    elif axis == Axis.Z:
        return update_state(z=p)
    else:
        raise ValueError(f"Invalid axis: {p}")


def goto(axis: Axis, p: float):

    if axis == Axis.Z and state.is_below(p):
        mill(axis, p)
    else:
        if update_axis_state(axis, p):
            pt = transformation.transform_axis(axis, p)
            print("G00 {:s}{:.3f}".format(axis.name, pt))


def goto_xy(x: float, y: float):

    if update_state(x, y):
        xt, yt = transformation.transform_xy(x, y)
        print("G00 X{:.3f} Y{:.3f}".format(xt, yt))


def goto_z(z: float, lazy: bool = False):

    if lazy:
        state.lazy_z_change(z)
    else:
        goto(Axis.Z, z)


def mill(axis: Axis, p: float, feed_rate: int = None):

    if update_axis_state(axis, p):
        if feed_rate is None:
            feed_rate = config.PLUNGE_RATE if axis == Axis.Z else config.FEED_RATE
        pt = transformation.transform_axis(axis, p)
        print("G01 {:s}{:.3f} F{:.0f}".format(axis.name, pt, feed_rate))


def mill_xy(x: float, y: float, feed_rate: int = None):

    if update_state(x, y):
        if feed_rate is None:
            feed_rate = config.FEED_RATE
        xt, yt = transformation.transform_xy(x, y)
        print("G01 X{:.3f} Y{:.3f} F{:.0f}".format(xt, yt, feed_rate))


def mill_line(x: float, y: float, z: float, feed_rate: int = None):

    if update_state(x, y, z):
        if feed_rate is None:
            feed_rate = config.FEED_RATE
        xt, yt, zt = transformation.transform(x, y, z)
        print("G01 X{:.3f} Y{:.3f} Z{:.3f} F{:.0f}".format(xt, yt, zt, feed_rate))


def mill_arc(x: float, y: float, z: float, r: float, clockwise: bool = True, feed_rate: int = None):

    if update_state(x, y, z):
        if feed_rate is None:
            feed_rate = config.FEED_RATE
        xt, yt, zt = transformation.transform(x, y, z)
        rt = transformation.transform_r(r)
        print("{:s} X{:.3f} Y{:.3f} Z{:.3f} R{:.3f} F{:.0f}".format("G02" if clockwise else "G03", xt, yt, zt, rt, feed_rate))
