from sys import stdout
from typing import TextIO

from Axis import Axis
from RouterState import RouterState
from Transformation import Transformation
from config.Config import Config


class GCode:

    def __init__(self, output_file: TextIO = None):

        self.router_state = RouterState()
        self.transformation = Transformation()
        self.output_file = output_file if output_file else stdout

        self._config = Config()

    def _write(self, s: str):

        self.output_file.write(s)
        self.output_file.write('\n')
        self.output_file.flush()

    def _update_state(self, x: float = None, y: float = None, z: float = None) -> bool:

        zl = self.router_state.pop_lazy_z_change(x, y)
        if zl is not None:
            self.goto_z(zl)
        return self.router_state.update(x, y, z)

    def _update_axis_state(self, axis: Axis, p: float) -> bool:

        if axis == Axis.X:
            return self._update_state(x=p)
        elif axis == Axis.Y:
            return self._update_state(y=p)
        elif axis == Axis.Z:
            return self._update_state(z=p)
        else:
            raise ValueError(f"Invalid axis: {p}")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: Config):
        if config.mill.index != self._config.mill.index:
            self._write("M06 T{}".format(config.mill.index))
        self._config = config

    @property
    def workpiece_top(self):
        return self.transformation.inverse_transform_z(self.config.workpiece.top)

    @property
    def retract_z(self):
        return self.transformation.inverse_transform_z(self.config.workpiece.top + self.config.milling.retract_height)

    @property
    def mill_diameter(self):
        return self.config.mill.diameter / abs(self.transformation.sxy)

    @property
    def mill_radius(self):
        return self.config.mill.radius / abs(self.transformation.sxy)

    @property
    def depth_of_cut(self):
        return self.config.milling.depth_of_cut / self.transformation.sz

    @property
    def width_of_cut(self):
        return self.config.milling.width_of_cut / abs(self.transformation.sxy)

    @property
    def milling_margin_xy(self):
        return self.config.milling.margin / abs(self.transformation.sxy)

    @property
    def milling_margin_z(self):
        return self.config.milling.margin / abs(self.transformation.sz)

    @property
    def tab_width(self):
        return self.config.tab.width / abs(self.transformation.sxy)

    @property
    def tab_height(self):
        return self.config.tab.height / self.transformation.sz

    @property
    def tab_distance(self):
        return self.config.tab.distance / abs(self.transformation.sxy)

    @property
    def feed_rate(self):
        return self.config.milling.feed_rate

    @property
    def plunge_rate(self):
        return self.config.milling.plunge_rate

    def get_ramp_rate(self, ramp_length: float) -> int:
        return min(self.feed_rate, int(ramp_length / self.depth_of_cut * self.plunge_rate))

    # TODO: Collapse actual movements above the workpiece-top into a single move to the position the top is reached.

    def goto(self, axis: Axis, p: float):

        if axis == Axis.Z and self.router_state.is_above(p) is True:  # Move downward
            if self.router_state.is_above(self.workpiece_top) is True:
                # Approach the workpiece top with full speed.
                z = max(p, self.workpiece_top)
                if self._update_axis_state(Axis.Z, z):
                    zt = self.transformation.transform_z(z)
                    self._write("G00 Z{:.2f}".format(zt))
            if self.router_state.is_above(p):
                self.plunge(p)
        else:
            if self._update_axis_state(axis, p):
                pt = self.transformation.transform_axis(axis, p)
                self._write("G00 {:s}{:.2f}".format(axis.name, pt))

    def goto_xy(self, x: float, y: float):

        if self._update_state(x, y):
            xt, yt = self.transformation.transform_xy(x, y)
            self._write("G00 X{:.2f} Y{:.2f}".format(xt, yt))

    def goto_z(self, z: float, lazy: bool = False):

        if lazy:
            self.router_state.lazy_z_change(z)
        else:
            self.goto(Axis.Z, z)

    def mill(self, axis: Axis, p: float, feed_rate: int = None):

        if feed_rate is None:
            feed_rate = self.plunge_rate if axis == Axis.Z else self.feed_rate
        if self._update_axis_state(axis, p):
            pt = self.transformation.transform_axis(axis, p)
            self._write("G01 {:s}{:.2f} F{}".format(axis.name, pt, feed_rate))

    def mill_line(self, x: float, y: float, z: float = None, feed_rate: int = None):

        if feed_rate is None:
            feed_rate = self.feed_rate
        if z is None:
            if self._update_state(x, y):
                xt, yt = self.transformation.transform_xy(x, y)
                self._write("G01 X{:.2f} Y{:.2f} F{}".format(xt, yt, feed_rate))
        else:
            if self._update_state(x, y, z):
                xt, yt, zt = self.transformation.transform(x, y, z)
                self._write("G01 X{:.2f} Y{:.2f} Z{:.2f} F{}".format(xt, yt, zt, feed_rate))

    def mill_arc(self, x: float, y: float, z: float, r: float, clockwise: bool = True, feed_rate: int = None):

        if self._update_state(x, y, z):
            if feed_rate is None:
                feed_rate = self.feed_rate
            xt, yt, zt = self.transformation.transform(x, y, z)
            rt = self.transformation.transform_r(r)
            self._write("{:s} X{:.2f} Y{:.2f} Z{:.2f} R{:.2f} F{}".format("G02" if clockwise else "G03", xt, yt, zt, rt, feed_rate))

    def retract(self, zr: float = None, force: bool = False):

        if zr is None:
            zr = self.retract_z
        if force:
            # First cancel a possibly outstanding lazy retract.
            self.cancel_retract()
        self.goto_z(zr, lazy=not force)

    def cancel_retract(self):

        self.goto_z(self.router_state.z)
        # This will remove a postponed z update to retract.
        # Note that it is always safe to call this function at any point in time,
        # since it actually does not change the position.

    def home_xy(self):

        self.retract(force=True)
        self.goto_xy(0, 0)

    def approach(self, x: float, y: float, z: float):

        self.goto_xy(x, y)
        self.goto_z(z)

    def plunge(self, z: float):

        self.mill(Axis.Z, z)

    def start(self, home_xy: bool = True):

        if home_xy:
            self.home_xy()
        else:
            self.retract(force=True)

    def finish(self):

        self.retract(force=True)

    def check_x_coordinate_constraints(self, xl: float, xr: float, mill_fit: bool = False):

        if xl > xr:
            raise ValueError("Left x coordinate must not be larger than right x coordinate")
        if mill_fit and xl > xr - self.config.mill.diameter:
            raise ValueError("Left x coordinate must not be larger than right x coordinate minus mill diameter")

    def check_y_coordinate_constraints(self, yf: float, yb: float, mill_fit: bool = False):

        if yf > yb:
            raise ValueError("Front y coordinate must not be larger than back y coordinate")
        if mill_fit and yf > yb - self.config.mill.diameter:
            raise ValueError("Front y coordinate must not be larger than back y coordinate minus mill diameter")

    @staticmethod
    def check_z_coordinate_constraints(zb: float, zt: float, zr: float = None):

        if zb > zt:
            raise ValueError("Bottom z coordinate must not be larger than top z coordinate")
        if zr is not None and zr <= zt:
            raise ValueError("Retract z coordinate must be above top z coordinate")

    def verify_bbox(self,
                    xl: float, xr: float, yf: float, yb: float, zb: float, zt: float, zr: float = None,
                    mill_fit: bool = False):

        self.check_x_coordinate_constraints(xl, xr, mill_fit)
        self.check_y_coordinate_constraints(yf, yb, mill_fit)
        self.check_z_coordinate_constraints(zb, zt, zr)

    def verify_position(self, x: float = None, y: float = None, z: float = None):
        if x is not None and x != self.router_state.x:
            raise ValueError(f"Router x position {self.router_state.x} does not match expectation {x}")
        if y is not None and y != self.router_state.y:
            raise ValueError(f"Router y position {self.router_state.y} does not match expectation {y}")
        if z is not None and z != self.router_state.z:
            raise ValueError(f"Router z position {self.router_state.z} does not match expectation {z}")
